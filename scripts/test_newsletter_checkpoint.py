import unittest,tempfile,json,zipfile,hashlib
from pathlib import Path
import newsletter_checkpoint as c
from unittest.mock import patch
from types import SimpleNamespace
class CheckpointTests(unittest.TestCase):
 def test_private_checkpoint_roundtrip_and_mode_identity(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/'source';(root/'.production-state').mkdir(parents=True)
   (root/'.production-state/draft.json').write_text(json.dumps({'date':'2026-10-30','mode':'test','stories':[]}))
   z=Path(temp)/'state.zip';c.pack(root,z,'2026-10-30','test')
   target=Path(temp)/'restore';c.unpack(z,target,'2026-10-30','test')
   self.assertTrue((target/'.production-state/draft.json').is_file())
   with self.assertRaises(ValueError):c.unpack(z,target,'2026-10-31','test')
   with self.assertRaises(ValueError):c.unpack(z,target,'2026-10-30','production')
 def test_draft_lookup_uses_authenticated_collection_not_uncreated_tag(self):
  result=SimpleNamespace(returncode=0,stdout=json.dumps([{'tag_name':'work','draft':True,'assets':[]}]))
  with patch.object(c,'gh',return_value=result) as gh:
   self.assertTrue(c.metadata('work')['draft']);self.assertIn('releases?per_page=100',gh.call_args.args[-1])
  result.stdout=json.dumps([{'tag_name':'work','draft':False}])
  with patch.object(c,'gh',return_value=result),self.assertRaises(ValueError):c.metadata('work')
 def test_no_noncheckpoint_paths_or_modified_bytes(self):
  with tempfile.TemporaryDirectory() as temp:
   z=Path(temp)/'bad.zip'
   with zipfile.ZipFile(z,'w') as out:
    out.writestr('checkpoint-manifest.json',json.dumps({'date':'2026-10-30','mode':'test','files':{'../.git/config':hashlib.sha256(b'bad').hexdigest()}}));out.writestr('../.git/config',b'bad')
   with self.assertRaises(ValueError):c.unpack(z,Path(temp)/'target','2026-10-30','test')
 def test_incomplete_new_upload_does_not_hide_last_uploaded_milestone(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/'source';(root/'.production-state').mkdir(parents=True)
   (root/'.production-state/draft.json').write_text(json.dumps({'date':'2026-10-30','mode':'test','stories':[]}))
   z=Path(temp)/'complete.zip';c.pack(root,z,'2026-10-30','test')
   name='AP-News-work-2026-10-30-123-attempt-1-checkpoint-1.zip'
   assets=[{'name':name,'state':'uploaded','size':z.stat().st_size,'updated_at':'2026-10-30T01:00:00Z'},{'name':name.replace('checkpoint-1','checkpoint-2'),'state':'starter','size':0,'updated_at':'2026-10-30T02:00:00Z'}]
   def download(*args):
    destination=Path(args[args.index('--dir')+1])/name;destination.write_bytes(z.read_bytes());return SimpleNamespace(returncode=0)
   with patch.object(c,'metadata',return_value={'assets':assets}),patch.object(c,'gh',side_effect=download):
    self.assertTrue(c.restore(Path(temp)/'restored','2026-10-30','test','123',required=True))
   self.assertTrue((Path(temp)/'restored/.production-state/draft.json').is_file())
if __name__=='__main__':unittest.main()
