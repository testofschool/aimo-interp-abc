#!/usr/bin/env python3
"""openreview_payload_gate.py — refuse an OpenReview submission whose payload or PDF does not satisfy the LIVE form.

Usage: python3 -I tools/openreview_payload_gate.py INVITATION.json PAYLOAD.json PDF
  INVITATION.json  fresh dump of api2.openreview.net/invitations?id=<venue>/-/Submission (re-fetch right before submitting)
  PAYLOAD.json     {"title":..., "authors":[{"fullname":..,"username":"~..."}], "reciprocal_reviewers":["~..."],
                    "keywords":[...], "TLDR":..., "abstract":..., "ai_assistance":[...], "ai_use_statement":...,
                    "reciprocal_reviewing_acknowledgement":..., "rules_compliance":..., "white_box_award":[...] (optional)}
Exit 0 = payload + PDF satisfy every required field, enum string, regex and length, and the PDF has a separate
         'AI Use Statement' section after the main text and before 'References' whose text covers each ticked box
         and states responsibility · 1 = violations (blocks the OpenReview submit/revise click) · 2 = unreadable.
Also refuses a payload whose keys the live form does not define (catches a form change since the payload was written).
Stdlib + pdftotext/pdfinfo (poppler).
"""
import json, re, subprocess, sys
from datetime import datetime, timezone

def load_inv(p):
    d = json.loads(open(p, encoding="utf-8").readline())
    return d["invitations"][0] if "invitations" in d else d

def main(a):
    if len(a) != 3:
        print(__doc__, file=sys.stderr); return 2
    try:
        inv = load_inv(a[0]); pay = json.load(open(a[1], encoding="utf-8"))
        txt = subprocess.run(["pdftotext", "-layout", a[2], "-"], capture_output=True, text=True, check=True).stdout
        pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", a[2]], capture_output=True, text=True, check=True).stdout).group(1))
    except Exception as e:
        print(json.dumps({"result": "UNREADABLE", "error": str(e)})); return 2
    v = []
    now = datetime.now(timezone.utc).timestamp() * 1000
    if not (inv.get("cdate", 0) <= now < inv["expdate"]):
        v.append("form is not open now (cdate/expdate)")
    fields = inv["edit"]["note"]["content"]
    auto = {"venue", "venueid", "pdf"}
    for k in pay:
        if k not in fields:
            v.append(f"payload key '{k}' is not a field of the live form (form changed?)")
    for k, spec in fields.items():
        if k in auto: continue
        p = (spec.get("value") or {}).get("param", {})
        val = pay.get(k)
        if val in (None, "", []):
            if not p.get("optional"): v.append(f"required field '{k}' missing")
            continue
        enum = p.get("enum") or p.get("items")
        if enum:
            allowed = [e["value"] if isinstance(e, dict) else e for e in enum]
            vals = val if isinstance(val, list) else [val]
            for x in vals:
                if x not in allowed: v.append(f"'{k}': value not an exact allowed string: {x[:60]!r}")
        if p.get("regex") and p.get("type") in ("string", "string[]", "profile[]"):
            vals = val if isinstance(val, list) else [val]
            for x in vals:
                if not re.search(p["regex"], x): v.append(f"'{k}': {x[:40]!r} fails regex {p['regex']}")
        if p.get("maxLength") and isinstance(val, str) and len(val) > p["maxLength"]:
            v.append(f"'{k}': length {len(val)} > {p['maxLength']}")
    for au in pay.get("authors", []):
        if not re.match(r"^~\S+$", au.get("username", "")): v.append(f"author {au} lacks a ~profile id")
    if "No AI assistance was used" in pay.get("ai_assistance", []) and len(pay["ai_assistance"]) > 1:
        v.append("ai_assistance: 'No AI assistance was used' combined with other boxes")
    # PDF checks
    low = txt.lower()
    i_ai = low.find("ai use statement"); i_ref = low.rfind("references")
    if i_ai < 0:
        v.append("PDF: no 'AI Use Statement' section heading")
    elif i_ref >= 0 and i_ai > i_ref:
        v.append("PDF: 'AI Use Statement' appears after 'References'")
    else:
        sec = low[i_ai:i_ref if i_ref > i_ai else None]
        for box in pay.get("ai_assistance", []):
            if box != "No AI assistance was used" and box.lower() not in sec:
                v.append(f"PDF AI Use Statement does not mention ticked box '{box}'")
        if "responsib" not in sec: v.append("PDF AI Use Statement lacks a responsibility statement")
        if not re.search(r"not used|did not use|was not used|no ai", sec): v.append("PDF AI Use Statement does not state what AI was NOT used for")
    for pat in ["working draft", "not submitted", "pending owner confirmation"]:
        if pat in low: v.append(f"PDF contains draft marker '{pat}'")
    print(json.dumps({"result": "PASS" if not v else "BLOCKED", "pages": pages, "form_mdate": inv.get("mdate"),
                      "violations": v}, indent=1, ensure_ascii=False))
    return 0 if not v else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
