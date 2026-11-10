import unittest
from newsletter_grounding import parse_json
class ModelJsonKeyTests(unittest.TestCase):
 def test_duplicate_keys_cannot_overwrite_word_scope_or_receipt_identity(self):
  for text in ('{"input_hash":"old","input_hash":"new"}','{"word_scope":{"0":"factual","0":"nonfactual"}}'):
   with self.subTest(text=text),self.assertRaises(ValueError):parse_json(text)
 def test_unique_word_scope_survives_exactly(self):
  self.assertEqual(parse_json('{"word_scope":{"0":"factual","1":"nonfactual"}}'),{'word_scope':{'0':'factual','1':'nonfactual'}})
