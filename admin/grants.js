// 지원사업 탭 — admin_grants / admin_grant_steps (owner-only RLS)
const esc = (s = '') => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const safeUrl = v => { try { const u = new URL(v); return ['https:', 'http:'].includes(u.protocol) && !u.username && !u.password ? u.href : ''; } catch { return ''; } };
const link = (url, label) => safeUrl(url) ? `<a href="${esc(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>` : '';
const STATUS = { watching: '검토', preparing: '준비 중', submitted: '제출 완료', screening: '평가 중', selected: '선정', rejected: '미선정', dropped: '중단' };
const STEP = { todo: '할 일', doing: '진행 중', done: '완료', blocked: '막힘', skipped: '생략' };
const NEXT = { todo: 'doing', doing: 'done', done: 'todo', blocked: 'doing', skipped: 'todo' };
const fmt = s => s ? new Intl.DateTimeFormat('ko-KR', { month: 'numeric', day: 'numeric', weekday: 'short', hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Seoul' }).format(new Date(s)) : '미정';
const kstDay = d => new Date(new Date(d).toLocaleString('en-US', { timeZone: 'Asia/Seoul' })).setHours(0, 0, 0, 0);
function dday(s) { if (!s) return { label: '마감 미정', tone: 'muted' }; const ms = Date.parse(s) - Date.now(); if (ms < 0) return { label: '마감', tone: 'muted' }; const d = Math.round((kstDay(s) - kstDay(Date.now())) / 864e5); return { label: d === 0 ? 'D-DAY' : `D-${d}`, tone: d <= 3 ? 'red' : d <= 7 ? 'amber' : 'blue', hours: Math.floor(ms / 36e5) }; }

export function createGrants(db, getUser) {
  const root = document.querySelector('#grants-section');
  let grants = [], steps = [], loaded = false, gen = 0, busy = false;
  root.innerHTML = `<div class="gr-toolbar"><p class="panel-note">클레어가 진행하고, 대표님 몫은 <b>대표</b> 표시로 구분해요. 단계 상태를 누르면 바뀌어요.</p><button class="secondary" data-gr="refresh" type="button">↻ 새로고침</button></div><p id="gr-message" class="form-message" role="status" aria-live="polite"></p><div id="gr-list"></div>`;
  const $ = s => root.querySelector(s), msg = s => { $('#gr-message').textContent = s; };
  async function load(force = false) {
    if (!getUser()) return; if (loaded && !force) { render(); return; }
    const t = ++gen; msg('불러오는 중…');
    try {
      const [a, b] = await Promise.all([db.from('admin_grants').select('*').order('sort').order('deadline_at'), db.from('admin_grant_steps').select('*').order('sort')]);
      if (a.error || b.error) throw a.error || b.error; if (t !== gen) return;
      grants = a.data; steps = b.data; loaded = true; msg(''); render();
    } catch { if (t === gen) msg('불러오지 못했어요. 로그인과 연결 상태를 확인하세요.'); }
  }
  function clear() { gen++; grants = []; steps = []; loaded = false; $('#gr-list').innerHTML = ''; msg(''); }
  function render() {
    $('#gr-list').innerHTML = grants.map(g => {
      const list = steps.filter(s => s.grant_id === g.id).sort((a, b) => (a.sort ?? 0) - (b.sort ?? 0));
      const done = list.filter(s => ['done', 'skipped'].includes(s.status)).length, pct = list.length ? Math.round(done / list.length * 100) : 0;
      const d = dday(g.deadline_at), now = Date.now();
      const mine = list.filter(s => s.owner === '대표' && !['done', 'skipped'].includes(s.status));
      const nextMine = mine[0];
      const rows = list.map(s => {
        const late = s.due_at && Date.parse(s.due_at) < now && !['done', 'skipped'].includes(s.status);
        return `<li class="gr-step" data-status="${esc(s.status)}"><button class="gr-state" data-gr="step" data-id="${esc(s.id)}" type="button" aria-label="${esc(s.title)} 상태: ${STEP[s.status]} — 눌러서 변경">${s.status === 'done' ? '✓' : s.status === 'doing' ? '◐' : s.status === 'blocked' ? '!' : ''}</button><div class="gr-step-body"><div class="gr-step-top"><span class="gr-owner" data-owner="${esc(s.owner)}">${esc(s.owner)}</span>${s.critical ? '<span class="gr-critical">필수·급함</span>' : ''}<b>${esc(s.title)}</b></div>${s.note ? `<p>${esc(s.note)}</p>` : ''}</div><time class="${late ? 'late' : ''}">${late ? '지남 · ' : ''}${fmt(s.due_at)}</time></li>`;
      }).join('');
      return `<article class="panel gr-card"><header class="gr-head"><div><p class="eyebrow">GRANT · ${esc(STATUS[g.status] || g.status)}</p><h2>${esc(g.name)}</h2><p class="gr-track">${esc(g.track)}</p></div><div class="gr-dday" data-tone="${d.tone}"><b>${d.label}</b><span>마감 ${fmt(g.deadline_at)}</span></div></header>
        <div class="gr-kpis"><div><span>지원 규모</span><b>${esc(g.amount_note)}</b></div><div><span>진행</span><b>${done}/${list.length} 단계 · ${pct}%</b><span class="progress-track"><span class="progress-bar" style="width:${pct}%"></span></span></div><div><span>대표님 차례</span><b>${nextMine ? esc(nextMine.title) : '지금은 없음'}</b>${nextMine ? `<span class="gr-due">${fmt(nextMine.due_at)}까지</span>` : ''}</div></div>
        ${g.risk ? `<div class="gr-risk"><b>⚠ 먼저 풀어야 할 것</b><p>${esc(g.risk)}</p></div>` : ''}
        <ol class="gr-steps">${rows}</ol>
        <details class="gr-more"><summary>공고 요약 · 문의처 · 링크</summary><p>${esc(g.program)}</p><p>${esc(g.agency)}</p><p>${esc(g.summary)}</p><p>${esc(g.contact)}</p><p class="gr-links">${link(g.notice_url, '공고 원문')}${link(g.apply_url, 'K-Startup 신청')}</p><p class="panel-note">최종 확인 ${fmt(g.updated_at)}</p></details></article>`;
    }).join('') || '<p class="empty">진행 중인 지원사업이 없어요.</p>';
  }
  async function cycle(id) {
    if (busy || !getUser()) return; const s = steps.find(x => x.id === id); if (!s) return;
    const next = NEXT[s.status] || 'todo', prev = s.status; busy = true; s.status = next; render();
    const { error } = await db.from('admin_grant_steps').update({ status: next, updated_at: new Date().toISOString() }).eq('id', id);
    busy = false; if (error) { s.status = prev; render(); msg('저장하지 못했어요.'); } else msg(`「${s.title}」 → ${STEP[next]}`);
  }
  root.addEventListener('click', e => { const b = e.target.closest('[data-gr]'); if (!b) return; if (b.dataset.gr === 'refresh') load(true); else if (b.dataset.gr === 'step') cycle(b.dataset.id); });
  return { load, clear };
}
