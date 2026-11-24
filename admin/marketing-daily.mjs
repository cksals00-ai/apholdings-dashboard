// Operational report contract lives in sources.daily; no schema change is required.
const esc = (value = '') => String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const list = value => Array.isArray(value) ? value.filter(x => x && typeof x === 'object') : [];
const numeric = value => typeof value === 'number' && Number.isFinite(value) && value >= 0;
const number = value => numeric(value) ? value.toLocaleString('ko-KR', { maximumFractionDigits: 1 }) : '미확인';
const finished = item => ['done', 'resolved', 'completed', 'cancelled', '완료', '해결', '취소'].includes(item.status);
const todaySeoul = () => new Intl.DateTimeFormat('sv-SE', { timeZone: 'Asia/Seoul' }).format(new Date());
const url = value => { try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) && !u.username && !u.password ? u.href : ''; } catch { return ''; } };
const plain = value => String(value ?? '').replace(/\([A-J](?:\+[A-J])*\)/g, '').replace(/\bRPS\b/g, '가위바위보').replace(/\bv\/f\b/g, '팔로워 대비 조회율').replace(/\s*\([^)]*[×x]\s*[\d.]+[^)]*\)/g, '');
const section = (title, body) => `<section class="mk-block"><h3>${title}</h3>${body}</section>`;
const empty = text => `<p class="mk-empty">${text}</p>`;

export function dailyView(report = {}, today = todaySeoul()) {
  const daily = report.sources?.daily;
  const structured = Boolean(daily && ['decisions', 'posts', 'results', 'blockers'].every(k => Array.isArray(daily[k])));
  const date = report.report_date || today;
  const yesterday = new Date(`${date}T00:00:00Z`);
  yesterday.setUTCDate(yesterday.getUTCDate() - 1);
  const previousDate = Number.isNaN(yesterday.getTime()) ? '' : yesterday.toISOString().slice(0, 10);
  const decisions = list(daily?.decisions).filter(d => d.owner === '대표' && !finished(d));
  return {
    structured, date, stale: date !== today, previousDate,
    decisions: decisions.slice(0, 3), extraDecisions: decisions.slice(3),
    posts: list(daily?.posts).filter(p => !p.date || p.date === date),
    results: list(daily?.results).filter(r => r.metric_date === previousDate),
    blockers: list(daily?.blockers).filter(b => !finished(b)),
    reels: list(report.top_reels).sort((a, b) => (numeric(b.ratio) ? b.ratio : -1) - (numeric(a.ratio) ? a.ratio : -1)).slice(0, 3),
    benchmarkDate: daily?.benchmark_updated_at,
    takeaway: daily?.benchmark_takeaway,
  };
}

function decision(item) {
  return `<li><b>${esc(plain(item.title))}</b>${item.deadline ? ` <small>기한 ${esc(item.deadline)}</small>` : ''}${url(item.url) ? ` · <a href="${esc(url(item.url))}" target="_blank" rel="noopener noreferrer">확인하기 ↗</a>` : ''}</li>`;
}
function result(item) {
  let comparison = '비교 자료 없음';
  if (numeric(item.views) && numeric(item.average_7d) && (!(item.posts > 1) || item.views_basis === 'per_post')) {
    comparison = `평소(7일 평균 ${number(item.average_7d)})보다 ${item.views > item.average_7d ? '↑ 높음' : item.views < item.average_7d ? '↓ 낮음' : '→ 같음'}`;
  }
  const ratio = numeric(item.views) && numeric(item.followers) && item.followers > 0 ? ` · 팔로워 대비 조회율 ${number(item.views / item.followers * 100)}%` : '';
  return `<li><b>${esc(item.channel || '채널 미확인')}</b> ${numeric(item.posts) ? `${number(item.posts)}편 · ` : ''}조회 ${number(item.views)}${ratio} <span>→ ${esc(comparison)}</span>${item.interpretation ? `<small>→ ${esc(plain(item.interpretation))}</small>` : ''}</li>`;
}

export function renderDailyReport(report = {}, today = todaySeoul()) {
  const view = dailyView(report, today);
  const decisions = view.decisions.length ? `<ul class="mk-decisions">${view.decisions.map(decision).join('')}</ul>` : empty(view.structured ? '오늘 대표님 할 일 없음' : '대표 할 일 확인 필요 · 기존 보고서의 담당자 분류가 아직 없습니다.');
  const extra = view.extraDecisions.length ? `<details><summary>추가 결정 ${view.extraDecisions.length}건</summary><ul>${view.extraDecisions.map(decision).join('')}</ul></details>` : '';
  const posts = view.posts.length ? `<div class="mk-table-wrap"><table class="mk-table"><thead><tr><th>채널</th><th>시각</th><th>한 줄 제목</th><th>상태</th></tr></thead><tbody>${view.posts.map((p, i) => {
    const states = { scheduled: '예약됨', published: '올라감', needs_click: '대표 클릭 필요', blocked: '막힘', '예약됨': '예약됨', '올라감': '올라감', '대표 클릭 필요': '대표 클릭 필요', '막힘': '막힘' };
    const status = states[p.status] || '확인 필요';
    return `<tr><td>${esc(p.channel || '미확인')}</td><td>${esc(p.time || '미정')}</td><td><b>${esc(plain(p.title || '제목 확인 필요'))}</b>${p.post_script ? `<details class="mk-script"><summary>대본 보기·복사</summary><pre>${esc(p.post_script)}</pre><button type="button" class="secondary" data-mk="copy-script" data-post="${i}">대본 복사</button></details>` : ''}</td><td><span class="mk-state" data-state="${status === '막힘' ? 'blocked' : status === '올라감' ? 'published' : 'pending'}">${esc(status)}</span>${p.reason ? `<small>${esc(plain(p.reason))}</small>` : ''}${url(p.url) ? `<small><a href="${esc(url(p.url))}" target="_blank" rel="noopener noreferrer">게시물 확인 ↗</a></small>` : ''}</td></tr>`;
  }).join('')}</tbody></table></div><p class="mk-note">시각은 한국 시간 기준 · 예약됨은 게시 완료가 아닙니다.</p>` : empty('게시 일정 확인 필요 · 이 보고서에 등록된 일정이 없습니다.');
  const blockers = view.blockers.length ? `<section class="mk-block mk-blockers"><h3>D. 막힌 것·이상 신호</h3><ul>${view.blockers.map(b => `<li><b>${esc(plain(b.reason || '원인 확인 필요'))}</b><small>담당 ${esc(b.owner || '담당 확인 필요')} · 기한 ${esc(b.deadline || '미정')}</small></li>`).join('')}</ul></section>` : '';
  const benchmarkDate = view.benchmarkDate ? `마지막 갱신 ${esc(view.benchmarkDate)}` : '갱신일 미확인';
  const benchmark = `<details class="mk-block mk-benchmark"><summary>E. 벤치마크 <span>주 1회 갱신 · 상위 3건</span></summary><p class="mk-note">${benchmarkDate} · 팔로워 대비 조회율 순</p>${view.reels.length ? `<ol>${view.reels.map(r => `<li><b>@${esc(r.handle)}</b> · ${url(r.permalink) ? `<a href="${esc(url(r.permalink))}" target="_blank" rel="noopener noreferrer">${esc(plain(r.caption || '영상 보기'))} ↗</a>` : esc(plain(r.caption || '제목 미확인'))}<small>조회 ${number(r.views)} · 팔로워 대비 조회율 ${numeric(r.ratio) ? `${number(r.ratio * 100)}%` : '미확인'}</small></li>`).join('')}</ol>` : empty('벤치마크 자료가 없습니다.')}<p>→ ${esc(plain(view.takeaway || '우리 콘텐츠에 적용할 내용은 아직 작성되지 않았습니다.'))}</p></details>`;
  const legacy = !view.structured ? `<details class="mk-block"><summary>기존 보고서·제작 자료</summary><p class="mk-legacy">${esc(report.summary || '요약 없음')}</p>${list(report.directives).map(d => `<details class="mk-script"><summary>${esc(d.target || '제작 자료')} 보기</summary><pre>${esc(d.action || '')}</pre><p>${esc(d.why || '')}</p></details>`).join('')}</details>` : '';
  return `<div class="mk-daily">${view.stale ? `<p class="mk-stale" role="status">지난 보고서 · ${esc(view.date)} 기준입니다. 오늘 일정과 다를 수 있습니다.</p>` : ''}${section('A. 오늘 결정할 것', decisions + extra)}${section('B. 오늘 올라가는 것', posts)}${section(`C. 어제 성적 <small>${esc(view.previousDate)}</small>`, view.results.length ? `<ul class="mk-results">${view.results.map(result).join('')}</ul>` : empty('전날 성과 자료 없음 · 조회수와 7일 평균을 확인해 주세요.'))}${blockers}${benchmark}${legacy}<p class="mk-copy-message" role="status" aria-live="polite"></p></div>`;
}
