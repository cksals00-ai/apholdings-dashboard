import unittest
from newsletter_grounding import indexed_source,resolve_evidence,normalized
class EvidenceTests(unittest.TestCase):
 def test_schema_bounds_ids_to_this_source(self):
  from newsletter_schemas import indexed_draft
  field=indexed_draft(2)['properties']['evidence_ids']
  self.assertEqual(field['items']['maximum'],1)
  self.assertEqual(field['maxItems'],2)
 def test_all_source_content_retained_and_bounded(self):
  source={'text':('Exact source with scope and caveats. '*80)+'Final qualification.','title':'Source'}
  indexed=indexed_source(source)
  self.assertNotIn('text',indexed)
  self.assertEqual(normalized(' '.join(s['text'] for s in indexed['source_segments'])),normalized(source['text']))
  self.assertTrue(all(30<=len(s['text'])<=800 for s in indexed['source_segments']))
 def test_selected_indices_extract_original_untranslated_text(self):
  indexed=indexed_source({'text':'NVIDIA uses its original architecture in selected preview regions.'})
  draft=resolve_evidence({'fact':'원문 사실','evidence_ids':[0]},indexed)
  self.assertEqual(draft['evidence'],[indexed['source_segments'][0]['text']])
  self.assertNotIn('evidence_ids',draft)
 def test_invalid_duplicate_boolean_or_out_of_range_indices_rejected(self):
  indexed=indexed_source({'text':'A genuine official source paragraph has enough original words.'})
  for ids in ([],[0,0],[1],[-1],[True],['0']):
   with self.subTest(ids=ids),self.assertRaises(ValueError):resolve_evidence({'evidence_ids':ids},indexed)
if __name__=='__main__':unittest.main()
