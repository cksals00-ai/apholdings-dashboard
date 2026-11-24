import copy,unittest
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import patch
import newsletter_rehearsal_resume as r

class ResumeTests(unittest.TestCase):
 def fixtures(self):
  day=datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat()
  state={'date':day,'mode':'test','asset_day':day+'-test-123','stories':[{'title':'verified','strong_review':{'supported':True}}],'image_attempts':{'old-file':2}}
  parent={'id':123,'head_branch':'main','event':'workflow_dispatch','status':'completed','conclusion':'cancelled','path':'.github/workflows/ap-news-production-rehearsal.yml','head_sha':'a'*40,'created_at':day+'T03:05:00+09:00'}
  jobs={'total_count':4,'jobs':[{'name':'produce / produce','steps':[{'name':'production'}]},{'name':'stage_preview','steps':[],'runner_id':0},{'name':'deploy','steps':[],'runner_id':0},{'name':'verify_and_mail','steps':[],'runner_id':0}]}
  return day,state,parent,jobs
 def test_resume_preserves_verified_content_and_image_namespace(self):
  day,state,parent,jobs=self.fixtures();before=copy.deepcopy(state)
  with patch.object(r,'api',side_effect=[parent,jobs]) as call:result=r.resume_state(state,day,'456','123')
  self.assertIn('filter=all',call.call_args_list[1].args[0])
  for key in before:self.assertEqual(result[key],before[key])
  self.assertEqual(result['rehearsal_execution_run'],'456')
  self.assertEqual(result['resume_history'][0]['from'],'123')
  with patch.object(r,'api') as call:self.assertEqual(r.resume_state(result,day,'456','123'),result);call.assert_not_called()
 def test_explicit_origin_and_current_test_date_required(self):
  day,state,parent,jobs=self.fixtures()
  for origin in ('','789'):
   with self.assertRaises(ValueError):r.resume_state(state,day,'456',origin)
  state['mode']='production'
  with self.assertRaises(ValueError):r.resume_state(state,day,'456','123')
 def test_published_or_running_parent_cannot_be_reused(self):
  day,state,parent,jobs=self.fixtures()
  for changes in ({'status':'in_progress'},{'conclusion':'success'},{'head_branch':'other'},{'created_at':'2000-01-01T00:00:00Z'}):
   with patch.object(r,'api',side_effect=[{**parent,**changes},jobs]):
    with self.assertRaises(ValueError):r.resume_state(copy.deepcopy(state),day,'456','123')
  jobs['jobs'][1]['steps']=[{'name':'publish preview','status':'completed'}]
  with patch.object(r,'api',side_effect=[parent,jobs]):
   with self.assertRaises(ValueError):r.resume_state(state,day,'456','123')
 def test_earlier_attempt_publication_rejects_resume(self):
  day,state,parent,jobs=self.fixtures();jobs['jobs'].append({'name':'stage_preview','steps':[{'name':'Publish preview','status':'completed'}],'runner_id':1});jobs['total_count']=len(jobs['jobs'])
  with patch.object(r,'api',side_effect=[parent,jobs]):
   with self.assertRaises(ValueError):r.resume_state(state,day,'456','123')
 def test_partial_jobs_response_fails_closed(self):
  day,state,parent,jobs=self.fixtures();jobs['total_count']=5
  with patch.object(r,'api',side_effect=[parent,jobs]):
   with self.assertRaises(ValueError):r.resume_state(state,day,'456','123')

if __name__=='__main__':unittest.main()
