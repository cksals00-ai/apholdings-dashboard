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
    rows.append({'field':row['field'],'id':row['id'],'kind':'no_factual_premise' if pure else 'factual_premise_present','premises':[] if pure else [{'first_word_id':0,'last_word_id':len(row['words'])-1}],'reason':'Pure hypothetical proposal with no asserted outcome.' if pure else 'Sentence asserts a factual announcement.'})
   return {'input_hash':q['input_hash'],'sentences':rows}
  model=Mock();model.ask.side_effect=ask;return model,calls
 def story(self):return {'title':'공식 기능 발표','summary':'새 기능을 발표했다.','fact':'공식 기능을 제공한다.','insight':'AP가 설계한다면 권한을 나누자.','action':'제공 지역을 확인한다.'}
 def test_source_blind_independent_passes_and_coverage_keep_draft(self):
  model,calls=self.setup_model();story=self.story();before=copy.deepcopy(story);out=classify(model,story)
  self.assertEqual(story,before);self.assertEqual(model.ask.call_count,11)
  self.assertEqual(calls[0],calls[1]);self.assertTrue(all('inventory' not in x for x in calls[:2]))
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
  def bool_range(x):x['sentences'][0]['premises'][0]['first_word_id']=True
  def reversed_range(x):x['sentences'][0]['premises']=[{'first_word_id':2,'last_word_id':0}]
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
    if row is not None:row.update(kind='factual_premise_present',premises=[{'first_word_id':1,'last_word_id':4}])
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
    self.assertEqual(set(target['properties']['premises']['items']['properties']),{'first_word_id','last_word_id'})
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

class WordAnchorMappingTests(unittest.TestCase):
 def test_given_word_anchors_copy_exact_original_without_model_retyping(self):
  story=SpeechActTests().story();story['action']='도입한다면 모든 학생에게 효과가 입증된 기능을 쓰자.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw:
    row=next((x for x in raw['sentences'] if x['field']=='action'),None)
    if row is not None:row.update(kind='factual_premise_present',premises=[{'first_word_id':1,'last_word_id':5}])
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
  with self.assertRaisesRegex(ValueError,'anchors'):classify(model,story)

class KoreanParticleAlignmentTests(unittest.TestCase):
 def test_negative_report_and_noun_particle_are_copied_from_whole_original_words(self):
  story=SpeechActTests().story();story['action']='학습 효과가 입증되지 않았다는 보고를 확인한다.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw:
    row=next((x for x in raw['sentences'] if x['field']=='action'),None)
    if row is not None:row.update(kind='factual_premise_present',premises=[{'first_word_id':0,'last_word_id':4}])
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
   if 'sentences' in raw and raw['sentences'][0]['field']=='fact':next(x for x in raw['sentences'] if x['field']=='fact')['premises']=[{'text':'기능을 제공'}]
   return raw
  model.ask.side_effect=answer
  with self.assertRaisesRegex(ValueError,'anchors'):classify(model,story)

class TerminalPunctuationAlignmentTests(unittest.TestCase):
 def test_terminal_period_is_always_copied_from_selected_original_words(self):
  story=SpeechActTests().story();model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if 'sentences' in raw and raw['sentences'][0]['field']=='fact':next(x for x in raw['sentences'] if x['field']=='fact')['premises']=[{'first_word_id':0,'last_word_id':2}]
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
    count+=1;row=next(x for x in raw['sentences'] if x['field']=='action')
    row.update(kind='factual_premise_present',premises=[{'first_word_id':2 if count==1 else 1,'last_word_id':5}])
   return raw
  model.ask.side_effect=answer
  with self.assertRaisesRegex(ValueError,'disagreement'):classify(model,story)
  self.assertEqual(model.ask.call_count,10)
 def test_case_particles_are_always_copied_with_selected_original_words(self):
  story=SpeechActTests().story();story['action']='AP가 얻은 기회를 활용한다.'
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect;count=0
  def answer(role,question,**kw):
   nonlocal count
   raw=base(role,question,**kw)
   if 'sentences' in raw and raw['sentences'][0]['field']=='action':
    count+=1;row=next(x for x in raw['sentences'] if x['field']=='action')
    row.update(kind='factual_premise_present',premises=[{'first_word_id':0,'last_word_id':2}])
   return raw
  model.ask.side_effect=answer;part=classify(model,story)['facts']['action'][0]
  self.assertEqual(part['text'],'AP가 얻은 기회를');self.assertEqual((part['word_start'],part['word_end']),(0,2));self.assertEqual(model.ask.call_count,11)

class IndependentWholeInventoryTests(unittest.TestCase):
 def test_two_whole_draft_blind_passes_share_no_answers_and_global_audit_follows(self):
  model,calls=SpeechActTests().setup_model();receipt=classify(model,SpeechActTests().story())
  self.assertEqual(len(calls),11);self.assertEqual(calls[0],calls[1])
  for q in calls[:-1]:
   self.assertEqual(len(q['sentences']),1);self.assertEqual(len(q['context']),5);self.assertNotIn('inventory',q);self.assertNotIn('decisions',q)
  self.assertEqual(len(calls[-1]['draft']['sentences']),5)
  self.assertTrue(all(len(v['sentences'])==5 for v in receipt['independent_decisions']))

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
    with self.assertRaisesRegex(ValueError,'anchors'):classify(model,story)

class FocusedNativePairTests(unittest.TestCase):
 def test_one_complete_target_per_pair_retains_global_context_and_final_audit(self):
  model,calls=SpeechActTests().setup_model();receipt=classify(model,SpeechActTests().story())
  self.assertEqual(len(calls),11)
  for i in range(0,10,2):
   self.assertEqual(calls[i],calls[i+1]);self.assertEqual(len(calls[i]['sentences']),1)
   self.assertEqual(len(calls[i]['context']),5)
   self.assertNotIn('inventory',calls[i]);self.assertNotIn('decisions',calls[i])
  self.assertEqual(len(calls[-1]['draft']['sentences']),5)
  self.assertEqual(len(receipt['independent_decisions']),2)
  for vote in receipt['independent_decisions']:
   self.assertEqual(len(vote['sentences']),5);self.assertEqual(len(vote['requests']),5)

class AnchorBoundsSafetyTests(unittest.TestCase):
 def test_character_offsets_boolean_and_legacy_quotes_are_not_word_anchors(self):
  for part in ({'first_word_id':0,'last_word_id':11},{'first_word_id':True,'last_word_id':2},{'first_word_id':0,'last_word_id':2.0},{'first_word_id':-1,'last_word_id':2},{'first_word_id':2,'last_word_id':0},{'text':'공식 기능 발표'}):
   with self.subTest(part=part):
    model,_=SpeechActTests().setup_model();base=model.ask.side_effect
    def answer(role,question,**kw):
     result=base(role,question,**kw);result['sentences'][0]['premises']=[part];return result
    model.ask.side_effect=answer
    with self.assertRaisesRegex(ValueError,'anchors'):classify(model,SpeechActTests().story())
 def test_negative_predicates_and_all_scope_particles_remain_original_whole_words(self):
  for suffix in ('만','도','까지','부터','조차','마저','보다','처럼'):
   story=SpeechActTests().story();story['fact']='학생'+suffix+' 기능을 제공하지 않는다.'
   model,_=SpeechActTests().setup_model();receipt=classify(model,story)
   self.assertEqual(receipt['facts']['fact'][0]['text'],story['fact'])

class ExactWordCoverageTests(unittest.TestCase):
 def test_adjacent_partitions_agree_only_when_the_original_factual_word_set_is_identical(self):
  model,_=SpeechActTests().setup_model();base=model.ask.side_effect
  def answer(role,question,**kw):
   raw=base(role,question,**kw)
   if role.startswith('Independent presupposition') and raw.get('sentences',[{}])[0].get('field')=='title':
    raw['sentences'][0]['premises']=[{'first_word_id':0,'last_word_id':0},{'first_word_id':1,'last_word_id':2}]
   return raw
  model.ask.side_effect=answer;receipt=classify(model,SpeechActTests().story())
  self.assertEqual(len(receipt['facts']['title']),1);self.assertEqual(receipt['facts']['title'][0]['text'],'공식 기능 발표')
 def test_a_gap_or_overlap_cannot_be_filled_or_silently_normalized(self):
  for parts,error in (([{'first_word_id':0,'last_word_id':0},{'first_word_id':2,'last_word_id':2}],'disagreement'),([{'first_word_id':0,'last_word_id':1},{'first_word_id':1,'last_word_id':2}],'Overlapping')):
   model,_=SpeechActTests().setup_model();base=model.ask.side_effect
   def answer(role,question,**kw):
    raw=base(role,question,**kw)
    if role.startswith('Independent presupposition') and raw.get('sentences',[{}])[0].get('field')=='title':raw['sentences'][0]['premises']=parts
    return raw
   model.ask.side_effect=answer
   with self.subTest(parts=parts),self.assertRaisesRegex(ValueError,error):classify(model,SpeechActTests().story())
