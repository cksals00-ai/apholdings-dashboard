import unittest,copy
from unittest.mock import patch
import newsletter_review_controls as controls

class ReviewControlsTests(unittest.TestCase):
 def fixture(self):
  sources=[];history=[]
  for label,suffix,expected in controls.SPECS:
   url='https://official.example/'+suffix
   sources.append({'url':url,'body_sha256':label})
   history.append({'draft':{'url':url,'title':'사례 발표','summary':'사례 결과를 소개했다.','fact':'구현 사례를 발표했다.','insight':'AP가 서비스를 설계한다면 권한 분리를 검토할 수 있다.' if expected else 'AP는 의료 교육 확대 기회를 얻었습니다.','action':'조건을 확인한다.','evidence':['Original source evidence']}})
  return {'copy_history':history},sources
 def verify(self,model,item,*args):
  if '기회를 얻었습니다' in item['insight']:
   e=ValueError('Unsupported factual premise');e.review={'findings':[{'field':'insight','assertion':item['insight'],'factual_premise':'AP가 의료 교육 확대 기회를 얻었다','source_mismatch':'원문에 AP의 실제 기회 확보에 대한 근거가 없다.','correction':'확보한 결과가 아니라 조건부 제안으로 고친다.'}]};raise e
  item['strong_review']={'review':{'findings':[]}}
 def test_actual_controls_wired_and_receipts_reused(self):
  state,sources=self.fixture();saves=[]
  with patch('newsletter_repair_rehearsal.identity'),patch('newsletter_copy_repair.verify',side_effect=self.verify) as verify:
   controls.verify_controls(object(),state,sources,[],lambda:saves.append(True));self.assertEqual(verify.call_count,3)
   controls.verify_controls(object(),state,sources,[],lambda:None);self.assertEqual(verify.call_count,3)
  self.assertTrue(controls.valid(state,sources,[]));self.assertEqual(len(saves),3)
  self.assertEqual(state['copy_history'][0]['draft']['insight'],'AP가 서비스를 설계한다면 권한 분리를 검토할 수 있다.')
  self.assertNotIn('copy_attempts',state)
  state['editorial_control_receipts']['agentcore_proposal']['cache_revision']-=1
  self.assertFalse(controls.valid(state,sources,[]))
 def test_positive_false_rejection_cannot_qualify(self):
  state,sources=self.fixture()
  with patch('newsletter_repair_rehearsal.identity'),patch('newsletter_copy_repair.verify',side_effect=ValueError('unsupported proposal')):
   with self.assertRaisesRegex(ValueError,'clean conditional'):controls.verify_controls(object(),state,sources,[],lambda:None)
  self.assertFalse(controls.valid(state,sources,[]))
 def test_negative_acceptance_or_unrelated_rejection_cannot_qualify(self):
  for bad in ('accept','other'):
   state,sources=self.fixture()
   def verify(model,item,*args):
    if '기회를 얻었습니다' in item['insight']:
     if bad=='other':raise ValueError('Novelty rejection')
    item['strong_review']={'review':{'findings':[]}}
   with patch('newsletter_repair_rehearsal.identity'),patch('newsletter_copy_repair.verify',side_effect=verify):
    with self.assertRaises(ValueError):controls.verify_controls(object(),state,sources,[],lambda:None)
   self.assertFalse(controls.valid(state,sources,[]))
 def test_source_or_draft_changes_invalidate_controls(self):
  state,sources=self.fixture()
  with patch('newsletter_repair_rehearsal.identity'),patch('newsletter_copy_repair.verify',side_effect=self.verify):controls.verify_controls(object(),state,sources,[],lambda:None)
  changed=copy.deepcopy(sources);changed[0]['body_sha256']='changed'
  self.assertFalse(controls.valid(state,changed,[]))
  state['copy_history'][0]['draft']['fact']='새 주장'
  self.assertFalse(controls.valid(state,sources,[]))
