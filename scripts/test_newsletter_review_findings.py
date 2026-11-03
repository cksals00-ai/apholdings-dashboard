import unittest
from unittest.mock import Mock
from newsletter_copy_repair import verify
import newsletter_schemas as shapes

class StrongFindingsTests(unittest.TestCase):
 def fixture(self):
  source={'title':'New AgentCore result','text':'AgentCore now provides role-scoped tools in a newly reported customer implementation.','body_sha256':'abc'}
  story={k:'AgentCore 구현 사례를 확인합니다.' for k in ('title','summary','fact')}
  story.update(insight='AP가 서비스를 설계한다면 조회와 변경 권한을 나누는 방식을 검토할 수 있다.',action='지역별 제공 조건을 확인한다.',evidence=[source['text']],image_prompt='ink keys',image_subject='keys',visual_approach='ink')
  return source,story
 def model(self,source,findings):
  m=Mock();m.ask.side_effect=[{'is_news':True,'is_duplicate':False,'novel_quote':source['text'],'reason':'new implementation'},findings];return m
 def test_empty_explicit_findings_accept_conditional_proposal(self):
  source,story=self.fixture();m=self.model(source,{'findings':[]});verify(m,story,source,[])
  self.assertTrue(story['strong_review']['supported']);self.assertEqual(story['strong_review']['review']['unsupported_claims'],[])
  self.assertEqual(m.ask.call_args.kwargs['schema'],shapes.STRONG_REVIEW)
 def test_specific_false_premise_in_advice_rejected(self):
  source,story=self.fixture();story['action']='학습 효과가 모든 학생에게 입증됐으므로 전면 적용한다.'
  finding={'field':'action','assertion':story['action'],'factual_premise':'학습 효과가 모든 학생에게 입증됐다','source_mismatch':'원문은 구현 사례이며 학습 효능을 입증하지 않는다.','correction':'보편적 학습 효과가 입증됐다는 전제를 삭제한다.'}
  with self.assertRaisesRegex(ValueError,'학습 효과'):verify(self.model(source,{'findings':[finding]}),story,source,[])
  self.assertNotIn('strong_review',story)
 def test_missing_or_misbound_findings_fail_closed(self):
  for response in ({'supported':True,'unsupported_claims':['제안']},{'findings':[{}]},{'findings':[{'field':'action','assertion':'다른 문장','factual_premise':'거짓 사실 전제','source_mismatch':'원문 불일치 근거','correction':'수정 필요 내용'}]}):
   source,story=self.fixture()
   with self.assertRaises(ValueError):verify(self.model(source,response),story,source,[])
 def test_no_automatic_advice_exemption_or_preset_approval(self):
  schema=shapes.STRONG_REVIEW
  self.assertNotIn('supported',schema['properties'])
  finding=schema['properties']['findings']['items']
  self.assertIn('insight',finding['properties']['field']['enum']);self.assertIn('action',finding['properties']['field']['enum'])
  self.assertEqual(set(finding['required']),{'field','assertion','factual_premise','source_mismatch','correction'})
