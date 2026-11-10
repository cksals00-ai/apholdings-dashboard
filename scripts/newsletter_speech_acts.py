"""Source-blind assertion inventory; disagreement/omission never grants approval."""
import hashlib,json,re
import newsletter_schemas as s
from newsletter_review_spans import request_for
FIELDS=('title','summary','fact','insight','action')
REVISION='source-blind-focused-verbatim-v6'
# The legacy internal label denotes ALL certified nonfactual editorial content.
# Only explicit model wire labels map here; uncertainty is never inferred away.
WIRE_KINDS={'no_factual_premise':'pure_proposal','factual_premise_present':'asserted_or_mixed','uncertain':'uncertain'}
INTERNAL_KINDS={v:k for k,v in WIRE_KINDS.items()}
REASON_LIMIT=200
RULES="""Inventory factual premises ANYWHERE in each Korean sentence. Do NOT classify only the main speech act. Output factual_premise_present if ANY assertion or presupposition needs factual support, even inside a proposal, question or conditional. Output no_factual_premise when there is NO asserted/presupposed fact: this category includes pure proposals, hypotheticals, questions and checking instructions. These are not uncertain just because they are not assertions. Use uncertain only when you cannot determine factual scope; uncertainty blocks approval.
A whether-question does not assert its answer; a hypothetical antecedent does not assert that its event happened. However, a definite noun phrase, factual relative clause or existing report can presuppose facts even when the main verb is a checking instruction or the main clause is conditional. '국내에서 인정되는 과정인지 확인' asks whether recognition holds; '국내에서 인정되는 이 과정을 확인' presupposes recognition. '기회를 얻었다면 검토' does not assert acquisition; '얻은 기회를 활용' presupposes acquisition. '효능이 입증됐으므로 검토' asserts efficacy; '도입한다면 모든 학생에게 입증된 기능' presupposes universal efficacy. Reports assert the report's existence and attributed content, not necessarily the truth of that content. Preserve negation, attribution and conditional scope.
Select maximal self-contained factual constituents, including their subject/domain, quantifiers, qualifications, negation and report attribution/content. Never return a bare predicate that drops these parts, or a bare checking verb/report noun that omits reported content. Exclude outside proposed main actions, but retain original full-sentence context. Quote each factual constituent verbatim from the original sentence as text. Copy the complete factual phrase including its subject/domain and qualifiers. Preserve original particles and punctuation where present. A uniquely located noun phrase that ends before a Korean grammatical case particle is conservatively extended to the original whole word; lexical or negative endings are never guessed. Never calculate numeric offsets, translate, paraphrase, omit interior words, or change whitespace. The program maps unique literal quotations to exact WORD IDs; ambiguous quotations block approval. Cover each sentence exactly once. title/summary/fact cannot have no_factual_premise. First give one concise scope reason under200 characters, without repeating/translating the sentence; then choose kind and literal quotations. No source material or preferred answers are supplied."""
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
  range_schema=s.obj({'text':s.string(2000)})
  branches.append(s.obj({'reason':s.string(REASON_LIMIT),'field':{'type':'string','enum':[row['field']]},'id':{'type':'integer','enum':[row['id']]},'kind':{'type':'string','enum':list(WIRE_KINDS)},'premises':{'type':'array','maxItems':8,'items':range_schema}}))
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
    if not isinstance(part,dict) or set(part)!={'text'} or not isinstance(part['text'],str) or not part['text']:raise ValueError('Invalid factual quotation')
    sentence=indexed[key]['text'];quote=part['text']
    positions=[m.start() for m in re.finditer('(?='+re.escape(quote)+')',sentence)]
    if len(positions)!=1:raise ValueError('Factual quotation missing or ambiguous')
    begin=positions[0];end=begin+len(quote)
    matches=offsets[key]
    starts={m.start():i for i,m in enumerate(matches)};ends={m.end():i for i,m in enumerate(matches)}
    if begin not in starts:raise ValueError('Factual quotation cuts a word')
    if end not in ends:
     # Only a grammatical noun-case suffix may be restored. Never complete a
     # lexical/negative predicate or guess a missing factual constituent.
     ending=next((m for m in matches if m.start()<end<m.end()),None)
     suffix=sentence[end:ending.end()] if ending else ''
     if not re.fullmatch(r'(?:(?:을|를|이|가|은|는|도|만|에|에서|에게|으로|로|와|과|의|까지|부터|처럼|보다|조차|마저|께|께서)[.!?,;:]?|[.!?,;:])',suffix):raise ValueError('Factual quotation cuts a word')
     end=ending.end()
    pair=(starts[begin],ends[end])
    if pair in ranges:raise ValueError('Duplicate factual range')
    ranges.append(pair)
   out[key]=(kind,tuple(sorted(ranges)))
  if set(out)!=expected:raise ValueError('Speech-act coverage incomplete')
  return out
 raw=[];votes=[]
 for role in ('Independent speech-act analyst. ','Independent presupposition and scope analyst. '):
  pass_raw=[];pass_votes={}
  for row,branch in zip(rows,branches):
   key=(row['field'],row['id'])
   focused={**payload,'draft_hash':payload['input_hash'],'target':{'field':key[0],'id':key[1]}}
   focused.pop('input_hash')
   focused['input_hash']=hashlib.sha256(json.dumps(focused,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
   schema=s.obj({'input_hash':{'type':'string','enum':[focused['input_hash']]},'sentences':{'type':'array','minItems':1,'maxItems':1,'items':{'anyOf':[branch]}}})
   answer=model.ask(role+RULES+' Assess ONLY the target sentence. Other original sentences supply linguistic context, never another reviewer answer. Return exactly one decision for target, including ALL of its factual qualifiers and factual constituents.',json.dumps(focused,ensure_ascii=False),tokens=700,schema=schema)
   pass_raw.append(answer);pass_votes.update(normalize(answer,{key},focused['input_hash']))
  raw.append(pass_raw);votes.append(pass_votes)
 if votes[0]!=votes[1]:raise ValueError('Independent speech-act disagreement')
 inventory=[];facts={f:[] for f in FIELDS}
 for key,(kind,ranges) in votes[0].items():
  row=indexed[key];parts=[]
  for begin,end in ranges:
   text=row['text'][offsets[key][begin].start():offsets[key][end].end()]
   part={'sentence_id':row['id'],'text':text,'sentence_context':row['text'],'word_start':begin,'word_end':end};parts.append(part);facts[key[0]].append(part)
  inventory.append({'field':key[0],'id':key[1],'kind':kind,'premises':parts})
 issue=s.obj({'field':{'type':'string','enum':list(FIELDS)},'id':{'type':'integer','minimum':0},'reason':s.string(350)})
 audit_payload={'draft':payload,'inventory':[{**r,'kind':INTERNAL_KINDS[r['kind']]} for r in inventory]}
 audit_hash=hashlib.sha256(json.dumps(audit_payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest();audit_payload['input_hash']=audit_hash
 audit_schema=s.obj({'input_hash':{'type':'string','enum':[audit_hash]},'complete':{'type':'boolean'},'issues':{'type':'array','maxItems':10,'items':issue}})
 audit=model.ask('Independent source-blind assertion coverage auditor. '+RULES+' Check the proposed inventory against original full sentences, without trusting the two analysts. Reject any omitted factual premise or presupposition, lost negation/conditional scope, or pure proposal misclassified as an assertion. Report exact field and sentence ID for each issue. No source data is supplied; do not ask whether a publisher mentions the company.',json.dumps(audit_payload,ensure_ascii=False),tokens=1600,schema=audit_schema)
 if not isinstance(audit,dict) or set(audit)!={'input_hash','complete','issues'} or audit['input_hash']!=audit_hash or audit['complete'] is not True or audit['issues']!=[]:raise ValueError('Source-blind assertion coverage failed: '+str(audit))
 return {'revision':REVISION,'input_hash':payload['input_hash'],'facts':facts,'inventory':inventory,'independent_decisions':raw,'coverage_audit':audit}
