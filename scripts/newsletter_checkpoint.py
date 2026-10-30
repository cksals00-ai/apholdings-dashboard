"""Company-only draft-release checkpoints. Never put source/draft data in public artifacts."""
import argparse,hashlib,json,os,re,subprocess,tempfile,zipfile
from datetime import date
from pathlib import Path,PurePosixPath
REPO='cksals00-ai/apholdings-dashboard'

def allowed(name,day):
 p=PurePosixPath(name)
 return not p.is_absolute() and '..' not in p.parts and '\\' not in name and (name.startswith('.production-state/') or name.startswith('img/newsletter/'+day))
def pack(root,path,day,mode):
 date.fromisoformat(day);root=Path(root)
 state=json.loads((root/'.production-state/draft.json').read_text())
 if state['date']!=day or state['mode']!=mode:raise ValueError('Checkpoint identity mismatch')
 paths=[p for p in (root/'.production-state').rglob('*') if p.is_file() and not p.is_symlink()]
 paths += [p for p in (root/'img/newsletter').glob(day+'*') if p.is_file() and not p.is_symlink()]
 files={str(p.relative_to(root)):p.read_bytes() for p in paths}
 if sum(map(len,files.values()))>200_000_000:raise ValueError('Checkpoint too large')
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as out:
  out.writestr('checkpoint-manifest.json',json.dumps({'date':day,'mode':mode,'files':{p:hashlib.sha256(data).hexdigest() for p,data in files.items()}}))
  for name,data in files.items():
   if not allowed(name,day):raise ValueError('Unexpected checkpoint path')
   out.writestr(name,data)

def unpack(path,root,day,mode):
 root=Path(root)
 with zipfile.ZipFile(path) as z:
  if sum(p.file_size for p in z.infolist())>200_000_000 or len(z.namelist())!=len(set(z.namelist())):raise ValueError('Unsafe checkpoint archive')
  manifest=json.loads(z.read('checkpoint-manifest.json'))
  if manifest['date']!=day or manifest['mode']!=mode:raise ValueError('Checkpoint date/mode mismatch')
  if set(z.namelist())!=set(manifest['files'])|{'checkpoint-manifest.json'}:raise ValueError('Unexpected checkpoint files')
  files={name:z.read(name) for name in manifest['files']}
  for name,data in files.items():
   if not allowed(name,day) or hashlib.sha256(data).hexdigest()!=manifest['files'][name]:raise ValueError('Checkpoint checksum/path mismatch')
  state=json.loads(files['.production-state/draft.json'])
  if state['date']!=day or state['mode']!=mode:raise ValueError('Draft identity mismatch')
  for name,data in files.items():
   target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)

def gh(*args):return subprocess.run(['gh',*args],capture_output=True,text=True)
def metadata(tag):
 # A draft's uncreated tag is not resolved by the by-tag REST endpoint.
 # The authenticated release collection includes drafts (same contract as handoff).
 result=gh('api',f'repos/{REPO}/releases?per_page=100')
 if result.returncode:raise RuntimeError('Cannot establish private checkpoint state')
 release=next((r for r in json.loads(result.stdout) if r['tag_name']==tag),None)
 if release is not None and release.get('draft') is not True:raise ValueError('Checkpoint release must remain private draft')
 return release

def tag_for(day,mode,run):
 date.fromisoformat(day)
 if not run.isdigit():raise ValueError('Invalid run identity')
 return f'ap-news-work-{day}-'+('production' if mode=='production' else 'test-'+run)

def save(root,day,mode,run,attempt):
 if not (Path(root)/'.production-state/draft.json').is_file():print('No draft exists to checkpoint');return
 tag=tag_for(day,mode,run);release=metadata(tag)
 if release is None:
  result=gh('release','create',tag,'--repo',REPO,'--draft','--target','main','--title',f'AP News private work {day} {mode}','--notes','Internal source evidence and generation checkpoints. Do not publish this draft release.')
  if result.returncode:raise RuntimeError('Private checkpoint release creation failed')
  metadata(tag)
 with tempfile.TemporaryDirectory() as folder:
  path=Path(folder)/f'AP-News-work-{day}-{run}-attempt-{attempt}.zip';pack(root,path,day,mode)
  result=gh('release','upload',tag,str(path),'--repo',REPO,'--clobber')
  if result.returncode:raise RuntimeError('Private checkpoint upload failed')
  release=metadata(tag)
  if not any(a['name']==path.name and a['size']==path.stat().st_size for a in release['assets']):raise ValueError('Private checkpoint upload not verified')
  print('Private draft checkpoint saved:',tag,path.name,path.stat().st_size)

def restore(root,day,mode,run,required=False):
 tag=tag_for(day,mode,run);release=metadata(tag)
 if release is None:
  if required:raise ValueError('Requested private test checkpoint not found')
  print('No earlier private checkpoint; begin fresh');return False
 assets=[a for a in release['assets'] if re.fullmatch(r'AP-News-work-\d{4}-\d{2}-\d{2}-\d+-attempt-\d+\.zip',a['name']) and a.get('state')=='uploaded' and a['size']>100]
 if not assets:
  if required:raise ValueError('Requested private checkpoint has no archive')
  return False
 asset=max(assets,key=lambda a:a['updated_at'])
 with tempfile.TemporaryDirectory() as folder:
  result=gh('release','download',tag,'--repo',REPO,'--pattern',asset['name'],'--dir',folder)
  if result.returncode:raise RuntimeError('Private checkpoint download failed; do not regenerate saved work')
  path=Path(folder)/asset['name']
  if path.stat().st_size!=asset['size']:raise ValueError('Private checkpoint size mismatch')
  unpack(path,root,day,mode)
 print('Private checkpoint restored:',asset['name']);return True
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['save','restore']);parser.add_argument('--root',type=Path,required=True);parser.add_argument('--date',required=True);parser.add_argument('--mode',choices=['test','production'],required=True);parser.add_argument('--run',default=os.environ.get('GITHUB_RUN_ID',''));parser.add_argument('--attempt',default=os.environ.get('GITHUB_RUN_ATTEMPT','1'));parser.add_argument('--required',action='store_true');args=parser.parse_args()
 if args.stage=='save':save(args.root,args.date,args.mode,args.run,args.attempt)
 else:restore(args.root,args.date,args.mode,args.run,args.required)
