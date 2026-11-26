"""Labelled historical regressions; never a new issue or current-date source."""
import copy,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from newsletter_cpu import REVIEW_REV,PROMPT_CACHE_REVISION
from newsletter_atomic_review import REVISION as ATOMIC_REVISION
FIXTURE=Path(__file__).with_name('fixtures')/'news-editorial-controls-20261103.json'

def inputs():
 rows=json.loads(FIXTURE.read_text())
 if len(rows)!=5 or len({r['label'] for r in rows})!=5:raise ValueError('Five distinct frozen controls required')
 for row in rows:
  if row.get('historical_only') is not True or row['origin_date']!='2026-11-03':raise ValueError('Historical provenance required')
  if hashlib.sha256(row['source']['text'].encode()).hexdigest()!=row['source']['body_sha256']:raise ValueError('Frozen source hash changed')
  row['input_hash']=hashlib.sha256(json.dumps(row,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 return rows

def specific_rejection(label,review):
 fields=review.get('fields',[])
 expected='insight' if label=='obtained_opportunity' else 'action' if label=='all_students' else 'fact'
 targets={'obtained_opportunity':('기회를 얻었습니다',('opportun','outcome','기회','AP')),'false_efficacy':('학습 효과를 높인다는 인과관계를 입증',('causal','efficacy','learning','인과','학습','효과')),'all_students':('모든 학생에게 입증',('universal','all students','all learners','모든','학생','입증'))}
 target,terms=targets[label]
 return any(d['field']==expected and d['verdict']=='unsupported' and any(p['status']=='unsupported' and target in p['claim'] and any(t.casefold() in p['reason'].casefold() for t in terms) for p in d['premises']) for d in fields)

def receipt_valid(row,r):
 from newsletter_copy_repair import REVISION
 if any(r.get(k)!=v for k,v in {'input_hash':row['input_hash'],'source_hash':row['source']['body_sha256'],'model_revision':REVIEW_REV,'cache_revision':PROMPT_CACHE_REVISION,'review_revision':REVISION,'atomic_revision':ATOMIC_REVISION,'expected_supported':row['expected_supported']}.items()):return False
 review=r.get('review',{})
 return (review.get('supported') is True and review.get('findings')==[]) if row['expected_supported'] else specific_rejection(row['label'],review)

def controls_valid(state):
 return all(receipt_valid(row,state.get('frozen_control_receipts',{}).get(row['label'],{})) for row in inputs())

def verify_controls(model,state,save):
 from newsletter_copy_repair import verify,REVISION
 from newsletter_repair_rehearsal import identity
 identity(state)
 if controls_valid(state):return
 for row in inputs():
  if receipt_valid(row,state.get('frozen_control_receipts',{}).get(row['label'],{})):continue
  candidate=copy.deepcopy(row['draft']);review={}
  try:
   verify(model,candidate,row['source'],[],[])
   review=candidate['strong_review']['review']
   if not row['expected_supported']:raise ValueError('Frozen false claim accepted: '+row['label'])
  except ValueError as exc:
   review=getattr(exc,'review',{})
   if row['expected_supported'] or not specific_rejection(row['label'],review):raise ValueError('Frozen control failed: '+row['label']+' | '+str(exc)) from exc
  state.setdefault('frozen_control_receipts',{})[row['label']]={'input_hash':row['input_hash'],'source_hash':row['source']['body_sha256'],'model_revision':REVIEW_REV,'cache_revision':PROMPT_CACHE_REVISION,'review_revision':REVISION,'atomic_revision':ATOMIC_REVISION,'expected_supported':row['expected_supported'],'historical_only':True,'review':review,'checked_at':datetime.now(timezone.utc).isoformat()};save()
