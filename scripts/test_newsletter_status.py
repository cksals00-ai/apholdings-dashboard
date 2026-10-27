import importlib.util, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

class StatusTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('newsletter_status'),'Publication status reporting is missing')
        import newsletter_status as status
        self.s=status

    def test_event_reporting_only_calls_status_rpc_and_never_mail_or_issues(self):
        calls=[]
        def db(method,route,body):
            calls.append((method,route,body));return {'last_state':'ready'}
        with patch.object(self.s.publisher,'database',db):
            result=self.s.report_event('2026-10-27','waiting')
        self.assertEqual(result['last_state'],'ready')
        self.assertEqual(calls[0][1],'rpc/ap_news_record_publication')
        self.assertEqual(calls[0][2]['p_event'],'waiting')

    def test_unknown_event_and_malformed_date_are_rejected_before_network(self):
        with patch.object(self.s.publisher,'database',side_effect=AssertionError('No request')):
            for day,event in [('2026-10-27','sent'),('../secret','handoff')]:
                with self.assertRaises(ValueError): self.s.report_event(day,event)

    def test_ready_evidence_is_derived_from_validated_bundle_not_a_local_flag(self):
        import newsletter_handoff as h
        import hashlib
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'AP-News-2026-10-27-ready.zip'
            h.create_bundle('2026-10-27',path,reviewed=True)
            evidence=self.s.ready_metadata(path,'2026-10-27')
            self.assertEqual(evidence['number'],19)
            self.assertEqual(evidence['bundle_sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
            path.write_bytes(b'bad')
            with self.assertRaises(Exception): self.s.ready_metadata(path,'2026-10-27')

if __name__=='__main__': unittest.main()
