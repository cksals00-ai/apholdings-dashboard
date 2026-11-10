"""Source-blind assertion inventory; disagreement/omission never grants approval."""
import hashlib,json,re
import newsletter_schemas as s
from newsletter_review_spans import request_for
FIELDS=('title','summary','fact','insight','action')
REVISION='source-blind-speech-v2'
RULES="""Classify what the Korean draft ACTUALLY ASSERTS, without source material or truth checking. Pure proposals, hypotheticals, questions and checking instructions do not assert that their proposed outcome already happened. An asserted or presupposed fact inside advice still counts: '효능이 입증됐으므로 검토' asserts efficacy; '도입한다면 모든 학생에게 입증된 기능' presupposes universal efficacy. '국내에서 인정되는 과정인지 확인' asks a question, but '국내에서 인정되는 이 과정을 확인' presupposes recognition. '기회를 얻었다면 검토' is hypothetical; '얻은 기회를 활용' presupposes acquisition. Preserve negation, quotation attribution and conditional scope. Analyze whether the sentence affirms a proposition, asks whether it holds, makes a hypothetical, or reports that someone made a claim. A report can assert that the report exists while negating the reported outcome. In your reason, resolve these scopes before choosing kind. Select exact word-index ranges for EVERY asserted factual premise, never paraphrase. start/end are inclusive WORD IDs, never character offsets or text lengths. Keep the whole original sentence in mind; do not extract a hypothetical antecedent as a completed fact. If uncertain choose uncertain. Cover every sentence exactly once; factual title/summary/fact cannot be pure proposals. Do not infer a preferred answer."""
def classify(model,story):
 rows=[];offsets={}
 for field in FIELDS:
  for span in request_for(field,story[field],'source-blind')['spans']:
   matches=list(re.finditer(r'\S+',span['text']));offsets[(field,span['id'])]=matches
   words=[{'id':i,'text':m.group()} for i,m in enumerate(matches)]
   rows.append({'field':field,'id':span['id'],'text':span['text'],'words':words})
 payload={'revision':REVISION,'sentences':rows}
 payload['input_hash']=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 branches=[]
 for row in rows:
  ids=list(range(len(row['words'])))
  range_schema=s.obj({'start':{'type':'integer','enum':ids},'end':{'type':'integer','enum':ids}})
  branches.append(s.obj({'reason':s.string(350),'field':{'type':'string','enum':[row['field']]},'id':{'type':'integer','enum':[row['id']]},'kind':{'type':'string','enum':['pure_proposal','asserted_or_mixed','uncertain']},'premises':{'type':'array','maxItems':8,'items':range_schema}}))
 item={'anyOf':branches}
 schema=s.obj({'input_hash':{'type':'string','enum':[payload['input_hash']]},'sentences':{'type':'array','minItems':len(rows),'maxItems':len(rows),'items':item}})
 indexed={(r['field'],r['id']):r for r in rows}
 def normalize(raw):
  if not isinstance(raw,dict) or set(raw)!={'input_hash','sentences'} or raw['input_hash']!=payload['input_hash'] or not isinstance(raw['sentences'],list):raise ValueError('Stale speech-act inventory')
  out={}
  for row in raw['sentences']:
   if not isinstance(row,dict) or set(row)!={'field','id','kind','premises','reason'} or not isinstance(row['field'],str) or type(row['id'])is not int:raise ValueError('Malformed speech-act inventory')
   key=(row['field'],row['id'])
   if key not in indexed or key in out or row['kind'] not in ('pure_proposal','asserted_or_mixed','uncertain') or not isinstance(row['reason'],str) or len(row['reason'].strip())<10 or not isinstance(row['premises'],list) or len(row['premises'])>8:raise ValueError('Invalid speech-act coverage')
   if row['kind']=='uncertain':raise ValueError('Uncertain speech act')
   if row['kind']=='pure_proposal' and (row['field'] in ('title','summary','fact') or row['premises']):raise ValueError('Invalid pure-proposal exemption')
   if row['kind']=='asserted_or_mixed' and not row['premises']:raise ValueError('Asserted premise inventory missing')
   ranges=[];words=indexed[key]['words']
   for part in row['premises']:
    if not isinstance(part,dict) or set(part)!={'start','end'} or any(type(part[k])is not int for k in part) or not 0<=part['start']<=part['end']<len(words):raise ValueError('Invalid factual word range')
    pair=(part['start'],part['end'])
    if pair in ranges:raise ValueError('Duplicate factual range')
    ranges.append(pair)
   out[key]=(row['kind'],tuple(sorted(ranges)))
  if set(out)!=set(indexed):raise ValueError('Speech-act coverage incomplete')
  return out
 raw=[];votes=[]
 for role in ('Independent speech-act analyst. ','Independent presupposition and scope analyst. '):
  answer=model.ask(role+RULES,json.dumps(payload,ensure_ascii=False),tokens=2600,schema=schema)
  raw.append(answer);votes.append(normalize(answer))
 if votes[0]!=votes[1]:raise ValueError('Independent speech-act disagreement')
 inventory=[];facts={f:[] for f in FIELDS}
 for key,(kind,ranges) in votes[0].items():
  row=indexed[key];parts=[]
  for begin,end in ranges:
   text=row['text'][offsets[key][begin].start():offsets[key][end].end()]
   part={'sentence_id':row['id'],'text':text,'sentence_context':row['text'],'word_start':begin,'word_end':end};parts.append(part);facts[key[0]].append(part)
  inventory.append({'field':key[0],'id':key[1],'kind':kind,'premises':parts})
 issue=s.obj({'field':{'type':'string','enum':list(FIELDS)},'id':{'type':'integer','minimum':0},'reason':s.string(350)})
 audit_payload={'draft':payload,'inventory':inventory}
 audit_hash=hashlib.sha256(json.dumps(audit_payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest();audit_payload['input_hash']=audit_hash
 audit_schema=s.obj({'input_hash':{'type':'string','enum':[audit_hash]},'complete':{'type':'boolean'},'issues':{'type':'array','maxItems':10,'items':issue}})
 audit=model.ask('Independent source-blind assertion coverage auditor. '+RULES+' Check the proposed inventory against original full sentences, without trusting the two analysts. Reject any omitted factual premise or presupposition, lost negation/conditional scope, or pure proposal misclassified as an assertion. Report exact field and sentence ID for each issue. No source data is supplied; do not ask whether a publisher mentions the company.',json.dumps(audit_payload,ensure_ascii=False),tokens=1600,schema=audit_schema)
 if not isinstance(audit,dict) or set(audit)!={'input_hash','complete','issues'} or audit['input_hash']!=audit_hash or audit['complete'] is not True or audit['issues']!=[]:raise ValueError('Source-blind assertion coverage failed: '+str(audit))
 return {'revision':REVISION,'input_hash':payload['input_hash'],'facts':facts,'inventory':inventory,'independent_decisions':raw,'coverage_audit':audit}
