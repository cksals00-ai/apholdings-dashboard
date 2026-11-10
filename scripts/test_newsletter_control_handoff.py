import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter_control_handoff as h
class VerifiedControlHandoffTests(unittest.TestCase):
 def execution(self):
  runtime='a'*40;head='b'*40;workflow=('ref: '+runtime+'\n').encode();digest=hashlib.sha256(workflow).hexdigest()
  run={'id':123,'status':'completed','conclusion':'success','run_attempt':1,'event':'workflow_dispatch','path':h.WORKFLOW,'head_sha':head,'head_repository':{'full_name':h.REPO}}
  jobs={'total_count':2,'jobs':[{'name':f'controls ({mode}, --{mode}-only)','status':'completed','conclusion':'success','steps':[{'name':f'Verify {mode} controls on fixed public CPU verifier','conclusion':'success'}]} for mode in ('scope','historical')]}
  return run,jobs,workflow,head,runtime,digest
 def test_both_actual_jobs_and_exact_definition_runtime_are_required(self):
  args=self.execution();h.verify_execution(*args,source_run=123)
  for key,value in (('status','in_progress'),('conclusion','failure'),('head_sha','c'*40),('run_attempt',2)):
   bad=copy.deepcopy(args[0]);bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):h.verify_execution(bad,*args[1:],source_run=123)
  bad=copy.deepcopy(args[1]);bad['jobs'].pop()
  with self.assertRaises(ValueError):h.verify_execution(args[0],bad,*args[2:],source_run=123)
  bad=copy.deepcopy(args[1]);bad['jobs'][1]['conclusion']='skipped'
  with self.assertRaises(ValueError):h.verify_execution(args[0],bad,*args[2:],source_run=123)
  with self.assertRaises(ValueError):h.verify_execution(args[0],args[1],b'changed',*args[3:],source_run=123)
 def proof(self):
  from newsletter_scope_controls import CASES
  from newsletter_speech_acts import REVISION
  draft={'title':'새 도구를 발표했다.','summary':'새 도구를 발표했다.','fact':'새 도구를 발표했다.','insight':'필요하다면 적용을 검토할 수 있다.','action':' '.join(CASES)}
  digest=h.scope_hash(draft)
  state={'date':'2026-11-10','mode':'test','asset_day':'2026-11-10-test-123','historical_controls_only':True,'scope_only':True,'historical_only':False}
  proof={'synthetic_regression_only':True,'draft':draft,'receipt':{'revision':REVISION,'reasoning_effort':'medium','input_hash':digest,'coverage_audit':{'complete':True,'issues':[]},'independent_decisions':[{'input_hash':digest},{'input_hash':digest}]}}
  payload=h.scope_payload(draft)
  requests=[{'field':row['field'],'id':row['id'],'input_hash':h.focused_request(payload,row)['input_hash']} for row in payload['sentences']]
  for vote in proof['receipt']['independent_decisions']:vote['requests']=copy.deepcopy(requests)
  history={**state,'scope_only':False,'historical_only':True,'frozen_control_receipts':{'a':'receipt'}}
  return state,proof,history
 def test_stale_scope_or_unverified_history_cannot_be_imported(self):
  scope,proof,history=self.proof()
  with patch.object(h,'controls_valid',return_value=True):h.verify_artifacts(scope,proof,history,123,'2026-11-10')
  bad=copy.deepcopy(proof);bad['receipt']['input_hash']='stale'
  with patch.object(h,'controls_valid',return_value=True),self.assertRaises(ValueError):h.verify_artifacts(scope,bad,history,123,'2026-11-10')
  with patch.object(h,'controls_valid',return_value=False),self.assertRaises(ValueError):h.verify_artifacts(scope,proof,history,123,'2026-11-10')
  bad=copy.deepcopy(proof);bad['receipt']['independent_decisions'][1]['requests'][0]['input_hash']='another target or context'
  with patch.object(h,'controls_valid',return_value=True),self.assertRaises(ValueError):h.verify_artifacts(scope,bad,history,123,'2026-11-10')
  bad=copy.deepcopy(proof);bad['receipt']['coverage_audit']['issues']=[{'reason':'missing quantifier'}]
  with patch.object(h,'controls_valid',return_value=True),self.assertRaises(ValueError):h.verify_artifacts(scope,bad,history,123,'2026-11-10')
  bad=copy.deepcopy(proof);bad['receipt']['reasoning_effort']='low'
  with patch.object(h,'controls_valid',return_value=True),self.assertRaises(ValueError):h.verify_artifacts(scope,bad,history,123,'2026-11-10')
 def test_install_preserves_news_and_images_and_never_targets_regular_production(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);state=root/'.production-state/draft.json';state.parent.mkdir()
   draft={'date':'2026-11-10','mode':'test','asset_day':'2026-11-10-test-999','stories':[{'fact':'preserved'}],'art_plans':[{'scene':'preserved'}]};state.write_text(json.dumps(draft))
   h.install(root,'2026-11-10','999',{'control':'verified'},{'source_run':123})
   installed=json.loads(state.read_text());self.assertEqual(installed['stories'],draft['stories']);self.assertEqual(installed['art_plans'],draft['art_plans'])
   self.assertEqual(installed['frozen_control_receipts'],{'control':'verified'})
   draft['mode']='production';state.write_text(json.dumps(draft));before=state.read_bytes()
   with self.assertRaises(ValueError):h.install(root,'2026-11-10','999',{},{} )
   self.assertEqual(state.read_bytes(),before)

 def test_raw_control_evidence_is_preserved_with_the_private_test_checkpoint(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder)/'test';state=root/'.production-state/draft.json';state.parent.mkdir(parents=True)
   state.write_text(json.dumps({'date':'2026-11-10','mode':'test','asset_day':'2026-11-10-test-999'}))
   evidence=Path(folder)/'evidence';raw=evidence/'scope/model-outputs/raw.json';raw.parent.mkdir(parents=True);raw.write_bytes(b'actual native receipt')
   h.install(root,'2026-11-10','999',{}, {'source_run':123},evidence=evidence)
   self.assertEqual((root/'.production-state/qualified-control-evidence/scope/model-outputs/raw.json').read_bytes(),raw.read_bytes())

class ControlExecutionCalendarTests(unittest.TestCase):
 def jobs(self):
  return {'jobs':[{'name':f'controls ({mode}, --{mode}-only)','steps':[{'name':f'Verify {mode} controls on fixed public CPU verifier','started_at':'2026-11-10T14:00:00Z'}]} for mode in ('scope','historical')]}
 def test_synthetic_proof_keeps_actual_execution_day_when_rehearsal_is_next_day(self):
  self.assertEqual(h.execution_days(self.jobs(),'2026-11-11'),{'scope':'2026-11-10','historical':'2026-11-10'})
 def test_unknown_unzoned_or_future_execution_day_is_not_guessed(self):
  for value in (None,'2026-11-10T14:00:00','2026-11-12T14:00:00Z','bad'):
   jobs=self.jobs();jobs['jobs'][0]['steps'][0]['started_at']=value
   with self.subTest(value=value),self.assertRaises(ValueError):h.execution_days(jobs,'2026-11-11')
 def test_proof_day_must_match_real_job_even_when_install_day_differs(self):
  helper=VerifiedControlHandoffTests();scope,proof,history=helper.proof()
  with patch.object(h,'controls_valid',return_value=True):h.verify_artifacts(scope,proof,history,123,'2026-11-11',control_days={'scope':'2026-11-10','historical':'2026-11-10'})
  with patch.object(h,'controls_valid',return_value=True),self.assertRaises(ValueError):h.verify_artifacts(scope,proof,history,123,'2026-11-11',control_days={'scope':'2026-11-11','historical':'2026-11-10'})
