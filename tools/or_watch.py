#!/usr/bin/env python3
"""Read public rule sources once; never authenticate, edit a note, or schedule.

Exit 0 = seeded/unchanged/cutoff, 3 = changed, 2 = an explicit error.
Healthy tracks still produce evidence when another track fails. watch_state.json
is an atomic last-successful baseline and is never advanced on a failed run.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

INV = "https://api2.openreview.net/invitations?id=NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission"
SITE = "https://github.com/aimo-interp/aimo-interp.github.io"
BY = "https://github.com/byeolki/aimo-interp"
CB = "https://www.codabench.org/api/competitions/16180/"
KST = datetime.timezone(datetime.timedelta(hours=9))
CUTOFF = datetime.datetime(2026, 11, 6, 20, 0, tzinfo=KST)
SHA_RE = re.compile(r"[0-9a-f]{40}")
SNAPSHOT_RE = re.compile(r"invitation_[0-9]+(?:_[0-9a-f]{12,64})?\.json")
MAX_BODY = 3 * 1024 * 1024


class WatchError(RuntimeError):
    pass


def atomic_bytes(path, raw):
    """A failed write/replace leaves the previous complete file in place."""
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix="." + path.name + ".", delete=False) as handle:
            temporary = handle.name
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def atomic_json(path, value):
    atomic_bytes(path, (json.dumps(value, indent=2) + "\n").encode())


def get(url):
    """Use TLS verification on both routes; curl bounds the certificate fallback."""
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            raw = response.read(MAX_BODY + 1)
    except urllib.error.HTTPError as error:
        raise WatchError("HTTP " + str(error.code)) from error
    except (urllib.error.URLError, ssl.SSLError) as error:
        reason = getattr(error, "reason", error)
        if not isinstance(reason, ssl.SSLError):
            raise WatchError("HTTPS acquisition failed: " + type(reason).__name__) from error
        result = subprocess.run(
            ["curl", "--disable", "--fail-with-body", "--silent", "--show-error",
             "--connect-timeout", "5", "--max-time", "20", "--max-filesize", str(MAX_BODY), url],
            capture_output=True, timeout=23, stdin=subprocess.DEVNULL)
        if result.returncode:
            raise WatchError("TLS-verified curl fallback exit " + str(result.returncode))
        raw = result.stdout
    if len(raw) > MAX_BODY:
        raise WatchError("public response exceeds size bound")
    return raw


def git(args, timeout=30):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": os.devnull}
    result = subprocess.run(["git", "-c", "credential.helper=", "-c", "credential.interactive=never", *args],
                            capture_output=True, text=True, timeout=timeout,
                            stdin=subprocess.DEVNULL, env=env)
    if result.returncode:
        raise WatchError("public git operation failed, exit " + str(result.returncode))
    return result.stdout


def head(repo):
    rows = [line.split() for line in git(["ls-remote", repo, "HEAD"]).splitlines()]
    if len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != "HEAD" or not SHA_RE.fullmatch(rows[0][0]):
        raise WatchError("invalid public HEAD response")
    return rows[0][0]


def site_diff(root, old, new):
    directory = root / "site_repo"
    if not directory.exists():
        git(["clone", "-q", "--no-checkout", SITE, str(directory)], timeout=60)
    if directory.is_symlink() or not directory.is_dir():
        raise WatchError("unsafe site cache path")
    if git(["-C", str(directory), "remote", "get-url", "origin"]).strip() not in (SITE, SITE + ".git"):
        raise WatchError("site cache origin mismatch")
    git(["-C", str(directory), "fetch", "-q", "--no-tags", "origin"], timeout=60)
    for revision in (old, new):
        try:
            git(["-C", str(directory), "cat-file", "-e", revision + "^{commit}"])
        except WatchError:
            git(["-C", str(directory), "fetch", "-q", "--no-tags", "origin", revision], timeout=60)
            git(["-C", str(directory), "cat-file", "-e", revision + "^{commit}"])
    return git(["-C", str(directory), "diff", "--no-ext-diff", "--no-textconv",
                old, new, "--", "index.html"])


def invitation(data):
    rows = data.get("invitations") if isinstance(data, dict) else None
    if not isinstance(rows, list) or len(rows) != 1 or data.get("count", 1) != 1:
        raise WatchError("expected exactly one invitation")
    value = rows[0]
    if value.get("id") != "NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge/-/Submission":
        raise WatchError("unexpected invitation id")
    if type(value.get("tmdate")) is not int or value["tmdate"] <= 0:
        raise WatchError("invalid invitation tmdate")
    content = value["edit"]["note"]["content"]
    if not isinstance(content, dict) or not content:
        raise WatchError("missing invitation content schema")
    for field in content.values():
        param = field["value"]["param"]
        if not isinstance(param, dict) or ("optional" in param and type(param["optional"]) is not bool):
            raise WatchError("malformed field parameter")
    return value


def required(field):
    param = field["value"]["param"]
    return "const" not in param and not param.get("optional", False)


def invitation_diff(old, new):
    before, after = old["edit"]["note"]["content"], new["edit"]["note"]["content"]
    added, common = sorted(after.keys() - before.keys()), sorted(before.keys() & after.keys())
    changed = [key for key in common if before[key] != after[key]]
    became_required = [key for key in common if not required(before[key]) and required(after[key])]
    types = {key: {"before": before[key]["value"]["param"].get("type"),
                   "after": after[key]["value"]["param"].get("type")}
             for key in common if before[key]["value"]["param"].get("type") != after[key]["value"]["param"].get("type")}
    dates = {key: {"before": old.get(key), "after": new.get(key)}
             for key in ("cdate", "duedate", "expdate") if old.get(key) != new.get(key)}
    old_license, new_license = old["edit"]["note"].get("license"), new["edit"]["note"].get("license")
    diff = {"old_tmdate": old["tmdate"], "new_tmdate": new["tmdate"], "added": added,
            "removed": sorted(before.keys() - after.keys()), "changed": changed,
            "required_added": [key for key in added if required(after[key])],
            "required_changed": [key for key in changed if required(after[key])],
            "became_required": became_required, "type_changed": types, "dates_changed": dates,
            "license_changed": old_license != new_license,
            "fields": {key: {"before": before.get(key), "after": after.get(key)}
                       for key in sorted(set(added + changed + list(before.keys() - after.keys())))},
            "note_mutations": 0}
    diff["requires_payload_review"] = bool(diff["required_added"] or diff["required_changed"] or became_required or types or diff["removed"])
    if (old["tmdate"] != new["tmdate"] or added or diff["removed"] or changed or dates or diff["license_changed"]):
        return diff
    return None


def phase(data):
    rows = [row for row in data["phases"] if row.get("id") == 30038]
    if len(rows) != 1:
        raise WatchError("expected exactly one phase 30038")
    value = {key: rows[0].get(key) for key in ("id", "name", "start", "end", "status", "submission_rule")}
    if not valid_old_phase(value):
        raise WatchError("invalid phase end or status")
    return value


def acquire(name):
    try:
        if name in ("site_head", "byeolki_head"):
            return {"status": "OK", "value": head(SITE if name == "site_head" else BY)}
        raw = get(INV if name == "invitation" else CB)
        value = invitation(json.loads(raw)) if name == "invitation" else phase(json.loads(raw))
        result = {"status": "OK", "value": value, "source_sha256": hashlib.sha256(raw).hexdigest()}
        if name == "invitation":
            result["raw"] = raw
        return result
    except (OSError, ValueError, TypeError, KeyError, AttributeError, WatchError, subprocess.SubprocessError) as error:
        return {"status": "ERROR", "error": str(error) if isinstance(error, WatchError) else type(error).__name__}


def old_invitation(state, root):
    if "inv_tmdate" not in state and "inv_file" not in state:
        return None
    if type(state.get("inv_tmdate")) is not int or not isinstance(state.get("inv_file"), str):
        raise WatchError("malformed invitation baseline")
    name = Path(state["inv_file"]).name
    if not SNAPSHOT_RE.fullmatch(name):
        raise WatchError("unsafe baseline snapshot name")
    path = root / name
    if path.is_symlink():
        raise WatchError("baseline snapshot may not be a symlink")
    value = invitation(json.loads(path.read_bytes()))
    if value["tmdate"] != state["inv_tmdate"]:
        raise WatchError("baseline tmdate mismatch")
    return value


def valid_old_phase(old):
    if isinstance(old, dict):
        return (type(old.get("id")) is int and old["id"] == 30038
                and isinstance(old.get("status"), str) and bool(old["status"])
                and valid_old_phase(old.get("end")))
    if isinstance(old, str):
        try:
            return datetime.datetime.fromisoformat(old.replace("Z", "+00:00")).tzinfo is not None
        except ValueError:
            return False
    return False


def run_watch(root, now=None):
    # `now` is dependency injection for offline tests only; no CLI test clock.
    now = now or datetime.datetime.now(KST)
    if now.tzinfo is None:
        raise WatchError("clock must include a timezone")
    if now >= CUTOFF:
        return {"result": "STOPPED_CUTOFF", "cutoff_KST": CUTOFF.isoformat(),
                "note_mutations": 0, "scheduled": False, "baseline_advanced": False}, 0
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    state_path = root / "watch_state.json"
    existed = state_path.exists()
    errors, changed, state = [], [], {}
    try:
        if existed:
            state = json.loads(state_path.read_bytes())
            if not isinstance(state, dict):
                raise WatchError("baseline must be an object")
    except (OSError, ValueError, WatchError) as error:
        state = {}
        errors.append({"source": "baseline", "error": type(error).__name__})
    names = ("invitation", "site_head", "byeolki_head", "codabench_phase")
    with ThreadPoolExecutor(max_workers=4) as pool:
        sources = dict(zip(names, pool.map(acquire, names)))
    for name, source in sources.items():
        if source["status"] != "OK":
            errors.append({"source": name, "error": source["error"]})
    candidate = dict(state)
    inv = sources["invitation"]
    if inv["status"] == "OK":
        try:
            previous = old_invitation(state, root)
            delta = invitation_diff(previous, inv["value"]) if previous else None
            if delta:
                path = root / ("INVITATION_DIFF_" + str(inv["value"]["tmdate"]) + ".json")
                atomic_json(path, delta)
                changed.append(str(path))
            name = "invitation_" + str(inv["value"]["tmdate"]) + "_" + inv["source_sha256"] + ".json"
            path = root / name
            if path.exists():
                if path.is_symlink() or path.read_bytes() != inv["raw"]:
                    raise WatchError("immutable snapshot conflict")
            else:
                atomic_bytes(path, inv["raw"])
            candidate.update(inv_tmdate=inv["value"]["tmdate"], inv_file=name,
                             duedate=inv["value"].get("duedate"), expdate=inv["value"].get("expdate"))
        except (OSError, ValueError, TypeError, KeyError, AttributeError, WatchError) as error:
            errors.append({"source": "invitation baseline/evidence", "error": type(error).__name__})
    for key, repo in (("site_head", SITE), ("byeolki_head", BY)):
        if sources[key]["status"] != "OK":
            continue
        new, old = sources[key]["value"], state.get(key)
        if key in state and (not isinstance(old, str) or not SHA_RE.fullmatch(old)):
            errors.append({"source": key + " baseline", "error": "invalid HEAD"})
            continue
        if old and old != new:
            path = root / ("SITE_DIFF_" + new + ".md" if key == "site_head" else "BYEOLKI_HEAD_CHANGE_" + new + ".md")
            body = "# " + repo + "\nold " + old + "\nnew " + new + "\nat " + now.isoformat() + "\n"
            if key == "site_head":
                try:
                    patch = site_diff(root, old, new)
                    body += "\nindex.html diff acquired successfully; full output, no truncation.\n```diff\n" + patch + "\n```\n"
                    if not patch:
                        body += "\nindex.html has no changes in this commit range.\n"
                except (OSError, WatchError, subprocess.SubprocessError) as error:
                    body += "\nINDEX_DIFF_UNAVAILABLE: " + type(error).__name__ + "\n"
                    errors.append({"source": "site index.html diff", "error": type(error).__name__})
            atomic_bytes(path, body.encode())
            changed.append(str(path))
        candidate[key] = new
    current = sources["codabench_phase"]
    if current["status"] == "OK":
        old = state.get("codabench_phase")
        # The supplied script stored only the end string; preserve compatibility
        # without pretending that it had measured the old phase status.
        comparable = current["value"]["end"] if isinstance(old, str) else current["value"]
        if old is not None and not valid_old_phase(old):
            errors.append({"source": "phase baseline", "error": "malformed or failed phase baseline"})
        elif old is not None and old != comparable:
            path = root / ("CODABENCH_PHASE_CHANGE_" + now.strftime("%Y%m%dT%H%M%S%f") + ".json")
            atomic_json(path, {"before": old, "after": current["value"]})
            changed.append(str(path))
        candidate["codabench_phase"] = current["value"]
    candidate.update(schema_version=2, last_run=now.isoformat())
    if not errors:
        atomic_json(state_path, candidate)
    public_sources = {key: {k: v for k, v in source.items() if k != "raw"} for key, source in sources.items()}
    result = {"result": "PARTIAL_ERROR" if errors else "CHANGED" if changed else "SEEDED" if not existed else "NO_CHANGE",
              "recorded_at_KST": now.isoformat(), "files": changed, "errors": errors, "sources": public_sources,
              "baseline_advanced": not errors, "note_mutations": 0, "scheduled": False}
    atomic_json(root / "watch_result.json", result)
    atomic_json(root / ("WATCH_RUN_" + now.astimezone(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json"), result)
    return result, 2 if errors else 3 if changed else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="v12-execution", type=Path)
    args = parser.parse_args(argv)
    try:
        result, code = run_watch(args.root)
    except (OSError, ValueError, WatchError) as error:
        result, code = {"result": "ERROR", "error": type(error).__name__, "note_mutations": 0, "scheduled": False}, 2
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
