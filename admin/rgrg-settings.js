// 알지알지 게임 설정 — 지금 게임이 실제로 쓰는 규칙을 한눈에. (2026-10-02 대표 지시)
//
// 읽기 전용이다. 숫자는 이 파일에 없다 — QuizArena 의 tools/parity/export_admin_settings.mjs 가
// **서버 함수(settle-match·start-match)를 그대로 불러** 낸 값을 /admin/rgrg-settings.json 으로 굽고,
// 이 화면은 그 파일만 읽는다. 화면이 숫자를 따로 들고 있으면 언젠가 게임과 어긋난다.
// 값을 바꾸는 일은 앱·서버·안드로이드 세 곳을 같이 고쳐야 해서(점수가 어긋나면 부정행위로 보인다)
// 여기서 직접 하지 않는다.
const SRC = '/admin/rgrg-settings.json';

const esc = (s = '') => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const num = n => n == null || Number.isNaN(Number(n)) ? '—' : Number(n).toLocaleString('ko-KR');
const sec = n => n == null ? '—' : `${Number(n) % 1 === 0 ? Number(n) : Number(n).toFixed(1)}초`;
const stamp = s => s ? new Intl.DateTimeFormat('ko-KR', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Seoul' }).format(new Date(s)) : '';
const mmss = s => { const m = Math.floor(s / 60), r = Math.round(s % 60); return `${m}분 ${String(r).padStart(2, '0')}초`; };
const CAT = { nonsense: '넌센스', elementary: '초등', middle: '중등', high: '고등', certification: '자격증', koreanHistory: '한국사', language: '어학', vocabulary: '영단어', general: '상식' };
const yes = ok => ok ? '<span class="gs-yes">나옴</span>' : '<span class="gs-no">안 나옴</span>';

export function createRgrgSettings(getUser) {
  const root = document.querySelector('#rgrg-settings-section');
  let data = null, state = 'idle', loaded = false, gen = 0;
  root.innerHTML = `<p id="gs-message" class="form-message" role="status" aria-live="polite"></p><div id="gs-body"></div>`;
  const $ = s => root.querySelector(s), msg = s => { $('#gs-message').textContent = s; };

  async function load(force = false) {
    if (!getUser()) return;
    if (loaded && !force) { render(); return; }
    const t = ++gen; msg('게임 설정을 불러오는 중…');
    try {
      const res = await fetch(SRC, { cache: 'no-store' });
      if (t !== gen) return;
      if (res.status === 404) { data = null; state = 'none'; }
      else if (!res.ok) { data = null; state = 'error'; }
      else { data = await res.json(); state = 'ok'; }
    } catch { if (t !== gen) return; data = null; state = 'error'; }
    loaded = true; msg(''); render();
  }
  function clear() { gen++; data = null; state = 'idle'; loaded = false; $('#gs-body').innerHTML = ''; msg(''); }

  function render() {
    const body = $('#gs-body');
    if (state !== 'ok' || !data) {
      body.innerHTML = `<section class="panel"><p class="panel-note">${state === 'error'
        ? '게임 설정을 불러오지 못했습니다. 잠시 뒤 다시 시도하세요.'
        : '아직 게임 설정 자료가 올라오지 않았습니다 (/admin/rgrg-settings.json).'}</p></section>`;
      return;
    }
    const rounds = data.rounds || [], rooms = data.rooms || [], abilities = data.abilities || [], age = data.age || [];
    const main = rounds.find(r => r.kind === 'main');
    const peek = abilities.find(a => a.ability === 'peek');
    const mid = main?.byDifficulty?.find(d => d.label === '보통');

    body.innerHTML = `
      <div class="app-kpis k4 gs-kpis">
        <div class="app-kpi"><span>버저 잡은 뒤 답 창</span><b>${sec(main?.answerSeconds)}</b><small>스피드 ${sec(rounds.find(r => r.kind === 'warmup')?.answerSeconds)} · 파이널 ${sec(rounds.find(r => r.kind === 'betting')?.answerSeconds)}</small></div>
        <div class="app-kpi"><span>부저 오답 감점</span><b>배점 그대로</b><small>본게임 보통 ${num(mid?.points)}점 → −${num(mid?.penalty)}</small></div>
        <div class="app-kpi"><span>보기</span><b>잡아야 열림</b><small>투시 ${peek ? `${peek.byTier[0]}~${peek.byTier[peek.byTier.length - 1]}초` : '—'} 엿보기</small></div>
        <div class="app-kpi"><span>나이에 맞는 문항</span><b>${age.length}칸</b><small>가장 어린 사람 기준</small></div>
      </div>

      <section class="panel">
        <div class="panel-head"><div><p class="eyebrow">ROUNDS</p><h2>라운드별 규칙</h2></div><span class="panel-note">기준 ${esc(stamp(data.generatedAt))}</span></div>
        <div class="asset-table-wrap"><table class="asset-table gs-table">
          <thead><tr><th>라운드</th><th>보기</th><th>잡은 뒤 답 창</th>${(rounds[0]?.byDifficulty || []).map(d => `<th class="num">${esc(d.label)}<small>배점 / 감점</small></th>`).join('')}<th class="num">모르고 찍으면<small>보통 기댓값</small></th><th>앱 안내 문구</th></tr></thead>
          <tbody>${rounds.map(r => {
            const m = r.byDifficulty.find(d => d.label === '보통');
            return `<tr>
              <td><b>${esc(r.title)}</b><small class="gs-sub">${r.usesBuzzer ? '부저' : '각자 답함'}</small></td>
              <td>${r.hidesChoices ? '<span class="gs-tag gs-hide">잡아야 열림</span>' : '<span class="gs-tag">처음부터 보임</span>'}</td>
              <td>${r.answerSeconds == null ? '—' : sec(r.answerSeconds)}</td>
              ${r.byDifficulty.map(d => `<td class="num">${num(d.points)} / <span class="gs-pen">${r.kind === 'betting' ? '판돈' : '−' + num(d.penalty)}</span></td>`).join('')}
              <td class="num">${m?.guessEv == null ? '—' : `<span class="${m.guessEv < 0 ? 'gs-pen' : ''}">${m.guessEv > 0 ? '+' : ''}${num(m.guessEv)}</span>`}</td>
              <td class="gs-rule">${esc(r.rule)}</td></tr>`;
          }).join('')}</tbody></table></div>
        <p class="rg-note">찍기 기댓값이 0 이하여야 「모르면 누르지 않는 쪽」이 이득입니다. 부저 라운드는 보기 넷 중 찍기라 배점의 −½, OX 는 각자 답해 0 입니다.</p>
      </section>

      <section class="panel">
        <div class="panel-head"><div><p class="eyebrow">ROOMS</p><h2>방 구성</h2></div></div>
        <div class="asset-table-wrap"><table class="asset-table gs-table">
          <thead><tr><th>방</th><th class="num">정원</th><th>라운드</th><th class="num">한 판</th><th>주제</th></tr></thead>
          <tbody>${rooms.map(r => `<tr>
            <td><b>${esc(r.title)}</b></td><td class="num">${num(r.capacity)}명</td>
            <td>${r.rounds.map(x => `${esc(x.title)} ${num(x.questions)}문항 · ${sec(x.seconds)}`).join('<br>')}</td>
            <td class="num">${mmss(r.totalSeconds)}</td>
            <td class="gs-pool">${(r.pool || []).map(c => esc(CAT[c] || c)).join(' · ')}</td></tr>`).join('')}</tbody></table></div>
      </section>

      <section class="panel">
        <div class="panel-head"><div><p class="eyebrow">ABILITIES</p><h2>캐릭터 능력</h2></div><span class="panel-note">숙련 단계 문턱: ${(data.masteryThresholds || []).map((n, i) => `${i + 1}단 ${num(n)}판`).join(' · ')}</span></div>
        <div class="asset-table-wrap"><table class="asset-table gs-table">
          <thead><tr><th>캐릭터</th><th>능력</th><th>하는 일</th>${[1, 2, 3, 4, 5].map(t => `<th class="num">${t}단</th>`).join('')}<th>점수에 닿나</th></tr></thead>
          <tbody>${abilities.map(a => `<tr>
            <td>${esc(a.character)}</td><td><b class="gs-ability">${esc(a.title)}</b></td><td>${esc(a.what)}</td>
            ${a.byTier.map(n => `<td class="num">${num(n)}</td>`).join('')}
            <td>${a.touchesScore ? '<span class="gs-tag gs-hide">서버도 계산</span>' : '<span class="gs-tag">화면에서만</span>'}</td></tr>`).join('')}</tbody></table></div>
      </section>

      <section class="panel">
        <div class="panel-head"><div><p class="eyebrow">AGE</p><h2>나이에 맞는 문항</h2></div><span class="panel-note">초등·상식·넌센스·한국사·영단어·어학은 누구에게나 나옵니다</span></div>
        <div class="asset-table-wrap"><table class="asset-table gs-table">
          <thead><tr><th>연령대</th><th>중등</th><th>고등</th><th>자격증</th></tr></thead>
          <tbody>${age.map(a => `<tr><td><b>${esc(a.title)}</b></td><td>${yes(a.middle)}</td><td>${yes(a.high)}</td><td>${yes(a.certification)}</td></tr>`).join('')}</tbody></table></div>
        <p class="rg-note">연령대는 Apple 「연령대 공유」(iOS 26) 또는 출생 연도로만 받습니다. 출생 연도는 사용자 기기에만 있고 서버에는 위 네 칸 중 하나만 올라갑니다.</p>
      </section>

      <section class="panel">
        <div class="panel-head"><div><p class="eyebrow">NOTES</p><h2>지금 규칙의 요점</h2></div></div>
        <ul class="gs-notes">${(data.notes || []).map(n => `<li>${esc(n)}</li>`).join('')}</ul>
        <p class="rg-note">이 화면은 읽기 전용입니다 · 숫자는 서버 함수가 실제로 쓰는 값을 그대로 옮겼습니다. 바꾸려면 앱·서버·안드로이드를 함께 고쳐야 하니(어긋나면 점수가 갈립니다) Claude 에게 요청하세요.</p>
      </section>`;
  }

  return { load, clear };
}
