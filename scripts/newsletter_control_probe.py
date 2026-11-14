"""Run only historical semantic regressions on public local CPU weights."""
import argparse,json,os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from newsletter_cpu import TextModel
from newsletter_frozen_controls import verify_controls,controls_valid

def run(runtime,folder,scope_only=False,historical_only=False):
 if scope_only and historical_only:raise ValueError('Conflicting control modes')
 folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
 run_id=os.environ.get('GITHUB_RUN_ID','')
 if not run_id.isdigit():raise ValueError('Isolated server probe run required')
 day=datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat()
 state={'date':day,'mode':'test','asset_day':f'{day}-test-{run_id}','historical_controls_only':True,'scope_only':scope_only,'historical_only':historical_only}
 def save():(folder/'controls.json').write_text(json.dumps(state,ensure_ascii=False,indent=2))
 save()
 with TextModel(runtime,folder,profile='review') as model:
  model.protocol_handshake()
  from newsletter_scope_controls import check
  if not historical_only:check(model,folder)
  if not scope_only:verify_controls(model,state,save)
 if not scope_only and not controls_valid(state):raise ValueError('Actual frozen control probe incomplete')
 print(('Synthetic scope controls' if scope_only else 'Five historical controls')+' verified on pinned local CPU model; no issue/art/publication/mail generated.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--runtime',required=True);p.add_argument('--folder',required=True);mode=p.add_mutually_exclusive_group();mode.add_argument('--scope-only',action='store_true');mode.add_argument('--historical-only',action='store_true');a=p.parse_args();run(a.runtime,a.folder,a.scope_only,a.historical_only)
