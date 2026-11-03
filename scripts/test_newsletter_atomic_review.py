import unittest
from newsletter_atomic_review import normalize_field, repair_fields
class AtomicReviewTests(unittest.TestCase):
 def decision(self,kind='supported'):
  return {'field':'fact','text':'공식 기능을 발표했다.','verdict':kind,'premises':[{'claim':'공식 기능을 발표했다.','status':'supported','source_ids':[0],'reason':'The source announces this feature.'}]}
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
 def test_independent_audit_rejects_supported_rationale_contradiction(self):
  from unittest.mock import Mock
  from newsletter_atomic_review import review_fields,FIELDS
  story={f:'공식 기능 발표' for f in FIELDS};model=Mock()
  model.ask.side_effect=[{'field':f,'text':story[f],'verdict':'supported','premises':[{'claim':story[f],'status':'supported','source_ids':[0],'reason':'Claim supported by official announcement.'}]} for f in FIELDS]+[{'consistent':False,'complete':True,'reason':'One rationale contradicts the source.'}]
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
