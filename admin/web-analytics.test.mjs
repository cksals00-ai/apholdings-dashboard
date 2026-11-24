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

test('준비 상태와 실제 성과를 구분하며, 없는 수치를 그래프로 그리지 않는다',()=>{
 const setup=renderWebAnalytics();assert.ok(setup.includes('wa-journey'));assert.ok(setup.includes('설치 6 / 6'));assert.ok(setup.includes('wa-sites'));
 const missing=renderLiveReport({status:'credentials_required'});assert.ok(missing.includes('wa-empty'));assert.ok(!missing.includes('wa-bar-fill'));
 const live=renderLiveReport({status:'connected',sites:[{host:'sports.apholdings.kr',views:12},{host:'edu.apholdings.kr',views:null}],blogArrivals:3,checkedAt:'2026-10-29'});assert.ok(live.includes('wa-bar-fill'));assert.ok(live.includes('집계 대기'));assert.ok(live.includes('12건'));
});

test('머니 머지 리아 캠페인 도착·시작·로그인·등록·공유를 구분해 보여주고, 없으면 그리지 않는다',()=>{
 const live=renderLiveReport({status:'connected',sites:[{host:'www.apholdings.kr',views:40}],blogArrivals:null,checkedAt:'2026-10-29',moneyMerge:{arrivals:{instagram:12,tiktok:5,youtube:null,share:3,other:null},starts:30,gameOvers:25,loginClicks:6,loginBlocked:2,logins:4,submits:4,shares:7}});
 assert.ok(live.includes('wa-mm'));assert.ok(live.includes('20건'));assert.ok(live.includes('인스타 12건'));assert.ok(live.includes('랭킹 등록 4건'));assert.ok(live.includes('집계 대기'));
 const without=renderLiveReport({status:'connected',sites:[{host:'www.apholdings.kr',views:40}],blogArrivals:1,checkedAt:'2026-10-29'});assert.ok(!without.includes('wa-mm'));
 assert.ok(renderWebAnalytics().includes('money_merge'));
});
