"""Bind accepted art to unchanged source facts, with resumable file moves."""
import copy,hashlib,json
from pathlib import Path
from newsletter_art_repair import record_failure

def identity(story):return hashlib.sha256(json.dumps([story.get(k) for k in ('url','summary','fact')],ensure_ascii=False).encode()).hexdigest()
def _save(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False));temp.replace(path)

def reconcile_art_bindings(root,folder,asset_day,state,before_stories,before_editorial):
 if not state.get('art_plans'):return False
 oldkeys=[identity(s) for s in before_stories];newkeys=[identity(s) for s in state['stories']]
 oldlead=before_editorial.get('lead_index');newlead=state['editorial']['lead_index']
 token=hashlib.sha256(json.dumps([oldkeys,newkeys,oldlead,newlead]).encode()).hexdigest()
 if token in state.get('art_binding_receipts',[]):return False
 if oldkeys==newkeys and oldlead==newlead:return False
 folder=Path(folder);images=Path(root)/'img/newsletter';work=folder/'art-bindings'/token;journal=work/'transaction.json'
 if journal.exists():transaction=json.loads(journal.read_text())
 else:
  plans={p['story_index']:p for p in state['art_plans']};used=set();mapping={}
  for index,key in enumerate(newkeys):
   match=next((i for i,k in enumerate(oldkeys) if k==key and i not in used),None)
   if match is not None:mapping[index]=match;used.add(match)
  unmatched=[i for i in range(5) if i not in used];changed=[i for i in range(5) if i not in mapping]
  for i,j in zip(changed,unmatched):mapping[i]=j
  updated=[]
  for i in range(5):p=copy.deepcopy(plans[mapping[i]]);p['story_index']=i;updated.append(p)
  updated.append(plans[5]);hero_changed=oldlead is None or oldkeys[oldlead]!=newkeys[newlead]
  queued=([5] if hero_changed else [])+changed
  moves=[]
  for i in range(5):
   destination=next((j for j,k in mapping.items() if k==i and j not in changed),None)
   name=f'{asset_day}-story-{i+1}.png'
   moves.append({'source':name,'destination':f'{asset_day}-story-{destination+1}.png' if destination is not None else None})
  if hero_changed:
   moves.extend({'source':f'{asset_day}-hero{suffix}','destination':None} for suffix in ('-original.png','.png','.gif'))
  # Remap already-pending failures to their unchanged semantic story, if present.
  existing=[state.get('pending_art_repair')]+state.get('art_repair_queue',[])
  for failure in existing:
   if not failure:continue
   oldindex=failure['story_index']
   newindex=5 if oldindex==5 else next((j for j,k in mapping.items() if k==oldindex and j not in changed),None)
   if newindex is not None and newindex not in queued:queued.append(newindex)
  transaction={'phase':'stage','plans':updated,'queued':queued,'moves':moves};_save(journal,transaction)
 work.mkdir(parents=True,exist_ok=True)
 if transaction['phase']=='stage':
  for move in transaction['moves']:
   source=images/move['source'];staged=work/move['source']
   if not staged.exists() and source.is_file():source.replace(staged)
  transaction['phase']='apply';_save(journal,transaction)
 for move in transaction['moves']:
  staged=work/move['source']
  if move['destination'] and staged.exists():staged.replace(images/move['destination'])
 state['art_plans']=transaction['plans'];queue=[]
 for index in transaction['queued']:
  name=f'{asset_day}-hero-original.png' if index==5 else f'{asset_day}-story-{index+1}.png'
  record_failure(state,index,name,'source facts or lead binding changed',{})
  queue.append(state.pop('pending_art_repair'))
 if queue:state['pending_art_repair']=queue[0];state['art_repair_queue']=queue[1:]
 state.setdefault('art_binding_receipts',[]).append(token)
 return True
