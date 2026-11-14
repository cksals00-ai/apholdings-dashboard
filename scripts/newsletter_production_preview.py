"""Publish only isolated test assets and send one idempotent owner test mail."""
import argparse,hashlib,json,os,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import newsletter as b
import newsletter_handoff as h
import newsletter_server as server
from newsletter_ops import emit

def run_id():
 value=os.environ['GITHUB_RUN_ID']
 if not value.isdigit():raise ValueError('Invalid test run')
 return value

def stage(bundle,day):
 run=run_id();issue,files=h.validate_bundle(Path(bundle),day)
 image_paths=[s['image']['path'].lstrip('/') for s in issue['stories']]+[issue['hero'][k].lstrip('/') for k in ('path','poster')]
 if any('-test-' not in path for path in image_paths):raise ValueError('Preview may only publish dedicated test images')
 web=f'ko/news/daily/preview/server-{run}/index.html';pdf=f'newsletters/previews/AP-News-server-test-{run}.pdf'
 page='/'+web[:-10]
 html=files[f'ko/news/daily/{day}/index.html'].decode().replace(b.page_path(issue),page).replace(b.pdf_path(issue),'/'+pdf).replace('content="index,follow"','content="noindex,nofollow"')
 for path in image_paths:
  target=b.ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(files[path])
 b.write(web,html);target=b.ROOT/pdf;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(files[f'newsletters/AP-News-{day}.pdf'])
 email=files[f'newsletters/email/{day}.html'].decode().replace(b.page_path(issue),page).replace(b.pdf_path(issue),'/'+pdf).replace('{{unsubscribe_url}}',b.ORIGIN+'/ko/news/daily/#subscribe').replace('구독 해지</a>','구독 안내</a>')
 email_path=f'newsletters/previews/AP-News-server-test-{run}.html'
 b.write(email_path,email)
 out=b.ROOT/'.ap-news-state/server-rehearsal';out.mkdir(parents=True,exist_ok=True)
 (out/'email.html').write_text(email);(out/'manifest.json').write_text(json.dumps({'paths':[web,pdf,email_path,*image_paths],'page':page,'pdf':'/'+pdf,'email':email_path,'run_id':run}))
 print('Prepared isolated server-production preview; regular edition/queue unchanged')

def finish():
 run=run_id();out=b.ROOT/'.ap-news-state/server-rehearsal';manifest=json.loads((out/'manifest.json').read_text())
 if manifest.get('run_id')!=run:raise ValueError('Preview belongs to a different test run')
 for path in manifest['paths']:
  url=path[:-10] if path.endswith('index.html') else path
  def fetch():
   with urlopen(Request(b.ORIGIN+'/'+url,headers={'Cache-Control':'no-cache'}),timeout=60) as response:data=response.read()
   if data!=(b.ROOT/path).read_bytes():raise ValueError('Public server-generated test bytes differ')
  server.retry(fetch)
 injected=False;result=None
 for attempt in range(3):
  try:
   result=emit(f'test-{run}:newsletter','test_newsletter',{'subject':'[AP News 서버 자동 제작 테스트호] 유료 AI API 없이 제작·공개 검증','message':'공식 원문 수집부터 공개 모델 편집·이미지·PDF·자동 검수까지 서버에서 생성한 별도 테스트호입니다. 정규호 재발송이 아닙니다.','run_url':os.environ['RUN_URL']},(out/'email.html').read_text(),inject=True)
   break
  except (HTTPError,ValueError) as exc:
   if isinstance(exc,HTTPError):
    code=exc.code
    try:injected=injected or 'injected_mail_failure' in exc.read().decode(errors='replace')
    finally:exc.close()
    if code not in (408,429,500,502,503,504):raise
   if attempt==2:raise
   print('Test mail failure recorded; retrying the same idempotency key without intermediate mail',flush=True)
   time.sleep(20)
 if not injected or not isinstance(result,dict) or result.get('accepted') is not True or not isinstance(result.get('id'),str) or not result['id']:
  raise ValueError('Actual injected failure and provider acceptance proof required')
 proof={'run_id':run,'public_files_verified':len(manifest['paths']),'injected_failure_observed':True,'attempts':attempt+1,'accepted':True,'provider_receipt_sha256':hashlib.sha256(result['id'].encode()).hexdigest(),'operational_mail_sent':0}
 (out/'mail-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
 print('Server-generated preview public bytes verified; one owner test mail accepted; recovery notices suppressed')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['stage','finish']);parser.add_argument('--bundle',type=Path);parser.add_argument('--date');args=parser.parse_args()
 stage(args.bundle,args.date) if args.stage=='stage' else finish()
