import test from 'node:test';
import assert from 'node:assert/strict';
import { renderWebAnalytics } from './web-analytics.mjs';

test('설치 전 통계를 실적 0으로 표시하지 않고 사이트별 준비 상태를 구분한다', () => {
  const html = renderWebAnalytics();
  for (const host of ['www.apholdings.kr', 'edu.apholdings.kr', 'games.apholdings.kr', 'shop.apholdings.kr', 'sports.apholdings.kr']) assert.ok(html.includes(host));
  assert.ok(html.includes('사이트 태그 설치 전'));
  assert.ok(html.includes('통계 자동 연동 전'));
  assert.ok(html.includes('2026-10-29'));
  assert.ok(!html.includes('0명'));
  assert.ok(!html.includes('0회'));
});
test('계정 보고서와 실제 소개 글로 연결하고 관리자에게 비밀키를 노출하지 않는다', () => {
  const html = renderWebAnalytics();
  assert.ok(html.includes('a413956552p561381925'));
  assert.ok(html.includes('https://blog.naver.com/cksals00/224457592380'));
  assert.ok(html.includes('courtmate_intro_20261029'));
  assert.ok(html.includes('링크 교체 전'));
  assert.ok(!/api_secret|access_token|googletagmanager.com/.test(html));
});
