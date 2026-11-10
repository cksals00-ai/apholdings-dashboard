import copy,json,unittest
from unittest.mock import Mock
from newsletter_speech_acts import classify,ROLES
class ExhaustiveWordScopeTests(unittest.TestCase):
 def story(self):return {'title':'공식 기능 발표','summary':'새 기능을 발표했다.','fact':'공식 기능을 제공한다.','insight':'AP가 설계한다면 권한을 나누자.','action':'도입한다면 모든 학생에게 효과가 입증된 기능을 쓰자.'}
 def model(self,mutation=None,omit=False):
  model=Mock()
  def ask(role,question,**kw):
   q=json.loads(question)
   if 'complete' in kw['schema']['properties']:return {'input_hash':q['input_hash'],'complete':not omit,'issues':[] if not omit else [{'field':'action','id':0,'reason':'Missing asserted qualification.'}]}
   row=q['sentences'][0];n=len(row['words']);field=row['field']
   scope={str(i):'factual' if field in ('title','summary','fact') or field=='action' and 1<=i<=4 else 'nonfactual' for i in range(n)}
   raw={'input_hash':q['input_hash'],'sentences':[{'field':field,'id':row['id'],'word_scope':scope,'reason':'Original scope includes every factual qualification and excludes proposed action.'}]}
   if mutation:mutation(raw,q,role,kw)
   return raw
  model.ask.side_effect=ask;return model
 def test_full_mask_copies_original_qualification_and_context(self):
  story=self.story();before=copy.deepcopy(story);model=self.model();out=classify(model,story)
  self.assertEqual(story,before);self.assertEqual(out['facts']['action'][0]['text'],'모든 학생에게 효과가 입증된');self.assertEqual(out['facts']['action'][0]['sentence_context'],story['action'])
  self.assertEqual(out['facts']['insight'],[]);self.assertEqual(model.ask.call_count,11)
  for vote in out['independent_decisions']:
   self.assertEqual(len(vote['sentences']),5);self.assertTrue(all('word_scope' in x for x in vote['sentences']))
 def test_schema_requires_every_provided_id_without_range_or_kind_guess(self):
  def check(raw,q,role,kw):
   props=kw['schema']['properties']['sentences']['items']['anyOf'][0]['properties'];scope=props['word_scope']
   expected={str(w['id']) for w in q['sentences'][0]['words']}
   self.assertEqual(set(scope['properties']),expected);self.assertEqual(set(scope['required']),expected);self.assertFalse(scope['additionalProperties']);self.assertNotIn('premises',props);self.assertNotIn('kind',props)
   self.assertEqual(list(props)[-1],'reason');self.assertEqual(kw['reasoning_effort'],'medium');self.assertNotIn('source_context',kw);self.assertNotIn('comparison_context',kw)
  classify(self.model(check),self.story())
 def test_unknown_missing_uncertain_or_legacy_scope_blocks(self):
  def missing(r,*a):r['sentences'][0]['word_scope'].pop('0')
  def extra(r,*a):r['sentences'][0]['word_scope']['99']='factual'
  def uncertain(r,*a):r['sentences'][0]['word_scope']['0']='uncertain'
  def boolean(r,*a):r['sentences'][0]['word_scope']['0']=True
  def wrong(r,*a):r['sentences'][0]['word_scope']['0']='proposal'
  def legacy(r,*a):r['sentences'][0]['premises']=[{'first_word_id':0,'last_word_id':2}]
  def duplicate(r,*a):r['sentences'].append(copy.deepcopy(r['sentences'][0]))
  def stale(r,*a):r['input_hash']='stale'
  def boolid(r,*a):r['sentences'][0]['id']=True
  def emptyfact(r,*a):r['sentences'][0]['word_scope']={k:'nonfactual' for k in r['sentences'][0]['word_scope']}
  for mutation in (missing,extra,uncertain,boolean,wrong,legacy,duplicate,stale,boolid,emptyfact):
   with self.subTest(mutation=mutation.__name__),self.assertRaises(ValueError):classify(self.model(mutation),self.story())
 def test_a_factual_gap_is_preserved_and_disagreement_blocks(self):
  def gap(raw,q,role,kw):
   if q['sentences'][0]['field']=='title' and role.startswith(ROLES[1]):raw['sentences'][0]['word_scope']['1']='nonfactual'
  with self.assertRaisesRegex(ValueError,'disagreement'):classify(self.model(gap),self.story())
 def test_disjoint_facts_never_fill_nonfactual_words(self):
  def gap(raw,q,role,kw):
   if q['sentences'][0]['field']=='title':raw['sentences'][0]['word_scope']['1']='nonfactual'
  out=classify(self.model(gap),self.story());self.assertEqual([(p['word_start'],p['word_end']) for p in out['facts']['title']],[(0,0),(2,2)])
 def test_independent_audit_still_blocks_agreeing_maps(self):
  with self.assertRaisesRegex(ValueError,'coverage'):classify(self.model(omit=True),self.story())

 def test_focused_pairs_keep_identical_complete_original_context_and_no_peer_answers(self):
  model=self.model();classify(model,self.story());calls=model.ask.call_args_list
  for i in range(0,10,2):
   a=json.loads(calls[i].args[1]);b=json.loads(calls[i+1].args[1]);self.assertEqual(a,b);self.assertEqual(len(a['sentences']),1);self.assertEqual(a['context'],self.story());self.assertNotIn('inventory',a);self.assertNotIn('decisions',a)
  self.assertEqual(len(json.loads(calls[-1].args[1])['draft']['sentences']),5)
 def test_whole_word_negative_predicates_particles_and_punctuation_are_not_retyped(self):
  for suffix in ('만','도','까지','부터','조차','마저','보다','처럼'):
   story=self.story();story['fact']='학생'+suffix+' 기능을 제공하지 않는다.'
   self.assertEqual(classify(self.model(),story)['facts']['fact'][0]['text'],story['fact'])
 def test_malformed_id_key_is_not_coerced_to_a_provided_id(self):
  for bad in ('00','-1','1.0','True'):
   def mutate(raw,*args):raw['sentences'][0]['word_scope'][bad]=raw['sentences'][0]['word_scope'].pop('0')
   with self.subTest(key=bad),self.assertRaises(ValueError):classify(self.model(mutate),self.story())
