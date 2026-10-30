"""Offline failure/drift/side-effect regressions for the formal watcher."""
import copy
import datetime
import importlib.util
import json
from pathlib import Path
import ssl
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

SPEC = importlib.util.spec_from_file_location("or_watch", Path(__file__).resolve().parents[1] / "tools/or_watch.py")
watch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(watch)
NOW = datetime.datetime(2026, 10, 30, 10, 0, tzinfo=watch.KST)


def form():
    return {"invitations": [{"id": "NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission",
                            "tmdate": 1, "duedate": 100, "expdate": 200,
                            "edit": {"note": {"license": "CC BY-SA 4.0", "content": {
                                "title": {"value": {"param": {"type": "string"}}},
                                "leaderboard_submission_ids": {"value": {"param": {"type": "string[]"}}},
                                "later": {"value": {"param": {"type": "string", "optional": True}}}}}}}], "count": 1}


class WatchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.inv = form()
        self.phases = {"phases": [{"id": 30038, "name": "Validation", "start": "2026-10-01T00:00:00Z",
                                   "end": "2026-11-01T11:55:00Z", "status": "Current"}]}
        self.heads = {watch.SITE: "a" * 40, watch.BY: "b" * 40}
        self.failures = {}

    @property
    def fields(self):
        return self.inv["invitations"][0]["edit"]["note"]["content"]

    def run_poll(self, patch_text="+new rule\n", diff_error=None):
        def get(url):
            if url in self.failures:
                raise self.failures[url]
            return json.dumps(self.inv if url == watch.INV else self.phases).encode()

        def head(url):
            if url in self.failures:
                raise self.failures[url]
            return self.heads[url]

        # Any process besides the explicitly stubbed public readers is a defect.
        with patch.object(watch, "get", side_effect=get), patch.object(watch, "head", side_effect=head), \
                patch.object(watch, "site_diff", side_effect=diff_error, return_value=patch_text), \
                patch.object(watch.subprocess, "run", side_effect=AssertionError("unexpected external process")) as external:
            result, code = watch.run_watch(self.root, now=NOW)
            external.assert_not_called()
        self.assertEqual(result["note_mutations"], 0)
        self.assertFalse(result["scheduled"])
        return result, code

    def seed(self):
        result, code = self.run_poll()
        self.assertEqual((result["result"], code), ("SEEDED", 0))
        return (self.root / "watch_state.json").read_bytes()

    def test_seed_then_unchanged(self):
        self.seed()
        result, code = self.run_poll()
        self.assertEqual((result["result"], code), ("NO_CHANGE", 0))
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["baseline_advanced"])

    def test_invitation_http503_does_not_stop_site_or_phase(self):
        baseline = self.seed()
        self.failures[watch.INV] = watch.WatchError("HTTP 503")
        self.heads[watch.SITE] = "c" * 40
        self.phases["phases"][0]["status"] = "Previous"
        result, code = self.run_poll()
        self.assertEqual((result["result"], code), ("PARTIAL_ERROR", 2))
        self.assertEqual(result["sources"]["codabench_phase"]["status"], "OK")
        self.assertTrue(any("SITE_DIFF_" in name for name in result["files"]))
        self.assertTrue(any("CODABENCH_PHASE_CHANGE_" in name for name in result["files"]))
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)
        self.assertFalse(result["baseline_advanced"])

    def test_git_timeout_does_not_hide_invitation_change(self):
        baseline = self.seed()
        self.fields["rules_no_duplicates"] = {"value": {"param": {"type": "string", "enum": ["Factual statement"]}}}
        self.inv["invitations"][0]["tmdate"] = 2
        self.failures[watch.BY] = subprocess.TimeoutExpired("git", 30)
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertEqual(result["sources"]["byeolki_head"]["status"], "ERROR")
        delta = json.loads((self.root / "INVITATION_DIFF_2.json").read_text())
        self.assertEqual(delta["required_added"], ["rules_no_duplicates"])
        self.assertTrue(delta["requires_payload_review"])
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)

    def test_phase_error_is_not_written_over_successful_phase(self):
        baseline = self.seed()
        self.failures[watch.CB] = watch.WatchError("HTTP 503")
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertEqual(result["sources"]["codabench_phase"]["error"], "HTTP 503")
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)

    def test_all_sources_failed_never_create_a_success_baseline(self):
        self.failures = {url: watch.WatchError("unavailable") for url in (watch.INV, watch.CB, watch.SITE, watch.BY)}
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertEqual(len(result["errors"]), 4)
        self.assertFalse((self.root / "watch_state.json").exists())

    def test_added_const_and_optional_are_not_required(self):
        old = watch.invitation(form())
        self.fields["venue"] = {"value": {"param": {"const": "fixed"}}}
        self.fields["extra"] = {"value": {"param": {"type": "string", "optional": True}}}
        delta = watch.invitation_diff(old, watch.invitation(self.inv))
        self.assertEqual(delta["required_added"], [])

    def test_optional_to_required_and_type_change_are_explicit(self):
        old = watch.invitation(copy.deepcopy(self.inv))
        del self.fields["later"]["value"]["param"]["optional"]
        self.fields["leaderboard_submission_ids"]["value"]["param"]["type"] = "string"
        delta = watch.invitation_diff(old, watch.invitation(self.inv))
        self.assertEqual(delta["became_required"], ["later"])
        self.assertEqual(delta["type_changed"]["leaderboard_submission_ids"], {"before": "string[]", "after": "string"})
        self.assertTrue(delta["requires_payload_review"])

    def test_same_tmdate_schema_change_keeps_old_snapshot_bytes(self):
        baseline = self.seed()
        state = json.loads(baseline)
        old_path = self.root / state["inv_file"]
        old_raw = old_path.read_bytes()
        self.fields["title"]["description"] = "New requirement"
        self.failures[watch.CB] = watch.WatchError("unavailable")
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertTrue((self.root / "INVITATION_DIFF_1.json").exists())
        self.assertEqual(old_path.read_bytes(), old_raw)
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)
        self.assertEqual(len(list(self.root.glob("invitation_*.json"))), 2)

    def test_deleted_field_deadline_and_license_are_recorded(self):
        old = watch.invitation(copy.deepcopy(self.inv))
        del self.fields["later"]
        self.inv["invitations"][0]["duedate"] = 150
        self.inv["invitations"][0]["edit"]["note"]["license"] = "Changed"
        delta = watch.invitation_diff(old, watch.invitation(self.inv))
        self.assertEqual(delta["removed"], ["later"])
        self.assertIn("duedate", delta["dates_changed"])
        self.assertTrue(delta["license_changed"])

    def test_required_enum_change_requests_payload_review(self):
        self.fields["rule"] = {"value": {"param": {"type": "string", "enum": ["Before"]}}}
        old = watch.invitation(copy.deepcopy(self.inv))
        self.fields["rule"]["value"]["param"]["enum"] = ["After"]
        delta = watch.invitation_diff(old, watch.invitation(self.inv))
        self.assertEqual(delta["required_changed"], ["rule"])
        self.assertTrue(delta["requires_payload_review"])

    def test_malformed_live_phase_cannot_poison_baseline(self):
        baseline = self.seed()
        self.phases["phases"][0]["end"] = 17
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertEqual(result["sources"]["codabench_phase"]["status"], "ERROR")
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)

    def test_malformed_baseline_is_reported_without_replacing_it(self):
        path = self.root / "watch_state.json"
        path.write_bytes(b"{broken")
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertEqual(path.read_bytes(), b"{broken")
        self.assertTrue(all(value["status"] == "OK" for value in result["sources"].values()))

    def test_missing_invitation_snapshot_does_not_block_healthy_by_diff(self):
        baseline = self.seed()
        (self.root / json.loads(baseline)["inv_file"]).unlink()
        self.heads[watch.BY] = "d" * 40
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertTrue(any("BYEOLKI_HEAD_CHANGE_" in name for name in result["files"]))
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)

    def test_bad_snapshot_name_and_tmdate_cannot_escape_output_root(self):
        self.seed()
        state = json.loads((self.root / "watch_state.json").read_text())
        state["inv_file"] = "../../secret.txt"
        (self.root / "watch_state.json").write_text(json.dumps(state))
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.inv["invitations"][0]["tmdate"] = "../../escape"
        result, code = self.run_poll()
        self.assertEqual(code, 2)
        self.assertEqual(result["sources"]["invitation"]["status"], "ERROR")
        self.assertFalse(any("escape" in path.name for path in self.root.iterdir()))

    def test_failed_site_patch_is_explicit_and_does_not_advance_baseline(self):
        baseline = self.seed()
        self.heads[watch.SITE] = "c" * 40
        result, code = self.run_poll(diff_error=watch.WatchError("git failed"))
        self.assertEqual(code, 2)
        body = Path(result["files"][0]).read_text()
        self.assertIn("INDEX_DIFF_UNAVAILABLE", body)
        self.assertNotIn("diff acquired successfully", body)
        self.assertEqual((self.root / "watch_state.json").read_bytes(), baseline)

    def test_successful_empty_patch_is_distinct_from_failed_patch(self):
        self.seed()
        self.heads[watch.SITE] = "c" * 40
        result, code = self.run_poll(patch_text="")
        self.assertEqual((result["result"], code), ("CHANGED", 3))
        self.assertIn("index.html has no changes", Path(result["files"][0]).read_text())

    def test_site_patch_is_not_silently_truncated(self):
        self.seed()
        self.heads[watch.SITE] = "c" * 40
        patch_text = "+line\n" * 5000 + "+FINAL_RULE\n"
        result, code = self.run_poll(patch_text=patch_text)
        self.assertEqual(code, 3)
        self.assertIn(patch_text, Path(result["files"][0]).read_text())

    def test_legacy_successful_phase_end_is_upgraded(self):
        self.seed()
        path = self.root / "watch_state.json"
        state = json.loads(path.read_text())
        state["codabench_phase"] = self.phases["phases"][0]["end"]
        path.write_text(json.dumps(state))
        result, code = self.run_poll()
        self.assertEqual(code, 0)
        self.assertIsInstance(json.loads(path.read_text())["codabench_phase"], dict)

    def test_legacy_failed_or_malformed_phase_baseline_is_not_silently_adopted(self):
        self.seed()
        path = self.root / "watch_state.json"
        state = json.loads(path.read_text())
        for bad in ("ERR 503", "none-current", "nonsense", {"id": 30038}, 17):
            with self.subTest(bad=bad):
                state["codabench_phase"] = bad
                path.write_text(json.dumps(state))
                before = path.read_bytes()
                result, code = self.run_poll()
                self.assertEqual(code, 2)
                self.assertEqual(path.read_bytes(), before)

    def test_atomic_replace_failure_preserves_old_file(self):
        path = self.root / "watch_state.json"
        path.write_bytes(b"original")
        with patch.object(watch.os, "replace", side_effect=OSError("disk unavailable")):
            with self.assertRaises(OSError):
                watch.atomic_json(path, {"new": True})
        self.assertEqual(path.read_bytes(), b"original")
        self.assertEqual(list(self.root.glob(".watch_state.json.*")), [])

    def test_cutoff_performs_no_network_or_baseline_write(self):
        target = self.root / "not-created"
        with patch.object(watch, "acquire") as acquire:
            result, code = watch.run_watch(target, now=watch.CUTOFF)
        acquire.assert_not_called()
        self.assertEqual((result["result"], code), ("STOPPED_CUTOFF", 0))
        self.assertFalse(target.exists())

    def test_http503_is_explicit_without_insecure_fallback(self):
        error = urllib.error.HTTPError(watch.INV, 503, "unavailable", None, None)
        with patch.object(watch.urllib.request, "urlopen", side_effect=error), patch.object(watch.subprocess, "run") as run:
            with self.assertRaisesRegex(watch.WatchError, "HTTP 503"):
                watch.get(watch.INV)
        run.assert_not_called()

    def test_certificate_fallback_verifies_tls_and_has_finite_bounds(self):
        error = urllib.error.URLError(ssl.SSLCertVerificationError("local CA issue"))
        response = subprocess.CompletedProcess([], 0, stdout=b"{}", stderr=b"")
        with patch.object(watch.urllib.request, "urlopen", side_effect=error), \
                patch.object(watch.subprocess, "run", return_value=response) as run:
            self.assertEqual(watch.get(watch.INV), b"{}")
        args, kwargs = run.call_args
        self.assertNotIn("--insecure", args[0])
        self.assertNotIn("-k", args[0])
        self.assertIn("--max-time", args[0])
        self.assertEqual(kwargs["timeout"], 23)

    def test_git_failure_is_checked_and_credentials_are_disabled(self):
        response = subprocess.CompletedProcess([], 128, stdout="", stderr="failure")
        with patch.object(watch.subprocess, "run", return_value=response) as run:
            with self.assertRaises(watch.WatchError):
                watch.head(watch.SITE)
        args, kwargs = run.call_args
        self.assertIn("credential.helper=", args[0])
        self.assertEqual(kwargs["env"]["GIT_TERMINAL_PROMPT"], "0")
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["timeout"], 30)

    def test_failed_git_diff_cannot_be_returned_as_empty_success(self):
        (self.root / "site_repo").mkdir()
        def git(args, timeout=30):
            if "remote" in args:
                return watch.SITE + "\n"
            if "diff" in args:
                raise watch.WatchError("git exit 128")
            return ""
        with patch.object(watch, "git", side_effect=git) as called:
            with self.assertRaises(watch.WatchError):
                watch.site_diff(self.root, "a" * 40, "c" * 40)
        diff_args = [call.args[0] for call in called.call_args_list if "diff" in call.args[0]][0]
        self.assertIn("--no-ext-diff", diff_args)
        self.assertEqual(diff_args[-4:], ["a" * 40, "c" * 40, "--", "index.html"])


if __name__ == "__main__":
    unittest.main()
