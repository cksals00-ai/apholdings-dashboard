"""Select only already-supported official candidates before editorial work.
No networking, source allowlist mutation, content fabrication or publication.
"""
import argparse,json
from datetime import date,timedelta
from pathlib import Path
import newsletter_server as server

def select_candidates(candidates,day,previous):
 today=date.fromisoformat(day);seen=set(previous);selected=[];rejected=[]
 for candidate in candidates:
  try:
   url=server.official_url(candidate['url']);published=date.fromisoformat(candidate['published'])
   if not today-timedelta(days=7)<=published<=today:raise ValueError('outside_seven_days')
   if url in seen:raise ValueError('duplicate')
   seen.add(url);selected.append(candidate)
  except (KeyError,ValueError,TypeError) as exc:rejected.append({'url':candidate.get('url',''),'reason':str(exc)[:120]})
 selected.sort(key=lambda c:c['published'],reverse=True)
 return {'ready':len(selected)>=5,'selected':selected[:7],'rejected':rejected,'note':'Candidate URL/date eligibility only; original content must still be verified.'}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--date',required=True);parser.add_argument('--candidates',type=Path,required=True);args=parser.parse_args()
 previous=[s['url'] for p in server.builder.ISSUES.glob('*.json') for s in json.loads(p.read_text()).get('stories',[])]
 result=select_candidates(json.loads(args.candidates.read_text()),args.date,previous);print(json.dumps(result,ensure_ascii=False,indent=2))
 raise SystemExit(0 if result['ready'] else 2)
