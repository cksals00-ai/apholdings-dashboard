// Verified setup snapshot; this card does not query GA4 or install a tracking tag.
export function renderWebAnalytics() {
  const sites = [
    ['AP 메인', 'www.apholdings.kr', '원본 확인 · 설치 대기'],
    ['교육', 'edu.apholdings.kr', '원본 확인 · 설치 대기'],
    ['게임', 'games.apholdings.kr', '원본 확인 · 설치 대기'],
    ['Lia Select 쇼핑', 'shop.apholdings.kr', '현재 배포 경로 확인 중'],
    ['코트메이트', 'sports.apholdings.kr', '현재 배포 경로 확인 중'],
  ];
  return `<section class="panel panel-wide" id="mk-web-analytics" aria-label="홈페이지 성과 분석">
    <div class="panel-head"><div><p class="eyebrow">WEBSITE ANALYTICS · GA4</p><h2>홈페이지 성과 분석</h2></div><span class="status-pill">사이트 태그 설치 전</span></div>
    <p class="panel-note">2026-10-29 확인한 설정 현황입니다. 실시간 상태가 아니며, 통계 자동 연동 전입니다.</p>
    <p>AP Holdings 계정과 ‘AP Holdings 웹사이트’ 속성 생성 완료. 한국 시간·원화 기준이며 추가 데이터 공유와 향상된 측정을 껐습니다. 아직 사이트에 태그를 설치하지 않아 방문·조회·유입 성과는 미확인입니다.</p>
    <div class="co-toolbar" style="margin:14px 0"><a class="secondary" href="https://analytics.google.com/analytics/web/#/a413956552p561381925/reports/intelligenthome" target="_blank" rel="noopener noreferrer">GA4 보고서 열기 ↗</a><a class="secondary" href="https://blog.naver.com/cksals00/224457592380" target="_blank" rel="noopener noreferrer">코트메이트 소개 글 ↗</a></div>
    <div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>사이트</th><th>주소</th><th>설치 상태</th><th>방문·조회</th></tr></thead><tbody>${sites.map(([name, host, status]) => `<tr><td>${name}</td><td>${host}</td><td>${status}</td><td>수집 전 · 미확인</td></tr>`).join('')}</tbody></table></div>
    <details style="margin-top:16px"><summary>소개 글 유입 측정 준비</summary><p>전용 링크 교체 전입니다. 예정 캠페인: <code>courtmate_intro_20261029</code> · 출처: naver · 매체: blog · 글 번호: 224457592380.</p><p>태그 설치·전용 링크 적용·테스트 유입 검증 후부터 집계합니다. 블로그 조회수와 코트메이트 도착 수는 별개이며, 과거 유입을 소급해 계산하지 않습니다. 쿠키 없는 최소 수집 조건을 유지하고, 관리자·개인정보 입력 화면은 측정 대상에서 제외합니다.</p></details>
    <p class="panel-note">다음 단계: 배포 경로 확인 → 최소 수집 코드·개인정보 안내 반영 → 사이트별 실제 수신 확인 → 관리자 통계 자동 연동. 현재 화면은 설정 요약이며 성과 수치를 자동 조회하지 않습니다.</p>
  </section>`;
}
