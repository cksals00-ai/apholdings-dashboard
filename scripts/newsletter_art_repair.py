"""Durable per-image repair; accepted assets and other plans are never mutated."""
import copy,json
from newsletter_art_direction import ROLE,VIEWS,MEDIA,scene_schema,complete_plan,validate_plans
MAX_REPLANS=3

def recent_directions(issues):
 return [item['visual_direction'] for issue in issues[:3] for item in [issue.get('hero',{})]+[s.get('image',{}) for s in issue.get('stories',[])] if isinstance(item.get('visual_direction'),dict)]

def record_failure(state,index,name,reason,scores):
 count=state.setdefault('art_repair_counts',{}).get(str(index),0)
 failure={'story_index':index,'name':name,'reason':reason,'scores':scores,'failed_plan':copy.deepcopy(next(p for p in state['art_plans'] if p['story_index']==index)),'repair_number':count+1}
 state.setdefault('art_failures',[]).append(failure)
 exhausted=count>=MAX_REPLANS
 state.setdefault('recovery_events',[]).append({'stage':'art','id':f'{name}:repair:{count+1}','reason':reason,'story_index':index,'exhausted':exhausted})
 if exhausted:
  state['stage']='art_repair_exhausted'
  raise ValueError('Art repair exhausted: '+name)
 state['art_repair_counts'][str(index)]=count+1
 state['pending_art_repair']=failure;state['stage']='needs_art_repair'
 return failure

def repair_pending(model,state,recent=None,on_progress=None):
 failure=state.get('pending_art_repair')
 if not failure:return False
 index=failure['story_index'];plans=state['art_plans'];lead=state['editorial']['lead_index']
 facts=state['stories'][lead if index==5 else index]
 context={'article':{k:facts[k] for k in ('title','summary','fact')},'failure':failure,'other_accepted_plans':[p for p in plans if p['story_index']!=index],'last_three_issue_directions':recent or []}
 views=list(VIEWS);media=list(MEDIA)
 # Preserve the six-plan diversity constraints, regardless of model choice.
 for attempt in range(2):
  key=f"{index}:{failure['repair_number']}"
  attempts=state.setdefault('art_plan_repair_attempts',{})
  if attempts.get(key,0)>=4:
   state['stage']='art_repair_exhausted'
   if on_progress:on_progress()
   raise ValueError('Art repair planning exhausted')
  attempts[key]=attempts.get(key,0)+1
  if on_progress:on_progress()
  question='Replan ONLY this failed image. Simplify to one clear action and two concrete objects, avoiding the failed composition. Keep AP palette and choose a motif unlike the previous three issues. Do not repeat the failed subject. Preserve other accepted plans. Data:\n'+json.dumps(context,ensure_ascii=False)
  raw=model.ask(ROLE,question,tokens=500,schema=scene_schema(views,media))
  try:
   replacement=complete_plan(raw,index)
   if replacement['subject'].lower()==failure['failed_plan']['subject'].lower() or replacement['scene'].lower()==failure['failed_plan']['scene'].lower():raise ValueError('Change failed subject and composition')
   candidate=[replacement if p['story_index']==index else p for p in plans];validate_plans(candidate,lead)
   break
  except ValueError as exc:
   context['rejected_repair']={'proposal':raw,'reason':str(exc)}
   if attempt:raise
 state['art_plans']=candidate;state.setdefault('art_repair_history',[]).append({'failure':failure,'replacement':replacement})
 state.pop('pending_art_repair')
 queue=state.get('art_repair_queue',[])
 if queue:state['pending_art_repair']=queue.pop(0)
 state['stage']='needs_art_repair' if queue or state.get('pending_art_repair') else 'art_repaired'
 if on_progress:on_progress()
 return True
