#!/usr/bin/env python3
"""audit_v83.py — independent re-measure of the v8.3 anonymous PDF (method differs from Codex's gates:
text via pypdf where available, poppler only for fonts/metadata).

Usage: python3 -I audit_v83.py ANON.pdf [REFERENCE_v8.1.txt]
Exit 0 = every check PASS · 1 = a check FAILED · 2 = unusable input.
Prints JSON. Identity tokens are counted, never echoed.
"""
import hashlib, json, re, shutil, subprocess, sys, difflib

ID_ASCII = ["testofschool", "gangjeongmin", "Felix", "felix", "Kang", "Korea", "Jung Min"]
FORBIDDEN = ["strongest non-perfect owner", "does not propose a new robustness predictor",
             "Working draft", "Not submitted", "pending owner", "UNMEASURED", "preceding ranks"]
URL = "https://anonymous.4open.science/r/aimo-identifiability"
QUEUE_IDS = ["bde5e370-4dba-4f19-8291-4a998bfecdcd", "0c736e59-8248-4dee-8e4f-2df037c552d7"]
HEAD = re.compile(r"^\s*(?:[0-9A-Z]{1,2}(?:\.[0-9]+)?\s+)?(Limitations\b|AI Use Statement|References|Appendix\b)", re.M)


def pages_text(path):
    try:
        import pypdf
        r = pypdf.PdfReader(path)
        return [p.extract_text() or "" for p in r.pages], "pypdf", (r.metadata or {})
    except Exception:
        out = []
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout).group(1))
        for i in range(1, n + 1):
            out.append(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), path, "-"], capture_output=True, text=True).stdout)
        return out, "pdftotext", {}


def norm(s):
    s = s.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
    s = re.sub(r"-\n(?=[a-z])", "", s)
    return re.sub(r"\s+", " ", s)


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__); return 2
    pdf = argv[1]
    try:
        raw = open(pdf, "rb").read()
    except OSError as e:
        print(json.dumps({"result": "UNUSABLE", "error": str(e)})); return 2
    pages, method, meta = pages_text(pdf)
    full = norm("\n".join(pages))
    rows = []

    def add(cid, ok, value=None):
        rows.append({"check": cid, "ok": bool(ok), "value": value})

    add("SHA256", True, hashlib.sha256(raw).hexdigest())
    add("PAGES", len(pages) == 10, len(pages))
    body_end = None
    for i, t in enumerate(pages, 1):
        m = HEAD.search(t)
        if m:
            before = t[:m.start()].strip()
            body_end = i if len(before.splitlines()) > 3 else i - 1
            break
    add("BODY_LE_5", body_end is not None and body_end <= 5, body_end)
    p5 = norm(pages[4]) if len(pages) >= 5 else ""
    add("P5_ENDS_validation_grid", "validation grid." in p5[-400:], p5[-120:].strip()[-60:])
    hits = {}
    for tok in ID_ASCII:
        n = len(re.findall(r"(?<![A-Za-z])" + re.escape(tok) + r"(?![A-Za-z])", full))
        if n:
            hits[f"token#{ID_ASCII.index(tok)}"] = n
    author = str(meta.get("/Author", "")) if meta else ""
    if not author and shutil.which("pdfinfo"):
        m = re.search(r"Author:\s+(.*)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout)
        author = m.group(1).strip() if m else ""
    add("IDENTITY_0", not hits, {"hits_by_index": hits, "author_meta_is_anonymous": author.lower().startswith("anonymous") or author == ""})
    add("URL_ANON", URL in full.replace(" ", "") or URL in full, URL in full)
    add("QUEUE_IDS_IN_E4", all(q in full.replace(" ", "") for q in QUEUE_IDS), [q[:8] in full for q in QUEUE_IDS])
    add("E4_7_14_FAIRCOIN", ("7/14" in full) and ("fair-coin" in full or "fair coin" in full), None)
    bad = {f: full.count(f) for f in FORBIDDEN if f in full}
    add("FORBIDDEN_0", not bad, bad)
    add("CITE_2607_13899", "2607.13899" in full, None)
    t3 = None
    if shutil.which("pdffonts"):
        fo = subprocess.run(["pdffonts", pdf], capture_output=True, text=True).stdout
        t3 = sum(1 for l in fo.splitlines()[2:] if re.search(r"\bType 3\b", l))
    add("TYPE3_0", t3 == 0, t3)
    if len(argv) == 3:
        ref = norm(open(argv[2], encoding="utf-8").read())
        a = re.split(r"(?<=[.!?])\s+", ref); b = re.split(r"(?<=[.!?])\s+", full)
        added = [s for s in b if s not in set(a) and len(s) > 25]
        removed = [s for s in a if s not in set(b) and len(s) > 25]
        rows.append({"check": "SENTENCE_DIFF_vs_v8.1", "ok": True,
                     "value": {"added_count": len(added), "removed_count": len(removed),
                               "added": added[:40], "removed": removed[:40]}})
    fails = [r["check"] for r in rows if not r["ok"]]
    print(json.dumps({"result": "PASS" if not fails else "FAIL", "text_method": method, "failed": fails, "rows": rows},
                     indent=1, ensure_ascii=False))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
