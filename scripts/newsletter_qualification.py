"""Fail-closed server rollout: current runtime needs a real recovered full rehearsal."""
import argparse,base64,json,os,re,subprocess
REPO='cksals00-ai/apholdings-dashboard'
WORKER='.github/workflows/ap-news-produce.yml'
REHEARSAL='.github/workflows/ap-news-production-rehearsal.yml'
def runtime_pin(text):
 pins=re.findall(r'(?m)^\s+ref:\s*([a-f0-9]{40})\s*\n\s+path:\s*\.production-runtime\s*$',text)
 if len(pins)!=1:raise ValueError('Producer must have exactly one immutable runtime pin')
 return pins[0]
def evaluate(run,current_worker,tested_worker,expected,run_id):
 if (run.get('id')!=run_id or run.get('status')!='completed' or run.get('conclusion')!='success' or run.get('head_branch')!='main' or run.get('event')!='workflow_dispatch' or run.get('path','').split('@')[0]!=REHEARSAL or run.get('run_attempt',0)<2 or run.get('triggering_actor',{}).get('login')!='github-actions[bot]'):
  raise ValueError('Full server qualification is not yet successful with automatic recovery: '+str(run.get('status'))+'/'+str(run.get('conclusion')))
 if runtime_pin(current_worker)!=expected or runtime_pin(tested_worker)!=expected:raise ValueError('Current producer runtime differs from qualified runtime')
 return True
def api(path):return json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/'+path],text=True))
def worker_at(revision):
 if not re.fullmatch('[a-f0-9]{40}',revision):raise ValueError('Immutable workflow revision required')
 data=api('contents/'+WORKER+'?ref='+revision)
 if data.get('encoding')!='base64':raise ValueError('Cannot verify producer workflow contents')
 return base64.b64decode(data['content']).decode()
def qualify(run_id,revision,expected):
 if not re.fullmatch('[a-f0-9]{40}',expected):raise ValueError('Immutable expected runtime required')
 run=api('actions/runs/'+str(run_id))
 evaluate(run,worker_at(revision),worker_at(run['head_sha']),expected,run_id)
 print(json.dumps({'qualified':True,'runtime':expected,'rehearsal_url':f'https://github.com/{REPO}/actions/runs/{run_id}','automatic_recovery_attempt':run['run_attempt']}))
 if os.environ.get('GITHUB_OUTPUT'):
  with open(os.environ['GITHUB_OUTPUT'],'a') as out:out.write('qualified=true\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--run',type=int,required=True);p.add_argument('--revision',required=True);p.add_argument('--runtime',required=True);a=p.parse_args()
 try:qualify(a.run,a.revision,a.runtime)
 except Exception as exc:print('::error::Server production qualification failed: '+str(exc)[:300]);raise
