#!/usr/bin/env python3
"""One unchanged CPU/claims check after the parent's two prose edits are saved."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import importlib.metadata
import json
import os
import signal
import socket
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
RUNTIME=ROOT/'v10-execution/numeric-runtime'
REPRO=RUNTIME/'individual-recovery/repro'
PY=RUNTIME/'env/bin/python'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def prose():
    return {p:sha(ROOT/p) for p in ['report/main-anonymous.tex','report/main.tex','report/REPORT_DRAFT.md'] if (ROOT/p).is_file()}

def main():
    if sys.argv[1:]!=['--prose-edits-saved']:
        raise SystemExit('Require parent confirmation that two prose edits are saved.')
    receipt=OUT/'NUMERIC_CHECK.json'
    if receipt.exists():raise SystemExit('One-shot receipt already exists; no automatic rerun.')
    before=prose()
    previous=json.loads((ROOT/'v10-execution/NUMERIC_RECOVERY.json').read_text())
    expected={x['path']:x['sha256'] for x in previous['final_inputs']}
    inputs=[]
    for p in ['tools/report_numbers.py','tools/leaderboard_identifiability.py','tools/queue_receipt_scope_v83.py','research/claims.json']:
        live=sha(ROOT/p);isolated=sha(REPRO/p)
        if live!=expected[p] or isolated!=expected[p]:raise SystemExit('Unchanged pipeline/claims hash precondition failed: '+p)
        inputs.append({'path':p,'current_workspace_sha256':live,'executed_isolated_sha256':isolated,'matches_previous_canonical':True})
    for row in previous['data']:
        p=REPRO/'data'/row['filename']
        if sha(p)!=row['sha256']:raise SystemExit('Pinned data mismatch: '+row['filename'])
        inputs.append({'path':'data/'+row['filename'],'sha256':row['sha256'],'bytes':p.stat().st_size,'matches_pinned_data':True})
    argv=[str(PY),'-I','-X','importtime',str(REPRO/'tools/report_numbers.py'),'--data-dir',str(REPRO/'data'),'--check',str(REPRO/'research/claims.json'),'--out',str(OUT/'report_numbers.json')]
    command={'argv':argv,'cwd':str(REPRO),'canonical_numeric_source_commit':'33328fed2a38255f8a85b9d6ae1d54672c44e3bf','scope':'CPU fixed-data/claims check; no PDF argument or new scientific/outcome analysis'}
    (OUT/'command.json').write_text(json.dumps(command,indent=2)+'\n')
    start=time.time();started=datetime.now(timezone.utc).isoformat()
    with (OUT/'stdout.txt').open('wb') as out,(OUT/'stderr.txt').open('wb') as err:
        child=subprocess.Popen(argv,cwd=REPRO,stdout=out,stderr=err,start_new_session=True)
        try:code=child.wait(timeout=60);execution_status='COMPLETED'
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=2)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=2)
            code=None;execution_status='TIMEOUT'
    after=prose()
    try:result=json.loads((OUT/'stdout.txt').read_text())
    except ValueError:result=None
    status=result.get('result') if isinstance(result,dict) and result.get('result') in ['PASS','FAIL'] else ('UNRUN_TIMEOUT' if execution_status=='TIMEOUT' else 'FAILED_EXECUTION')
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True,timeout=5).stdout.strip()
    record={'schema_version':1,'status':status,'started_at_utc':started,'completed_at_utc':datetime.now(timezone.utc).isoformat(),'host':socket.gethostname(),'workspace':str(ROOT),'workspace_head':head,'canonical_numeric_source_commit':command['canonical_numeric_source_commit'],'execution_status':execution_status,'exit_code':code,'elapsed_s':round(time.time()-start,3),'bound_s':60,'result':result,'inputs':inputs,'saved_prose_sha256_before':before,'saved_prose_sha256_after':after,'saved_prose_unchanged_during_numeric_run':before==after,'stdout_sha256':sha(OUT/'stdout.txt'),'stderr_sha256':sha(OUT/'stderr.txt'),'command':'command.json','scope':'Numeric pipeline and claims unchanged; this is not the approved revised audit_v83.py and not a PDF-specific numerical measurement.','scientific_or_official_result_queries':0,'auth_requests':0,'POSTs':0,'uploads':0,'H1_process_interactions':0,'git_commits':0}
    receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':status,'result':result,'elapsed_s':record['elapsed_s'],'prose_stable':before==after}),flush=True)

if __name__=='__main__':main()
