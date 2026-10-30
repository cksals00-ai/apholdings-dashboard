import json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from datetime import datetime
import newsletter_producer as p

class ProducerTests(unittest.TestCase):
 def test_recovery_reuses_validated_bundle_even_after_local_published_json(self):
  day=datetime.now(p.server.KST).date().isoformat()
  with tempfile.TemporaryDirectory() as temp:
   folder=Path(temp);bundle=folder/f'AP-News-{day}-ready.zip';bundle.write_bytes(b'checkpoint')
   state={'date':day,'mode':'production','input_published_today':False,'stage':'validated'}
   (folder/'draft.json').write_text(json.dumps(state))
   with patch.dict(os.environ,AP_NEWS_SITE_ROOT=temp),patch.object(p.b,'ROOT',folder),patch.object(p,'previous_issues',return_value=[{'date':day,'status':'published','number':23}]),patch.object(p.handoff,'download_bundle',return_value=None),patch.object(p.handoff,'validate_bundle') as validate,patch.object(p.handoff,'upload_bundle') as upload,patch.object(p,'TextModel') as model:
    p.produce(day,folder,folder)
   validate.assert_called_once_with(bundle,day);upload.assert_called_once_with(bundle,day);model.assert_not_called()
 def test_dry_run_cannot_write_runtime_checkout(self):
  with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,AP_NEWS_SITE_ROOT=''):
   with self.assertRaises(ValueError):p.produce(datetime.now(p.server.KST).date().isoformat(),Path(temp),Path(temp),True)
 def test_published_input_main_never_resends(self):
  day=datetime.now(p.server.KST).date().isoformat()
  with tempfile.TemporaryDirectory() as temp:
   folder=Path(temp)
   with patch.dict(os.environ,AP_NEWS_SITE_ROOT=temp),patch.object(p.b,'ROOT',folder),patch.object(p,'previous_issues',return_value=[{'date':day,'status':'published'}]),patch.object(p.handoff,'download_bundle') as download,patch.object(p,'TextModel') as model:
    p.produce(day,folder,folder)
   download.assert_not_called();model.assert_not_called()
if __name__=='__main__':unittest.main()
