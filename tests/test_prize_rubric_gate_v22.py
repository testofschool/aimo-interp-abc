#!/usr/bin/env python3
"""Nine protocol test groups. Synthetic text/probes are never submission evidence."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]
AFTER = '2026-11-03T12:00:00+09:00'
BASE = '''SYNTHETIC PROTOCOL FIXTURE. All example material is invented for local tests.
The frozen calculation reports 59 of 61 Small owners and 40 of 41 Main owners.
The BH rule rejects ranks 1 through r. The 21 October removal was attributed to profiling.
We do not identify which owners were affected. Reference baselines remain contextual methods.
The design target is not as a statement about the unpublished final set.
The calculation uses at least 76 independent items and 169 at a smaller effect; paired, problem-clustered comparisons need separate sizing.
The held-out problem evaluation is CPU based rather than additional model runs.
The source package is https://github.com/testofschool/aimo-interp-abc and the proposal is arXiv2607.13899.
This fixture supplies lexical context only. It supplies no native receipt or actual private measurement.
'''
LINES = {
    'outage': 'Codabench remains unreachable.',
    'unmeasured': 'Private-validation results of both reference baselines remain UNMEASURED.',
    'planned': 'The reference baselines are planned-not-run.',
    'ids': 'Evaluation IDs: none.',
    'announcement': "The organizers\' 24 October Discord announcement reports the outage.",
}
AI = '\nAI Use Statement\nAI was not used to fabricate observations. The author takes full responsibility.\n'

@contextmanager
def head_server(status=200):
    class Handler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(status)
            if status == 302:
                self.send_header("Location", "http://127.0.0.1:1/unreachable-redirect-target")
            self.end_headers()
        def log_message(self, *_args):
            pass
    server = HTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield 'http://127.0.0.1:%s/' % server.server_port
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gate', default=str(ROOT / 'tools/prize_rubric_gate.py'))
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    gate = Path(args.gate).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    fixtures = out / 'synthetic_fixtures'
    fixtures.mkdir(exist_ok=True)
    groups = []
    cases = []
    def fixture(name, omit=(), replacement=None, measured=False):
        if measured:
            body = BASE + 'A synthetic baseline scored 7/14 (submission id SYNTHETIC_ONLY, 2026-10-24 00:00).\n'
        else:
            body = BASE + '\n'.join((replacement or {}).get(k, v) for k, v in LINES.items() if k not in omit) + '\n'
        p = fixtures / (name + '.txt')
        p.write_text(body + AI, encoding='utf-8')
        return p
    good = fixture('qualified_fallback')
    missing = {k: fixture('missing_' + k, omit=(k,)) for k in LINES}
    measured = fixture('synthetic_measured', measured=True)
    def run(group, name, report, flags, code, label, extra=None):
        command = [sys.executable, '-I', str(gate), str(report), *flags]
        r = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=25)
        prefix = out / ('%02d_' % group + name)
        prefix.with_suffix('.stdout.txt').write_text(r.stdout)
        prefix.with_suffix('.stderr.txt').write_text(r.stderr)
        try:
            value = json.loads(r.stdout)
        except (ValueError, TypeError):
            value = {}
        checks = {'exit': r.returncode == code, 'label': value.get('result') == label,
                  'no_traceback': 'Traceback' not in r.stderr}
        if extra:
            checks.update(extra(value))
        row = {'group': group, 'case': name, 'input_kind': 'ACTUAL_APPROVED_PDF' if Path(report).suffix == '.pdf' else 'SYNTHETIC_TEST_ONLY',
               'command': command, 'expected': {'exit': code, 'result': label},
               'observed': {'exit': r.returncode, 'result': value.get('result'), 'failed': value.get('failed'), 'blocks': value.get('blocks')},
               'checks': checks, 'ok': all(checks.values())}
        cases.append(row)
        return value
    def group(number, title, fn):
        before = len(cases)
        fn()
        these = cases[before:]
        groups.append({'group': number, 'title': title, 'status': 'PASS' if all(c['ok'] for c in these) else 'FAIL',
                       'cases': len(these), 'failed_cases': [c['case'] for c in these if not c['ok']]})
    fb = ['--fallback-none', '--ids', 'none']
    sim = [*fb, '--now', AFTER, '--probe-result', 'down']
    pdf = ROOT / 'report/aimo-interp-report-v8-named.pdf'
    def baseline():
        run(1, 'real_normal', pdf, [], 1, 'FAIL', lambda v: {'15_of_17': v.get('passed') == 15 and v.get('total') == 17,
            'genuine_missing_only': v.get('failed') == ['ID_FIELD', 'OWN_SCORE']})
        run(1, 'real_clock_fallback_before_deadline', pdf, fb, 1, 'FAIL', lambda v: {'two_missing_checks': v.get('failed') == ['ID_FIELD', 'OWN_SCORE']})
    group(1, 'Actual PDF normal and current-clock fallback', baseline)
    def boundary():
        for name, time, label in [('before', '2026-11-03T11:59:59+09:00', 'TEST_ONLY(FAIL)'),
                                  ('at_kst', AFTER, 'TEST_ONLY(PASS_FALLBACK)'),
                                  ('at_equivalent_utc', '2026-11-03T03:00:00+00:00', 'TEST_ONLY(PASS_FALLBACK)')]:
            run(2, name, good, [*fb, '--now', time, '--probe-result', 'down'], 3, label)
    group(2, 'Cutoff just-before, inclusive boundary and equivalent UTC', boundary)
    def invalid_time():
        for name, time in [('bad_iso', 'not-a-time'), ('missing_offset', '2026-11-03T12:00:00')]:
            run(3, name, good, [*fb, '--now', time, '--probe-result', 'down'], 2, 'UNUSABLE')
    group(3, 'Invalid and timezone-free clocks fail cleanly', invalid_time)
    def isolation():
        run(4, 'clock_only', missing['outage'], [*fb, '--now', AFTER], 3, 'TEST_ONLY(FAIL)')
        run(4, 'probe_only', good, [*fb, '--probe-result', 'down'], 3, 'TEST_ONLY(FAIL)')
        run(4, 'simulation_never_unblocks', good, sim, 3, 'TEST_ONLY(PASS_FALLBACK)',
            lambda v: {'blocks_present': bool(v.get('blocks'))})
        with head_server() as url:
            run(4, 'custom_probe_is_test_only', good, [*fb, '--probe-url', url], 3, 'TEST_ONLY(FAIL)')
    group(4, 'Injected clock, fake probe and alternate target cannot unblock', isolation)
    def declarations():
        for name, p in missing.items():
            run(5, 'missing_' + name, p, sim, 3, 'TEST_ONLY(FAIL)')
        wrapped = fixture('valid_pdf_like_linewraps', replacement={
            'outage': 'Codabench remains unreach-\nable.',
            'planned': 'The reference baselines are planned-\nnot-run.',
            'announcement': "The organizers' 24 October Dis-\ncord announcement reports the outage."})
        run(5, 'valid_pdf_like_linewraps', wrapped, sim, 3, 'TEST_ONLY(PASS_FALLBACK)')
    group(5, 'Each required outage/unmeasured/planned/ID/citation declaration', declarations)
    def ids():
        run(6, 'missing_ids', good, ['--fallback-none'], 2, 'UNUSABLE')
        for name, value in [('numeric', '123'), ('mixed', 'none,123'), ('duplicate', 'none,none')]:
            run(6, name, good, ['--fallback-none', '--ids', value, '--now', AFTER, '--probe-result', 'down'], 3, 'TEST_ONLY(FAIL)')
    group(6, 'Exact none ID value and required IDs argument', ids)
    def resolved():
        p = fixture('resolved_outage', replacement={'outage': 'Codabench outage has ended; service is available.'})
        run(7, 'resolved_outage', p, sim, 3, 'TEST_ONLY(FAIL)')
        p = fixture('contradictory_outage', replacement={'outage': 'Codabench remains unreachable. Codabench outage has ended.'})
        run(7, 'contradictory_outage', p, sim, 3, 'TEST_ONLY(FAIL)')
        p = fixture('working_workaround', replacement={'outage': 'Codabench remains unreachable. The organizer workaround is working and available at https://example.invalid/evaluate.'})
        run(7, 'working_workaround', p, sim, 3, 'TEST_ONLY(FAIL)')
    group(7, 'Resolved outage and working workaround invalidate fallback', resolved)
    def probes():
        run(8, 'injected_up', good, [*fb, '--now', AFTER, '--probe-result', 'up'], 3, 'TEST_ONLY(FAIL)')
        for status in [200, 302, 404, 503]:
            with head_server(status) as url:
                run(8, 'http_' + str(status), good, [*fb, '--now', AFTER, '--probe-url', url], 3, 'TEST_ONLY(FAIL)')
    group(8, 'An answering HEAD probe blocks fallback, including HTTP errors', probes)
    def mode():
        run(9, 'measured_normal_fixture', measured, ['--probe-result', 'down'], 3, 'TEST_ONLY(PASS)')
        run(9, 'fallback_cannot_skip_preconditions', measured, ['--fallback-none', '--ids', '123'], 1, 'FAIL')
    group(9, 'Normal measured semantics retained; fallback checks always apply', mode)
    report = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'platform': sys.platform,
              'python': sys.version, 'gate': str(gate), 'gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(),
              'nine_group_mapping': 'Grouped from prior review requirements; subcases include all named edge cases. This is not a claimed verbatim missing historical list.',
              'result': 'PASS' if all(g['status'] == 'PASS' for g in groups) else 'FAIL',
              'groups_passed': sum(g['status'] == 'PASS' for g in groups), 'groups_total': len(groups),
              'cases_passed': sum(c['ok'] for c in cases), 'cases_total': len(cases), 'groups': groups, 'cases': cases,
              'synthetic_evidence_is_not_service_receipts': True, 'publications_or_submissions': 0}
    (out / 'RESULT.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['gate_sha256', 'platform', 'result', 'groups_passed', 'groups_total', 'cases_passed', 'cases_total', 'groups']}, indent=2))
    return 0 if report['result'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
