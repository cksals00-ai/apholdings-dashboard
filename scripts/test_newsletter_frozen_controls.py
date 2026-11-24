import copy,unittest
from unittest.mock import Mock,patch
import newsletter_frozen_controls as f
class FrozenControlTests(unittest.TestCase):
 def test_unrelated_rejection_cannot_count_as_specific_fault_rejection(self):
  for label,field in [('obtained_opportunity','insight'),('false_efficacy','fact'),('all_students','action')]:
   review={'fields':[{'field':field,'verdict':'unsupported','premises':[{'claim':'다른 지원되는 문장','status':'unsupported','reason':'unrelated'}]}]}
   self.assertFalse(f.specific_rejection(label,review))
 def test_named_fault_must_have_precise_rejection(self):
  cases=[('obtained_opportunity','insight','기회를 얻었습니다','AP outcome unsupported'),('false_efficacy','fact','학습 효과를 높인다는 인과관계를 입증','causal learning efficacy unsupported'),('all_students','action','모든 학생에게 입증','universal effect unsupported')]
  for label,field,claim,reason in cases:
   review={'fields':[{'field':field,'verdict':'unsupported','premises':[{'claim':claim,'status':'unsupported','reason':reason}]}]}
   self.assertTrue(f.specific_rejection(label,review))
 def test_partial_valid_receipt_is_reused(self):
  from newsletter_copy_repair import REVISION
  from newsletter_cpu import ART_REV,PROMPT_CACHE_REVISION
  rows=f.inputs();row=rows[0];review={'supported':True,'findings':[]}
  state={'frozen_control_receipts':{row['label']:{'input_hash':row['input_hash'],'source_hash':row['source']['body_sha256'],'model_revision':ART_REV,'cache_revision':PROMPT_CACHE_REVISION,'review_revision':REVISION,'atomic_revision':f.ATOMIC_REVISION,'expected_supported':True,'historical_only':True,'review':review}}}
  with patch('newsletter_repair_rehearsal.identity'),patch('newsletter_copy_repair.verify',side_effect=ValueError('stop')) as verify:
   with self.assertRaises(ValueError):f.verify_controls(object(),state,lambda:None)
  self.assertEqual(verify.call_args.args[1]['url'],rows[1]['draft']['url'])
if __name__=='__main__':unittest.main()
