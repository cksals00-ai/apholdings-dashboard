import json,unittest
from unittest.mock import Mock
from newsletter_speech_acts import classify
class WordAnchorProtocolTests(unittest.TestCase):
 def test_model_selects_given_ids_and_never_retypes_korean_particle_spacing(self):
  story={'title':'AWS가 API를 발표했다.','summary':'AWS가 API를 발표했다.','fact':'AWS가 API를 발표했다.','insight':'필요하다면 검토하자.','action':'제공 지역을 확인한다.'}
  calls=[]
  def ask(role,question,**kw):
   data=json.loads(question);calls.append(data)
   if 'complete' in kw['schema']['properties']:return {'input_hash':data['input_hash'],'complete':True,'issues':[]}
   self.assertEqual(data['context'],story);self.assertNotIn('input_hash',data['context']);self.assertEqual(len(data['sentences']),1)
   row=data['sentences'][0];shape=kw['schema']['properties']['sentences']['items']['anyOf'][0]['oneOf'][0]['properties']['word_scope']
   self.assertEqual(set(shape['properties']),{str(i) for i in range(len(row['words']))})
   self.assertEqual(set(shape['required']),set(shape['properties']))
   pure=row['field'] in ('insight','action')
   return {'input_hash':data['input_hash'],'sentences':[{'field':row['field'],'id':row['id'],'kind':'no_actual_world_claim' if pure else 'actual_world_claim_present','word_scope':{str(i):'not_claim' if pure else 'claim' for i in range(len(row['words']))},'reason':'Hypothetical proposal only.' if pure else 'Full factual announcement requires support.'}]}
  model=Mock();model.ask.side_effect=ask;result=classify(model,story)
  self.assertEqual(result['facts']['summary'][0]['text'],'AWS가 API를 발표했다.')
  self.assertNotIn('input_hash',calls[-1]['draft'])
