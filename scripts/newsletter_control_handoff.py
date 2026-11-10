"""Reuse successful immutable control evidence, never source/copy/art from a prior issue."""
import argparse,base64,hashlib,json,os,re,shutil,subprocess
from pathlib import Path
from newsletter_frozen_controls import controls_valid
from newsletter_speech_acts import FIELDS,REVISION
from newsletter_scope_controls import CASES
from newsletter_review_spans import request_for
REPO='cksals00-ai/apholdings-dashboard'
WORKFLOW='.github/workflows/ap-news-editorial-probe.yml'
def verify_execution(run,jobs,workflow,head,runtime,digest,source_run):
 if not re.fullmatch('[a-f0-9]{40}',head) or not re.fullmatch('[a-f0-9]{40}',runtime) or not re.fullmatch('[a-f0-9]{64}',digest):raise ValueError('Immutable control identities required')
 if any(run.get(k)!=v for k,v in {'id':source_run,'status':'completed','conclusion':'success','run_attempt':1,'event':'workflow_dispatch','head_sha':head}.items()) or run.get('path','').split('@')[0]!=WORKFLOW or run.get('head_repository',{}).get('full_name')!=REPO:raise ValueError('Actual successful company control run required')
 if hashlib.sha256(workflow).hexdigest()!=digest or re.findall(rb'(?m)^\s*ref:\s*([a-f0-9]{40})\s*$',workflow)!=[runtime.encode()]:raise ValueError('Control definition/runtime differs')
 expected={f'controls ({mode}, --{mode}-only)':mode for mode in ('scope','historical')}
 rows=jobs.get('jobs',[])
 if jobs.get('total_count')!=2 or len(rows)!=2 or {j.get('name') for j in rows}!=set(expected):raise ValueError('Both complete control job inventories required')
 for job in rows:
  step='Verify '+expected[job['name']]+' controls on native-thinking CPU verifier'
  if job.get('status')!='completed' or job.get('conclusion')!='success' or not any(x.get('name')==step and x.get('conclusion')=='success' for x in job.get('steps',[])):raise ValueError('Both actual control executions must succeed')
def scope_hash(draft):
 rows=[]
 for field in FIELDS:
  for span in request_for(field,draft[field],'source-blind')['spans']:
   rows.append({'field':field,'id':span['id'],'text':span['text'],'words':[{'id':i,'text':m.group()} for i,m in enumerate(re.finditer(r'\S+',span['text']))]})
 return hashlib.sha256(json.dumps({'revision':REVISION,'sentences':rows},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def verify_artifacts(scope,proof,history,source_run,day):
 for state,mode in ((scope,'scope'),(history,'historical')):
  if any(state.get(k)!=v for k,v in {'date':day,'mode':'test','asset_day':f'{day}-test-{source_run}','historical_controls_only':True,'scope_only':mode=='scope','historical_only':mode=='historical'}.items()):raise ValueError('Control artifact identity mismatch')
 if proof.get('synthetic_regression_only') is not True or proof.get('draft',{}).get('action')!=' '.join(CASES):raise ValueError('Actual current scope dataset required')
 receipt=proof.get('receipt',{});digest=scope_hash(proof['draft'])
 if receipt.get('revision')!=REVISION or receipt.get('input_hash')!=digest or receipt.get('coverage_audit',{}).get('complete') is not True or receipt.get('coverage_audit',{}).get('issues')!=[]:raise ValueError('Complete current source-blind scope audit required')
 raw=receipt.get('independent_decisions',[])
 if len(raw)!=2 or any(r.get('input_hash')!=digest for r in raw):raise ValueError('Two actual same-input independent controls required')
 if not controls_valid(history):raise ValueError('Five current historical controls required')
 return history['frozen_control_receipts'],digest
def install(root,day,execution_run,receipts,provenance,evidence=None):
 path=Path(root)/'.production-state/draft.json';state=json.loads(path.read_text())
 if state.get('date')!=day or state.get('mode')!='test' or state.get('asset_day')!=f'{day}-test-{execution_run}':raise ValueError('Control reuse may only seed the current isolated rehearsal')
 if evidence is not None:shutil.copytree(evidence,path.parent/'qualified-control-evidence',dirs_exist_ok=True)
 state['frozen_control_receipts']=receipts;state['qualified_controls']=provenance
 temporary=path.with_suffix('.control.tmp');temporary.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');temporary.replace(path)
def api(path):return json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/'+path],text=True))
def restore(source_run,head,runtime,digest,root,day,folder):
 run=api('actions/runs/'+str(source_run));jobs=api(f'actions/runs/{source_run}/attempts/1/jobs?per_page=100')
 source=api('contents/'+WORKFLOW+'?ref='+head)
 if source.get('encoding')!='base64':raise ValueError('Cannot verify immutable control definition')
 verify_execution(run,jobs,base64.b64decode(source['content']),head,runtime,digest,source_run)
 folder=Path(folder)
 for mode in ('scope','historical'):
  target=folder/mode;target.mkdir(parents=True,exist_ok=True)
  subprocess.run(['gh','run','download',str(source_run),'--repo',REPO,'--name',f'ap-news-editorial-controls-{source_run}-{mode}','--dir',str(target)],check=True)
 read=lambda p:json.loads(p.read_text())
 receipts,scope_digest=verify_artifacts(read(folder/'scope/controls.json'),read(folder/'scope/scope-controls.json'),read(folder/'historical/controls.json'),source_run,day)
 provenance={'source_run':source_run,'url':f'https://github.com/{REPO}/actions/runs/{source_run}','runtime':runtime,'head_sha':head,'definition_sha256':digest,'scope_input_hash':scope_digest}
 install(root,day,os.environ['GITHUB_RUN_ID'],receipts,provenance,evidence=folder)
 print('Reused successful exact-runtime scope and historical evidence; fresh news/source/art generation remains required')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source-run',type=int,required=True);p.add_argument('--expected-head',required=True);p.add_argument('--expected-runtime',required=True);p.add_argument('--definition-sha',required=True);p.add_argument('--root',type=Path,required=True);p.add_argument('--date',required=True);p.add_argument('--folder',type=Path,required=True);a=p.parse_args()
 restore(a.source_run,a.expected_head,a.expected_runtime,a.definition_sha,a.root,a.date,a.folder)
