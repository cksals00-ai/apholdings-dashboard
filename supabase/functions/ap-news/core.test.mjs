import test from 'node:test';
import assert from 'node:assert/strict';
import { validateSubscription, canDeliver, escapeHtml, validateToken, freezeRequest } from './core.mjs';

test('동의 누락과 이메일 헤더 주입을 거절한다', () => {
  assert.throws(() => validateSubscription({ email: 'reader@example.com', consent: false }));
  assert.throws(() => validateSubscription({ email: 'a@example.com\nBcc:evil@example.com', consent: true }));
  assert.throws(() => validateSubscription({ email: 'broken', consent: true }));
  assert.deepEqual(validateSubscription({ email: ' Reader@Example.com ', consent: true }), { email: 'reader@example.com', name: '', locale: 'ko' });
});
test('확인 전, 해지, 이미 발송한 호, 비공개 호는 발송할 수 없다', () => {
  const issue = { status: 'published', verified: true };
  assert.equal(canDeliver({ status: 'pending' }, issue), false);
  assert.equal(canDeliver({ status: 'unsubscribed' }, issue), false);
  assert.equal(canDeliver({ status: 'active' }, { ...issue, status: 'draft' }), false);
  assert.equal(canDeliver({ status: 'active' }, issue, { state: 'sent' }), false);
  assert.equal(canDeliver({ status: 'active' }, issue), true);
});
test('토큰 형태를 제한하고 HTML 주입을 이스케이프한다', () => {
  assert.equal(validateToken('a'.repeat(64)), true);
  assert.equal(validateToken('short'), false);
  assert.equal(validateToken('<script>' + 'a'.repeat(56)), false);
  assert.equal(escapeHtml('<img src=x onerror="x">'), '&lt;img src=x onerror=&quot;x&quot;&gt;');
});
test('발행 내용이 수정되어도 재시도는 최초 제공사 요청을 유지한다', () => {
  const original={from:'AP News <alfred.park@apholdings.kr>',to:['reader@example.com'],subject:'Original',html:'First edition',headers:{}};
  const first=freezeRequest({payload:{}},original);
  const retry=freezeRequest({payload:{mail:first}},{...original,subject:'Corrected',html:'Updated'});
  assert.deepEqual(retry,original);
});
