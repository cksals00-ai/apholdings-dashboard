import unittest
import newsletter_environment_qualification as q
class EnvironmentTests(unittest.TestCase):
 def setUp(self):
  self.old='jobs:\n  produce:\n    runs-on: ubuntu-latest\n    steps: unchanged\n'
  self.new=self.old.replace('ubuntu-latest','ubuntu-24.04')
  self.run={'id':123,'status':'completed','conclusion':'success','head_branch':'main','head_sha':'a'*40,'event':'workflow_dispatch','path':'.github/workflows/ap-news-environment.yml'}
 def test_accepts_only_exact_os_pin_with_successful_current_revision_probe(self):
  self.assertTrue(q.evaluate(self.old,self.new,self.new,self.run,123))
 def test_rejects_worker_changes_and_unknown_os(self):
  for changed in [self.new+'extra step',self.new.replace('24.04','26.04'),self.old]:
   with self.subTest(changed=changed),self.assertRaises(ValueError):q.evaluate(self.old,changed,self.new,self.run,123)
 def test_rejects_failed_pending_other_branch_or_wrong_workflow_probe(self):
  for key,value in [('conclusion','failure'),('status','in_progress'),('head_branch','other'),('event','push'),('path','other.yml'),('id',124)]:
   bad=dict(self.run);bad[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):q.evaluate(self.old,self.new,self.new,bad,123)
 def test_rejects_probe_of_different_worker(self):
  with self.assertRaises(ValueError):q.evaluate(self.old,self.new,self.new+'extra',self.run,123)
if __name__=='__main__':unittest.main()
