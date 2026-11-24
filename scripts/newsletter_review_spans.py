"""Literal sentence IDs for reviewer transport, never semantic approval."""
import hashlib,json,re
REVISION='literal-draft-sentences-v1'
def request_for(field,text,source_hash):
 if field not in ('title','summary','fact','insight','action') or not isinstance(text,str) or not text.strip():raise ValueError('Invalid review input')
 # Keep conditional clauses together; split only at sentence punctuation followed
 # by whitespace. Every selected value remains a literal substring of the draft.
 parts=[p.strip() for p in re.split(r'(?<=[.!?。！？])\s+',text.strip()) if p.strip()]
 spans=[{'id':i,'text':p} for i,p in enumerate(parts)]
 data={'revision':REVISION,'field':field,'text':text,'source_hash':source_hash,'spans':spans}
 data['input_hash']=hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 return data

def schema_for(request):
 import newsletter_schemas as s
 item=s.obj({'id':{'type':'integer','enum':[x['id'] for x in request['spans']]},'status':{'type':'string','enum':['supported','editorial','unsupported','uncertain']},'source_ids':{'type':'array','maxItems':4,'items':{'type':'integer','minimum':0}},'reason':s.string(350)})
 return s.obj({'input_hash':{'type':'string','enum':[request['input_hash']]},'sentences':{'type':'array','minItems':len(request['spans']),'maxItems':len(request['spans']),'items':item}})

def resolve(raw,request):
 if not isinstance(raw,dict) or set(raw)!={'input_hash','sentences'} or raw['input_hash']!=request['input_hash'] or not isinstance(raw['sentences'],list):raise ValueError('Stale or malformed sentence review')
 rows=raw['sentences'];ids=[];premises=[];statuses=[]
 for row in rows:
  if not isinstance(row,dict) or set(row)!={'id','status','source_ids','reason'} or type(row['id'])is not int:raise ValueError('Invalid sentence decision')
  i=row['id'];status=row['status']
  if i<0 or i>=len(request['spans']) or i in ids or status not in ('supported','editorial','unsupported','uncertain'):raise ValueError('Invalid sentence ID or status')
  ids.append(i);statuses.append(status)
  if not isinstance(row['reason'],str) or len(row['reason'].strip())<10 or not isinstance(row['source_ids'],list):raise ValueError('Missing sentence rationale')
  if status=='editorial':
   if request['field'] in ('title','summary','fact') or row['source_ids']:raise ValueError('Invalid editorial exemption')
  else:premises.append({'claim':request['spans'][i]['text'],'status':status,'source_ids':row['source_ids'],'reason':row['reason']})
 if sorted(ids)!=list(range(len(request['spans']))):raise ValueError('Sentence coverage incomplete')
 verdict='unsupported' if 'unsupported' in statuses else 'uncertain' if 'uncertain' in statuses else 'supported' if 'supported' in statuses else 'editorial'
 return {'field':request['field'],'text':request['text'],'verdict':verdict,'premises':premises}
