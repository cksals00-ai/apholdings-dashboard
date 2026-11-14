"""Parent-only isolated rehearsal. No publishing, recipient lookup, or mail calls."""
import argparse,copy,hashlib,json,os,re,tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import newsletter_checkpoint as checkpoint
import newsletter_sources as sources
from newsletter_art_direction import complete_plan,validate_plans
from newsletter_copy_repair import receipt_valid

def today():return datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat()
def guard(day,run,dry_run):
 if os.environ.get('AP_NEWS_REPAIR_REHEARSAL')!='1' or dry_run is not True:raise ValueError('Rehearsal requires explicit enabled dry run')
 if day!=today() or not isinstance(run,str) or not re.fullmatch(r'[0-9]+',run):raise ValueError('Rehearsal requires current KST date and numeric run')
def identity(state):
 day=state['date'];prefix=day+'-test-';asset=state.get('asset_day','')
 if state.get('mode')!='test' or not asset.startswith(prefix):raise ValueError('Rehearsal must remain isolated test')
 run=asset[len(prefix):];guard(day,run,True);return day,run

def seed(root,day,run,dry_run=True,resume_run=""):
 guard(day,run,dry_run);root=Path(root);folder=root/'.production-state'
 if (folder/'draft.json').exists():
  state=json.loads((folder/'draft.json').read_text());identity(state)
  if state['asset_day']!=f'{day}-test-{run}':
   from newsletter_rehearsal_resume import resume_state
   state=resume_state(state,day,run,resume_run)
   (folder/'draft.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
  return state
 state={'date':day,'mode':'test','asset_day':f'{day}-test-{run}','input_published_today':False,'stories':[],'errors':[],'rehearsal_version':2,'rehearsal_faults':{},'stage':'rehearsal_fresh_seed'}
 folder.mkdir(parents=True,exist_ok=True);(folder/'draft.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');return state

def inject_copy_fault(state):
 if state.get('rehearsal_version')!=2:return False
 identity(state)
 faults=state.setdefault('rehearsal_faults',{})
 if faults.get('copy_injected') or len(state.get('stories',[]))!=5:return False
 target,advice=state['stories'][:2]
 target['fact']='이번 발표는 AI가 모든 학습자의 학습 효과를 높인다는 인과관계를 입증했습니다.'
 advice['action']='AI 교육 효과가 모든 학생에게 입증됐으므로 AP 교육에 전면 적용한다.'
 for story in (target,advice):story.pop('strong_review',None)
 faults.update(copy_injected=True,copy_url=target['url'],advice_premise_injected=True,advice_url=advice['url'])
 return True

def inject_art_fault(state,dry_run,enabled):
 if not enabled:return False
 if dry_run is not True:raise ValueError('Art rehearsal cannot run in production')
 identity(state);faults=state.setdefault('rehearsal_faults',{})
 if faults.get('art_injected'):return False
 if not faults.get('copy_injected'):raise ValueError('Only labelled repair rehearsal may inject art fault')
 hero=next(p for p in state['art_plans'] if p['story_index']==5)
 faulty=complete_plan({'viewpoint':hero['viewpoint'],'medium':hero['medium'],'subject':'A red sports car','scene':'Yellow flowers stand in an ivory vase on a wooden table.'},5)
 state['art_plans']=[faulty if p['story_index']==5 else p for p in state['art_plans']]
 validate_plans(state['art_plans'],state['editorial']['lead_index']);faults.update(art_injected=True,art_failed_plan=copy.deepcopy(faulty));return True

def advice_fault_rejected(history,faults):
 for item in history:
  draft=item.get('draft') or {};reason=str(item.get('reason','')).casefold();compact=re.sub(r'\s+','',reason)
  if draft.get('url')!=faults.get('advice_url') or '모든 학생에게 입증' not in draft.get('action','') or not reason.startswith('independent source review rejected draft:'):continue
  universal=any(term in compact for term in ('모든학생','allstudents','alllearners','universal'))
  efficacy=any(term in reason for term in ('효과','학습','efficacy','learning'))
  if universal and efficacy:return True
 return False

def cache_challenge_inputs(state,sources,prior):
 from newsletter_copy_repair import identity
 faults=state.get('rehearsal_faults',{});by_url={s['url']:s for s in sources};result=[]
 for label,key in (('copy','copy_url'),('advice','advice_url')):
  url=faults.get(key);draft=next((h['draft'] for h in state.get('copy_history',[]) if (h.get('draft') or {}).get('url')==url),None)
  if not draft or url not in by_url:raise ValueError('Missing archived controlled faulty copy')
  source=by_url[url];result.append((label,draft,source,identity(draft,source,prior,[])))
 return result

def cache_rejection_matches(label,draft,reason,faults):
 if not reason.startswith('Independent source review rejected draft:'):return False
 if label=='advice':return advice_fault_rejected([{'draft':draft,'reason':reason}],faults)
 compact=re.sub(r'\s+','',reason.casefold())
 return any(term in compact for term in ('학습효과','인과','learningefficacy','learningoutcome')) and any(term in compact for term in ('입증','높였','improv','causal','prove'))

def cache_challenge_receipts_valid(state,sources,prior):
 from newsletter_cpu import PROMPT_CACHE_REVISION,REVIEW_REV
 try:specs=cache_challenge_inputs(state,sources,prior)
 except ValueError:return False
 from newsletter_review_controls import valid
 if not valid(state,sources,prior):return False
 receipts=state.get('resumed_cache_checks',{})
 return all(receipts.get(label,{}).get('input_hash')==digest and receipts[label].get('cache_revision')==PROMPT_CACHE_REVISION and receipts[label].get('model_revision')==REVIEW_REV and receipts[label].get('rejected') is True and cache_rejection_matches(label,draft,str(receipts[label].get('reason','')),state['rehearsal_faults']) for label,draft,source,digest in specs)

def verify_resumed_cache_challenges(model,state,sources,prior,save):
 from newsletter_copy_repair import verify
 from newsletter_cpu import PROMPT_CACHE_REVISION,REVIEW_REV
 identity(state)
 from newsletter_review_controls import verify_controls
 verify_controls(model,state,sources,prior,save)
 for label,draft,source,digest in cache_challenge_inputs(state,sources,prior):
  receipt=state.get('resumed_cache_checks',{}).get(label,{})
  if receipt.get('input_hash')==digest and receipt.get('cache_revision')==PROMPT_CACHE_REVISION and receipt.get('model_revision')==REVIEW_REV and receipt.get('rejected') is True and cache_rejection_matches(label,draft,str(receipt.get('reason','')),state['rehearsal_faults']):continue
  try:verify(model,copy.deepcopy(draft),source,prior,[])
  except ValueError as exc:
   reason=str(exc)
   if not cache_rejection_matches(label,draft,reason,state['rehearsal_faults']):raise ValueError('Controlled factual premise was not specifically rejected: '+reason)
   state.setdefault('resumed_cache_checks',{})[label]={'input_hash':digest,'cache_revision':PROMPT_CACHE_REVISION,'model_revision':REVIEW_REV,'rejected':True,'reason':reason,'checked_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat()};save()
  else:raise ValueError('Controlled faulty copy passed after prompt cache change')

def verify_receipts(folder):
 folder=Path(folder);state=json.loads((folder/'draft.json').read_text());day,asset_run=identity(state);run=state.get('rehearsal_execution_run',asset_run);guard(day,run,True);faults=state.get('rehearsal_faults',{})
 def require(ok,message):
  if not ok:raise ValueError(message)
 require(faults.get('copy_injected') and faults.get('art_injected'),'Both real rehearsal faults required')
 require(state.get('rehearsal_version')==2 or state.get('input_published_today') is True,'Recognized immutable rehearsal input required')
 require(not any(k in state for k in ('recipients','mail_recipients','ordinary_delivery','production_delivery')),'Ordinary delivery data forbidden')
 candidates={s['url']:s for s in state['candidates']};prior=state.get('copy_review_prior',[])
 if state.get('rehearsal_version')==2:
  from newsletter_frozen_controls import controls_valid
  require(controls_valid(state),'Five immutable historical editorial controls required')
 elif state.get('resume_history'):require(cache_challenge_receipts_valid(state,state['candidates'],prior),'Resumed cache must reject both archived factual faults under current prompt layout')
 require(len(state['stories'])==5 and all(receipt_valid(s,candidates[s['url']],prior,state['stories'][:i]) for i,s in enumerate(state['stories'])),'Five current independent strong review receipts required')
 require(any(h.get('draft',{}).get('url')==faults['copy_url'] for h in state.get('copy_history',[]) if h.get('draft')),'Injected copy rejection required')
 require(faults.get('advice_premise_injected') and advice_fault_rejected(state.get('copy_history',[]),faults),'Unsupported factual premise in advice must be rejected')
 require(all('모든 학생에게 입증' not in s.get('action','') for s in state['stories']),'Unsupported advice premise survived')
 failures=[f for f in state.get('art_failures',[]) if f.get('story_index')==5]
 history=[h for h in state.get('art_repair_history',[]) if h.get('failure',{}).get('story_index')==5]
 require(failures and history,'Actual hero failure and replan required')
 require(any(f.get('reason')=='subject' and isinstance(f.get('scores'),dict) and f['scores'] for f in failures),'Actual CLIP subject rejection receipt required')
 require(state.get('image_attempts',{}).get(state['asset_day']+'-hero-original.png',0)>=4,'Three rejected image samples plus repaired generation required')
 require(all((folder.parent/'img/newsletter'/f"{state['asset_day']}-story-{i}.png").is_file() for i in range(1,6)),'Five accepted story images must survive repair')
 require(any(h['failure']['failed_plan']==faults['art_failed_plan'] for h in history),'Injected hero must be the rejected plan')
 hero=next(p for p in state['art_plans'] if p['story_index']==5)
 require(hero['subject']!=faults['art_failed_plan']['subject'] and hero['scene']!=faults['art_failed_plan']['scene'],'Hero fault must be replaced')
 receipts=json.loads((folder/'notification-receipts.json').read_text())
 for stage in ('copy','art'):
  require(any(receipts.get(e['id'],{}).get('recorded') is True and receipts[e['id']].get('suppressed') is True and receipts[e['id']].get('accepted') is False and receipts[e['id']].get('policy')=='terminal-only-v1' for e in state.get('recovery_events',[]) if e.get('stage')==stage),'Silent parent '+stage+' repair record required')
 proof={'date':day,'mode':'test','run':run,'asset_run':asset_run,'resume_history':state.get('resume_history',[]),'copy_rejected':True,'recommendation_premise_rejected':True,'strong_review_count':5,'hero_repaired':True,'parent_repair_records':['copy','art'],'recoverable_mail_sent':0,'resumed_cache_faults_rechecked':bool(state.get('resume_history')),'editorial_controls':state.get('frozen_control_receipts',{}) if state.get('rehearsal_version')==2 else state.get('editorial_control_receipts',{})}
 (folder/'recovery-proof.json').write_text(json.dumps(proof,indent=2)+'\n');return proof

if __name__=='__main__':
 parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('seed');p.add_argument('--root',type=Path,required=True);p.add_argument('--date',required=True);p.add_argument('--run',required=True);p.add_argument('--dry-run',action='store_true',required=True);p.add_argument('--resume-run',default='')
 p=sub.add_parser('verify');p.add_argument('--folder',type=Path,required=True)
 args=parser.parse_args()
 if args.command=='seed':seed(args.root,args.date,args.run,dry_run=args.dry_run,resume_run=args.resume_run)
 else:print(json.dumps(verify_receipts(args.folder)))
