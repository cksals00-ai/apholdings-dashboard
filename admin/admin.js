import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.116.0/+esm';

const SUPABASE_URL = 'https://cgijpcimixaregbpvqbf.supabase.co';
const SUPABASE_KEY = 'sb_publishable_68JEef0wu8PIRAF9wXvuvQ_7jyd1zzv';
const OWNER_EMAIL = 'cksals00@gmail.com';
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, detectSessionInUrl: true } });

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

const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value = '') => String(value).replace(/[&<>'"]/g, (char) => ({ '&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;' }[char]));
const formatDate = (value) => value ? new Intl.DateTimeFormat('ko-KR', { month:'short', day:'numeric' }).format(new Date(`${value}T00:00:00`)) : '미정';
const clamp = (value, min, max) => Math.max(min, Math.min(max, value));

function setAuthView(loggedIn) {
  $('#login-view').hidden = loggedIn;
  $('#app-view').hidden = !loggedIn;
}

async function verifyOwner(session) {
  if (!session?.user || session.user.email?.toLowerCase() !== OWNER_EMAIL) return false;
  const { error } = await supabase.from('admin_portfolio_items').select('id').limit(1);
  return !error;
}

async function initialize() {
  populateSelects();
  const { data: { session } } = await supabase.auth.getSession();
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

$('#logout').addEventListener('click', async () => { await supabase.auth.signOut(); items = []; currentUser = null; setAuthView(false); });

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

initialize();
