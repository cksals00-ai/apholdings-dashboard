// 홍보 탭 — AP 애드렌즈 벤치마크·훅 분석 일일 보고 + 전략 계층(일/주/월/년/5년) + 사업계획 연결
// admin_marketing_reports(일별) · admin_marketing_strategy(1행) · admin_marketing_benchmarks(계정)
const esc = (s = '') => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const safeUrl = v => { try { const u = new URL(v); return ['https:', 'http:'].includes(u.protocol) && !u.username && !u.password ? u.href : ''; } catch { return ''; } };
const link = (url, label) => safeUrl(url) ? `<a href="${esc(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>` : esc(label);
const num = n => n == null ? '—' : Number(n).toLocaleString('ko-KR');
const day = s => s ? new Intl.DateTimeFormat('ko-KR', { month: 'numeric', day: 'numeric', weekday: 'short', timeZone: 'Asia/Seoul' }).format(new Date(s.length === 10 ? s + 'T00:00:00+09:00' : s)) : '미정';
const HORIZONS = [['daily', '오늘', '하루 한 편'], ['weekly', '이번 주', '주간 로테이션'], ['monthly', '이번 달', '시리즈·확장'], ['yearly', '올해', '채널이 사업이 되는 해'], ['five_year', '5개년', '데이터 자산·IP']];

export function createMarketing(db, getUser) {
  const root = document.querySelector('#marketing-section');
  let strategy = null, reports = [], benchmarks = [], nsrc = [], nitems = [], loaded = false, gen = 0, idx = 0, horizon = 'daily';
  root.innerHTML = `<p id="mk-message" class="form-message" role="status" aria-live="polite"></p><div id="mk-body"></div>
    <section class="panel panel-wide" id="mk-ads-panel"><div class="panel-head"><div><p class="eyebrow">PAID · APPLE ADS (중단 · 기록 보존)</p><h2>검색 광고 성과 — 앱 현황에서 이관</h2></div><span id="app-ads-state" class="status-pill">연결 예정</span></div><p class="panel-note" style="margin:-8px 0 14px">유료 광고는 2026-09-29 전부 중단(재개는 대표 판단). 캠페인 기록과 동기화는 그대로 유지해 무료 채널 성과와 비교하는 기준선으로 쓴다.</p><div id="app-ads"></div></section>`;
  const $ = s => root.querySelector(s), msg = s => { $('#mk-message').textContent = s; };

  async function load(force = false) {
    if (!getUser()) return; if (loaded && !force) { render(); return; }
    const t = ++gen; msg('홍보 현황을 불러오는 중…');
    try {
      const [a, b, c, d, f] = await Promise.all([
        db.from('admin_marketing_strategy').select('*').eq('id', 1).maybeSingle(),
        db.from('admin_marketing_reports').select('*').order('report_date', { ascending: false }).limit(60),
        db.from('admin_marketing_benchmarks').select('*').order('followers', { ascending: false, nullsFirst: false }),
        db.from('admin_news_sources').select('*').order('priority').order('name'),
        db.from('admin_news_items').select('*').order('published', { ascending: false, nullsFirst: false }).limit(80),
      ]);
      if (a.error || b.error || c.error) throw a.error || b.error || c.error; if (t !== gen) return;
      strategy = a.data; reports = b.data || []; benchmarks = c.data || []; nsrc = d.error ? [] : d.data || []; nitems = f.error ? [] : f.data || []; loaded = true; idx = 0; render(); msg('');
    } catch { if (t === gen) msg('홍보 현황을 불러오지 못했습니다. 로그인과 연결 상태를 확인한 후 새로고침하세요.'); }
  }
  function clear() { gen++; strategy = null; reports = []; benchmarks = []; nsrc = []; nitems = []; loaded = false; $('#mk-body').innerHTML = ''; msg(''); }

  function render() {
    const r = reports[idx], h = strategy?.horizons || {}, ad = strategy?.adlens || {};
    const bench = benchmarks.filter(b => !String(b.note || '').startsWith('제외'));
    const kpis = r ? [
      ['벤치 계정', r.sources?.instagram?.accounts, '인스타 · 유튜브 ' + (r.sources?.youtube?.status ? '연결 전' : '연결'), 'blue'],
      ['분석 릴스', r.sources?.instagram?.reels_with_views, `수집 ${num(r.sources?.instagram?.posts)}편 중 조회수 공개분`, 'purple'],
      ['상위 훅', r.hook_types?.[0]?.type, `${r.hook_types?.[0]?.median_ratio ?? '—'}배 (조회수÷팔로워)`, 'green'],
      ['오늘 지시', r.directives?.length, '리아 · 한글컵스', 'amber'],
    ] : [];
    $('#mk-body').innerHTML = `
      <div class="co-hero"><div><p class="eyebrow">MARKETING INTELLIGENCE · AP ADLENS</p><h2>${esc(ad.title || '홍보 — 벤치마크·훅 분석')}</h2><p>${esc(ad.pitch || '')}</p><p class="panel-note">${esc(ad.status || '')} · ${link(ad.url, '애드렌즈 포털 열기')}</p></div><div class="co-toolbar"><button class="secondary" data-mk="refresh">↻ 새로고침</button><button class="secondary" data-mk="plan">사업계획 시트 →</button></div></div>
      ${r ? `<div class="summary-grid" style="grid-template-columns:repeat(4,minmax(0,1fr))">${kpis.map(([l, v, d, c]) => `<article class="summary-card co-kpi ${c}"><span>${esc(l)}</span><b style="font-size:${typeof v === 'string' && v.length > 4 ? '1.2rem' : '2rem'}">${esc(typeof v === 'number' ? num(v) : v ?? '—')}</b><small>${esc(d)}</small></article>`).join('')}</div>` : ''}
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">DAILY REPORT</p><h2>${r ? esc(r.title) : '아직 보고가 없습니다'}</h2></div><div class="co-toolbar"><select id="mk-date">${reports.map((x, i) => `<option value="${i}" ${i === idx ? 'selected' : ''}>${esc(x.report_date)} ${day(x.report_date)}</option>`).join('')}</select></div></div>
        ${r ? `<p style="line-height:1.75;margin:0 0 18px">${esc(r.summary)}</p>
        <div style="display:grid;gap:18px">
          <div><p class="eyebrow">DIRECTIVES · 오늘 내리는 지시</p><div class="priority-list" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">${(r.directives || []).map(d => `<div class="priority-item" style="cursor:default"><div class="meta"><span class="tag" data-status="${d.target === '리아' ? 'IN_PROGRESS' : d.target === '한글컵스' ? 'DONE' : 'WAITING'}">${esc(d.target)}</span></div><h3>${esc(d.action)}</h3><p>근거 — ${esc(d.why)}</p></div>`).join('') || '<p class="empty">지시 없음</p>'}</div></div>
          <div><p class="eyebrow">HOOK TYPES · 무엇이 터지나</p><div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>훅 유형</th><th>편</th><th>조회÷팔로워</th><th>대표</th></tr></thead><tbody>${(r.hook_types || []).map(t => `<tr><td><b>${esc(t.type)}</b></td><td>${num(t.n)}</td><td>${esc(t.median_ratio)}배</td><td class="co-small">${esc(t.example)}</td></tr>`).join('')}</tbody></table></div></div>
        </div>
        <details class="panel co-details" style="margin-top:18px"><summary>상위 릴스 ${(r.top_reels || []).length}편 <span>조회수÷팔로워 순 · 링크</span></summary><div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>계정</th><th>훅</th><th>조회수</th><th>배수</th><th>날짜</th><th>유형</th></tr></thead><tbody>${(r.top_reels || []).map(x => `<tr><td>@${esc(x.handle)}</td><td>${link(x.permalink, x.caption)}</td><td>${num(x.views)}</td><td>${esc(x.ratio)}</td><td>${esc(x.date)}</td><td>${esc(x.type)}</td></tr>`).join('')}</tbody></table></div></details>` : '<p class="empty">일일 보고가 쌓이면 여기에 표시됩니다.</p>'}
      </section>
      ${(() => { const m = strategy?.master; if (!m?.title) return ''; const kinds = { Owned: 'DONE', Earned: 'IN_PROGRESS', Community: 'WAITING', Engine: 'ON_HOLD' };
        return `<section class="panel"><div class="panel-head"><div><p class="eyebrow">MASTER PLAN · 광고 0원</p><h2>${esc(m.title)}</h2></div><span class="panel-note">${esc(m.updated || '')}</span></div>
        <p style="line-height:1.8;margin:0 0 18px;font-size:1.02rem">${esc(m.thesis)}</p>
        <div style="display:grid;grid-template-columns:1.1fr .9fr;gap:22px">
          <div><p class="eyebrow">원칙</p><ol style="margin:0 0 18px;padding-left:20px;line-height:1.8">${(m.principles || []).map(x => `<li>${esc(x)}</li>`).join('')}</ol>
            <p class="eyebrow">플라이휠</p><ol style="margin:0;padding-left:20px;line-height:1.8">${(m.flywheel || []).map(x => `<li>${esc(x)}</li>`).join('')}</ol></div>
          <div><p class="eyebrow">하지 않는 것</p><ul style="margin:0 0 18px;padding-left:18px;line-height:1.8">${(m.dont || []).map(x => `<li>${esc(x)}</li>`).join('')}</ul>
            <p class="eyebrow">KPI 트리</p>${(m.kpi_tree || []).map(k => `<p style="margin:6px 0 2px"><b>${esc(k.level)}</b></p><ul style="margin:0;padding-left:18px;line-height:1.7">${(k.items || []).map(i => `<li>${esc(i)}</li>`).join('')}</ul>`).join('')}</div>
        </div>
        <p class="eyebrow" style="margin-top:22px">채널 지도</p>
        <div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>구분</th><th>채널</th><th>역할</th><th>KPI</th></tr></thead><tbody>${(m.channels || []).map(c => `<tr><td><span class="tag" data-status="${kinds[c.kind] || ''}">${esc(c.kind)}</span></td><td><b>${esc(c.name)}</b></td><td>${esc(c.role)}</td><td class="co-small">${esc(c.kpi)}</td></tr>`).join('')}</tbody></table></div>
        <p class="eyebrow" style="margin-top:22px">5축별 홍보 라인</p>
        <div class="priority-list" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">${(m.pillars || []).map(x => `<div class="priority-item" style="cursor:default"><h3>${esc(x.pillar)}</h3><p>${esc(x.line)}</p><p class="co-small" style="margin-top:8px">자산 — ${esc(x.asset)}</p></div>`).join('')}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:22px">
          <div><p class="eyebrow">주간 슬롯</p><div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>요일</th><th>슬롯</th><th>담당</th><th>게시</th></tr></thead><tbody>${(m.weekly_slots || []).map(w => `<tr><td><b>${esc(w.day)}</b></td><td>${esc(w.slot)}</td><td class="co-small">${esc(w.owner)}</td><td class="co-small">${esc(w.dest)}</td></tr>`).join('')}</tbody></table></div></div>
          <div><p class="eyebrow">90일 로드맵</p>${(m.roadmap_90d || []).map(r => `<p style="margin:8px 0 2px"><b>${esc(r.when)}</b></p><ul style="margin:0;padding-left:18px;line-height:1.7">${(r.goals || []).map(g => `<li>${esc(g)}</li>`).join('')}</ul>`).join('')}</div>
        </div></section>`; })()}
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">STRATEGY LAYERS</p><h2>하루 → 주 → 월 → 년 → 5개년</h2></div><span class="panel-note">${strategy?.updated_at ? '갱신 ' + day(strategy.updated_at) : ''}</span></div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px">${HORIZONS.map(([k, l, s]) => `<button data-mk="horizon" data-h="${k}" class="${k === horizon ? 'primary' : 'secondary'}" style="padding:9px 13px">${l} <small style="opacity:.75">· ${s}</small></button>`).join('')}</div>
        ${(() => { const x = h[horizon]; if (!x) return '<p class="empty">전략이 아직 없습니다.</p>'; return `<div style="display:grid;grid-template-columns:1.3fr .7fr;gap:22px"><div><h3 style="margin:0 0 10px;font-size:1.15rem">${esc(x.goal)}</h3><ol style="margin:0;padding-left:20px;line-height:1.8">${(x.moves || []).map(m => `<li>${esc(m)}</li>`).join('')}</ol></div><div><p class="eyebrow">KPI</p><ul style="margin:0 0 14px;padding-left:18px;line-height:1.8">${(x.kpi || []).map(k => `<li>${esc(k)}</li>`).join('')}</ul><p class="eyebrow">사업계획 연결</p><button class="secondary" data-mk="plan" style="width:100%;text-align:left">${esc(x.plan_ref || '사업계획 시트')} →</button></div></div>`; })()}
      </section>
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">BENCHMARK ACCOUNTS</p><h2>같은 카테고리 상위 계정 ${bench.length}</h2></div><span class="panel-note">중앙값 = 릴스 조회수÷팔로워 · 장르 기준선 0.10</span></div>
        <div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>플랫폼</th><th>계정</th><th>팔로워</th><th>표본</th><th>중앙값</th><th>최고</th><th>메모</th></tr></thead><tbody>${bench.map(b => `<tr><td>${esc(b.platform)}</td><td>${link(b.platform === 'instagram' ? 'https://www.instagram.com/' + b.handle + '/' : b.platform === 'youtube' ? 'https://www.youtube.com/@' + b.handle : '', '@' + b.handle)}</td><td>${num(b.followers)}</td><td>${num(b.posts_sampled)}</td><td>${b.median_ratio == null ? '—' : Number(b.median_ratio).toFixed(2)}</td><td>${b.top_ratio == null ? '—' : Number(b.top_ratio).toFixed(1)}</td><td class="co-small">${esc(b.note || '')}</td></tr>`).join('')}</tbody></table></div>
      </section>
      <section class="panel"><div class="panel-head"><div><p class="eyebrow">AP NEWS · 소스 링크 DB</p><h2>뉴스 소스 ${nsrc.length} · 참고 글 ${nitems.length}</h2></div><span class="panel-note">주 1회 자동 점검 · 재해석 초안 ${nitems.filter(i => i.status === 'drafted' || i.status === 'published').length}건 · <a href="/ko/news/" target="_blank" rel="noopener">AP News 보기</a></span></div>
        <div class="asset-table-wrap"><table class="asset-table"><thead><tr><th>소스</th><th>종류</th><th>상태</th><th>점검 주기</th><th>마지막 점검</th><th>메모</th></tr></thead><tbody>${nsrc.map(x => `<tr><td>${link(x.list_url || x.url, x.name)}</td><td>${esc(x.kind)}</td><td>${esc(x.status)}</td><td>${x.check_every_days}일</td><td>${x.last_checked ? esc(String(x.last_checked).slice(0, 10)) : '—'}</td><td>${esc(x.notes || '')}</td></tr>`).join('') || '<tr><td colspan="6">소스가 없습니다.</td></tr>'}</tbody></table></div>
        <div class="asset-table-wrap" style="margin-top:14px"><table class="asset-table"><thead><tr><th>날짜</th><th>참고 글</th><th>상태</th><th>우리 글</th></tr></thead><tbody>${nitems.map(i => `<tr><td>${esc(String(i.published || '').slice(0, 10))}</td><td>${link(i.url, i.title)}</td><td>${esc(i.status)}</td><td>${i.our_slug ? link('https://www.apholdings.kr/ko/news/' + i.our_slug + '/', i.our_slug) : '—'}</td></tr>`).join('') || '<tr><td colspan="4">수집된 글이 없습니다.</td></tr>'}</tbody></table></div>
      </section>
      `;
  }

  root.addEventListener('click', e => {
    const b = e.target.closest('[data-mk]'); if (!b) return;
    if (b.dataset.mk === 'refresh') load(true);
    if (b.dataset.mk === 'horizon') { horizon = b.dataset.h; render(); }
    if (b.dataset.mk === 'plan') document.querySelector('.nav-item[data-section="plan"]')?.click();
  });
  root.addEventListener('change', e => { if (e.target.id === 'mk-date') { idx = Number(e.target.value); render(); } });
  return { load, clear };
}
