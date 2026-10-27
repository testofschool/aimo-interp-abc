#!/usr/bin/env python3
"""End-to-end checker controls on synthetic text observations of one unchanged PDF.
No PDF is created or modified. Real fonts/metadata are still read from that PDF.
"""
from pathlib import Path
import contextlib, copy, hashlib, importlib.util, io, json, sys

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'v10-execution/audit_v83_ai_exception.py'
PDF = ROOT / 'report/aimo-interp-report-v8.3-anonymous.pdf'
REF = ROOT / 'v10-execution/reference/v8.1-named-approved.txt'
OUT = ROOT / 'results/v8.3/two-edits-20261027/ai-exception/CONTROLS.json'


def main():
    spec = importlib.util.spec_from_file_location('audit_scoped', AUDIT)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    pages, method, meta = audit.pages_text(str(PDF))
    pdf_sha_before = hashlib.sha256(PDF.read_bytes()).hexdigest()
    ai_index = next(i for i, page in enumerate(pages) if '\nAI Use Statement\n' in '\n' + page + '\n')
    refs_index = next(i for i, page in enumerate(pages) if '\nReferences\n' in '\n' + page + '\n')
    cases = []

    def case(name, edit, expect_exit, required_failed=None):
        sample = copy.deepcopy(pages)
        edit(sample)
        audit.pages_text = lambda path: (sample, method + '+synthetic-text-control', meta)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = audit.main(['audit_scoped', str(PDF), str(REF)])
        result = json.loads(output.getvalue())
        ok = code == expect_exit and (required_failed is None or required_failed in result['failed'])
        rows = {r['check']: r for r in result['rows']}
        cases.append({'name': name, 'expected_exit': expect_exit, 'actual_exit': code,
                      'result': result['result'], 'failed': result['failed'], 'expectation_met': ok,
                      'scope': rows['CODEX_AI_SCOPE_UNAMBIGUOUS'], 'forbidden': rows['FORBIDDEN_0']})

    def prepend_page(index, value):
        return lambda p: p.__setitem__(index, value + '\n' + p[index])
    def replace_at(index, old, new):
        def edit(p):
            assert p[index].count(old) == 1, (index, old)
            p[index] = p[index].replace(old, new, 1)
        return edit

    case('actual_frozen_PDF', lambda p: None, 0)
    case('REQUESTED_main_body_Codex_FAIL', prepend_page(0, 'Codex'), 1, 'FORBIDDEN_0')
    case('REQUESTED_AI_disclosure_Codex_PASS', replace_at(ai_index, 'AI Use Statement\n', 'AI Use Statement\nCodex\n'), 0)
    case('bibliography_Codex_FAIL', replace_at(refs_index, 'References\n', 'References\nCodex\n'), 1, 'FORBIDDEN_0')
    case('appendix_Codex_FAIL', prepend_page(9, 'Codex'), 1, 'FORBIDDEN_0')
    case('AI_other_forbidden_handoff_FAIL', replace_at(ai_index, 'AI Use Statement\n', 'AI Use Statement\nhandoff\n'), 1, 'FORBIDDEN_0')
    case('main_body_lowercase_codex_FAIL', prepend_page(0, 'codex'), 1, 'FORBIDDEN_0')
    case('main_body_UNMEASURED_FAIL', prepend_page(0, 'UNMEASURED'), 1, 'FORBIDDEN_0')
    case('missing_AI_heading_FAIL', replace_at(ai_index, 'AI Use Statement\n', 'AI disclosure\n'), 1, 'CODEX_AI_SCOPE_UNAMBIGUOUS')
    case('duplicate_AI_heading_FAIL', prepend_page(0, 'AI Use Statement'), 1, 'CODEX_AI_SCOPE_UNAMBIGUOUS')
    case('missing_References_heading_FAIL', replace_at(refs_index, 'References\n', 'Bibliography\n'), 1, 'CODEX_AI_SCOPE_UNAMBIGUOUS')
    case('duplicate_References_heading_FAIL', prepend_page(9, 'References'), 1, 'CODEX_AI_SCOPE_UNAMBIGUOUS')
    def reverse(p):
        replace_at(refs_index, 'References\n', 'Bibliography\n')(p)
        prepend_page(0, 'References')(p)
    case('References_before_AI_FAIL', reverse, 1, 'CODEX_AI_SCOPE_UNAMBIGUOUS')
    stable = pdf_sha_before == hashlib.sha256(PDF.read_bytes()).hexdigest()
    report = {'result': 'PASS' if all(c['expectation_met'] for c in cases) and stable else 'FAIL',
              'control_type': 'synthetic in-memory extracted-text observations; not edited PDFs or submission evidence',
              'PDF_sha256': pdf_sha_before, 'PDF_unchanged': stable,
              'supplemental_script_sha256': hashlib.sha256(AUDIT.read_bytes()).hexdigest(),
              'passed': sum(c['expectation_met'] for c in cases), 'total': len(cases), 'cases': cases}
    OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, indent=2))
    return 0 if report['result'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
