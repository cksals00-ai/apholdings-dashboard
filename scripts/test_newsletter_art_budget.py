import json,unittest
import newsletter_art_repair as r
class PlanBudgetTests(unittest.TestCase):
 def test_restart_cannot_reset_same_plan_sample_allowance(self):
  state={}
  r.begin_plan_sample(state,'a fixed scene');r.begin_plan_sample(state,'a fixed scene')
  restored=json.loads(json.dumps(state));self.assertEqual(r.remaining_plan_samples(restored,'a fixed scene'),1)
  r.begin_plan_sample(restored,'a fixed scene');self.assertEqual(r.remaining_plan_samples(restored,'a fixed scene'),0)
  with self.assertRaises(ValueError):r.begin_plan_sample(restored,'a fixed scene')
  self.assertEqual(r.remaining_plan_samples(restored,'a different corrected scene'),3)
if __name__=='__main__':unittest.main()
