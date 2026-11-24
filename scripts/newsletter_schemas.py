"""Local constrained-decoding shapes. They constrain syntax, never force a verdict."""
def string(limit=1000):return {'type':'string','maxLength':limit}
def obj(properties):return {'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}
REVIEW=obj({'supported':{'type':'boolean'},'unsupported_claims':{'type':'array','items':string(250)}})
NOVELTY=obj({'is_news':{'type':'boolean'},'is_duplicate':{'type':'boolean'},'novel_quote':string(700),'reason':string(300)})
DRAFT=obj({'title':string(90),'summary':string(160),'fact':string(700),'insight':string(400),'action':string(180),'evidence':{'type':'array','items':string(700),'minItems':1,'maxItems':3},'image_prompt':string(650),'image_subject':string(120),'visual_approach':string(100)})
EDITORIAL=obj({'lead_index':{'type':'integer','minimum':0,'maximum':4},'title':string(90),'intro':string(250),'takeaway':string(800),'hero_prompt':string(650),'hero_subject':string(120),'hero_approach':string(100)})
ART=obj({'plans':{'type':'array','minItems':6,'maxItems':6,'items':obj({'story_index':{'type':'integer','minimum':0,'maximum':5},'prompt':string(650),'subject':string(120),'approach':string(100)})}})

DRAFT_INDEXED=obj({**{k:v for k,v in DRAFT["properties"].items() if k!="evidence"},"evidence_ids":{"type":"array","items":{"type":"integer","minimum":0},"minItems":1,"maxItems":4}})

def indexed_draft(segment_count):
 if type(segment_count) is not int or segment_count<1:raise ValueError('Evidence segments required')
 return obj({**DRAFT_INDEXED['properties'],'evidence_ids':{'type':'array','items':{'type':'integer','minimum':0,'maximum':segment_count-1},'minItems':1,'maxItems':min(4,segment_count)}})


def source_novelty(segments):
 if not isinstance(segments,list) or not segments:raise ValueError('Original source segments required')
 texts=[part.get('text') if isinstance(part,dict) else None for part in segments]
 if any(not isinstance(text,str) or not 30<=len(text)<=800 for text in texts):raise ValueError('Unusable source novelty evidence')
 if any(type(part.get('id')) is not int for part in segments) or [part.get('id') for part in segments]!=list(range(len(segments))):raise ValueError('Source segment IDs must be contiguous')
 # Select an ID, then copy the literal text in code. Embedding publisher quotes
 # in enum strings triggers grammar conversion failures in pinned llama b5401.
 return obj({'is_news':{'type':'boolean'},'is_duplicate':{'type':'boolean'},'novel_segment_id':{'type':'integer','minimum':-1,'maximum':len(segments)-1},'reason':string(300)})



# No independent boolean can contradict the precise rejection findings.
STRONG_REVIEW=obj({'findings':{'type':'array','items':obj({
 'field':{'type':'string','enum':['title','summary','fact','insight','action']},
 'assertion':{'type':'string','minLength':2,'maxLength':1800},
 'factual_premise':{'type':'string','minLength':5,'maxLength':500},
 'source_mismatch':{'type':'string','minLength':10,'maxLength':600},
 'correction':{'type':'string','minLength':5,'maxLength':400}})}})
