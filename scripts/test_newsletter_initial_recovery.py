import hashlib,json,tempfile,unittest
from pathlib import Path
from newsletter_initial_recovery import recover_product_drafts
from newsletter_grounding import indexed_source
import test_newsletter_grounding as fixtures
class InitialRecoveryTests(unittest.TestCase):
 def fixture(self,root):
  source={**fixtures.GroundingTests().source(),'title':'New Bedrock feature','source':'AWS','body_sha256':hashlib.sha256(fixtures.GroundingTests().source()['text'].encode()).hexdigest()}
  story=fixtures.GroundingTests().story();story['title']='베드로크 미리보기';wire={k:v for k,v in story.items() if k!='evidence'};wire['evidence_ids']=[0]
  prompt='<source_data>'+json.dumps(indexed_source(source),ensure_ascii=False)+'</source_data>'
  raw={'prompt':prompt,'content':json.dumps(wire,ensure_ascii=False),'_ap_runtime':{'profile':'copy','prompt_sha256':hashlib.sha256(('copy\n'+prompt).encode()).hexdigest()}}
  folder=root/'model-outputs';folder.mkdir();(folder/'copy-123.json').write_text(json.dumps(raw,ensure_ascii=False))
  state={'stories':[],'copy_history':[{'reason':'Keep original product name in Latin spelling: Bedrock','draft':None,'source':source}]}
  return state,source,raw,folder/'copy-123.json'
 def test_recover_exact_source_bound_failed_draft_without_regeneration_or_approval(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);state,source,raw,path=self.fixture(root);saved=[]
   recover_product_drafts(root,state,[source],lambda:saved.append(True))
   self.assertEqual(len(state['stories']),1);self.assertIn('Bedrock',state['stories'][0]['title'])
   self.assertFalse(state['stories'][0]['review']['supported']);self.assertNotIn('strong_review',state['stories'][0]);self.assertEqual(len(saved),1)
   recover_product_drafts(root,state,[source],lambda:saved.append(True));self.assertEqual(len(saved),1)
 def test_recovered_draft_requires_actual_independent_review_before_server_qa(self):
  from unittest.mock import Mock,patch
  from newsletter_copy_repair import verify
  from newsletter_production_qa import check_copy_receipts
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);state,source,raw,path=self.fixture(root)
   recover_product_drafts(root,state,[source],lambda:None);story=state['stories'][0]
   with self.assertRaisesRegex(ValueError,'receipt missing or stale'):check_copy_receipts({'stories':[story]},[(story,source)],[])
   model=Mock();model.ask.return_value={'is_news':True,'is_duplicate':False,'novel_segment_id':0,'reason':'new feature'}
   with patch('newsletter_atomic_review.review_fields',return_value={'supported':False,'unsupported_claims':['unsupported factual premise']}):
    with self.assertRaises(ValueError):verify(model,story,source,[])
   self.assertNotIn('strong_review',story)
   with patch('newsletter_atomic_review.review_fields',return_value={'supported':True,'unsupported_claims':[]}):verify(model,story,source,[])
   self.assertTrue(check_copy_receipts({'stories':[story]},[(story,source)],[])['independent_public_14b'])
 def test_raw_prompt_or_source_identity_mismatch_is_never_reused(self):
  for changed in ('prompt','source'):
   with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);state,source,raw,path=self.fixture(root)
    if changed=='prompt':raw['prompt']+=' altered';path.write_text(json.dumps(raw))
    else:source={**source,'body_sha256':'different'}
    recover_product_drafts(root,state,[source],lambda:None);self.assertEqual(state['stories'],[])
 def test_saved_draft_and_assets_are_never_replaced(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);state,source,raw,path=self.fixture(root)
   accepted={'url':source['url'],'title':'보존 원고','image':{'hash':'keep'}};state['stories']=[accepted]
   recover_product_drafts(root,state,[source],lambda:None);self.assertEqual(state['stories'],[accepted])
if __name__=='__main__':unittest.main()
