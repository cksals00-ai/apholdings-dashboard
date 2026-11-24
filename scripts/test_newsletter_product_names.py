import copy,unittest
from newsletter_grounding import retain_source_product_names,required_product_names
class ProductNameTests(unittest.TestCase):
 def test_observed_bedrock_transliteration_is_bound_to_original_name(self):
  source={'title':'Introducing India-based inference for Kimi K3 on Amazon Bedrock','text':'Official source evidence.'}
  draft={'title':'아마존 베드로크, 인도 기반 추론 도입','summary':'모델의 추론 위치를 발표했습니다.','fact':'새 기능을 소개합니다.','evidence':['unchanged literal source'],'image':{'hash':'keep'}}
  before=copy.deepcopy(draft);result=retain_source_product_names(draft,source)
  self.assertIn('Bedrock',result['title'])
  self.assertEqual({k:v for k,v in result.items() if k!='title'},{k:v for k,v in before.items() if k!='title'})
  self.assertEqual(draft,before)
 def test_already_retained_name_never_changes_accepted_copy(self):
  draft={'title':'기존 제목','summary':'Amazon Bedrock의 변경 발표','fact':'원문 사실','strong_review':{'supported':True}}
  self.assertEqual(retain_source_product_names(draft,{'title':'New Amazon Bedrock release'}),draft)
 def test_product_in_body_alone_cannot_be_invented_in_headline(self):
  draft={'title':'다른 소식','summary':'설명','fact':'사실'}
  self.assertEqual(retain_source_product_names(draft,{'title':'New research result','text':'Bedrock background mention'}),draft)
 def test_formatting_is_idempotent_and_never_approves_facts(self):
  draft={'title':'새로운 기능 발표','summary':'설명','fact':'입증되지 않은 효과','review':{'supported':False,'unsupported_claims':['효과 근거 없음']}}
  source={'title':'New Bedrock result'};one=retain_source_product_names(draft,source)
  self.assertEqual(retain_source_product_names(one,source),one);self.assertFalse(one['review']['supported'])
 def test_overlong_label_fails_instead_of_truncating_claim(self):
  with self.assertRaises(ValueError):retain_source_product_names({'title':'가'*89,'summary':'요약','fact':'사실'},{'title':'New Bedrock release'})
 def test_multiple_required_names_and_stale_receipt(self):
  d={'title':'새 소식','summary':'설명','fact':'사실','strong_review':{'supported':True}}
  out=retain_source_product_names(d,{'title':'Amazon Bedrock AgentCore update'})
  self.assertEqual(out['title'],'AgentCore / Bedrock · 새 소식');self.assertNotIn('strong_review',out)

class WriterProductNameTests(unittest.TestCase):
 def test_real_transliteration_no_longer_enters_whole_redraft_loop(self):
  from unittest.mock import Mock
  from newsletter_producer import draft_story
  from test_newsletter_grounding import GroundingTests
  source={**GroundingTests().source(),'title':'New Amazon Bedrock feature','source':'AWS','body_sha256':'hash'}
  story=GroundingTests().story();story['title']='아마존 베드로크 미리보기'
  wire={k:v for k,v in story.items() if k!='evidence'};wire['evidence_ids']=[0]
  model=Mock();model.ask.side_effect=[{'is_news':True,'is_duplicate':False,'novel_segment_id':0,'reason':'new'},wire,{'supported':True,'unsupported_claims':[]}]
  result=draft_story(model,source)
  self.assertIn('Bedrock',result['title']);self.assertEqual(model.ask.call_count,3)
  self.assertEqual(result['fact'],story['fact'])
 def test_structural_failure_preserves_exact_resolved_draft(self):
  from unittest.mock import Mock
  from newsletter_producer import draft_story
  from test_newsletter_grounding import GroundingTests
  source={**GroundingTests().source(),'title':'New feature','source':'Google','body_sha256':'hash'}
  story=GroundingTests().story();story['fact']='확인하지 않은 950% 효과입니다.'
  wire={k:v for k,v in story.items() if k!='evidence'};wire['evidence_ids']=[0]
  model=Mock();model.ask.side_effect=[{'is_news':True,'is_duplicate':False,'novel_segment_id':0,'reason':'new'},wire,{'supported':True,'unsupported_claims':[]}]
  with self.assertRaises(ValueError) as error:draft_story(model,source)
  self.assertEqual(error.exception.draft['fact'],story['fact']);self.assertEqual(error.exception.draft['source_hash'],'hash')
  self.assertEqual(model.ask.call_count,3)
