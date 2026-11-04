import unittest
from newsletter_atomic_review import normalize_field, repair_fields
class AtomicReviewTests(unittest.TestCase):
 def decision(self,kind='supported'):
  return {'field':'fact','text':'공식 기능을 발표했다.','verdict':kind,'premises':[{'claim':'공식 기능을 발표했다.','status':'supported','source_ids':[0],'reason':'The source announces this feature.'}]}
 def test_generation_requires_one_disposition_for_every_sentence(self):
  from newsletter_review_spans import request_for,schema_for
  request=request_for('fact','공식 발표다. 별도 자격이 필요하다.','sourcehash');schema=schema_for(request)
  self.assertEqual(schema['properties']['sentences']['minItems'],2)
  self.assertEqual(schema['properties']['sentences']['maxItems'],2)
  self.assertNotIn('claim',schema['properties']['sentences']['items']['properties'])
 def test_supported_claim_requires_exact_source_ids(self):
  self.assertEqual(normalize_field(self.decision(),'fact','공식 기능을 발표했다.',1)['verdict'],'supported')
  x=self.decision();x['premises'][0]['source_ids']=[]
  with self.assertRaises(ValueError):normalize_field(x,'fact',x['text'],1)
 def test_contradictory_verdict_cannot_pass(self):
  x=self.decision();x['premises'][0]['status']='unsupported'
  with self.assertRaises(ValueError):normalize_field(x,'fact',x['text'],1)
 def test_advice_with_unsupported_premise_cannot_pass(self):
  x=self.decision('editorial');x['field']='insight';x['premises'][0]['status']='unsupported';x['premises'][0]['source_ids']=[]
  with self.assertRaises(ValueError):normalize_field(x,'insight',x['text'],1)
 def test_factual_fields_cannot_be_exempted_as_advice(self):
  x=self.decision('editorial');x['premises']=[]
  with self.assertRaises(ValueError):normalize_field(x,'fact',x['text'],1)
 def test_pure_conditional_advice_may_have_no_factual_premises(self):
  x={'field':'action','text':'조건을 확인한다.','verdict':'editorial','premises':[]}
  self.assertEqual(normalize_field(x,'action',x['text'],1),x)
 def test_stale_or_fabricated_span_fails(self):
  x=self.decision();x['text']='다른 문장'
  with self.assertRaises(ValueError):normalize_field(x,'fact','공식 기능을 발표했다.',1)
 def test_targeted_repair_preserves_every_other_field_and_assets(self):
  old={'fact':'오류 주장','title':'유지 제목','image':{'sha256':'keep'},'evidence':['literal source']}
  out=repair_fields(old,{'fact':'수정 사실'},['fact'])
  self.assertEqual(out['image'],old['image']);self.assertEqual(out['title'],old['title']);self.assertEqual(old['fact'],'오류 주장')
 def test_repair_cannot_replace_accepted_or_unknown_fields(self):
  for patch in ({'title':'불필요 변경'},{'fact':'수정','image':'bad'},{'fact':''}):
   with self.assertRaises(ValueError):repair_fields({'fact':'오류','title':'유지'},patch,['fact'])
if __name__=='__main__':unittest.main()

class AuditTests(unittest.TestCase):
 def setUp(self):
  from unittest.mock import patch
  from test_newsletter_speech_acts import fixture_inventory
  self.enterContext(patch('newsletter_speech_acts.classify',side_effect=fixture_inventory))
 def test_independent_audit_rejects_supported_rationale_contradiction(self):
  from unittest.mock import Mock
  from newsletter_atomic_review import review_fields,FIELDS
  story={f:'공식 기능 발표' for f in FIELDS};model=Mock()
  import json
  def answer(system,question,**kw):
   if 'consistent' in kw['schema']['properties']:return {'consistent':False,'complete':True,'reason':'One rationale contradicts the source.','issues':[]}
   request=json.loads(question);return {'input_hash':request['input_hash'],'sentences':[{'id':x['id'],'status':'supported','source_ids':[0],'reason':'Claim supported by official announcement.'} for x in request['spans']]}
  model.ask.side_effect=answer
  with self.assertRaisesRegex(ValueError,'consistency'):review_fields(model,story,{'source_segments':[{'id':0,'text':'Official evidence'}]})
  self.assertEqual(model.ask.call_count,6)
 def test_repair_calls_14b_with_only_rejected_field_schema(self):
  from unittest.mock import Mock
  from newsletter_atomic_review import targeted_repair
  story={'fact':'오류 주장','title':'그대로','image':{'hash':'keep'}}
  review={'fields':[{'field':'fact','text':'오류 주장','verdict':'unsupported','premises':[{'claim':'오류 주장','reason':'Not in source'}]}]}
  model=Mock();model.ask.return_value={'fact':'원문 사실'}
  out=targeted_repair(model,story,review,{'source_segments':[]})
  self.assertEqual(out['title'],'그대로');self.assertEqual(out['image'],story['image'])
  self.assertEqual(set(model.ask.call_args.kwargs['schema']['properties']),{'fact'})

class DecisionRepairTests(unittest.TestCase):
 def setUp(self):
  from unittest.mock import patch
  from test_newsletter_speech_acts import fixture_inventory
  self.enterContext(patch('newsletter_speech_acts.classify',side_effect=fixture_inventory))
 def run_review(self,second_audit_clean=True):
  import json,copy
  from unittest.mock import Mock
  from newsletter_atomic_review import review_fields,FIELDS
  story={f:'공식 기능 발표' for f in FIELDS};story['insight']='AP가 설계한다면 권한 분리를 검토할 수 있다.';before=copy.deepcopy(story);counts={};audits=[]
  def answer(system,question,**kw):
   q=json.loads(question)
   if 'consistent' in kw['schema']['properties']:
    audits.append(q)
    if len(audits)>1 and second_audit_clean:return {'consistent':True,'complete':True,'reason':'Every factual premise and editorial distinction verified.','issues':[]}
    return {'consistent':False,'complete':True,'reason':'Conditional proposal mistaken for asserted AP adoption.','issues':[{'field':'fact','span_id':0,'reason':'This is hypothetical advice, not an asserted AP outcome.'}]}
   f=q['field'];counts[f]=counts.get(f,0)+1
   status='unsupported' if f=='fact' and counts[f]==1 else 'editorial' if False else 'supported'
   return {'input_hash':q['input_hash'],'sentences':[{'id':x['id'],'status':status,'source_ids':[0] if status=='supported' else [],'reason':'Source lacks AP adoption evidence.' if status=='unsupported' else 'Conditional proposal only.' if status=='editorial' else 'Official source supports the factual statement.'} for x in q['spans']]}
  model=Mock();model.ask.side_effect=answer
  if second_audit_clean:
   out=review_fields(model,story,{'source_segments':[{'id':0,'text':'Official feature announcement.'}]})
   self.assertTrue(out['supported']);self.assertEqual(len(out['decision_history']),2)
  else:
   with self.assertRaisesRegex(ValueError,'consistency'):review_fields(model,story,{'source_segments':[{'id':0,'text':'Official feature announcement.'}]})
  self.assertEqual(counts,{f:2 if f=='fact' else 1 for f in FIELDS if f!='insight'});self.assertEqual(len(audits),2);self.assertEqual(story,before)
 def test_only_audit_flagged_decision_rechecked_then_full_fresh_audit(self):self.run_review()
 def test_remaining_audit_error_never_passes_or_retries_forever(self):self.run_review(False)
