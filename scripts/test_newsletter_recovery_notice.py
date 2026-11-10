import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter_recovery_notice as n
class RecoveryNoticeTests(unittest.TestCase):
 def state(self,root):
  p=root/'.production-state';p.mkdir();(p/'draft.json').write_text(json.dumps({'recovery_events':[{'id':'copy-a','stage':'copy','code':'copy_rejected','reason':'Unsupported benefit; correcting from source'}]}))
 def test_recoverable_fault_is_recorded_once_without_provider_mail(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root)
   with patch.dict(os.environ,{'GITHUB_RUN_ID':'123','SUPABASE_SERVICE_KEY':'synthetic'}),patch('newsletter_ops.emit') as sender,patch('urllib.request.urlopen',side_effect=AssertionError('No network for a recovery record')):
    n.notify_pending(root,'2026-11-10','production',now=100);n.notify_pending(root,'2026-11-10','production',now=200)
   sender.assert_not_called();row=json.loads((root/'.production-state/notification-receipts.json').read_text())['copy-a']
   self.assertTrue(row['recorded']);self.assertTrue(row['suppressed']);self.assertFalse(row['accepted']);self.assertNotIn('provider_id',row);self.assertEqual(row['recorded_at'],100)
 def test_test_mode_also_stays_silent_without_a_service_key(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root)
   with patch.dict(os.environ,{'SUPABASE_SERVICE_KEY':''}),patch('newsletter_ops.emit') as sender:
    for i in range(8):n.notify_pending(root,'2026-11-10','test',now=100+i*61)
   sender.assert_not_called();row=json.loads((root/'.production-state/notification-receipts.json').read_text())['copy-a'];self.assertTrue(row['suppressed']);self.assertFalse(row['accepted'])
 def test_same_scope_across_attempts_reuses_silent_record(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root);p=root/'.production-state/draft.json';d=json.loads(p.read_text())
   d['recovery_events'][0]['source_url']='https://example.invalid/article';p.write_text(json.dumps(d))
   n.notify_pending(root,'2026-11-10','production',now=100)
   d['recovery_events'].append(dict(d['recovery_events'][0],id='copy-b'));p.write_text(json.dumps(d));n.notify_pending(root,'2026-11-10','production',now=200)
   rows=json.loads((root/'.production-state/notification-receipts.json').read_text());self.assertEqual(rows['copy-a']['scope_digest'],rows['copy-b']['scope_digest']);self.assertEqual(rows['copy-b']['recorded_at'],100)
 def test_routine_candidate_exclusion_is_quiet(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root);p=root/'.production-state/draft.json';d=json.loads(p.read_text());d['recovery_events'][0]['notify']=False;p.write_text(json.dumps(d))
   n.notify_pending(root,'2026-11-10','production');self.assertFalse((root/'.production-state/notification-receipts.json').exists())
 def test_malformed_event_is_never_a_delivery_receipt(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root);p=root/'.production-state/draft.json';d=json.loads(p.read_text());del d['recovery_events'][0]['reason'];p.write_text(json.dumps(d))
   n.notify_pending(root,'2026-11-10','production');self.assertFalse((root/'.production-state/notification-receipts.json').exists())
if __name__=='__main__':unittest.main()
