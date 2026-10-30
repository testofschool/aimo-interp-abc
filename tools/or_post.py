#!/usr/bin/env python3
"""Prepare, post/revise once, or read back the existing AIMO-Interp note.

Usage: or_post.py PAYLOAD [--dry-run [--inv SAVED_INV]] [--out POST.json]
       or_post.py PAYLOAD --revise NOTE_ID --out REVISE.json
       or_post.py [PAYLOAD] --readback NOTE_ID --expect-pdf-sha256 HEX --out READBACK.json
Readback uses PAYLOAD, or payload.json(.filled.json) beside --out, for title/IDs.
Only hidden interactive Terminal password/OTP entry is supported. No credential
arguments or environment fallback. Dry-run imports no SDK and never logs in.
Readback uploads/edits nothing. A mismatch exits nonzero. A creation intent is
retained before any upload; uncertain outcomes require owner reconciliation,
never a repeated creation. Do not create if the report was already posted.
"""
import contextlib
import copy
import getpass
import hashlib
import importlib.util
import inspect
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import warnings

VENUE='NeurIPS.cc/2026/Workshop/AIMOInterp_Challenge'
INV_ID=VENUE+'/-/Submission'
VENUEID=VENUE+'/Submission'
DEFAULT_USER='gangjeongmin23@gmail.com'
STATE_DIR=Path(__file__).resolve().parents[1]/'v12-execution'/'private'


class Refused(Exception): pass


def digest(data): return hashlib.sha256(data).hexdigest()


def load_gate():
    path=Path(__file__).with_name('or_payload_gate.py')
    spec=importlib.util.spec_from_file_location('aimo_live_gate',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def options(args):
    flags={'--dry-run','--no-trial'}
    valued={'--out','--username','--revise','--readback','--expect-pdf-sha256','--expect-title','--expect-ids','--inv'}
    opts={};positions=[];i=0
    while i<len(args):
        key=args[i]
        if key in flags: opts[key]=True;i+=1
        elif key in valued and i+1<len(args) and not args[i+1].startswith('--'):
            if key in opts: raise Refused('duplicate option')
            opts[key]=args[i+1];i+=2
        elif key.startswith('--'): raise Refused('unsupported option; credential arguments and trial edits are disabled')
        else: positions.append(key);i+=1
    if len(positions)>1 or ('--revise' in opts and '--readback' in opts): raise Refused('invalid mode or payload arguments')
    if '--inv' in opts and '--dry-run' not in opts: raise Refused('saved invitations are allowed only in dry-run; writes always fetch live schema')
    if '--dry-run' in opts and ('--readback' in opts or '--revise' in opts): raise Refused('dry-run previews payload only')
    return opts,positions


def atomic_json(path,value,exclusive=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,indent=1,ensure_ascii=False)+'\n').encode()
    if exclusive:
        try: fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except FileExistsError: raise Refused('existing creation intent; reconcile the known/uncertain note, never create again')
        with os.fdopen(fd,'wb') as stream: stream.write(data);stream.flush();os.fsync(stream.fileno())
    else:
        fd,name=tempfile.mkstemp(prefix='.or-receipt-',dir=path.parent)
        try:
            with os.fdopen(fd,'wb') as stream: stream.write(data);stream.flush();os.fsync(stream.fileno())
            os.replace(name,path)
        finally:
            if os.path.exists(name): os.unlink(name)
    fd=os.open(path.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def load_payload(path):
    data=json.loads(Path(path).read_text())
    if not isinstance(data,dict): raise Refused('payload must be an object')
    data=copy.deepcopy(data)
    for key in ('venue','venueid'):data.pop(key,None)
    value=data.get('pdf')
    if isinstance(value,str) and not Path(value).is_absolute():data['pdf']=str(Path(path).absolute().parent/value)
    return data


def first_author(content):
    cell=content.get('authors',{});value=cell.get('value') if isinstance(cell,dict) else None
    ids=[]
    if isinstance(value,list):
        for author in value:
            profile=author.get('username') if isinstance(author,dict) else author
            if not isinstance(profile,str) or re.fullmatch(r'~\S+',profile) is None: raise Refused('ambiguous author metadata; owner reconciliation required')
            ids.append(profile)
    legacy=content.get('authorids',{})
    legacy=legacy.get('value') if isinstance(legacy,dict) else None
    if legacy is not None:
        if not isinstance(legacy,list) or not legacy or any(not isinstance(x,str) or re.fullmatch(r'~\S+',x) is None for x in legacy): raise Refused('ambiguous legacy author metadata')
        if ids and ids!=legacy: raise Refused('conflicting author metadata')
        ids=legacy
    if not ids:raise Refused('missing author metadata; owner reconciliation required')
    return ids[0]


def all_pages(client,filters,trash):
    required={'limit','offset','with_count','trash'}|set(filters)
    if not required<=set(inspect.signature(client.get_notes).parameters): raise Refused('unsupported SDK note-query contract')
    initial=client.get_notes(limit=1000,with_count=True,trash=trash,**filters)
    if not isinstance(initial,tuple) or len(initial)!=2: raise Refused('note-query completeness unavailable')
    rows,count=initial
    if not isinstance(rows,list) or isinstance(count,bool) or not isinstance(count,int) or not 0<=count<=50000: raise Refused('invalid note-query count')
    rows=list(rows)
    while len(rows)<count:
        page=client.get_notes(limit=1000,offset=len(rows),trash=trash,**filters)
        if not isinstance(page,list) or not page: raise Refused('incomplete note enumeration')
        rows+=page
    ids=[getattr(note,'id',None) for note in rows]
    if len(rows)!=count or any(not isinstance(x,str) or not x for x in ids) or len(set(ids))!=count: raise Refused('note enumeration changed or was truncated')
    return rows


def existing_notes(client,me):
    relevant={}
    # The owning API contract defines tauthor as a boolean for the current
    # user, unlike the SDK's stale Group-ID prose. Query both trash modes rather
    # than assuming whether trash=True includes live notes or only deleted ones.
    for query in ({'invitation':INV_ID},{'content':{'venueid':VENUEID}},{'tauthor':True,'domain':VENUE}):
        for trash in (False,True):
            for note in all_pages(client,query,trash):
                content=getattr(note,'content',None)
                if not isinstance(content,dict): raise Refused('unreadable prior note metadata')
                venue=(content.get('venueid') or {}).get('value')
                invitations=getattr(note,'invitations',[]) or []
                if 'tauthor' in query and venue!=VENUEID and INV_ID not in invitations:continue
                if note.id in relevant and first_author(relevant[note.id].content)!=first_author(content):raise Refused('prior author metadata changed during reconciliation')
                relevant[note.id]=note
    matches=[note.id for note in relevant.values() if first_author(note.content)==me]
    if matches: raise Refused('an existing/deleted first-author note exists; recover its ID and revise it only')
    return {'queries':6,'visible_venue_notes':len(relevant),'matching_first_author_notes':0,'queried_live_and_trash_modes':True}


def hidden_entry(label):
    if not sys.stdin.isatty():raise Refused('use your own interactive Terminal; credential environment fallback is disabled')
    with warnings.catch_warnings():
        warnings.simplefilter('error',getpass.GetPassWarning)
        value=getpass.getpass(label)
    if not value:raise Refused('empty credential entry refused')
    return value


def terminal_client(username):
    password=hidden_entry('OpenReview password (hidden): ')
    # Import only after the explicit TTY gate. Suppress SDK authentication output,
    # which can contain authentication responses; errors are reported by type only.
    from openreview.api import OpenReviewClient,Note
    from openreview import mfa
    if 'mfa_code_provider' not in inspect.signature(OpenReviewClient).parameters or not hasattr(mfa,'_default_mfa_code_prompt'):raise Refused('unsupported private-OTP SDK contract')
    original=mfa._default_mfa_code_prompt
    mfa._default_mfa_code_prompt=lambda method:hidden_entry('OpenReview OTP (hidden): ')
    try:
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            client=OpenReviewClient(baseurl='https://api2.openreview.net',username=username,password=password,mfa_code_provider=lambda method:hidden_entry('OpenReview OTP (hidden): '))
    finally:
        password=None;mfa._default_mfa_code_prompt=original
    return client,Note


def no_write_retries(client):
    adapters=getattr(getattr(client,'session',None),'adapters',None)
    if not isinstance(adapters,dict) or not adapters:raise Refused('cannot verify single-attempt SDK transport')
    for adapter in adapters.values():
        retry=adapter.max_retries.new(total=0,connect=0,read=0,redirect=0,status=0,other=0)
        adapter.max_retries=retry
        if retry.total!=0:raise Refused('cannot disable SDK write retries')


def flat_content(note):
    if not isinstance(note.content,dict):raise Refused('target content unavailable')
    flat={}
    for key,cell in note.content.items():
        if not isinstance(cell,dict) or 'value' not in cell:raise Refused('target has unsupported content cells')
        flat[key]=copy.deepcopy(cell['value'])
    return flat


def readback(client,nid,expected):
    note=client.get_note(nid)
    if note.id!=nid:raise Refused('readback returned a different note ID')
    flat=flat_content(note)
    rb={'id':note.id,'forum':note.forum,'tmdate':note.tmdate,'cdate':note.cdate,
        'leaderboard_submission_ids':flat.get('leaderboard_submission_ids'),'title':flat.get('title'),'TLDR':flat.get('TLDR'),'license':getattr(note,'license',None),'fields':sorted(flat)}
    try:
        data=client.get_attachment(id=nid,field_name='pdf');rb.update(pdf_sha256=digest(data),pdf_bytes=len(data))
    except Exception:
        rb['pdf_download_failed']=True
    rb['ids_match']=rb.get('leaderboard_submission_ids')==expected['ids']
    rb['title_match']=rb.get('title')==expected['title']
    rb['author_match']=first_author(note.content)==expected['first_author']
    rb['license_match']=rb['license']=='CC BY-SA 4.0'
    return rb,rb.get('pdf_sha256')==expected['pdf_sha256']


def run(opts,positions,client_factory=None,state_dir=None):
    gate=load_gate();out=Path(opts.get('--out','POST.json')).absolute()
    is_read='--readback' in opts;is_revise='--revise' in opts
    payload_path=Path(positions[0]).absolute() if positions else None
    if payload_path is None and is_read:
        payload_path=next((out.parent/name for name in ('payload.json.filled.json','payload.json') if (out.parent/name).is_file()),None)
    if payload_path is None:raise Refused('an expected payload baseline is required')
    payload=load_payload(payload_path)
    if '--dry-run' in opts:
        inv=gate.fetch_inv(opts.get('--inv'));report,filled=gate.validate(inv,payload,payload_path.parent)
        if report['result']!='PASS':return {'result':'REFUSED','gate':report},1
        return {'result':'DRY_RUN','invitation':INV_ID,'content':{k:{'value':v} for k,v in filled.items() if k!='pdf'},'pdf_file':filled['pdf'],'license':'CC BY-SA 4.0','gate':report},0
    authors=payload.get('authors')
    first=first_author({'authors':{'value':authors}})
    expected={'ids':opts.get('--expect-ids',payload.get('leaderboard_submission_ids')),'title':opts.get('--expect-title',payload.get('title')),'first_author':first}
    expected_hash=opts.get('--expect-pdf-sha256')
    if expected_hash is None and isinstance(payload.get('pdf'),str) and Path(payload['pdf']).is_file():expected_hash=digest(Path(payload['pdf']).read_bytes())
    if not all(isinstance(expected[k],str) and expected[k] for k in ('ids','title')) or not isinstance(expected_hash,str) or re.fullmatch('[0-9a-f]{64}',expected_hash) is None:raise Refused('complete expected title/IDs/PDF hash required')
    expected['pdf_sha256']=expected_hash
    state_dir=Path(state_dir or STATE_DIR)
    intent=state_dir/('creation-intent-'+digest((INV_ID+'|'+first).encode())[:24]+'.json')
    if not is_read and not is_revise and (intent.exists() or out.exists()):raise Refused('existing receipt or creation intent; recover/reconcile the posted note and revise only')
    client,Note=(client_factory or terminal_client)(opts.get('--username',DEFAULT_USER))
    # SDK login sets client.profile from the authenticated authorization
    # response. get_profile(None) is an unfiltered directory query, not identity.
    me=getattr(getattr(client,'profile',None),'id',None)
    if not isinstance(me,str) or re.fullmatch(r'~\S+',me) is None:raise Refused('authenticated profile is absent or malformed; refusing to infer identity')
    if not is_read and me!=first:raise Refused('authenticated principal must equal the intended first author')
    rec={'invitation':INV_ID,'steps':[],'expected_pdf_sha256':expected_hash}
    if is_read:
        nid=opts['--readback']
    else:
        no_write_retries(client)
        target=None
        if is_revise:
            target=client.get_note(opts['--revise'])
            if target.id!=opts['--revise'] or first_author(target.content)!=first:raise Refused('revision target ID or first author mismatch')
            venue=(target.content.get('venueid') or {}).get('value')
            if venue!=VENUEID and INV_ID not in (getattr(target,'invitations',[]) or []):raise Refused('revision target belongs to another or unknown venue')
            merged=flat_content(target);merged.update(payload);payload=merged
        else:
            rec['reconciliation']=existing_notes(client,me)
        # Never trust a previous .filled.json suffix or gate receipt. This fresh
        # fetched schema and exact file hash are checked immediately before writes.
        inv=client.get_invitation(INV_ID);inv=gate.invitation_object(inv.to_json())
        report,filled=gate.validate(inv,payload,payload_path.parent)
        if report['result']!='PASS':return {'result':'REFUSED','gate':report},1
        if report['pdf_sha256']!=expected_hash:raise Refused('local PDF differs from expected hash')
        rec.update(invitation_tmdate=inv.get('tmdate'),gate=report,local_pdf_sha256=report['pdf_sha256'])
        if not is_revise:
            state_dir.mkdir(parents=True,exist_ok=True,mode=0o700)
            atomic_json(intent,{'state':'PREPARED','invitation':INV_ID,'payload_sha256':report['payload_sha256'],'pdf_sha256':expected_hash},exclusive=True)
        try:
            if digest(Path(filled['pdf']).read_bytes())!=expected_hash:raise Refused('PDF changed after validation')
            attachment=client.put_attachment(filled['pdf'],INV_ID,'pdf')
            rec['steps'].append({'attachment_uploaded':True,'pdf_sha256':expected_hash})
            content=copy.deepcopy(target.content) if target else {}
            for key,value in filled.items():
                if key=='pdf':continue
                cell=copy.deepcopy(content.get(key,{}));cell['value']=value;content[key]=cell
            for key in ('venue','venueid'):content.pop(key,None)
            cell=copy.deepcopy(content.get('pdf',{}));cell['value']=attachment;content['pdf']=cell
            note=Note(content=content,license='CC BY-SA 4.0')
            if is_revise:note.id=opts['--revise']
            else:atomic_json(intent,{'state':'REQUEST_IN_FLIGHT','invitation':INV_ID,'payload_sha256':report['payload_sha256'],'pdf_sha256':expected_hash})
            rec['result']='REQUEST_IN_FLIGHT'
            atomic_json(out,rec)
            edit=client.post_note_edit(invitation=INV_ID,signatures=[me],note=note)
            nid=edit['note']['id']
            if not isinstance(nid,str) or not nid or (is_revise and nid!=opts['--revise']):raise Refused('write response note ID is invalid')
            rec.update(note_id=nid,result='POSTED_PENDING_READBACK')
            rec['steps'].append({'post_note_edit':edit['id'],'note':nid,'tmdate':edit.get('tmdate')})
            atomic_json(out,rec)
            if not is_revise:atomic_json(intent,{'state':'POSTED','note_id':nid,'pdf_sha256':expected_hash})
        except Exception as error:
            rec.update(result='WRITE_OUTCOME_UNCERTAIN',error_type=type(error).__name__)
            if not is_revise:atomic_json(intent,{'state':'UNKNOWN_OUTCOME','pdf_sha256':expected_hash,'note_id':rec.get('note_id')})
            atomic_json(out,rec)
            return rec,1
    try:
        rb,match=readback(client,nid,expected)
        rec.update(note_id=nid,readback=rb,match_pdf=match,ids_match=rb['ids_match'],title_match=rb['title_match'])
        passed=match and rb['ids_match'] and rb['title_match'] and rb['author_match'] and rb['license_match']
        rec['result']='VERIFIED_READBACK' if passed else 'READBACK_MISMATCH'
    except Exception as error:
        rec.update(result='READBACK_UNAVAILABLE',note_id=nid,error_type=type(error).__name__);passed=False
    atomic_json(out,rec)
    return rec,0 if passed else 1


def main(args=None):
    args=sys.argv[1:] if args is None else args
    if not args:print(__doc__);return 2
    try:
        opts,pos=options(args);result,code=run(opts,pos)
    except Refused as error:result={'result':'REFUSED','reason':str(error)};code=1
    except Exception as error:result={'result':'FAILED','error_type':type(error).__name__,'reason':'operation failed; inspect the minimal receipt, reconcile before any create retry'};code=1
    print(json.dumps(result,indent=1,ensure_ascii=False));return code


if __name__=='__main__':sys.exit(main())
