#!/usr/bin/env python3
"""prize_rubric_gate.py — blocks T3 (push) and T4 (OpenReview submit) until the report PDF carries
every item the AIMO-Interp writeup-prize judge and the submission form can check.

Usage:  python3 prize_rubric_gate.py REPORT.pdf [--negations-max 40] [--json OUT.json]
        python3 prize_rubric_gate.py REPORT.pdf --fallback-none [--now ISO8601]
          Fallback mode (HANDOFF §3): only when no evaluation path exists by 2026-11-03 12:00 KST.
          ID_FIELD/OWN_SCORE then pass only if (a) the clock is past the fallback time and (b) the PDF
          states why no id exists: the Codabench outage and the organizers' announcement. Without this mode
          the gate would block submission forever during an outage — a rule that makes the goal impossible.
        (or REPORT.txt already produced by `pdftotext -layout`)
Exit 0 = PASS or PASS_FALLBACK (push/submit may proceed) · 1 = FAIL · 2 = unusable input · 3 = TEST_ONLY
(any run with --now or --probe-result; a test clock or a faked probe can never unblock a step).
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
  [FORM5]  OpenReview invitation tmdate 2026-10-24 18:30:57 KST, pdf field: "The main body of the report should not exceed
           5 pages and needs to be anonymized. In addition, you can use an unlimited number of pages for the AI usage
           statement, limitations, s, and appendix."
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
     lambda t: (bool(re.search(r"https?://(github\.com|gitlab\.com|huggingface\.co|zenodo\.org|anonymous\.4open\.science)/\S+", t)),
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


ALLOWED_HEAD = re.compile(r"^\s*(?:[0-9A-Z]{1,2}(?:\.[0-9]+)?\s+)?(Limitations\b.*|AI Use Statement|References|Appendix\b.*|Appendices)\s*$")
IDENTITY = ["testofschool", "gangjeongmin", "Jung Min", "Kang", "Korea", "Felix", "github.com/testofschool"]


def page_texts(path):
    r = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    m = re.search(r"Pages:\s+(\d+)", r.stdout)
    n = int(m.group(1)) if m else 0
    out = []
    for i in range(1, n + 1):
        out.append(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", path, "-"], capture_output=True, text=True).stdout)
    return out, r.stdout


def main_body_pages(pages):
    """pages occupied by the main body = up to the first heading of an unlimited section (Limitations, AI Use Statement,
    References, Appendix). Returns (pages_used, first_allowed_page, lines_of_body_on_that_page)."""
    for i, t in enumerate(pages, 1):
        body_lines = 0
        for line in t.splitlines():
            if ALLOWED_HEAD.match(line):
                return (i - 1 + (1 if body_lines > 3 else 0)), i, body_lines
            if line.strip() and not re.fullmatch(r"\s*\d+\s*", line):
                body_lines += 1
    return len(pages), None, None


def negation_count(t):
    return len(re.findall(r"\b(not|no|never|cannot|neither|nor)\b", t, flags=re.I))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--negations-max", type=int, default=40)
    ap.add_argument("--json")
    ap.add_argument("--fallback-none", action="store_true")
    ap.add_argument("--now", help="TEST ONLY: ISO8601 with offset; any run with --now reports TEST_ONLY and exits 3")
    ap.add_argument("--ids", help="comma-separated leaderboard_submission_ids exactly as they will be posted")
    ap.add_argument("--probe-url", default="https://www.codabench.org/", help="live outage probe target")
    ap.add_argument("--probe-result", choices=["down", "up"], help="TEST ONLY: skip the live probe (forces TEST_ONLY)")
    a = ap.parse_args(argv)
    _probe = {}
    def probe_state():
        if "v" in _probe:
            return _probe["v"]
        if a.probe_result:
            _probe["v"] = a.probe_result
            return _probe["v"]
        import urllib.request
        try:
            with urllib.request.urlopen(urllib.request.Request(a.probe_url, method="HEAD"), timeout=15) as r:
                _probe["v"] = "up" if r.status < 500 else "down"
        except Exception as e:
            code = getattr(e, "code", None)
            _probe["v"] = "up" if (code is not None and code < 500) else "down"
        return _probe["v"]
    ap_test = bool(a.now) or bool(a.probe_result)  # --now is a test clock: the run can never unblock a step (result TEST_ONLY, exit 3)
    now = datetime.datetime.fromisoformat(a.now) if a.now else datetime.datetime.now(datetime.timezone.utc)
    if a.fallback_none and not a.ids:
        print(json.dumps({"result": "UNUSABLE", "error": "--fallback-none requires --ids with the exact payload value(s); only ['none'] is accepted in fallback"}))
        return 2
    text, err = load_text(a.report)
    if text is None or len(text.strip()) < 500:
        print(json.dumps({"result": "UNUSABLE", "error": err or "empty text"}))
        return 2
    mt = main_text(text)
    rows, fails = [], []
    for cid, src, desc, fn in CHECKS:
        scope = text if cid in ("AI_STATEMENT", "CITE_PROPOSAL", "REPO_URL") else mt
        ok, detail = fn(scope)
        if a.fallback_none and cid in ("ID_FIELD", "OWN_SCORE") and not ok:
            if now < FALLBACK_AT:
                detail = f"fallback refused: now {now.isoformat()} is before {FALLBACK_AT.isoformat()}"
            elif not OUTAGE_RE.search(mt):
                detail = "fallback refused: the PDF must state that no evaluation id exists because of the Codabench outage"
            elif not ANNOUNCE_RE.search(text):
                detail = "fallback refused: the PDF must cite the organizers' outage announcement (24 October, Discord #announcements)"
            elif [x.strip() for x in a.ids.split(",")] != ["none"]:
                detail = f"fallback refused: payload ids must be exactly ['none'], got {a.ids!r}"
            elif probe_state() != "down":
                detail = f"fallback refused: live probe says Codabench is {probe_state()} — submit the two baselines instead"
            else:
                ok, detail = True, f"fallback: time reached, outage + announcement cited, ids=['none'], probe={probe_state()}"
        rows.append({"check": cid, "source": src, "ok": ok, "fix": (detail if (ok and str(detail).startswith("fallback:")) else (None if ok else detail))})
        if not ok:
            fails.append(cid)
    if a.report.lower().endswith(".pdf"):
        pages, info = page_texts(a.report)
        used, first, lines = main_body_pages(pages)
        ok = used <= 5
        rows.append({"check": "MAIN_BODY_5_PAGES", "source": "[FORM5]", "ok": ok, "value": used,
                     "first_unlimited_section_page": first,
                     "fix": None if ok else f"main body uses {used} pages (> 5): move sections to an appendix after Limitations/AI Use Statement"})
        if not ok:
            fails.append("MAIN_BODY_5_PAGES")
        hits = sorted({w for w in IDENTITY if re.search(r"\b" + re.escape(w) + r"\b", text)})
        author_ok = bool(re.search(r"Author:\s+Anonymous", info)) or "Author:" not in info
        ok = not hits and author_ok
        rows.append({"check": "ANONYMIZED", "source": "[FORM5]", "ok": ok, "value": {"identity_hits": len(hits), "pdf_author_anonymous": author_ok},
                     "fix": None if ok else "remove identity strings (counts only, tokens not echoed) and use an anonymized repository link (e.g. anonymous.4open.science); set PDF Author metadata to Anonymous"})
        if not ok:
            fails.append("ANONYMIZED")
    n = negation_count(mt)
    ok = n <= a.negations_max
    rows.append({"check": "NEGATIONS", "source": "[K1]", "ok": ok, "value": n, "max": a.negations_max,
                 "fix": None if ok else f"cut hedging: {n} > {a.negations_max}"})
    if not ok:
        fails.append("NEGATIONS")
    used_fallback = a.fallback_none and any(r["check"] in ("ID_FIELD", "OWN_SCORE") and r["ok"] and (r.get("fix") or "").startswith("fallback:") for r in rows)
    label = ("PASS_FALLBACK" if used_fallback else "PASS") if not fails else "FAIL"
    if ap_test:
        label = "TEST_ONLY(" + label + ")"
    out = {"result": label, "failed": fails, "passed": len(rows) - len(fails), "total": len(rows),
           "blocks": "T3 push and T4 OpenReview submit" if fails else None,
           "mode": "fallback-none" if a.fallback_none else "normal", "rows": rows}
    s = json.dumps(out, indent=1, ensure_ascii=False)
    print(s)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(s)
    if ap_test:
        return 3
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
