export const escapeHtml = (s = '') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function validateSubscription(input) {
  if (input?.consent !== true) throw new Error('동의 항목을 확인해주세요.');
  const email = String(input.email || '').trim().toLowerCase();
  if (email.length > 254 || !/^[^\s<>@,;:\\"\x00-\x1f]+@[^\s<>@,;:\\"\x00-\x1f]+\.[a-z]{2,63}$/i.test(email)) throw new Error('이메일 주소를 확인해주세요.');
  const name = String(input.name || '').trim().slice(0, 60);
  return { email, name, locale: 'ko' };
}
export function canDeliver(subscriber, issue, delivery) {
  return subscriber?.status === 'active' && issue?.status === 'published' && issue?.verified === true && !['sent','processing','uncertain'].includes(delivery?.state);
}
export const validateToken = s => typeof s === 'string' && /^[a-f0-9]{64}$/.test(s);
export const freezeRequest = (delivery, candidate) => structuredClone(delivery?.payload?.mail || candidate);
