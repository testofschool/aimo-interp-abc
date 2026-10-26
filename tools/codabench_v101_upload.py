#!/usr/bin/env python3
"""Bounded, interactive Codabench H1 uploader. --check-local never uses network.

Password entry belongs only in a local TTY. No credentials, authenticated HTML,
cookies or signed storage URLs are written to disk. Uncertain mutations HOLD.
"""
import argparse
import datetime as dt
import fcntl
import getpass
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import parse_qs, urljoin, urlparse
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.codabench.org"
USER, COMPETITION, PHASE, TASK = "testofschool", 16180, 30038, 36241
PREREG = "773b39e1a2ca0f1c4001e0ae1459e7d567e56c80"
TARGET = dt.datetime(2026, 11, 1, 11, 0, tzinfo=dt.timezone.utc)
PHASE_END = dt.datetime(2026, 11, 1, 11, 55, tzinfo=dt.timezone.utc)
JOURNAL = ROOT / "v9-execution/official-upload-journal.json"
SCORES = ROOT / "v9-execution/SCORES.json"
BUNDLES = [
    ("v9-execution/upload-order/solution-always-true-small.zip", 519,
     "4a3718e38f915a49ab1a74c5d99f45ee2814fb2845ebb1da3cb0daaa0b249e0a"),
    ("v9-execution/upload-order/solution-text-length-control-small.zip", 1387,
     "30e59012351a09c5f413376cf600678fe9cd62fe990042f2b43661c3219cbbfd"),
    ("v9-execution/bundle3-trained-probe-small.zip", 27662500,
     "852fff17372ebdcf967549a4270339a2e792372c1b5496da968b2df884ccc67b"),
]
TERMINAL = {"Finished", "Failed", "Cancelled"}


class Hold(Exception):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp():
    return now().isoformat()


def persist(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def deadline(at=None):
    if (at or now()) >= min(TARGET, PHASE_END):
        raise Hold("UPLOAD_DEADLINE_REACHED: target 2026-11-01 20:00 KST")


def check_local():
    records = []
    for order, (relative, size, digest) in enumerate(BUNDLES, 1):
        path = ROOT / relative
        if path.stat().st_size != size:
            raise Hold("ZIP_SIZE_MISMATCH: bundle " + str(order))
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise Hold("ZIP_SHA256_MISMATCH: bundle " + str(order))
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if names.count("small.txt") != 1 or archive.read("small.txt") != b"":
                raise Hold("SMALL_TRACK_MARKER_MISMATCH: bundle " + str(order))
            if archive.testzip() is not None:
                raise Hold("ZIP_CRC_MISMATCH: bundle " + str(order))
        records.append({"order": order, "name": path.name, "path": relative,
                        "bytes": size, "sha256": digest})
    code = subprocess.run(["git", "merge-base", "--is-ancestor", PREREG, "HEAD"],
                          cwd=ROOT, capture_output=True).returncode
    if code:
        raise Hold("PREREG_COMMIT_NOT_ANCESTOR")
    for relative in ["v9-execution/PREREG.md", "v9-execution/paired_protocol.py"]:
        blob = subprocess.run(["git", "show", PREREG + ":" + relative],
                              cwd=ROOT, capture_output=True, check=True).stdout
        if (ROOT / relative).read_bytes() != blob:
            raise Hold("PREREG_WORKTREE_CHANGED: " + relative)
    return records


def identity_from_html(text):
    match = re.search(r'user\s*:\s*JSON\.parse\(("(?:\\.|[^"\\])*")\)', text)
    if not match:
        raise Hold("AUTH_IDENTITY_MARKER_MISSING")
    try:
        user = json.loads(json.loads(match.group(1)))
    except (ValueError, TypeError):
        raise Hold("AUTH_IDENTITY_INVALID")
    if user.get("logged_in") is not True or user.get("username") != USER:
        raise Hold("AUTH_IDENTITY_MISMATCH: require testofschool")
    if user.get("is_staff") or user.get("is_superuser"):
        raise Hold("ADMIN_SESSION_NOT_ALLOWED_FOR_OWN_ONLY_LIST")
    return {"username": USER, "id": user.get("id")}


def duplicate_matches(rows, bundle):
    """Unique filename linkage is allowed; never call that a verified server SHA."""
    strong = []
    for row in rows:
        data = row.get("data") if isinstance(row.get("data"), dict) else {}
        digest = row.get("sha256", row.get("file_sha256", data.get("sha256")))
        size = row.get("file_size", data.get("file_size"))
        name = row.get("filename", data.get("file_name"))
        if digest is not None and name == bundle["name"] and digest != bundle["sha256"]:
            raise Hold("AMBIGUOUS_EXISTING_FILENAME_HASH: bundle " + str(bundle["order"]))
        if digest == bundle["sha256"]:
            if task_id(row) != TASK:
                raise Hold("EXISTING_MATCH_TASK_UNVERIFIED")
            strong.append(row)
        elif name == bundle["name"]:
            if task_id(row) != TASK:
                raise Hold("EXISTING_MATCH_TASK_UNVERIFIED")
            if size is not None and size != bundle["bytes"]:
                raise Hold("EXISTING_FILENAME_SIZE_MISMATCH")
            strong.append(row)
    if len(strong) > 1:
        raise Hold("MULTIPLE_EXISTING_MATCHES: bundle " + str(bundle["order"]))
    return strong


def task_id(row):
    task = row.get("task")
    return task.get("id") if isinstance(task, dict) else task if type(task) is int else None


def match_evidence(row, bundle):
    data = row.get("data") if isinstance(row.get("data"), dict) else {}
    digest = row.get("sha256", row.get("file_sha256", data.get("sha256")))
    size = row.get("file_size", data.get("file_size"))
    return "native SHA field matches local ZIP" if digest == bundle["sha256"] else (
        "unique filename and native size match" if size == bundle["bytes"] else
        "unique filename with owner/phase/Small task; server bytes unverified")


def chronology(journal, entry, row, external=False):
    if entry["order"] != 3:
        return
    committed = dt.datetime.fromtimestamp(int(subprocess.check_output(
        ["git", "show", "-s", "--format=%ct", PREREG], cwd=ROOT, text=True).strip()), dt.timezone.utc)
    record = {"prereg_commit": PREREG, "prereg_commit_time_utc": committed.isoformat(),
              "native_submission_created_when": row.get("created_when"), "status": "UNKNOWN",
              "source": "git commit timestamp compared with native owned submission.created_when"}
    try:
        submitted = dt.datetime.fromisoformat(row["created_when"].replace("Z", "+00:00"))
        if submitted.tzinfo is None:
            raise ValueError()
        record["status"] = "PREREG_PRECEDES_SUBMISSION" if committed < submitted else "SUBMISSION_NOT_AFTER_PREREG"
        if committed >= submitted:
            journal["exploratory"] = True
    except (KeyError, ValueError, TypeError, AttributeError):
        pass
    if external:
        record["prior_exposure"] = "UNKNOWN: preexisting official receipt outside this journal"
        record["classification"] = "EXPLORATORY_OR_UNVERIFIED"
        journal["exploratory_or_unverified"] = True
    else:
        record["classification"] = "EXPLORATORY" if journal.get("exploratory") else (
            "PREREG_CHRONOLOGY_VERIFIED" if record["status"] == "PREREG_PRECEDES_SUBMISSION" else "UNKNOWN")
    entry["prereg_chronology"] = record


def receipt(row):
    """Whitelist fields only; never serialize secret, arbitrary logs or URLs."""
    result = {k: row[k] for k in ["id", "pk", "phase", "owner", "status",
              "created_when", "parent", "children", "has_children"] if k in row}
    if isinstance(row.get("filename"), str):
        result["filename"] = Path(row["filename"]).name
    if isinstance(row.get("data"), str):
        try:
            result["dataset_key"] = str(uuid.UUID(row["data"]))
        except ValueError:
            pass
    task = row.get("task")
    if isinstance(task, dict):
        result["task"] = {k: task[k] for k in ["id", "name"] if k in task}
    elif isinstance(task, int):
        result["task"] = {"id": task}
    result["scores"] = [{k: score[k] for k in ["id", "index", "score",
                          "column_key", "precision", "is_primary"] if k in score}
                         for score in row.get("scores", []) if isinstance(score, dict)]
    return result


class Client:
    def __init__(self):
        import requests
        self.requests = requests
        self.session = requests.Session()
        self.session.trust_env = False
        adapter = requests.adapters.HTTPAdapter(max_retries=0)
        self.session.mount("https://", adapter)

    def close(self):
        self.session.cookies.clear()
        self.session.close()

    def request(self, method, path, **kwargs):
        target = urljoin(BASE, path)
        if urlparse(target).netloc != urlparse(BASE).netloc or urlparse(target).scheme != "https":
            raise Hold("NON_PLATFORM_API_TARGET")
        headers = kwargs.pop("headers", {})
        if method not in {"GET", "HEAD"}:
            deadline()
            token = self.session.cookies.get("csrftoken")
            if not token:
                raise Hold("CSRF_COOKIE_MISSING")
            headers.update({"X-CSRFToken": token, "Referer": BASE + "/"})
        try:
            return self.session.request(method, target, headers=headers, timeout=(15, 60),
                                        allow_redirects=False, **kwargs)
        except self.requests.RequestException:
            raise Hold("NETWORK_UNCERTAINTY_" + method)

    def get_json(self, path):
        response = self.request("GET", path)
        if response.status_code != 200:
            raise Hold("GET_FAILED_HTTP_" + str(response.status_code))
        try:
            return response.json()
        except ValueError:
            raise Hold("GET_INVALID_JSON")

    def login(self):
        response = self.request("GET", "/accounts/login/")
        if response.status_code != 200:
            raise Hold("LOGIN_PAGE_FAILED_HTTP_" + str(response.status_code))
        match = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', response.text)
        if not match:
            raise Hold("LOGIN_CSRF_FORM_MISSING")
        csrf = html.unescape(match.group(1))
        if not sys.stdin.isatty():
            raise Hold("LOCAL_TTY_REQUIRED: no password was read")
        password = getpass.getpass("Codabench testofschool password (local terminal only): ")
        try:
            if not password:
                raise Hold("EMPTY_PASSWORD")
            response = self.request("POST", "/accounts/login/", data={
                "username": USER, "password": password, "csrfmiddlewaretoken": csrf})
        finally:
            del password
        if response.status_code not in {200, 302, 303}:
            raise Hold("LOGIN_FAILED_HTTP_" + str(response.status_code))
        location = response.headers.get("Location", "/")
        if urlparse(urljoin(BASE, location)).netloc != urlparse(BASE).netloc:
            raise Hold("LOGIN_EXTERNAL_REDIRECT")
        response = self.request("GET", "/")
        if response.status_code != 200:
            raise Hold("AUTH_HOME_FAILED")
        return identity_from_html(response.text)

    def own_submissions(self):
        path = "/api/submissions/?phase=%d&page=1&page_size=100" % PHASE
        rows, seen, ids, total = [], set(), set(), None
        while path:
            parsed = urlparse(urljoin(BASE, path))
            if parsed.path != "/api/submissions/" or parse_qs(parsed.query).get("phase") != [str(PHASE)]:
                raise Hold("PAGINATION_SCOPE_MISMATCH")
            if path in seen:
                raise Hold("PAGINATION_LOOP")
            seen.add(path)
            page = self.get_json(path)
            if not isinstance(page, dict) or type(page.get("count")) is not int or page["count"] < 0 or "next" not in page:
                raise Hold("OWN_LIST_COMPLETENESS_UNVERIFIED")
            batch = page.get("results")
            if total is None:
                total = page["count"]
            if not isinstance(batch, list) or page["count"] != total:
                raise Hold("OWN_LIST_SCHEMA_MISMATCH")
            for row in batch:
                if row.get("owner") != USER or row.get("phase") != PHASE:
                    raise Hold("OWN_LIST_SCOPE_MISMATCH")
                if type(row.get("id")) is not int or row["id"] in ids:
                    raise Hold("OWN_LIST_DUPLICATE_OR_INVALID_ID")
                ids.add(row["id"])
            rows.extend(batch)
            path = page.get("next")
            if len(seen) > 100:
                raise Hold("PAGINATION_BOUND_EXCEEDED")
        if len(rows) != total:
            raise Hold("OWN_LIST_COUNT_MISMATCH")
        return rows


def mutate(client, journal, entry, state, method, path, **kwargs):
    entry.update({"state": state + "_PENDING", "intent_at_utc": stamp()})
    persist(JOURNAL, journal)
    try:
        response = client.request(method, path, **kwargs)
    except Hold:
        entry["state"] = state + "_UNCERTAIN"
        persist(JOURNAL, journal)
        raise
    if not 200 <= response.status_code < 300:
        entry.update({"state": state + "_REJECTED", "http_status": response.status_code})
        persist(JOURNAL, journal)
        raise Hold(state + "_HTTP_" + str(response.status_code))
    return response


def scores_file(journal):
    persist(SCORES, {"schema_version": 1, "source": "official authenticated own API",
        "competition_id": COMPETITION, "phase_id": PHASE, "task_id": TASK,
        "recorded_at_utc": stamp(), "prereg_commit": PREREG,
        "exploratory": journal.get("exploratory", False),
        "exploratory_or_unverified": journal.get("exploratory_or_unverified", False),
        "score_contract": "UNVERIFIED: decimal score does not establish k/N",
        "runs": [{"order": e["order"], "name": e["name"], "sha256": e["sha256"],
                  "sha256_scope": "local immutable ZIP only", "server_zip_bytes_verified": False,
                  "external_existing_match": e.get("external_existing_match", False),
                  "match_evidence": e.get("match_evidence", "local validated ZIP stream -> dataset key -> native accepted id"),
                  "submission_id": e.get("submission_id"), "state": e.get("state"),
                  "native_receipt": e.get("receipt"), "small_score_submission_id": e.get("small_score_submission_id"),
                  "small_score_receipt": e.get("small_score_receipt"), "prereg_chronology": e.get("prereg_chronology"),
                  "k": None, "N": None, "coverage": "UNKNOWN", "finished_time_KST": None,
                  "observed_finished_KST": e.get("observed_finished_KST")}
                 for e in journal["bundles"] if e.get("submission_id")]})


def poll(client, journal, entry):
    end = time.monotonic() + 3600
    while True:
        row = client.get_json("/api/submissions/%d/" % entry["submission_id"])
        if row.get("owner") != USER or row.get("phase") != PHASE:
            raise Hold("POLL_OWNER_PHASE_MISMATCH")
        entry["receipt"] = receipt(row)
        chronology(journal, entry, row, external=entry.get("external_existing_match", False))
        if task_id(row) == TASK:
            entry["small_score_submission_id"] = row["id"]
            entry["small_score_receipt"] = receipt(row)
        elif row.get("children"):
            children = [client.get_json("/api/submissions/%d/" % child_id) for child_id in row["children"]]
            if any(c.get("owner") != USER or c.get("phase") != PHASE or c.get("parent") != row["id"] or task_id(c) != TASK for c in children):
                raise Hold("CHILD_OWNER_PHASE_TASK_MISMATCH")
            entry["child_receipts"] = [receipt(c) for c in children]
            if len(children) != 1:
                raise Hold("MULTIPLE_SMALL_CHILD_SCORES_REQUIRE_REVIEW")
            entry["small_score_submission_id"] = children[0]["id"]
            entry["small_score_receipt"] = receipt(children[0])
        elif row.get("status") in TERMINAL:
            raise Hold("FINISHED_SMALL_TASK_UNVERIFIED")
        entry["state"] = "ACCEPTED_" + str(row.get("status", "UNKNOWN")).upper()
        entry["last_observed_utc"] = stamp()
        if row.get("status") == "Finished":
            entry.setdefault("observed_finished_KST", now().astimezone(dt.timezone(dt.timedelta(hours=9))).isoformat())
        persist(JOURNAL, journal)
        scores_file(journal)
        print("Bundle %d submission %d: %s" % (entry["order"], entry["submission_id"], row.get("status", "UNKNOWN")), flush=True)
        if row.get("status") in TERMINAL or end - time.monotonic() < 120:
            return
        time.sleep(120)


def run(records):
    if not sys.stdin.isatty():
        raise Hold("LOCAL_TTY_REQUIRED: no password was read")
    deadline()
    if SCORES.exists() and not JOURNAL.exists():
        raise Hold("EXISTING_SCORES_WITHOUT_JOURNAL_REQUIRES_RECONCILIATION")
    journal = json.loads(JOURNAL.read_text()) if JOURNAL.exists() else {
        "schema_version": 1, "prereg_commit": PREREG, "created_at_utc": stamp(),
        "exploratory": False, "bundles": [dict(b, state="LOCAL_READY") for b in records]}
    if journal.get("prereg_commit") != PREREG or len(journal.get("bundles", [])) != 3:
        raise Hold("JOURNAL_CONTRACT_MISMATCH")
    for entry, record in zip(journal["bundles"], records):
        if any(entry.get(k) != record[k] for k in ["order", "name", "sha256", "bytes", "path"]):
            raise Hold("JOURNAL_ZIP_MISMATCH")
    client = Client()
    try:
        identity = client.login()
        journal["authenticated_user"] = identity
        competition = client.get_json("/api/competitions/%d/" % COMPETITION)
        phase = next((p for p in competition.get("phases", []) if p.get("id") == PHASE), None)
        if not phase or phase.get("end") != "2026-11-01T11:55:00Z" or TASK not in [t.get("id") for t in phase.get("tasks", [])]:
            raise Hold("COMPETITION_PHASE_TASK_DEADLINE_CHANGED")
        if competition.get("fact_sheet"):
            raise Hold("FACT_SHEET_REQUIRES_REVIEW")
        queue = competition.get("queue")
        queue = queue.get("id") if isinstance(queue, dict) else queue
        rows = client.own_submissions()
        persist(JOURNAL, journal)
        # Reconcile ALL bundles before allowing the first new mutation.
        for entry in journal["bundles"]:
            if entry.get("submission_id"):
                matches = [r for r in rows if r.get("id") == entry["submission_id"]]
                expected_name = entry.get("receipt", {}).get("filename", entry["name"])
                if len(matches) != 1 or matches[0].get("filename") != expected_name:
                    raise Hold("JOURNALED_ACCEPTANCE_NOT_RECONCILED")
                entry["receipt"] = receipt(matches[0])
                chronology(journal, entry, matches[0], external=entry.get("external_existing_match", False))
            elif entry["state"] != "LOCAL_READY":
                raise Hold("PRIOR_MUTATION_REQUIRES_MANUAL_RECONCILIATION: bundle " + str(entry["order"]))
            else:
                matches = duplicate_matches(rows, entry)
                if matches:
                    entry.update({"submission_id": matches[0]["id"], "state": "EXISTING_MATCH_NO_UPLOAD",
                                  "external_existing_match": True, "match_evidence": match_evidence(matches[0], entry),
                                  "receipt": receipt(matches[0])})
                    chronology(journal, entry, matches[0], external=True)
                    journal["last_submission_attempt_utc"] = stamp()
        persist(JOURNAL, journal)
        for entry in journal["bundles"]:
            if entry.get("submission_id"):
                poll(client, journal, entry)
                continue
            check_local()
            deadline()
            # Another authorized path could have submitted while earlier polling ran.
            latest = client.own_submissions()
            matches = duplicate_matches(latest, entry)
            if matches:
                entry.update({"submission_id": matches[0]["id"], "state": "EXISTING_MATCH_NO_UPLOAD",
                              "external_existing_match": True, "match_evidence": match_evidence(matches[0], entry),
                              "receipt": receipt(matches[0])})
                chronology(journal, entry, matches[0], external=True)
                journal["last_submission_attempt_utc"] = stamp()
                persist(JOURNAL, journal)
                poll(client, journal, entry)
                continue
            if journal.get("last_submission_attempt_utc"):
                previous = dt.datetime.fromisoformat(journal["last_submission_attempt_utc"])
                wait = 120 - (now() - previous).total_seconds()
                if wait > 0:
                    time.sleep(wait)
            can = client.get_json("/api/can_make_submission/%d/" % PHASE)
            if can.get("can") is not True:
                raise Hold("SUBMISSION_NOT_CURRENTLY_ALLOWED")
            path = ROOT / entry["path"]
            response = mutate(client, journal, entry, "DATASET_CREATE", "POST", "/api/datasets/", json={
                "type": "submission", "competition": COMPETITION, "request_sassy_file_name": path.name,
                "file_name": path.name, "file_size": entry["bytes"]})
            try:
                dataset = response.json()
                key = str(uuid.UUID(dataset["key"]))
                signed = dataset["sassy_url"]
                if urlparse(signed).scheme != "https" or not urlparse(signed).netloc:
                    raise ValueError()
            except (ValueError, KeyError, TypeError):
                raise Hold("DATASET_CREATE_RESPONSE_UNCERTAIN")
            entry.update({"dataset_key": key, "state": "STORAGE_PUT_PENDING"})
            persist(JOURNAL, journal)
            deadline()
            # Separate cookie-free session; never send platform CSRF to storage.
            storage = client.requests.Session()
            storage.trust_env = False
            storage.mount("https://", client.requests.adapters.HTTPAdapter(max_retries=0))
            try:
                with path.open("rb") as stream:
                    response = storage.put(signed, data=stream, headers={"Content-Type": "application/zip"},
                                           allow_redirects=False, timeout=(15, 180))
                if not 200 <= response.status_code < 300:
                    raise Hold("STORAGE_PUT_FAILED")
            except client.requests.RequestException:
                raise Hold("STORAGE_PUT_UNCERTAIN")
            finally:
                storage.close()
                del signed, dataset
            mutate(client, journal, entry, "DATASET_COMPLETE", "PUT", "/api/datasets/completed/%s/" % key)
            entry["state"] = "DATASET_COMPLETED"
            if duplicate_matches(client.own_submissions(), entry):
                persist(JOURNAL, journal)
                raise Hold("EXTERNAL_MATCH_APPEARED_AFTER_DATASET_UPLOAD")
            journal["last_submission_attempt_utc"] = stamp()
            persist(JOURNAL, journal)
            response = mutate(client, journal, entry, "SUBMISSION_CREATE", "POST", "/api/submissions/", json={
                "data": key, "phase": PHASE, "tasks": [TASK], "fact_sheet_answers": {},
                "organization": None, "queue": queue, "selected_groups": []})
            try:
                row = response.json()
                if type(row.get("id")) is not int or row.get("phase") != PHASE:
                    raise ValueError()
            except (ValueError, TypeError):
                raise Hold("SUBMISSION_CREATE_RESPONSE_UNCERTAIN")
            entry.update({"submission_id": row["id"], "state": "ACCEPTED",
                          "accepted_at_utc": stamp(), "receipt": receipt(row)})
            chronology(journal, entry, row)
            persist(JOURNAL, journal)
            poll(client, journal, entry)
        print("H1 processing finished; native receipts saved. Unknown k/N remains unknown.", flush=True)
    except (Hold, KeyboardInterrupt):
        journal["run_state"] = "HOLD_RECONCILE_BEFORE_ANY_RESTART"
        journal["held_at_utc"] = stamp()
        persist(JOURNAL, journal)
        raise
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check-local", action="store_true")
    modes.add_argument("--run", action="store_true")
    args = parser.parse_args()
    lockpath = ROOT / "v9-execution/official-upload.lock"
    lockpath.parent.mkdir(parents=True, exist_ok=True)
    try:
        with lockpath.open("a") as lock:
            try:
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Hold("ANOTHER_UPLOADER_IS_RUNNING")
            records = check_local()
            if args.check_local:
                print(json.dumps({"state": "LOCAL_READY", "network_used": False,
                      "prereg_commit": PREREG, "bundles": records}, indent=2))
            else:
                run(records)
        return 0
    except Hold as error:
        print("HOLD: " + str(error), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("HOLD: INTERRUPTED; reconcile journal before restart", file=sys.stderr)
        return 130
    except Exception as error:
        # Exceptions may contain signed URLs/credentials: emit class only.
        print("HOLD: INTERNAL_" + type(error).__name__ + "; inspect local code, not secret response data", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
