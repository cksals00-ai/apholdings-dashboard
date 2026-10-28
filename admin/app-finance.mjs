const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const isoDay = () => new Date(Date.now() + 9 * 3600e3).toISOString().slice(0,10);
const money = (v) => v === null ? '미수집' : `${v.toLocaleString('ko-KR')} KRW`;
export function financeRows({apps=[],metrics=[],today=isoDay(),days=30,platform='apple',metricsError=false}={}) {
  const n=[7,30,90].includes(Number(days)) ? Number(days) : 30;
  const start=new Date(`${today}T00:00:00Z`); start.setUTCDate(start.getUTCDate()-n+1);
  const since=start.toISOString().slice(0,10);
  return apps.filter(a=>a.status!=='excluded').map(a=>{
    // The existing collector is Apple-only; Google must never inherit its rows.
    const rows=platform==='apple' && !metricsError ? metrics.filter(r=>r.app_id===a.id && (!r.platform || r.platform==='apple') && r.day>=since && r.day<=today && !/sandbox|test/i.test(r.environment || '')) : [];
    const values=rows.filter(r=>r.proceeds_krw!==null && r.proceeds_krw!==undefined && r.proceeds_krw!=='' && Number.isFinite(Number(r.proceeds_krw)));
    return {id:a.id,name:a.name,platform,status:platform==='apple' ? ({live:'출시',in_review:'심사 중',preparing:'준비 중',paused:'보류'}[a.status] || '확인 필요') : '출시 상태 미연결',revenue:values.length ? values.reduce((sum,r)=>sum+Number(r.proceeds_krw),0) : null,latest:rows.map(r=>r.day).sort().at(-1) || null,partial:rows.length<n,fx:rows.some(r=>r.fx_note),error:metricsError,since,today};
  });
}
export function renderFinance(options={}) {
  const {platform='apple',days=30,runtime=[]}=options;
  const rows=financeRows(options),rt=runtime.find(r=>r.id===(platform==='apple'?'asc_sales':'google_sales'));
  const updated=rt?.checked_at && Number.isFinite(Date.parse(rt.checked_at)) ? new Date(rt.checked_at).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})+' KST' : '미수집';
  return `<section class="app-finance" aria-label="앱 매출 정산 통합"><h3 class="app-sub">출시 · 매출 · 정산 · 입금</h3><div class="app-sync"><label>플랫폼 <select data-finance-platform><option value="apple" ${platform==='apple'?'selected':''}>Apple</option><option value="google" ${platform==='google'?'selected':''}>Google Play</option></select></label><label>기간 <select data-finance-days>${[7,30,90].map(n=>`<option value="${n}" ${Number(days)===n?'selected':''}>최근 ${n}일</option>`).join('')}</select></label><span>${platform==='google' && rt?.status!=='ready'?'연결 상태 확인':'판매 마지막 수집'}: ${esc(updated)}</span></div><p class="panel-note">${platform==='apple'?'예상 개발자 수익 · Apple 일별 보고서 · KRW 환산 추정 포함 가능':'Google 판매·정산 연결 대기 · '+esc(rt?.detail || '판매 보고서 미수집 · 연결 상태 확인 필요')} · 확정 정산과 은행 입금은 별도입니다.</p><div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>앱 / 플랫폼</th><th>출시 상태</th><th>선택 기간 예상 개발자 수익</th><th>확정 정산</th><th>최신 판매 보고서</th></tr></thead><tbody>${rows.map(r=>`<tr><td><b>${esc(r.name)}</b><small>${platform==='apple'?'Apple':'Google Play'}</small></td><td>${esc(r.status)}</td><td>${r.error?'수집 오류':money(r.revenue)}${r.revenue!==null && r.partial?'<small>기간 일부만 수집 · 누락일 미확정</small>':''}${r.fx?'<small>환율 환산 추정 포함</small>':''}</td><td>미연결</td><td>${esc(r.latest || '미수집')}</td></tr>`).join('') || '<tr><td colspan="5">등록된 앱 정보가 없습니다.</td></tr>'}</tbody></table></div><div class="app-sync"><div><b>정산 · 플랫폼 지급 · 계정 단위</b>${accountEvidence(runtime,platform)}</div></div><p class="panel-note">테스트 결제는 실매출에서 제외합니다. 환불은 보고서 반영 시 포함되며, 미수집은 0원이 아닙니다. 판매·정산·지급·입금의 출처와 기간이 일치할 때만 대조합니다.</p></section>`;
}

export function metricSummary(rows=[]) {
  const sum=(key)=>{const xs=rows.filter(r=>r[key]!==null && r[key]!==undefined && r[key]!=='' && Number.isFinite(Number(r[key])));return xs.length ? xs.reduce((v,r)=>v+Number(r[key]),0):null;};
  const units=sum('units'),iap=sum('iap_units');
  return {downloads:sum('downloads'),revenue:sum('proceeds_krw'),units:units===null && iap===null ? null:(units??0)+(iap??0),reportedDays:new Set(rows.map(r=>r.day).filter(Boolean)).size};
}
function accountEvidence(runtime,platform) {
  const r=runtime.find(r=>r.id=== (platform==='apple'?'asc_finance':'google_finance'));
  if(platform==='google' && r?.status==='blocked') return `<p>정산·지급 내역 미수집 · ${esc(r.detail)}</p><p>공식 화면 확인: ${esc(r.checked_at)} · 금액과 지급 상태는 확인되지 않았습니다.</p><a href="https://play.google.com/console/u/0/developers/7870440470636306408/paymentssettings" target="_blank" rel="noopener">Google 판매자 결제 프로필 설정 ↗</a><p>은행 입금 미확인 · 은행 거래내역 연결 없음</p>`;
  if(!r || r.status!=='ready') return '<p>정산·지급 내역 미연결 · 앱별 입금으로 배분하지 않습니다.</p><p>은행 입금 미확인 · 확인 필요 · 은행 거래내역 연결 없음</p>';
  let e;try{e=JSON.parse(r.detail);}catch{return '<p>정산·지급 내역 미연결 · 자료 형식 확인 필요</p>';}
  if(!e || typeof e!=='object' || e.schemaVersion!==1 || e.platform!==platform || !/^\d{4}-\d{2}$/.test(e.period) || e.currency!=='KRW' || ![e.gross,e.adjustment,e.expectedProceeds].every(Number.isFinite)) return '<p>정산·지급 내역 미연결 · 자료 검증 필요</p>';
  const won=v=>`${v.toLocaleString('ko-KR')} KRW`;
  return `<div><b>${esc(e.period)} · ${esc(e.source)}</b><p>공식 화면 직접 확인 · 확인 시각 ${esc(e.observedAt)} · 원본 갱신일 ${esc(e.sourceUpdatedAt)}</p><p>재무 보고서 수입 ${won(e.gross)} · 세금·조정 ${won(e.adjustment)} · 예상 수익금 <strong>${won(e.expectedProceeds)}</strong></p><p>${e.paymentStatus==='paid'?'Apple 지급 완료':'지급 예정 · 실제 지급 미확인'} · 예상 지급일 ${esc(e.expectedPaymentDate || '미확인')}</p><p>계정 전체 금액 · 특정 앱 매출·입금으로 배분하지 않습니다.</p><p><b>은행 입금 미확인</b> · 확인 필요 · 은행 거래내역 연결 없음</p><a href="https://appstoreconnect.apple.com/itc/payments_and_financial_reports#/" target="_blank" rel="noopener">Apple 원본 확인 ↗</a><p>자동 금융 API 수집이 아닌 확인 시점의 공식 자료입니다. 이후 상태는 다시 확인해야 합니다.</p></div>`;
}
