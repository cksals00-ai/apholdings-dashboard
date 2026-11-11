"""Source-blind assertion inventory; disagreement/omission never grants approval."""
import hashlib,json,re
from concurrent.futures import ThreadPoolExecutor
import newsletter_schemas as s
from newsletter_review_spans import request_for
FIELDS=('title','summary','fact','insight','action')
REVISION='source-blind-world-commitment-v27'
REASONING_EFFORT='scope-plan'
AUDIT_MODE='instruct-only'
ROLES=('Independent author-commitment reviewer A. ','Independent author-commitment reviewer B. ')
# The legacy internal label denotes ALL certified nonfactual editorial content.
# Only explicit model wire labels map here; uncertainty is never inferred away.
WIRE_KINDS={'no_actual_world_claim':'pure_proposal','actual_world_claim_present':'asserted_or_mixed','uncertain':'uncertain'}
INTERNAL_KINDS={v:k for k,v in WIRE_KINDS.items()}
REASON_LIMIT=200
SEMANTIC_RULES="""Identify propositions the author commits to as true about the actual world, including assertions and projected presuppositions. Commitments can concern past, present, future, capabilities, general relations, quantities or attributed statements. Headlines and nominal descriptions can express implicit propositions; an overt predicate is not required.
Resolve each proposition's operator scope. A proposition merely entertained in a question, hypothesis, imagined scenario or recommendation is not thereby asserted as actual. Generic entities, concepts and contemplated activities are not claims merely because they are mentioned. A logical assumption inside a hypothetical is not the same as an actual-world commitment.
Presuppositions may project through questions or conditions: retain them only when the author commits to the actual property or event. Conversely, conditional wording can assert a real causal, efficacy or general relationship; it is not an automatic exemption. An attributed report commits to the reporting occurrence and what was attributed without automatically endorsing the reported proposition as true.
Preserve every original word expressing the actual commitment, including arguments, attribution, qualifications, quantifiers and negation. Exclude words belonging solely to uncommitted propositions or proposed actions. Field purpose supplies context, never automatic exemption: title/summary/fact report news; insight/action present AP interpretations or practical next steps, which may themselves contain claims. If commitment or scope cannot be determined, mark uncertainty; uncertainty blocks approval. The news-report fields cannot be entirely uncommitted.
판단 대상은 필자가 실제 세계에서 참이라고 주장하거나 전제하는 명제다. 질문·가정 속에서 임시로 상정한 내용이나 대상·개념의 단순 언급을 실제 사실 주장과 혼동하지 않는다. 의문·조건을 통과해 실제로 유지되는 전제는 보존하고, 조건부 문장이라도 실제 인과·효능·일반 관계를 주장하면 검증 대상으로 남긴다. 제안이라는 필드 이름만으로 사실 주장을 면제하지 않는다.
"""
WORD_OUTPUT_RULES="""Mark EVERY displayed word ID exactly once: claim when the whole original word expresses an actual-world commitment identified above, not_claim when it belongs only to uncommitted material, uncertain when its status cannot be determined. First complete your separate analysis of the sole target, then choose global kind actual_world_claim_present, no_actual_world_claim or uncertain. Global no_actual_world_claim requires every word not_claim; actual_world_claim_present requires actual claim words. Return the global kind before the full compatible map and one concise justification under200 characters. Do not retype quotations: the program copies original words and whitespace. No source data or preferred answers are supplied. Uncertainty blocks approval."""
RULES=SEMANTIC_RULES+WORD_OUTPUT_RULES
def focused_request(payload,row):
 # Plain original context has no competing row lists or nested request hashes.
 # Both target and full original draft participate in the one root hash.
 request={'revision':REVISION,'sentences':[row],'context':payload['draft']}
 request['input_hash']=hashlib.sha256(json.dumps(request,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 return request
def classify(model,story):
 rows=[];offsets={}
 for field in FIELDS:
  for span in request_for(field,story[field],'source-blind')['spans']:
   matches=list(re.finditer(r'\S+',span['text']));offsets[(field,span['id'])]=matches
   words=[{'id':i,'text':m.group()} for i,m in enumerate(matches)]
   rows.append({'field':field,'id':span['id'],'text':span['text'],'words':words})
 payload={'revision':REVISION,'draft':{field:story[field] for field in FIELDS},'sentences':rows}
 payload['input_hash']=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 branches=[]
 for row in rows:
  choices=[]
  for kind in WIRE_KINDS:
   if kind=='no_actual_world_claim' and row['field'] in ('title','summary','fact'):continue
   labels=['not_claim'] if kind=='no_actual_world_claim' else ['claim','not_claim','uncertain']
   scope=s.obj({str(w['id']):{'type':'string','enum':labels} for w in row['words']})
   choices.append(s.obj({'field':{'type':'string','enum':[row['field']]},'id':{'type':'integer','enum':[row['id']]},'kind':{'type':'string','enum':[kind]},'word_scope':scope,'reason':s.string(REASON_LIMIT)}))
  branches.append({'oneOf':choices})
 indexed={(r['field'],r['id']):r for r in rows}
 def normalize(raw,expected,request_hash):
  if not isinstance(raw,dict) or set(raw)!={'input_hash','sentences'} or raw['input_hash']!=request_hash or not isinstance(raw['sentences'],list):raise ValueError('Stale speech-act inventory')
  out={}
  for row in raw['sentences']:
   if not isinstance(row,dict) or set(row)!={'field','id','kind','word_scope','reason'} or not isinstance(row['field'],str) or type(row['id'])is not int:raise ValueError('Malformed speech-act inventory')
   key=(row['field'],row['id'])
   if key not in indexed or key in out or not isinstance(row['reason'],str) or len(row['reason'].strip())<10 or len(row['reason'])>REASON_LIMIT:raise ValueError('Invalid speech-act coverage')
   if type(row['kind'])is not str or row['kind'] not in WIRE_KINDS:raise ValueError('Invalid global speech act')
   kind=WIRE_KINDS[row['kind']]
   if kind=='uncertain':raise ValueError('Uncertain speech act')
   scope=row['word_scope'];ids={str(w['id']) for w in indexed[key]['words']}
   if not isinstance(scope,dict) or set(scope)!=ids or any(type(v)is not str or v not in ('claim','not_claim','uncertain') for v in scope.values()):raise ValueError('Every original word ID needs exactly one valid scope label')
   if 'uncertain' in scope.values():raise ValueError('Uncertain speech act')
   factual=[i for i in range(len(ids)) if scope[str(i)]=='claim']
   if (kind=='pure_proposal' and factual) or (kind=='asserted_or_mixed' and not factual):raise ValueError('Global speech act contradicts complete word mask')
   if not factual and row['field'] in ('title','summary','fact'):raise ValueError('Invalid pure-proposal exemption')
   ranges=[]
   for i in factual:
    if ranges and i==ranges[-1][1]+1:ranges[-1]=(ranges[-1][0],i)
    else:ranges.append((i,i))
   out[key]=(kind,tuple(ranges))
  if set(out)!=expected:raise ValueError('Speech-act coverage incomplete')
  return out
 raw=[{'input_hash':payload['input_hash'],'sentences':[],'requests':[]} for _ in range(2)];votes=[{},{}]
 roles=ROLES
 # Each native reasoning call has one complete target, never a large output
 # inventory to repeatedly recount. Both analysts see identical full context
 # and no other analyst's answer. The fixed runtime schedules full requests.
 with ThreadPoolExecutor(max_workers=2) as pool:
  for row,branch in zip(rows,branches):
   key=(row['field'],row['id'])
   focused=focused_request(payload,row)
   schema=s.obj({'input_hash':{'type':'string','enum':[focused['input_hash']]},'sentences':{'type':'array','minItems':1,'maxItems':1,'items':{'anyOf':[branch]}}})
   instruction=RULES+' Return exactly the single target in sentences; context is the complete original draft for interpretation only, not additional output rows. Do not classify another context sentence or count its rows.'
   question=json.dumps(focused,ensure_ascii=False)
   futures=[pool.submit(model.ask,role+instruction,question,tokens=900,schema=schema,reasoning_effort=REASONING_EFFORT) for role in roles]
   decisions=[]
   for i,future in enumerate(futures):
    answer=future.result();decision=normalize(answer,{key},focused['input_hash']);decisions.append(decision)
    votes[i].update(decision);raw[i]['sentences'].extend(answer['sentences'])
    raw[i]['requests'].append({'field':key[0],'id':key[1],'input_hash':focused['input_hash']})
   if decisions[0]!=decisions[1]:raise ValueError('Independent speech-act disagreement')
 if votes[0]!=votes[1] or set(votes[0])!=set(indexed):raise ValueError('Independent speech-act coverage incomplete')
 inventory=[];facts={f:[] for f in FIELDS}
 for key,(kind,ranges) in votes[0].items():
  row=indexed[key];parts=[]
  for begin,end in ranges:
   text=row['text'][offsets[key][begin].start():offsets[key][end].end()]
   part={'sentence_id':row['id'],'text':text,'sentence_context':row['text'],'word_start':begin,'word_end':end};parts.append(part);facts[key[0]].append(part)
  inventory.append({'field':key[0],'id':key[1],'kind':kind,'premises':parts})
 issue=s.obj({'field':{'type':'string','enum':list(FIELDS)},'id':{'type':'integer','minimum':0},'reason':s.string(350)})
 audit_payload={'draft':{k:v for k,v in payload.items() if k!='input_hash'},'inventory':[{**r,'kind':INTERNAL_KINDS[r['kind']]} for r in inventory]}
 audit_hash=hashlib.sha256(json.dumps(audit_payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest();audit_payload['input_hash']=audit_hash
 audit_schema=s.obj({'input_hash':{'type':'string','enum':[audit_hash]},'complete':{'type':'boolean'},'issues':{'type':'array','maxItems':10,'items':issue}})
 audit=model.ask('Independent source-blind assertion coverage auditor. '+SEMANTIC_RULES+' Check the proposed inventory against original full sentences, without trusting the two analysts. Reject any omitted actual-world commitment or projected presupposition, lost negation/conditional scope, or uncommitted proposal misclassified as an actual-world claim. Report exact field and sentence ID for each issue. No source data is supplied; do not ask whether a publisher mentions the company.',json.dumps(audit_payload,ensure_ascii=False),tokens=1600,schema=audit_schema,reasoning_effort=AUDIT_MODE)
 if not isinstance(audit,dict) or set(audit)!={'input_hash','complete','issues'} or audit['input_hash']!=audit_hash or audit['complete'] is not True or audit['issues']!=[]:raise ValueError('Source-blind assertion coverage failed: '+str(audit))
 return {'revision':REVISION,'reasoning_effort':REASONING_EFFORT,'input_hash':payload['input_hash'],'facts':facts,'inventory':inventory,'independent_decisions':raw,'coverage_audit_mode':AUDIT_MODE,'coverage_audit':audit}
