"""Source-blind assertion inventory; disagreement/omission never grants approval."""
import hashlib,json,re
from concurrent.futures import ThreadPoolExecutor
import newsletter_schemas as s
from newsletter_review_spans import request_for
FIELDS=('title','summary','fact','insight','action')
REVISION='source-blind-exhaustive-word-scope-v20'
REASONING_EFFORT='medium'
ROLES=('Independent complete factual-content reviewer A. ','Independent complete factual-content reviewer B. ')
# The legacy internal label denotes ALL certified nonfactual editorial content.
# Only explicit model wire labels map here; uncertainty is never inferred away.
WIRE_KINDS={'no_factual_premise':'pure_proposal','factual_premise_present':'asserted_or_mixed','uncertain':'uncertain'}
INTERNAL_KINDS={v:k for k,v in WIRE_KINDS.items()}
REASON_LIMIT=200
RULES="""Determine whether/hypothetical, negation and reporting scopes before selecting content. Exhaustively inventory BOTH outer asserted facts AND embedded asserted/presupposed facts at EVERY depth of the Korean sentence. Neither layer may replace or exclude the other. NEVER decide from the main speech act or a checking/recommendation verb alone. A factually modified definite object retains its presupposed existence/properties outside whether/hypothetical scope even when the main action is proposed, investigated or checked. Factual support is required whenever any such factual premise remains. A sentence is entirely nonfactual only when no asserted/presupposed factual content remains after scope resolution, such as a genuinely nonfactual proposal or open inquiry. Use uncertain only if factual scope cannot be determined; uncertainty blocks approval. 진위를 묻는 절과 사실 수식어가 붙은 특정 대상을 구분한다. 확인·검토 주절만 보고 판정하지 않으며, 의문·가정의 범위 밖에 있는 특정 대상의 수식절과 전제는 사실 근거를 요구한다.
A whether-question does not assert its answer; a hypothetical antecedent does not assert that its event happened. However, a definite noun phrase, factual relative clause or existing report can presuppose facts even when the main verb is a checking instruction or the main clause is conditional. Reports assert the report's existence and attributed content, not necessarily the truth of that content. Preserve negation, attribution and conditional scope. When a report/explanation is presented as an actual event outside a hypothetical or whether-question, its speaker/source, entire reported proposition AND completed reporting predicate form the factual premise together. The asserted reporting act is not metadata or an excluded proposed action. Exclude only genuinely nonfactual recommended/checking main actions. If the reporting act itself is under a whether-question or hypothetical, do not assert that it occurred. 실제로 있었다고 서술한 설명·발표·보고는 귀속·내용뿐 아니라 그 보고 행위까지 사실 전제로 보존한다. 이를 제안된 행동이나 메타데이터로 제외하지 않는다.
Select maximal self-contained factual constituents including subject/domain, quantifiers, qualifications, negation and report attribution/content; exclude outside proposed main actions. Assign EVERY displayed word ID exactly one word_scope label: factual when that whole original word belongs to any asserted/presupposed factual constituent, nonfactual when outside all such constituents, uncertain only when its scope cannot be determined. Nested factual layers label the same word factual once; do not list overlapping ranges or retype quotations. The program derives contiguous factual runs from your exhaustive word map and copies exact original words. Do not omit a domain, qualification, attribution or negation. For title/summary/fact identify the underlying factual headline/report content even when phrased as a noun phrase or infinitive; these fields cannot be entirely nonfactual. Cover only the requested target once. Give all word labels before one concise scope reason under200 characters. The reason is a short justification after the decision, not an interrupted analysis before it. No source material or preferred answers are supplied. Uncertainty blocks approval."""
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
  scope=s.obj({str(w['id']):{'type':'string','enum':['factual','nonfactual','uncertain']} for w in row['words']})
  branches.append(s.obj({'field':{'type':'string','enum':[row['field']]},'id':{'type':'integer','enum':[row['id']]},'word_scope':scope,'reason':s.string(REASON_LIMIT)}))
 indexed={(r['field'],r['id']):r for r in rows}
 def normalize(raw,expected,request_hash):
  if not isinstance(raw,dict) or set(raw)!={'input_hash','sentences'} or raw['input_hash']!=request_hash or not isinstance(raw['sentences'],list):raise ValueError('Stale speech-act inventory')
  out={}
  for row in raw['sentences']:
   if not isinstance(row,dict) or set(row)!={'field','id','word_scope','reason'} or not isinstance(row['field'],str) or type(row['id'])is not int:raise ValueError('Malformed speech-act inventory')
   key=(row['field'],row['id'])
   if key not in indexed or key in out or not isinstance(row['reason'],str) or len(row['reason'].strip())<10 or len(row['reason'])>REASON_LIMIT:raise ValueError('Invalid speech-act coverage')
   scope=row['word_scope'];ids={str(w['id']) for w in indexed[key]['words']}
   if not isinstance(scope,dict) or set(scope)!=ids or any(type(v)is not str or v not in ('factual','nonfactual','uncertain') for v in scope.values()):raise ValueError('Every original word ID needs exactly one valid scope label')
   if 'uncertain' in scope.values():raise ValueError('Uncertain speech act')
   factual=[i for i in range(len(ids)) if scope[str(i)]=='factual']
   if not factual and row['field'] in ('title','summary','fact'):raise ValueError('Invalid pure-proposal exemption')
   ranges=[]
   for i in factual:
    if ranges and i==ranges[-1][1]+1:ranges[-1]=(ranges[-1][0],i)
    else:ranges.append((i,i))
   out[key]=('asserted_or_mixed' if factual else 'pure_proposal',tuple(ranges))
  if set(out)!=expected:raise ValueError('Speech-act coverage incomplete')
  return out
 raw=[{'input_hash':payload['input_hash'],'sentences':[],'requests':[]} for _ in range(2)];votes=[{},{}]
 roles=ROLES
 # Each native reasoning call has one complete target, never a large output
 # inventory to repeatedly recount. Both analysts see identical full context
 # and no other analyst's answer. Separate server slots batch their decoding.
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
 audit=model.ask('Independent source-blind assertion coverage auditor. '+RULES+' Check the proposed inventory against original full sentences, without trusting the two analysts. Reject any omitted factual premise or presupposition, lost negation/conditional scope, or pure proposal misclassified as an assertion. Report exact field and sentence ID for each issue. No source data is supplied; do not ask whether a publisher mentions the company.',json.dumps(audit_payload,ensure_ascii=False),tokens=1600,schema=audit_schema,reasoning_effort=REASONING_EFFORT)
 if not isinstance(audit,dict) or set(audit)!={'input_hash','complete','issues'} or audit['input_hash']!=audit_hash or audit['complete'] is not True or audit['issues']!=[]:raise ValueError('Source-blind assertion coverage failed: '+str(audit))
 return {'revision':REVISION,'reasoning_effort':REASONING_EFFORT,'input_hash':payload['input_hash'],'facts':facts,'inventory':inventory,'independent_decisions':raw,'coverage_audit':audit}
