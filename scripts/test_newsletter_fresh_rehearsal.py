import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter_repair_rehearsal as r
class FreshRehearsalTests(unittest.TestCase):
 def test_seed_does_not_depend_on_published_issue_or_old_checkpoint(self):
  with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}),patch.object(r.checkpoint,'restore',side_effect=AssertionError('No published prerequisite')):
   state=r.seed(temp,r.today(),'123',True)
   self.assertEqual(state['stories'],[]);self.assertEqual(state['rehearsal_version'],2)
   self.assertFalse(state['input_published_today']);self.assertNotIn('issue_number',state)
 def test_past_date_still_blocked(self):
  with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   with self.assertRaises(ValueError):r.seed(temp,'2000-01-01','123',True)
 def test_live_fault_only_changes_two_fields_once_in_isolation(self):
  from newsletter_repair_rehearsal import inject_copy_fault
  state={'date':r.today(),'mode':'test','asset_day':r.today()+'-test-123','rehearsal_version':2,'stories':[{'url':str(i),'fact':'유지 사실','action':'유지 행동','image':{'hash':'keep'}} for i in range(5)]}
  with patch.dict(os.environ,{'AP_NEWS_REPAIR_REHEARSAL':'1'}):
   self.assertTrue(inject_copy_fault(state));self.assertEqual(state['stories'][0]['image'],{'hash':'keep'})
   self.assertEqual(state['stories'][2]['fact'],'유지 사실');self.assertFalse(inject_copy_fault(state))
if __name__=='__main__':unittest.main()
