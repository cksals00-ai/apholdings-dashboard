import unittest,tempfile,json
from pathlib import Path
from newsletter_art_direction import validate_plans,plan_art,reset_invalid_saved_art
from unittest.mock import Mock
class ArtDirectionTests(unittest.TestCase):
 def plans(self):
  views=['cutaway','overhead','profile','macro','eye_level','wide']
  media=['ink','gouache','diagram','linocut','still_life','watercolor']
  return [{'story_index':i,'prompt':f'{media[i]} illustration of visible object number {i}, {views[i]}, navy ivory accents, no text','subject':f'visible distinct object number {i}','approach':media[i]+' '+views[i],'viewpoint':views[i],'medium':media[i]} for i in range(6)]
 def test_invalid_legacy_plan_is_archived_without_touching_copy_or_regular_images(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);images=root/'img/newsletter';images.mkdir(parents=True);folder=root/'.production-state';folder.mkdir()
   regular=images/'2026-10-30-hero.png';regular.write_bytes(b'published image')
   generated=images/'2026-10-30-test-123-story-1.png';generated.write_bytes(b'unusable image')
   plans=self.plans();plans[0]['subject']='로봇'
   state={'stories':[{'title':'kept'}],'editorial':{'lead_index':0},'art_plans':plans,'quality':{'old':True}}
   self.assertTrue(reset_invalid_saved_art(root,folder,'2026-10-30-test-123',state))
   self.assertEqual(state['stories'],[{'title':'kept'}])
   self.assertEqual(regular.read_bytes(),b'published image')
   self.assertFalse(generated.exists())
   self.assertEqual(next((folder/'rejected-art').rglob('*.png')).read_bytes(),b'unusable image')
   self.assertNotIn('art_plans',state);self.assertNotIn('quality',state)
 def test_text_only_repair_keeps_valid_art_using_fixed_lead(self):
  state={'art_plans':self.plans(),'fixed_lead':0,'stage':'needs_text_repair'}
  self.assertFalse(reset_invalid_saved_art('/unused','/unused','2026-10-30',state))
  self.assertIn('art_plans',state)
 def test_production_quarantine_never_moves_same_day_test_preview_assets(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);images=root/'img/newsletter';images.mkdir(parents=True);folder=root/'.production-state';folder.mkdir()
   own=images/'2026-10-30-story-1.png';own.write_bytes(b'bad')
   preview=images/'2026-10-30-test-123-story-1.png';preview.write_bytes(b'keep preview')
   unrelated=images/'2026-10-30-health.png';unrelated.write_bytes(b'keep other asset')
   plans=self.plans();plans[0]['subject']='로봇'
   state={'editorial':{'lead_index':0},'art_plans':plans}
   self.assertTrue(reset_invalid_saved_art(root,folder,'2026-10-30',state))
   self.assertFalse(own.exists())
   self.assertEqual(preview.read_bytes(),b'keep preview')
   self.assertEqual(unrelated.read_bytes(),b'keep other asset')
 def test_valid_saved_plan_and_art_are_unchanged(self):
  state={'art_plans':self.plans(),'editorial':{'lead_index':0}}
  self.assertFalse(reset_invalid_saved_art('/unused','/unused','2026-10-30-test-123',state))
  self.assertIn('art_plans',state)
 def test_medium_keyword_cannot_be_a_substring_of_an_unrelated_word(self):
  plans=self.plans();plans[0]['prompt']='A thinking robot in cutaway with navy accents, no text'
  with self.assertRaises(ValueError):validate_plans(plans,0)
 def test_english_distinct_views_and_cover(self):validate_plans(self.plans(),0)
 def test_korean_or_repeated_cover_or_homogeneous_angles_rejected(self):
  for kind in ['korean','cover','angles']:
   plans=self.plans()
   if kind=='korean':plans[0]['subject']='로봇 조작'
   elif kind=='cover':plans[5]['subject']=plans[0]['subject']
   else:
    for p in plans:p['viewpoint']='wide'
   with self.subTest(kind=kind),self.assertRaises(ValueError):validate_plans(plans,0)
 def test_invalid_plan_gets_bounded_english_correction(self):
  valid=self.plans();bad=self.plans();bad[0]['prompt']='로봇 그림'
  model=Mock();model.ask.side_effect=[{'plans':bad},{'plans':valid}]
  self.assertEqual(plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0),valid)
  self.assertIn('English',model.ask.call_args_list[0].args[0])
  self.assertIn('English',model.ask.call_args_list[1].args[0])
  self.assertEqual(len(model.ask.call_args_list),2)
if __name__=='__main__':unittest.main()
