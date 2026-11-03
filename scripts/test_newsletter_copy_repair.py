import unittest
import hashlib
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
 def test_same_issue_duplicate_rejected_by_independent_peer_gate(self):
  from unittest.mock import Mock
  source={'title':'New case','text':'A company reports a concrete new implementation result for its customers today.','body_sha256':'abc'}
  model=Mock();model.ask.return_value={'is_news':True,'is_duplicate':True,'novel_quote':source['text'],'reason':'same peer event'}
  peer={'title':'기존 사건','summary':'같은 도입 사례','fact':'같은 결과'}
  with self.assertRaisesRegex(ValueError,'novelty rejection'):verify(model,{},source,[],[peer])
  self.assertEqual(model.ask.call_args.kwargs['comparison_context']['peers'][0]['summary'],'같은 도입 사례')
  self.assertEqual(model.ask.call_count,1)
 def test_server_qa_receipts_require_prior_and_ordered_peer_context(self):
  from newsletter_production_qa import check_copy_receipts
  text='An official publisher reports a concrete new implementation result today.'
  source={'text':text,'body_sha256':hashlib.sha256(text.encode()).hexdigest()}
  stories=[]
  for i in range(2):
   item={'url':str(i),'title':'제목','source_hash':source['body_sha256'],'review':{'supported':True},'novelty':{'is_news':True,'is_duplicate':False,'novel_quote':text}}
   item['strong_review']={'revision':REVISION,'model_revision':ART_REV,'input_hash':identity(item,source,[],stories),'supported':True}
   stories.append(item)
  checks=[(item,source) for item in stories]
  issue={'stories':list(reversed(stories))}
  with patch('newsletter_grounding.validate_grounding'):
   self.assertTrue(check_copy_receipts(issue,checks,[])['ordered_peer_events_verified'])
   with self.assertRaisesRegex(ValueError,'prior context'):check_copy_receipts(issue,checks)
   with self.assertRaisesRegex(ValueError,'stale'):check_copy_receipts(issue,list(reversed(checks)),[])
   stories[0].pop('strong_review')
   with self.assertRaisesRegex(ValueError,'stale'):check_copy_receipts(issue,checks,[])
 def test_receipt_changes_when_peer_event_changes(self):
  from newsletter_copy_repair import identity
  story={'title':'제목'};source={'body_sha256':'hash'}
  self.assertNotEqual(identity(story,source,[],[{'title':'first event'}]),identity(story,source,[],[{'title':'second event'}]))
 def test_roundup_excluded_before_model_and_archived_once(self):
  source={'url':'roundup','title':'October AI roundup','text':'Monthly recap','body_sha256':'hash'}
  state={'stories':[]};opened=[]
  def factory(profile):opened.append(profile);return nullcontext(None)
  with self.assertRaises(ValueError):ensure_copy(state,[source],[],factory,lambda *a:None,lambda:None)
  self.assertEqual(opened,[])
  self.assertEqual(state['copy_attempts']['roundup'],1)
  self.assertEqual(state['copy_history'][0]['source'],source)
 def test_independent_efficacy_rejection(self):
  source={'title':'New NotebookLM study guide','text':'NotebookLM now offers a new study guide for learners to organize their source material.','body_sha256':'abc'}
  class Model:
   def __init__(self):self.calls=[]
   def ask(self,system,question,**kw):
    self.calls.append((system,question,kw))
    if len(self.calls)==1:return {'is_news':True,'is_duplicate':False,'novel_quote':source['text'],'reason':'new feature'}
    import json
    if len(self.calls)==7:return {'consistent':True,'complete':True,'reason':'All efficacy premises rejected.'}
    request=json.loads(question)
    return {'field':request['field'],'text':request['text'],'verdict':'unsupported','premises':[{'claim':request['text'],'status':'unsupported','source_ids':[],'reason':'Feature availability does not demonstrate improved learning efficacy.'}]}
  model=Model();item={k:'학습 효과가 향상됐어요' for k in ('title','summary','fact','insight','action')};item.update(evidence=[source['text']],image_prompt='study book',image_subject='book',visual_approach='ink')
  with self.assertRaisesRegex(ValueError,'Independent source review'):verify(model,item,source,[])
  self.assertNotIn('학습 효과',model.calls[0][1])
  self.assertNotIn('draft',model.calls[0][2]['source_context'])
  self.assertIn('learning efficacy',model.calls[1][0])
 def test_failed_story_replaced_preserves_good(self):
  sources=[{'url':str(i),'title':'New result','text':'A concrete implementation result has been reported today.','body_sha256':str(i)} for i in range(6)]
  def story(i):return {'url':str(i),'title':'제목','source_hash':str(i),'review':{'supported':True}}
  good=[story(i) for i in range(4)]
  for index,item in enumerate(good):item['strong_review']={'revision':REVISION,'model_revision':ART_REV,'input_hash':identity(item,sources[int(item['url'])],[],good[:index]),'supported':True}
  state={'stories':good+[story(4)]};saved=[]
  def check(model,item,source,prior,peers=None):
   if item['url']=='4':raise ValueError('Unsupported learning efficacy')
   item['strong_review']={'revision':REVISION,'model_revision':ART_REV,'input_hash':identity(item,source,prior,peers),'supported':True}
  def draft(model,source,prior,feedback):return story(int(source['url']))
  with patch('newsletter_copy_repair.validate_grounding'),patch('newsletter_copy_repair.verify',side_effect=check):
   ensure_copy(state,sources,[],lambda profile:nullcontext(object()),draft,lambda:saved.append(dict(state.get('copy_attempts',{}))))
  self.assertEqual([s['url'] for s in state['stories']],['0','1','2','3','5'])
  self.assertIs(state['stories'][0],good[0])
  self.assertEqual(state['copy_attempts']['4'],2)
  self.assertIn({'4':1},saved)
if __name__=='__main__':unittest.main()

class PendingRepairTests(unittest.TestCase):
 def test_interrupted_targeted_repair_resumes_verification_without_redraft(self):
  from newsletter_copy_repair import finish_pending_copy,identity
  story={'url':'u','fact':'오류 사실','title':'보존 제목','image':{'hash':'keep'}}
  source={'text':'The official source describes a concrete feature announcement.','body_sha256':'hash'}
  review={'fields':[{'field':'fact','text':'오류 사실','verdict':'unsupported','premises':[]}]}
  state={'pending_copy_repairs':{'u':{'phase':'correct','input_hash':identity(story,source,[],[]),'review':review}}}
  with patch('newsletter_atomic_review.targeted_repair',return_value={**story,'fact':'원문 사실'}) as repair,patch('newsletter_copy_repair.verify') as verify:
   with self.assertRaises(RuntimeError):finish_pending_copy(None,state,story,source,[],[],lambda:(_ for _ in ()).throw(RuntimeError('interrupted')))
   self.assertEqual(state['pending_copy_repairs']['u']['phase'],'verify')
   finish_pending_copy(None,state,story,source,[],[],lambda:None)
   self.assertEqual(repair.call_count,1);self.assertEqual(verify.call_count,1)
  self.assertNotIn('u',state['pending_copy_repairs']);self.assertEqual(story['image'],{'hash':'keep'})
