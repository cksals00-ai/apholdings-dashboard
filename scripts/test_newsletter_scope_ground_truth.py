import ast,copy,textwrap,unittest
from pathlib import Path
class StaticScopeGroundTruthTests(unittest.TestCase):
 def checker(self):
  source=(Path(__file__).resolve().parents[1]/'.github/workflows/ap-news-produce.yml').read_text()
  body=textwrap.dedent(source.split('# SCOPE_GROUND_TRUTH_BEGIN\n',1)[1].split('# SCOPE_GROUND_TRUTH_END',1)[0])
  tree=ast.parse(body);function=next(x for x in tree.body if isinstance(x,ast.FunctionDef));namespace={}
  exec(compile(ast.Module(body=[function],type_ignores=[]),'<actual-workflow-scope-check>','exec'),namespace)
  return namespace['assert_scope_ground_truth']
 def receipt(self):
  rows=[]
  for field in ('title','summary','fact','insight'):
   rows.append({'field':field,'id':0,'kind':'pure_proposal' if field=='insight' else 'asserted_or_mixed','premises':[] if field=='insight' else [{'sentence_id':0,'word_start':0,'word_end':2}]})
  ranges=[[],[(0,3)],[],[(0,2)],[(0,2)],[(1,5)],[],[(0,4)],[(0,3)],[(0,4)],[(0,5)],[(0,4)],[],[(0,2)],[(0,2)]]
  for i,parts in enumerate(ranges):rows.append({'field':'action','id':i,'kind':'asserted_or_mixed' if parts else 'pure_proposal','premises':[{'sentence_id':i,'word_start':a,'word_end':b} for a,b in parts]})
  return {'inventory':rows,'facts':{f:[p for row in rows if row['field']==f for p in row['premises']] for f in ('title','summary','fact','insight','action')}}
 def test_exact_known_linguistic_scopes_pass(self):self.assertTrue(self.checker()(self.receipt()))
 def test_two_identical_omissions_or_extra_advice_words_cannot_pass_a_true_audit_flag(self):
  check=self.checker()
  for ident,start,end in ((1,1,3),(3,1,2),(4,1,2),(5,3,5),(5,0,6),(7,2,4),(8,1,3),(9,2,4),(10,1,5),(11,0,3),(13,1,2),(14,1,2)):
   receipt=self.receipt();part=next(r for r in receipt['inventory'] if r['field']=='action' and r['id']==ident)['premises'][0];part.update(word_start=start,word_end=end)
   with self.subTest(ident=ident,start=start,end=end),self.assertRaises(ValueError):check(receipt)
 def test_missing_duplicate_or_inconsistent_inventory_never_passes(self):
  check=self.checker()
  for mutate in (lambda r:r['inventory'].pop(),lambda r:r['inventory'].append(copy.deepcopy(r['inventory'][0])),lambda r:r['facts']['fact'].clear()):
   receipt=self.receipt();mutate(receipt)
   with self.assertRaises(ValueError):check(receipt)
