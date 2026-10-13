const API='https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news';
const esc=(s='')=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels={pending:'대기',processing:'전송 중',retry:'재시도 대기',sent:'전송 서비스 접수',cancelled:'취소',failed:'실패',uncertain:'결과 확인 필요'};
const statuses={pending:'이메일 확인 대기',active:'구독 중',unsubscribed:'해지'};
const stamp=value=>{if(!value)return '—';const d=new Date(value);return Number.isNaN(d.getTime())?'—':d.toLocaleString('ko-KR',{timeZone:'Asia/Seoul',hour12:false});};
const fold=(title,body)=>`<details class="news-fold"><summary>${title}</summary><div class="news-fold-body">${body}</div></details>`;
const delivery=d=>`<p class="news-delivery">${esc(d.kind==='confirmation'?'구독 확인':d.issue_date||'뉴스레터')} · ${esc(labels[d.state]||d.state)} · 시도 ${Number(d.attempts)||0}회<br><small>${esc(stamp(d.created_at))}${d.last_error?' · '+esc(d.last_error):''}</small></p>`;
const issue=i=>`<article class="news-issue"><small>${esc(i.issue_date)} · NO. ${esc(i.number)} · ${i.status==='published'?'발행':'초안'}</small><h3>${esc(i.title)}</h3><a href="${esc(i.web_url)}" target="_blank" rel="noopener">웹 ↗</a> · <a href="${esc(i.pdf_url)}" target="_blank" rel="noopener">PDF ↓</a></article>`;
export function createNewsletter(db,getUser){
  let generation=0;
  const box=()=>document.querySelector('#newsletter-section');
  async function load(){
    const host=box();if(!host||!getUser())return;
    const current=++generation;host.innerHTML='<section class="panel"><h2>AP뉴스 구독·발송</h2><p>운영 상태를 불러오고 있습니다.</p></section>';
    try{
      const {data:{session}}=await db.auth.getSession();
      const r=await fetch(`${API}/admin`,{headers:{Authorization:`Bearer ${session?.access_token}`},signal:AbortSignal.timeout(15000)});
      if(!r.ok)throw new Error('운영 상태를 불러오지 못했습니다. 관리자 로그인을 확인해주세요.');
      const data=await r.json();if(current!==generation||!getUser())return;
      const people=data.subscribers||[], mails=data.deliveries||[], issues=data.issues||[];
      const person=s=>`<article class="news-person"><div class="news-person-head"><div><strong>${esc(s.name||'이름 미입력')}</strong><div class="news-email">${esc(s.email)}</div></div><span class="news-status">${esc(statuses[s.status]||s.status)}</span></div><small>신청 ${esc(stamp(s.created_at||s.consent_at))}</small><details class="news-fold" data-news-history="${esc(s.id)}"><summary>확인·발송 상세</summary><div class="news-fold-body"><p>이메일 확인 ${esc(stamp(s.confirmed_at))} · 해지 ${esc(stamp(s.unsubscribed_at))}</p><div data-history-body>펼치면 최근 발송 기록을 불러옵니다.</div></div></details></article>`;
      host.innerHTML=`<section class="panel"><div class="panel-head"><div><p class="eyebrow">AP NEWS · DAILY</p><h2>구독·발행·발송</h2></div><button class="secondary" data-news-refresh>새로고침</button></div><p>${data.mail_ready?'회사 메일 발송 연결됨':'구독 신청 접수 중 · 메일 발송 연결 대기'}</p><div class="news-kpis">${[['구독 중',data.counts.active],['확인 대기',data.counts.pending],['해지',data.counts.unsubscribed]].map(([label,n])=>`<div><span>${label}</span><strong>${Number(n)||0}</strong></div>`).join('')}</div>${fold('운영 설정 더보기',`<p>발신 alfred.park@apholdings.kr · 한국어 무료 일일판 · 발행 목표 오전 8시</p><p>이메일 확인을 완료한 구독자에게 발송합니다. 전송 서비스 접수는 받은편지함 도착을 보장하지 않습니다.</p><p>최근 처리 ${esc(stamp(data.runtime?.last_run))}</p>${!data.mail_ready?'<p>Resend 도메인 인증 → Supabase에 RESEND_API_KEY와 AP_NEWS_MAIL_ENABLED=true 저장 → 발송 확인</p><p><a href="https://resend.com/domains" target="_blank" rel="noopener">도메인 설정 ↗</a> · <a href="https://supabase.com/dashboard/project/cgijpcimixaregbpvqbf/functions/secrets" target="_blank" rel="noopener">발송 설정 ↗</a></p>':''}`)}</section><section class="panel"><h2>최근 구독 신청</h2><p class="news-caption">최근 5명 · 신청 시각은 한국시간입니다.</p>${people.slice(0,5).map(person).join('')||'<p>구독 신청이 없습니다.</p>'}${fold('구독 신청 목록 더보기',`<div class="news-filters"><label>이름·이메일 검색<input type="search" data-news-search placeholder="이름 또는 이메일"></label><label>구독 상태<select data-news-status><option value="">전체</option><option value="pending">확인 대기</option><option value="active">구독 중</option><option value="unsubscribed">해지</option></select></label></div><p data-news-result aria-live="polite">${people.length}명</p><div data-news-people>${people.map(person).join('')||'<p>구독 신청이 없습니다.</p>'}</div>`)}</section><section class="panel"><div class="panel-head"><h2>최신 발행호</h2><a href="/ko/news/daily/" target="_blank" rel="noopener">공개 뉴스레터 ↗</a></div>${issues.length?issue(issues[0]):'<p>등록된 발행호가 없습니다.</p>'}${issues.length>1?fold(`이전 발행호 더보기 (${issues.length-1})`,issues.slice(1).map(issue).join('')):''}${fold(`최근 발송 내역 더보기 (${mails.length})`,mails.map(d=>`<div>${esc(people.find(s=>s.id===d.subscriber_id)?.email||'신청자 정보 없음')}${delivery(d)}</div>`).join('')||'<p>발송 내역이 없습니다.</p>')}</section>`;
      if(host.newsToggle)host.removeEventListener('toggle',host.newsToggle,true);
      host.newsToggle=async event=>{
        const detail=event.target;if(!detail.matches?.('[data-news-history]')||!detail.open||detail.dataset.loading==='true'||detail.dataset.loaded==='true')return;
        detail.dataset.loading='true';const body=detail.querySelector('[data-history-body]');body.textContent='발송 기록을 불러오고 있습니다.';
        try{const response=await fetch(`${API}/admin-history?id=${encodeURIComponent(detail.dataset.newsHistory)}`,{headers:{Authorization:`Bearer ${session?.access_token}`},signal:AbortSignal.timeout(15000)});if(!response.ok)throw new Error();const history=await response.json();if(current!==generation||!getUser())return;body.innerHTML=history.deliveries.map(delivery).join('')||'<p>발송 기록이 없습니다.</p>';detail.dataset.loaded='true';}catch{if(current===generation&&getUser())body.textContent='발송 기록을 불러오지 못했습니다. 접었다가 다시 열어주세요.';}finally{detail.dataset.loading='false';}
      };host.addEventListener('toggle',host.newsToggle,true);
      const search=host.querySelector('[data-news-search]'), status=host.querySelector('[data-news-status]');
      const filter=()=>{const q=search.value.trim().toLocaleLowerCase(),state=status.value;const matches=people.filter(s=>(!state||s.status===state)&&`${s.name} ${s.email}`.toLocaleLowerCase().includes(q));host.querySelector('[data-news-people]').innerHTML=matches.map(person).join('')||'<p>검색 결과가 없습니다.</p>';host.querySelector('[data-news-result]').textContent=`${matches.length}명`;};
      search?.addEventListener('input',filter);status?.addEventListener('change',filter);
      host.querySelector('[data-news-refresh]')?.addEventListener('click',load);
    }catch(e){if(current===generation&&getUser())host.innerHTML=`<section class="panel"><h2>AP뉴스 운영 상태</h2><p>${esc(e.message)}</p><button class="secondary" data-news-retry>다시 불러오기</button></section>`;host.querySelector('[data-news-retry]')?.addEventListener('click',load);}
  }
  function clear(){generation++;const host=box();if(host){if(host.newsToggle)host.removeEventListener('toggle',host.newsToggle,true);host.innerHTML='';}}
  return {load,clear};
}
