"""English visual direction with explicit viewpoint/medium diversity gates."""
import json,re,shutil,time
from pathlib import Path
from newsletter_schemas import obj,string
VIEWS={'overhead':('overhead','top-down','top down','bird'), 'profile':('profile','side view','side-on'), 'wide':('wide','panoramic'), 'macro':('macro','close-up','close up'), 'cutaway':('cutaway','cross-section','cross section'), 'eye_level':('eye-level','eye level','eye_level')}
MEDIA={'ink':('ink',),'watercolor':('watercolor','watercolour'),'gouache':('gouache',),'linocut':('linocut',),'still_life':('still life','still-life','still_life'),'diagram':('diagram',)}
ROLE='''You are an English-language editorial art director, not a Korean copywriter. The supplied Korean articles are source data. Interpret them, but write every prompt, subject and approach in ENGLISH ONLY, never Korean. All images are original conceptual editorial illustrations, not actual products/screens, official photos, certifications or logos. Choose concrete visible objects and actions, meaningful for the article. Keep AP ivory/navy/sage/brass accents, varying ratios. Avoid miniature architecture, paper cutouts, centered hubs, generic abstract AI, text and logos. Choose style and viewpoint by meaning, not a fixed per-story sequence. The cover must differ from the lead article in subject framing AND viewpoint. Select at least4 viewpoints and3 media across6 images. Include the chosen medium and viewpoint explicitly in each English prompt.'''
SCHEMA=obj({'plans':{'type':'array','minItems':6,'maxItems':6,'items':obj({'story_index':{'type':'integer','minimum':0,'maximum':5},'prompt':string(650),'subject':string(120),'approach':string(100),'viewpoint':{'type':'string','enum':list(VIEWS)},'medium':{'type':'string','enum':list(MEDIA)}})}})
def validate_plans(plans,lead):
 if not isinstance(plans,list) or len(plans)!=6 or any(not isinstance(p,dict) or type(p.get('story_index')) is not int for p in plans) or {p['story_index'] for p in plans}!=set(range(6)):raise ValueError('Exactly6 distinct story_index values0..5 required')
 for p in plans:
  for key,limit in (('prompt',650),('subject',120),('approach',100)):
   value=p.get(key)
   if not isinstance(value,str) or not 1<=len(value)<=limit or re.search('[가-힣\u4e00-\u9fff\u3040-\u30ff]',value) or len(re.findall('[A-Za-z]',value))<5:raise ValueError('Write '+key+' in English, within its length limit')
  if p.get('viewpoint') not in VIEWS or p.get('medium') not in MEDIA:raise ValueError('Choose permitted viewpoint and medium')
  prompt=p['prompt'].lower()
  if not any(re.search(r'\b'+re.escape(word)+r'\b',prompt) for word in VIEWS[p['viewpoint']]) or not any(re.search(r'\b'+re.escape(word)+r'\b',prompt) for word in MEDIA[p['medium']]):raise ValueError('Prompt must explicitly describe its selected viewpoint and medium')
 if len({p['viewpoint'] for p in plans})<4 or len({p['medium'] for p in plans})<3:raise ValueError('Need at least4 viewpoints and3 media, selected by content')
 subjects=[' '.join(re.findall('[a-z0-9]+',p['subject'].lower())) for p in plans]
 if len(set(subjects))!=6:raise ValueError('Distinct concrete subject/action descriptions required')
 lookup={p['story_index']:p for p in plans}
 if lookup[5]['viewpoint']==lookup[lead]['viewpoint']:raise ValueError('Cover viewpoint must differ from lead article')
 return True

def plan_art(model,stories,lead):
 facts=[{k:s[k] for k in ('title','summary','fact')} for s in stories]
 question='Plan6 illustrations. story_index0..4 match the5 articles;5 is the cover of lead_index. Use concrete visible subjects/actions, not terms such as API transformation or AI model execution. No product screens or certificate imagery. Return the exact JSON schema. Article data:\n'+json.dumps({'lead_index':lead,'stories':facts},ensure_ascii=False)
 error=None;previous=None
 for attempt in range(2):
  result=model.ask(ROLE,question+('\nCorrect this rejected plan, preserving only valid content: '+json.dumps({'error':error,'previous_plan':previous},ensure_ascii=False) if error else ''),tokens=2200,schema=SCHEMA)
  plans=result.get('plans')
  try:validate_plans(plans,lead);return plans
  except ValueError as exc:
   error=str(exc);previous=plans
   if attempt:raise

def reset_invalid_saved_art(root,folder,asset_day,state):
 if not state.get('art_plans'):return False
 try:
  lead=state.get('editorial',{}).get('lead_index',state.get('fixed_lead'))
  validate_plans(state['art_plans'],lead);return False
 except (ValueError,KeyError) as exc:reason=str(exc)
 if not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:-test-(?:\d+|local))?',asset_day):raise ValueError('Unsafe art identity')
 root=Path(root);folder=Path(folder);archive=folder/'rejected-art'/str(time.time_ns());archive.mkdir(parents=True)
 moved=[]
 names=[asset_day+f'-story-{i}.png' for i in range(1,6)]+[asset_day+'-hero-original.png',asset_day+'-hero.png',asset_day+'-hero.gif']
 for name in names:
  path=root/'img/newsletter'/name
  if path.is_file() and not path.is_symlink():shutil.move(str(path),str(archive/path.name));moved.append(path.name)
 state.setdefault('art_plan_history',[]).append({'reason':reason,'plans':state.pop('art_plans'),'scores':state.pop('image_subject_scores',{}),'archived_images':moved})
 state.pop('quality',None);state['stage']='needs_art_replan'
 return True
