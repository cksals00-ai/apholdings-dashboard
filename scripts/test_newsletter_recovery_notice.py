import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter_recovery_notice as n
class RecoveryNoticeTests(unittest.TestCase):
 def state(self,root):
  p=root/'.production-state';p.mkdir();(p/'draft.json').write_text(json.dumps({'recovery_events':[{'id':'copy-a','stage':'copy','code':'copy_rejected','reason':'Unsupported benefit; correcting from source'}]}))
 def test_fixed_owner_notice_emitted_once_and_receipt_persisted(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root)
   with patch.dict(os.environ,{'GITHUB_RUN_ID':'123','SUPABASE_SERVICE_KEY':'dummy'}),patch.object(n,'emit',return_value={'accepted':True,'id':'provider-1'}) as emit:
    n.notify_pending(root,'2026-11-03','production');n.notify_pending(root,'2026-11-03','production')
    self.assertEqual(emit.call_count,1)
    key,event,detail=emit.call_args.args
    self.assertTrue(key.startswith('2026-11-03:repair-'));self.assertEqual(event,'ops_alert');self.assertIn('아직',detail['message'])
    self.assertTrue(json.loads((root/'.production-state/notification-receipts.json').read_text())['copy-a']['accepted'])
 def test_isolated_test_alert_and_bounded_retries(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root)
   with patch.dict(os.environ,{'GITHUB_RUN_ID':'123','SUPABASE_SERVICE_KEY':'dummy'}),patch.object(n,'emit',side_effect=OSError('temporary')) as emit:
    for i in range(8):n.notify_pending(root,'2026-11-03','test',now=100+i*61)
    self.assertEqual(emit.call_count,5);self.assertTrue(emit.call_args.args[0].startswith('test-123:repair-'));self.assertEqual(emit.call_args.args[1],'test_alert')
 def test_same_unresolved_source_across_attempts_is_not_reported_twice(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root)
   p=root/'.production-state/draft.json';d=json.loads(p.read_text());d['recovery_events']=[{'id':'copy-attempt-1','stage':'copy','code':'copy_rejected','source_url':'https://example.invalid/article','reason':'Unsupported benefit'}];p.write_text(json.dumps(d))
   with patch.dict(os.environ,{'GITHUB_RUN_ID':'123','SUPABASE_SERVICE_KEY':'dummy'}),patch.object(n,'emit',return_value={'accepted':True}) as emit:
    n.notify_pending(root,'2026-11-03','production')
    d['recovery_events'].append(dict(d['recovery_events'][0],id='copy-attempt-2'));p.write_text(json.dumps(d))
    n.notify_pending(root,'2026-11-03','production')
    self.assertEqual(emit.call_count,1)
 def test_no_key_or_unknown_event_cannot_send(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);self.state(root)
   with patch.dict(os.environ,{'SUPABASE_SERVICE_KEY':''}),patch.object(n,'emit') as emit:
    n.notify_pending(root,'2026-11-03','production');emit.assert_not_called()
if __name__=='__main__':unittest.main()
