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
 def test_verify_rejects_missing_real_receipts(self):
  with tempfile.TemporaryDirectory() as tmp:
   Path(tmp,'draft.json').write_text(json.dumps(self.state()))
   with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
    with self.assertRaises(ValueError):r.verify_receipts(tmp)

if __name__=='__main__':unittest.main()
