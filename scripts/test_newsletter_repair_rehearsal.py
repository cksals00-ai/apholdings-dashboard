import copy,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter_repair_rehearsal as r
from newsletter_art_direction import complete_plan

class RehearsalTests(unittest.TestCase):
 def state(self):
  return {'date':r.today(),'mode':'test','asset_day':r.today()+'-test-123','rehearsal_faults':{'copy_injected':True},'editorial':{'lead_index':0},'art_plans':[complete_plan({'viewpoint':v,'medium':m,'subject':'Paper objects '+str(i),'scene':'Paper objects rest beside a wooden pencil.'},i) for i,(v,m) in enumerate(zip(['overhead','profile','wide','macro','cutaway','eye_level'],['ink','watercolor','gouache','ink','watercolor','gouache']))]}
 def test_guards_fail_closed(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(ValueError):r.guard(r.today(),'123',True)
  with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   for day,run,dry in [('2000-01-01','123',True),(r.today(),'local',True),(r.today(),'123',False)]:
    with self.assertRaises(ValueError):r.guard(day,run,dry)
 def test_art_fault_schema_valid_and_once(self):
  s=self.state();before=copy.deepcopy(s['art_plans'][:5])
  with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   self.assertTrue(r.inject_art_fault(s,True,True));self.assertEqual(s['art_plans'][:5],before)
   self.assertEqual(s['art_plans'][5]['subject'],'A red sports car')
   self.assertFalse(r.inject_art_fault(s,True,True))
 def test_seed_downloads_only_five_and_removes_stale_receipts(self):
  fixture=Path('/private/tmp/ap-news-nov3-complete/.production-state/draft.json')
  if not fixture.exists():self.skipTest('local accepted fixture unavailable')
  old=json.loads(fixture.read_text());old['date']=r.today()
  for story in old['stories']:story['strong_review']={'supported':True}
  accepted={c['url']:c for c in old['candidates'] if c['url'] in {s['url'] for s in old['stories']}}
  def restore(root,*args,**kwargs):
   (root/'.production-state').mkdir();(root/'.production-state/draft.json').write_text(json.dumps(old));return True
  def parse(body,url,*args):return copy.deepcopy(accepted[url])
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}),patch.object(r.checkpoint,'restore',side_effect=restore) as download,patch.object(r.sources,'fetch',return_value=b'official') as fetch,patch.object(r.sources,'parse_article',side_effect=parse):
   state=r.seed(tmp,r.today(),'123',dry_run=True)
   self.assertEqual(fetch.call_count,5);self.assertEqual(len(state['candidates']),5)
   self.assertTrue(state['rehearsal_faults']['advice_premise_injected'])
   self.assertIn('모든 학생에게 입증',next(s for s in state['stories'] if s['url']==state['rehearsal_faults']['advice_url'])['action'])
   self.assertTrue(all('strong_review' not in s for s in state['stories']))
   self.assertEqual(state['issue_number'],old['issue_number']);self.assertNotIn('bundle',state)
   self.assertEqual(state['stories'][0]['review']['supported'],True)
   self.assertEqual(r.seed(tmp,r.today(),'123'),state);self.assertEqual(download.call_count,1)
 def test_seed_resume_preserves_existing_accepted_image_bytes(self):
  state=self.state()
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   folder=Path(tmp,'.production-state');folder.mkdir();(folder/'draft.json').write_text(json.dumps(state))
   image=Path(tmp,'img/newsletter',state['asset_day']+'-story-1.png');image.parent.mkdir(parents=True);image.write_bytes(b'accepted-art')
   def resume(saved,day,run,origin):
    self.assertEqual(origin,'123');saved['rehearsal_execution_run']=run;return saved
   with patch('newsletter_rehearsal_resume.resume_state',side_effect=resume) as call:
    result=r.seed(tmp,r.today(),'456',resume_run='123')
   self.assertEqual(result['asset_day'],state['asset_day']);self.assertEqual(result['rehearsal_execution_run'],'456');call.assert_called_once()
   self.assertEqual(image.read_bytes(),b'accepted-art')
   self.assertEqual(json.loads((folder/'draft.json').read_text())['rehearsal_execution_run'],'456')
 def test_verify_writes_only_safe_summary_after_real_receipts(self):
  from newsletter_copy_repair import identity,REVISION
  from newsletter_cpu import REVIEW_REV
  state=self.state();state['input_published_today']=True
  state['stories']=[{'url':'https://blog.google/'+str(i),'title':'accepted '+str(i)} for i in range(5)]
  state['candidates']=[{'url':s['url'],'body_sha256':'body'+str(i)} for i,s in enumerate(state['stories'])]
  for i,story in enumerate(state['stories']):story['strong_review']={'revision':REVISION,'model_revision':REVIEW_REV,'supported':True,'input_hash':identity(story,state['candidates'][i],[],state['stories'][:i])}
  failed={'subject':'A red sports car','scene':'Yellow flowers'}
  state['rehearsal_faults'].update(art_injected=True,copy_url=state['stories'][0]['url'],art_failed_plan=failed)
  state['rehearsal_faults'].update(advice_premise_injected=True,advice_url=state['stories'][1]['url'])
  state['copy_history']=[{'draft':state['stories'][0]},{'draft':{**state['stories'][1],'action':'AI 교육 효과가 모든 학생에게 입증됐으므로 전면 적용한다.'},'reason':'Independent source review rejected draft: AI 교육 효과가 모든 학생에게 입증됐다는 근거 없음'}]
  failure={'story_index':5,'reason':'subject','scores':{'matched':False},'failed_plan':failed}
  state['art_failures']=[failure];state['art_repair_history']=[{'failure':failure}]
  state['image_attempts']={state['asset_day']+'-hero-original.png':4}
  state['recovery_events']=[{'id':'copy-notice','stage':'copy'},{'id':'art-notice','stage':'art'}]
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   folder=Path(tmp,'.production-state');folder.mkdir();images=Path(tmp,'img/newsletter');images.mkdir(parents=True)
   for i in range(1,6):(images/f"{state['asset_day']}-story-{i}.png").write_bytes(b'preserved')
   (folder/'draft.json').write_text(json.dumps(state));(folder/'notification-receipts.json').write_text(json.dumps({k:{'accepted':False,'recorded':True,'suppressed':True,'policy':'terminal-only-v1'} for k in ['copy-notice','art-notice']}))
   result=r.verify_receipts(folder);self.assertEqual(result['strong_review_count'],5)
   self.assertNotIn('https://',(folder/'recovery-proof.json').read_text())
 def test_advice_proof_requires_specific_factual_rejection(self):
  fault={'advice_url':'u'};draft={'url':'u','action':'AI 교육 효과가 모든 학생에게 입증됐으므로 전면 적용한다.'}
  self.assertFalse(r.advice_fault_rejected([{'draft':draft,'reason':'Independent novelty rejection: old source'}],fault))
  self.assertFalse(r.advice_fault_rejected([{'draft':draft,'reason':'Independent source review rejected draft: unclear recommendation'}],fault))
  self.assertTrue(r.advice_fault_rejected([{'draft':draft,'reason':'Independent source review rejected draft: AI 교육 효과가 모든 학생에게 입증됐다는 근거 없음'}],fault))
 def cache_fixture(self):
  state=self.state();state['resume_history']=[{'from':'123','to':'456'}];state['rehearsal_faults'].update(copy_url='copy-url',advice_url='advice-url')
  state['copy_history']=[{'draft':None},{'draft':{'url':'copy-url','fact':'학습 효과가 입증됐다는 과장'}},{'draft':{'url':'advice-url','action':'AI 교육 효과가 모든 학생에게 입증됐으므로 전면 적용한다.'}}]
  sources=[{'url':url,'body_sha256':url} for url in ('copy-url','advice-url')]
  return state,sources
 def test_resumed_cache_rechecks_old_faults_without_redrafting_verified_work(self):
  state,sources=self.cache_fixture();saved=[]
  failures=[ValueError('Independent source review rejected draft: 학습 효과 입증 근거 없음'),ValueError('Independent source review rejected draft: 모든 학생에게 학습 효과가 입증됐다는 근거 없음')]
  with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}),patch('newsletter_review_controls.verify_controls'),patch('newsletter_review_controls.valid',return_value=True),patch('newsletter_copy_repair.verify',side_effect=failures) as verify:
   r.verify_resumed_cache_challenges(object(),state,sources,[],lambda:saved.append(True))
   self.assertEqual(verify.call_count,2);self.assertEqual(len(saved),2)
   r.verify_resumed_cache_challenges(object(),state,sources,[],lambda:None);self.assertEqual(verify.call_count,2)
  with patch('newsletter_review_controls.valid',return_value=True):self.assertTrue(r.cache_challenge_receipts_valid(state,sources,[]))
 def test_resumed_cache_cannot_accept_fault_or_count_novelty_rejection(self):
  for answer in (None,ValueError('Independent novelty rejection: duplicate'),ValueError('Independent source review rejected draft: unrelated AP suggestion')):
   state,sources=self.cache_fixture()
   with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}),patch('newsletter_copy_repair.verify',side_effect=answer):
    with self.assertRaises(ValueError):r.verify_resumed_cache_challenges(object(),state,sources,[],lambda:None)
   self.assertFalse(r.cache_challenge_receipts_valid(state,sources,[]))
 def test_verify_rejects_missing_real_receipts(self):
  with tempfile.TemporaryDirectory() as tmp:
   Path(tmp,'draft.json').write_text(json.dumps(self.state()))
   with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
    with self.assertRaises(ValueError):r.verify_receipts(tmp)

if __name__=='__main__':unittest.main()
