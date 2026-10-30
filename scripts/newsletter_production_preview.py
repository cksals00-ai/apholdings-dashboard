"""Publish only isolated test assets and send one idempotent owner test mail."""
import argparse,json,os,time
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
 out=b.ROOT/'.ap-news-state/server-rehearsal';out.mkdir(parents=True,exist_ok=True)
 (out/'email.html').write_text(email);(out/'manifest.json').write_text(json.dumps({'paths':[web,pdf,*image_paths],'page':page,'pdf':'/'+pdf,'run_id':run}))
 print('Prepared isolated server-production preview; regular edition/queue unchanged')

def finish():
 run=run_id();out=b.ROOT/'.ap-news-state/server-rehearsal';manifest=json.loads((out/'manifest.json').read_text())
 for path in manifest['paths']:
  url=path[:-10] if path.endswith('index.html') else path
  def fetch():
   with urlopen(Request(b.ORIGIN+'/'+url,headers={'Cache-Control':'no-cache'}),timeout=60) as response:data=response.read()
   if data!=(b.ROOT/path).read_bytes():raise ValueError('Public server-generated test bytes differ')
  server.retry(fetch)
 for attempt in range(3):
  try:
   emit(f'test-{run}:newsletter','test_newsletter',{'subject':'[AP News 서버 자동 제작 테스트호] 유료 AI API 없이 제작·공개 검증','message':'공식 원문 수집부터 공개 모델 편집·이미지·PDF·자동 검수까지 서버에서 생성한 별도 테스트호입니다. 정규호 재발송이 아닙니다.','run_url':os.environ['RUN_URL']},(out/'email.html').read_text(),inject=True);break
  except (HTTPError,ValueError):
   if attempt==2:raise
   time.sleep(20)
 emit(f'test-{run}:recovery','test_recovery',{'subject':'[AP News 서버 자동 제작 검증 완료] 공개·메일 접수 확인','message':'서버 제작 테스트호의 웹/PDF/모든 이미지 공개 바이트를 검증했고, 메일의 첫 주입 장애는 재시도로 복구해 제공사가1건 접수했습니다. 받은편지함 도착 확인과는 구분합니다. '+b.ORIGIN+manifest['page'],'run_url':os.environ['RUN_URL']})
 print('Server-generated preview public bytes verified; one owner test mail accepted')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['stage','finish']);parser.add_argument('--bundle',type=Path);parser.add_argument('--date');args=parser.parse_args()
 stage(args.bundle,args.date) if args.stage=='stage' else finish()
