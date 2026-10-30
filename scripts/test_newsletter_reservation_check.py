import unittest
from newsletter_reservation_check import active_for_day
class ReservationTests(unittest.TestCase):
 def test_receipt_other_day_and_completed_do_not_suppress_recovery(self):
  for title,status in [('AP News 2026-10-31 receipt','in_progress'),('AP News 2026-10-30 reservation','queued'),('AP News 2026-10-31 reservation','completed')]:
   self.assertFalse(active_for_day([{'displayTitle':title,'status':status}],'2026-10-31'))
 def test_exact_date_or_korean_today_publication_matches(self):
  self.assertTrue(active_for_day([{'displayTitle':'AP News 2026-10-31 reservation','status':'queued'}],'2026-10-31'))
  self.assertTrue(active_for_day([{'displayTitle':'AP News today publication','status':'in_progress','createdAt':'2026-10-30T23:00:00Z'}],'2026-10-31'))
if __name__=='__main__':unittest.main()
