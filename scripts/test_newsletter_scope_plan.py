import hashlib,io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from newsletter_cpu import TextModel
class NativeScopePlanTests(unittest.TestCase):
 def response(self,content):return {'content':content,'stop_type':'eos','tokens':[42,128009]}
 def test_naturally_completed_own_analysis_precedes_and_binds_final_instance(self):
  plan=self.response('OWN_SCOPE_ANALYSIS: distinguish actual propositions from generic contemplated activity.');final=self.response('{"result":"decision"}')
  with tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',side_effect=[io.BytesIO(json.dumps(x).encode()) for x in (plan,final)]) as call:
   model=TextModel('.',folder,profile='review');result=model.ask('Trusted scope rules','EXACT_ORIGINAL_DRAFT',schema={'type':'object'},reasoning_effort='scope-plan')
   self.assertEqual(result,{'result':'decision'});self.assertEqual(call.call_count,2)
   first,last=[json.loads(c.args[0].data) for c in call.call_args_list];self.assertNotIn('json_schema',first);self.assertEqual(first['n_predict'],1800);self.assertIn('json_schema',last)
   self.assertIn('EXACT_ORIGINAL_DRAFT',first['prompt']);self.assertIn('EXACT_ORIGINAL_DRAFT',last['prompt']);self.assertNotIn('OWN_SCOPE_ANALYSIS',first['prompt']);self.assertIn('OWN_SCOPE_ANALYSIS',last['prompt']);self.assertIn('<|eot_id|><|start_header_id|>user',last['prompt'])
   rows=[json.loads(p.read_text()) for p in (Path(folder)/'model-outputs').glob('*.json')];raw_plan=next(x for x in rows if x['_ap_runtime']['phase']=='scope-analysis');answer=next(x for x in rows if x['_ap_runtime']['phase']=='scope-answer')
   digest=hashlib.sha256(json.dumps(raw_plan,sort_keys=True,ensure_ascii=False).encode()).hexdigest();self.assertEqual(answer['_ap_runtime']['parent_response_sha256'],digest);self.assertEqual(answer['_ap_runtime']['reasoning_effort'],'scope-plan')
 def test_partial_unexpected_channel_or_empty_plan_never_forces_a_final_decision(self):
  for change in ({'tokens':[]},{'tokens':[42,128256]},{'stop_type':'limit'},{'truncated':True},{'content':''},{'content':'<function=run>{}</function>'},{'content':'<|start_header_id|>assistant'}):
   plan=self.response('Complete plain-language scope analysis.');plan.update(change)
   with self.subTest(change=change),tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',return_value=io.BytesIO(json.dumps(plan).encode())) as call:
    with self.assertRaises(ValueError):TextModel('.',folder,profile='review').ask('Scope','Original',reasoning_effort='scope-plan')
    self.assertEqual(call.call_count,1);self.assertEqual(len(list((Path(folder)/'model-outputs').glob('*.json'))),1)
 def test_scope_plan_cannot_receive_source_or_peer_metadata(self):
  for data in ({'source_context':{'text':'SOURCE'}},{'comparison_context':{'peer':'CLAIM'}}):
   with self.subTest(data=data),tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen') as call:
    with self.assertRaises(ValueError):TextModel('.',folder,profile='review').ask('Scope','Original',reasoning_effort='scope-plan',**data)
    call.assert_not_called()
 def test_independent_request_never_inherits_another_completed_analysis(self):
  replies=[self.response('UNIQUE_FIRST_ANALYSIS'),self.response('{"ok":true}'),self.response('SECOND_ANALYSIS'),self.response('{"ok":true}')]
  with tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',side_effect=[io.BytesIO(json.dumps(x).encode()) for x in replies]) as call:
   model=TextModel('.',folder,profile='review');model.ask('A','Original',reasoning_effort='scope-plan');model.ask('B','Original',reasoning_effort='scope-plan')
   for c in call.call_args_list[2:]:self.assertNotIn('UNIQUE_FIRST_ANALYSIS',json.loads(c.args[0].data)['prompt'])
 def test_concurrent_reviewers_cannot_exchange_completed_analysis(self):
  import threading
  from concurrent.futures import ThreadPoolExecutor
  rendezvous=threading.Barrier(2)
  def response(request,**kw):
   data=json.loads(request.data);prompt=data['prompt'];owner='FIRST' if 'FIRST_CONTEXT' in prompt else 'SECOND';other='SECOND' if owner=='FIRST' else 'FIRST'
   if 'json_schema' not in data:
    rendezvous.wait(timeout=2);raw=self.response('COMPLETE_PLAN_FOR_'+owner)
   else:
    self.assertIn('COMPLETE_PLAN_FOR_'+owner,prompt);self.assertNotIn('COMPLETE_PLAN_FOR_'+other,prompt);raw=self.response('{"ok":true}')
   return io.BytesIO(json.dumps(raw).encode())
  with tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',side_effect=response):
   model=TextModel('.',folder,profile='review')
   with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(lambda owner:model.ask(owner,owner+'_CONTEXT',reasoning_effort='scope-plan'),('FIRST','SECOND')))
   self.assertEqual(results,[{'ok':True},{'ok':True}])
 def test_a_premature_json_verdict_cannot_masquerade_as_completed_plain_analysis(self):
  for content in ('{"kind":"no_factual_premise"}','[{"kind":"no_factual_premise"}]','```json\n{"kind":"no_factual_premise"}\n```'):
   with self.subTest(content=content),tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',side_effect=lambda *a,**k:io.BytesIO(json.dumps(self.response(content)).encode())) as call:
    with self.assertRaisesRegex(ValueError,'analysis'):TextModel('.',folder,profile='review').ask('Scope','Original',reasoning_effort='scope-plan')
    self.assertEqual(call.call_count,1)
