import copy,json,unittest
from unittest.mock import Mock
class SpeechActTests:
 def story(self):return {'title':'공식 기능 발표','summary':'새 기능을 발표했다.','fact':'공식 기능을 제공한다.','insight':'AP가 설계한다면 권한을 나누자.','action':'제공 지역을 확인한다.'}

def fixture_inventory(model,story):
 # Isolate old entailment tests from the separately tested speech-act stage.
 import hashlib
 facts={}
 for field,text in story.items():
  if field not in ('title','summary','fact','insight','action'):continue
  pure=(field in ('insight','action') and ('설계한다면' in text or '조건을 확인' in text or '지역별 제공 조건' in text))
  facts[field]=[] if pure else [{'sentence_id':0,'text':text,'sentence_context':text,'word_start':0,'word_end':len(text.split())-1}]
 return {'input_hash':hashlib.sha256(json.dumps(story,sort_keys=True).encode()).hexdigest(),'facts':facts,'inventory':[],'independent_decisions':[],'coverage_audit':{'complete':True,'issues':[]}}

class AtomicIntegrationTests(unittest.TestCase):
 def test_inventory_failure_stops_before_any_source_entailment(self):
  from unittest.mock import patch
  from newsletter_atomic_review import review_fields
  model=Mock();story=SpeechActTests().story()
  with patch('newsletter_speech_acts.classify',side_effect=ValueError('coverage failed')):
   with self.assertRaisesRegex(ValueError,'coverage'):review_fields(model,story,{'source_segments':[]})
  model.ask.assert_not_called()
 def test_pure_proposal_requires_certified_inventory_and_is_absent_from_entailment_audit(self):
  from unittest.mock import patch
  from newsletter_atomic_review import review_fields
  model=Mock();story=SpeechActTests().story();story['action']='지역별 제공 조건을 확인한다.'
  def inventory(m,s):
   m.ask.assert_not_called();return fixture_inventory(m,s)
  def answer(role,question,**kw):
   q=json.loads(question)
   if 'consistent' in kw['schema']['properties']:
    self.assertNotIn('AP가',question)
    return {'consistent':True,'complete':True,'reason':'Every extracted factual premise has valid source evidence.','issues':[]}
   self.assertNotIn(q['field'],('insight','action'))
   return {'input_hash':q['input_hash'],'sentences':[{'id':x['id'],'status':'supported','source_ids':[0],'reason':'The source directly supports this asserted factual premise.'} for x in q['spans']]}
  model.ask.side_effect=answer
  with patch('newsletter_speech_acts.classify',side_effect=inventory):out=review_fields(model,story,{'source_segments':[{'id':0,'text':'Official feature announcement'}]})
  self.assertTrue(out['supported']);self.assertIn('speech_inventory',out);self.assertEqual(model.ask.call_count,4)

class MixedFieldIsolationTests(unittest.TestCase):
 def test_separate_certified_proposal_never_reenters_source_aware_review(self):
  from unittest.mock import patch
  from newsletter_atomic_review import review_fields
  story=SpeechActTests().story();story['insight']='공식 기능을 제공한다. AP가 설계한다면 권한을 나누자.';story['action']='지역별 제공 조건을 확인한다.'
  receipt=fixture_inventory(None,story);receipt['facts']['insight']=[{'sentence_id':0,'text':'공식 기능을 제공한다.','sentence_context':'공식 기능을 제공한다.','word_start':0,'word_end':2}]
  model=Mock()
  def answer(role,question,**kw):
   q=json.loads(question);self.assertNotIn('AP가',question)
   if 'consistent' in kw['schema']['properties']:return {'consistent':True,'complete':True,'reason':'All asserted spans supported by source evidence.','issues':[]}
   self.assertNotIn('text',q)
   return {'input_hash':q['input_hash'],'sentences':[{'id':x['id'],'status':'supported','source_ids':[0],'reason':'The source supports this precise factual span.'} for x in q['spans']]}
  model.ask.side_effect=answer
  with patch('newsletter_speech_acts.classify',return_value=receipt):out=review_fields(model,story,{'source_segments':[{'id':0,'text':'Official feature'}]})
  self.assertTrue(out['supported']);self.assertEqual(out['fields'][3]['text'],story['insight'])
