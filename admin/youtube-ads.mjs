const esc=(value='')=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const timestamp=row=>Date.parse(row?.observed_at)||0;
const newest=rows=>[...rows].filter(r=>timestamp(r)>0).sort((a,b)=>timestamp(b)-timestamp(a));
const amount=value=>value==null||value===''||typeof value==='boolean'||!Number.isFinite(Number(value))||Number(value)<0?null:Number(value);
const metric=value=>{const n=amount(value);return Number.isSafeInteger(n)?n:null;};
const number=value=>{const n=metric(value);return n==null?'미확인':n.toLocaleString('ko-KR');};
const money=value=>{const n=amount(value);return n==null?'미확인':'₩'+n.toLocaleString('ko-KR',{maximumFractionDigits:2});};
const time=value=>timestamp({observed_at:value})?new Intl.DateTimeFormat('ko-KR',{dateStyle:'medium',timeStyle:'short',timeZone:'Asia/Seoul'}).format(new Date(value))+' KST':'미확인';
const day=value=>/^\d{4}-\d{2}-\d{2}$/.test(value??'')?esc(value):'미확인';

export function adViewState(observations=[],apiChecks=[],now=Date.now()){
  const attempts=newest(observations.filter(r=>r.source==='youtube_studio'));
  const promotion=attempts[0]?.promotion_id||newest(apiChecks)[0]?.promotion_id;
  const relevant=attempts.filter(r=>r.promotion_id===promotion);
  const observation=relevant.find(r=>r.succeeded===true)||null;
  const checks=newest(apiChecks.filter(r=>r.promotion_id===promotion));
  const cost=amount(observation?.cost_krw),budget=amount(observation?.ad_budget_krw);
  return {observation,lastAttempt:relevant[0]||null,api:checks[0]||null,lastApiSuccess:checks.find(r=>r.ok===true)||null,
    studioFailed:relevant[0]?.succeeded===false,
    stale:!!observation&&now-timestamp(observation)>4*60*60*1000,
    budgetExceeded:cost!=null&&budget!=null&&cost>budget};
}

export function renderYouTubeAdCard(state){
  const {observation:o,lastAttempt,api,lastApiSuccess,studioFailed,stale,budgetExceeded}=state;
  const id=o?.promotion_id||lastAttempt?.promotion_id;
  const video=o?.video_id;
  const links=[/^\d+$/.test(id??'')?`<a href="https://studio.youtube.com/promotion/${id}/edit" target="_blank" rel="noopener noreferrer">Studio에서 확인 ↗</a>`:'',/^[\w-]{11}$/.test(video??'')?`<a href="https://www.youtube.com/watch?v=${video}" target="_blank" rel="noopener noreferrer">본편 보기 ↗</a>`:''].filter(Boolean).join('');
  const warnings=[studioFailed?'최근 점검 실패 · 아래 수치는 마지막으로 확인한 기록입니다.':'',stale?'성과 확인 후 4시간 이상 지났습니다. 마지막 확인 시각을 참고하세요.':'',budgetExceeded?'기록된 광고 예산 초과 · 설정 변경 없이 확인이 필요합니다.':''].filter(Boolean);
  const apiLabel=!api?'연결 확인 대기':api.ok?'연결 확인 성공':'최근 연결 확인 실패';
  const apiNote=api?.report_state==='campaign_unavailable'?'이번 Studio 프로모션의 캠페인 보고는 API에서 반환되지 않았습니다. 아래 성과는 Studio 확인 기록입니다.':api?.report_state==='available'?'API 계정과 캠페인 응답을 확인했습니다. 아래 성과의 출처는 Studio입니다.':'아래 성과와 별도로 Google Ads API 연결 결과를 표시합니다.';
  return `<section class="panel ya-panel" aria-label="한글컵스 YouTube 광고"><div class="ya-heading"><div><p class="eyebrow">HANGEUL CUBS · YOUTUBE</p><h2>한글컵스 광고</h2><p class="ya-title">${esc(o?.ad_title||'새 ㅏ 본편 프로모션')}</p></div><div class="ya-links">${links}</div></div>
    <div class="ya-api"><div><strong>Google Ads API</strong><span class="ya-badge ${api?.ok?'ya-ok':'ya-neutral'}">${apiLabel}</span></div><p>${apiNote}</p><small>API 확인 ${time(api?.observed_at)}${api&&!api.ok&&lastApiSuccess?' · 최근 정상 '+time(lastApiSuccess.observed_at):''}</small></div>
    ${warnings.map(w=>`<p class="ya-warning" role="status">${w}</p>`).join('')}
    <div class="ya-status"><strong>프로모션 상태 <span class="ya-badge ${o?.status==='활성'?'ya-ok':'ya-neutral'}">${esc(o?.status||'미확인')}</span></strong><span>출처: YouTube Studio 직접 확인</span></div>
    ${o?`<div class="ya-metrics">${[['광고 지출',money(o.cost_krw)],['노출수',number(o.impressions)],['광고 조회수',number(o.views)],['구독자 수',number(o.subscribers)],['후속 조회수',number(o.follow_on_views)]].map(([label,value])=>`<div><span>${label}</span><b>${value}</b></div>`).join('')}</div>
    <div class="ya-meta"><span>총 광고 예산 <b>${money(o.ad_budget_krw)}</b></span><span>기간 ${day(o.start_date)} ~ ${day(o.end_date)}</span><span>성과 확인 ${time(o.observed_at)}</span></div>`:'<p class="ya-empty">성과 확인 대기 · 확인하지 못한 수치는 0으로 표시하지 않습니다.</p>'}
    <p class="ya-footnote">2시간 간격 점검 기록 · 실시간 수치가 아닙니다.${lastAttempt?' 최근 점검 '+time(lastAttempt.observed_at)+'.':''} 지출은 광고비이며 세금 포함 실제 청구액과 다를 수 있습니다. 광고 조회수는 본편 전체 조회수와 구분합니다. 활성 상태만으로 노출 시작을 뜻하지 않습니다.</p>
    <p class="ya-load-message" role="status" aria-live="polite"></p></section>`;
}

export function createYouTubeAdsPanel(db,getUser,root){
  let observations=[],checks=[],generation=0;
  function render(){root.innerHTML=renderYouTubeAdCard(adViewState(observations,checks));}
  function clear(){generation++;observations=[];checks=[];root.innerHTML='';}
  async function load(_force=false){
    const user=getUser();if(!user){clear();return false;}
    const token=++generation;
    try{
      const results=await Promise.all(['admin_youtube_ad_observations','admin_youtube_ad_api_checks'].map(t=>db.from(t).select('*').order('observed_at',{ascending:false}).limit(40)));
      if(token!==generation||getUser()?.id!==user.id)return false;
      if(results.some(r=>r.error))throw new Error('read_failed');
      observations=results[0].data||[];checks=results[1].data||[];render();return true;
    }catch{
      if(token!==generation||getUser()?.id!==user.id)return false;
      render();
      const message='저장된 기록을 불러오지 못했습니다. 기존 표시값은 마지막 정상 기록입니다. 새로고침으로 다시 확인하세요.';
      root.querySelector('.ya-load-message').textContent=message;
      return false;
    }
  }
  return {load,clear};
}
