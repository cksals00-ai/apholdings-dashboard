"""Source-blind assertion inventory; disagreement/omission never grants approval."""
import hashlib,json,re
from concurrent.futures import ThreadPoolExecutor
import newsletter_schemas as s
from newsletter_review_spans import request_for
FIELDS=('title','summary','fact','insight','action')
REVISION='source-blind-complete-constituents-v18'
ROLES=('Independent complete factual-content reviewer A. ','Independent complete factual-content reviewer B. ')
# The legacy internal label denotes ALL certified nonfactual editorial content.
# Only explicit model wire labels map here; uncertainty is never inferred away.
WIRE_KINDS={'no_factual_premise':'pure_proposal','factual_premise_present':'asserted_or_mixed','uncertain':'uncertain'}
INTERNAL_KINDS={v:k for k,v in WIRE_KINDS.items()}
REASON_LIMIT=200
RULES="""Determine whether/hypothetical, negation and reporting scopes before selecting content. Exhaustively inventory BOTH outer asserted facts AND embedded asserted/presupposed facts at EVERY depth of the Korean sentence. Neither layer may replace or exclude the other. NEVER decide from the main speech act or a checking/recommendation verb alone. A factually modified definite object retains its presupposed existence/properties outside whether/hypothetical scope even when the main action is proposed, investigated or checked. Output factual_premise_present whenever any such factual premise requires support. Output no_factual_premise only when no asserted/presupposed factual content remains after scope resolution, such as a genuinely nonfactual proposal or open inquiry. Use uncertain only if factual scope cannot be determined; uncertainty blocks approval. 진위를 묻는 절과 사실 수식어가 붙은 특정 대상을 구분한다. 확인·검토 주절만 보고 판정하지 않으며, 의문·가정의 범위 밖에 있는 특정 대상의 수식절과 전제는 사실 근거를 요구한다.
A whether-question does not assert its answer; a hypothetical antecedent does not assert that its event happened. However, a definite noun phrase, factual relative clause or existing report can presuppose facts even when the main verb is a checking instruction or the main clause is conditional. Reports assert the report's existence and attributed content, not necessarily the truth of that content. Preserve negation, attribution and conditional scope. When a report/explanation is presented as an actual event outside a hypothetical or whether-question, its speaker/source, entire reported proposition AND completed reporting predicate form the factual premise together. The asserted reporting act is not metadata or an excluded proposed action. Exclude only genuinely nonfactual recommended/checking main actions. If the reporting act itself is under a whether-question or hypothetical, do not assert that it occurred. 실제로 있었다고 서술한 설명·발표·보고는 귀속·내용뿐 아니라 그 보고 행위까지 사실 전제로 보존한다. 이를 제안된 행동이나 메타데이터로 제외하지 않는다.
Select maximal self-contained factual constituents including subject/domain, quantifiers, qualifications, negation and report attribution/content; exclude outside proposed main actions. For each premise select first_word_id and last_word_id directly from the displayed words list. These are provided word IDs, NOT character offsets or counts. Never generate or retype a quotation: the program copies the entire original words and intervening whitespace. Do not omit a domain, qualification, attribution or negation. For title/summary/fact identify the underlying factual headline/report content even when phrased as a noun phrase or infinitive; these fields cannot be exempted as nonfactual. Cover only the requested target once. First select kind and exact provided word anchors consistently. Only after that give one concise scope reason under200 characters without restating the format or hash. The reason is a short justification after the decision, not an interrupted analysis before it. No source material or preferred answers are supplied. Uncertainty blocks approval."""
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
  ids=list(range(len(row['words'])))
  range_schema=s.obj({'first_word_id':{'type':'integer','enum':ids},'last_word_id':{'type':'integer','enum':ids}})
  choices=[]
  # Encode the same invariants independently enforced by normalize below.
  # Decide before the length-constrained justification: grammar must never
  # terminate a partial analysis before choosing a label and factual range.
  for kind in WIRE_KINDS:
   if kind=='no_factual_premise' and row['field'] in ('title','summary','fact'):continue
   premises={'type':'array','maxItems':0 if kind=='no_factual_premise' else 8,'items':range_schema}
   if kind=='factual_premise_present':premises['minItems']=1
   choices.append(s.obj({'field':{'type':'string','enum':[row['field']]},'id':{'type':'integer','enum':[row['id']]},'kind':{'type':'string','enum':[kind]},'premises':premises,'reason':s.string(REASON_LIMIT)}))
  branches.append({'oneOf':choices})
 indexed={(r['field'],r['id']):r for r in rows}
 def normalize(raw,expected,request_hash):
  if not isinstance(raw,dict) or set(raw)!={'input_hash','sentences'} or raw['input_hash']!=request_hash or not isinstance(raw['sentences'],list):raise ValueError('Stale speech-act inventory')
  out={}
  for row in raw['sentences']:
   if not isinstance(row,dict) or set(row)!={'field','id','kind','premises','reason'} or not isinstance(row['field'],str) or type(row['id'])is not int:raise ValueError('Malformed speech-act inventory')
   key=(row['field'],row['id'])
   if key not in indexed or key in out or not isinstance(row['kind'],str) or row['kind'] not in WIRE_KINDS or not isinstance(row['reason'],str) or len(row['reason'].strip())<10 or len(row['reason'])>REASON_LIMIT or not isinstance(row['premises'],list) or len(row['premises'])>8:raise ValueError('Invalid speech-act coverage')
   kind=WIRE_KINDS[row['kind']]
   if kind=='uncertain':raise ValueError('Uncertain speech act')
   if kind=='pure_proposal' and (row['field'] in ('title','summary','fact') or row['premises']):raise ValueError('Invalid pure-proposal exemption')
   if kind=='asserted_or_mixed' and not row['premises']:raise ValueError('Asserted premise inventory missing')
   ranges=[]
   for part in row['premises']:
    if not isinstance(part,dict) or set(part)!={'first_word_id','last_word_id'}:raise ValueError('Invalid factual word anchors')
    begin,end=part['first_word_id'],part['last_word_id']
    if type(begin)is not int or type(end)is not int or not 0<=begin<=end<len(offsets[key]):raise ValueError('Invalid factual word anchors')
    pair=(begin,end)
    if pair in ranges:raise ValueError('Duplicate factual range')
    ranges.append(pair)
   canonical=[]
   for begin,end in sorted(ranges):
    if canonical and begin<=canonical[-1][1]:raise ValueError('Overlapping factual word ranges')
    if canonical and begin==canonical[-1][1]+1:canonical[-1]=(canonical[-1][0],end)
    else:canonical.append((begin,end))
   out[key]=(kind,tuple(canonical))
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
   futures=[pool.submit(model.ask,role+instruction,question,tokens=900,schema=schema) for role in roles]
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
 audit=model.ask('Independent source-blind assertion coverage auditor. '+RULES+' Check the proposed inventory against original full sentences, without trusting the two analysts. Reject any omitted factual premise or presupposition, lost negation/conditional scope, or pure proposal misclassified as an assertion. Report exact field and sentence ID for each issue. No source data is supplied; do not ask whether a publisher mentions the company.',json.dumps(audit_payload,ensure_ascii=False),tokens=1600,schema=audit_schema)
 if not isinstance(audit,dict) or set(audit)!={'input_hash','complete','issues'} or audit['input_hash']!=audit_hash or audit['complete'] is not True or audit['issues']!=[]:raise ValueError('Source-blind assertion coverage failed: '+str(audit))
 return {'revision':REVISION,'input_hash':payload['input_hash'],'facts':facts,'inventory':inventory,'independent_decisions':raw,'coverage_audit':audit}
