import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
from newsletter_cpu import TextModel

class TimeoutBudgetTests(unittest.TestCase):
 def test_review_has_bounded_cpu_headroom_without_changing_other_profiles(self):
  for profile,expected in [('copy',1500),('art',1500),('review',3600)]:
   with self.subTest(profile=profile),tempfile.TemporaryDirectory() as folder:
    response=MagicMock();response.__enter__.return_value.read.return_value=json.dumps({'content':'{"supported":true,"unsupported_claims":[]}'}).encode()
    with patch('newsletter_cpu.urllib.request.urlopen',return_value=response) as call:
     value=TextModel('.',folder,profile=profile).ask('source verifier','check',tokens=20)
    self.assertTrue(value['supported']);self.assertEqual(call.call_args.kwargs['timeout'],expected)
    self.assertEqual(call.call_args.args[0].full_url,'http://127.0.0.1:8080/completion')
 def test_timeout_does_not_create_success_receipt(self):
  with tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',side_effect=TimeoutError):
   with self.assertRaises(TimeoutError):TextModel('.',folder,profile='review').ask('source verifier','check')
   self.assertFalse((Path(folder)/'model-outputs').exists())

if __name__=='__main__':unittest.main()
