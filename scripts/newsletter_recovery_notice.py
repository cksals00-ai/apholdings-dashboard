"""Durable repair records only. Independent server watch owns terminal mail."""
import hashlib,json,time
from pathlib import Path
POLICY='terminal-only-v1'

def notify_pending(root,day,mode,now=None):
 folder=Path(root)/'.production-state';draft=folder/'draft.json'
 if not draft.is_file():return
 state=json.loads(draft.read_text());path=folder/'notification-receipts.json'
 receipts=json.loads(path.read_text()) if path.exists() else {}
 now=time.time() if now is None else now;changed=False
 for event in state.get('recovery_events',[]):
  if not isinstance(event,dict) or event.get('notify') is False:continue
  if not all(isinstance(event.get(k),str) and event[k] for k in ('id','stage','reason')):continue
  ident=event['id'];scope=event.get('source_url') or event.get('url') or ('art-'+str(event['story_index']) if 'story_index' in event else ident)
  digest=hashlib.sha256((event['stage']+'\n'+str(scope)+'\n'+str(event.get('code','repair'))).encode()).hexdigest()[:24]
  if receipts.get(ident,{}).get('policy')==POLICY:continue
  prior=next((r for r in receipts.values() if r.get('scope_digest')==digest and r.get('policy')==POLICY),None)
  receipts[ident]=dict(prior or {'scope_digest':digest,'recorded_at':now,'recorded':True,'suppressed':True,'accepted':False,'policy':POLICY})
  changed=True
 if changed:
  temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(receipts,ensure_ascii=False,indent=2)+'\n');temporary.replace(path)
