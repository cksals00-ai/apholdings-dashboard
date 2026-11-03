"""Reuse private, same-day test work without changing any accepted content/assets."""
import json,re
from datetime import datetime
from zoneinfo import ZoneInfo
import newsletter_checkpoint as checkpoint

def api(path):
 result=checkpoint.gh('api',f'repos/{checkpoint.REPO}/'+path)
 if result.returncode:raise RuntimeError('Cannot establish rehearsal origin')
 return json.loads(result.stdout)

def resume_state(state,day,run,origin):
 current=datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat()
 match=re.fullmatch(re.escape(day)+r'-test-([0-9]+)',state.get('asset_day',''))
 if day!=current or state.get('date')!=day or state.get('mode')!='test' or not match or not re.fullmatch(r'[0-9]+',run):raise ValueError('Only current-day isolated test work can resume')
 existing=str(state.get('rehearsal_execution_run',match.group(1)))
 if not re.fullmatch(r'[0-9]+',existing):raise ValueError('Invalid execution origin')
 if existing==run:
  history=state.get('resume_history',[])
  if history and history[-1].get('from')==origin and history[-1].get('to')==run and re.fullmatch(r'[a-f0-9]{40}',history[-1].get('origin_revision','')):return state
  raise ValueError('Missing resume provenance')
 if not origin or origin!=existing:raise ValueError('Explicit checkpoint origin required')
 parent=api('actions/runs/'+origin)
 if (parent.get('id')!=int(origin) or parent.get('head_branch')!='main' or parent.get('event')!='workflow_dispatch' or parent.get('status')!='completed' or parent.get('conclusion') not in ('cancelled','failure','timed_out') or parent.get('path','').split('@')[0]!='.github/workflows/ap-news-production-rehearsal.yml' or not re.fullmatch(r'[a-f0-9]{40}',parent.get('head_sha',''))):raise ValueError('Only interrupted main rehearsal can resume')
 try:parent_day=datetime.fromisoformat(parent['created_at'].replace('Z','+00:00')).astimezone(ZoneInfo('Asia/Seoul')).date().isoformat()
 except Exception:raise ValueError('Unknown parent creation time')
 if parent_day!=day:raise ValueError('Cross-day rehearsal reuse forbidden')
 jobs=api('actions/runs/'+origin+'/jobs?filter=all&per_page=100')
 rows=jobs.get('jobs')
 if not isinstance(rows,list) or not rows or jobs.get('total_count')!=len(rows) or {j.get('name') for j in rows}!={'produce / produce','stage_preview','deploy','verify_and_mail'}:raise ValueError('Unknown rehearsal job history')
 for job in rows:
  if job.get('name')=='produce / produce':continue
  if not isinstance(job.get('steps'),list) or job['steps'] or job.get('runner_id') not in (None,0):raise ValueError('Preview or delivery may already have run; do not mutate its image namespace')
 state['rehearsal_execution_run']=run
 state.setdefault('resume_history',[]).append({'from':origin,'to':run,'origin_revision':parent['head_sha']})
 return state
