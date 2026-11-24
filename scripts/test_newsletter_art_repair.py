import copy,json,unittest
from unittest.mock import Mock
import test_newsletter_art_direction as fixtures
from newsletter_art_repair import record_failure,repair_pending,recent_directions

class RepairTests(unittest.TestCase):
 def state(self):return {'art_plans':fixtures.ArtDirectionTests().plans(),'stories':[{'title':'news','summary':'update','fact':'facts'}]*5,'editorial':{'lead_index':0}}
 def test_failed_hero_replans_only_hero_with_prior_feedback(self):
  state=self.state();old=copy.deepcopy(state['art_plans']);state['image_subject_scores']={'accepted.png':{'positive':1}}
  record_failure(state,5,'hero.png','subject',{'positive':.1});state=json.loads(json.dumps(state))
  model=Mock();model.ask.return_value={'viewpoint':'wide','medium':'watercolor','subject':'teacher and child reading book','scene':'A teacher and child read one open book beside a wooden table.'}
  repair_pending(model,state,[{'subject':'store window'}])
  self.assertEqual(state['art_plans'][:5],old[:5]);self.assertNotEqual(state['art_plans'][5],old[5])
  self.assertEqual(state['image_subject_scores']['accepted.png'],{'positive':1})
  self.assertIn('positive',model.ask.call_args.args[1]);self.assertIn('store window',model.ask.call_args.args[1]);self.assertNotIn('pending_art_repair',state)
 def test_counter_cap_survives_reload_and_stops_generation(self):
  state=self.state()
  for _ in range(3):
   record_failure(state,5,'hero.png','subject',{});state.pop('pending_art_repair');state=json.loads(json.dumps(state))
  with self.assertRaisesRegex(ValueError,'exhausted'):record_failure(state,5,'hero.png','subject',{})
  self.assertEqual(state['stage'],'art_repair_exhausted')
 def test_rejected_mixed_language_preserves_pending_and_other_plans(self):
  state=self.state();old=copy.deepcopy(state['art_plans']);record_failure(state,0,'story.png','diversity',{})
  model=Mock();model.ask.return_value={'viewpoint':'cutaway','medium':'ink','subject':'교사 book','scene':'A book beside a table.'}
  with self.assertRaises(ValueError):repair_pending(model,state,[])
  self.assertEqual(state['art_plans'],old);self.assertIn('pending_art_repair',state)
 def test_planning_failure_is_bounded_across_jobs(self):
  state=self.state();record_failure(state,0,'story.png','subject',{})
  model=Mock();model.ask.side_effect=RuntimeError('model crashed')
  for _ in range(4):
   with self.assertRaises(RuntimeError):repair_pending(model,state,[])
   state=json.loads(json.dumps(state))
  with self.assertRaisesRegex(ValueError,'planning exhausted'):repair_pending(model,state,[])
  self.assertEqual(model.ask.call_count,4)
 def test_recent_metadata_limited_to_three_issues(self):
  issues=[{'hero':{'visual_direction':{'subject':str(i)}},'stories':[]} for i in range(4)]
  self.assertEqual([p['subject'] for p in recent_directions(issues)],['0','1','2'])
if __name__=='__main__':unittest.main()
