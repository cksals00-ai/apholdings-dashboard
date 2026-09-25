import { createInvestment } from './investment.js?v=1.7-investment-ai';
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.116.0/+esm';

const SUPABASE_URL = 'https://cgijpcimixaregbpvqbf.supabase.co';
const SUPABASE_KEY = 'sb_publishable_68JEef0wu8PIRAF9wXvuvQ_7jyd1zzv';
const OWNER_EMAIL = 'cksals00@gmail.com';
const RECOVERY_REDIRECT = `${window.location.origin}/admin/`;
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: 'implicit' } });

const BUSINESSES = {
  CORPORATE: 'Corporate',
  DECISION_INTELLIGENCE: 'Decision Intelligence',
  COMMERCE: 'Commerce',
  PLAY_LEARN: 'Play & Learn'
};
const STATUSES = {
  TODO: '해야 할 일',
  IN_PROGRESS: '진행 중',
  WAITING: '기다릴 일',
  ON_HOLD: '보류',
  CANCELLED: '취소',
  DONE: '완료'
};
const STATUS_ORDER = Object.keys(STATUSES);
let items = [];
let currentUser = null;
let recoveryMode = false;
let tradingGeneration = 0;
let tradingLoaded = false;
let tradingLoading = false;

const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value = '') => String(value).replace(/[&<>'"]/g, (char) => ({ '&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;' }[char]));
const formatDate = (value) => value ? new Intl.DateTimeFormat('ko-KR', { month:'short', day:'numeric' }).format(new Date(`${value}T00:00:00`)) : '미정';
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

function setAuthView(loggedIn) {
  if (!loggedIn) { clearTradingDocument(); investment.clear(); clearCommerce(); }
  $('#login-view').hidden = loggedIn;
  $('#app-view').hidden = !loggedIn;
}

function showAuthForm(name) {
  $('#login-form').hidden = name !== 'login';
  $('#recovery-form').hidden = name !== 'recovery';
  $('#new-password-form').hidden = name !== 'new-password';
  $('#login-title').textContent = name === 'new-password' ? '관리자 비밀번호 설정' : '사업 진행 현황';
}

async function verifyOwner(session) {
  if (!session?.user || session.user.email?.toLowerCase() !== OWNER_EMAIL) return false;
  const { error } = await supabase.from('admin_portfolio_items').select('id').limit(1);
  return !error;
}

async function initialize() {
  populateSelects();
  const { data: { session } } = await supabase.auth.getSession();
  if (recoveryMode && session?.user?.email?.toLowerCase() === OWNER_EMAIL) {
    currentUser = session.user;
    setAuthView(false);
    showAuthForm('new-password');
    return;
  }
  if (await verifyOwner(session)) {
    currentUser = session.user;
    setAuthView(true);
    $('#user-email').textContent = currentUser.email;
    await Promise.all([loadItems(), loadNotionStatus()]);
  } else {
    if (session) await supabase.auth.signOut();
    setAuthView(false);
  }
}

supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_OUT') {
    currentUser = null;
    setAuthView(false);
  }
  if (event === 'PASSWORD_RECOVERY') {
    recoveryMode = true;
    currentUser = session?.user || null;
    setAuthView(false);
    showAuthForm('new-password');
  }
});

$('#login-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  $('#login-message').textContent = '';
  const { data, error } = await supabase.auth.signInWithPassword({ email: OWNER_EMAIL, password: $('#password').value });
  if (error || !(await verifyOwner(data.session))) {
    await supabase.auth.signOut();
    $('#login-message').textContent = '로그인 정보가 맞지 않거나 관리자 권한이 없습니다.';
    button.disabled = false;
    return;
  }
  currentUser = data.user;
  $('#password').value = '';
  $('#user-email').textContent = currentUser.email;
  setAuthView(true);
  button.disabled = false;
  await Promise.all([loadItems(), loadNotionStatus()]);
});

$('#forgot-password').addEventListener('click', () => showAuthForm('recovery'));
document.querySelectorAll('[data-back-login]').forEach((button) => button.addEventListener('click', () => showAuthForm('login')));

$('#recovery-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  $('#recovery-message').textContent = '';
  const { error } = await supabase.auth.resetPasswordForEmail(OWNER_EMAIL, { redirectTo: RECOVERY_REDIRECT });
  $('#recovery-message').textContent = error
    ? '메일을 보내지 못했습니다. 잠시 후 다시 시도해 주세요.'
    : '재설정 메일을 보냈습니다. 받은 메일의 링크를 눌러 새 비밀번호를 설정해 주세요.';
  button.disabled = false;
});

$('#new-password-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const password = $('#new-password').value;
  const confirmPassword = $('#new-password-confirm').value;
  const message = $('#new-password-message');
  if (password !== confirmPassword) { message.textContent = '비밀번호가 서로 일치하지 않습니다.'; return; }
  const button = event.submitter;
  button.disabled = true;
  const { error } = await supabase.auth.updateUser({ password });
  if (error) {
    message.textContent = '비밀번호를 저장하지 못했습니다. 재설정 링크를 다시 받아 주세요.';
    button.disabled = false;
    return;
  }
  recoveryMode = false;
  history.replaceState({}, '', '/admin/');
  await supabase.auth.signOut({ scope: 'local' });
  $('#new-password-form').reset();
  showAuthForm('login');
  $('#login-message').textContent = '비밀번호가 설정됐습니다. 새 비밀번호로 로그인해 주세요.';
  button.disabled = false;
});

$('#logout').addEventListener('click', async () => { await supabase.auth.signOut(); items = []; assets = []; assetsLoaded = false; currentUser = null; setAuthView(false); });

async function loadItems() {
  $('.workspace').classList.add('loading');
  const { data, error } = await supabase.from('admin_portfolio_items').select('*').order('sort_order').order('created_at');
  $('.workspace').classList.remove('loading');
  if (error) { alert('진행 현황을 불러오지 못했습니다. 다시 로그인해 주세요.'); return; }
  items = data || [];
  render();
}

function filteredItems() {
  const business = $('#business-filter').value;
  const status = $('#status-filter').value;
  const query = $('#search-filter').value.trim().toLowerCase();
  return items.filter((item) =>
    (business === 'ALL' || item.business_unit === business) &&
    (status === 'ALL' || item.status === status) &&
    (!query || `${item.product} ${item.title} ${item.description}`.toLowerCase().includes(query))
  );
}

function render() {
  const visible = filteredItems();
  renderSummary(visible);
  renderBusinessSummary(visible);
  renderPriority(visible);
  renderGantt(visible);
  renderBoard(visible);
}

function renderSummary(list) {
  const values = [
    ['전체 Action', list.length, '현재 필터 기준'],
    ['진행 중', list.filter((x) => x.status === 'IN_PROGRESS').length, '직접 실행'],
    ['기다릴 일', list.filter((x) => x.status === 'WAITING').length, '외부 입력·승인'],
    ['보류·취소', list.filter((x) => ['ON_HOLD','CANCELLED'].includes(x.status)).length, '우선순위 제외'],
    ['완료', list.filter((x) => x.status === 'DONE').length, '검증·정리 완료']
  ];
  $('#summary-cards').innerHTML = values.map(([label,value,note]) => `<article class="summary-card"><span>${label}</span><b>${value}</b><small>${note}</small></article>`).join('');
}

function renderBusinessSummary(list) {
  $('#business-summary').innerHTML = Object.entries(BUSINESSES).map(([key,label]) => {
    const rows = list.filter((x) => x.business_unit === key);
    const progress = rows.length ? Math.round(rows.reduce((sum,x) => sum + x.progress, 0) / rows.length) : 0;
    return `<div class="business-row"><span class="business-name">${label}</span><div class="progress-track"><div class="progress-bar" style="width:${progress}%"></div></div><span class="business-value">${progress}%</span></div>`;
  }).join('');
}

function renderPriority(list) {
  const rank = { CRITICAL:0, HIGH:1, MEDIUM:2, LOW:3 };
  const active = list.filter((x) => !['DONE','CANCELLED'].includes(x.status)).sort((a,b) => rank[a.priority]-rank[b.priority] || (a.end_date||'9999').localeCompare(b.end_date||'9999')).slice(0,6);
  $('#priority-list').innerHTML = active.length ? active.map((item) => `<article class="priority-item" data-edit="${item.id}"><div class="meta"><span class="tag" data-status="${item.status}">${STATUSES[item.status]}</span><span>${escapeHtml(item.product)}</span><span>${formatDate(item.end_date)}</span></div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.next_action || item.dependency || '다음 행동을 입력하세요.')}</p></article>`).join('') : '<p class="empty">표시할 Action이 없습니다.</p>';
}

function renderBoard(list) {
  $('#status-board').innerHTML = STATUS_ORDER.map((status) => {
    const rows = list.filter((x) => x.status === status);
    return `<section class="status-column"><div class="status-column-head"><h2>${STATUSES[status]}</h2><span class="status-column-count">${rows.length}</span></div><div class="task-stack">${rows.map((item) => `<article class="task-card" data-edit="${item.id}"><div class="meta"><span>${escapeHtml(BUSINESSES[item.business_unit])}</span><span>${escapeHtml(item.product)}</span></div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.next_action || item.dependency || '')}</p><div class="progress-track"><div class="progress-bar" style="width:${item.progress}%"></div></div></article>`).join('') || '<p class="empty">없음</p>'}</div></section>`;
  }).join('');
}

function renderGantt(list) {
  const dated = list.filter((x) => x.start_date || x.end_date);
  if (!dated.length) { $('#gantt').innerHTML = '<p class="empty">기간이 입력된 Action이 없습니다.</p>'; return; }
  const dates = dated.flatMap((x) => [x.start_date,x.end_date]).filter(Boolean).map((x) => new Date(`${x}T00:00:00`));
  let start = new Date(Math.min(...dates)); let end = new Date(Math.max(...dates));
  start = new Date(start.getFullYear(), start.getMonth(), 1);
  end = new Date(end.getFullYear(), end.getMonth()+1, 0);
  const months = []; for (let d = new Date(start); d <= end; d.setMonth(d.getMonth()+1)) months.push(new Date(d));
  const span = Math.max(1, end - start);
  const monthHtml = months.map((d) => `<span class="gantt-month">${d.getFullYear()}.${String(d.getMonth()+1).padStart(2,'0')}</span>`).join('');
  const rows = dated.map((item) => {
    const s = new Date(`${item.start_date || item.end_date}T00:00:00`); const e = new Date(`${item.end_date || item.start_date}T23:59:59`);
    const left = clamp(((s-start)/span)*100,0,100); const width = clamp(((e-s)/span)*100,1.2,100-left);
    return `<div class="gantt-row"><div class="gantt-label"><b>${escapeHtml(item.product)}</b><span>${escapeHtml(item.title)}</span></div><div class="gantt-track"><button class="gantt-bar" data-edit="${item.id}" data-status="${item.status}" style="left:${left}%;width:${width}%" title="${escapeHtml(item.title)} · ${STATUSES[item.status]}">${item.progress}%</button></div></div>`;
  }).join('');
  $('#gantt').innerHTML = `<div class="gantt-grid" style="--months:${months.length}"><div class="gantt-head"><div class="gantt-label-head">제품 / Action</div><div class="gantt-months">${monthHtml}</div></div>${rows}</div>`;
}

function populateSelects() {
  $('#business-filter').insertAdjacentHTML('beforeend', Object.entries(BUSINESSES).map(([v,l]) => `<option value="${v}">${l}</option>`).join(''));
  $('#status-filter').insertAdjacentHTML('beforeend', Object.entries(STATUSES).map(([v,l]) => `<option value="${v}">${l}</option>`).join(''));
  $('#item-business').innerHTML = Object.entries(BUSINESSES).map(([v,l]) => `<option value="${v}">${l}</option>`).join('');
  $('#item-status').innerHTML = Object.entries(STATUSES).map(([v,l]) => `<option value="${v}">${l}</option>`).join('');
}

document.querySelectorAll('.filters select,.filters input').forEach((el) => el.addEventListener('input', render));
document.addEventListener('click', (event) => {
  const edit = event.target.closest('[data-edit]');
  if (edit) openDialog(items.find((x) => x.id === edit.dataset.edit));
  const nav = event.target.closest('[data-section]');
  if (nav) showSection(nav.dataset.section);
});

function showSection(name) {
  const investing = name === 'trading';
  document.querySelector('.workspace').classList.toggle('investment-mode', investing);
  document.querySelector('.topbar h1').textContent = investing ? '투자운용' : name === 'commerce' ? '커머스' : 'Portfolio Control Room';
  if (investing) investment.load();
  if (name === 'assets') loadAssets();
  if (name === 'commerce') loadCommerce();
  $('.filters').hidden = name === 'assets' || name === 'commerce';
  $('.top-actions').hidden = name === 'commerce';
  document.querySelectorAll('.view-section').forEach((section) => { section.hidden = section.id !== `${name}-section`; });
  document.querySelectorAll('.nav-item').forEach((item) => item.classList.toggle('active', item.dataset.section === name));
}

function openDialog(item = null) {
  $('#item-form').reset(); $('#item-message').textContent = '';
  $('#dialog-title').textContent = item ? 'Action 편집' : 'Action 추가';
  $('#delete-item').hidden = !item; $('#item-id').value = item?.id || '';
  $('#item-business').value = item?.business_unit || 'DECISION_INTELLIGENCE';
  $('#item-product').value = item?.product || '';
  $('#item-title').value = item?.title || '';
  $('#item-description').value = item?.description || '';
  $('#item-status').value = item?.status || 'TODO';
  $('#item-priority').value = item?.priority || 'MEDIUM';
  $('#item-start').value = item?.start_date || '';
  $('#item-end').value = item?.end_date || '';
  $('#item-progress').value = item?.progress ?? 0;
  $('#item-owner').value = item?.owner_name || 'Alfred Park';
  $('#item-dependency').value = item?.dependency || '';
  $('#item-next').value = item?.next_action || '';
  $('#item-dialog').showModal();
}

$('#add-button').addEventListener('click', () => openDialog());
document.querySelectorAll('[data-close]').forEach((button) => button.addEventListener('click', () => $('#item-dialog').close()));
$('#item-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const id = $('#item-id').value;
  const payload = {
    business_unit: $('#item-business').value, product: $('#item-product').value.trim(), title: $('#item-title').value.trim(),
    description: $('#item-description').value.trim(), status: $('#item-status').value, priority: $('#item-priority').value,
    start_date: $('#item-start').value || null, end_date: $('#item-end').value || null, progress: Number($('#item-progress').value),
    owner_name: $('#item-owner').value.trim() || 'Alfred Park', dependency: $('#item-dependency').value.trim(), next_action: $('#item-next').value.trim(),
    updated_by: currentUser.id, updated_at: new Date().toISOString()
  };
  const query = id ? supabase.from('admin_portfolio_items').update(payload).eq('id',id) : supabase.from('admin_portfolio_items').insert({ ...payload, created_by: currentUser.id });
  const { error } = await query;
  if (error) { $('#item-message').textContent = '저장하지 못했습니다. 날짜와 입력값을 확인해 주세요.'; return; }
  $('#item-dialog').close(); await loadItems();
});

$('#delete-item').addEventListener('click', async () => {
  const id = $('#item-id').value; if (!id || !confirm('이 Action을 삭제할까요?')) return;
  const { error } = await supabase.from('admin_portfolio_items').delete().eq('id',id);
  if (error) { $('#item-message').textContent = '삭제하지 못했습니다.'; return; }
  $('#item-dialog').close(); await loadItems();
});

async function loadNotionStatus() {
  const { data, error } = await supabase.from('admin_notion_connections').select('*').maybeSingle();
  const status = error ? 'ERROR' : (data?.status || 'CONFIG_REQUIRED');
  const labels = { NOT_CONNECTED:'연결 안 됨', CONFIG_REQUIRED:'OAuth 설정 필요', CONNECTED:'연결됨', ERROR:'확인 오류' };
  $('#notion-status').textContent = labels[status];
  $('#notion-message').textContent = status === 'CONNECTED' ? `마지막 동기화: ${data.last_synced_at ? new Date(data.last_synced_at).toLocaleString('ko-KR') : '아직 없음'}` : '';
}

async function startNotionConnection() {
  $('#notion-message').textContent = 'Notion OAuth 앱의 Client ID·Secret과 연결할 데이터베이스 승인이 필요합니다. 준비되면 이 버튼이 OAuth 승인 화면으로 연결됩니다.';
  showSection('settings');
}
$('#notion-button').addEventListener('click', startNotionConnection);
$('#notion-connect-main').addEventListener('click', startNotionConnection);
$('#notion-refresh').addEventListener('click', loadNotionStatus);

$('#change-password-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const password = $('#settings-password').value;
  const confirmPassword = $('#settings-password-confirm').value;
  const message = $('#change-password-message');
  if (password !== confirmPassword) { message.textContent = '비밀번호가 서로 일치하지 않습니다.'; return; }
  const button = event.submitter;
  button.disabled = true;
  message.textContent = '';
  const { error } = await supabase.auth.updateUser({ password });
  message.textContent = error ? '변경하지 못했습니다. 다시 로그인한 뒤 시도해 주세요.' : '비밀번호가 변경됐습니다.';
  if (!error) event.currentTarget.reset();
  button.disabled = false;
});

const investment = createInvestment(supabase, () => currentUser, () => {
  $('#trading-archive').open = true;
  loadTradingDocument();
  $('#trading-archive').scrollIntoView({ behavior: 'smooth' });
});
$('#trading-archive').addEventListener('toggle', () => { if ($('#trading-archive').open) loadTradingDocument(); });
initialize();


function clearTradingDocument() {
  tradingGeneration += 1;
  tradingLoaded = false;
  tradingLoading = false;
  const frame = $('#trading-document');
  frame.hidden = true;
  frame.removeAttribute('srcdoc');
  $('#trading-message').textContent = '';
  $('#trading-retry').hidden = true;
}

async function loadTradingDocument() {
  if (tradingLoaded || tradingLoading || !currentUser) return;
  tradingLoading = true;
  const generation = tradingGeneration;
  const userId = currentUser.id;
  const stillCurrent = () => generation === tradingGeneration && currentUser?.id === userId;
  $('#trading-message').textContent = '총람을 불러오는 중입니다…';
  $('#trading-retry').hidden = true;
  try {
    const { data, error } = await supabase.from('admin_trading_documents')
      .select('key_hex,sha256').eq('id', 'overview-20260925').single();
    if (error || !data) throw new Error('document-access');
    const response = await fetch('/admin/trading-overview.enc.json?v=20260925', { cache: 'no-store' });
    if (!response.ok) throw new Error('document-fetch');
    const encrypted = await response.json();
    const decode = (value) => Uint8Array.from(atob(value), (c) => c.charCodeAt(0));
    const key = await crypto.subtle.importKey('raw',
      Uint8Array.from(data.key_hex.match(/.{2}/g), (byte) => parseInt(byte, 16)),
      'AES-GCM', false, ['decrypt']);
    const plaintext = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: decode(encrypted.iv) }, key, decode(encrypted.ciphertext));
    const digest = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', plaintext)), (b) => b.toString(16).padStart(2, '0')).join('');
    if (digest !== data.sha256) throw new Error('document-integrity');
    if (!stillCurrent()) return;
    const policy = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'">`;
    const html = new TextDecoder().decode(plaintext).replace(/<head[^>]*>/i, (head) => head + policy);
    $('#trading-document').srcdoc = html;
    $('#trading-document').hidden = false;
    $('#trading-message').textContent = '';
    tradingLoaded = true;
  } catch {
    if (!stillCurrent()) return;
    $('#trading-message').textContent = '총람을 불러오지 못했습니다. 로그인 상태와 연결을 확인한 뒤 다시 시도해 주세요.';
    $('#trading-retry').hidden = false;
  } finally {
    if (stillCurrent()) tradingLoading = false;
  }
}

$('#trading-retry').addEventListener('click', loadTradingDocument);


// ── 데이터 자산 원장 (2026-09-26) — admin_data_assets, 소유자만 읽고 쓴다 ──
const ASSET_PRODUCTS = { safe: '세이프리스트', light: '라이트리스트', common: '공통' };
const ASSET_KINDS = { public_db: '공공 원천 DB', derived: '가공 판정 DB', dictionary: '사전', rule: '판정 규칙', paper: '논문', other: '기타' };
const ASSET_STATUS = { active: '사용 중', planned: '예정', retired: '이전 버전' };
let assets = [];
let assetsLoaded = false;
const fmtNum = (n) => (n === null || n === undefined || n === '') ? '—' : Number(n).toLocaleString('ko-KR');
const fmtBig = (n) => n >= 10000 ? `${(n / 10000).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}만` : fmtNum(n);

async function loadAssets(force = false) {
  if (!currentUser || (assetsLoaded && !force)) { renderAssets(); return; }
  $('#asset-message').textContent = '불러오는 중입니다…';
  const { data, error } = await supabase.from('admin_data_assets').select('*').order('collected_on', { ascending: false, nullsFirst: false }).order('created_at', { ascending: false });
  if (error) { $('#asset-message').textContent = '데이터 자산을 불러오지 못했습니다. 다시 로그인해 주세요.'; return; }
  assets = data || []; assetsLoaded = true;
  $('#asset-message').textContent = '';
  renderAssets();
}

function visibleAssets() {
  const product = $('#asset-product').value, kind = $('#asset-kind').value, status = $('#asset-status').value;
  const q = $('#asset-search').value.trim().toLowerCase();
  return assets.filter((a) => (product === 'ALL' || a.product === product) && (kind === 'ALL' || a.kind === kind)
    && (status === 'ALL' || a.status !== 'retired')
    && (!q || `${a.title} ${a.provider || ''} ${a.source || ''} ${a.note || ''}`.toLowerCase().includes(q)));
}

function renderAssetCards() {
  const product = $('#asset-product').value;
  const live = assets.filter((a) => a.status === 'active' && (product === 'ALL' || a.product === product));
  const sum = (k) => live.filter((a) => a.kind === k).reduce((s, a) => s + Number(a.records || 0), 0);
  const cnt = (ks) => live.filter((a) => ks.includes(a.kind)).length;
  const cards = [
    ['공공 원천 DB', `${fmtBig(sum('public_db'))}행`, `${cnt(['public_db'])}종 · 식약처 등 전량 수집`],
    ['가공 판정 DB', `${fmtBig(sum('derived'))}건`, `${cnt(['derived'])}종 · 앱·AI 커넥터가 쓰는 자산`],
    ['사전 · 규칙', `${cnt(['dictionary', 'rule'])}종`, '오탐·누락을 잡아 온 판단 기준'],
    ['논문', `${cnt(['paper'])}편`, '분석해 쌓을 예정'],
    ['전체 기록', `${assets.length}건`, `이전 버전 포함 · 최신 ${assets.map((a) => a.collected_on || '').sort().pop() || '—'}`]
  ];
  $('#asset-cards').innerHTML = cards.map(([l, v, n]) => `<article class="summary-card"><span>${l}</span><b>${v}</b><small>${escapeHtml(n)}</small></article>`).join('');
}

function renderAssets() {
  renderAssetCards();
  const rows = visibleAssets();
  $('#asset-rows').innerHTML = rows.length ? rows.map((a) => `<tr data-asset="${a.id}" class="${a.status}">
    <td class="date">${a.collected_on || '—'}</td>
    <td>${ASSET_PRODUCTS[a.product] || a.product}</td>
    <td><span class="asset-kind" data-kind="${a.kind}">${ASSET_KINDS[a.kind] || a.kind}</span>${a.status !== 'active' ? `<div class="asset-growth">${ASSET_STATUS[a.status]}</div>` : ''}</td>
    <td class="title"><b>${escapeHtml(a.title)}</b>${a.note ? `<small>${escapeHtml(a.note)}</small>` : ''}</td>
    <td class="num">${fmtNum(a.records)} ${escapeHtml(a.unit || '')}${a.size_bytes ? `<div class="asset-growth">${(a.size_bytes / 1048576).toLocaleString('ko-KR', { maximumFractionDigits: 1 })} MB</div>` : ''}</td>
    <td>${escapeHtml(a.provider || '')}${a.source ? `<div class="asset-growth">${escapeHtml(a.source)}</div>` : ''}</td>
    <td>${escapeHtml(a.refresh || '—')}${a.as_of ? `<div class="asset-growth">기준 ${escapeHtml(a.as_of)}</div>` : ''}</td>
  </tr>`).join('') : '<tr><td colspan="7" class="empty">조건에 맞는 자산이 없습니다.</td></tr>';
}

function openAssetDialog(a = null) {
  $('#asset-form').reset(); $('#asset-form-message').textContent = '';
  $('#asset-dialog-title').textContent = a ? '자산 편집' : '자산 추가';
  $('#asset-delete').hidden = !a; $('#asset-id').value = a?.id || '';
  const set = (id, v) => { $(id).value = v ?? ''; };
  set('#asset-f-product', a?.product || ($('#asset-product').value !== 'ALL' ? $('#asset-product').value : 'safe'));
  set('#asset-f-kind', a?.kind || 'public_db'); set('#asset-f-title', a?.title); set('#asset-f-provider', a?.provider);
  set('#asset-f-source', a?.source); set('#asset-f-records', a?.records); set('#asset-f-unit', a?.unit);
  set('#asset-f-date', a?.collected_on || new Date().toISOString().slice(0, 10)); set('#asset-f-asof', a?.as_of);
  set('#asset-f-refresh', a?.refresh); set('#asset-f-status', a?.status || 'active'); set('#asset-f-license', a?.license);
  set('#asset-f-size', a?.size_bytes ? Math.round(a.size_bytes / 104857.6) / 10 : ''); set('#asset-f-location', a?.location);
  set('#asset-f-url', a?.url); set('#asset-f-note', a?.note);
  $('#asset-dialog').showModal();
}

function assetsToCsv(list) {
  const cols = ['collected_on', 'product', 'kind', 'status', 'title', 'provider', 'source', 'records', 'unit', 'size_bytes', 'as_of', 'refresh', 'license', 'url', 'note'];
  const cell = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
  return '\ufeff' + [cols.join(','), ...list.map((a) => cols.map((c) => cell(c === 'product' ? ASSET_PRODUCTS[a[c]] : c === 'kind' ? ASSET_KINDS[a[c]] : c === 'status' ? ASSET_STATUS[a[c]] : a[c])).join(','))].join('\n');
}

(function initAssets() {
  $('#asset-product').insertAdjacentHTML('beforeend', Object.entries(ASSET_PRODUCTS).map(([v, l]) => `<option value="${v}">${l}</option>`).join(''));
  $('#asset-kind').insertAdjacentHTML('beforeend', Object.entries(ASSET_KINDS).map(([v, l]) => `<option value="${v}">${l}</option>`).join(''));
  $('#asset-f-product').innerHTML = Object.entries(ASSET_PRODUCTS).map(([v, l]) => `<option value="${v}">${l}</option>`).join('');
  $('#asset-f-kind').innerHTML = Object.entries(ASSET_KINDS).map(([v, l]) => `<option value="${v}">${l}</option>`).join('');
  ['#asset-product', '#asset-kind', '#asset-status', '#asset-search'].forEach((s) => $(s).addEventListener('input', renderAssets));
  $('#asset-rows').addEventListener('click', (e) => { const tr = e.target.closest('[data-asset]'); if (tr) openAssetDialog(assets.find((a) => a.id === tr.dataset.asset)); });
  $('#asset-add').addEventListener('click', () => openAssetDialog());
  document.querySelectorAll('[data-asset-close]').forEach((b) => b.addEventListener('click', () => $('#asset-dialog').close()));
  $('#asset-export').addEventListener('click', () => {
    const blob = new Blob([assetsToCsv(visibleAssets())], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `ap_data_assets_${new Date().toISOString().slice(0, 10)}.csv`; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  });
  $('#asset-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const id = $('#asset-id').value; const v = (s) => $(s).value.trim();
    const mb = v('#asset-f-size');
    const payload = {
      product: v('#asset-f-product'), kind: v('#asset-f-kind'), title: v('#asset-f-title'), provider: v('#asset-f-provider') || null,
      source: v('#asset-f-source') || null, records: v('#asset-f-records') === '' ? null : Number(v('#asset-f-records')), unit: v('#asset-f-unit') || null,
      collected_on: v('#asset-f-date') || null, as_of: v('#asset-f-asof') || null, refresh: v('#asset-f-refresh') || null,
      status: v('#asset-f-status'), license: v('#asset-f-license') || null, size_bytes: mb === '' ? null : Math.round(Number(mb) * 1048576),
      location: v('#asset-f-location') || null, url: v('#asset-f-url') || null, note: v('#asset-f-note') || null,
      updated_by: currentUser.id, updated_at: new Date().toISOString()
    };
    const q = id ? supabase.from('admin_data_assets').update(payload).eq('id', id) : supabase.from('admin_data_assets').insert({ ...payload, created_by: currentUser.id });
    const { error } = await q;
    if (error) { $('#asset-form-message').textContent = '저장하지 못했습니다. 입력값을 확인해 주세요.'; return; }
    $('#asset-dialog').close(); await loadAssets(true);
  });
  $('#asset-delete').addEventListener('click', async () => {
    const id = $('#asset-id').value; if (!id || !confirm('이 자산 기록을 삭제할까요? 이전 버전으로 두려면 상태를 바꾸세요.')) return;
    const { error } = await supabase.from('admin_data_assets').delete().eq('id', id);
    if (error) { $('#asset-form-message').textContent = '삭제하지 못했습니다.'; return; }
    $('#asset-dialog').close(); await loadAssets(true);
  });
})();



// ── 커머스 (2026-09-26) — admin_commerce_*, 소유자만 읽고 쓴다 ──
const CM_PARTNER_STATUS = { live: ['ok', '운영중'], approved: ['ok', '승인'], pending: ['warn', '승인대기'], applied: ['warn', '신청'], candidate: ['', '검토'], paused: ['', '중단'], rejected: ['bad', '거절'] };
const CM_SEVERITY = { blocking: ['bad', '막힘'], normal: ['warn', '보통'], watch: ['', '관찰'] };
const CM_EXCLUSIONS = [['chk_cosmetic', '화장품'], ['chk_kidfood', '아동식품'], ['chk_sono', '소노'], ['chk_travel_dup', '여행중복'], ['chk_medical', '의료기기']];
const CM_COMPLIANCE = [['chk_disclosure', '대가성'], ['chk_ai_notice', 'AI고지'], ['chk_info_tone', '정보형'], ['chk_screenshot', '스크린샷']];
let cmPartners = [], cmProducts = [], cmContent = [], cmBlockers = [], cmStats = [];
let commerceLoaded = false;
let commerceGeneration = 0;
const cmWon = (n) => Number(n || 0).toLocaleString('ko-KR');
const cmDate = (d) => d && /^\d{4}-\d{2}-\d{2}$/.test(d) && Number.isFinite(Date.parse(d)) ? new Intl.DateTimeFormat('ko-KR', { month: 'short', day: 'numeric' }).format(new Date(`${d}T00:00:00`)) : '—';
const cmPartnerName = (id) => cmPartners.find((p) => p.id === id)?.name || '—';
const cmTag = (cls, label) => `<span class="pill ${cls}">${escapeHtml(label)}</span>`;

function clearCommerce() {
  commerceGeneration += 1;
  commerceLoaded = false;
  cmPartners = []; cmProducts = []; cmContent = []; cmBlockers = []; cmStats = [];
  for (const id of ['commerce-cards', 'commerce-partners', 'commerce-products', 'commerce-content', 'commerce-blockers']) $('#' + id).innerHTML = '';
  $('#commerce-filter').innerHTML = '<option value="ALL">전체</option>';
  $('#commerce-imp-partner').innerHTML = '';
  $('#commerce-message').textContent = '';
}

async function cmReadAll(query) {
  const rows = [];
  for (let from = 0; ; from += 500) {
    const { data, error } = await query().range(from, from + 499);
    if (error) throw error;
    rows.push(...(data || []));
    if (!data || data.length < 500) return rows;
  }
}

async function loadCommerce(force = false) {
  if (!currentUser) return false;
  if (commerceLoaded && !force) { renderCommerce(); return true; }
  const generation = ++commerceGeneration;
  $('#commerce-message').textContent = '불러오는 중입니다…';
  const today = new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Seoul' });
  const since = new Date(Date.parse(today + 'T00:00:00Z') - 29 * 864e5).toISOString().slice(0, 10);
  try {
    const result = await Promise.all([
      cmReadAll(() => supabase.from('admin_commerce_partners').select('*').order('sort_order').order('id')),
      cmReadAll(() => supabase.from('admin_commerce_products').select('*').order('created_at').order('id')),
      cmReadAll(() => supabase.from('admin_commerce_content').select('*').order('created_at').order('id')),
      cmReadAll(() => supabase.from('admin_commerce_blockers').select('*').eq('status', 'open').order('severity').order('due_on', { nullsFirst: false }).order('id')),
      cmReadAll(() => supabase.from('admin_commerce_stats').select('*').gte('stat_date', since).lte('stat_date', today).order('stat_date').order('partner_id').order('sub_id'))
    ]);
    if (generation !== commerceGeneration || !currentUser) return false;
    [cmPartners, cmProducts, cmContent, cmBlockers, cmStats] = result;
    commerceLoaded = true;
    const selected = $('#commerce-filter').value;
    const importer = $('#commerce-imp-partner').value;
    const opts = cmPartners.map((x) => `<option value="${escapeHtml(x.id)}">${escapeHtml(x.name)}</option>`).join('');
    $('#commerce-filter').innerHTML = `<option value="ALL">전체</option>${opts}`;
    $('#commerce-imp-partner').innerHTML = opts;
    if (cmPartners.some(x => x.id === selected)) $('#commerce-filter').value = selected;
    if (cmPartners.some(x => x.id === importer)) $('#commerce-imp-partner').value = importer;
    renderCommerce();
    $('#commerce-message').textContent = '';
    return true;
  } catch (error) {
    if (generation === commerceGeneration && currentUser) $('#commerce-message').textContent = '커머스 데이터를 불러오지 못했습니다. 연결과 접근 권한을 확인한 뒤 새로고침해 주세요.';
    return false;
  }
}

function renderCommerce() {
  const sum = (k) => cmStats.reduce((a, r) => a + Number(r[k] || 0), 0);
  const live = cmPartners.filter((x) => x.status === 'live').length;
  const posted = cmContent.filter((x) => x.status === 'posted').length;
  const cards = [
    ['운영 파트너', `${live} / ${cmPartners.length}`, '승인 나면 상태를 올립니다'],
    ['클릭', cmWon(sum('clicks')), '최근 30일'],
    ['구매', `${cmWon(sum('orders'))}건`, `전환 ${sum('clicks') ? (sum('orders') / sum('clicks') * 100).toFixed(2) : '0.00'}%`],
    ['수익', `${cmWon(sum('commission'))}원`, '최근 30일 · 세전'],
    ['막힌 것', `${cmBlockers.length}건`, `게시 ${posted}건`]
  ];
  $('#commerce-cards').innerHTML = cards.map(([l, v, n]) => `<article class="summary-card"><span>${l}</span><b>${v}</b><small>${escapeHtml(n)}</small></article>`).join('');

  $('#commerce-partners').innerHTML = cmPartners.map((x) => {
    const [cls, label] = CM_PARTNER_STATUS[x.status] || ['', x.status];
    const line = (k, v) => v ? `<small>${k} · ${escapeHtml(v)}</small>` : '';
    return `<article class="summary-card"><span>${escapeHtml(x.name)} ${cmTag(cls, label)}</span><b style="font-size:.95rem">${escapeHtml(x.region || '')}</b>${line('계정', x.account_id)}${line('요율', x.commission)}${line('채널', x.channels)}</article>`;
  }).join('') || '<p class="panel-note">등록된 파트너가 없습니다.</p>';

  $('#commerce-blockers').innerHTML = cmBlockers.map((x) => {
    const [cls, label] = CM_SEVERITY[x.severity] || ['', x.severity];
    return `<tr><td><b>${escapeHtml(x.title)}</b>${x.detail ? `<br><small>${escapeHtml(x.detail)}</small>` : ''}</td><td>${escapeHtml(cmPartnerName(x.partner_id))}</td><td>${escapeHtml(x.owner)}</td><td>${cmDate(x.due_on)}</td><td>${cmTag(cls, label)}</td></tr>`;
  }).join('') || '<tr><td colspan="5">막힌 것 없습니다.</td></tr>';

  const filter = $('#commerce-filter').value || 'ALL';
  const rows = cmProducts.filter((x) => filter === 'ALL' || x.partner_id === filter);
  $('#commerce-products').innerHTML = rows.map((x) => {
    const hit = CM_EXCLUSIONS.filter(([k]) => x[k]);
    const flags = hit.length ? hit.map(([, l]) => cmTag('bad', l)).join(' ') : cmTag('ok', '전항 통과');
    const st = { live: 'ok', approved: 'ok', candidate: 'warn' }[x.status] || '';
    return `<tr><td>${escapeHtml(x.name)}${x.note ? `<br><small>${escapeHtml(x.note)}</small>` : ''}</td><td>${escapeHtml(cmPartnerName(x.partner_id))}</td><td>${escapeHtml(x.linked_app || '—')}</td><td class="num">${x.product_price != null ? cmWon(x.product_price) : '—'}</td><td>${flags}</td><td>${cmTag(st, x.status)}</td><td>${cmSafeURL(x.tracking_url) ? `<a href="${escapeHtml(x.tracking_url)}" target="_blank" rel="nofollow sponsored noopener">열기</a>` : '—'}</td></tr>`;
  }).join('') || '<tr><td colspan="7">등록된 상품이 없습니다.</td></tr>';

  $('#commerce-content').innerHTML = cmContent.map((x) => {
    const chips = CM_COMPLIANCE.map(([k, l]) => cmTag(x[k] ? 'ok' : 'warn', l)).join(' ');
    const st = { posted: 'ok', ready: 'warn' }[x.status] || '';
    return `<tr><td>${cmSafeURL(x.post_url) ? `<a href="${escapeHtml(x.post_url)}" target="_blank" rel="noopener">${escapeHtml(x.title)}</a>` : escapeHtml(x.title)}</td><td>${escapeHtml(cmPartnerName(x.partner_id))}</td><td>${escapeHtml(x.channel)}</td><td>${x.dm_keyword ? `<code>${escapeHtml(x.dm_keyword)}</code>` : '—'}</td><td>${cmDate(x.posted_on)}</td><td>${chips}</td><td>${cmTag(st, x.status)}</td></tr>`;
  }).join('') || '<tr><td colspan="7">등록된 콘텐츠가 없습니다.</td></tr>';
}

$('#commerce-filter').addEventListener('change', renderCommerce);

function cmSafeURL(value) {
  try { return ['https:', 'http:'].includes(new URL(value).protocol); } catch { return false; }
}

function cmParseCSV(text) {
  const rows = []; let row = [], field = '', quoted = false, closed = false;
  text = text.replace(/^\uFEFF/, '');
  const finishField = () => { row.push(field.trim()); field = ''; closed = false; };
  const finishRow = () => { finishField(); if (row.some(v => v !== '')) rows.push(row); row = []; };
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else { quoted = false; closed = true; }
      } else field += ch;
    } else if (ch === ',') finishField();
    else if (ch === '\n' || ch === '\r') { if (ch === '\r' && text[i + 1] === '\n') i++; finishRow(); }
    else if (ch === '"' && !field.trim() && !closed) { field = ''; quoted = true; }
    else if (ch === '"' || (closed && ch.trim())) throw new Error('CSV 따옴표 형식이 올바르지 않습니다.');
    else if (!closed) field += ch;
  }
  if (quoted) throw new Error('CSV에 닫히지 않은 따옴표가 있습니다.');
  finishRow(); return rows;
}

function cmReportRows(text, partner_id) {
  const [head, ...records] = cmParseCSV(text);
  if (!head || !records.length) throw new Error('행이 없습니다.');
  const col = re => head.findIndex(h => re.test(h));
  const idx = { date: col(/날짜|일자|date/i), clicks: col(/클릭|click/i), orders: col(/구매\s*건|주문|건수|order/i), gross_amount: col(/합산|거래|매출|gross|^금액$/i), commission: col(/수익|커미션|수수료|commission/i), sub: col(/서브|채널|sub/i) };
  if (idx.date < 0 || idx.clicks < 0) throw new Error('날짜·클릭 열을 찾지 못했습니다. 기간별 리포트 CSV인지 확인해 주세요.');
  const keys = new Set();
  return records.map((cells, index) => {
    const fail = message => { throw new Error(`${index + 2}행: ${message}`); };
    if (cells.length !== head.length) fail('열 개수가 다릅니다.');
    const match = cells[idx.date].match(/^(\d{4})[-./]?\s?(\d{1,2})[-./]?\s?(\d{1,2})\.?$/);
    if (!match) fail('날짜 형식이 올바르지 않습니다.');
    const stat_date = `${match[1]}-${match[2].padStart(2, '0')}-${match[3].padStart(2, '0')}`;
    const date = new Date(stat_date + 'T00:00:00Z');
    if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0,10) !== stat_date) fail('존재하지 않는 날짜입니다.');
    const row = { partner_id, stat_date, sub_id: idx.sub >= 0 && cells[idx.sub] ? cells[idx.sub] : '기본값', source: 'csv' };
    const key = JSON.stringify([stat_date, row.sub_id]);
    if (keys.has(key)) fail('같은 날짜·서브ID가 중복됩니다. 합산 또는 정리한 뒤 다시 올려 주세요.');
    keys.add(key);
    for (const name of ['clicks', 'orders', 'gross_amount', 'commission']) {
      const value = idx[name] < 0 ? '' : cells[idx[name]].replace(/[,₩\s원]/g, '');
      if (value && !/^-?\d+(?:\.\d+)?$/.test(value)) fail('숫자 형식이 올바르지 않습니다.');
      row[name] = value === '' ? 0 : Number(value);
      if (!Number.isFinite(row[name]) || Math.abs(row[name]) > Number.MAX_SAFE_INTEGER) fail('숫자가 너무 큽니다.');
      if (!Number.isInteger(row[name])) fail('현재 실적 원장은 정수 단위만 저장합니다. 소수 금액은 확인 후 정리해 주세요.');
      if (['clicks', 'orders'].includes(name) && (row[name] < 0 || row[name] > 2147483647)) fail('클릭·주문 수 범위를 확인해 주세요.');
    }
    return row;
  });
}

$('#commerce-refresh').addEventListener('click', () => loadCommerce(true));
$('#commerce-file').addEventListener('change', async event => {
  const input = event.target, file = input.files?.[0];
  const partner_id = $('#commerce-imp-partner').value;
  if (!file) return;
  if (!currentUser || !partner_id) { $('#commerce-message').textContent = '로그인 상태와 선택한 파트너를 확인해 주세요.'; input.value = ''; return; }
  if (file.size > 5 * 1024 * 1024) { $('#commerce-message').textContent = '5MB 이하의 CSV 파일을 선택해 주세요.'; input.value = ''; return; }
  const userId = currentUser.id;
  const generation = commerceGeneration;
  const active = () => currentUser?.id === userId && generation === commerceGeneration;
  input.disabled = true;
  $('#commerce-imp-partner').disabled = true;
  $('#commerce-refresh').disabled = true;
  $('#commerce-message').textContent = '읽는 중입니다…';
  try {
    const buffer = await file.arrayBuffer();
    let text;
    try { text = new TextDecoder('utf-8', { fatal: true }).decode(buffer); }
    catch { text = new TextDecoder('euc-kr', { fatal: true }).decode(buffer); }
    const rows = cmReportRows(text, partner_id);
    if (!active()) return;
    $('#commerce-message').textContent = `${rows.length}행 저장 중입니다…`;
    const { error } = await supabase.from('admin_commerce_stats').upsert(rows, { onConflict: 'partner_id,stat_date,sub_id' });
    if (error) throw error;
    if (!active()) return;
    const refreshed = await loadCommerce(true);
    if (currentUser?.id !== userId) return;
    $('#commerce-message').textContent = `${rows.length}행 저장했습니다.${refreshed ? '' : ' 화면 갱신에 실패했습니다. 새로고침해 주세요.'}`;
  } catch (error) {
    if (active()) $('#commerce-message').textContent = `저장하지 못했습니다: ${error.message || error}`;
  } finally {
    input.value = ''; input.disabled = false;
    $('#commerce-imp-partner').disabled = false;
    $('#commerce-refresh').disabled = false;
  }
});
