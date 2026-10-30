import json,os,tempfile,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
from datetime import datetime
import newsletter_producer as p

class ProducerTests(unittest.TestCase):
 def test_corrective_pass_keeps_korean_and_specific_reviewer_feedback(self):
  from unittest.mock import Mock
  from test_newsletter_grounding import GroundingTests
  story=GroundingTests().story();source=GroundingTests().source();source.update(source='Google',body_sha256='hash')
  novelty={'is_news':True,'is_duplicate':False,'novel_quote':source['text'][:70]}
  review={'supported':False,'unsupported_claims':['Remove unsupported availability']}
  wire={**{k:v for k,v in story.items() if k!='evidence'},'evidence_ids':[0]}
  model=Mock();model.ask.side_effect=[novelty,wire,review,wire,{'supported':True,'unsupported_claims':[]}]
  p.draft_story(model,source)
  correction=model.ask.call_args_list[3].args[1]
  self.assertIn('in Korean',correction)
  self.assertIn('Remove unsupported availability',correction)
  self.assertIn('Select evidence_ids',correction)
 def test_recovery_reuses_validated_bundle_even_after_local_published_json(self):
  day=datetime.now(p.server.KST).date().isoformat()
  with tempfile.TemporaryDirectory() as temp:
   folder=Path(temp);bundle=folder/f'AP-News-{day}-ready.zip';bundle.write_bytes(b'checkpoint')
   state={'date':day,'mode':'production','input_published_today':False,'stage':'validated','quality':{'revision':p.QA_REVISION},'stories':[{'url':f'https://blog.google/a{i}','review':{},'source_hash':hashlib.sha256(b'evidence').hexdigest()} for i in range(5)],'candidates':[{'url':f'https://blog.google/a{i}','parser_revision':p.PARSER_REVISION,'text':'evidence','body_sha256':hashlib.sha256(b'evidence').hexdigest()} for i in range(5)]}
   (folder/'draft.json').write_text(json.dumps(state))
   with patch.dict(os.environ,AP_NEWS_SITE_ROOT=temp),patch.object(p.b,'ROOT',folder),patch.object(p,'previous_issues',return_value=[{'date':day,'status':'published','number':23}]),patch.object(p.handoff,'download_bundle',return_value=None),patch.object(p.handoff,'validate_bundle',return_value=({},{})) as validate,patch.object(p.handoff,'upload_bundle') as upload,patch.object(p,'TextModel') as model,patch.object(p,'validate_grounding',return_value=True):
    p.produce(day,folder,folder)
   validate.assert_called_once_with(bundle,day);upload.assert_called_once_with(bundle,day);model.assert_not_called()
 def test_old_qa_receipt_cannot_bypass_new_pdf_image_gate(self):
  day=datetime.now(p.server.KST).date().isoformat()
  with tempfile.TemporaryDirectory() as temp:
   folder=Path(temp);bundle=folder/f'AP-News-{day}-ready.zip';bundle.write_bytes(b'checkpoint')
   state={'date':day,'mode':'production','input_published_today':False,'stage':'validated','stories':[],'candidates':[{'parser_revision':p.PARSER_REVISION,'url':f'https://blog.google/a{i}'} for i in range(24)]}
   (folder/'draft.json').write_text(json.dumps(state))
   with patch.dict(os.environ,AP_NEWS_SITE_ROOT=temp),patch.object(p.b,'ROOT',folder),patch.object(p,'previous_issues',return_value=[]),patch.object(p.handoff,'download_bundle',return_value=None),patch.object(p.handoff,'validate_bundle',return_value=({},{})),patch.object(p,'check_all',side_effect=ValueError('PDF editorial image missing')),patch.object(p.handoff,'upload_bundle') as upload,patch.object(p,'TextModel') as model:
    with self.assertRaisesRegex(ValueError,'PDF editorial image'):p.produce(day,folder,folder)
   self.assertEqual(json.loads((folder/'draft.json').read_text())['stage'],'needs_qa');upload.assert_not_called();model.assert_not_called()
 def test_dry_run_cannot_write_runtime_checkout(self):
  with tempfile.TemporaryDirectory() as temp,patch.dict(os.environ,AP_NEWS_SITE_ROOT=''):
   with self.assertRaises(ValueError):p.produce(datetime.now(p.server.KST).date().isoformat(),Path(temp),Path(temp),True)
 def test_published_input_main_never_resends(self):
  day=datetime.now(p.server.KST).date().isoformat()
  with tempfile.TemporaryDirectory() as temp:
   folder=Path(temp)
   with patch.dict(os.environ,AP_NEWS_SITE_ROOT=temp),patch.object(p.b,'ROOT',folder),patch.object(p,'previous_issues',return_value=[{'date':day,'status':'published'}]),patch.object(p.handoff,'download_bundle') as download,patch.object(p,'TextModel') as model,patch.object(p,'validate_grounding',return_value=True):
    p.produce(day,folder,folder)
   download.assert_not_called();model.assert_not_called()
if __name__=='__main__':unittest.main()
