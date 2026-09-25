export function validateState(value) {
  if (!value || !Array.isArray(value.checks) || !Array.isArray(value.snapshots) || typeof value.notes !== 'string' || value.notes.length > 4000 || value.snapshots.length > 60) throw new Error('invalid-state');
  if (value.checks.some(v => !Number.isInteger(v) || v < 0 || v > 4) || new Set(value.checks).size !== value.checks.length) throw new Error('invalid-check');
  const dates = new Set();
  const snapshots = value.snapshots.map(s => {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s.asof) || Number.isNaN(Date.parse(s.asof)) || new Date(s.asof).toISOString().slice(0, 10) !== s.asof || dates.has(s.asof)) throw new Error('invalid-date');
    if (![s.nav, s.deposits, s.withdrawals].every(v => Number.isSafeInteger(v) && v >= 0 && v <= 1e12)) throw new Error('invalid-amount');
    dates.add(s.asof);
    return { asof: s.asof, nav: s.nav, deposits: s.deposits, withdrawals: s.withdrawals };
  });
  return { checks: [...value.checks], notes: value.notes, snapshots };
}

export function createInvestment(supabase, getUser, openArchive) {
  const frame = document.querySelector('#investment-dashboard');
  const message = document.querySelector('#investment-message');
  const retry = document.querySelector('#investment-retry');
  let generation = 0, loaded = false, loading = false, saving = false;
  function clear() {
    generation++; loaded = false; loading = false; saving = false;
    frame.hidden = true; frame.removeAttribute('srcdoc');
    message.textContent = ''; retry.hidden = true;
  }
  function send(data) { frame.contentWindow?.postMessage(data, '*'); }
  async function readState(epoch) {
    const { data, error } = await supabase.from('admin_investment_state').select('state,revision').eq('id', 'workspace').single();
    if (error || !data) throw new Error('state-read');
    const state = validateState(data.state);
    if (epoch === generation && getUser()) send({ type: 'ap-investment-state', state, revision: data.revision });
  }
  async function readAI(epoch) {
    try {
      const month = new Date().toISOString().slice(0, 7) + '-01T00:00:00Z';
      const results = await Promise.all([
        supabase.from('admin_investment_ai_runtime').select('status,detail,checked_at,monthly_budget_usd,model').eq('id', 'worker').maybeSingle(),
        supabase.from('admin_investment_ai_runs').select('kind,status,summary,source_asof,source_revision,model,created_at').order('created_at', { ascending: false }).limit(10),
        supabase.from('admin_investment_ai_runs').select('reserved_usd').gte('created_at', month)
      ]);
      if (results.some(r => r.error)) throw new Error('ai-read');
      if (epoch === generation && getUser()) send({ type: 'ap-investment-ai', runtime: results[0].data, runs: results[1].data || [], reserved: (results[2].data || []).reduce((sum, row) => sum + Number(row.reserved_usd || 0), 0) });
    } catch { if (epoch === generation && getUser()) send({ type: 'ap-investment-ai-error' }); }
  }
  window.addEventListener('message', async event => {
    if (event.source !== frame.contentWindow || !getUser() || !loaded) return;
    const m = event.data, epoch = generation;
    if (!m || typeof m.type !== 'string') return;
    try {
      if (m.type === 'ap-investment-ready') await Promise.all([readState(epoch), readAI(epoch)]);
      if (m.type === 'ap-investment-ai-refresh') await readAI(epoch);
      if (m.type === 'ap-investment-archive') openArchive();
      if (m.type === 'ap-investment-save') {
        if (saving) return;
        saving = true;
        const state = validateState(m.state);
        if (!Number.isSafeInteger(m.revision) || m.revision < 0) throw new Error('revision');
        const { data, error } = await supabase.from('admin_investment_state')
          .update({ state, revision: m.revision + 1 }).eq('id', 'workspace').eq('revision', m.revision).select('revision');
        if (error) throw new Error('save');
        if (!data?.length) {
          await readState(epoch);
          if (epoch === generation) send({ type: 'ap-investment-error', message: '다른 화면에서 기록이 변경됐습니다. 최신 내용을 불러왔으니 다시 입력해 주세요.' });
        } else await readState(epoch);
      }
    } catch {
      if (epoch === generation && getUser()) send({ type: 'ap-investment-error', message: '저장소 연결 또는 입력 확인에 실패했습니다. 화면을 새로고침한 뒤 다시 시도해 주세요.' });
    } finally { if (epoch === generation) saving = false; }
  });
  async function load() {
    if (loaded || loading || !getUser()) return;
    loading = true;
    const epoch = generation;
    message.textContent = '투자운용 화면을 불러오는 중입니다…'; retry.hidden = true;
    try {
      const { data, error } = await supabase.from('admin_trading_documents').select('key_hex,sha256').eq('id', 'investment-v2').single();
      if (error || !data) throw new Error('access');
      const response = await fetch('/admin/investment-v2.enc.json?v=20260926-2', { cache: 'no-store' });
      if (!response.ok) throw new Error('fetch');
      const encrypted = await response.json();
      const decode = v => Uint8Array.from(atob(v), c => c.charCodeAt(0));
      const key = await crypto.subtle.importKey('raw', Uint8Array.from(data.key_hex.match(/.{2}/g), b => parseInt(b, 16)), 'AES-GCM', false, ['decrypt']);
      const bytes = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: decode(encrypted.iv) }, key, decode(encrypted.ciphertext));
      const digest = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), b => b.toString(16).padStart(2, '0')).join('');
      if (digest !== data.sha256) throw new Error('integrity');
      if (epoch !== generation || !getUser()) return;
      const csp = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'">`;
      loaded = true;
      frame.srcdoc = new TextDecoder().decode(bytes).replace(/<head[^>]*>/i, h => h + csp);
      frame.hidden = false; message.textContent = '';
    } catch {
      if (epoch === generation) { message.textContent = '투자운용 화면을 불러오지 못했습니다. 다시 시도해 주세요.'; retry.hidden = false; }
    } finally { if (epoch === generation) loading = false; }
  }
  retry.addEventListener('click', load);
  return { load, clear };
}
