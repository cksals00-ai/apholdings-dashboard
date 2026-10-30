import unittest,tempfile,json
from pathlib import Path
from newsletter_art_direction import validate_plans,plan_art,reset_invalid_saved_art,validate_scene,complete_plan
from unittest.mock import Mock
class ArtDirectionTests(unittest.TestCase):
 def plans(self):
  views=['cutaway','overhead','profile','macro','eye_level','wide']
  media=['ink','gouache','diagram','linocut','still_life','watercolor']
  return [complete_plan({'subject':f'visible distinct object number {i}','viewpoint':views[i],'medium':media[i],'scene':'A metal object and a ceramic plate arranged with unusual shapes and gentle shadows.'},i) for i in range(6)]
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
 def raw(self,plan):return {k:plan[k] for k in ('viewpoint','medium','subject','scene')}
 def test_invalid_plan_gets_bounded_english_correction(self):
  valid=self.plans();bad=self.raw(valid[0]);bad['scene']='로봇 그림'
  model=Mock();model.ask.side_effect=[bad]+[self.raw(p) for p in valid]
  result=plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0)
  validate_plans(result,0)
  self.assertIn('English',model.ask.call_args_list[0].args[0])
  self.assertIn('English',model.ask.call_args_list[1].args[0])
  self.assertEqual(len(model.ask.call_args_list),7)
 def test_views_and_media_are_constrained_by_content_choices_not_fixed_indices(self):
  model=Mock();counter=0
  def ask(*args,**kwargs):
   nonlocal counter
   counter+=1;props=kwargs['schema']['properties'];views=props['viewpoint']['enum'];media=props['medium']['enum']
   return {'viewpoint':'cutaway' if 'cutaway' in views else views[0],'medium':'watercolor' if 'watercolor' in media else media[0],'subject':'metal pieces beside ceramic object '+str(counter),'scene':'A metal object and a ceramic plate arranged with gentle shadows.'}
  model.ask.side_effect=ask
  result=plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0)
  validate_plans(result,0)
  self.assertGreaterEqual(len({p['viewpoint'] for p in result}),4)
  self.assertGreaterEqual(len({p['medium'] for p in result}),3)
 def test_saved_valid_partial_plans_resume_without_repeating_them(self):
  plans=self.plans();model=Mock();model.ask.side_effect=[self.raw(p) for p in plans[2:]];progress=[]
  result=plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0,previous_plans=plans[:2],on_progress=lambda x:progress.append(len(x)))
  self.assertEqual(result[:2],plans[:2]);self.assertEqual(model.ask.call_count,4);self.assertEqual(progress,[3,4,5,6])
 def test_failure_preserves_completed_individual_plans_for_recovery(self):
  first=self.raw(self.plans()[0]);bad={**first,'scene':'A doctor reviewing patient data.'};model=Mock();model.ask.side_effect=[first,bad,bad];progress=[]
  with self.assertRaises(ValueError):plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0,on_progress=lambda x:progress.append(x))
  self.assertEqual(len(progress),1);self.assertEqual(len(progress[0]),1)
 def test_normalized_duplicate_is_rejected_during_generation(self):
  plans=self.plans();duplicate={**self.raw(plans[1]),'subject':plans[0]['subject'].replace(' ',' & ',1)}
  model=Mock();model.ask.side_effect=[self.raw(plans[0]),duplicate]+[self.raw(p) for p in plans[1:]]
  result=plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0)
  validate_plans(result,0);self.assertEqual(model.ask.call_count,7)
 def test_saved_duplicate_suffix_replanned_without_losing_valid_prefix(self):
  plans=self.plans();duplicate={**plans[1],'subject':plans[0]['subject'].replace(' ',' & ',1)}
  model=Mock();model.ask.side_effect=[self.raw(p) for p in plans[1:]];progress=[]
  result=plan_art(model,[{'title':'기사','summary':'요약','fact':'사실'}]*5,0,previous_plans=[plans[0],duplicate],on_progress=lambda x:progress.append(len(x)))
  self.assertEqual(result[0],plans[0]);self.assertEqual(model.ask.call_count,5);self.assertEqual(progress,[1,2,3,4,5,6])
 def test_patient_ai_and_product_interfaces_rejected_before_diffusion(self):
  for scene in ('A doctor reviewing patient data with AI recommendations.','A laptop screen showing code and a product interface.'):
   with self.subTest(scene=scene),self.assertRaises(ValueError):validate_scene('a person beside a tablet',scene)
  validate_scene('hands and blank study cards','Hands arranging blank study cards beside a book, no text or logos.')
if __name__=='__main__':unittest.main()
