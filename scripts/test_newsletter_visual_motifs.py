import unittest
import newsletter_art_direction as a
class VisualMotifTests(unittest.TestCase):
 def test_prior_window_motif_cannot_be_reused_as_primary_composition(self):
  class Model:
   def ask(self,*args,**kwargs):return {'viewpoint':'overhead','medium':'ink','subject':'An open workshop window','scene':'An open workshop window faces a simple wooden bench in a quiet room.'}
  stories=[dict(title='소식',summary='요약',fact='원문 사실') for _ in range(5)]
  with self.assertRaisesRegex(ValueError,'motif'):
   a.plan_art(Model(),stories,0,recent_directions=[{'subject':'A shop window with shelves','viewpoint':'wide','medium':'linocut'}])
 def test_changed_subject_and_camera_are_allowed(self):
  a.validate_plan_novelty({'subject':'A stage and a curtain','viewpoint':'wide'},[{'subject':'A shop window with shelves','viewpoint':'wide'}])
  a.validate_plan_novelty({'subject':'A teacher and child reading a book','viewpoint':'profile'},[{'subject':'A tutor and student studying an open workbook','viewpoint':'eye_level'}])
  with self.assertRaisesRegex(ValueError,'motif'):
   a.validate_plan_novelty({'subject':'A teacher and child reading a book','viewpoint':'eye_level'},[{'subject':'A tutor and student studying an open workbook','viewpoint':'eye_level'}])
 def test_legacy_seed_is_used_only_for_matching_last_three_issue_images(self):
  from newsletter_art_repair import recent_directions
  directions=recent_directions([{'date':'2026-11-02','stories':[{'image':{'path':'/img/newsletter/2026-11-02-story-4.png'}}]}])
  self.assertEqual(len(directions),1);self.assertIn('window',directions[0]['subject'])
  self.assertEqual(recent_directions([{'date':'2099-01-01','stories':[{'image':{'path':'/img/newsletter/2026-11-02-story-4.png'}}]}]),[])
if __name__=='__main__':unittest.main()
