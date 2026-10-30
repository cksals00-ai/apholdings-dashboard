"""English visual direction with explicit viewpoint/medium diversity gates."""
import json,re,shutil,time
from pathlib import Path
from newsletter_schemas import obj,string
VIEWS={'overhead':('overhead','top-down','top down','bird'), 'profile':('profile','side view','side-on'), 'wide':('wide','panoramic'), 'macro':('macro','close-up','close up'), 'cutaway':('cutaway','cross-section','cross section'), 'eye_level':('eye-level','eye level','eye_level')}
MEDIA={'ink':('ink',),'watercolor':('watercolor','watercolour'),'gouache':('gouache',),'linocut':('linocut',),'still_life':('still life','still-life','still_life'),'diagram':('diagram',)}
ROLE="""You are an English-language conceptual editorial art director. Plan ONE image at a time. Korean article facts are data; every output string must be English. Subject must be under12 words, naming only2-3 concrete objects. Scene must be under45 words. Do not print publisher names, labels or handwriting. Avoid centered glowing hubs, concentric circles and repeated hexagon clusters. First choose one allowed viewpoint and medium suitable for the content, then describe concrete visible objects and actions. Use original physical metaphors, not literal software or product screens. No brands, printed text, code, logos, certificates, patient treatment, holographic interfaces or generic futuristic cityscapes. For education news depict studying or practice, never clinical AI recommendations or professional credentials. The subject is a short description of visible objects, NOT the article title or abstract terms such as AI, API, model execution or development. The scene describes objects/actions only; code adds the chosen camera/medium and AP palette. Invent a content-appropriate scene; do not copy the article wording or prior subjects."""
def english(value,limit):return isinstance(value,str) and 1<=len(value)<=limit and not re.search('[가-힣\u4e00-\u9fff\u3040-\u30ff]',value) and len(re.findall('[A-Za-z]',value))>=5

def validate_scene(subject,scene):
 if not english(subject,120) or not english(scene,450) or len(re.findall(r'\b\w+\b',subject))>12:raise ValueError('Write the visible subject and physical scene in English only')
 if re.search(r'\b(?:AI|API|NVIDIA|Google|Gemini|AWS|execution|development|certification|cover|model)\b',subject,re.I):raise ValueError('Subject must name visible objects/actions, not article titles, brands or AI/API/model jargon')
 clean=re.sub(r'\b(?:no|without)\s+(?:(?:visible|printed|written|product|actual|real)\s+)*(?:text|logos?|screens?|interfaces?|code|certificates?)(?:\s+or\s+(?:text|logos?|screens?|interfaces?|code|certificates?))*','',scene,flags=re.I)
 if re.search(r'\b(?:labels?|labelled|labeled|handwritten|handwriting|publisher|hexagons?|hexagonal|concentric)\b|in the cent(?:er|re)|at the cent(?:er|re)|\bcentered\b',clean,re.I):raise ValueError('No printed publisher labels/handwriting or repeated centered hexagon hubs; use unmarked physical objects and asymmetric framing')
 if re.search(r'\b(?:text|logos?|screens?|interfaces?|screenshots?|code|flowcharts?|certificates?|patients?|diagnos\w*|treatments?|cityscapes?|holograph\w*)\b|(?:computer|digital) displays?',clean,re.I):raise ValueError('Use physical objects/metaphors; remove software screens, code, certificates, patient care, holograms and cityscapes')
 return True

def scene_schema(views,media):return obj({'viewpoint':{'type':'string','enum':views},'medium':{'type':'string','enum':media},'subject':string(120),'scene':string(450)})
def choices(plans,index,lead):
 seen_views={p['viewpoint'] for p in plans};seen_media={p['medium'] for p in plans};remaining=6-index
 views=[v for v in VIEWS if remaining!=max(0,4-len(seen_views)) or v not in seen_views]
 media=[m for m in MEDIA if remaining!=max(0,3-len(seen_media)) or m not in seen_media]
 if index==5:views=[v for v in views if v!=plans[lead]['viewpoint']]
 return views,media

def complete_plan(raw,index):
 if raw.get('viewpoint') not in VIEWS or raw.get('medium') not in MEDIA:raise ValueError('Select the allowed viewpoint and medium')
 validate_scene(raw.get('subject'),raw.get('scene'))
 medium=raw['medium'].replace('_',' ');view=raw['viewpoint'].replace('_',' ')
 prompt=f'{medium} editorial illustration, {view} view. '+raw['scene']+' Navy, ivory, sage and brass accents; no text or logos, not a product screenshot.'
 if len(prompt)>650:raise ValueError('Shorten the physical scene description')
 return {'story_index':index,'viewpoint':raw['viewpoint'],'medium':raw['medium'],'subject':raw['subject'],'scene':raw['scene'],'prompt':prompt,'approach':medium+' / '+view}

def subject_key(value):return ' '.join(re.findall('[a-z0-9]+',value.lower()))

def validate_plans(plans,lead):
 if not isinstance(plans,list) or len(plans)!=6 or any(not isinstance(p,dict) or type(p.get('story_index')) is not int for p in plans) or {p['story_index'] for p in plans}!=set(range(6)):raise ValueError('Exactly6 distinct story_index values0..5 required')
 for p in plans:
  validate_scene(p.get('subject'),p.get('scene'))
  for key,limit in (('prompt',650),('subject',120),('approach',100)):
   value=p.get(key)
   if not isinstance(value,str) or not 1<=len(value)<=limit or re.search('[가-힣\u4e00-\u9fff\u3040-\u30ff]',value) or len(re.findall('[A-Za-z]',value))<5:raise ValueError('Write '+key+' in English, within its length limit')
  if p.get('viewpoint') not in VIEWS or p.get('medium') not in MEDIA:raise ValueError('Choose permitted viewpoint and medium')
  prompt=p['prompt'].lower()
  if not any(re.search(r'\b'+re.escape(word)+r'\b',prompt) for word in VIEWS[p['viewpoint']]) or not any(re.search(r'\b'+re.escape(word)+r'\b',prompt) for word in MEDIA[p['medium']]):raise ValueError('Prompt must explicitly describe its selected viewpoint and medium')
 if len({p['viewpoint'] for p in plans})<4 or len({p['medium'] for p in plans})<3:raise ValueError('Need at least4 viewpoints and3 media, selected by content')
 subjects=[subject_key(p['subject']) for p in plans]
 if len(set(subjects))!=6:raise ValueError('Distinct concrete subject/action descriptions required')
 lookup={p['story_index']:p for p in plans}
 if lookup[5]['viewpoint']==lookup[lead]['viewpoint']:raise ValueError('Cover viewpoint must differ from lead article')
 return True

def plan_art(model,stories,lead,previous_plans=None,on_progress=None):
 facts=[{k:s[k] for k in ('title','summary','fact')} for s in stories]
 saved=list(previous_plans or []);plans=[]
 for index,p in enumerate(saved):
  try:
   if index>=6:raise ValueError('Too many partial plans')
   views,media=choices(plans,index,lead)
   if p.get('story_index')!=index or p.get('viewpoint') not in views or p.get('medium') not in media or complete_plan(p,index)!=p or subject_key(p['subject']) in {subject_key(prior['subject']) for prior in plans}:raise ValueError('Invalid saved partial art plan')
  except (ValueError,KeyError,TypeError):
   if on_progress:on_progress(list(plans))
   break
  plans.append(p)
 for index in range(len(plans),6):
  views,media=choices(plans,index,lead);error=None;previous=None
  context={'kind':'lead-news cover' if index==5 else 'article illustration','article':facts[lead if index==5 else index],'previous_subjects':[p['subject'] for p in plans]}
  if index==5:context['lead_article_plan']=plans[lead]
  for attempt in range(2):
   question='Choose from the schema options by the article meaning. Describe one physical scene, not interfaces or abstract titles. For a cover, use different objects/framing from its article. Data:\n'+json.dumps(context,ensure_ascii=False)
   if error:question+='\nCorrect this rejected proposal: '+json.dumps({'error':error,'proposal':previous},ensure_ascii=False)
   raw=model.ask(ROLE,question,tokens=500,schema=scene_schema(views,media))
   try:
    if raw.get('viewpoint') not in views or raw.get('medium') not in media:raise ValueError('Choose permitted camera/medium options')
    plan=complete_plan(raw,index)
    if subject_key(plan['subject']) in {subject_key(p['subject']) for p in plans}:raise ValueError('Choose a distinct concrete subject/action, especially for the cover')
    break
   except ValueError as exc:
    error=str(exc);previous=raw
    if attempt:raise
  plans.append(plan)
  if on_progress:on_progress(list(plans))
 validate_plans(plans,lead)
 return plans

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
