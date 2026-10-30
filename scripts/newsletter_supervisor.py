"""Keep private durable milestones while a credential-free producer runs."""
import argparse,hashlib,json,os,subprocess,time
from pathlib import Path
import newsletter_checkpoint as checkpoints
SAFE_ENV=('PATH','HOME','LANG','LC_ALL','TMPDIR','CI','GITHUB_RUN_ID','GITHUB_RUN_ATTEMPT','GITHUB_WORKSPACE','RUNNER_TEMP','RUNNER_TRACKING_ID','AP_NEWS_SITE_ROOT','HF_HUB_DISABLE_TELEMETRY','HF_HUB_DISABLE_IMPLICIT_TOKEN','DO_NOT_TRACK')
def child_environment():return {key:os.environ[key] for key in SAFE_ENV if key in os.environ}
def milestone(root,day):
 path=root/'.production-state/draft.json'
 if not path.is_file():return None
 raw=path.read_bytes();json.loads(raw)
 images=tuple(sorted(p.name for p in (root/'img/newsletter').glob(day+'*') if p.is_file() and p.suffix in ('.png','.gif')))
 return hashlib.sha256(raw).hexdigest(),images
def supervise(command,root,day,mode,interval=60,poll=1):
 root=Path(root);process=subprocess.Popen(command,env=child_environment());last=None;last_saved=0;sequence=0
 def preserve():
  nonlocal sequence,last,last_saved
  current=milestone(root,day)
  if current is None:return
  sequence+=1
  checkpoints.save(root,day,mode,os.environ['GITHUB_RUN_ID'],os.environ.get('GITHUB_RUN_ATTEMPT','1')+'-checkpoint-'+str(sequence))
  last=current;last_saved=time.monotonic()
 try:
  while process.poll() is None:
   current=milestone(root,day)
   if current is not None and current!=last and time.monotonic()-last_saved>=interval:
    try:preserve()
    except Exception as exc:
     last_saved=time.monotonic()
     print('Private milestone backup failed; final backup will retry: '+type(exc).__name__,flush=True)
   time.sleep(poll)
  preserve()
  return process.returncode
 finally:
  if process.poll() is None:process.terminate();process.wait(timeout=30)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--date',required=True);p.add_argument('--mode',choices=['test','production'],required=True);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
 command=a.command[1:] if a.command[:1]==['--'] else a.command
 if not command:p.error('Producer command required')
 raise SystemExit(supervise(command,a.root,a.date,a.mode))
