const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const count=v=>typeof v==='number' && Number.isSafeInteger(v) && v>=0;
const label={production:'정식 공개',in_review:'심사 중',internal:'내부 테스트',not_created:'미생성 · 주간 한도'};
export function downloadSummary({apps=[],androidApps=[],metrics=[],runtime=[],today=new Date(Date.now()+9*3600e3).toISOString().slice(0,10),metricsError=false}={}) {
  const start=new Date(`${today}T00:00:00Z`);start.setUTCDate(start.getUTCDate()-27);const since=start.toISOString().slice(0,10);
  let snapshot;try{snapshot=JSON.parse(runtime.find(r=>r.id==='google_downloads')?.detail);}catch{}
  if(!snapshot || snapshot.schemaVersion!==1 || snapshot.platform!=='google' || !Array.isArray(snapshot.apps)) snapshot=null;
  const samePeriod=snapshot?.periodStart===since && snapshot?.periodEnd===today;
  const googleRows=androidApps.map(a=>{
    const matches=snapshot?.apps.filter(r=>r.packageId===a.package_id)||[],r=matches.length===1?matches[0]:null;
    const available=Boolean(samePeriod && r?.metric==='installed_users' && count(r.installs));
    return {...a,releaseStatus:r?.status || null,value:available?r.installs:null,complete:available && r.complete===true,sourceStatus:r?.sourceStatus||'uncollected'};
  });
  const registered=googleRows.filter(r=>r.releaseStatus!=='not_created');
  const google=registered.some(r=>r.value!==null)?registered.reduce((s,r)=>s+(r.value??0),0):null;
  const appleRows=apps.filter(a=>a.status!=='excluded').map(a=>{
    const rows=metricsError?[]:metrics.filter(r=>r.app_id===a.id && (!r.platform || r.platform==='apple') && r.day>=since && r.day<=today && !/sandbox|test/i.test(r.environment||'') && count(r.downloads));
    const days=new Set(rows.map(r=>r.day));
    return {id:a.id,value:rows.length?rows.reduce((s,r)=>s+r.downloads,0):null,complete:days.size===28};
  });
  const apple=appleRows.some(r=>r.value!==null)?appleRows.reduce((s,r)=>s+(r.value??0),0):null;
  const complete=appleRows.length>0 && appleRows.every(r=>r.complete) && registered.length>0 && registered.every(r=>r.complete);
  return {apple,google,total:complete?apple+google:null,subtotal:apple===null && google===null?null:(apple??0)+(google??0),googleRows,since,today,snapshot,samePeriod};
}
export function renderDownloads(options={}) {
  const s=downloadSummary(options),n=v=>v===null?'집계 대기':`${v.toLocaleString('ko-KR')}건`;
  let sync;try{sync=JSON.parse(options.runtime?.find(r=>r.id==='google_downloads_sync')?.detail);}catch{}
  const syncState=options.runtime?.find(r=>r.id==='google_downloads_sync')?.status;
  const autoLabel=syncState==='configuration_required'?'자동 수집 설정 대기 · Google 보고서 저장소·읽기 권한 확인 필요':syncState==='source_error'||syncState==='connection_error'?'자동 수집 오류 · 이전 수집 결과 유지':s.snapshot?.collectionMode==='automatic_official'?'공식 보고서 자동 수집 · 매일 01:50 / 08:50 KST · 3~7일 반영 지연':'수동 확인 기록 · 자동 수집 미연결';
  const checked=s.snapshot?.observedAt && Number.isFinite(Date.parse(s.snapshot.observedAt))?new Date(s.snapshot.observedAt).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})+' KST':'미확인';
  return `<section class="app-downloads" aria-label="스토어 다운로드 합산"><h3 class="app-sub">다운로드 · 두 스토어 합산</h3><p><b>${s.total===null?'전체 합계 미확정':n(s.total)}</b> · 수집분 소계 ${n(s.subtotal)} · Apple ${n(s.apple)} / Google ${n(s.google)}</p><p class="panel-note">최근 28일 ${esc(s.since)} ~ ${esc(s.today)} · Apple 다운로드 + Google 설치 사용자 집계 건수의 합이며 고유 사용자 수가 아닙니다. 같은 기간의 양쪽 보고서가 완전할 때만 전체 합계를 확정합니다. 미수집은 0이 아닙니다.</p><p>Google 공식 화면 확인: ${esc(checked)} · ${esc(autoLabel)}${s.snapshot && !s.samePeriod?' · 저장된 집계 기간이 현재 기간과 달라 수치는 합산에서 제외':''}</p><div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>Google 앱</th><th>출시 상태</th><th>최근 28일 설치 사용자 수</th><th>집계 상태</th></tr></thead><tbody>${s.googleRows.map(r=>`<tr><td><b>${esc(r.name)}</b><small>${esc(r.package_id)}</small></td><td>${esc(label[r.releaseStatus]||'미확인')}</td><td>${r.releaseStatus==='not_created'?'해당 없음':n(r.value)}</td><td>${esc(r.sourceStatus==='partial_report'?'공식 보고서 일부 수집 · 반영 대기':r.sourceStatus==='waiting_report'?'공식 설치 보고서 생성 대기':r.sourceStatus==='quota_blocked'?'앱 미생성':r.complete?'공식 집계 확인':'미수집 · 확인 필요')}</td></tr>`).join('')}</tbody></table></div><p class="panel-note">Google 저장 기간: ${esc(s.snapshot?.periodStart||'미확인')} ~ ${esc(s.snapshot?.periodEnd||'미확인')} · <a href="https://play.google.com/console/u/0/developers/7870440470636306408/download-reports/statistics" target="_blank" rel="noopener">공식 설치 보고서 확인 ↗</a></p></section>`;
}
