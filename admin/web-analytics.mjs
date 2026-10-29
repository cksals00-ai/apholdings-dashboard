// Verified setup snapshot; this card does not query GA4 or install a tracking tag.
export function renderWebAnalytics() {
  const sites = [
    ['AP 메인', 'www.apholdings.kr', '설치 배포 진행 중'],
    ['교육', 'edu.apholdings.kr', '설치 배포 진행 중'],
    ['게임', 'games.apholdings.kr', '설치 배포 진행 중'],
    ['Lia Select 쇼핑', 'shop.apholdings.kr', '설치 배포 진행 중'],
    ['코트메이트', 'sports.apholdings.kr', '설치 배포 진행 중'],
    ['엔터테인먼트', 'ent.apholdings.kr', '설치 배포 진행 중'],
  ];
  return `<section class="panel panel-wide" id="mk-web-analytics" aria-label="홈페이지 성과 분석">
    <div class="panel-head"><div><p class="eyebrow">WEBSITE ANALYTICS · GA4</p><h2>홈페이지 성과 분석</h2></div><span class="status-pill">사이트 설치 진행 중</span></div>
    <p class="panel-note">2026-10-29 확인한 설정 현황입니다. 설치 상태는 확인 시점 기준이며, 아래 통계는 서버 연결 후 자동 갱신합니다.</p>
    <p>AP Holdings 계정과 ‘AP Holdings 웹사이트’ 속성 생성 완료. 한국 시간·원화 기준이며 추가 데이터 공유와 향상된 측정을 껐습니다. 공개 페이지에 쿠키 없는 측정 코드를 설치하고 있습니다. 아래 통계 연결 결과와 실제 수신 여부를 구분해 확인합니다.</p>
    <div class="co-toolbar" style="margin:14px 0"><a class="secondary" href="https://analytics.google.com/analytics/web/#/a413956552p561381925/reports/intelligenthome" target="_blank" rel="noopener noreferrer">GA4 보고서 열기 ↗</a><a class="secondary" href="https://blog.naver.com/cksals00/224457592380" target="_blank" rel="noopener noreferrer">코트메이트 소개 글 ↗</a></div>
    <div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>사이트</th><th>주소</th><th>설치 상태</th><th>방문·조회</th></tr></thead><tbody>${sites.map(([name, host, status]) => `<tr><td>${name}</td><td>${host}</td><td>${status}</td><td>수집 전 · 미확인</td></tr>`).join('')}</tbody></table></div>
    <div id="mk-ga4-live" aria-live="polite"><p>Google 통계 연결 확인 중…</p></div><details style="margin-top:16px"><summary>소개 글 유입 측정 준비</summary><p>전용 링크 교체 전입니다. 예정 캠페인: <code>courtmate_intro_20261029</code> · 출처: naver · 매체: blog · 글 번호: 224457592380.</p><p>태그 설치·전용 링크 적용·테스트 유입 검증 후부터 집계합니다. 블로그 조회수와 코트메이트 도착 수는 별개이며, 과거 유입을 소급해 계산하지 않습니다. 쿠키 없는 최소 수집 조건을 유지하고, 관리자·개인정보 입력 화면은 측정 대상에서 제외합니다.</p></details>
    <p class="panel-note">페이지 조회와 전용 소개 링크 도착 이벤트만 집계합니다. 설치 테스트 이벤트는 이 보고서에서 제외합니다. 관리자·문의·제보·결제 화면은 측정하지 않습니다.</p>
  </section>`;
}

const escapeMetric = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function renderLiveReport(report) {
  if (!report || !['connected','waiting_data'].includes(report.status)) {
    const states={credentials_required:'Google 통계 읽기 전용 인증 연결 대기',permission_required:'Google 통계 읽기 권한 또는 API 연결 확인 필요',upstream_error:'Google 통계 응답 확인 필요',connection_error:'통계 연결 오류 · 수치 미확인'};
    return `<p>${states[report?.status] || '통계 연결 확인 필요 · 수치 미확인'}</p><p class="panel-note">미연결·오류를 조회 0회로 계산하지 않습니다.</p>`;
  }
  const n=value=>value==null?'집계 대기':`${Number(value).toLocaleString('ko-KR')}건`;
  return `<p><b>최근 28일 전부터 오늘까지 · 한국 시간</b> · 오늘은 집계 중이며 Google 처리 지연이 있을 수 있습니다.</p><p>코트메이트 소개 글 도착: <strong>${n(report.blogArrivals)}</strong> · 반복 도착 포함, 사람 수 아님</p><div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>사이트</th><th>보고된 페이지 조회</th></tr></thead><tbody>${(report.sites||[]).map(s=>`<tr><td>${escapeMetric(s.host)}</td><td>${n(s.views)}</td></tr>`).join('')}</tbody></table></div><p class="panel-note">출처: Google Analytics Data API · 조회 시각 ${escapeMetric(report.checkedAt)} · 관리자 화면 열기·새로고침 및 활성 탭에서 5분마다 갱신. ${report.thresholded?'Google 임계값 적용 · 일부 데이터 제한.':''}${report.sampled?'표본 추정 포함.':''} 미표시 행은 집계 대기로 표시합니다.</p>`;
}
export async function loadWebAnalytics(db, root) {
  const target=root.querySelector('#mk-ga4-live');if(!target)return;
  try {const {data,error}=await db.functions.invoke('web-analytics',{body:{}});target.innerHTML=renderLiveReport(error?{status:'connection_error'}:data);}
  catch {target.innerHTML=renderLiveReport({status:'connection_error'});}
}
