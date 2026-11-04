import unittest
from newsletter_review_spans import request_for,resolve
class ReviewSpanTests(unittest.TestCase):
 def test_literal_sentences_preserve_conditional_context(self):
  r=request_for('insight','AP가 도입한다면 역할을 나눠 검토할 수 있다. 모든 학생의 효과가 입증됐다.','source-hash')
  self.assertEqual([s['text'] for s in r['spans']],['AP가 도입한다면 역할을 나눠 검토할 수 있다.','모든 학생의 효과가 입증됐다.'])
 def test_every_span_requires_explicit_disposition(self):
  r=request_for('action','조건을 확인한다. 효과가 입증됐다.','hash')
  base={'input_hash':r['input_hash'],'sentences':[{'id':0,'status':'editorial','source_ids':[],'reason':'A proposed verification task only.'}]}
  with self.assertRaises(ValueError):resolve(base,r)
  base['sentences'].append({'id':1,'status':'unsupported','source_ids':[],'reason':'Universal efficacy is absent from the source.'})
  out=resolve(base,r);self.assertEqual(out['verdict'],'unsupported');self.assertEqual(out['premises'][0]['claim'],'효과가 입증됐다.')
 def test_wrong_bool_duplicate_or_stale_identity_fails(self):
  r=request_for('fact','공식 발표다.','hash')
  for ids in ([True],[2],[0,0]):
   with self.assertRaises(ValueError):resolve({'input_hash':r['input_hash'],'sentences':[{'id':i,'status':'supported','source_ids':[0],'reason':'Supported by the official announcement.'} for i in ids]},r)
  with self.assertRaises(ValueError):resolve({'input_hash':'stale','sentences':[]},r)

def wire_for(result,request):
 """Translate legacy test decisions to transport fixtures; never used at runtime."""
 rows=[]
 for span in request['spans']:
  premises=[p for p in result['premises'] if p['claim'] in span['text']]
  status=next((x['status'] for x in premises if x['status']!='supported'),result['verdict'])
  rows.append({'id':span['id'],'status':status,'source_ids':list(dict.fromkeys(i for p in premises for i in p['source_ids'])),'reason':'; '.join(p['reason'] for p in premises) or 'Pure editorial recommendation, not an asserted outcome.'})
 return {'input_hash':request['input_hash'],'sentences':rows}
