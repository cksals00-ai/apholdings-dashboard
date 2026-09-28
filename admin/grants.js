// 지원사업 탭 — 지원금 유치 전략 + Action Plan 연동
// admin_grant_strategy(1행) · admin_grants(phase/status) · admin_portfolio_items.grant_id
const esc = (s = '') => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const safeUrl = v => { try { const u = new URL(v); return ['https:', 'http:'].includes(u.protocol) && !u.username && !u.password ? u.href : ''; } catch { return ''; } };
const link = (url, label) => safeUrl(url) ? `<a href="${esc(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>` : '';
const STATUS = { watching: '주시', preparing: '준비 중', submitted: '제출 완료', screening: '평가 중', selected: '선정', rejected: '미선정', dropped: '패스' };
const MONEY = { grant: '지원금', loan: '융자', prize: '상금', support: '현물·지원' };
const ACT = { TODO: '할 일', IN_PROGRESS: '진행 중', WAITING: '기다림', ON_HOLD: '보류', CANCELLED: '취소', DONE: '완료' };
const OPEN = s => !['DONE', 'CANCELLED'].includes(s);
const day = s => s ? new Intl.DateTimeFormat('ko-KR', { month: 'numeric', day: 'numeric', weekday: 'short', timeZone: 'Asia/Seoul' }).format(new Date(s.length === 10 ? s + 'T00:00:00+09:00' : s)) : '미정';
const kst = d => new Date(new Date(d).toLocaleString('en-US', { timeZone: 'Asia/Seoul' })).setHours(0, 0, 0, 0);
function dday(s) { if (!s) return ''; const d = Math.round((kst(s) - kst(Date.now())) / 864e5); return d < 0 ? '마감' : d === 0 ? 'D-DAY' : `D-${d}`; }
const today = () => new Date(Date.now() + 9 * 36e5).toISOString().slice(0, 10);

export function createGrants(db, getUser) {
  const root = document.querySelector('#grants-section');
  let strategy = null, grants = [], actions = [], loaded = false, gen = 0, selected = null;
  root.innerHTML = `<p id="gr-message" class="form-message" role="status" aria-live="polite"></p><div id="gr-body"></div>`;
  const $ = s => root.querySelector(s), msg = s => { $('#gr-message').textContent = s; };

  async function load(force = false) {
    if (!getUser()) return; if (loaded && !force) { render(); return; }
    const t = ++gen; msg('불러오는 중…');
    try {
      const [a, b, c] = await Promise.all([
        db.from('admin_grant_strategy').select('*').eq('id', 1).maybeSingle(),
        db.from('admin_grants').select('*').order('sort').order('deadline_at'),
        db.from('admin_portfolio_items').select('*').not('grant_id', 'is', null).order('end_date', { nullsFirst: false }).order('sort_order'),
      ]);
      if (a.error || b.error || c.error) throw a.error || b.error || c.error; if (t !== gen) return;
      strategy = a.data; grants = b.data; actions = c.data; loaded = true; msg(''); render();
    } catch { if (t === gen) msg('불러오지 못했어요. 로그인과 연결 상태를 확인하세요.'); }
  }
  function clear() { gen++; strategy = null; grants = []; actions = []; loaded = false; selected = null; $('#gr-body').innerHTML = ''; msg(''); }
  document.addEventListener('ap:items', () => { if (loaded) load(true); });

  const actsOf = id => actions.filter(a => a.grant_id === id);
  function grantCard(g) {
    const list = actsOf(g.id), done = list.filter(a => !OPEN(a.status)).length, pct = list.length ? Math.round(done / list.length * 100) : 0, dd = dday(g.deadline_at);
    return `<button type="button" class="gr-g${selected === g.id ? ' on' : ''}" data-gr="pick" data-id="${esc(g.id)}" data-status="${esc(g.status)}"><span class="gr-g-top"><span class="gr-money" data-m="${esc(g.money_type || '')}">${esc(MONEY[g.money_type] || '공고')}</span><span class="gr-st">${esc(STATUS[g.status] || g.status)}</span>${dd ? `<b class="gr-dd${/D-[0-7]$|D-DAY/.test(dd) ? ' hot' : ''}">${dd}</b>` : ''}</span><strong>${esc(g.name)}</strong><small>${esc(g.amount_note || '')}</small>${list.length ? `<span class="gr-bar"><span style="width:${pct}%"></span></span><small>Action ${done}/${list.length}</small>` : ''}</button>`;
  }
  function actionRow(a) {
    const late = a.end_date && a.end_date < today() && OPEN(a.status);
    return `<li class="gr-act" data-status="${esc(a.status)}"><button type="button" data-edit="${esc(a.id)}"><span class="gr-owner" data-owner="${/claire/i.test(a.owner_name) ? 'claire' : 'alfred'}">${/claire/i.test(a.owner_name) ? '클레어' : '대표'}</span><span class="gr-act-t"><b>${esc(a.title)}</b>${a.next_action ? `<small>${esc(a.next_action)}</small>` : ''}</span><span class="gr-act-s">${esc(ACT[a.status] || a.status)}</span><time class="${late ? 'late' : ''}">${late ? '지남 · ' : ''}${day(a.end_date)}</time></button></li>`;
  }
  function render() {
    if (!strategy) { $('#gr-body').innerHTML = '<p class="empty">전략이 아직 없어요.</p>'; return; }
    const phases = strategy.phases || [], principles = strategy.principles || [];
    const g = grants.find(x => x.id === selected);
    const open = actions.filter(a => OPEN(a.status)).sort((a, b) => (a.end_date || '9999').localeCompare(b.end_date || '9999'));
    const mine = open.filter(a => !/claire/i.test(a.owner_name));
    const watch = grants.filter(x => !x.phase), dropped = grants.filter(x => x.phase === 'dropped');
    $('#gr-body').innerHTML = `
      <section class="gr-hero panel"><p class="eyebrow">FUNDING STRATEGY · 지원금 유치 전략</p><h2>${esc(strategy.goal)}</h2><p>${esc(strategy.summary || '')}</p>
        <div class="gr-rules">${principles.map((p, i) => `<div><span>${i + 1}</span><b>${esc(p.title)}</b><small>${esc(p.text)}</small></div>`).join('')}</div></section>
      <section class="gr-road">${phases.map(p => { const list = grants.filter(x => x.phase === p.key); return `<div class="gr-phase" data-phase="${esc(p.key)}"><header><b>${esc(p.label)}</b><span>${esc(p.period)}</span></header><p>${esc(p.summary)}</p>${list.map(grantCard).join('') || '<small class="gr-none">등록된 사업 없음</small>'}</div>`; }).join('')}</section>
      ${g ? `<section class="panel gr-detail"><div class="panel-head"><div><p class="eyebrow">${esc(MONEY[g.money_type] || '')} · ${esc(STATUS[g.status] || '')}${g.deadline_at ? ' · 마감 ' + day(g.deadline_at) : ''}</p><h2>${esc(g.name)}</h2></div><div class="top-actions"><button class="primary" type="button" data-gr="add" data-id="${esc(g.id)}">+ Action 추가</button><button class="secondary" type="button" data-gr="pick" data-id="${esc(g.id)}">닫기</button></div></div>
        <p class="gr-sum">${esc(g.summary || '')}</p>${g.risk ? `<div class="gr-risk"><b>⚠ 먼저 풀 것</b><p>${esc(g.risk)}</p></div>` : ''}<p class="gr-links">${link(g.notice_url, '공고·안내')}${g.contact ? `<span>${esc(g.contact)}</span>` : ''}</p>
        <ol class="gr-acts">${actsOf(g.id).map(actionRow).join('') || '<li class="gr-none">연결된 Action이 없어요. 「+ Action 추가」로 Action Plan에 올리세요.</li>'}</ol></section>` : ''}
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">ACTION PLAN 연동</p><h2>지금 할 일</h2></div><span class="panel-note">대표님 몫 ${mine.length}건 · 누르면 Action Plan 편집 창이 열려요</span></div>
        <ol class="gr-acts">${open.slice(0, 12).map(actionRow).join('') || '<li class="gr-none">열린 Action이 없어요.</li>'}</ol></section>
      <details class="panel gr-more"><summary>감시 목록 ${watch.length} · 패스 ${dropped.length}</summary>${[...watch, ...dropped].map(x => `<p><b>${esc(x.name)}</b> · ${esc(STATUS[x.status] || x.status)}${x.deadline_at ? ' · 마감 ' + day(x.deadline_at) : ''}<br><small>${esc(x.risk || x.summary || '')}</small></p>`).join('')}<p class="panel-note">전략 갱신 ${day(strategy.updated_at)} · 감시는 매주 월 09:00 자동</p></details>`;
  }
  root.addEventListener('click', e => {
    const b = e.target.closest('[data-gr]'); if (!b) return;
    if (b.dataset.gr === 'pick') { selected = selected === b.dataset.id ? null : b.dataset.id; render(); root.querySelector('.gr-detail')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
    else if (b.dataset.gr === 'add') { const g = grants.find(x => x.id === b.dataset.id); document.dispatchEvent(new CustomEvent('ap:new-action', { detail: { grantId: b.dataset.id, product: '지원금 유치', title: g ? g.name.split(' ')[0] + ' · ' : '' } })); }
  });
  return { load, clear };
}
