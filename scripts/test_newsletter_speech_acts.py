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
    if q.get('target') and (row['field'],row['id'])!=(q['target']['field'],q['target']['id']):continue
    pure=row['field'] in ('insight','action')
    if disagree and role.startswith('Independent presupposition') and row['field']=='action':pure=False
    rows.append({'field':row['field'],'id':row['id'],'kind':'no_factual_premise' if pure else 'factual_premise_present','premises':[] if pure else [{'text':row['text']}],'reason':'Pure hypothetical proposal with no asserted outcome.' if pure else 'Sentence asserts a factual announcement.'})
   return {'input_hash':q['input_hash'],'sentences':rows}
  model=Mock();model.ask.side_effect=ask;return model,calls
 def story(self):return {'title':'공식 기능 발표','summary':'새 기능을 발표했다.','fact':'공식 기능을 제공한다.','insight':'AP가 설계한다면 권한을 나누자.','action':'제공 지역을 확인한다.'}
 def test_source_blind_independent_passes_and_coverage_keep_draft(self):
  model,calls=self.setup_model();story=self.story();before=copy.deepcopy(story);out=classify(model,story)
  self.assertEqual(story,before);self.assertEqual(model.ask.call_count,11)
  self.assertEqual(calls[:5],calls[5:10]);self.assertTrue(all('inventory' not in x for x in calls[:10]))
  self.assertEqual(out['facts']['title'][0]['text'],'공식 기능 발표');self.assertEqual(out['facts']['action'],[])
 def test_disagreement_cannot_exempt_a_sentence(self):
  model,_=self.setup_model(disagree=True)
  with self.assertRaisesRegex(ValueError,'disagreement'):classify(model,self.story())
  self.assertEqual(model.ask.call_count,10)
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
  def pure_fact(x):x['sentences'][0].update(kind='no_factual_premise',premises=[])
  def pure_with_fact(x):x['sentences'][-1].update(kind='no_factual_premise',premises=[{'text':'공식'}])
  def missing_fact(x):x['sentences'][0]['premises']=[]
  def bool_range(x):x['sentences'][0]['premises'][0]['text']=True
  def reversed_range(x):x['sentences'][0]['premises']=[{'text':'발표 기능 공식'}]
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
    row=next((x for x in raw['sentences'] if x['field']=='action'),None)
    if row is not None:row.update(kind='factual_premise_present',premises=[{'text':'모든 학생에게 효과가 입증된'}])
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
    target=branches[0]
    self.assertEqual(set(target['properties']['premises']['items']['properties']),{'text'})
   return base(role,question,**kw)
  model.ask.side_effect=answer
  classify(model,SpeechActTests().story())

class UncertaintyPolicyTests(unittest.TestCase):
 def test_a_nonfactual_sounding_reason_never_turns_uncertain_into_approval(self):
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def changed(role,question,**kw):
   raw=base(role,question,**kw)
   raw['sentences'][-1].update(kind='uncertain',premises=[],reason='This is only a checking instruction and does not assert an outcome.')
   return raw
  model.ask.side_effect=changed
  with self.assertRaisesRegex(ValueError,'Uncertain'):classify(model,SpeechActTests().story())

class VerbatimMappingTests(unittest.TestCase):
 def test_quotes_map_to_exact_word_ids_without_counting_by_the_model(self):
  story=SpeechActTests().story();story['action']='도입한다면 모든 학생에게 효과가 입증된 기능을 쓰자.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw:
    row=next((x for x in raw['sentences'] if x['field']=='action'),None)
    if row is not None:row.update(kind='factual_premise_present',premises=[{'text':'모든 학생에게 효과가 입증된 기능을'}])
   return raw
  model.ask.side_effect=answer;part=classify(model,story)['facts']['action'][0]
  self.assertEqual((part['word_start'],part['word_end']),(1,5));self.assertEqual(part['text'],'모든 학생에게 효과가 입증된 기능을')
 def test_nonliteral_ambiguous_and_partial_word_quotes_fail_closed(self):
  for quote in ('공식 기능 발명','식 기능','공식  기능 발표','공식 기'):
   with self.subTest(quote=quote):
    model,_=SpeechActTests().setup_model();base=model.ask.side_effect
    def answer(role,question,**kw):
     raw=base(role,question,**kw);raw['sentences'][0]['premises']=[{'text':quote}];return raw
    model.ask.side_effect=answer
    with self.assertRaises(ValueError):classify(model,SpeechActTests().story())
  story=SpeechActTests().story();story['title']='공식 기능 공식 기능'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw);raw['sentences'][0]['premises']=[{'text':'공식 기능'}];return raw
  model.ask.side_effect=answer
  with self.assertRaisesRegex(ValueError,'ambiguous'):classify(model,story)

class KoreanParticleAlignmentTests(unittest.TestCase):
 def test_omitted_noun_particle_is_restored_from_the_original_word(self):
  story=SpeechActTests().story();story['action']='학습 효과가 입증되지 않았다는 보고를 확인한다.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw:
    row=next((x for x in raw['sentences'] if x['field']=='action'),None)
    if row is not None:row.update(kind='factual_premise_present',premises=[{'text':'학습 효과가 입증되지 않았다는 보고'}])
   else:
    q=json.loads(question);part=next(x for x in q['inventory'] if x['field']=='action')['premises'][0]
    self.assertEqual(part['text'],'학습 효과가 입증되지 않았다는 보고를')
   return raw
  model.ask.side_effect=answer;part=classify(model,story)['facts']['action'][0]
  self.assertEqual((part['word_start'],part['word_end']),(0,4));self.assertIn('입증되지 않았다는',part['text'])
 def test_expansion_retains_original_negative_suffix_instead_of_truncating_it(self):
  story=SpeechActTests().story();story['fact']='기능을 제공하지 않는다.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw and raw['sentences'][0]['field']=='fact':raw['sentences'][0]['premises']=[{'text':'기능을 제공'}]
   return raw
  model.ask.side_effect=answer
  with self.assertRaisesRegex(ValueError,'cuts a word'):classify(model,story)

class TerminalPunctuationAlignmentTests(unittest.TestCase):
 def test_terminal_period_is_restored_from_original_not_invented(self):
  story=SpeechActTests().story();model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw and raw['sentences'][0]['field']=='fact':raw['sentences'][0]['premises']=[{'text':'공식 기능을 제공한다'}]
   return raw
  model.ask.side_effect=answer;self.assertEqual(classify(model,story)['facts']['fact'][0]['text'],'공식 기능을 제공한다.')

class QuantifierScopeAgreementTests(unittest.TestCase):
 def test_missing_universal_quantifier_is_never_normalized_into_agreement(self):
  story=SpeechActTests().story();story['action']='도입한다면 모든 학생에게 효과가 입증된 기능을 쓰자.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect;count=0
  def answer(role,question,**kw):
   nonlocal count
   raw=base(role,question,**kw)
   if 'sentences' in raw and raw['sentences'][0]['field']=='action':
    count+=1;row=raw['sentences'][0]
    row.update(kind='factual_premise_present',premises=[{'text':'학생에게 효과가 입증된 기능' if count==1 else '모든 학생에게 효과가 입증된 기능을'}])
   return raw
  model.ask.side_effect=answer
  with self.assertRaisesRegex(ValueError,'disagreement'):classify(model,story)
  self.assertEqual(model.ask.call_count,10)
 def test_case_particle_variants_agree_only_on_the_exact_original_whole_words(self):
  story=SpeechActTests().story();story['action']='AP가 얻은 기회를 활용한다.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect;count=0
  def answer(role,question,**kw):
   nonlocal count
   raw=base(role,question,**kw)
   if 'sentences' in raw and raw['sentences'][0]['field']=='action':
    count+=1;row=raw['sentences'][0]
    row.update(kind='factual_premise_present',premises=[{'text':'AP가 얻은 기회' if count==1 else 'AP가 얻은 기회를'}])
   return raw
  model.ask.side_effect=answer;part=classify(model,story)['facts']['action'][0]
  self.assertEqual(part['text'],'AP가 얻은 기회를');self.assertEqual((part['word_start'],part['word_end']),(0,2));self.assertEqual(model.ask.call_count,11)

class FocusedIndependentInventoryTests(unittest.TestCase):
 def test_each_sentence_gets_two_focused_blind_decisions_before_global_audit(self):
  story=SpeechActTests().story();calls=[];model=Mock()
  def answer(role,question,**kw):
   q=json.loads(question);calls.append(q)
   self.assertNotIn('source_context',kw);self.assertNotIn('comparison_context',kw)
   if 'complete' in kw['schema']['properties']:
    self.assertEqual(len(calls),11)
    self.assertEqual(len(q['draft']['sentences']),5)
    return {'input_hash':q['input_hash'],'complete':True,'issues':[]}
   target=q['target'];row=next(x for x in q['sentences'] if (x['field'],x['id'])==(target['field'],target['id']))
   self.assertNotIn('inventory',q);self.assertNotIn('decisions',q)
   self.assertEqual(len(q['sentences']),1)
   self.assertEqual(kw['schema']['properties']['sentences']['minItems'],1)
   pure=row['field'] in ('insight','action')
   return {'input_hash':q['input_hash'],'sentences':[{'field':row['field'],'id':row['id'],'kind':'no_factual_premise' if pure else 'factual_premise_present','premises':[] if pure else [{'text':row['text']}],'reason':'No factual premise in this checking instruction.' if pure else 'This is an asserted factual announcement.'}]}
  model.ask.side_effect=answer;receipt=classify(model,story)
  self.assertEqual(calls[:5],calls[5:10]);self.assertEqual(len(receipt['independent_decisions']),2)
  self.assertTrue(all(len(v)==5 for v in receipt['independent_decisions']))

class ScopeParticleOmissionTests(unittest.TestCase):
 def test_scope_comparison_and_range_particles_are_not_silently_restored(self):
  for suffix in ('만','도','까지','부터','조차','마저','보다','처럼'):
   with self.subTest(suffix=suffix):
    story=SpeechActTests().story();story['title']='학생'+suffix+' 참여한다.'
    model,_=SpeechActTests().setup_model();base=model.ask.side_effect
    def answer(role,question,**kw):
     raw=base(role,question,**kw)
     if 'sentences' in raw and raw['sentences'][0]['field']=='title':raw['sentences'][0]['premises']=[{'text':'학생'}]
     return raw
    model.ask.side_effect=answer
    with self.assertRaisesRegex(ValueError,'cuts a word'):classify(model,story)
