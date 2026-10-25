#!/usr/bin/env python3
"""Receipt/generation boundary tests; local copies never constitute new submissions."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded

q = module('queue_scope', ROOT/'tools/queue_receipt_scope_v83.py')
renderer = module('renderer', ROOT/'tools/render_report.py')


class QueueReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='queue-contract-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for source in [ROOT/'research/PREREG_v6.json', *[ROOT/'research/v8_3_sources/queue'/s['file'] for s in q.RECEIPTS.values()], *[ROOT/'bundles'/b for b in q.RECEIPTS]]:
            target = self.root/source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source,target)
        self.now = datetime(2026,10,25,12,tzinfo=timezone.utc)

    def inspect(self):
        return q.inspect(receipts_dir=self.root/'research/v8_3_sources/queue',bundle_root=self.root/'bundles',prereg_path=self.root/'research/PREREG_v6.json',now=self.now)

    def changed(self, fields):
        """Coherently re-pin a synthetic mutation to reach semantic validation."""
        specs=deepcopy(q.RECEIPTS); spec=next(iter(specs.values())); p=self.root/'research/v8_3_sources/queue'/spec['file']
        row=json.loads(p.read_text())
        for key,value in fields.items():
            cursor=row; parts=key.split('.')
            for part in parts[:-1]: cursor=cursor[part]
            cursor[parts[-1]]=value
        raw=json.dumps(row).encode(); p.write_bytes(raw); spec['sha256']=hashlib.sha256(raw).hexdigest()
        return patch.object(q,'RECEIPTS',specs)

    def blocked(self):
        state=self.inspect(); self.assertFalse(state['measured_score_statements_allowed']);self.assertTrue(state['errors'])
        with self.assertRaises(ValueError): q.numbers(state)
        return state

    def test_exact_supplied_results_and_provenance_scope(self):
        s=self.inspect(); self.assertTrue(s['measured_score_statements_allowed'])
        self.assertFalse(s['native_owner_receipt_verified']);self.assertFalse(s['on_codabench_leaderboard'])
        self.assertFalse(s['per_problem_balance_inference_allowed']);self.assertFalse(s['pairwise_ranking_inference_allowed'])
        n=q.numbers(s);self.assertEqual(n['queue_always_true_k'],7)
        self.assertEqual(n['queue_always_true_created_at_kst'],'2026-10-24 19:01:28')
        self.assertEqual(n['queue_text_length_control_created_at_kst'],'2026-10-24 19:03:37')
        self.assertEqual(n['queue_always_true_faircoin_one_sided_p'],0.604736328125)
        self.assertEqual(len(n),12)

    def test_missing_receipt(self):
        (self.root/'research/v8_3_sources/queue/receipt_always_robust.json').unlink();self.blocked()

    def test_receipt_byte_tamper(self):
        (self.root/'research/v8_3_sources/queue/receipt_always_robust.json').write_text('{}');self.blocked()

    def test_local_zip_byte_tamper(self):
        (self.root/'bundles/solution-always-true-small.zip').write_bytes(b'changed');self.blocked()

    def test_registered_mapping_must_stay_fixed(self):
        p=self.root/'research/PREREG_v6.json'; data=json.loads(p.read_text());data['predictions'][0]['sha256']='0'*64;p.write_text(json.dumps(data));self.blocked()

    def test_uuid_task_and_terminal_status(self):
        for field,value in [('id','00000000-0000-4000-8000-000000000001'),('task','main'),('status','Failed')]:
            with self.subTest(field=field),self.changed({field:value}):self.blocked()
            self.setUp()

    def test_off_grid_and_invalid_accuracy(self):
        for value in [0.501,True,'0.5',float('nan'),float('inf'),-0.1,1.1]:
            with self.subTest(value=value),self.changed({'scores.accuracy':value}):self.blocked()
            self.setUp()

    def test_registered_stop_threshold(self):
        with self.changed({'scores.accuracy':12/14}):self.blocked()

    def test_source_url_must_match_uuid(self):
        with self.changed({'_provenance.source':'public GET https://example.invalid/'}):self.blocked()

    def test_time_requires_offset_and_registration_order(self):
        for value in ['2026-10-24T19:01:28','2026-10-19T00:00:00Z','2026-12-01T00:00:00Z']:
            with self.subTest(value=value),self.changed({'created_at':value}):self.blocked()
            self.setUp()

    def renderer_files(self):
        for name in ['report/OWNER_PRIVATE_VAL_UNMEASURED.md','tools/queue_receipt_scope_v83.py','tools/codabench_receipt_scope.py','tools/prereg_codabench_gate.py']:
            dest=self.root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dest)
        text='## Abstract\nResult {{queue_always_true_k}}/14.\n\n## Appendix A. Supporting analysis\n'+renderer.OWNER_BEGIN+'\nScored {{queue_always_true_k}}/14.\n'+renderer.OWNER_END+'\n\n## Appendix B. Reproduction\nOther body.\n'
        return text,self.root/'report/REPORT_OUTLINE.md'

    def test_queue_protected_block_is_allowed_in_appendix_A(self):
        text,outline=self.renderer_files()
        with patch.object(renderer,'ROOT',self.root):
            rendered,state=renderer.owner_private_validation(text,outline,now=self.now)
        self.assertTrue(state['measured_score_statements_allowed']);self.assertIn('Scored {{queue_always_true_k}}',rendered)
        self.assertFalse(state['native_owner_receipt_verified'])

    def test_queue_missing_source_blocks_entire_render(self):
        text,outline=self.renderer_files();(self.root/'research/v8_3_sources/queue/receipt_always_robust.json').unlink()
        with patch.object(renderer,'ROOT',self.root), self.assertRaisesRegex(ValueError,'queue receipt source invalid'):
            renderer.owner_private_validation(text,outline,now=self.now)

    def test_queue_block_cannot_be_moved_outside_declared_appendix(self):
        text,outline=self.renderer_files();text=text.replace('## Appendix A.','## Appendix C.')
        with patch.object(renderer,'ROOT',self.root), self.assertRaisesRegex(ValueError,'inside Appendix A'):
            renderer.owner_private_validation(text,outline,now=self.now)

    def test_legacy_numeric_guard_is_not_replaced_by_queue_receipts(self):
        text,outline=self.renderer_files();text=text.replace('## Appendix A.','## 4.').replace('{{queue_always_true_k}}','7')
        with patch.object(renderer,'ROOT',self.root):
            rendered,state=renderer.owner_private_validation(text,outline,now=self.now)
        self.assertFalse(state['measured_score_statements_allowed']);self.assertIn('UNMEASURED',rendered)

    def test_original_152_claim_records_preserved(self):
        original=json.loads(subprocess.check_output(['git','show','144ce58:research/claims.json'],cwd=ROOT))['claims']
        current=json.loads((ROOT/'research/claims.json').read_text())['claims']
        self.assertEqual(len(original),152);self.assertEqual(current[:152],original)


if __name__=='__main__':unittest.main()
