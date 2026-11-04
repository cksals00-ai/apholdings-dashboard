import json,unittest
import newsletter_schemas as s
from newsletter_grounding import indexed_source,resolve_novelty
class NoveltyIDTests(unittest.TestCase):
 def test_quotes_and_backslashes_never_enter_grammar_enum(self):
  text='Official programme offers "train the trainer" sessions and C:\\training resources, without changing eligibility.'
  context=indexed_source({'text':text});schema=s.source_novelty(context['source_segments'])
  self.assertNotIn(text,json.dumps(schema));self.assertNotIn('novel_quote',schema['properties'])
  result=resolve_novelty({'is_news':True,'is_duplicate':False,'novel_segment_id':0,'reason':'New sessions'},context)
  self.assertEqual(result['novel_quote'],text)
 def test_invalid_or_boolean_ids_cannot_select_source(self):
  c=indexed_source({'text':'Official new programme announcement with complete source words.'})
  for value in (True,False,1,-2,'0',None):
   with self.assertRaises(ValueError):resolve_novelty({'is_news':True,'is_duplicate':False,'novel_segment_id':value,'reason':'test'},c)
 def test_no_event_keeps_empty_evidence_and_boolean_verdicts_free(self):
  c=indexed_source({'text':'Official current source describes its complete programme conditions.'})
  r=resolve_novelty({'is_news':False,'is_duplicate':False,'novel_segment_id':-1,'reason':'No event'},c)
  self.assertEqual(r['novel_quote'],'');self.assertEqual(s.source_novelty(c['source_segments'])['properties']['is_news'],{'type':'boolean'})
if __name__=='__main__':unittest.main()
