import tempfile,unittest
from unittest.mock import patch
from newsletter_scope_controls import check
class ScopeProbeTests(unittest.TestCase):
 def receipt(self,negative):
  return {'inventory':[{'field':'action','id':i,'kind':'pure_proposal' if i in (0,2,6) else 'asserted_or_mixed'} for i in range(8)],'facts':{'action':[{'sentence_id':7,'text':text} for text in negative]}}
 def test_correct_negated_attributed_proposition_passes(self):
  with tempfile.TemporaryDirectory() as folder,patch('newsletter_scope_controls.classify',return_value=self.receipt(['학습 효과가 입증되지 않았다는 보고를'])):check(None,folder)
 def test_lost_negation_attribution_or_extra_affirmative_fragment_fails(self):
  for negative in (['학습 효과가 입증됐다는 보고를'],['학습 효과가 입증되지 않았다는'],['학습 효과가 입증되지 않았다는 보고를','학습 효과가 입증']):
   with self.subTest(negative=negative),tempfile.TemporaryDirectory() as folder,patch('newsletter_scope_controls.classify',return_value=self.receipt(negative)):
    with self.assertRaisesRegex(ValueError,'scope lost'):check(None,folder)
