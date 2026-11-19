import unittest
from newsletter_recovery_policy import qualification_only as classify, KNOWN_BLOCK

def qualification_only(workflow, payload):
    return classify(workflow, payload, KNOWN_BLOCK)


class RecoveryPolicyTests(unittest.TestCase):
    def payload(self, name='qualification', conclusion='failure'):
        return {'total_count': 2, 'jobs': [
            {'name': name, 'status': 'completed', 'conclusion': conclusion},
            {'name': 'produce', 'status': 'completed', 'conclusion': 'skipped'}]}

    def test_closed_qualification_does_not_retry_or_repeat_alert(self):
        self.assertTrue(qualification_only('AP News server production', self.payload()))

    def test_real_production_and_daily_failures_still_recover(self):
        self.assertFalse(classify('AP News server production', self.payload(), 'Unexpected credential or verifier error'))
        self.assertFalse(qualification_only('AP News server production', self.payload('produce')))
        self.assertFalse(qualification_only('AP News server daily', self.payload()))
        p = self.payload(); p['jobs'][1]['conclusion'] = 'failure'
        self.assertFalse(qualification_only('AP News server production', p))

    def test_unknown_incomplete_or_active_jobs_do_not_hide_failure(self):
        for p in [None, {}, {'total_count': 0, 'jobs': []}, self.payload()]:
            if p and p.get('jobs'): p['total_count'] = 3
            self.assertFalse(qualification_only('AP News server production', p))
        p = self.payload(); p['jobs'][1]['status'] = 'in_progress'
        self.assertFalse(qualification_only('AP News server production', p))
        p = self.payload(); p['jobs'][1]['conclusion'] = 'cancelled'
        self.assertFalse(qualification_only('AP News server production', p))


if __name__ == '__main__': unittest.main()

class RehearsalRecoveryProofTests(unittest.TestCase):
 def proof(self):
  return {'total_count':1,'jobs':[{'name':'produce / produce','status':'completed','conclusion':'failure','steps':[{'name':'Preserve source evidence and unfinished work in a private company draft release','conclusion':'success'},{'name':'Inject first-attempt failure after saving validated test bundle','conclusion':'failure'}]}]}
 def test_only_deliberate_failure_after_private_checkpoint_allows_rehearsal_retry(self):
  from newsletter_recovery_policy import planned_rehearsal_failure
  p=self.proof();self.assertTrue(planned_rehearsal_failure(p))
  for changed in ('missing_checkpoint','semantic_failure','unknown_jobs'):
   import copy
   p=copy.deepcopy(self.proof())
   if changed=='missing_checkpoint':p['jobs'][0]['steps'][0]['conclusion']='failure'
   if changed=='semantic_failure':p['jobs'][0]['steps'][1]['name']='Supervise credential-free source, copy, art and document production'
   if changed=='unknown_jobs':p['total_count']=2
   with self.subTest(changed=changed):self.assertFalse(planned_rehearsal_failure(p))
