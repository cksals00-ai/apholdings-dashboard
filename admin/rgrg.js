// 알지알지오알지 탭 — 문제은행 반입·탈락 관측 화면
//
// 읽기 전용이다. 문항을 고치거나 내리는 일은 파이프라인(tools/bank/export_admin.py)에서 하고,
// 이 화면은 그 결과물인 정적 JSON 하나(/admin/rgrg-bank.json)만 읽는다.
// quizarena Supabase 프로젝트는 이 관리자 로그인 세션과 다른 프로젝트라
// 브라우저에서 안전하게 쓸 수 없다 — 그래서 db 핸들을 아예 받지 않는다.
const SRC = '/admin/rgrg-bank.json';

const esc = (s = '') => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const safeUrl = v => { try { const u = new URL(v); return ['https:', 'http:'].includes(u.protocol) && !u.username && !u.password ? u.href : ''; } catch { return ''; } };
const link = (url, label) => safeUrl(url) ? `<a href="${esc(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>` : esc(label);
const num = n => n == null || Number.isNaN(Number(n)) ? '—' : Number(n).toLocaleString('ko-KR');
const day = s => s ? new Intl.DateTimeFormat('ko-KR', { month: 'numeric', day: 'numeric', weekday: 'short', timeZone: 'Asia/Seoul' }).format(new Date(String(s).length === 10 ? s + 'T00:00:00+09:00' : s)) : '미정';
const stamp = s => s ? new Intl.DateTimeFormat('ko-KR', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Seoul' }).format(new Date(s)) : '';

// 앱의 QuizCategory 와 같은 이름을 쓴다. 모르는 키는 지우지 않고 원문 그대로 보여 준다 —
// 파이프라인이 주제를 하나 더 늘렸을 때 화면에서 조용히 사라지면 안 된다.
const CAT = { nonsense: '넌센스', elementary: '초등', middle: '중등', high: '고등', certification: '자격증', koreanHistory: '한국사', language: '어학', vocabulary: '영단어', general: '상식', idol: '아이돌' };
const catName = k => CAT[k] || String(k ?? '미분류');

// 사지선다에서 「제일 긴 보기」를 찍었을 때 맞을 확률. 25%가 아니면 보기 길이가 정답을 알려 주고 있다는 뜻.
const BIAS_BASE = 25;
// null 은 「아직 재지 않았다」는 뜻이다. 숫자로 바꾸면 0%가 되어 멀쩡한 주제를 빨갛게 칠한다.
const fin = v => v == null || v === '' || !Number.isFinite(Number(v)) ? null : Number(v);
const biasLevel = v => { const n = fin(v); if (n == null) return 'na'; const d = Math.abs(n - BIAS_BASE); return d <= 2 ? 'ok' : d <= 5 ? 'warn' : 'bad'; };
const biasBadge = v => { const n = fin(v); return n == null ? '<span class="rg-bias" data-level="na">—</span>' : `<span class="rg-bias" data-level="${biasLevel(n)}">${n.toFixed(1)}%</span>`; };

// 은행 총량 추이 — 눈금 없는 선 하나. 숫자는 아래 표에 그대로 있으니 여기선 방향만 본다.
function spark(points) {
  if (points.length < 2) return '';
  const vals = points.map(p => p.v), lo = Math.min(...vals), hi = Math.max(...vals), span = hi - lo || 1;
  const W = 100, H = 28;
  const xy = points.map((p, i) => [i / (points.length - 1) * W, H - (p.v - lo) / span * (H - 4) - 2]);
  const d = xy.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
  const [lx, ly] = xy[xy.length - 1];
  return `<svg class="rg-spark" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none" role="img" aria-label="은행 총량 ${num(lo)} → ${num(hi)}"><path d="${d}" fill="none" stroke="currentColor" stroke-width="1.6" vector-effect="non-scaling-stroke"/><circle cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="2"/></svg>`;
}

export function createRgrg(getUser) {
  const root = document.querySelector('#rgrg-section');
  let data = null, state = 'idle', loaded = false, gen = 0;
  root.innerHTML = `<p id="rg-message" class="form-message" role="status" aria-live="polite"></p><div id="rg-body"></div>`;
  const $ = s => root.querySelector(s), msg = s => { $('#rg-message').textContent = s; };

  async function load(force = false) {
    if (!getUser()) return;
    if (loaded && !force) { render(); return; }
    const t = ++gen; msg('문제은행 자료를 불러오는 중…');
    try {
      // 파이프라인이 같은 경로를 덮어쓰므로 캐시를 쓰면 어제 숫자를 보게 된다.
      const res = await fetch(SRC, { cache: 'no-store' });
      if (t !== gen) return;
      if (res.status === 404) { data = null; state = 'none'; }
      else if (!res.ok) { data = null; state = 'error'; }
      else { data = await res.json(); state = 'ok'; }
      if (t !== gen) return;
    } catch { if (t !== gen) return; data = null; state = 'error'; }
    loaded = true; msg(''); render();
  }
  function clear() { gen++; data = null; state = 'idle'; loaded = false; $('#rg-body').innerHTML = ''; msg(''); }

  // ── 자료 정리 ──
  const ledgerAsc = () => [...(data?.ledger || [])].sort((a, b) => String(a.date || '').localeCompare(String(b.date || '')));
  const rejected = () => data?.rejected || [];
  const recent = () => data?.recent || [];
  function catKeys() {
    const keys = new Set(Object.keys(data?.categories || {}));
    recent().forEach(q => keys.add(q.category));
    rejected().forEach(r => keys.add(r.category));
    return [...keys].filter(Boolean);
  }

  function readOnlyNote() {
    return '<p class="rg-note">이 화면은 읽기 전용입니다 · 문항을 내리거나 고치는 일은 파이프라인에서 합니다.</p>';
  }

  function render() {
    if (state === 'ok' && data) { renderShell(); paintRejected(); paintBank(); return; }
    const line = state === 'error'
      ? '자료를 불러오지 못했습니다. 잠시 뒤 다시 시도하거나 파이프라인 게시 상태를 확인하세요.'
      : '아직 올라온 자료가 없습니다.';
    $('#rg-body').innerHTML = `<section class="panel"><div class="panel-head"><div><p class="eyebrow">RGRG · 문제은행</p><h2>알지알지오알지 문제은행</h2></div><button class="secondary" type="button" data-rg="refresh">↻ 다시 불러오기</button></div>
      ${readOnlyNote()}<p class="empty">${esc(line)}</p>
      <p class="panel-note">파이프라인이 <code>/admin/rgrg-bank.json</code> 을 올리면 반입 현황·탈락 사유·은행 검색이 여기에 나타납니다.</p></section>`;
  }

  function renderShell() {
    const asc = ledgerAsc(), last = asc[asc.length - 1], prev = asc[asc.length - 2];
    const bank = data.bankSize ?? last?.bankSize;
    const rate = last && (last.accepted + last.rejected) ? last.rejected / (last.accepted + last.rejected) * 100 : null;
    const bias = data.longestChoiceBias?.overall;
    const kpis = [
      ['은행 총량', num(bank), last?.date ? day(last.date) + ' 기준' : '', ''],
      ['최근 반입 · 통과', num(last?.accepted), last ? `들어옴 ${num((last.accepted || 0) + (last.rejected || 0))}건 중` : '반입 기록 없음', ''],
      ['최근 반입 · 탈락', num(last?.rejected), rate == null ? '' : `탈락률 ${rate.toFixed(1)}%`, rate != null && rate >= 20 ? 'alert' : ''],
      ['긴 선택지 찍기', fin(bias) == null ? '—' : fin(bias).toFixed(1) + '%', '25%가 정상 · 멀어지면 보기 길이가 정답을 알려 줍니다', biasLevel(bias) === 'bad' ? 'alert' : ''],
    ];

    const rows = [...asc].reverse().map((r, i, arr) => {
      const before = arr[i + 1];
      const delta = before && Number.isFinite(r.bankSize) && Number.isFinite(before.bankSize) ? r.bankSize - before.bankSize : null;
      const got = (r.accepted || 0) + (r.rejected || 0);
      const rr = got ? (r.rejected || 0) / got * 100 : null;
      const files = Object.entries(r.files || {}).map(([name, v]) =>
        `<small class="rg-file"><b>${esc(name)}</b> ${Object.entries(v || {}).map(([k, n]) => `${esc(k)} ${num(n)}`).join(' · ')}</small>`).join('');
      return `<tr><td class="date"><b>${esc(r.date || '')}</b><br><small>${esc(day(r.date))}</small></td>
        <td class="num">${num(got)}</td><td class="num">${num(r.accepted)}</td>
        <td class="num${rr != null && rr >= 20 ? ' rg-hot' : ''}">${num(r.rejected)}${rr == null ? '' : `<small> ${rr.toFixed(1)}%</small>`}</td>
        <td class="num">${num(r.bankSize)}${delta == null ? '' : `<small class="rg-delta">${delta >= 0 ? '+' : ''}${num(delta)}</small>`}</td>
        <td class="rg-files">${files || '<small class="rg-file">파일 내역 없음</small>'}</td></tr>`;
    }).join('');

    const dist = Object.entries(data.categories || {}).sort((a, b) => (b[1] || 0) - (a[1] || 0));
    const distMax = Math.max(1, ...dist.map(([, v]) => v || 0));
    const distTotal = dist.reduce((s, [, v]) => s + (v || 0), 0);
    const byCat = data.longestChoiceBias?.byCategory || {};

    const dups = data.crossSubjectDuplicates || [];
    const cats = catKeys();
    const catOptions = cats.map(k => `<option value="${esc(k)}">${esc(catName(k))}</option>`).join('');
    const rejDates = [...new Set(rejected().map(r => r.date).filter(Boolean))].sort().reverse();

    $('#rg-body').innerHTML = `
      <div class="co-hero rg-hero"><div><p class="eyebrow">RGRG · QUESTION BANK</p><h2>알지알지오알지 문제은행</h2>
        <p>파이프라인이 CSV를 읽어 은행에 넣은 결과입니다. 떨어진 문항과 그 사유를 보고 CSV 만드는 쪽을 고칩니다.</p>
        <p class="panel-note">자료 생성 ${esc(stamp(data.generatedAt) || '시각 미기재')}</p></div>
        <div class="co-toolbar"><button class="secondary" type="button" data-rg="refresh">↻ 새로고침</button></div></div>
      ${readOnlyNote()}

      <div class="app-kpis k4 viz-kpis">${kpis.map(([l, v, d, c]) => `<article class="app-kpi ${c}"><span>${esc(l)}</span><b>${esc(v)}</b><small>${esc(d)}</small></article>`).join('')}</div>

      <section class="panel panel-wide rg-panel">
        <div class="panel-head"><div><p class="eyebrow">INTAKE · 반입 현황</p><h2>며칠 동안 몇 개가 들어와 몇 개가 붙었나</h2></div>
          <span class="rg-trend">${spark(asc.filter(r => Number.isFinite(r.bankSize)).map(r => ({ v: r.bankSize })))}<small>은행 총량 추이${prev && Number.isFinite(last?.bankSize) && Number.isFinite(prev?.bankSize) ? ` · 마지막 ${last.bankSize - prev.bankSize >= 0 ? '+' : ''}${num(last.bankSize - prev.bankSize)}` : ''}</small></span></div>
        <p class="panel-note">「들어옴」은 통과와 탈락을 합한 수입니다. 파일별 내역은 파이프라인이 적은 숫자를 그대로 옮겼습니다.</p>
        <div class="asset-table-wrap"><table class="asset-table rg-ledger"><thead><tr><th>날짜</th><th class="num">들어옴</th><th class="num">통과</th><th class="num">탈락</th><th class="num">은행 총량</th><th>파일별</th></tr></thead>
          <tbody>${rows || '<tr><td colspan="6" class="empty">반입 기록이 아직 없습니다.</td></tr>'}</tbody></table></div>
      </section>

      <section class="panel panel-wide rg-panel rg-rej">
        <div class="panel-head"><div><p class="eyebrow">REJECTED · 떨어진 문항과 사유</p><h2>왜 떨어졌나</h2></div><span id="rg-rej-count" class="panel-note"></span></div>
        <p class="panel-note">사유는 파이프라인이 적은 문장을 고치지 않고 그대로 옮깁니다. 같은 사유가 반복되면 CSV 만드는 쪽을 고칠 자리입니다.</p>
        <div class="asset-filters rg-filters">
          <label>날짜<select id="rg-rej-date"><option value="ALL">전체 날짜</option>${rejDates.map(d => `<option value="${esc(d)}">${esc(d)}</option>`).join('')}</select></label>
          <label>주제<select id="rg-rej-cat"><option value="ALL">전체 주제</option>${catOptions}</select></label>
          <label>파일<select id="rg-rej-file"><option value="ALL">전체 파일</option>${[...new Set(rejected().map(r => r.file).filter(Boolean))].sort().map(f => `<option value="${esc(f)}">${esc(f)}</option>`).join('')}</select></label>
          <label class="search-field">검색<input id="rg-rej-q" type="search" placeholder="지문 · 사유 · 문항 ID"></label>
        </div>
        <div class="asset-table-wrap"><table class="asset-table rg-rej-table"><thead><tr><th>날짜</th><th>출처</th><th>주제</th><th>지문</th><th>떨어진 사유</th></tr></thead>
          <tbody id="rg-rej-rows"></tbody></table></div>
      </section>

      <section class="panel panel-wide rg-panel">
        <div class="panel-head"><div><p class="eyebrow">SEARCH · 은행 검색</p><h2>최근 추가분에서 찾기</h2></div><span id="rg-bank-count" class="panel-note"></span></div>
        <p class="panel-note">최근 추가분 ${num(recent().length)}문항 안에서만 찾습니다. 은행 전체 ${num(bank)}문항은 JSON 크기 때문에 담지 않습니다 — 전체 검색은 파이프라인에서 하세요.</p>
        <div class="asset-filters rg-filters rg-filters-2">
          <label>주제<select id="rg-bank-cat"><option value="ALL">전체 주제</option>${catOptions}</select></label>
          <label class="search-field">검색<input id="rg-bank-q" type="search" placeholder="지문 · 보기 글자"></label>
        </div>
        <div id="rg-bank-rows"></div>
      </section>

      <section class="panel rg-panel">
        <div class="panel-head"><div><p class="eyebrow">DISTRIBUTION · 주제별</p><h2>어느 주제가 비어 있나</h2></div><span class="panel-note">합계 ${num(distTotal)}문항</span></div>
        <div class="asset-table-wrap"><table class="asset-table rg-dist"><thead><tr><th>주제</th><th class="num">문항</th><th>비중</th><th class="num">긴 선택지 찍기</th></tr></thead>
          <tbody>${dist.map(([k, v]) => `<tr${!v ? ' class="retired"' : ''}><td><b>${esc(catName(k))}</b> <small>${esc(k)}</small></td><td class="num">${num(v)}</td>
            <td><span class="progress-track"><span class="progress-bar" style="width:${Math.round((v || 0) / distMax * 100)}%"></span></span></td>
            <td class="num">${biasBadge(byCat[k])}</td></tr>`).join('') || '<tr><td colspan="4" class="empty">주제별 숫자가 아직 없습니다.</td></tr>'}</tbody></table></div>
        <p class="panel-note">「긴 선택지 찍기」는 보기 중 가장 긴 것을 고르면 맞는 비율입니다. 25%에서 멀면 그 주제의 보기 길이가 정답을 알려 주고 있습니다.</p>
      </section>

      <details class="panel rg-panel rg-dups"${dups.length ? ' open' : ''}><summary>주제가 다른 중복 ${num(dups.length)}건</summary>
        ${dups.length ? `<ul class="rg-dup-list">${dups.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
          <p class="panel-note">같은 문항이 학년만 달리해 두 번 들어간 경우입니다. 어느 쪽을 남길지는 파이프라인에서 정합니다.</p>`
        : '<p class="panel-note">주제가 다른 중복은 없습니다.</p>'}</details>`;
  }

  // ── 탈락분 표 (필터가 바뀌어도 입력 칸의 초점을 잃지 않게 tbody만 다시 그린다) ──
  function paintRejected() {
    const box = $('#rg-rej-rows'); if (!box) return;
    const d = $('#rg-rej-date').value, c = $('#rg-rej-cat').value, f = $('#rg-rej-file').value;
    const q = $('#rg-rej-q').value.trim().toLowerCase();
    const list = rejected().filter(r =>
      (d === 'ALL' || r.date === d) && (c === 'ALL' || r.category === c) && (f === 'ALL' || r.file === f) &&
      (!q || [r.prompt, r.sourceID, ...(r.reasons || [])].join(' ').toLowerCase().includes(q)));
    $('#rg-rej-count').textContent = `${num(list.length)}건 표시 · 전체 ${num(rejected().length)}건`;
    box.innerHTML = list.map(r => `<tr>
      <td class="date">${esc(r.date || '')}</td>
      <td class="rg-src"><b>${esc(r.file || '')}</b><small>${r.line == null ? '' : `${num(r.line)}줄`}${r.sourceID ? ` · ${esc(r.sourceID)}` : ''}</small></td>
      <td>${esc(catName(r.category))}</td>
      <td class="rg-prompt">${esc(r.prompt || '')}</td>
      <td><ul class="rg-reasons">${(r.reasons || []).map(x => `<li>${esc(x)}</li>`).join('') || '<li class="rg-reason-none">사유 미기재</li>'}</ul></td></tr>`).join('')
      || `<tr><td colspan="5" class="empty">${rejected().length ? '조건에 맞는 탈락 문항이 없습니다.' : '떨어진 문항이 없습니다.'}</td></tr>`;
  }

  // ── 은행 검색 결과 ──
  function paintBank() {
    const box = $('#rg-bank-rows'); if (!box) return;
    const c = $('#rg-bank-cat').value, q = $('#rg-bank-q').value.trim().toLowerCase();
    const list = recent().filter(x =>
      (c === 'ALL' || x.category === c) &&
      (!q || [x.prompt, x.explanation, ...(x.choices || [])].join(' ').toLowerCase().includes(q)));
    $('#rg-bank-count').textContent = `${num(list.length)}문항 표시 · 최근 추가분 ${num(recent().length)}문항`;
    if (!list.length) { box.innerHTML = `<p class="empty">${recent().length ? '조건에 맞는 문항이 없습니다.' : '최근 추가분이 아직 없습니다.'}</p>`; return; }
    box.innerHTML = `<div class="asset-table-wrap"><table class="asset-table rg-bank"><thead><tr><th>주제</th><th>문항</th><th class="num">난이도</th><th>추가</th></tr></thead><tbody>${list.map(x => `<tr>
      <td><b>${esc(catName(x.category))}</b><small class="rg-id">${esc(x.id || '')}</small></td>
      <td class="rg-qcell"><b>${esc(x.prompt || '')}</b>
        <ol class="rg-choices">${(x.choices || []).map((ch, i) => `<li${i === x.answerIndex ? ' class="on"' : ''}>${esc(ch)}</li>`).join('')}</ol>
        ${x.explanation ? `<small class="rg-exp">${esc(x.explanation)}</small>` : ''}
        ${x.source ? `<small class="rg-exp">${link(x.source, '출처')}</small>` : ''}</td>
      <td class="num">${fin(x.difficulty) == null ? '—' : fin(x.difficulty).toFixed(2)}</td>
      <td class="date">${esc(x.addedOn || '')}</td></tr>`).join('')}</tbody></table></div>`;
  }

  root.addEventListener('click', e => {
    if (e.target.closest('[data-rg="refresh"]')) load(true);
  });
  root.addEventListener('input', e => {
    const id = e.target.id;
    if (['rg-rej-date', 'rg-rej-cat', 'rg-rej-file', 'rg-rej-q'].includes(id)) paintRejected();
    else if (['rg-bank-cat', 'rg-bank-q'].includes(id)) paintBank();
  });

  return { load, clear };
}
