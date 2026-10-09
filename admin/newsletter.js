const API='https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/ap-news';
const esc=(s='')=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels={pending:'확인 메일 대기',processing:'전송 중',retry:'재시도 대기',sent:'전송 서비스 접수',cancelled:'취소',failed:'실패',uncertain:'결과 확인 필요'};
export function createNewsletter(db,getUser){
  let generation=0;
  const box=()=>document.querySelector('#newsletter-section');
  async function load(){
    const host=box();if(!host||!getUser())return;
    const current=++generation;host.innerHTML='<section class="panel"><h2>AP뉴스 구독·발송</h2><p>실제 운영 상태를 불러오고 있습니다.</p></section>';
    try{
      const {data:{session}}=await db.auth.getSession();
      const r=await fetch(`${API}/admin`,{headers:{Authorization:`Bearer ${session?.access_token}`},signal:AbortSignal.timeout(15000)});
      if(!r.ok)throw new Error('운영 상태를 불러오지 못했습니다. 관리자 로그인을 확인해주세요.');
      const data=await r.json();if(current!==generation||!getUser())return;
      host.innerHTML=`<section class="panel"><div class="panel-head"><div><p class="eyebrow">AP NEWS · DAILY</p><h2>구독·발행·발송</h2></div><button class="secondary" data-news-refresh>새로고침</button></div><p>${data.mail_ready?'회사 메일 발송이 연결됐습니다. 확인된 구독자에게만 발행된 호를 보냅니다.':'신청 접수는 가능하며, 회사 메일 발송 연결을 준비하고 있습니다. 확인 전에는 발송하지 않습니다.'}</p><p>발신 <b>alfred.park@apholdings.kr</b> · 한국어 무료 일일판 · 발행 목표 오전 8시</p><div class="co-kpis" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:24px 0"><div class="co-kpi"><span>활성 구독</span><strong style="display:block;font-size:30px">${data.counts.active}</strong></div><div class="co-kpi"><span>이메일 확인 대기</span><strong style="display:block;font-size:30px">${data.counts.pending}</strong></div><div class="co-kpi"><span>구독 해지</span><strong style="display:block;font-size:30px">${data.counts.unsubscribed}</strong></div></div><p><a href="/ko/news/daily/" target="_blank" rel="noopener">공개 뉴스레터 보기 ↗</a></p>${!data.mail_ready?'<p>연결 방법: Resend에서 apholdings.kr 발신 도메인 인증 → Supabase Edge Function Secrets에 RESEND_API_KEY 등록 → AP_NEWS_MAIL_ENABLED=true 설정 → 본인 주소로 구독 확인·발송 시험.</p><p><a href="https://resend.com/domains" target="_blank" rel="noopener">Resend 도메인 설정 ↗</a> · <a href="https://supabase.com/dashboard/project/cgijpcimixaregbpvqbf/functions/secrets" target="_blank" rel="noopener">발송 비밀키 설정 ↗</a></p>':''}</section><section class="panel"><h2>발행호</h2>${data.issues.length?data.issues.map(i=>`<div style="padding:18px 0;border-bottom:1px solid #ddd"><small>${esc(i.issue_date)} · NO. ${i.number} · ${i.status==='published'?'발행':'초안'}</small><h3>${esc(i.title)}</h3><p><a href="${esc(i.web_url)}" target="_blank" rel="noopener">웹 ↗</a> · <a href="${esc(i.pdf_url)}" target="_blank" rel="noopener">PDF ↓</a></p></div>`).join(''):'<p>아직 등록된 발행호가 없습니다.</p>'}</section><section class="panel"><h2>최근 발송 상태</h2><p>「전송 서비스 접수」는 메일 제공사가 요청을 받았다는 뜻이며, 받은편지함 도착을 보장하지 않습니다.</p>${data.deliveries.length?data.deliveries.map(d=>`<p>${esc(d.issue_date||'구독 확인')} · ${esc(labels[d.state]||d.state)} · 시도 ${d.attempts}회 ${d.last_error?'· '+esc(d.last_error):''}</p>`).join(''):'<p>아직 발송 내역이 없습니다.</p>'}<p>최근 처리 ${esc(data.runtime?.last_run||'없음')}</p></section>`;
      host.querySelector('[data-news-refresh]')?.addEventListener('click',load);
    }catch(e){if(current===generation&&getUser())host.innerHTML=`<section class="panel"><h2>AP뉴스 운영 상태</h2><p>${esc(e.message)}</p></section>`;}
  }
  function clear(){generation++;if(box())box().innerHTML='';}
  return {load,clear};
}
