#!/usr/bin/env python3
"""Read-only independent v8.3 text, movement, provenance and anonymity checks."""
from pathlib import Path
import hashlib,json,re,subprocess,difflib,ast
from pypdf import PdfReader
R=Path(__file__).resolve().parents[3]
C=R.parents[1]/'v8-execution/v8.3-preflight/canon'
O=R/'results/v8.3/fidelity';O.mkdir(exist_ok=True)
build=json.loads((R/'results/v8.3/anonymous_build.json').read_text());pdf=Path(build['pdf'])
old=(C/'report/REPORT_OUTLINE.md').read_text();new=(R/'report/REPORT_OUTLINE.md').read_text()
def sections(s):
 a=re.split(r'^## (.+)\n',s,flags=re.M);return {a[i]:a[i+1].strip() for i in range(1,len(a),2)}
a,b=sections(old),sections(new);checks={}
e4="Both reference baselines were scored once each through the organizers' temporary evaluation queue during the Codabench outage [S13]; these runs are not on the leaderboard. The always-robust rule scored {{queue_always_true_k}}/{{queue_always_true_n}} (submission id {{queue_always_true_submission_id}}, {{queue_always_true_created_at_kst}} KST) and the length-and-digit control scored {{queue_text_length_control_k}}/{{queue_text_length_control_n}} (submission id {{queue_text_length_control_submission_id}}, {{queue_text_length_control_created_at_kst}} KST); each equals the fair-coin expectation and is not separable from it under the declared null."
checks['title_unchanged']=old.splitlines()[0]==new.splitlines()[0]
checks['section_order_exactly_E11']=list(b)==['Abstract','1. Task and the evidence a leaderboard supplies','2. A conditional analysis of the visible leaderboard','3. Exact power and an item-budget design target','Limitations and sensitivity directions','AI Use Statement','Source index','Appendix A. Supporting label audit and problem-only controls','Appendix B. Reproduction and assistance']
for key in ['1. Task and the evidence a leaderboard supplies','3. Exact power and an item-budget design target']:
 checks[key+'_word_for_word']=a[key]==b[key]
s2='2. A conditional analysis of the visible leaderboard'
checks['section2_only_country_to_KST_delta']=a[s2].replace('fetched on October 20 in Korea.','fetched on October 20 KST.')==b[s2]
checks['section2_3_not_shortened']=a[s2].split('### Results and the later removal announcement',1)[1]==b[s2].split('### Results and the later removal announcement',1)[1]
expected_abs=a['Abstract'].replace('labels. We do not identify which owners were affected. [S13]','labels. [S13] We do not identify which owners were affected.').replace('We provide CPU reproduction and frozen reference baselines whose private-validation results remain unmeasured.','We provide CPU reproduction rather than additional model runs. '+e4)
checks['abstract_only_E4_citation_and_declared_CPU_clause']=expected_abs==b['Abstract']
oldA=a['4. Supporting label audit and problem-only controls'];newA=b['Appendix A. Supporting label audit and problem-only controls']
oldblock=re.search(r'<!-- BEGIN_OWNER_PRIVATE_VALIDATION -->\n(.+?)\n<!-- END_OWNER_PRIVATE_VALIDATION -->',oldA,re.S).group(1)
newblock=e4+' Final-test performance of these bundles is also UNMEASURED. This owner-result limitation is separate from our observed analysis of the public board.'
expected_A=oldA.replace('The two frozen bundles are reference baselines (a constant rule and a surface-feature control), planned for one submission each when the service and owner session permit.','The two frozen bundles are reference baselines (a constant rule and a surface-feature control).').replace(oldblock,newblock).replace('Private-validation receipts are pending.','The recorded queue receipt JSONs accompany the reproduction archive.')
checks['AppendixA_word_for_word_except_reported_E4_status_delta']=expected_A==newA
checks['AppendixB_exact_moved_original_source']=a['6. Reproduction and assistance']==b['Appendix B. Reproduction and assistance']
oldlim=a['5. Limitations and sensitivity directions']
newlim=oldlim.replace('Private-validation receipts for our frozen reference baselines (a constant rule and a surface-feature control) remain pending; the report has no final-test outcomes.',e4+' The report has no final-test outcomes.').replace(' provide context for evaluation cautions while the owner measurements remain unavailable.',' provide context for evaluation cautions.')
checks['Limitations_only_E4_and_false_pending_cleanup']=newlim==b['Limitations and sensitivity directions']
checks['AI_statement_word_for_word']=a['AI Use Statement']==b['AI Use Statement']
refs=a['Source index'].replace('Original bytes, source hash and date-provenance notes accompany the evidence manifest in the reproduction archive.','The 24 October temporary-evaluation-queue notice is documented in the supplied v8.3 handoff; the recorded queue responses accompany the archive. Original bytes, source hash and date-provenance notes accompany the evidence manifest in the reproduction archive.')
checks['SourceIndex_only_declared_24Oct_notice_provenance']=refs==b['Source index']
def tables(s):return re.findall(r'(?:^\|[^\n]*\n)+',s,re.M)
ot,nt=tables(old),tables(new);checks['six_table_contents_byte_identical']=len(ot)==6 and ot==nt
oldclaims=json.loads((C/'research/claims.json').read_text())['claims'];newclaims=json.loads((R/'research/claims.json').read_text())['claims'];look={x['key']:x for x in newclaims}
checks['old152_claim_records_identical']=len(oldclaims)==152 and all(look.get(x['key'])==x for x in oldclaims)
checks['only12_new_receipt_keys']=len(newclaims)==164 and all(x['key'].startswith('queue_') for x in newclaims if x['key'] not in {y['key'] for y in oldclaims})
nums=json.loads((R/'results/report_numbers.json').read_text())
def get(key):
 x=nums
 for k in key.split('.'):x=x[k]
 return x
expected_draft=new.replace('<!-- BEGIN_OWNER_PRIVATE_VALIDATION -->','').replace('<!-- END_OWNER_PRIVATE_VALIDATION -->','')
expected_draft=re.sub(r'\{\{([A-Za-z0-9_.]+)\}\}',lambda m:str(get(m.group(1))),expected_draft)
checks['draft_is_checked_outline_render']=expected_draft.split()==(R/'report/REPORT_DRAFT.md').read_text().split()
for n in ['main.tex','main-anonymous.tex']:
 oldtex=(C/'report'/n).read_text();newtex=(R/'report'/n).read_text();tag='\\hypersetup{pdftitle='
 checks[n+'_preamble_style_fonts_margins_unchanged']=oldtex.split(tag,1)[0]==newtex.split(tag,1)[0]
anon=(R/'report/main-anonymous.tex').read_text();named=(R/'report/main.tex').read_text()
checks['anonymous_source_redactions_only_declared_variants']=anon.split('\\hypersetup{pdftitle=',1)[1].replace('Anonymous Author(s)','Jung Min Kang').replace('\\author{Jung Min Kang}','\\author{Jung Min Kang\\\\Independent}').replace('https://anonymous.4open.science/r/aimo-identifiability','https://github.com/testofschool/aimo-interp-abc').replace('[withheld for anonymous review]','\\texttt{'+'\\allowbreak{}'.join('6f81bc3b31472dfeb1179b25c31fd7bb128dd19f'[i:i+8] for i in range(0,40,8))+'}')==named.split('\\hypersetup{pdftitle=',1)[1]
# Sourcecommit anonymized masking is rendered as plain text; adjust expected only from declared marker ifneeded.
reader=PdfReader(pdf);metadata={str(k):str(v) for k,v in reader.metadata.items()};uris=[]
for i,page in enumerate(reader.pages,1):
 for ref in page.get('/Annots',[]):
  obj=ref.get_object();action=obj.get('/A')
  if action and '/URI' in action:uris.append({'page':i,'uri':str(action['/URI'])})
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
identity=['testofschool','gangjeongmin','Jung Min','Kang','Korea','Felix','6f81bc3b31472dfeb1179b25c31fd7bb128dd19f','/Users/felix']
scan=lambda value:[w for w in identity if re.search(r'\b'+re.escape(w)+r'\b',value,re.I)]
text_hits=scan(text);metadata_hits=scan(json.dumps(metadata));uri_hits=scan(json.dumps(uris))
checks['anonymous_pdf_text_identity_hits_zero']=not text_hits
checks['anonymous_pdf_metadata_identity_hits_zero']=not metadata_hits and metadata.get('/Author')=='Anonymous Author(s)'
checks['anonymous_pdf_link_targets_identity_hits_zero']=not uri_hits
checks['anonymous_mirror_URL_occurs_twice']=text.count('https://anonymous.4open.science/r/aimo-identifiability')==2
checks['PDF_total10_pages']=len(reader.pages)==10
page_text=[subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),'-layout',str(pdf),'-'],text=True) for i in range(1,len(reader.pages)+1)]
checks['main_body_exact5_pages_independent_boundary']=not any('Limitations and sensitivity directions' in t for t in page_text[:5]) and page_text[5].lstrip().startswith('Limitations and sensitivity directions')
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True);checks['Type3_zero']='Type 3' not in fonts
checks['locked_v3_gate_sha_unchanged']=hashlib.sha256((R/'tools/prize_rubric_gate.py').read_bytes()).hexdigest()=='152e2a488eb0c3cdeadbe4195bb09ac90acab464df4326a612098dc63f5c7630'
oldpdf=C/'report/aimo-interp-report-v8-anonymous.pdf';oldtext=subprocess.check_output(['pdftotext','-layout',str(oldpdf),'-'],text=True)
(O/'pdftotext_v8.1_to_v8.3_anonymous.diff').write_text(''.join(difflib.unified_diff(oldtext.splitlines(True),text.splitlines(True),fromfile='approved_v8.1_anonymous',tofile='built_v8.3_anonymous')))
(O/'anonymous_pdfinfo.txt').write_text(subprocess.check_output(['pdfinfo',str(pdf)],text=True));(O/'anonymous_pdffonts.txt').write_text(fonts)
(O/'anonymous_metadata_and_URIs.json').write_text(json.dumps({'metadata':metadata,'URIs':uris,'identity_counts':{'text':len(text_hits),'metadata':len(metadata_hits),'URIs':len(uri_hits)}},indent=2)+'\n')
result={'scope':'independent read-only fidelity/anonymous PDF audit','pdf':str(pdf),'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'checks':checks,'failed_checks':[k for k,v in checks.items() if not v],'result':'PASS' if all(checks.values()) else 'FAIL','old_claims':len(oldclaims),'new_claims':len(newclaims),'tables':len(nt),'visual_review':'PENDING_RECORD','mirror_verification':'PENDING_G_MIRROR_NOT_IN_T1','G_LOOK':'PENDING_HUMAN'}
(O/'MECHANICAL_FINAL.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
