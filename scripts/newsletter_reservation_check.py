"""Match only a live reservation/publication for the requested Korean edition."""
import argparse,json,re,sys
from datetime import datetime
from zoneinfo import ZoneInfo

def active_for_day(runs,day):
 for run in runs:
  if run.get('status') not in ('queued','in_progress'):continue
  match=re.fullmatch(r'AP News (today|\d{4}-\d{2}-\d{2}) (reservation|publication)',run.get('displayTitle',''))
  if not match:continue
  edition=match[1]
  if edition=='today':edition=datetime.fromisoformat(run['createdAt'].replace('Z','+00:00')).astimezone(ZoneInfo('Asia/Seoul')).date().isoformat()
  if edition==day:return True
 return False
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--date',required=True);args=parser.parse_args();print(str(active_for_day(json.load(sys.stdin),args.date)).lower())
