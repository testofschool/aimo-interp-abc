#!/usr/bin/env python3
"""Local fake-client tests. No real credentials, SDK client, or network."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import ssl
import subprocess
import urllib.error
import tempfile
import types
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

gate=load('or_payload_gate');post=load('or_post')


def field(kind,**kwargs):return {'value':{'param':{'type':kind,**kwargs}}}


def fixture():
    inv={'id':gate.INV_ID,'cdate':0,'duedate':9999999999998,'expdate':9999999999999,'tmdate':1,'edit':{'note':{'content':{
        'title':field('string',regex='^.{1,250}$'),'abstract':field('string',maxLength=5000),
        'authors':field('author{}',properties={'fullname':{'param':{'type':'string'}},'username':{'param':{'type':'string','regex':r'^~\S+$'}},'institutions':{'param':{'type':'object{}','optional':True,'properties':{'name':{'param':{'type':'string'}}}}}}),
        'reciprocal_reviewers':field('profile[]',regex=r'^~\S+$'),'keywords':field('string[]'),
        'voluntary_reviewers':field('profile[]',optional=True),'TLDR':field('string',optional=True,maxLength=250),
        'pdf':field('file',extensions=['pdf'],maxSize=50),
        'leaderboard_submission_ids':field('string',regex=r'^\s*[^\s,]+\s*(,\s*[^\s,]+\s*)?$'),
        'rules_no_duplicates':field('string',enum=['Synthetic exact acknowledgement.']),
        'ai_assistance':field('string[]',items=[{'value':x} for x in ['Ideation','Coding','Analysis','Writing','No AI assistance was used']]),
        'venueid':{'value':{'param':{'const':post.VENUEID,'hidden':True}}}
    }}}}
    payload={'title':'SYNTHETIC FIXTURE ONLY','abstract':'SYNTHETIC content.','authors':[{'fullname':'Fictional Person','username':'~Synthetic_Author1'}],'reciprocal_reviewers':['~Synthetic_Author1'],'keywords':['synthetic'],'leaderboard_submission_ids':'1012526, 1012549','ai_assistance':['Ideation','Coding','Analysis','Writing']}
    return inv,payload


class Note:
    def __init__(self,**kwargs):self.__dict__.update(kwargs)


class FakeClient:
    def __init__(self,inv,pdf,prior=None,principal='~Synthetic_Author1'):
        self.inv=copy.deepcopy(inv);self.pdf=pdf;self.prior=prior or [];self.principal=principal
        self.profile=types.SimpleNamespace(id=principal)
        self.puts=0;self.posts=0;self.queries=[];self.return_wrong_pdf=False;self.ambiguous=False;self.query_error=False
        class Retry:
            def __init__(self,total=5):self.total=total
            def new(self,**kwargs):return Retry(kwargs['total'])
        retry=Retry()
        self.session=types.SimpleNamespace(adapters={'https':types.SimpleNamespace(max_retries=retry)})
        self.notes={};self.at_post=None
    def get_profile(self,*args,**kwargs):raise AssertionError('unfiltered directory lookup must never establish principal')
    def get_notes(self,invitation=None,content=None,tauthor=None,domain=None,trash=None,limit=None,offset=None,with_count=None):
        if self.query_error:raise PermissionError('SYNTHETIC_PRIVATE_ERROR')
        self.queries.append({'invitation':invitation,'content':content,'tauthor':tauthor,'domain':domain,'trash':trash,'offset':offset})
        rows=self.prior
        page=rows[(offset or 0):(offset or 0)+(limit or 1000)]
        return (page,len(rows)) if with_count and offset is None else page
    def get_invitation(self,id):return types.SimpleNamespace(to_json=lambda:copy.deepcopy(self.inv))
    def put_attachment(self,*args):self.puts+=1;return '/attachment/SYNTHETIC_PRIVATE_REFERENCE.pdf'
    def post_note_edit(self,invitation,signatures,note):
        self.posts+=1
        if self.at_post:self.at_post()
        if self.ambiguous:raise TimeoutError('SYNTHETIC_PRIVATE_ERROR')
        nid=getattr(note,'id','SYNTHETIC_NOTE')
        note.id=nid;note.forum=nid;note.tmdate=10;note.cdate=1;note.invitations=[post.INV_ID]
        self.notes[nid]=note
        return {'id':'SYNTHETIC_EDIT','tmdate':10,'note':{'id':nid}}
    def get_note(self,id):return self.notes[id]
    def get_attachment(self,**kwargs):return b'%PDF-WRONG' if self.return_wrong_pdf else self.pdf


class HardeningTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='synthetic-or-hardening-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.inv,self.payload=fixture()
        self.pdf=self.root/'synthetic.pdf';self.pdf.write_bytes(b'%PDF-1.4\nSYNTHETIC FIXTURE ONLY\n')
        self.payload['pdf']=str(self.pdf);self.path=self.root/'payload.json'
        self.out=self.root/'POST.json';self.state=self.root/'private'
    def save(self):self.path.write_text(json.dumps(self.payload))
    def validate(self):return gate.validate(self.inv,self.payload,self.root)
    def execute(self,client,opts=None):
        self.save();options={'--out':str(self.out)};options.update(opts or {})
        return post.run(options,[str(self.path)],client_factory=lambda user:(client,Note),state_dir=self.state)
    def test_ssl_fetch_falls_back_to_bounded_verified_curl(self):
        failure=urllib.error.URLError(ssl.SSLCertVerificationError('SYNTHETIC_CHAIN_ERROR'))
        response=subprocess.CompletedProcess([],0,stdout=json.dumps({'invitations':[self.inv],'count':1}).encode(),stderr=b'')
        with mock.patch.object(gate.urllib.request,'urlopen',side_effect=failure),mock.patch.object(gate.subprocess,'run',return_value=response) as curl:
            self.assertEqual(gate.fetch_inv()['id'],gate.INV_ID)
        args=curl.call_args.args[0]
        self.assertEqual(args[:2],['/usr/bin/curl','--disable']);self.assertNotIn('-k',args);self.assertNotIn('--insecure',args)
        self.assertEqual(curl.call_args.kwargs['timeout'],30)
        self.assertEqual(gate.LAST_FETCH_ROUTE,'curl_verified_after_urllib_tls_failure')
    def test_failed_verified_fallback_is_explicit_and_does_not_echo_errors(self):
        failure=urllib.error.URLError(ssl.SSLCertVerificationError('SYNTHETIC_SECRET'))
        response=subprocess.CompletedProcess([],60,stdout=b'',stderr=b'SYNTHETIC_SECRET')
        with mock.patch.object(gate.urllib.request,'urlopen',side_effect=failure),mock.patch.object(gate.subprocess,'run',return_value=response):
            with self.assertRaises(gate.FetchFailure) as raised:gate.fetch_inv()
        self.assertIn('verified curl fallback failed',str(raised.exception));self.assertNotIn('SYNTHETIC_SECRET',str(raised.exception))
    def test_exact_autofill_current_shapes(self):
        result,filled=self.validate();self.assertEqual(result['result'],'PASS',result)
        self.assertEqual(filled['rules_no_duplicates'],'Synthetic exact acknowledgement.')
        self.assertNotIn('venueid',filled)
    def test_unsupported_malformed_and_empty_required_rejected(self):
        for spec,value in [(field('number'),42),({},'x'),(field('string',regex='['),'x')]:
            with self.subTest(spec=spec):
                inv=copy.deepcopy(self.inv);inv['edit']['note']['content']['future']=spec
                payload=copy.deepcopy(self.payload);payload['future']=value
                self.assertEqual(gate.validate(inv,payload,self.root)[0]['result'],'FAIL')
        self.payload['abstract']='  ';self.assertEqual(self.validate()[0]['result'],'FAIL')
    def test_expired_due_opening_and_expiration_rejected(self):
        for dates in [{'duedate':1},{'expdate':1},{'cdate':9999999999999}]:
            with self.subTest(dates=dates):
                inv=copy.deepcopy(self.inv);inv.update(dates)
                self.assertEqual(gate.validate(inv,self.payload,self.root)[0]['result'],'FAIL')
    def test_file_signature_nested_properties_and_bad_username_rejected(self):
        self.pdf.write_bytes(b'not a PDF');self.assertEqual(self.validate()[0]['result'],'FAIL')
        self.pdf.write_bytes(b'%PDF-1.4\n')
        for mutation in [lambda a:a.update(institutions='wrong'),lambda a:a.update(institutions=[{'name':3}]),lambda a:a.update(username=42)]:
            payload=copy.deepcopy(self.payload);mutation(payload['authors'][0])
            self.assertEqual(gate.validate(self.inv,payload,self.root)[0]['result'],'FAIL')
    def test_wrong_ids_and_reciprocal_reviewer_rejected(self):
        self.payload['leaderboard_submission_ids']=['1012526'];self.assertEqual(self.validate()[0]['result'],'FAIL')
        self.payload['leaderboard_submission_ids']='1012526, 1012549';self.payload['reciprocal_reviewers']=['~Unrelated1']
        self.assertEqual(self.validate()[0]['result'],'FAIL')
    def test_dry_run_never_constructs_client(self):
        self.save()
        with mock.patch.object(post,'terminal_client',side_effect=AssertionError('no login')),mock.patch.object(gate,'fetch_inv',return_value=self.inv),mock.patch.object(post,'load_gate',return_value=gate):
            result,code=post.run({'--dry-run':True},[str(self.path)])
        self.assertEqual((code,result['result']),(0,'DRY_RUN'))
    def test_first_author_must_be_authenticated_principal(self):
        client=FakeClient(self.inv,self.pdf.read_bytes(),principal='~Other1')
        with self.assertRaises(post.Refused):self.execute(client)
        self.assertEqual((client.puts,client.posts),(0,0))
    def test_absent_or_malformed_authenticated_profile_blocks_before_any_write(self):
        for profile in [None,{},types.SimpleNamespace(id=None),types.SimpleNamespace(id='email@example.invalid'),types.SimpleNamespace(id=42),types.SimpleNamespace(id='~bad id')]:
            with self.subTest(profile=profile):
                client=FakeClient(self.inv,self.pdf.read_bytes());client.profile=profile
                with self.assertRaises(post.Refused):self.execute(client)
                self.assertEqual((client.puts,client.posts),(0,0));self.assertEqual(client.queries,[])
    def test_stale_enum_payload_rechecked_before_any_write(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());self.payload['rules_no_duplicates']='Old acknowledgement.'
        result,code=self.execute(client)
        self.assertEqual((code,result['result']),(1,'REFUSED'));self.assertEqual((client.puts,client.posts),(0,0))
    def test_creation_queries_live_and_trash_and_boolean_author_scope(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());result,code=self.execute(client)
        self.assertEqual((code,result['result']),(0,'VERIFIED_READBACK'),result)
        self.assertEqual(len(client.queries),6);self.assertEqual({q['trash'] for q in client.queries},{False,True})
        authored=[q for q in client.queries if q['tauthor'] is not None]
        self.assertEqual(len(authored),2);self.assertTrue(all(q['tauthor'] is True and q['domain']==post.VENUE for q in authored))
        self.assertEqual(client.session.adapters['https'].max_retries.total,0)
        self.assertNotIn('SYNTHETIC_PRIVATE_REFERENCE',self.out.read_text())
        self.assertTrue(result['readback']['ids_match'] and result['readback']['title_match'] and result['match_pdf'])
    def test_mismatch_returns_nonzero_with_known_note_id(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());client.return_wrong_pdf=True
        result,code=self.execute(client)
        self.assertEqual(code,1);self.assertEqual(result['result'],'READBACK_MISMATCH');self.assertFalse(result['match_pdf']);self.assertEqual(result['note_id'],'SYNTHETIC_NOTE')
    def test_prior_note_for_first_author_or_ambiguous_metadata_refuses(self):
        for authors in [[{'username':'~Synthetic_Author1'}],['Anonymous']]:
            prior=Note(id='PRIOR',content={'authors':{'value':authors},'venueid':{'value':post.VENUEID}},invitations=[post.INV_ID])
            client=FakeClient(self.inv,self.pdf.read_bytes(),prior=[prior])
            with self.subTest(authors=authors),self.assertRaises(post.Refused):self.execute(client)
            self.assertEqual((client.puts,client.posts),(0,0))
    def test_permission_error_fails_closed(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());client.query_error=True
        with self.assertRaises(PermissionError):self.execute(client)
        self.assertEqual((client.puts,client.posts),(0,0))
    def test_unknown_creation_outcome_blocks_next_attempt_before_login(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());client.ambiguous=True
        def durable_before_request():
            self.assertEqual(json.loads(self.out.read_text())['result'],'REQUEST_IN_FLIGHT')
            self.assertEqual(len(list(self.state.glob('creation-intent-*'))),1)
        client.at_post=durable_before_request
        result,code=self.execute(client);self.assertEqual((code,result['result']),(1,'WRITE_OUTCOME_UNCERTAIN'))
        with mock.patch.object(post,'terminal_client',side_effect=AssertionError('no second login')):
            with self.assertRaises(post.Refused):post.run({'--out':str(self.root/'DIFFERENT_RECEIPT.json')},[str(self.path)],state_dir=self.state)
        self.assertEqual(client.posts,1)
        self.assertNotIn('SYNTHETIC_PRIVATE_ERROR',self.out.read_text())
    def test_readback_has_all_matches_and_makes_no_remote_writes(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());self.execute(client)
        client.puts=client.posts=0
        result,code=self.execute(client,{'--readback':'SYNTHETIC_NOTE','--expect-pdf-sha256':post.digest(self.pdf.read_bytes())})
        self.assertEqual((code,result['result']),(0,'VERIFIED_READBACK'));self.assertTrue(result['ids_match'] and result['title_match'])
        self.assertEqual((client.puts,client.posts),(0,0))
    def test_readback_wrong_ids_or_title_returns_nonzero_without_writes(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());self.execute(client)
        client.puts=client.posts=0
        client.notes['SYNTHETIC_NOTE'].content['leaderboard_submission_ids']={'value':'999999'}
        client.notes['SYNTHETIC_NOTE'].content['title']={'value':'Wrong title'}
        result,code=self.execute(client,{'--readback':'SYNTHETIC_NOTE'})
        self.assertEqual(code,1);self.assertFalse(result['ids_match']);self.assertFalse(result['title_match'])
        self.assertEqual((client.puts,client.posts),(0,0))
    def test_incomplete_prior_note_query_blocks_creation(self):
        client=FakeClient(self.inv,self.pdf.read_bytes())
        def incomplete(invitation=None,content=None,tauthor=None,domain=None,trash=None,limit=None,offset=None,with_count=None):
            return ([],1) if with_count else []
        client.get_notes=incomplete
        with self.assertRaises(post.Refused):self.execute(client)
        self.assertEqual((client.puts,client.posts),(0,0))
    def test_wrong_license_is_reported_and_returns_nonzero(self):
        client=FakeClient(self.inv,self.pdf.read_bytes());self.execute(client)
        client.puts=client.posts=0;client.notes['SYNTHETIC_NOTE'].license='Wrong license'
        result,code=self.execute(client,{'--readback':'SYNTHETIC_NOTE'})
        self.assertEqual(code,1);self.assertFalse(result['readback']['license_match'])
        self.assertEqual(result['readback']['license'],'Wrong license')
        self.assertTrue(result['ids_match'] and result['title_match'] and result['match_pdf'])
        self.assertEqual((client.puts,client.posts),(0,0))
    def test_installed_sdk_serializes_boolean_author_query(self):
        try:
            from openreview.api import OpenReviewClient
        except ModuleNotFoundError:
            self.skipTest('run this serialization probe with installed /Users/felix/orvenv/bin/python')
        captured={}
        response=types.SimpleNamespace(json=lambda:{'notes':[],'count':0})
        def get(url,params,headers):captured.update(params);return response
        fake=types.SimpleNamespace(session=types.SimpleNamespace(get=get),notes_url='https://api2.openreview.net/notes',headers={},_OpenReviewClient__handle_response=lambda r:r)
        rows,count=OpenReviewClient.get_notes(fake,tauthor=True,domain=post.VENUE,trash=True,limit=1000,with_count=True)
        self.assertEqual((rows,count),([],0));self.assertEqual(captured['tauthor'],'true')
        self.assertEqual(captured['trash'],'true');self.assertEqual(captured['domain'],post.VENUE)
    def test_revision_target_ownership_and_full_content_preserved(self):
        client=FakeClient(self.inv,self.pdf.read_bytes())
        content={k:{'value':v} for k,v in self.payload.items()};content['venueid']={'value':post.VENUEID};content['TLDR']={'value':'Preserve this optional sentence.','readers':['~Synthetic_Author1']}
        target=Note(id='KNOWN',content=content,invitations=[post.INV_ID]);client.notes['KNOWN']=target
        result,code=self.execute(client,{'--revise':'KNOWN'})
        self.assertEqual(code,0,result);self.assertEqual(client.notes['KNOWN'].content['TLDR'],content['TLDR'])
        client.notes['KNOWN'].content['authors']={'value':[{'username':'~Other1'}]}
        with self.assertRaises(post.Refused):self.execute(client,{'--revise':'KNOWN'})
    def test_no_token_password_argument_or_nontty_environment_login(self):
        for args in [['x','--token','SYNTHETIC_SECRET'],['x','--password','SYNTHETIC_SECRET'],['x','--trial']]:
            with self.subTest(args=args),self.assertRaises(post.Refused):post.options(args)
        with mock.patch.object(sys,'stdin',io.StringIO('')),mock.patch.dict(os.environ,{'OPENREVIEW_PASSWORD':'SYNTHETIC_SECRET'}),mock.patch.object(getattr(post,'getpass'),'getpass',side_effect=AssertionError('no prompt')):
            with self.assertRaises(post.Refused):post.terminal_client('synthetic@example.invalid')
        output=io.StringIO()
        with contextlib.redirect_stdout(output):code=post.main(['x','--token','SYNTHETIC_SECRET'])
        self.assertEqual(code,1);self.assertNotIn('SYNTHETIC_SECRET',output.getvalue())


if __name__=='__main__':unittest.main()
