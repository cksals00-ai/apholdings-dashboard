import io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
from newsletter_cpu import TextModel

class TimeoutBudgetTests(unittest.TestCase):
 def test_review_has_bounded_cpu_headroom_without_changing_other_profiles(self):
  for profile,expected,native in [('copy',1500,False),('art',1500,False),('review',3600,False),('review',3600,True)]:
   with self.subTest(profile=profile,native=native),tempfile.TemporaryDirectory() as folder:
    replies=([{'content':'Reason through the original factual scope.<|end|>','stop_type':'word','stopping_word':'<|start|>assistant<|channel|>final<|message|>','tokens':[123,200007,200006,173781,200005,17196,200008]}] if profile=='review' else [])+[{'content':'{"supported":true,"unsupported_claims":[]}', 'stop_type':'eos','tokens':[123,200002]}]
    with patch('newsletter_cpu.urllib.request.urlopen',side_effect=[io.BytesIO(json.dumps(x).encode()) for x in replies]) as call:
     value=TextModel('.',folder,profile=profile,native_reasoning=native).ask('source verifier','check',tokens=20)
    self.assertTrue(value['supported']);self.assertTrue(all(x.kwargs['timeout']==expected for x in call.call_args_list))
    self.assertEqual(call.call_args.args[0].full_url,'http://127.0.0.1:8080/completion')
 def test_timeout_does_not_create_success_receipt(self):
  with tempfile.TemporaryDirectory() as folder,patch('newsletter_cpu.urllib.request.urlopen',side_effect=TimeoutError):
   with self.assertRaises(TimeoutError):TextModel('.',folder,profile='review').ask('source verifier','check')
   self.assertFalse((Path(folder)/'model-outputs').exists())

if __name__=='__main__':unittest.main()
