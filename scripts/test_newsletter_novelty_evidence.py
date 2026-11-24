import unittest
from unittest.mock import Mock
import newsletter_schemas as shapes
from newsletter_grounding import indexed_source,resolve_novelty
class NoveltyEvidenceTests(unittest.TestCase):
 def test_only_original_source_paragraphs_can_be_selected(self):
  source={'text':'An official new programme has been announced for healthcare professionals. '*15}
  context=indexed_source(source);schema=shapes.source_novelty(context['source_segments'])
  ids=schema['properties']['novel_segment_id'];self.assertEqual(ids,{'type':'integer','minimum':-1,'maximum':len(context['source_segments'])-1})
  for i,part in enumerate(context['source_segments']):
   r=resolve_novelty({'is_news':True,'is_duplicate':False,'novel_segment_id':i,'reason':'new event'},context);self.assertEqual(r['novel_quote'],part['text'])
  self.assertEqual(schema['properties']['is_news'],{'type':'boolean'});self.assertEqual(schema['properties']['is_duplicate'],{'type':'boolean'})
 def test_writer_and_independent_verifier_use_source_bound_choices(self):
  from newsletter_producer import draft_story
  from newsletter_copy_repair import verify
  source={'title':'New AI programme','text':'An official new AI programme has been announced for healthcare professionals.','body_sha256':'body'}
  for function in (draft_story,verify):
   model=Mock();model.ask.return_value={'is_news':False,'is_duplicate':False,'novel_segment_id':-1,'reason':'no new event'}
   with self.assertRaises(ValueError):
    if function is draft_story:function(model,source,[])
    else:function(model,{},source,[])
   self.assertEqual(model.ask.call_args.kwargs['schema']['properties']['novel_segment_id']['maximum'],0);self.assertEqual(model.ask.call_count,1)
 def test_empty_or_non_source_choices_fail_closed(self):
  for rows in ([],[{'text':'too short'}],[{'text':'x'*801}],[{'text':None}]):
   with self.assertRaises(ValueError):shapes.source_novelty(rows)
 def test_long_valid_paragraph_is_not_truncated(self):
  text='Official announcement: '+('complete source words '*34);self.assertTrue(700<len(text)<=800)
  context={'source_segments':[{'id':0,'text':text}]};shapes.source_novelty(context['source_segments'])
  self.assertEqual(resolve_novelty({'is_news':True,'is_duplicate':False,'novel_segment_id':0,'reason':'new'},context)['novel_quote'],text)
if __name__=='__main__':unittest.main()
