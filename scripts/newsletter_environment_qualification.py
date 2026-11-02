"""Narrow OS compatibility migration, retaining the original full qualification."""
import argparse, base64, hashlib, json, os
import newsletter_qualification as original
PROBE='.github/workflows/ap-news-environment.yml'
PROBE_SHA256='6e412a1928665747e6a7e3020579d7968879952f38b53aa849a50983dc7b6bcb'
OLD='    runs-on: ubuntu-latest\n'
PINNED='    runs-on: ubuntu-24.04\n'
def evaluate(tested,current,probed,run,run_id):
 if tested.count(OLD)!=1 or current!=tested.replace(OLD,PINNED,1):
  raise ValueError('Only the reviewed Ubuntu 24.04 runner pin may differ from full rehearsal')
 if current!=probed:raise ValueError('Environment probe worker differs from current worker')
 if (run.get('id')!=run_id or run.get('status')!='completed' or run.get('conclusion')!='success' or run.get('head_branch')!='main' or run.get('event')!='workflow_dispatch' or run.get('path','').split('@')[0]!=PROBE):
  raise ValueError('Exact successful main environment probe required')
 return True
def qualify(full,probe,revision,runtime):
 full_run=original.api('actions/runs/'+str(full))
 tested=original.worker_at(full_run['head_sha'])
 original.evaluate(full_run,tested,tested,runtime,full)
 current=original.worker_at(revision)
 probe_run=original.api('actions/runs/'+str(probe))
 evaluate(tested,current,original.worker_at(probe_run['head_sha']),probe_run,probe)
 data=original.api('contents/'+PROBE+'?ref='+probe_run['head_sha'])
 if data.get('encoding')!='base64' or hashlib.sha256(base64.b64decode(data['content'])).hexdigest()!=PROBE_SHA256:
  raise ValueError('Environment probe definition differs from reviewed immutable proof')
 print(json.dumps({'qualified':True,'runtime':runtime,'full_rehearsal':full,'environment_probe':probe,'runner':'ubuntu-24.04'}))
 with open(os.environ['GITHUB_OUTPUT'],'a') as out:out.write('qualified=true\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--full',type=int,required=True);p.add_argument('--probe',type=int,required=True);p.add_argument('--revision',required=True);p.add_argument('--runtime',required=True);a=p.parse_args();qualify(a.full,a.probe,a.revision,a.runtime)
