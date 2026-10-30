import unittest
import newsletter_grounding as g
class GroundingTests(unittest.TestCase):
 def source(self):return {'text':'The new feature is available in preview for selected users. It helps users edit documents inside one conversation.','url':'https://blog.google/a','published':'2026-10-29'}
 def story(self):return {'title':'문서 편집 기능 미리보기','summary':'일부 사용자가 대화 안에서 문서를 편집할 수 있습니다.','fact':'선택된 사용자를 대상으로 미리보기 기능을 제공합니다.','insight':'AP 교육에서는 제공 조건을 확인한 뒤 실습 범위를 정하는 것이 좋겠습니다.','action':'제공 조건을 확인하세요.','evidence':['The new feature is available in preview for selected users.'],'image_prompt':'Side view ink editorial illustration of a person editing documents, no text, navy sage ivory','image_subject':'person editing documents','visual_approach':'ink drawing'}
 def test_english_number_words_authorize_only_equivalent_figures(self):
  self.assertIn('7',g.numbers('seven AWS Regions'))
  self.assertIn('5',g.numbers('under five hours'))
  self.assertNotIn('1',g.numbers('five hours'))
  self.assertNotIn('1',g.numbers('twenty-one regions'))
  self.assertNotIn('20',g.numbers('twenty one regions'))
  self.assertNotIn('1',g.numbers('thirty-one regions'))
  self.assertNotIn('20',g.numbers('twenty-first release'))
  self.assertNotIn('1',g.numbers('one hundred and one regions'))
 def test_missing_number_error_identifies_field_and_value(self):
  story=self.story();story['fact']+=' 카테고리 1입니다.'
  with self.assertRaisesRegex(ValueError,'fact.*1'):g.validate_grounding(story,self.source(),{'supported':True,'unsupported_claims':[]})
 def test_real_quote_and_supported_review(self):
  g.validate_grounding(self.story(),self.source(),{'supported':True,'unsupported_claims':[]})
 def test_fabricated_quote_or_numbers_or_failed_review_block(self):
  a=self.story();a['evidence']=['Available to everyone worldwide.']
  with self.assertRaises(ValueError):g.validate_grounding(a,self.source(),{'supported':True,'unsupported_claims':[]})
  a=self.story();a['fact']+=' 비용이 50% 줄었습니다.'
  with self.assertRaises(ValueError):g.validate_grounding(a,self.source(),{'supported':True,'unsupported_claims':[]})
  with self.assertRaises(ValueError):g.validate_grounding(self.story(),self.source(),{'supported':False,'unsupported_claims':['scope']})
 def test_original_product_name_must_not_be_mistransliterated(self):
  source=self.source();source['title']='Gemini feature update';source['text']='Gemini is available in preview for selected users.'
  story=self.story();story['evidence']=[source['text']];story['fact']='기미는 선택된 사용자를 위한 미리보기로 제공됩니다.'
  with self.assertRaises(ValueError):g.validate_grounding(story,source,{'supported':True,'unsupported_claims':[]})
 def test_untrusted_model_output_is_data_not_executable(self):
  with self.assertRaises(ValueError):g.parse_json('import os; os.system("bad")')
  self.assertEqual(g.parse_json('```json\n{"supported":true}\n```'),{'supported':True})
if __name__=='__main__':unittest.main()
