const API='https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news';
const esc=(s='')=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels={pending:'대기',processing:'전송 중',retry:'재시도 대기',sent:'전송 서비스 접수',cancelled:'취소',failed:'실패',uncertain:'결과 확인 필요'};
const statuses={pending:'이메일 확인 대기',active:'구독 중',unsubscribed:'해지'};
const stamp=value=>{if(!value)return '—';const d=new Date(value);return Number.isNaN(d.getTime())?'—':d.toLocaleString('ko-KR',{timeZone:'Asia/Seoul',hour12:false});};
const fold=(title,body)=>`<details class="news-fold"><summary>${title}</summary><div class="news-fold-body">${body}</div></details>`;
const delivery=d=>`<p class="news-delivery">${esc(d.kind==='confirmation'?'구독 확인':d.issue_date||'뉴스레터')} · ${esc(labels[d.state]||d.state)} · 시도 ${Number(d.attempts)||0}회<br><small>${esc(stamp(d.created_at))}${d.last_error?' · '+esc(d.last_error):''}</small></p>`;
const issue=i=>`<article class="news-issue"><small>${esc(i.issue_date)} · NO. ${esc(i.number)} · ${i.status==='published'?'발행':'초안'}</small><h3>${esc(i.title)}</h3><a href="${esc(i.web_url)}" target="_blank" rel="noopener">웹 ↗</a> · <a href="${esc(i.pdf_url)}" target="_blank" rel="noopener">PDF ↓</a></article>`;
const badge=s=>`<span class="news-status" data-status="${esc(s.status)}">${esc(statuses[s.status]||s.status)}</span>`;
const kstDay=now=>new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
const safeLink=value=>{try{const u=new URL(value);return u.protocol==='https:'&&['www.apholdings.kr','apholdings.kr','github.com'].includes(u.hostname)?u.href:'';}catch{return '';}};
export function pipelineSummary(data,now=new Date()){
  const pipeline=data.pipeline||{},day=pipeline.today||kstDay(now);
  const run=(pipeline.runs||[]).find(r=>r.issue_date===day)||{};
  const edition=(data.issues||[]).find(i=>i.issue_date===day);
  const totals=(pipeline.delivery_summary||[]).find(d=>d.issue_date===day)||{};
  const count=key=>Math.max(0,Number(totals[key])||0);
  const ready=run.ready_verified_at?{tone:'ok',label:'전달·검증 완료',time:run.ready_verified_at}:
    run.ready_at?{tone:'working',label:'전달 확인 중',time:run.ready_at}:{tone:'wait',label:'완성본 전달 대기'};
  const publication=run.public_verified_at&&run.registered_at&&edition?.status==='published'&&edition?.verified?
    {tone:'ok',label:'공개·등록 확인',time:run.public_verified_at}:
    run.public_verified_at?{tone:'working',label:'공개 확인 · 등록 대기',time:run.public_verified_at}:
    run.deployed_at?{tone:'working',label:'배포 완료 · 공개 확인 중',time:run.deployed_at}:
    run.publication_started_at?{tone:'working',label:'발행 처리 중',time:run.publication_started_at}:
    edition?{tone:'unknown',label:'등록됨 · 공개 확인 대기'}:
    {tone:'wait',label:ready.tone==='ok'?'발행 예약 대기':'완성본 준비 후 발행'};
  const accepted=count('accepted'),waiting=count('pending')+count('processing')+count('retry');
  const failed=count('failed'),uncertain=count('uncertain')+count('unconfirmed');
  let mail={tone:'wait',label:publication.tone==='ok'?'메일 큐 처리 대기':'발행 후 발송 대기'};
  if(accepted||waiting||failed||uncertain){
    const parts=[`접수 ${accepted}건`];
    if(waiting)parts.push(`대기 ${waiting}건`);
    if(failed)parts.push(`실패 ${failed}건`);
    if(uncertain)parts.push(`확인 필요 ${uncertain}건`);
    const complete=accepted>0&&accepted===count('total')-count('cancelled')&&!waiting&&!failed&&!uncertain;
    mail={tone:failed?'error':uncertain?'warn':complete?'ok':'working',label:parts.join(' · '),time:totals.last_attempted_at,time_label:'전송 시도 '};
  }else if(!data.mail_ready)mail={tone:'warn',label:'메일 연결 확인 필요'};
  else if(publication.tone==='ok'&&Number(data.counts?.confirmed_active??data.counts?.active)===0)mail={tone:'unknown',label:'발송 대상 없음'};
  return {day,title:run.title||edition?.title||'완성본 전달 대기',ready,publication,mail,run,edition,totals,checked_at:pipeline.checked_at};
}
export function renderPipeline(data){
  const s=pipelineSummary(data);
  const steps=[['서버 전달',s.ready],['홈페이지 발행',s.publication],['메일 발송',s.mail]];
  const runs=data.pipeline?.runs||[],others=runs.filter(r=>r.issue_date!==s.day);
  const links=[['웹 보기',s.edition?.web_url],['PDF 보기',s.edition?.pdf_url],['서버 처리 기록',s.run.workflow_url]].map(([label,url])=>safeLink(url)?`<a href="${esc(safeLink(url))}" target="_blank" rel="noopener noreferrer">${label} ↗</a>`:'').filter(Boolean).join(' · ');
  const details=`<p>서버 조회 ${esc(stamp(s.checked_at))} · 발행 목표 오전 8시 (한국시간)</p><p>${links||'공개 링크는 발행 확인 후 표시됩니다.'}</p>${s.run.bundle_filename?`<p>전달 파일 ${esc(s.run.bundle_filename)}<br><small class="news-hash">SHA256 ${esc(s.run.bundle_sha256||'—')}</small></p>`:''}${s.run.last_error?`<p class="news-pipeline-error">최근 오류: ${esc(s.run.last_error)}</p>`:''}<p>메일 접수는 전송 서비스가 요청을 받은 상태이며, 받은편지함 도착을 의미하지 않습니다. 완성본이 없으면 이전 호를 재발송하지 않습니다.</p>${others.length?`<p>다른 날짜 기록</p><ul>${others.map(r=>`<li>${esc(r.issue_date)} · ${esc(r.title||'뉴스레터')} · ${r.registered_at?'공개 확인':r.ready_verified_at?'전달 완료 · 발행 대기':'처리 확인 중'}${r.last_error?' · 오류 있음':''}</li>`).join('')}</ul>`:''}`;
  return `<section class="news-pipeline" aria-label="뉴스레터 전달·발행·메일 상태"><div class="news-pipeline-heading"><div><p class="eyebrow">TODAY · ${esc(s.day)}</p><h3>${esc(s.title)}</h3></div><span class="news-caption">유료 AI API 사용 안 함</span></div><div class="news-pipeline-steps">${steps.map(([label,step],i)=>`<article class="news-pipeline-step" data-tone="${step.tone}"><p><span>${i+1}</span> ${label}</p><strong>${esc(step.label)}</strong><small>${esc(step.time?(step.time_label||'')+stamp(step.time):'확인 기록 대기')}</small></article>`).join('')}</div>${s.run.last_error?'<p class="news-pipeline-error" role="status">최근 처리 오류가 있습니다. 상세 기록을 확인하세요.</p>':''}${fold('전달·발행 상세 더보기',details)}</section>`;
}
export function createNewsletter(db,getUser){
  let generation=0,filter={q:'',state:''},editing=null,flash=null,people=[];
  const box=()=>document.querySelector('#newsletter-section');
  const token=async()=>{const {data:{session}}=await db.auth.getSession();return session?.access_token;};
  async function request(path,body){
    const init={headers:{Authorization:`Bearer ${await token()}`},signal:AbortSignal.timeout(15000)};
    if(body!==undefined){init.method='POST';init.headers['Content-Type']='application/json';init.body=JSON.stringify(body);}
    const r=await fetch(`${API}/${path}`,init);
    let json={};try{json=await r.json();}catch{}
    if(!r.ok)throw new Error(json.message||'처리하지 못했습니다. 잠시 후 다시 시도해주세요.');
    return json;
  }
  const visible=()=>{const q=filter.q.trim().toLocaleLowerCase();return people.filter(s=>(!filter.state||s.status===filter.state)&&`${s.name} ${s.email}`.toLocaleLowerCase().includes(q));};
  const row=s=>{
    const id=esc(s.id);
    if(editing===s.id){
      return `<tr class="news-edit" data-id="${id}"><td><input data-f="name" value="${esc(s.name)}" maxlength="60" placeholder="이름(선택)" aria-label="이름"></td><td>${s.status==='active'?`${esc(s.email)}<small class="news-hint">구독 중인 주소는 바꿀 수 없어요</small>`:`<input data-f="email" type="email" value="${esc(s.email)}" aria-label="이메일">`}</td><td>${badge(s)}</td><td>${esc(stamp(s.created_at||s.consent_at))}</td><td>${esc(stamp(s.confirmed_at))}</td><td class="news-actions"><button data-act="save">저장</button> <button class="secondary" data-act="cancel">취소</button></td></tr>`;
    }
    const buttons=[`<button class="secondary" data-act="edit">수정</button>`];
    if(s.status==='pending')buttons.push(`<button class="secondary" data-act="resend">확인 메일 재발송</button>`);
    if(s.status==='active')buttons.push(`<button class="secondary" data-act="unsubscribe">해지</button>`);
    if(s.status!=='active')buttons.push(`<button class="secondary danger" data-act="delete">삭제</button>`);
    return `<tr data-id="${id}"><td>${esc(s.name||'이름 미입력')}</td><td class="news-email">${esc(s.email)}</td><td>${badge(s)}</td><td>${esc(stamp(s.created_at||s.consent_at))}</td><td>${esc(stamp(s.confirmed_at))}</td><td class="news-actions">${buttons.join(' ')}<details class="news-fold" data-news-history="${id}"><summary>확인·발송 기록</summary><div class="news-fold-body"><p>해지 ${esc(stamp(s.unsubscribed_at))}</p><div data-history-body>펼치면 최근 발송 기록을 불러옵니다.</div></div></details></td></tr>`;
  };
  const table=()=>{const list=visible();return list.length?`<div class="news-table-wrap"><table class="news-table"><thead><tr><th>이름</th><th>이메일</th><th>상태</th><th>신청</th><th>확인</th><th>관리</th></tr></thead><tbody>${list.map(row).join('')}</tbody></table></div>`:'<p>조건에 맞는 구독자가 없습니다.</p>';};
  const paint=host=>{const t=host.querySelector('[data-news-people]'),c=host.querySelector('[data-news-result]');if(t)t.innerHTML=table();if(c)c.textContent=`${visible().length}명`;};
  async function load(){
    const host=box();if(!host||!getUser())return;
    const current=++generation;
    if(!people.length)host.innerHTML='<section class="panel"><h2>AP뉴스 구독·발송</h2><p>운영 상태를 불러오고 있습니다.</p></section>';
    try{
      const data=await request('admin');if(current!==generation||!getUser())return;
      people=data.subscribers||[];const mails=data.deliveries||[],issues=data.issues||[];
      host.innerHTML=`<section class="panel"><div class="panel-head"><div><p class="eyebrow">AP NEWS · DAILY</p><h2>구독·발행·발송</h2></div><button class="secondary" data-news-refresh>새로고침</button></div>${renderPipeline(data)}<p>${data.mail_ready?'회사 메일 발송 연결됨':'구독 신청 접수 중 · 메일 발송 연결 대기'}</p><div class="news-kpis">${[['구독 중',data.counts.active],['확인 대기',data.counts.pending],['해지',data.counts.unsubscribed]].map(([label,n])=>`<div><span>${label}</span><strong>${Number(n)||0}</strong></div>`).join('')}</div>${fold('운영 설정 더보기',`<p>발신 alfred.park@apholdings.kr · 한국어 무료 일일판 · 발행 목표 오전 8시</p><p>이메일 확인을 완료한 구독자에게 발송합니다. 전송 서비스 접수는 받은편지함 도착을 보장하지 않습니다.</p><p>최근 처리 ${esc(stamp(data.runtime?.last_run))}</p>${!data.mail_ready?'<p>Resend 도메인 인증 → Supabase에 RESEND_API_KEY와 AP_NEWS_MAIL_ENABLED=true 저장 → 발송 확인</p><p><a href="https://resend.com/domains" target="_blank" rel="noopener">도메인 설정 ↗</a> · <a href="https://supabase.com/dashboard/project/cgijpcimixaregbpvqbf/functions/secrets" target="_blank" rel="noopener">발송 설정 ↗</a></p>':''}`)}</section><section class="panel"><h2>구독자 관리</h2><p class="news-caption">신청 시각은 한국시간입니다. 추가한 주소로는 확인 메일(약 5분)이 가고, 본인이 확인 링크를 눌러야 구독이 시작됩니다.</p><div class="news-add"><label>이름(선택)<input data-add="name" maxlength="60" placeholder="이름"></label><label>이메일<input data-add="email" type="email" placeholder="name@company.com"></label><button data-act="add">추가하고 확인 메일 보내기</button></div><p class="news-flash" data-news-flash aria-live="polite" ${flash?`data-kind="${esc(flash.kind)}"`:''}>${flash?esc(flash.text):''}</p><div class="news-filters"><label>이름·이메일 검색<input type="search" data-news-search placeholder="이름 또는 이메일" value="${esc(filter.q)}"></label><label>구독 상태<select data-news-status><option value="">전체</option>${Object.entries(statuses).map(([v,l])=>`<option value="${v}"${filter.state===v?' selected':''}>${l}</option>`).join('')}</select></label></div><p data-news-result aria-live="polite">${visible().length}명</p><div data-news-people>${table()}</div></section><section class="panel"><div class="panel-head"><h2>최신 발행호</h2><a href="/ko/news/daily/" target="_blank" rel="noopener">공개 뉴스레터 ↗</a></div>${issues.length?issue(issues[0]):'<p>등록된 발행호가 없습니다.</p>'}${issues.length>1?fold(`이전 발행호 더보기 (${issues.length-1})`,issues.slice(1).map(issue).join('')):''}${fold(`최근 발송 내역 더보기 (${mails.length})`,mails.map(d=>`<div>${esc(people.find(s=>s.id===d.subscriber_id)?.email||'신청자 정보 없음')}${delivery(d)}</div>`).join('')||'<p>발송 내역이 없습니다.</p>')}</section>`;
      flash=null;
      bind(host,current);
    }catch(e){if(current===generation&&getUser())host.innerHTML=`<section class="panel"><h2>AP뉴스 운영 상태</h2><p>${esc(e.message)}</p><button class="secondary" data-news-retry>다시 불러오기</button></section>`;host.querySelector('[data-news-retry]')?.addEventListener('click',load);}
  }
  function bind(host,current){
    if(host.newsToggle)host.removeEventListener('toggle',host.newsToggle,true);
    if(host.newsClick)host.removeEventListener('click',host.newsClick);
    if(host.newsInput)host.removeEventListener('input',host.newsInput);
    host.newsToggle=async event=>{
      const detail=event.target;if(!detail.matches?.('[data-news-history]')||!detail.open||detail.dataset.loading==='true'||detail.dataset.loaded==='true')return;
      detail.dataset.loading='true';const body=detail.querySelector('[data-history-body]');body.textContent='발송 기록을 불러오고 있습니다.';
      try{const history=await request(`admin-history?id=${encodeURIComponent(detail.dataset.newsHistory)}`);if(current!==generation||!getUser())return;body.innerHTML=history.deliveries.map(delivery).join('')||'<p>발송 기록이 없습니다.</p>';detail.dataset.loaded='true';}catch{if(current===generation&&getUser())body.textContent='발송 기록을 불러오지 못했습니다. 접었다가 다시 열어주세요.';}finally{detail.dataset.loading='false';}
    };
    host.newsInput=event=>{
      if(event.target.matches?.('[data-news-search]')){filter.q=event.target.value;paint(host);}
      else if(event.target.matches?.('[data-news-status]')){filter.state=event.target.value;paint(host);}
    };
    host.newsClick=async event=>{
      const btn=event.target.closest?.('[data-act],[data-news-refresh]');if(!btn)return;
      if(btn.matches('[data-news-refresh]')){await load();return;}
      const act=btn.dataset.act,tr=btn.closest('tr'),id=tr?.dataset.id,person=people.find(s=>s.id===id);
      const run=async(path,body,ok)=>{
        btn.disabled=true;
        try{const r=await request(path,body);editing=null;flash={kind:'ok',text:r.message||ok};}
        catch(e){flash={kind:'error',text:e.message};btn.disabled=false;const f=host.querySelector('[data-news-flash]');if(f){f.dataset.kind='error';f.textContent=e.message;}return;}
        await load();
      };
      if(act==='edit'){editing=id;paint(host);return;}
      if(act==='cancel'){editing=null;paint(host);return;}
      if(act==='save'){const name=tr.querySelector('[data-f="name"]')?.value??'',email=tr.querySelector('[data-f="email"]')?.value;const body={id,name};if(email!==undefined)body.email=email;await run('admin-update',body,'저장했어요.');return;}
      if(act==='resend'){await run('admin-resend',{id},'확인 메일을 다시 보냅니다.');return;}
      if(act==='unsubscribe'){if(globalThis.confirm?.(`${person?.email} 구독을 해지할까요? 앞으로 뉴스레터가 가지 않아요.`)===false)return;await run('admin-unsubscribe',{id},'해지했어요.');return;}
      if(act==='delete'){if(globalThis.confirm?.(`${person?.email} 을(를) 목록에서 삭제할까요? 되돌릴 수 없어요.`)===false)return;await run('admin-delete',{id},'삭제했어요.');return;}
      if(act==='add'){const name=host.querySelector('[data-add="name"]')?.value??'',email=host.querySelector('[data-add="email"]')?.value??'';await run('admin-add',{name,email},'추가했어요.');return;}
    };
    host.addEventListener('toggle',host.newsToggle,true);host.addEventListener('click',host.newsClick);host.addEventListener('input',host.newsInput);
  }
  function clear(){generation++;people=[];editing=null;flash=null;const host=box();if(host){if(host.newsToggle)host.removeEventListener('toggle',host.newsToggle,true);if(host.newsClick)host.removeEventListener('click',host.newsClick);if(host.newsInput)host.removeEventListener('input',host.newsInput);host.innerHTML='';}}
  return {load,clear};
}
