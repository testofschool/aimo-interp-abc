#!/usr/bin/env python3
"""prize_rubric_gate.py — blocks T3 (push) and T4 (OpenReview submit) until the report PDF carries
every item the AIMO-Interp writeup-prize judge and the submission form can check.

Usage:  python3 prize_rubric_gate.py REPORT.pdf [--negations-max 40] [--json OUT.json]
        python3 prize_rubric_gate.py REPORT.pdf --fallback-none --ids none [--json OUT.json]
          Fallback mode (HANDOFF §3): only when no evaluation path exists by 2026-11-03 12:00 KST.
          ID_FIELD/OWN_SCORE require the real cutoff, IDs none, a current outage declaration,
          UNMEASURED and planned-not-run baselines, no available evaluation IDs, the organizers'
          announcement citation, and a down probe. The operator also checks actual workaround status.
        (or REPORT.txt already produced by `pdftotext -layout`)
Local hardening of supplied v2.2; exact supplied bytes remain in research/gate_v2_2/source/.
Exit 0 = PASS or PASS_FALLBACK · 1 = FAIL · 2 = unusable input · 3 = TEST_ONLY.
Every usable run with a test clock, fake probe or alternate target exits 3 and remains blocked.
Malformed input exits 2. A local PASS does not establish organizer acceptance or authority.
Stdlib + poppler `pdftotext` only. Every rule names its primary source.

Sources:
  [PRIZE]  aimo-interp.github.io: "$4,000 ... selected technical reports, regardless of their ranking,
           judged on their scientific contribution" — interests: generalization, actionable
           interpretability, negative results, efficient methods.
  [RULE4]  site Rule 4: report must give "details on their submission and its open-sourced implementation".
  [RULE5]  site Rule 5: "The report must document the training data, the training codebase and the submission bundle".
  [FORM]   OpenReview invitation 2026-10-22 01:12 KST: required `leaderboard_submission_ids` ("Enter one or two IDs");
           ai_use_statement must name tasks used / not used / responsibility.
  [K1]     judge killer 2026-10-22: dead on "does not propose a new robustness predictor"; organizer_rerun insinuation;
           64 negations hide the result.
  [K2]     statistics killer 2026-10-22: "rejects the preceding ranks" contradicts BH (ranks 1..r).
  [K3]     rules killer 2026-10-22: no repo URL; own results UNMEASURED.
  [KC1/KC2] 2026-10-24 kill round on the Discord #announcements transcript (10/9 balance warning, 10/16 re-evaluation,
           10/21 removal of two 100% submissions for label profiling, 10/23 required citation): snapshot must be stated
           pre-removal, owners not identified, queue explained, bundles = baselines, item budget = design target.
"""
import json, re, subprocess, sys, shutil, argparse, datetime

FALLBACK_AT = datetime.datetime(2026, 11, 3, 12, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
ANNOUNCE_RE = re.compile(r"(24 October|October 24|2026-10-24)[^\n]{0,160}(announce|Discord)|(announce|Discord)[^\n]{0,160}(24 October|October 24|2026-10-24)", re.I)
OUTAGE_RE = re.compile(r"Codabench[^.]{0,120}(outage|unavailable|inaccessible|unreachable)", re.I)


def load_text(path):
    if path.lower().endswith(".pdf"):
        if not shutil.which("pdftotext"):
            return None, "pdftotext not installed"
        r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
        if r.returncode != 0:
            return None, r.stderr.strip()
        return r.stdout, None
    try:
        return open(path, encoding="utf-8").read(), None
    except OSError as e:
        return None, str(e)


def main_text(t):
    """main text = before the AI Use Statement heading (everything a judge scores)."""
    i = t.find("AI Use Statement")
    return t if i < 0 else t[:i]


CHECKS = [
    # id, source, description, test(text)->(ok, detail)
    ("ID_FIELD", "[FORM]+[RULE5]", "a Codabench submission id appears next to a measured own score",
     lambda t: (bool(re.search(r"submission id\s+\S+", t, re.I)) and not re.search(r"\bUNMEASURED\b", t),
                "needs 'submission id <id>' and no UNMEASURED")),
    ("OWN_SCORE", "[K1]+[K3]", "an own private-validation score k/14 is stated with a timestamp",
     lambda t: (bool(re.search(r"scored\s+\d{1,2}/14", t)) and bool(re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}", t)),
                "needs 'scored k/14' and an ISO timestamp")),
    ("REPO_URL", "[RULE4]", "a public repository URL appears in the report",
     lambda t: (bool(re.search(r"https?://(github\.com|gitlab\.com|huggingface\.co|zenodo\.org)/\S+", t)),
                "needs an https URL to the open-sourced implementation")),
    ("BH_WORDING", "[K2]", "BH step-up rule rejects ranks 1 through r, not 'the preceding ranks'",
     lambda t: ("preceding ranks" not in t and bool(re.search(r"ranks?\s+1\s+through\s+r", t)),
                "replace 'rejects the preceding ranks' with 'rejects ranks 1 through r'")),
    ("QUEUE_EXPLAINED", "[K1]+[KC1]+[KC2] (Discord 10/16 L14)", "the organizer rerun queue, if named, is explained as the 16 Oct per-problem re-evaluation, never as an unexplained perfect score",
     lambda t: ("make no inference about how that run was produced" not in t and
                ("aimo_organizer_rerun" not in t or bool(re.search(r"organizer re-evaluation|re-evaluated by the organizers|per-problem protocol", t, re.I))),
                "replace the queue paragraph with: rows from aimo_organizer_rerun are organizer re-evaluations under the 16 October per-problem protocol")),
    ("CITE_PROPOSAL", "[Discord 10/23 L63] required citation", "the proposal paper arXiv 2607.13899 is cited",
     lambda t: ("2607.13899" in t, "add the stefanik2026aimointerp citation (bibtex given in the 10/23 announcement)")),
    ("PRE_REMOVAL", "[KC1]+[KC2] (Discord 10/21 L41)", "the snapshot is stated as taken before the organizers' 21 October removal of two 100% submissions, with the announcement cited",
     lambda t: (bool(re.search(r"(21 October|October 21|2026-10-21)", t)) and bool(re.search(r"removed|removal", t)) and bool(re.search(r"profiling", t)),
                "state: snapshot predates the organizers' 21 Oct removal of two 100% submissions attributed to iterative label profiling (organizer announcement, Discord #announcements)")),
    ("NO_OWNER_ID", "[KC2] tone", "the report says it does not identify which owners were affected",
     lambda t: (bool(re.search(r"do not identify which owners|does not identify which owners|without identifying", t, re.I)),
                "add: 'We do not identify which owners were affected.'")),
    ("BASELINES_NOT_PROBES", "[KC1] (Discord 10/21 L45 'exploit labels ... disqualified')", "own bundles are described as reference baselines, never as a check of label balance on the private board",
     lambda t: (not re.search(r"(check|verify|test|probe)\w*\s+(the\s+)?(label\s+)?balance", t, re.I) and bool(re.search(r"reference baseline", t, re.I)),
                "describe the two bundles as reference baselines; remove any sentence that uses them to check label balance")),
    ("DESIGN_TARGET", "[KC1] (final set = unpublished AIMO sets)", "the item budget is offered as a design target for future validation boards, not a statement about the final set",
     lambda t: (bool(re.search(r"design target|future validation boards|future editions", t, re.I)) and bool(re.search(r"not (as )?a statement about the (unpublished )?final", t, re.I)),
                "add: 'We offer this as a design target for future validation boards, not as a statement about the unpublished final set.'")),
    ("NO_SELF_NEGATION", "[K1]", "the report does not say it proposes nothing",
     lambda t: ("does not propose a new robustness predictor" not in t,
                "replace with the actionable rule for organizers")),
    ("ACTIONABLE", "[PRIZE] actionable", "an explicit item-budget rule is stated for organizers (76 / 169 items, paired, problem-clustered)",
     lambda t: (bool(re.search(r"at least 76", t)) and bool(re.search(r"169", t)) and bool(re.search(r"paired", t, re.I)) and bool(re.search(r"problem-clustered|problem clusters?", t, re.I)),
                "needs 'at least 76 ... 169 ... paired ... problem-clustered' in abstract/§1")),
    ("NEGATIVE_RESULT", "[PRIZE] negative results", "the negative result is stated as a count a judge can repeat (59 of 61 / 40 of 41)",
     lambda t: (bool(re.search(r"59 of 61", t)) and bool(re.search(r"40 of 41", t)),
                "needs '59 of 61' and '40 of 41' in the abstract")),
    ("GENERALIZATION", "[PRIZE] generalization", "the generalization claim is anchored in a held-out statement (problem-grouped / leave-one-problem-out)",
     lambda t: (bool(re.search(r"leave-one-problem-out|held-out problem", t, re.I)), "keep the LOPO sentence")),
    ("EFFICIENT", "[PRIZE] efficient methods", "the method's cost is stated (CPU-only, no model runs)",
     lambda t: (bool(re.search(r"CPU", t)) and bool(re.search(r"rather than additional model runs|no (paid )?GPU|without GPU", t, re.I)),
                "state 'CPU ... rather than additional model runs' in §6")),
    ("AI_STATEMENT", "[FORM]", "AI Use Statement names tasks used, tasks not used, and author responsibility",
     lambda t: (("AI Use Statement" in t) and bool(re.search(r"was not used|did not use", t)) and bool(re.search(r"full responsibility", t)),
                "needs used / not used / full responsibility")),
]


def negation_count(t):
    return len(re.findall(r"\b(not|no|never|cannot|neither|nor)\b", t, flags=re.I))


DEFAULT_PROBE_URL = "https://www.codabench.org/"
LOCAL_VERSION = "2.2+local.1"


def live_probe(url):
    """Reachability evidence only; an HTTP reply never proves service usability."""
    import errno
    import ssl
    import urllib.error
    import urllib.request
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, message, headers, newurl):
            return None
    try:
        request = urllib.request.Request(url, method="HEAD")
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=15) as response:
            return {"state": "up", "url": url, "http_status": response.status,
                    "source": "live_HEAD", "reason": "HTTP response received"}
    except urllib.error.HTTPError as error:
        return {"state": "up", "url": url, "http_status": error.code,
                "source": "live_HEAD", "reason": "HTTP error response received"}
    except Exception as error:
        reason = getattr(error, "reason", error)
        network_errors = {errno.ECONNREFUSED, errno.ECONNRESET, errno.ECONNABORTED,
                          errno.ETIMEDOUT, errno.ENETUNREACH, errno.EHOSTUNREACH}
        down = (not isinstance(reason, ssl.SSLError) and
                (isinstance(reason, (TimeoutError, ConnectionError)) or
                 (isinstance(reason, OSError) and getattr(reason, "errno", None) in network_errors)))
        return {"state": "down" if down else "unverified", "url": url,
                "source": "live_HEAD", "error_type": type(reason).__name__,
                "reason": str(reason)}


def fallback_context(args, now, text, mt):
    """Apply every fallback prerequisite, including when ordinary score checks pass."""
    def flattened(value):
        # PDF extraction can break a word or a lexical compound at a line end.
        value = re.sub(r"(?<=[A-Za-z])-\s*\n\s*(?=[a-z])", "", value)
        return " ".join(value.split())
    flat = flattened(mt)
    citation_text = flattened(text)
    if now < FALLBACK_AT:
        return False, f"fallback refused: now {now.isoformat()} is before {FALLBACK_AT.isoformat()}", None
    ids = [x.strip() for x in args.ids.split(",")]
    if ids != ["none"]:
        return False, f"fallback refused: payload ids must be exactly ['none'], got {args.ids!r}", None
    current_outage = re.search(
        r"\bCodabench\s+(?:remains|is\s+still|is\s+currently|is|has\s+remained)\s+"
        r"(?:unreachable|unavailable|inaccessible)\b|"
        r"\bCodabench\s+outage\s+(?:is\s+)?(?:ongoing|unresolved|continuing)\b", flat, re.I)
    if not current_outage:
        return False, "fallback refused: state that Codabench remains unreachable/unavailable, not only a historical outage", None
    resolved = re.search(
        r"\bCodabench(?:\s+outage|\s+service)?[^.]{0,80}\b"
        r"(?:has\s+ended|has\s+been\s+resolved|is\s+resolved|is\s+restored|is\s+available|is\s+reachable|has\s+recovered)\b", flat, re.I)
    workaround = re.search(
        r"\b(?:the|a)\s+(?:organizer(?:s)?['’]?\s+)?workaround\s+(?:is|remains)\s+"
        r"(?:working|available|online|operational)\b", flat, re.I)
    if resolved or workaround:
        return False, "fallback refused: report states recovered service or an available organizer workaround", None
    if not re.search(r"\b(?:private[- ]?validation\s+results|baselines?)[^.]{0,180}\bunmeasured\b", flat, re.I):
        return False, "fallback refused: baseline private-validation results must remain explicitly UNMEASURED", None
    if not re.search(r"\bplanned[- ]?not[- ]?run\b", flat, re.I):
        return False, "fallback refused: describe the baselines as planned-not-run", None
    no_ids = re.search(r"\b(?:evaluation|leaderboard)\s+(?:submission\s+)?ids?\s*:\s*none\b", flat, re.I)
    no_ids = no_ids or re.search(r"\bno\s+(?:evaluation|leaderboard|submission)\s+ids?\s+(?:are\s+)?(?:available|exist|exists|obtained)\b", flat, re.I)
    if not no_ids:
        return False, "fallback refused: explicitly state that evaluation IDs are unavailable (Evaluation IDs: none)", None
    if not ANNOUNCE_RE.search(citation_text) or not re.search(r"\borganizers?\b", citation_text, re.I):
        return False, "fallback refused: cite the organizers' 24 October Discord outage announcement", None
    if args.probe_result:
        probe = {"state": args.probe_result, "source": "TEST_INJECTION"}
    else:
        probe = live_probe(args.probe_url)
    if probe["state"] != "down":
        return False, f"fallback refused: probe state is {probe['state']}; current evaluation path remains to be resolved", probe
    return True, "fallback: real cutoff reached, current outage and unmeasured/planned status declared, IDs none, announcement cited, probe down", probe


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--negations-max", type=int, default=40)
    ap.add_argument("--json")
    ap.add_argument("--fallback-none", action="store_true")
    ap.add_argument("--now", help="TEST ONLY: timezone-aware ISO8601; usable simulations always exit 3")
    ap.add_argument("--ids", help="comma-separated exact payload IDs; fallback requires only none")
    ap.add_argument("--probe-url", default=DEFAULT_PROBE_URL,
                    help="Any alternate target is TEST ONLY and cannot unblock publication")
    ap.add_argument("--probe-result", choices=["down", "up"], help="TEST ONLY: inject probe result")
    args = ap.parse_args(argv)
    test_inputs = {"clock": args.now is not None, "probe_result": args.probe_result is not None,
                   "alternate_probe_url": args.probe_url != DEFAULT_PROBE_URL}
    test_only = any(test_inputs.values())
    def emit(value, code):
        value["version"] = LOCAL_VERSION
        value["test_only"] = test_only
        value["test_inputs"] = test_inputs
        output = json.dumps(value, indent=1, ensure_ascii=False)
        print(output)
        if args.json:
            try:
                with open(args.json, "w", encoding="utf-8") as handle:
                    handle.write(output)
            except OSError as error:
                print(str(error), file=sys.stderr)
                return 2
        return code
    try:
        now = datetime.datetime.fromisoformat(args.now) if args.now else datetime.datetime.now(datetime.timezone.utc)
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("--now must include an explicit timezone offset")
    except (ValueError, TypeError, OverflowError) as error:
        return emit({"result": "UNUSABLE", "error": str(error),
                     "blocks": "T3 push and T4 OpenReview submit"}, 2)
    if args.fallback_none and not args.ids:
        return emit({"result": "UNUSABLE", "error": "--fallback-none requires --ids; only ['none'] is accepted",
                     "blocks": "T3 push and T4 OpenReview submit"}, 2)
    text, error = load_text(args.report)
    if text is None or len(text.strip()) < 500:
        return emit({"result": "UNUSABLE", "error": error or "empty text",
                     "blocks": "T3 push and T4 OpenReview submit"}, 2)
    mt = main_text(text)
    eligible, detail, probe = (False, None, None)
    if args.fallback_none:
        eligible, detail, probe = fallback_context(args, now, text, mt)
    rows, fails = [], []
    for cid, source, description, check in CHECKS:
        scope = text if cid in ("AI_STATEMENT", "CITE_PROPOSAL", "REPO_URL") else mt
        ok, fix = check(scope)
        if args.fallback_none and cid in ("ID_FIELD", "OWN_SCORE"):
            ok, fix = eligible, detail
        rows.append({"check": cid, "source": source, "ok": ok,
                     "fix": fix if (not ok or (args.fallback_none and cid in ("ID_FIELD", "OWN_SCORE"))) else None})
        if not ok:
            fails.append(cid)
    count = negation_count(mt)
    ok = count <= args.negations_max
    rows.append({"check": "NEGATIONS", "source": "[K1]", "ok": ok, "value": count,
                 "max": args.negations_max, "fix": None if ok else f"cut hedging: {count} > {args.negations_max}"})
    if not ok:
        fails.append("NEGATIONS")
    label = ("PASS_FALLBACK" if args.fallback_none else "PASS") if not fails else "FAIL"
    if test_only:
        label = "TEST_ONLY(" + label + ")"
    result = {"result": label, "failed": fails, "passed": len(rows) - len(fails), "total": len(rows),
              "blocks": "T3 push and T4 OpenReview submit" if (fails or test_only) else None,
              "mode": "fallback-none" if args.fallback_none else "normal", "rows": rows,
              "evaluated_at": now.isoformat(), "fallback_at": FALLBACK_AT.isoformat(), "probe": probe,
              "fallback_eligible": eligible if args.fallback_none else None,
              "scope": "Local text/clock/probe gate; operator must also verify actual organizer workaround state and submission authority"}
    return emit(result, 3 if test_only else (0 if not fails else 1))


if __name__ == "__main__":
    sys.exit(main())
