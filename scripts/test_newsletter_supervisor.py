import json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import newsletter_supervisor as s
class SupervisorTests(unittest.TestCase):
 def test_live_milestone_backup_and_credential_free_child(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);seen=[]
   code="""import os,json,time,pathlib
p=pathlib.Path(os.environ['AP_NEWS_SITE_ROOT']);(p/'.production-state').mkdir()
(p/'child-env.json').write_text(json.dumps({k:os.getenv(k) for k in ['GH_TOKEN','SUPABASE_SERVICE_KEY','PRIVATE_TEST_CREDENTIAL','GITHUB_RUN_ID']}))
(p/'.production-state/draft.json').write_text(json.dumps({'date':'2026-10-30','mode':'test','stories':[]}))
time.sleep(.15)
(p/'finished').touch()
"""
   def backup(*args):seen.append((root/'finished').exists())
   with patch.dict(os.environ,{'AP_NEWS_SITE_ROOT':str(root),'GITHUB_RUN_ID':'123','GH_TOKEN':'dummy','SUPABASE_SERVICE_KEY':'dummy','PRIVATE_TEST_CREDENTIAL':'dummy'}),patch.object(s.checkpoints,'save',side_effect=backup):
    self.assertEqual(s.supervise([sys.executable,'-c',code],root,'2026-10-30','test',interval=0,poll=.01),0)
   env=json.loads((root/'child-env.json').read_text())
   self.assertEqual(env,{'GH_TOKEN':None,'SUPABASE_SERVICE_KEY':None,'PRIVATE_TEST_CREDENTIAL':None,'GITHUB_RUN_ID':'123'})
   self.assertIn(False,seen);self.assertTrue(seen[-1])
 def test_child_failure_is_not_hidden_by_backup(self):
  with tempfile.TemporaryDirectory() as folder,patch.object(s.checkpoints,'save'):
   self.assertEqual(s.supervise([sys.executable,'-c','raise SystemExit(7)'],Path(folder),'2026-10-30','test',poll=.01),7)
if __name__=='__main__':unittest.main()
