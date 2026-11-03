import datetime as dt
import unittest
from newsletter_start_window import wait_for_source_start

class WindowTests(unittest.TestCase):
    def test_real_early_run_waits_in_bounded_chunks(self):
        clock=[dt.datetime(2026,11,1,17,45,tzinfo=dt.timezone.utc)]
        waits=[]
        def sleep(seconds):
            waits.append(seconds)
            clock[0]+=dt.timedelta(seconds=seconds)
        wait_for_source_start(False, now=lambda:clock[0], sleep=sleep)
        self.assertEqual(sum(waits),1200)
        self.assertLessEqual(max(waits),60)
    def test_dry_and_on_time_never_sleep(self):
        for dry,hour,minute in [(True,17,45),(False,18,5),(False,20,0)]:
            wait_for_source_start(dry,now=lambda:dt.datetime(2026,11,1,hour,minute,tzinfo=dt.timezone.utc),sleep=lambda _:self.fail('unexpected sleep'))

    def test_workflow_wait_is_real_only_and_before_supervisor(self):
        from pathlib import Path
        text=(Path(__file__).resolve().parents[1]/'.github/workflows/ap-news-produce.yml').read_text()
        wait=text.index('- name: Wait for Korean 03:05')
        supervise=text.index('- name: Supervise credential-free')
        self.assertLess(wait,supervise)
        self.assertIn("inputs.dry_run != true",text[wait:supervise])
        source=(Path(__file__).parent/'newsletter_start_window.py').read_text()
        self.assertNotIn('supabase',source.lower())
        self.assertNotIn('dispatch',source.lower())
