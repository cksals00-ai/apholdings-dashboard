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
