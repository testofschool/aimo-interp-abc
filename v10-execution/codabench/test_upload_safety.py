"""Invented data only. No auth/network, official receipt or outcome fixtures."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[2] / "tools/codabench_v101_upload.py"
spec = importlib.util.spec_from_file_location("uploader", SOURCE)
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.bundle = {"order": 1, "name": "invented.zip", "bytes": 123, "sha256": "a" * 64}

    def test_filename_without_task_holds(self):
        with self.assertRaisesRegex(u.Hold, "TASK_UNVERIFIED"):
            u.duplicate_matches([{"id": 999, "filename": "invented.zip"}], self.bundle)

    def test_unique_filename_small_linkage_is_not_sha_proof(self):
        row = {"id": 999, "filename": "invented.zip", "task": u.TASK}
        self.assertEqual(u.duplicate_matches([row], self.bundle), [row])
        row["file_sha256"] = "b" * 64
        with self.assertRaisesRegex(u.Hold, "FILENAME_HASH"):
            u.duplicate_matches([row], self.bundle)

    def test_strong_match_requires_small_task(self):
        row = {"id": 999, "filename": "different.zip", "sha256": "a" * 64,
               "task": {"id": 36237}}
        with self.assertRaisesRegex(u.Hold, "TASK_UNVERIFIED"):
            u.duplicate_matches([row], self.bundle)
        row["task"]["id"] = u.TASK
        self.assertEqual(u.duplicate_matches([row], self.bundle), [row])

    def test_name_size_match_and_multiple_match_holds(self):
        row = {"id": 999, "filename": "invented.zip", "file_size": 123,
               "task": {"id": u.TASK}}
        self.assertEqual(u.duplicate_matches([row], self.bundle), [row])
        with self.assertRaisesRegex(u.Hold, "MULTIPLE_EXISTING_MATCHES"):
            u.duplicate_matches([row, dict(row, id=1000)], self.bundle)

    def test_identity_exact_user_and_not_admin(self):
        def body(user):
            return "user: JSON.parse(" + json.dumps(json.dumps(user)) + ")"
        self.assertEqual(u.identity_from_html(body({"logged_in": True,
                         "username": "testofschool", "id": 999}))["username"], "testofschool")
        for user in [{"logged_in": False}, {"logged_in": True, "username": "other"},
                     {"logged_in": True, "username": "testofschool", "is_staff": True}]:
            with self.assertRaises(u.Hold):
                u.identity_from_html(body(user))

    def test_receipt_drops_secrets_urls_and_arbitrary_logs(self):
        native = {"id": 999, "owner": "testofschool", "status": "Finished",
                  "secret": "synthetic-secret", "sassy_url": "https://invalid.example/secret",
                  "status_details": "synthetic private log", "password": "invented",
                  "scores": [{"score": "0.5", "column_key": "accuracy", "url": "https://invalid.example"}]}
        clean = json.dumps(u.receipt(native))
        self.assertNotIn("secret", clean)
        self.assertNotIn("https", clean)
        self.assertNotIn("password", clean)
        self.assertNotIn("private log", clean)
        self.assertIn('"score": "0.5"', clean)

    def test_uncertain_mutation_is_persisted_and_not_repeated(self):
        class Fake:
            calls = 0
            def request(self, *args, **kwargs):
                self.calls += 1
                raise u.Hold("NETWORK_UNCERTAINTY_POST")
        with tempfile.TemporaryDirectory() as directory, patch.object(u, "JOURNAL", Path(directory) / "journal.json"):
            entry = {"state": "LOCAL_READY"}
            journal = {"bundles": [entry]}
            client = Fake()
            with self.assertRaises(u.Hold):
                u.mutate(client, journal, entry, "SUBMISSION_CREATE", "POST", "/api/submissions/")
            self.assertEqual(client.calls, 1)
            self.assertEqual(json.loads(u.JOURNAL.read_text())["bundles"][0]["state"],
                             "SUBMISSION_CREATE_UNCERTAIN")

    def test_deadline_exact_boundary(self):
        u.deadline(u.TARGET - u.dt.timedelta(seconds=1))
        with self.assertRaises(u.Hold):
            u.deadline(u.TARGET)

    def test_own_list_count_and_scope_completeness(self):
        client = object.__new__(u.Client)
        good = {"id": 999, "owner": u.USER, "phase": u.PHASE}
        for page, reason in [({"count": 1, "next": None, "results": []}, "COUNT_MISMATCH"),
                             ({"count": 2, "next": None, "results": [good, good]}, "DUPLICATE"),
                             ({"count": 1, "next": None, "results": [dict(good, owner="other")]}, "SCOPE_MISMATCH")]:
            client.get_json = lambda path, page=page: page
            with self.assertRaisesRegex(u.Hold, reason):
                client.own_submissions()
        client.get_json = lambda path: {"count": 1, "next": None, "results": [good]}
        self.assertEqual(client.own_submissions(), [good])

    def test_pending_restart_holds_before_mutations(self):
        records = [dict(self.bundle, order=i, path="invented-%d.zip" % i) for i in (1, 2, 3)]
        journal = {"prereg_commit": u.PREREG,
                   "bundles": [dict(r, state="SUBMISSION_CREATE_UNCERTAIN") for r in records]}
        class Fake:
            def login(self): return {"username": "testofschool", "id": 999}
            def get_json(self, path):
                return {"phases": [{"id": u.PHASE, "end": "2026-11-01T11:55:00Z",
                                   "tasks": [{"id": u.TASK}]}]}
            def own_submissions(self): return []
            def close(self): pass
            def request(self, *args, **kwargs):
                raise AssertionError("A pending restart must never mutate")
        with tempfile.TemporaryDirectory() as directory, patch.object(u, "JOURNAL", Path(directory) / "journal.json"), \
             patch.object(u, "SCORES", Path(directory) / "scores.json"), \
             patch.object(u, "Client", Fake), patch.object(u.sys.stdin, "isatty", return_value=True), \
             patch.object(u, "deadline"):
            u.persist(u.JOURNAL, journal)
            with self.assertRaisesRegex(u.Hold, "PRIOR_MUTATION_REQUIRES_MANUAL_RECONCILIATION"):
                u.run(records)


if __name__ == "__main__":
    unittest.main()
