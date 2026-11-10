import copy,json,unittest
from unittest.mock import Mock
from newsletter_speech_acts import classify
class SpeechActTests(unittest.TestCase):
 def setup_model(self,disagree=False,omission=False):
  calls=[]
  def ask(role,question,**kw):
   self.assertNotIn('source_context',kw);self.assertNotIn('comparison_context',kw)
   q=json.loads(question);calls.append(q)
   if 'complete' in kw['schema']['properties']:return {'input_hash':q['input_hash'],'complete':not omission,'issues':[] if not omission else [{'field':'action','id':0,'reason':'Recognition presupposition omitted from the inventory.'}]}
   rows=[]
   for row in q['sentences']:
    pure=row['field'] in ('insight','action')
    if disagree and len(calls)==2 and row['field']=='action':pure=False
    rows.append({'field':row['field'],'id':row['id'],'kind':'pure_proposal' if pure else 'asserted_or_mixed','premises':[] if pure else [{'start':0,'end':len(row['words'])-1}],'reason':'Pure hypothetical proposal with no asserted outcome.' if pure else 'Sentence asserts a factual announcement.'})
   return {'input_hash':q['input_hash'],'sentences':rows}
  model=Mock();model.ask.side_effect=ask;return model,calls
 def story(self):return {'title':'공식 기능 발표','summary':'새 기능을 발표했다.','fact':'공식 기능을 제공한다.','insight':'AP가 설계한다면 권한을 나누자.','action':'제공 지역을 확인한다.'}
 def test_source_blind_independent_passes_and_coverage_keep_draft(self):
  model,calls=self.setup_model();story=self.story();before=copy.deepcopy(story);out=classify(model,story)
  self.assertEqual(story,before);self.assertEqual(model.ask.call_count,3)
  self.assertEqual(calls[0],calls[1]);self.assertNotIn('inventory',calls[1])
  self.assertEqual(out['facts']['title'][0]['text'],'공식 기능 발표');self.assertEqual(out['facts']['action'],[])
 def test_disagreement_cannot_exempt_a_sentence(self):
  model,_=self.setup_model(disagree=True)
  with self.assertRaisesRegex(ValueError,'disagreement'):classify(model,self.story())
  self.assertEqual(model.ask.call_count,2)
 def test_coverage_omission_blocks_even_when_both_classifiers_agree(self):
  model,_=self.setup_model(omission=True)
  with self.assertRaisesRegex(ValueError,'coverage'):classify(model,self.story())


def fixture_inventory(model,story):
 # Isolate old entailment tests from the separately tested speech-act stage.
 import hashlib
 facts={}
 for field,text in story.items():
  if field not in ('title','summary','fact','insight','action'):continue
  pure=(field in ('insight','action') and ('설계한다면' in text or '조건을 확인' in text or '지역별 제공 조건' in text))
  facts[field]=[] if pure else [{'sentence_id':0,'text':text,'sentence_context':text,'word_start':0,'word_end':len(text.split())-1}]
 return {'input_hash':hashlib.sha256(json.dumps(story,sort_keys=True).encode()).hexdigest(),'facts':facts,'inventory':[],'independent_decisions':[],'coverage_audit':{'complete':True,'issues':[]}}

class InvalidInventoryTests(unittest.TestCase):
 setup_model=SpeechActTests.setup_model
 story=SpeechActTests.story
 def test_invalid_inventory_never_grants_proposal_exemption(self):
  def missing(x):x['sentences'].pop()
  def duplicate(x):x['sentences'].append(copy.deepcopy(x['sentences'][0]))
  def boolean_id(x):x['sentences'][0]['id']=True
  def uncertain(x):x['sentences'][0]['kind']='uncertain'
  def pure_fact(x):x['sentences'][0].update(kind='pure_proposal',premises=[])
  def pure_with_fact(x):x['sentences'][-1]['premises']=[{'start':0,'end':0}]
  def missing_fact(x):x['sentences'][0]['premises']=[]
  def bool_range(x):x['sentences'][0]['premises'][0]['end']=True
  def reversed_range(x):x['sentences'][0]['premises']=[{'start':1,'end':0}]
  def stale(x):x['input_hash']='stale'
  for mutate in (missing,duplicate,boolean_id,uncertain,pure_fact,pure_with_fact,missing_fact,bool_range,reversed_range,stale):
   with self.subTest(mutation=mutate.__name__):
    model,_=self.setup_model();answer=model.ask.side_effect
    def changed(role,question,**kw):
     raw=answer(role,question,**kw);mutate(raw);return raw
    model.ask.side_effect=changed
    with self.assertRaises(ValueError):classify(model,self.story())
 def test_mixed_advice_exact_fact_range_preserves_full_conditional_scope(self):
  story=self.story();story['action']='도입한다면 모든 학생에게 효과가 입증된 기능을 쓰자.'
  model,_=self.setup_model();answer=model.ask.side_effect
  def changed(role,question,**kw):
   raw=answer(role,question,**kw)
   if 'sentences' in raw:
    row=next(x for x in raw['sentences'] if x['field']=='action');row.update(kind='asserted_or_mixed',premises=[{'start':1,'end':4}])
   return raw
  model.ask.side_effect=changed;out=classify(model,story);part=out['facts']['action'][0]
  self.assertEqual(part['text'],'모든 학생에게 효과가 입증된');self.assertEqual(part['sentence_context'],story['action'])

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

class WordIdProtocolTests(unittest.TestCase):
 def test_model_never_sees_character_offsets_and_each_sentence_has_its_own_word_bounds(self):
  model,calls=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   q=json.loads(question)
   if 'complete' not in kw['schema']['properties']:
    for row in q['sentences']:
     self.assertTrue(all(set(w)=={'id','text'} for w in row['words']))
    branches=kw['schema']['properties']['sentences']['items']['anyOf']
    title=next(b for b in branches if b['properties']['field']['enum']==['title'])
    self.assertEqual(title['properties']['premises']['items']['properties']['end']['enum'],[0,1,2])
   return base(role,question,**kw)
  model.ask.side_effect=answer
  classify(model,SpeechActTests().story())
