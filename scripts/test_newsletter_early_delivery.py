import unittest
from datetime import datetime
import newsletter_server as s
class EarlyDelivery(unittest.TestCase):
 def test_delivery_window_starts_twenty_minutes_before_eight(self):
  self.assertFalse(s.publication_due(datetime.fromisoformat('2026-11-10T07:39:59+09:00')))
  self.assertTrue(s.publication_due(datetime.fromisoformat('2026-11-10T07:40:00+09:00')))
 def test_reservation_releases_at_seven_forty(self):
  now=[datetime.fromisoformat('2026-11-10T07:39:40+09:00')];sleeps=[]
  def sleep(n):
   from datetime import timedelta
   sleeps.append(n);now[0]+=timedelta(seconds=n)
  s.wait_for_publication('2026-11-10',now=lambda:now[0],sleep=sleep)
  self.assertEqual(sum(sleeps),20)
if __name__=='__main__':unittest.main()
