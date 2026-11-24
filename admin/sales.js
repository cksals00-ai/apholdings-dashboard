// 매출 만들기 탭 (2026-10-27) — 첫 매출 → 3개월 연속 매출
// admin_sales_plan(전략 1행) · admin_sales_listings(상품 파이프라인) · admin_sales_orders(주문 원장)
// 막힌 것은 admin_commerce_blockers(open)를 채널별로 묶어 보여준다. 소유자만 읽고 쓴다(RLS).
const esc = (s = '') => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const won = n => n == null || Number.isNaN(Number(n)) ? '—' : Math.round(Number(n)).toLocaleString('ko-KR') + '원';
const man = n => n == null ? '—' : (Math.abs(n) >= 10000 ? (Math.round(n / 1000) / 10).toLocaleString('ko-KR') + '만' : Math.round(n).toLocaleString('ko-KR')) + '원';
const kst = () => new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);
const md = s => s ? `${Number(s.slice(5, 7))}/${Number(s.slice(8, 10))}` : '';
const dayDiff = (a, b) => Math.round((Date.parse(a + 'T00:00:00Z') - Date.parse(b + 'T00:00:00Z')) / 864e5);
const safeUrl = v => { try { const u = new URL(v); return ['https:', 'http:'].includes(u.protocol) && !u.username && !u.password ? u.href : ''; } catch { return ''; } };

const CHANNELS = {
  naver_buyagent: { name: '네이버 구매대행', short: '네이버', color: '#03a94d', partner: 'naver_smartstore' },
  shopee_sg: { name: '쇼피 싱가포르', short: '쇼피 SG', color: '#ee4d2d', partner: 'shopee_sg' },
  coupang_partners: { name: '쿠팡 파트너스', short: '쿠팡', color: '#346aff', partner: 'coupang' },
  other: { name: '기타', short: '기타', color: '#667085', partner: '' },
};
const STAGES = [
  ['idea', '후보', '클레어가 올린 후보 · 대표 선택 전'],
  ['sourcing', '공급 확인', '재고·가격·사진 사용 확인 중'],
  ['ready', '등록 준비', '원고·사진 준비 완료'],
  ['listed', '등록됨', '판매 페이지 열림 · 주문 대기'],
  ['selling', '판매 중', '주문이 1건 이상'],
];
const STAGE_NAME = Object.fromEntries([...STAGES.map(s => [s[0], s[1]]), ['paused', '중지'], ['dropped', '제외']]);
const ORDER_STATUS = { ordered: '주문', shipped: '발송', delivered: '배송완료', settled: '정산완료', cancelled: '취소', returned: '반품' };
const COUNTS = new Set(['ordered', 'shipped', 'delivered', 'settled']);

export function createSales(db, getUser) {
  const root = document.querySelector('#sales-section');
  let plan = {}, listings = [], orders = [], blockers = [], partners = [], loaded = false, gen = 0, chFilter = 'ALL';
  root.innerHTML = `<p id="sl-message" class="form-message" role="status" aria-live="polite"></p><div id="sl-body"></div>
  <dialog id="sl-listing-dialog"><form id="sl-listing-form" class="sl-form" method="dialog">
    <div class="dialog-head"><div><p class="eyebrow">PRODUCT</p><h2 id="sl-l-title">상품</h2></div><button class="icon-button" type="button" data-sl-close aria-label="닫기">×</button></div>
    <div class="form-grid">
      <label class="span-2">상품명<input name="title" required maxlength="200"></label>
      <label>채널<select name="channel">${Object.entries(CHANNELS).map(([k, c]) => `<option value="${k}">${c.name}</option>`).join('')}</select></label>
      <label>단계<select name="stage">${Object.entries(STAGE_NAME).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select></label>
      <label>재고 방식<select name="stock_mode"><option value="dropship">무재고(주문 후 구매)</option><option value="stocked">사입</option></select></label>
      <label>사입 수량<input name="stock_qty" type="number" min="0" step="1"></label>
      <label>판매가<input name="sale_price" type="number" min="0" step="0.01"></label>
      <label>통화<select name="currency"><option>KRW</option><option>SGD</option><option>USD</option></select></label>
      <label>원가(원)<input name="unit_cost_krw" type="number" min="0" step="1"></label>
      <label>배송비(원)<input name="ship_cost_krw" type="number" min="0" step="1"></label>
      <label>수수료율(%)<input name="fee_rate" type="number" min="0" max="100" step="0.1"></label>
      <label>등록일<input name="listed_on" type="date"></label>
      <label class="span-2">공급처 링크<input name="source_url" type="url" placeholder="https://"></label>
      <label class="span-2">판매 페이지 링크<input name="listing_url" type="url" placeholder="https://"></label>
      <label class="span-2">메모<textarea name="note" rows="3" maxlength="2000"></textarea></label>
    </div>
    <p id="sl-l-est" class="sl-est"></p>
    <div class="dialog-actions"><button type="button" class="danger" data-sl-drop hidden>제외</button><span></span><button type="button" class="secondary" data-sl-close>취소</button><button type="submit" class="primary">저장</button></div>
  </form></dialog>
  <dialog id="sl-order-dialog"><form id="sl-order-form" class="sl-form" method="dialog">
    <div class="dialog-head"><div><p class="eyebrow">ORDER</p><h2 id="sl-o-title">주문 기록</h2></div><button class="icon-button" type="button" data-sl-close aria-label="닫기">×</button></div>
    <div class="form-grid">
      <label>주문일<input name="order_date" type="date" required></label>
      <label>채널<select name="channel">${Object.entries(CHANNELS).map(([k, c]) => `<option value="${k}">${c.name}</option>`).join('')}</select></label>
      <label class="span-2">상품<select name="listing_id"><option value="">(직접 입력)</option></select></label>
      <label>상품명(직접)<input name="item_title" maxlength="200"></label>
      <label>주문번호<input name="order_no" maxlength="80"></label>
      <label>수량<input name="qty" type="number" min="1" step="1" value="1"></label>
      <label>상태<select name="status">${Object.entries(ORDER_STATUS).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select></label>
      <label>결제 금액(원)<input name="sale_amount_krw" type="number" min="0" step="1" required></label>
      <label>상품 원가(원)<input name="product_cost_krw" type="number" min="0" step="1"></label>
      <label>플랫폼 수수료(원)<input name="platform_fee_krw" type="number" min="0" step="1"></label>
      <label>배송비(원)<input name="shipping_cost_krw" type="number" min="0" step="1"></label>
      <label>기타 비용(원)<input name="other_cost_krw" type="number" min="0" step="1"></label>
      <label>정산일<input name="settled_on" type="date"></label>
      <label>정산 입금액(원)<input name="settled_amount_krw" type="number" min="0" step="1"></label>
      <label class="span-2">메모<textarea name="note" rows="2" maxlength="2000"></textarea></label>
    </div>
    <p id="sl-o-net" class="sl-est"></p>
    <div class="dialog-actions"><span></span><span></span><button type="button" class="secondary" data-sl-close>취소</button><button type="submit" class="primary">저장</button></div>
  </form></dialog>`;
  const $ = s => root.querySelector(s), msg = s => { $('#sl-message').textContent = s; };
  const ld = $('#sl-listing-dialog'), od = $('#sl-order-dialog'), lf = $('#sl-listing-form'), of = $('#sl-order-form');
  let editL = null, editO = null;

  const fx = () => Number(plan.fx?.SGD) || 1050;
  const toKrw = l => l.sale_price == null ? null : Number(l.sale_price) * (l.currency === 'SGD' ? fx() : l.currency === 'USD' ? (Number(plan.fx?.USD) || 1400) : 1);
  function est(l) {
    const p = toKrw(l); if (p == null || l.unit_cost_krw == null) return null;
    const fee = l.fee_rate == null ? null : p * Number(l.fee_rate) / 100;
    const profit = p - (fee ?? 0) - Number(l.unit_cost_krw) - Number(l.ship_cost_krw ?? 0);
    return { price: p, profit, margin: p ? profit / p : null, missing: [l.fee_rate == null && '수수료', l.ship_cost_krw == null && '배송비'].filter(Boolean) };
  }
  const net = o => (o.sale_amount_krw || 0) - (o.product_cost_krw || 0) - (o.platform_fee_krw || 0) - (o.shipping_cost_krw || 0) - (o.other_cost_krw || 0);

  async function load(force = false) {
    if (!getUser()) return; if (loaded && !force) { render(); return; }
    const t = ++gen; msg('매출 현황을 불러오는 중…');
    try {
      const [a, b, c, d, e] = await Promise.all([
        db.from('admin_sales_plan').select('*').eq('id', 1).maybeSingle(),
        db.from('admin_sales_listings').select('*').order('sort_order').order('created_at'),
        db.from('admin_sales_orders').select('*').order('order_date', { ascending: false }).order('created_at', { ascending: false }),
        db.from('admin_commerce_blockers').select('*').eq('status', 'open'),
        db.from('admin_commerce_partners').select('id,code,name,status'),
      ]);
      const err = a.error || b.error || c.error; if (err) throw err; if (t !== gen) return;
      plan = a.data?.payload || {}; listings = b.data || []; orders = c.data || []; blockers = d.error ? [] : d.data || []; partners = e.error ? [] : e.data || [];
      loaded = true; render(); msg('');
    } catch (e) { if (t === gen) msg('매출 현황을 불러오지 못했습니다. 로그인과 연결 상태를 확인한 후 새로고침하세요.'); }
  }
  function clear() { gen++; plan = {}; listings = []; orders = []; blockers = []; partners = []; loaded = false; $('#sl-body').innerHTML = ''; msg(''); }

  /* ───── 계산 ───── */
  function monthStats() {
    const m = {};
    for (const o of orders) {
      if (!COUNTS.has(o.status)) continue;
      const k = o.order_date.slice(0, 7); m[k] ??= { gmv: 0, net: 0, orders: 0, settled: 0 };
      m[k].gmv += o.sale_amount_krw || 0; m[k].net += net(o); m[k].orders += 1; m[k].settled += o.settled_amount_krw || 0;
    }
    return m;
  }

  /* ───── 그리기 ───── */
  function render() {
    const today = kst(), month = today.slice(0, 7), ms = monthStats(), cur = ms[month] || { gmv: 0, net: 0, orders: 0 };
    const tg = plan.targets?.[month] || {};
    const valid = orders.filter(o => COUNTS.has(o.status));
    const first = valid.length ? valid.reduce((a, o) => (o.order_date < a.order_date ? o : a)) : null;
    const firstSettled = valid.some(o => o.status === 'settled' || o.settled_amount_krw > 0);
    const firstBy = plan.milestones?.find(x => /첫 주문|첫 매출/.test(x.label))?.date || '2026-11-30';
    const live = ch => listings.filter(l => l.channel === ch && ['listed', 'selling'].includes(l.stage)).length;
    const streakMonths = Object.keys(plan.targets || {}).filter(k => k >= '2026-12');
    const streak = streakMonths.filter(k => (ms[k]?.gmv || 0) > 0).length;

    $('#sl-body').innerHTML = `
    <section class="sl-hero">
      <div><p class="eyebrow">SALES FIRST · ${esc(plan.updated || '')}</p><h2>${esc(plan.title || '매출 만들기')}</h2><p>${esc(plan.thesis || '')}</p></div>
      <div class="sl-hero-actions"><button class="primary" data-sl="add-order">+ 주문 기록</button><button class="secondary" data-sl="add-listing">+ 상품</button><button class="secondary" data-sl="csv">원장 CSV</button><button class="secondary" data-sl="refresh">↻</button></div>
    </section>

    <div class="sl-kpis">
      <article class="sl-kpi ${first ? 'good' : dayDiff(firstBy, today) < 7 ? 'warn' : ''}"><span>첫 매출</span><b>${first ? '달성' : 'D-' + Math.max(0, dayDiff(firstBy, today))}</b><small>${first ? `${md(first.order_date)} · ${esc(CHANNELS[first.channel]?.short || '')} · ${firstSettled ? '정산 입금 확인' : '정산 전'}` : `목표 ${md(firstBy)} · 주문 1건 → 정산 입금`}</small></article>
      <article class="sl-kpi"><span>${Number(month.slice(5))}월 거래액</span><b>${man(cur.gmv)}</b>${tg.gmv ? `<div class="sl-bar"><i style="width:${Math.min(100, cur.gmv / tg.gmv * 100).toFixed(1)}%"></i></div><small>목표 ${man(tg.gmv)} · ${Math.round(cur.gmv / tg.gmv * 100)}%</small>` : '<small>목표 없음</small>'}</article>
      <article class="sl-kpi ${cur.net < 0 ? 'bad' : ''}"><span>${Number(month.slice(5))}월 순이익</span><b>${man(cur.net)}</b><small>주문 ${cur.orders}건 · 원가·수수료·배송비 뺀 값</small></article>
      <article class="sl-kpi"><span>판매 페이지</span><b>${live('naver_buyagent') + live('shopee_sg')}</b><small>네이버 ${live('naver_buyagent')}/10 · 쇼피 ${live('shopee_sg')}/3</small></article>
      <article class="sl-kpi ${streak >= 3 ? 'good' : ''}"><span>연속 매출 (12~2월)</span><b>${streak}/3</b><small>3개월 채우면 은행·보증 상담</small></article>
    </div>

    ${timeline(today, !!first)}

    <div class="sl-grid2">
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">MONTHLY · 목표 대비</p><h2>월별 거래액 · 순이익</h2></div><div class="sl-legend"><span><i class="sw t"></i>목표</span><span><i class="sw g"></i>거래액</span><span><i class="sw n"></i>순이익</span></div></div>${monthChart(ms)}<p class="panel-note">${esc(plan.targets_note || '')}</p></section>
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">WHY · 순서를 바꾼다</p><h2>왜 매출부터인가</h2></div></div><ol class="sl-list">${(plan.why || []).map(x => `<li>${esc(x)}</li>`).join('')}</ol>
        <p class="eyebrow" style="margin-top:16px">대표가 정할 것</p><ul class="sl-list">${(plan.decisions || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul></section>
    </div>

    <div class="sl-channels">${(plan.channels || []).map(ch => channelCard(ch)).join('')}</div>

    <section class="panel"><div class="panel-head"><div><p class="eyebrow">PIPELINE · 후보 → 판매</p><h2>상품 보드</h2></div>
      <div class="sl-chips">${[['ALL', '전체'], ...Object.entries(CHANNELS).filter(([k]) => k !== 'other').map(([k, c]) => [k, c.short])].map(([k, v]) => `<button class="sl-chip ${chFilter === k ? 'on' : ''}" data-sl-ch="${k}">${esc(v)} <small>${k === 'ALL' ? listings.filter(l => !['dropped'].includes(l.stage)).length : listings.filter(l => l.channel === k && l.stage !== 'dropped').length}</small></button>`).join('')}</div></div>
      <div class="sl-board">${STAGES.map(([k, name, hint]) => { const cards = listings.filter(l => l.stage === k && (chFilter === 'ALL' || l.channel === chFilter));
        return `<div class="sl-col"><div class="sl-col-head"><b>${name}</b><span>${cards.length}</span></div><p class="sl-col-hint">${hint}</p>${cards.map(card).join('') || '<p class="sl-empty">없음</p>'}</div>`; }).join('')}</div>
      ${listings.some(l => ['paused', 'dropped'].includes(l.stage)) ? `<details class="sl-more"><summary>중지·제외 ${listings.filter(l => ['paused', 'dropped'].includes(l.stage)).length}개</summary><div class="sl-mini">${listings.filter(l => ['paused', 'dropped'].includes(l.stage)).map(l => `<button data-sl-l="${l.id}">${esc(l.title)} · ${STAGE_NAME[l.stage]}</button>`).join('')}</div></details>` : ''}
    </section>

    <section class="panel panel-wide"><div class="panel-head sl-pad"><div><p class="eyebrow">LEDGER · 매출 증빙</p><h2>주문 원장</h2></div><span class="panel-note">월말에 정산 입금과 맞춰 마감 · 은행 상담 근거</span></div>
      <div class="asset-table-wrap"><table class="asset-table sl-ledger"><thead><tr><th>주문일</th><th>채널</th><th>상품</th><th class="num">결제</th><th class="num">원가</th><th class="num">수수료</th><th class="num">배송</th><th class="num">순이익</th><th>상태</th><th>정산</th></tr></thead>
      <tbody>${orders.map(o => `<tr data-sl-o="${o.id}" class="${COUNTS.has(o.status) ? '' : 'retired'}"><td class="date">${esc(o.order_date)}</td><td><span class="sl-dot" style="--c:${CHANNELS[o.channel]?.color}"></span>${esc(CHANNELS[o.channel]?.short || o.channel)}</td><td class="title"><b>${esc(o.item_title || listings.find(l => l.id === o.listing_id)?.title || '—')}</b>${o.qty > 1 ? `<small> ×${o.qty}</small>` : ''}</td><td class="num">${won(o.sale_amount_krw)}</td><td class="num">${won(o.product_cost_krw)}</td><td class="num">${won(o.platform_fee_krw)}</td><td class="num">${won(o.shipping_cost_krw)}</td><td class="num ${net(o) < 0 ? 'sl-neg' : ''}">${won(net(o))}</td><td><span class="tag" data-status="${o.status === 'settled' ? 'DONE' : COUNTS.has(o.status) ? 'IN_PROGRESS' : 'CANCELLED'}">${ORDER_STATUS[o.status]}</span></td><td class="date">${o.settled_on ? esc(o.settled_on) + (o.settled_amount_krw ? ' · ' + won(o.settled_amount_krw) : '') : '—'}</td></tr>`).join('') || `<tr><td colspan="10" class="empty">아직 주문이 없습니다. 첫 주문이 들어오면 「+ 주문 기록」으로 바로 남겨 주세요.</td></tr>`}</tbody>
      ${valid.length ? `<tfoot><tr><td colspan="3"><b>합계 (취소·반품 제외)</b></td><td class="num"><b>${won(valid.reduce((s, o) => s + (o.sale_amount_krw || 0), 0))}</b></td><td colspan="3"></td><td class="num"><b>${won(valid.reduce((s, o) => s + net(o), 0))}</b></td><td colspan="2"></td></tr></tfoot>` : ''}</table></div>
    </section>

    <div class="sl-grid2">
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">WEEKLY RHYTHM · 평일 저녁 1시간 + 주말 반나절</p><h2>한 주 돌리는 법</h2></div></div>
        <div class="sl-rhythm">${(plan.rhythm || []).map(([d, t]) => `<div><b>${esc(d)}</b><span>${esc(t)}</span></div>`).join('')}</div>
        <p class="eyebrow" style="margin-top:16px">클레어가 맡는 것</p><ul class="sl-list">${(plan.claire || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul></section>
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">STOP · 첫 매출 전까지</p><h2>하지 않는 것</h2></div></div><ul class="sl-list sl-stop">${(plan.stop || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul></section>
    </div>`;
  }

  function timeline(today, firstDone) {
    const ms = plan.milestones || []; if (!ms.length) return '';
    const a = ms[0].date, b = ms[ms.length - 1].date, span = Math.max(1, dayDiff(b, a));
    const pos = d => Math.min(100, Math.max(0, dayDiff(d, a) / span * 100));
    const tp = pos(today);
    return `<section class="panel sl-tl"><div class="panel-head"><div><p class="eyebrow">ROADMAP · 오늘 ${md(today)}</p><h2>매출 → 증빙 3개월 → 상담</h2></div></div>
      <div class="sl-track"><div class="sl-fill" style="width:${tp}%"></div><div class="sl-today" style="left:${tp}%"><span>오늘</span></div>
      ${ms.map((m, i) => { const done = m.date < today || (firstDone && /첫 주문|첫 매출/.test(m.label)); return `<div class="sl-ms ${done ? 'done' : ''} ${i % 2 ? 'low' : ''}" style="left:${pos(m.date)}%"><i></i><b>${md(m.date)}</b><span>${esc(m.label)}</span></div>`; }).join('')}</div></section>`;
  }

  function monthChart(ms) {
    const keys = Object.keys(plan.targets || {}); if (!keys.length) return '<p class="empty">월 목표가 없습니다.</p>';
    const vals = keys.map(k => ({ k, t: plan.targets[k].gmv || 0, g: ms[k]?.gmv || 0, n: ms[k]?.net || 0 }));
    const max = Math.max(1, ...vals.map(v => Math.max(v.t, v.g))), W = 560, H = 220, pad = 34, bw = (W - pad * 2) / vals.length;
    const y = v => H - 28 - (Math.max(0, v) / max) * (H - 60);
    return `<svg class="sl-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="월별 목표 대비 거래액">
      <line x1="${pad}" x2="${W - pad}" y1="${H - 28}" y2="${H - 28}" class="ax"/>
      ${vals.map((v, i) => { const x = pad + i * bw + bw * .2, w = bw * .6;
        return `<rect class="t" x="${x}" y="${y(v.t)}" width="${w}" height="${H - 28 - y(v.t)}" rx="6"/>
        <rect class="g" x="${x + w * .18}" y="${y(v.g)}" width="${w * .64}" height="${H - 28 - y(v.g)}" rx="4"/>
        ${v.n ? `<circle class="n" cx="${x + w / 2}" cy="${y(v.n)}" r="5"/>` : ''}
        <text x="${x + w / 2}" y="${H - 10}" class="lb">${Number(v.k.slice(5))}월</text>
        <text x="${x + w / 2}" y="${Math.min(y(v.t), y(v.g)) - 6}" class="vl">${v.g ? man(v.g) : man(v.t)}</text>`; }).join('')}
    </svg>`;
  }

  function channelCard(ch) {
    const c = CHANNELS[ch.key] || CHANNELS.other, mine = listings.filter(l => l.channel === ch.key);
    const counts = STAGES.map(([k, n]) => [n, mine.filter(l => l.stage === k).length]);
    const total = Math.max(1, counts.reduce((s, [, n]) => s + n, 0));
    const pid = partners.find(p => p.code === c.partner)?.id;
    const bl = blockers.filter(b => b.partner_id && b.partner_id === pid);
    const ord = orders.filter(o => o.channel === ch.key && COUNTS.has(o.status));
    return `<article class="panel sl-ch" style="--c:${c.color}">
      <div class="sl-ch-head"><div><p class="eyebrow">${esc(ch.mode || '')}</p><h3>${esc(ch.name)}</h3></div><div class="sl-ch-num"><b>${ord.length}</b><small>주문 · ${man(ord.reduce((s, o) => s + (o.sale_amount_krw || 0), 0))}</small></div></div>
      <p class="sl-goal">🎯 ${esc(ch.goal || '')}</p>
      <div class="sl-funnel">${counts.map(([n, v]) => `<div style="flex:${Math.max(v, .35)}" title="${n} ${v}"><span>${n}</span><b>${v}</b></div>`).join('')}</div>
      ${(ch.unlock || []).length ? `<p class="eyebrow">열어야 할 문</p><ul class="sl-check">${ch.unlock.map(u => `<li>${esc(u)}</li>`).join('')}</ul>` : ''}
      <p class="sl-rule">${esc(ch.rule || '')}</p>
      ${bl.length ? `<details class="sl-more"><summary>막힌 것 ${bl.length}건</summary><ul class="sl-list sl-small">${bl.map(b => `<li><b>${esc(b.title)}</b> <span class="tag" data-status="${b.severity === 'blocking' ? 'CANCELLED' : 'WAITING'}">${b.severity === 'blocking' ? '막힘' : '주시'}</span></li>`).join('')}</ul></details>` : ''}
    </article>`;
  }

  function card(l) {
    const c = CHANNELS[l.channel] || CHANNELS.other, e = est(l), i = STAGES.findIndex(s => s[0] === l.stage), next = STAGES[i + 1];
    return `<div class="sl-card" data-sl-l="${l.id}" style="--c:${c.color}">
      <div class="sl-card-top"><span class="sl-dot"></span><small>${esc(c.short)} · ${l.stock_mode === 'stocked' ? '사입' + (l.stock_qty != null ? ' ' + l.stock_qty + '개' : '') : '무재고'}</small></div>
      <h4>${esc(l.title)}</h4>
      <div class="sl-card-num"><span>${l.sale_price != null ? (l.currency === 'KRW' ? won(l.sale_price) : `${l.currency} ${Number(l.sale_price).toLocaleString('en')}`) : '가격 미정'}</span>${e ? `<b class="${e.profit < 0 ? 'sl-neg' : ''}">${e.profit < 0 ? '' : '+'}${man(e.profit)}${e.missing.length ? '*' : ''}</b>` : ''}</div>
      ${e?.missing.length ? `<small class="sl-miss">* ${e.missing.join('·')} 미입력 추정</small>` : ''}
      ${next ? `<button class="sl-next" data-sl-next="${l.id}">→ ${next[1]}</button>` : ''}
    </div>`;
  }

  /* ───── 편집 ───── */
  function openListing(l) {
    editL = l || null; lf.reset();
    $('#sl-l-title').textContent = l ? '상품 편집' : '상품 추가';
    const v = l || { channel: chFilter !== 'ALL' ? chFilter : 'naver_buyagent', stage: 'idea', stock_mode: 'dropship', currency: 'KRW' };
    for (const el of lf.elements) if (el.name && v[el.name] != null) el.value = v[el.name];
    if (!l && v.channel === 'shopee_sg') { lf.elements.currency.value = 'SGD'; lf.elements.stock_mode.value = 'stocked'; }
    lf.querySelector('[data-sl-drop]').hidden = !l || l.stage === 'dropped';
    showEst(); ld.showModal();
  }
  function formListing() {
    const f = lf.elements, n = k => f[k].value === '' ? null : Number(f[k].value);
    return { title: f.title.value.trim(), channel: f.channel.value, stage: f.stage.value, stock_mode: f.stock_mode.value, stock_qty: n('stock_qty'),
      sale_price: n('sale_price'), currency: f.currency.value, unit_cost_krw: n('unit_cost_krw'), ship_cost_krw: n('ship_cost_krw'), fee_rate: n('fee_rate'),
      listed_on: f.listed_on.value || null, source_url: safeUrl(f.source_url.value) || '', listing_url: safeUrl(f.listing_url.value) || '', note: f.note.value };
  }
  function showEst() { const e = est(formListing()); $('#sl-l-est').innerHTML = e ? `예상 순이익 <b class="${e.profit < 0 ? 'sl-neg' : ''}">${won(e.profit)}</b> · 판매가 ${won(e.price)}${e.margin != null ? ` · 이익률 ${(e.margin * 100).toFixed(1)}%` : ''}${e.missing.length ? ` <small>(${e.missing.join('·')} 미입력 — 실제보다 높게 보일 수 있음)</small>` : ''}${lf.elements.currency.value === 'SGD' ? ` <small>· 환율 ${fx().toLocaleString()}원/SGD</small>` : ''}` : '판매가와 원가를 넣으면 예상 순이익이 계산됩니다.'; }
  lf.addEventListener('input', showEst);
  lf.addEventListener('submit', async ev => {
    ev.preventDefault(); const row = formListing(); if (!row.title) return;
    if (row.listed_on == null && ['listed', 'selling'].includes(row.stage) && !editL?.listed_on) row.listed_on = kst();
    row.updated_at = new Date().toISOString(); row.updated_by = getUser()?.id;
    const r = editL ? await db.from('admin_sales_listings').update(row).eq('id', editL.id) : await db.from('admin_sales_listings').insert({ ...row, created_by: getUser()?.id });
    if (r.error) { msg('저장하지 못했습니다: ' + r.error.message); return; }
    ld.close(); await load(true);
  });
  lf.querySelector('[data-sl-drop]').addEventListener('click', async () => {
    if (!editL) return; const r = await db.from('admin_sales_listings').update({ stage: 'dropped', updated_at: new Date().toISOString(), updated_by: getUser()?.id }).eq('id', editL.id);
    if (r.error) { msg('바꾸지 못했습니다: ' + r.error.message); return; } ld.close(); await load(true);
  });

  function openOrder(o) {
    editO = o || null; of.reset();
    $('#sl-o-title').textContent = o ? '주문 편집' : '주문 기록';
    const sel = of.elements.listing_id;
    sel.innerHTML = '<option value="">(직접 입력)</option>' + listings.filter(l => l.stage !== 'dropped').map(l => `<option value="${l.id}">${esc(CHANNELS[l.channel]?.short)} · ${esc(l.title)}</option>`).join('');
    const v = o || { order_date: kst(), channel: chFilter !== 'ALL' ? chFilter : 'naver_buyagent', status: 'ordered', qty: 1 };
    for (const el of of.elements) if (el.name && v[el.name] != null) el.value = v[el.name];
    showNet(); od.showModal();
  }
  function formOrder() {
    const f = of.elements, n = k => f[k].value === '' ? 0 : Math.round(Number(f[k].value));
    return { order_date: f.order_date.value, channel: f.channel.value, listing_id: f.listing_id.value || null, item_title: f.item_title.value.trim(), order_no: f.order_no.value.trim(),
      qty: Math.max(1, n('qty')), status: f.status.value, sale_amount_krw: n('sale_amount_krw'), product_cost_krw: n('product_cost_krw'), platform_fee_krw: n('platform_fee_krw'),
      shipping_cost_krw: n('shipping_cost_krw'), other_cost_krw: n('other_cost_krw'), settled_on: f.settled_on.value || null,
      settled_amount_krw: f.settled_amount_krw.value === '' ? null : Math.round(Number(f.settled_amount_krw.value)), note: f.note.value };
  }
  function showNet() { const o = formOrder(); $('#sl-o-net').innerHTML = `순이익 <b class="${net(o) < 0 ? 'sl-neg' : ''}">${won(net(o))}</b> = 결제 ${won(o.sale_amount_krw)} − 원가·수수료·배송·기타`; }
  of.addEventListener('input', showNet);
  of.elements.listing_id.addEventListener('change', () => {
    const l = listings.find(x => x.id === of.elements.listing_id.value); if (!l) return;
    of.elements.channel.value = l.channel; if (!of.elements.item_title.value) of.elements.item_title.value = l.title;
    if (!of.elements.product_cost_krw.value && l.unit_cost_krw != null) of.elements.product_cost_krw.value = l.unit_cost_krw;
    showNet();
  });
  of.addEventListener('submit', async ev => {
    ev.preventDefault(); const row = formOrder(); if (!row.order_date) return;
    row.updated_at = new Date().toISOString(); row.updated_by = getUser()?.id;
    const r = editO ? await db.from('admin_sales_orders').update(row).eq('id', editO.id) : await db.from('admin_sales_orders').insert({ ...row, created_by: getUser()?.id });
    if (r.error) { msg('저장하지 못했습니다: ' + r.error.message); return; }
    // 주문이 생긴 상품은 「판매 중」으로 올린다.
    if (row.listing_id && COUNTS.has(row.status)) { const l = listings.find(x => x.id === row.listing_id); if (l && l.stage !== 'selling') await db.from('admin_sales_listings').update({ stage: 'selling', updated_at: new Date().toISOString(), updated_by: getUser()?.id }).eq('id', l.id); }
    od.close(); await load(true);
  });

  function csv() {
    const head = ['주문일', '채널', '주문번호', '상품', '수량', '결제금액', '상품원가', '플랫폼수수료', '배송비', '기타비용', '순이익', '상태', '정산일', '정산입금액', '메모'];
    const q = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
    const rows = orders.slice().reverse().map(o => [o.order_date, CHANNELS[o.channel]?.name, o.order_no, o.item_title || listings.find(l => l.id === o.listing_id)?.title, o.qty, o.sale_amount_krw, o.product_cost_krw, o.platform_fee_krw, o.shipping_cost_krw, o.other_cost_krw, net(o), ORDER_STATUS[o.status], o.settled_on, o.settled_amount_krw, o.note].map(q).join(','));
    const blob = new Blob(['﻿' + [head.map(q).join(','), ...rows].join('\r\n')], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `AP_매출원장_${kst()}.csv`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }

  root.addEventListener('click', async ev => {
    const t = ev.target.closest('[data-sl],[data-sl-ch],[data-sl-l],[data-sl-o],[data-sl-next],[data-sl-close]'); if (!t) return;
    if (t.dataset.slClose !== undefined) { t.closest('dialog')?.close(); return; }
    if (t.dataset.slNext) { ev.stopPropagation(); const l = listings.find(x => x.id === t.dataset.slNext), i = STAGES.findIndex(s => s[0] === l?.stage), nx = STAGES[i + 1]?.[0]; if (!l || !nx) return;
      const patch = { stage: nx, updated_at: new Date().toISOString(), updated_by: getUser()?.id }; if (['listed', 'selling'].includes(nx) && !l.listed_on) patch.listed_on = kst();
      const r = await db.from('admin_sales_listings').update(patch).eq('id', l.id); if (r.error) msg('바꾸지 못했습니다: ' + r.error.message); else await load(true); return; }
    if (t.dataset.slCh) { chFilter = t.dataset.slCh; render(); return; }
    if (t.dataset.slL) { openListing(listings.find(x => x.id === t.dataset.slL)); return; }
    if (t.dataset.slO) { openOrder(orders.find(x => x.id === t.dataset.slO)); return; }
    const a = t.dataset.sl;
    if (a === 'refresh') load(true); else if (a === 'add-listing') openListing(); else if (a === 'add-order') openOrder(); else if (a === 'csv') csv();
  });

  return { load, clear };
}
