"""Parent-only recovery notices; never expose mail credentials to model children."""
import hashlib,json,os,time
from pathlib import Path
from newsletter_ops import emit
MAX_ATTEMPTS=5

def notify_pending(root,day,mode,now=None):
 root=Path(root);folder=root/'.production-state';draft=folder/'draft.json'
 if not draft.is_file() or not os.environ.get('SUPABASE_SERVICE_KEY'):return
 state=json.loads(draft.read_text());receipt_path=folder/'notification-receipts.json'
 receipts=json.loads(receipt_path.read_text()) if receipt_path.exists() else {};now=time.time() if now is None else now
 for event in state.get('recovery_events',[]):
  if not isinstance(event,dict) or not all(isinstance(event.get(k),str) and event[k] for k in ('id','stage','reason')):continue
  ident=event['id']
  scope=event.get('source_url') or event.get('url') or ('art-'+str(event['story_index']) if 'story_index' in event else ident)
  digest=hashlib.sha256((event['stage']+'\n'+str(scope)+'\n'+str(event.get('code','repair'))).encode()).hexdigest()[:24]
  related=[r for r in receipts.values() if r.get('scope_digest')==digest]
  if any(r.get('accepted') for r in related):continue
  prior=max(related,key=lambda r:r.get('attempts',0),default={})
  if prior.get('attempts',0)>=MAX_ATTEMPTS or now-prior.get('last_attempt',-1000)<60:continue
  run=os.environ.get('GITHUB_RUN_ID','')
  if not run.isdigit():continue
  key=('test-'+run if mode=='test' else day)+':repair-'+digest
  detail={'subject':('[AP News 테스트 자동 교정 감지] ' if mode=='test' else '[AP News 자동 교정 감지] ')+day,'message':f"{event['stage'][:40]} 단계에서 문제를 발견했습니다: {event['reason'][:400]} 자동 교정 또는 해당 단계 재계획을 진행합니다. 아직 전체 제작·발행·메일 완료가 아닙니다.",'run_url':f'https://github.com/cksals00-ai/apholdings-dashboard/actions/runs/{run}'}
  row={'scope_digest':digest,'attempts':prior.get('attempts',0)+1,'last_attempt':now,'accepted':False}
  try:
   result=emit(key,'test_alert' if mode=='test' else 'ops_alert',detail)
   row['accepted']=result.get('accepted') is True
  except Exception as exc:row['error_type']=type(exc).__name__
  receipts[ident]=row
  temporary=receipt_path.with_suffix('.tmp');temporary.write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n');temporary.replace(receipt_path)
