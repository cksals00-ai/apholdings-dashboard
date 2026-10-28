import unittest,json,copy
from unittest.mock import patch
import newsletter_server as s
import newsletter_preflight as p
class UnattendedTests(unittest.TestCase):
 def test_candidate_fault_does_not_require_code_change(self):
  candidates=[{'url':'https://unknown.invalid/news','published':'2026-10-28'}]+[{'url':f'https://blog.google/story-{n}','published':'2026-10-28'} for n in range(5)]
  result=p.select_candidates(candidates,'2026-10-29',[])
  self.assertEqual(len(result['selected']),5);self.assertEqual(len(result['rejected']),1)
 def test_duplicate_stale_impostor_rejected_without_weakening_safety(self):
  result=p.select_candidates([{'url':'https://blog.google.evil.test/a','published':'2026-10-28'},{'url':'https://blog.google/old','published':'2026-10-01'},{'url':'https://blog.google/repeated','published':'2026-10-28'}],'2026-10-29',['https://blog.google/repeated'])
  self.assertFalse(result['ready']);self.assertFalse(result['selected'])
 def test_mail_wait_retries_pending_until_all_accepted(self):
  states=[{'active':3,'accepted':0,'pending':3},{'active':3,'accepted':3,'pending':0}]
  with patch.object(s,'database',side_effect=states),patch.object(s.time,'sleep') as sleep:
   result=s.wait_mail('2026-10-29',attempts=2)
  self.assertEqual(result['accepted'],3);sleep.assert_called_once_with(30)
 def test_mail_wait_never_reports_success_on_partial_or_uncertain(self):
  for state in ({'active':3,'accepted':2},{'active':3,'accepted':3,'uncertain':1},{'active':0,'accepted':0,'processing':1}):
   with patch.object(s,'database',return_value=state),self.assertRaises(ValueError):s.wait_mail('2026-10-29',attempts=1)
 def test_zero_active_is_valid_only_with_no_remaining_mail(self):
  with patch.object(s,'database',return_value={'active':0,'accepted':0}):self.assertEqual(s.wait_mail('2026-10-29',attempts=1)['active'],0)
if __name__=='__main__':unittest.main()
