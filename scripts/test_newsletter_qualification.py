import unittest
import newsletter_qualification as q
PIN='2cd3090b7bf585b9afebfc59094d9b771a853c83'
WORKER=f'          ref: {PIN}\n          path: .production-runtime\n'
def proof():return {'id':40999503801,'status':'completed','conclusion':'success','head_branch':'main','head_sha':'a'*40,'event':'workflow_dispatch','path':'.github/workflows/ap-news-production-rehearsal.yml','run_attempt':2,'triggering_actor':{'login':'github-actions[bot]'}}
class QualificationTests(unittest.TestCase):
 def test_only_actual_successful_auto_recovery_qualifies(self):
  self.assertTrue(q.evaluate(proof(),WORKER,WORKER,PIN,40999503801))
  for key,value in [('status','in_progress'),('conclusion','failure'),('head_branch','feature'),('run_attempt',1),('path','.github/workflows/unrelated.yml'),('id',1),('triggering_actor',{'login':'a-person'})]:
   run=proof();run[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):q.evaluate(run,WORKER,WORKER,PIN,40999503801)
 def test_runtime_change_or_unpinned_worker_cannot_reuse_old_proof(self):
  for current,tested in [(WORKER.replace(PIN,'b'*40),WORKER),(WORKER,WORKER.replace(PIN,'c'*40)),('ref: main\npath: .production-runtime',WORKER),(WORKER+WORKER,WORKER),(WORKER+'# additional untested step\n',WORKER)]:
   with self.assertRaises(ValueError):q.evaluate(proof(),current,tested,PIN,40999503801)
if __name__=='__main__':unittest.main()
