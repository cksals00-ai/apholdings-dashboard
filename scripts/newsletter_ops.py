"""Server-only operational email and isolated end-to-end rehearsal."""
import json,os,sys,time,re,tempfile
from pathlib import Path
from datetime import datetime,timezone,timedelta
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import newsletter as b
import newsletter_server as server
ROOT=b.ROOT
API='https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news-ops'

def emit(key,event,detail,html=None,inject=False):
 token=os.environ['SUPABASE_SERVICE_KEY']
 data={'key':key,'event':event,'detail':detail,'html':html,'inject_failure':inject}
 request=Request(API,data=json.dumps(data).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
 with urlopen(request,timeout=30) as r:result=json.load(r)
 if not result.get('accepted'):raise ValueError('Operational mail not accepted')
 print(json.dumps({'event':event,'accepted':True,'id':result['id']}),flush=True);return result

def ident():
 run=os.environ['GITHUB_RUN_ID']
 if not run.isdigit():raise ValueError('Invalid run')
 return run

def build_preview():
 run=ident();due=datetime.fromisoformat(os.environ['REHEARSAL_DUE'].replace('Z','+00:00'))
 if due.tzinfo is None or abs((due-datetime.now(timezone.utc)).total_seconds())>900:raise ValueError('Test due must be within15 minutes')
 print('Server reservation waiting until '+due.isoformat(),flush=True)
 while datetime.now(timezone.utc)<due:time.sleep(min(10,(due-datetime.now(timezone.utc)).total_seconds()))
 if int(os.environ.get('GITHUB_RUN_ATTEMPT','1'))==1:
  print('Intentional first publication failure; automatic recovery workflow must rerun this job',flush=True)
  raise ValueError('INJECTED_PUBLICATION_FAILURE')
 issue=json.loads(sorted(b.ISSUES.glob('*.json'))[-1].read_text())
 # Reproduce today's unsupported-source blocker without touching production policy.
 from newsletter_preflight import select_candidates
 candidates=[{'url':'https://unapproved.example.invalid/news','published':issue['date']}]+issue['stories']
 eligibility=select_candidates(candidates,issue['date'],[])
 if not eligibility['ready'] or len(eligibility['rejected'])!=1:raise ValueError('Source preflight recovery failed')
 issue['stories']=eligibility['selected']
 print('Injected unsupported source excluded; supported official candidates retained; no code change or user approval',flush=True)
 issue['title']='AP News 자동화 테스트호'
 issue.update(layout='editorial-v2',hero={'path':'/img/newsletter/ap-editorial-v2.gif','poster':'/img/newsletter/ap-editorial-v2.png','alt':'AP 편집 지면 모션','caption':'AP 브랜드 모션 그래픽 · 실제 제품 화면 아님'})
 issue['intro']='이미 발행된 기사를 사용한 자동 공개·메일·복구 검증입니다. 정규 발행과 구분한 테스트호입니다.'
 webpath=f'/ko/news/daily/preview/automation-{run}/';pdfpath=f'/newsletters/previews/AP-News-test-{run}.pdf'
 web=b.render_issue(issue).replace(b.page_path(issue),webpath).replace(b.pdf_path(issue),pdfpath).replace('content="index,follow"','content="noindex,nofollow"')
 mail=b.render_email(issue).replace(b.page_path(issue),webpath).replace(b.pdf_path(issue),pdfpath)
 mail=mail.replace('{{unsubscribe_url}}',b.ORIGIN+'/ko/news/daily/#subscribe').replace('구독 해지</a>','구독 안내</a>')
 mail=mail.replace('font:36px Georgia,serif"','font:36px Georgia,serif;color:#f7f4ed"')
 b.write(webpath+'index.html',web)
 with tempfile.TemporaryDirectory() as folder:
  previous=b.ROOT;b.ROOT=Path(folder)
  for name in ('img','site-source'):(b.ROOT/name).symlink_to(previous/name,target_is_directory=True)
  try:pdf=b.render_pdf(issue).read_bytes()
  finally:b.ROOT=previous
 target=ROOT/pdfpath.lstrip('/');target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(pdf)
 out=ROOT/'.ap-news-state/rehearsal';out.mkdir(parents=True,exist_ok=True)
 (out/'email.html').write_text(mail)
 (out/'manifest.json').write_text(json.dumps({'run_id':run,'due_at':due.isoformat(),'web_path':webpath,'pdf_path':pdfpath,'attempt':int(os.environ['GITHUB_RUN_ATTEMPT'])}))
 print('Isolated test preview built; no issue registration or subscriber mutation',flush=True)

def finish():
 run=ident();folder=ROOT/'.ap-news-state/rehearsal';m=json.loads((folder/'manifest.json').read_text())
 for path in (m['web_path']+'index.html',m['pdf_path']):
  def check():
   with urlopen(b.ORIGIN+path,timeout=30) as r:data=r.read()
   if data!=(ROOT/path.lstrip('/')).read_bytes():raise ValueError('Public rehearsal bytes differ')
  server.retry(check)
 key=f'test-{run}:newsletter';detail={'subject':'[AP News 자동검증 테스트호] 새 디자인·자동 발행 검증','message':'이미 공개된 기사를 사용한 테스트호','run_url':os.environ.get('RUN_URL')}
 for attempt in range(1,4):
  try:emit(key,'test_newsletter',detail,(folder/'email.html').read_text(),inject=True);break
  except (HTTPError,ValueError) as e:
   print(f'Test mail attempt{attempt} failed; automatic retry in20 seconds',flush=True)
   if attempt==3:raise
   time.sleep(20)
 emit(f'test-{run}:recovery','test_recovery',{'subject':'[AP News 자동검증 복구 완료] 발행·메일 접수 확인','message':f'테스트호 자동 공개 검증 완료. 첫 발행 오류는 자동 재실행으로 복구했고 첫 메일 오류는 자동 재시도로 복구했습니다. 테스트 메일은 지정한 한 주소로1건만 접수됐습니다. 테스트 URL: {b.ORIGIN}{m["web_path"]}','run_url':os.environ.get('RUN_URL')})

def alert():
 run=os.environ['FAILED_RUN_ID'];attempt=int(os.environ['FAILED_ATTEMPT']);test=os.environ['FAILED_NAME']=='AP News automation rehearsal'
 day=datetime.now(server.KST).date().isoformat();key=f'test-{run}:failure-{attempt}' if test else f'{day}:workflow-{run}-{attempt}'
 emit(key,'test_alert' if test else 'ops_alert',{'subject':'[AP News 자동검증 장애 감지]' if test else '[AP News 운영 장애 감지]','message':f'{"의도적으로 주입한 테스트 장애입니다. " if test else ""}서버 실행 {run}의 {attempt}차 시도가 실패했습니다. '+('자동 재실행을 시작합니다.' if attempt<3 else '재시도 한도에 도달했습니다. 관리자 확인이 필요합니다.'),'run_url':f'https://github.com/cksals00-ai/apholdings-dashboard/actions/runs/{run}'})
if __name__=='__main__':
 {'build':build_preview,'finish':finish,'alert':alert}[sys.argv[1]]()
