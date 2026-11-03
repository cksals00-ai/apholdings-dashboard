import unittest
from unittest.mock import patch
from contextlib import nullcontext
from newsletter_copy_repair import ensure_copy,identity,REVISION,verify
from newsletter_cpu import ART_REV
from newsletter_grounding import require_news_topic,validate_korean_copy
from newsletter_copy_repair import record_failure,receipt_valid
class CopyRepairTests(unittest.TestCase):
 def test_monthly_roundup(self):
  for title in ('Google AI updates from October','The latest AI news we announced in October','October AI roundup'):
   with self.assertRaises(ValueError):require_news_topic({'title':title,'text':'Here is a recap of this month’s announcements.'})
 def test_korean_corruption(self):
  with self.assertRaises(ValueError):validate_korean_copy('발표 자료 데ck를 검토하세요')
  validate_korean_copy('NotebookLM 자료를 검토하세요')
 def test_durable_counter_and_event(self):
  state={};record_failure(state,'u','bad');record_failure(state,'u','bad')
  self.assertEqual(state['copy_attempts']['u'],2)
  self.assertEqual(len(state['recovery_events']),2)
 def test_old_receipt_not_trusted(self):
  self.assertFalse(receipt_valid({'review':{'supported':True}}, {'body_sha256':'abc'}, []))
 def test_independent_efficacy_rejection(self):
  source={'title':'New NotebookLM study guide','text':'NotebookLM now offers a new study guide for learners to organize their source material.','body_sha256':'abc'}
  class Model:
   def __init__(self):self.calls=[]
   def ask(self,system,question,**kw):
    self.calls.append((system,question,kw))
    if len(self.calls)==1:return {'is_news':True,'is_duplicate':False,'novel_quote':source['text'],'reason':'new feature'}
    return {'supported':False,'unsupported_claims':['Feature availability does not demonstrate improved learning efficacy']}
  model=Model();item={k:'학습 효과가 향상됐어요' for k in ('title','summary','fact','insight','action')};item.update(evidence=[source['text']],image_prompt='study book',image_subject='book',visual_approach='ink')
  with self.assertRaisesRegex(ValueError,'Independent source review'):verify(model,item,source,[])
  self.assertNotIn('학습 효과',model.calls[0][1])
  self.assertNotIn('draft',model.calls[0][2]['source_context'])
  self.assertIn('learning efficacy',model.calls[1][0])
 def test_failed_story_replaced_preserves_good(self):
  sources=[{'url':str(i),'title':'New result','text':'A concrete implementation result has been reported today.','body_sha256':str(i)} for i in range(6)]
  def story(i):return {'url':str(i),'title':'제목','source_hash':str(i),'review':{'supported':True}}
  good=[story(i) for i in range(4)]
  for item in good:item['strong_review']={'revision':REVISION,'model_revision':ART_REV,'input_hash':identity(item,sources[int(item['url'])],[]),'supported':True}
  state={'stories':good+[story(4)]};saved=[]
  def check(model,item,source,prior):
   if item['url']=='4':raise ValueError('Unsupported learning efficacy')
   item['strong_review']={'revision':REVISION,'model_revision':ART_REV,'input_hash':identity(item,source,prior),'supported':True}
  def draft(model,source,prior,feedback):return story(int(source['url']))
  with patch('newsletter_copy_repair.validate_grounding'),patch('newsletter_copy_repair.verify',side_effect=check):
   ensure_copy(state,sources,[],lambda profile:nullcontext(object()),draft,lambda:saved.append(dict(state.get('copy_attempts',{}))))
  self.assertEqual([s['url'] for s in state['stories']],['0','1','2','3','5'])
  self.assertIs(state['stories'][0],good[0])
  self.assertEqual(state['copy_attempts']['4'],2)
  self.assertIn({'4':1},saved)
if __name__=='__main__':unittest.main()
