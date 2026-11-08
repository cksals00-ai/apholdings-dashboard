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
