import test from 'node:test';
import assert from 'node:assert/strict';
import { renderWebAnalytics, renderLiveReport } from './web-analytics.mjs';

test('설치 전 통계를 실적 0으로 표시하지 않고 사이트별 준비 상태를 구분한다', () => {
  const html = renderWebAnalytics();
  for (const host of ['www.apholdings.kr', 'edu.apholdings.kr', 'games.apholdings.kr', 'shop.apholdings.kr', 'sports.apholdings.kr']) assert.ok(html.includes(host));
  assert.ok(html.includes('6개 사이트 설치 확인'));
  assert.ok(html.includes('Google 통계 연결 확인 중'));
  assert.ok(html.includes('2026-10-29'));
  assert.ok(!html.includes('0명'));
  assert.ok(!html.includes('0회'));
});
test('계정 보고서와 실제 소개 글로 연결하고 관리자에게 비밀키를 노출하지 않는다', () => {
  const html = renderWebAnalytics();
  assert.ok(html.includes('a413956552p561381925'));
  assert.ok(html.includes('https://blog.naver.com/cksals00/224457592380'));
  assert.ok(html.includes('courtmate_intro_20261029'));
  assert.ok(html.includes('전용 링크 적용 완료'));
  assert.ok(!/api_secret|access_token|googletagmanager.com/.test(html));
});

test('연결 실패를 0회로 바꾸지 않고 API 출처와 도착 건수를 구분한다',()=>{assert.ok(!renderLiveReport({status:'credentials_required'}).includes('0건'));const html=renderLiveReport({status:'connected',sites:[{host:'sports.apholdings.kr',views:4}],blogArrivals:2,checkedAt:'2026-10-29'});assert.ok(html.includes('2건'));assert.ok(html.includes('사람 수 아님'));assert.ok(html.includes('Google Analytics Data API'));});
