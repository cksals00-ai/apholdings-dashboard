(() => {
  const form = document.querySelector('#subscribe-form');
  const endpoint = form?.dataset.api;
  const state = document.querySelector('#subscribe-state');
  async function request(action, body) {
    const r = await fetch(`${endpoint}/${action}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), signal: AbortSignal.timeout(20000) });
    const result = await r.json();
    if (!r.ok) throw new Error(result.message || '요청을 처리하지 못했습니다. 잠시 후 다시 시도해주세요.');
    return result;
  }
  form?.addEventListener('submit', async event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const button = form.querySelector('button');button.disabled = true;
    state.textContent = '신청을 접수하고 있습니다.';
    try {
      const data = new FormData(form);
      const result = await request('subscribe', { email: data.get('email'), consent: data.get('consent') === 'on', website: data.get('website') });
      state.textContent = result.message;form.reset();
    } catch (e) { state.textContent = e.name === 'TimeoutError' ? '접수 여부를 확인하지 못했습니다. 잠시 후 다시 시도해주세요.' : (e.message === 'Failed to fetch' ? '연결을 확인하지 못했습니다. 잠시 후 다시 시도하거나 구독 문의로 연락해주세요.' : e.message); }
    finally { button.disabled = false; }
  });
  if (state) fetch(`${endpoint}/status`, { signal: AbortSignal.timeout(10000) }).then(r=>r.json()).then(s=>{
    if (s.storage_ready === false) { form.querySelector('button').disabled = true; state.textContent = '온라인 구독 접수를 준비하고 있습니다. 구독 문의로 연락해주세요.'; return; }
    if (!s.mail_ready) state.textContent = '이메일 발송 서비스를 준비하고 있습니다. 신청은 접수되며, 준비 후 확인 메일을 드립니다.';
  }).catch(()=>{});
  const manage = document.querySelector('#manage-state');
  const button = document.querySelector('#manage-action');
  if (manage && button) {
    // URL fragment keeps bearer tokens out of server logs and referrer headers.
    const params = new URLSearchParams(location.hash.slice(1));
    const action = params.get('action'), token = params.get('token'), id = params.get('id');
    history.replaceState(null, '', location.pathname);
    if (!['confirm','unsubscribe'].includes(action) || !/^[a-f0-9]{64}$/.test(token || '')) { manage.textContent = '유효한 구독 관리 링크가 아닙니다. 이메일의 링크를 다시 확인해주세요.';return; }
    manage.textContent = action === 'confirm' ? '아래 버튼을 누르면 AP News 구독이 시작됩니다.' : '아래 버튼을 누르면 AP News 수신이 중단됩니다.';
    button.hidden = false;button.textContent = action === 'confirm' ? '이메일 확인하고 구독 시작' : '구독 해지';
    button.addEventListener('click', async()=>{
      button.disabled=true;
      try {const result=await request(action,{token,id});manage.textContent=result.message;button.hidden=true;}
      catch(e){manage.textContent=e.message;button.disabled=false;}
    });
  }
})();
