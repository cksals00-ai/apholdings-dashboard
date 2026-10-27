import unittest
from datetime import datetime,timedelta
import newsletter_server as s
class ReservationTests(unittest.TestCase):
 def test_waits_until_eight_without_crossing_early(self):
  now=[datetime.fromisoformat('2026-10-29T07:58:40+09:00')]; sleeps=[]
  def sleep(n):sleeps.append(n);now[0]+=timedelta(seconds=n)
  s.wait_for_publication('2026-10-29',now=lambda:now[0],sleep=sleep)
  self.assertEqual(sum(sleeps),80);self.assertTrue(all(n<=60 for n in sleeps))
 def test_due_returns_without_sleep(self):
  s.wait_for_publication('2026-10-29',now=lambda:datetime.fromisoformat('2026-10-29T08:01:00+09:00'),sleep=lambda n:self.fail('Already due'))
 def test_wrong_date_and_excessive_wait_rejected(self):
  for day,clock in [('2026-10-30','2026-10-29T07:00:00+09:00'),('2026-10-28','2026-10-29T08:00:00+09:00'),('2026-10-29','2026-10-29T02:59:00+09:00')]:
   with self.assertRaises(ValueError):s.wait_for_publication(day,now=lambda:datetime.fromisoformat(clock),sleep=lambda n:self.fail('Invalid reservation'))
if __name__=='__main__':unittest.main()
