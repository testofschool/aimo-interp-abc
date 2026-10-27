"""Persist only journaled own native receipt fields; do not invent k/N or finish time."""
from pathlib import Path
import datetime as dt
import json
import subprocess
import hashlib
from decimal import Decimal

ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'v9-execution/official-upload-journal.json'
j=json.loads(p.read_text())
committed=dt.datetime.fromtimestamp(int(subprocess.check_output(['git','show','-s','--format=%ct',j['prereg_commit']],cwd=ROOT,text=True).strip()),dt.timezone.utc)
runs=[]
validation_path=ROOT/'v9-execution/NATIVE_OUTPUT_CHECK.json'
validation=json.loads(validation_path.read_text()) if validation_path.exists() else None
validated={r['native_submission_id']:r for r in validation['runs']} if validation and validation.get('status')=='PASS' else {}
for e in j['bundles']:
    if not e.get('submission_id'):continue
    receipt=e.get('receipt',{})
    if receipt.get('owner')!='testofschool' or receipt.get('phase')!=30038:raise SystemExit('HOLD_OWNER_PHASE_MISMATCH')
    task=receipt.get('task'); task_id=task.get('id') if isinstance(task,dict) else task
    if task_id!=36241:raise SystemExit('HOLD_SMALL_TASK_NOT_VERIFIED')
    values={v['column_key']:v.get('score') for v in receipt.get('scores',[]) if isinstance(v,dict) and 'column_key'in v}
    chronology=None
    if e['order']==3:
        created=receipt.get('created_when')
        valid=committed<dt.datetime.fromisoformat(created.replace('Z','+00:00')) if created else None
        chronology={'prereg_commit':j['prereg_commit'],'prereg_commit_time_utc':committed.isoformat(),'native_submission_created_when':created,'status':'PREREG_PRECEDES_SUBMISSION' if valid is True else 'UNKNOWN' if valid is None else 'SUBMISSION_NOT_AFTER_PREREG','classification':'PREREG_CHRONOLOGY_VERIFIED' if valid is True else 'UNKNOWN'}
        e['prereg_chronology']=chronology
    runs.append({'order':e['order'],'name':e['name'],'sha256':e['sha256'],'sha256_scope':'local immutable ZIP only','server_zip_bytes_verified':False,'external_existing_match':False,'match_evidence':'One browser chooser selection of hash-verified local ZIP, Small-only task, native owned filename/ID/phase/task readback','submission_id':e['submission_id'],'state':e['state'],'native_receipt':receipt,'small_score_submission_id':e.get('small_score_submission_id'),'small_score_receipt':e.get('small_score_receipt'),'native_score_values':values,'accuracy':values.get('accuracy'),'k':None,'N':None,'coverage':values.get('coverage','UNKNOWN'),'invalid_predictions':values.get('invalid_predictions'),'finished_time_KST':None,'observed_finished_KST':e.get('observed_finished_KST'),'prereg_chronology':chronology,'S1_check':('MATCH_RAW_ACCURACY_EXPECTATION_N_UNVERIFIED' if values.get('accuracy')=='0.5000000000' else 'PENDING' if not values else 'MISMATCH') if e['order']in(1,2) else 'NO_PREDECLARED_PROBE_SCORE'})
for run in runs:
    proof=validated.get(run['submission_id'])
    if proof is None: continue
    if proof['zips']['submitted-bundle.zip']['sha256']!=run['sha256']:raise SystemExit('HOLD_SERVER_BUNDLE_HASH_MISMATCH')
    if Decimal(proof['accuracy_native_raw'])!=Decimal(run['accuracy']):raise SystemExit('HOLD_NATIVE_ACCURACY_MISMATCH')
    if Decimal(proof['coverage_native_raw'])!=Decimal(run['coverage']):raise SystemExit('HOLD_NATIVE_COVERAGE_MISMATCH')
    if proof['prediction_rows']!=proof['unique_ids'] or proof['summary_cases']!=proof['N']:raise SystemExit('HOLD_COUNT_PROOF_MISMATCH')
    if not proof['all_prediction_rows_valid_binary'] or not proof['native_scoring_json_matches_api']:raise SystemExit('HOLD_NATIVE_OUTPUT_VALIDATION')
    run.update({'server_zip_bytes_verified':True,'k':proof['k'],'N':proof['N'],'count_proof':'v9-execution/NATIVE_OUTPUT_CHECK.json','count_identification':proof['count_identification']})
    if run['order'] in (1,2):run['S1_check']='MATCH_7_OF14' if (run['k'],run['N'])==(7,14) else 'MISMATCH'
result={'schema_version':1,'source':'official authenticated own API rendered in logged-in browser; whitelisted DOM-visible JSON receipt fields only','competition_id':16180,'phase_id':30038,'task_id':36241,'recorded_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'prereg_commit':j['prereg_commit'],'exploratory':j.get('exploratory',False),'score_contract':'Validated frozen unweighted binary reference scorer plus native full coverage/zero invalid, 14 unique valid output records and ingestion cases14 identify k7/N14; actual server deployment source hash and exact finish time remain unexposed.','runs':runs}
result['native_output_validation']={'path':str(validation_path.relative_to(ROOT)),'sha256':hashlib.sha256(validation_path.read_bytes()).hexdigest()} if validation else None
for path,value in [(p,j),(ROOT/'v9-execution/SCORES.json',result)]:
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');temp.replace(path)
print(json.dumps({'runs':len(runs),'native_ids':[r['submission_id']for r in runs],'statuses':[r['native_receipt']['status']for r in runs],'k_N_invented':False}))
