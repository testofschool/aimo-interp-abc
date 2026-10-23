#!/usr/bin/env python3
"""prize_rubric_gate.py — blocks T3 (push) and T4 (OpenReview submit) until the report PDF carries
every item the AIMO-Interp writeup-prize judge and the submission form can check.

Usage:  python3 prize_rubric_gate.py REPORT.pdf [--negations-max 40] [--json OUT.json]
        (or REPORT.txt already produced by `pdftotext -layout`)
Exit 0 = PASS (push/submit may proceed) · 1 = FAIL (named checks) · 2 = unusable input.
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
import json, re, subprocess, sys, shutil, argparse


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


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--negations-max", type=int, default=40)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    text, err = load_text(a.report)
    if text is None or len(text.strip()) < 500:
        print(json.dumps({"result": "UNUSABLE", "error": err or "empty text"}))
        return 2
    mt = main_text(text)
    rows, fails = [], []
    for cid, src, desc, fn in CHECKS:
        scope = text if cid in ("AI_STATEMENT", "CITE_PROPOSAL", "REPO_URL") else mt
        ok, detail = fn(scope)
        rows.append({"check": cid, "source": src, "ok": ok, "fix": None if ok else detail})
        if not ok:
            fails.append(cid)
    n = negation_count(mt)
    ok = n <= a.negations_max
    rows.append({"check": "NEGATIONS", "source": "[K1]", "ok": ok, "value": n, "max": a.negations_max,
                 "fix": None if ok else f"cut hedging: {n} > {a.negations_max}"})
    if not ok:
        fails.append("NEGATIONS")
    out = {"result": "PASS" if not fails else "FAIL", "failed": fails, "passed": len(rows) - len(fails), "total": len(rows),
           "blocks": "T3 push and T4 OpenReview submit" if fails else None, "rows": rows}
    s = json.dumps(out, indent=1, ensure_ascii=False)
    print(s)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(s)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
