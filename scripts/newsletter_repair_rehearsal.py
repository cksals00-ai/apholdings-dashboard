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

def seed(root,day,run,dry_run=True):
 guard(day,run,dry_run);root=Path(root);folder=root/'.production-state'
 if (folder/'draft.json').exists():
  state=json.loads((folder/'draft.json').read_text());identity(state)
  if state['asset_day']!=f'{day}-test-{run}':raise ValueError('Existing rehearsal run mismatch')
  return state
 with tempfile.TemporaryDirectory() as tmp:
  if not checkpoint.restore(Path(tmp),day,'production',run,required=True):raise ValueError('Missing published checkpoint')
  old=json.loads((Path(tmp)/'.production-state/draft.json').read_text())
 if old.get('mode')!='production' or old.get('date')!=day or len(old.get('stories',[]))!=5:raise ValueError('Invalid accepted production checkpoint')
 candidates={c['url']:c for c in old['candidates']};fresh=[];stories=[]
 for saved in old['stories']:
  prior=candidates[saved['url']];sources.publisher.official_url(saved['url'])
  if prior['published']!=saved['published'] or hashlib.sha256(prior['text'].encode()).hexdigest()!=prior['body_sha256'] or saved['source_hash']!=prior['body_sha256']:raise ValueError('Saved source identity mismatch')
  source=sources.parse_article(sources.fetch(saved['url']),saved['url'],prior['source'],prior['published'])
  if prior.get('published_at'):source['published_at']=prior['published_at']
  fresh.append(source)
  if all(isinstance(q,str) and q in source['text'] for q in saved.get('evidence',[])) and saved.get('evidence'):
   story=copy.deepcopy(saved);story['source_hash']=source['body_sha256'];story.pop('strong_review',None);stories.append(story)
 if len(stories)!=5:raise ValueError('Saved copy evidence changed; cannot seed fixed five-source rehearsal')
 target=next((s for s in stories if re.search('교육|학습|연구',s['title'])),None)
 if target is None:raise ValueError('No education/research story for controlled copy fault')
 target['title']='AI 교육이 학습 효과를 높였다는 연구 결과'
 target['summary']='이번 발표는 AI 활용 교육이 학습자의 이해도와 학습 성과를 개선했음을 입증했습니다.'
 target['fact']='이 교육 및 연구는 AI 활용이 학습 효과를 높인다는 인과관계를 입증했습니다.'
 target['review']={'supported':True,'unsupported_claims':[],'method':'rehearsal simulated weak verifier acceptance'}
 state={'date':day,'mode':'test','asset_day':f'{day}-test-{run}','input_published_today':True,'issue_number':old['issue_number'],'stories':stories,'candidates':fresh,'errors':[],'art_plans':copy.deepcopy(old['art_plans']),'editorial':copy.deepcopy(old['editorial']),'rehearsal_faults':{'copy_injected':True,'copy_url':target['url']},'stage':'rehearsal_seeded'}
 validate_plans(state['art_plans'],state['editorial']['lead_index'])
 folder.mkdir(parents=True,exist_ok=True);(folder/'draft.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');return state

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

def verify_receipts(folder):
 folder=Path(folder);state=json.loads((folder/'draft.json').read_text());day,run=identity(state);faults=state.get('rehearsal_faults',{})
 def require(ok,message):
  if not ok:raise ValueError(message)
 require(faults.get('copy_injected') and faults.get('art_injected'),'Both real rehearsal faults required')
 require(state.get('input_published_today') is True,'Published production input must remain acknowledged')
 require(not any(k in state for k in ('recipients','mail_recipients','ordinary_delivery','production_delivery')),'Ordinary delivery data forbidden')
 candidates={s['url']:s for s in state['candidates']};prior=state.get('copy_review_prior',[])
 require(len(state['stories'])==5 and all(receipt_valid(s,candidates[s['url']],prior,state['stories'][:i]) for i,s in enumerate(state['stories'])),'Five current independent strong review receipts required')
 require(any(h.get('draft',{}).get('url')==faults['copy_url'] for h in state.get('copy_history',[]) if h.get('draft')),'Injected copy rejection required')
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
  require(any(receipts.get(e['id'],{}).get('accepted') is True for e in state.get('recovery_events',[]) if e.get('stage')==stage),'Parent accepted '+stage+' notice required')
 proof={'date':day,'mode':'test','run':run,'copy_rejected':True,'strong_review_count':5,'hero_repaired':True,'parent_notices_accepted':['copy','art']}
 (folder/'recovery-proof.json').write_text(json.dumps(proof,indent=2)+'\n');return proof

if __name__=='__main__':
 parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('seed');p.add_argument('--root',type=Path,required=True);p.add_argument('--date',required=True);p.add_argument('--run',required=True);p.add_argument('--dry-run',action='store_true',required=True)
 p=sub.add_parser('verify');p.add_argument('--folder',type=Path,required=True)
 args=parser.parse_args()
 if args.command=='seed':seed(args.root,args.date,args.run,dry_run=args.dry_run)
 else:print(json.dumps(verify_receipts(args.folder)))
