(() => {
'use strict';
const form = document.getElementById('reset-form');
const password = document.getElementById('new-password');
const confirmation = document.getElementById('confirm-password');
const submit = document.getElementById('reset-submit');
const status = document.getElementById('reset-status');
// Recovery credentials live only in this closure; remove the URL before any API call.
const fragment = new URLSearchParams(location.hash.slice(1));
let accessToken = fragment.get('type') === 'recovery' ? fragment.get('access_token') : null;
fragment.delete('access_token');
fragment.delete('refresh_token');
history.replaceState(null, '', location.pathname);
let busy = false;
let completed = false;
function message(text, state) {
  status.textContent = text;
  status.dataset.state = state;
}
function lock(locked) {
  password.disabled = locked;
  confirmation.disabled = locked;
  submit.disabled = locked;
}
if (accessToken) {
  lock(false);
  message('새 비밀번호를 입력해 주세요.', 'ready');
} else {
  lock(true);
  message('유효한 재설정 링크가 없습니다. 앱에서 비밀번호 찾기를 다시 요청해 주세요.', 'error');
}
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (!accessToken || busy || completed) return;
  if (Array.from(password.value).length < 8 || password.value.length > 128) {
    message('비밀번호는 8자 이상, 128자 이하로 입력해 주세요.', 'error');
    password.focus();
    return;
  }
  if (password.value !== confirmation.value) {
    message('비밀번호가 일치하지 않습니다. 다시 확인해 주세요.', 'error');
    confirmation.focus();
    return;
  }
  busy = true;
  lock(true);
  message('새 비밀번호를 저장하고 있습니다.', 'working');
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch('https://cxwdrlrqhxpnpepzrths.supabase.co/auth/v1/user', {
      method: 'PUT',
      credentials: 'omit',
      referrerPolicy: 'no-referrer',
      headers: {'Content-Type': 'application/json', 'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4d2RybHJxaHhwbnBlcHpydGhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMTgxNjUsImV4cCI6MjEwNDg5NDE2NX0.wRxgeJlHaMWiIgacOwGVMoSQ1gbpCxKZ8D6EBI8OL_8', 'Authorization': 'Bearer ' + accessToken},
      body: JSON.stringify({password: password.value}),
      signal: controller.signal
    });
    if (response.ok) {
      accessToken = null;
      completed = true;
      password.value = '';
      confirmation.value = '';
      message('비밀번호를 변경했습니다. 앱으로 돌아가 새 비밀번호로 로그인해 주세요.', 'success');
    } else if (response.status === 401 || response.status === 403) {
      accessToken = null;
      message('링크가 만료되었거나 사용할 수 없습니다. 앱에서 비밀번호 찾기를 다시 요청해 주세요.', 'error');
    } else if (response.status === 429) {
      message('요청이 많습니다. 잠시 후 다시 시도해 주세요.', 'error');
    } else {
      // Never display raw server payloads, which may contain account details.
      message('비밀번호를 저장하지 못했습니다. 이전과 다른 비밀번호로 다시 시도해 주세요.', 'error');
    }
  } catch {
    message('연결을 확인할 수 없습니다. 잠시 후 다시 시도해 주세요.', 'error');
  } finally {
    clearTimeout(timeout);
    busy = false;
    lock(completed || !accessToken);
  }
});
window.addEventListener('pagehide', () => {
  accessToken = null;
  password.value = '';
  confirmation.value = '';
});
})();
