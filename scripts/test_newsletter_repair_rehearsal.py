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
   self.assertTrue(all('strong_review' not in s for s in state['stories']))
   self.assertEqual(state['issue_number'],old['issue_number']);self.assertNotIn('bundle',state)
   self.assertEqual(state['stories'][0]['review']['supported'],True)
   self.assertEqual(r.seed(tmp,r.today(),'123'),state);self.assertEqual(download.call_count,1)
 def test_verify_writes_only_safe_summary_after_real_receipts(self):
  from newsletter_copy_repair import identity,REVISION
  from newsletter_cpu import ART_REV
  state=self.state();state['input_published_today']=True
  state['stories']=[{'url':'https://blog.google/'+str(i),'title':'accepted '+str(i)} for i in range(5)]
  state['candidates']=[{'url':s['url'],'body_sha256':'body'+str(i)} for i,s in enumerate(state['stories'])]
  for i,story in enumerate(state['stories']):story['strong_review']={'revision':REVISION,'model_revision':ART_REV,'supported':True,'input_hash':identity(story,state['candidates'][i],[],state['stories'][:i])}
  failed={'subject':'A red sports car','scene':'Yellow flowers'}
  state['rehearsal_faults'].update(art_injected=True,copy_url=state['stories'][0]['url'],art_failed_plan=failed)
  state['copy_history']=[{'draft':state['stories'][0]}]
  failure={'story_index':5,'reason':'subject','scores':{'matched':False},'failed_plan':failed}
  state['art_failures']=[failure];state['art_repair_history']=[{'failure':failure}]
  state['image_attempts']={state['asset_day']+'-hero-original.png':4}
  state['recovery_events']=[{'id':'copy-notice','stage':'copy'},{'id':'art-notice','stage':'art'}]
  with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   folder=Path(tmp,'.production-state');folder.mkdir();images=Path(tmp,'img/newsletter');images.mkdir(parents=True)
   for i in range(1,6):(images/f"{state['asset_day']}-story-{i}.png").write_bytes(b'preserved')
   (folder/'draft.json').write_text(json.dumps(state));(folder/'notification-receipts.json').write_text(json.dumps({k:{'accepted':True} for k in ['copy-notice','art-notice']}))
   result=r.verify_receipts(folder);self.assertEqual(result['strong_review_count'],5)
   self.assertNotIn('https://',(folder/'recovery-proof.json').read_text())
 def test_verify_rejects_missing_real_receipts(self):
  with tempfile.TemporaryDirectory() as tmp:
   Path(tmp,'draft.json').write_text(json.dumps(self.state()))
   with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
    with self.assertRaises(ValueError):r.verify_receipts(tmp)

if __name__=='__main__':unittest.main()
