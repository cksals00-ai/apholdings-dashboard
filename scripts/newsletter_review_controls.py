"""Immutable, isolated acceptance/rejection controls for the independent editor."""
import copy
from datetime import datetime,timezone

SPECS=(('moengage_proposal','how-moengage-turned-over-400-apis-into-agent-tools-with-agentcore-gateway/',True),('agentcore_proposal','preview-web-apps-live-as-your-coding-agent-builds-them-with-amazon-bedrock-agentcore-runtime/',True),('obtained_opportunity','google-ai-for-healthcare-professionals-certificate/',False))
def inputs(state,sources,prior):
 from newsletter_copy_repair import identity
 by_url={s['url']:s for s in sources};result=[]
 for label,suffix,expected in SPECS:
  draft=next((h['draft'] for h in state.get('copy_history',[]) if isinstance(h.get('draft'),dict) and h['draft'].get('url','').endswith(suffix) and (('설계한다면' in h['draft'].get('insight','')) if expected else ('기회를 얻었습니다' in h['draft'].get('insight','')))),None)
  if draft is None or draft['url'] not in by_url:raise ValueError('Missing immutable editorial control: '+label)
  source=by_url[draft['url']];result.append((label,draft,source,identity(draft,source,prior,[]),expected))
 return result

def valid(state,sources,prior):
 from newsletter_copy_repair import REVISION
 from newsletter_cpu import PROMPT_CACHE_REVISION,ART_REV
 try:specs=inputs(state,sources,prior)
 except ValueError:return False
 receipts=state.get('editorial_control_receipts',{})
 for label,draft,source,digest,expected in specs:
  r=receipts.get(label,{})
  if not (r.get('input_hash')==digest and r.get('source_hash')==source['body_sha256'] and r.get('review_revision')==REVISION and r.get('cache_revision')==PROMPT_CACHE_REVISION and r.get('model_revision')==ART_REV and r.get('expected_supported') is expected):return False
  findings=r.get('findings')
  if expected and findings!=[]:return False
  if not expected and not opportunity_rejected(findings,draft):return False
 return True

def opportunity_rejected(findings,draft):
 return isinstance(findings,list) and any(isinstance(f,dict) and f.get('field')=='insight' and isinstance(f.get('assertion'),str) and len(f['assertion'].strip())>=2 and f['assertion'] in draft.get('insight','') and '기회' in f.get('factual_premise','') and any(w in f.get('factual_premise','') for w in ('얻','확보','obtain')) for f in findings)

def verify_controls(model,state,sources,prior,save):
 from newsletter_copy_repair import verify,REVISION
 from newsletter_cpu import PROMPT_CACHE_REVISION,ART_REV
 # This is called only through the explicitly enabled isolated rehearsal gate.
 from newsletter_repair_rehearsal import identity
 identity(state)
 for label,draft,source,digest,expected in inputs(state,sources,prior):
  previous=state.get('editorial_control_receipts',{}).get(label)
  if previous:
   # All three valid receipts short-circuit below; partial receipts still avoid
   # rerunning a matching individual control after an interrupted job.
   r=previous
   same=r.get('input_hash')==digest and r.get('source_hash')==source['body_sha256'] and r.get('review_revision')==REVISION and r.get('cache_revision')==PROMPT_CACHE_REVISION and r.get('model_revision')==ART_REV and r.get('expected_supported') is expected
   if same and ((expected and r.get('findings')==[]) or (not expected and opportunity_rejected(r.get('findings'),draft))):continue
  candidate=copy.deepcopy(draft)
  try:
   verify(model,candidate,source,prior,[])
   findings=candidate['strong_review']['review']['findings']
   if not expected:raise ValueError('Editorial control accepted unsupported obtained AP opportunity')
  except ValueError as exc:
   if expected:raise ValueError('Editorial control rejected a clean conditional recommendation: '+label+' | '+str(exc)) from exc
   findings=getattr(exc,'review',{}).get('findings')
   if not opportunity_rejected(findings,draft):raise ValueError('Editorial control did not reject the specific obtained-opportunity premise') from exc
  state.setdefault('editorial_control_receipts',{})[label]={'input_hash':digest,'source_hash':source['body_sha256'],'review_revision':REVISION,'cache_revision':PROMPT_CACHE_REVISION,'model_revision':ART_REV,'expected_supported':expected,'findings':findings,'checked_at':datetime.now(timezone.utc).isoformat()};save()
