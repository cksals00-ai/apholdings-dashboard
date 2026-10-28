import test from 'node:test';
import assert from 'node:assert/strict';
import { dailyView, renderDailyReport } from './marketing-daily.mjs';

const base = { report_date: '2026-10-28', sources: { daily: { decisions: [], posts: [], results: [], blockers: [] } } };
const report = daily => ({ ...base, sources: { daily: { ...base.sources.daily, ...daily } } });
const now = '2026-10-28';

test('only pending representative decisions appear; the first three fit the main view', () => {
  const decisions = [
    { title: '제작 완료', owner: '대표', status: 'done' },
    { title: '자동 제작', owner: 'Claude' },
    ...['한도 결정', '폼 확인', '소재 승인', '일정 승인'].map(title => ({ title, owner: '대표', status: 'pending' }))
  ];
  const view = dailyView(report({ decisions }), now);
  assert.deepEqual(view.decisions.map(d => d.title), ['한도 결정', '폼 확인', '소재 승인']);
  assert.equal(view.extraDecisions.length, 1);
  assert.doesNotMatch(renderDailyReport(report({ decisions }), now), /자동 제작|제작 완료/);
});
test('missing structured data is not a declaration that the representative has no work', () => {
  const html = renderDailyReport({ report_date: now, summary: '기존 보고', directives: [{ target: '오늘 게시물', action: '컷1 대본' }] }, now);
  assert.match(html, /대표 할 일 확인 필요/);
  assert.doesNotMatch(html, /오늘 대표님 할 일 없음/);
  assert.match(html, /<details[\s\S]*컷1 대본/);
  assert.match(renderDailyReport(base, now), /오늘 대표님 할 일 없음/);
});
test('yesterday excludes reports published today and comparisons preserve verified zero', () => {
  const results = [
    { channel: '인스타', metric_date: '2026-10-28', views: 246, followers: 800 },
    { channel: '틱톡', metric_date: '2026-10-27', views: 150, average_7d: 100, posts: 1 },
    { channel: '유튜브', metric_date: '2026-10-27', views: 0, average_7d: 0 },
    { channel: '기타', metric_date: '2026-10-27', views: null, average_7d: 100 }
  ];
  const html = renderDailyReport(report({ results }), now);
  assert.match(html, /150/); assert.match(html, /7일 평균 100/); assert.match(html, /↑/);
  assert.doesNotMatch(html, /246/); assert.match(html, /조회 0/); assert.match(html, /조회 미확인/);
  assert.doesNotMatch(html, /NaN|Infinity|undefined/);
});
test('no average means no invented good or bad judgment and incomplete data means no comparison', () => {
  const html = renderDailyReport(report({ results: [{ channel: '틱톡', metric_date: '2026-10-27', views: 150, average_7d: '', followers: 0 }] }), now);
  assert.match(html, /비교 자료 없음/); assert.doesNotMatch(html, /↑|↓|Infinity/);
});
test('a daily total across multiple posts cannot be compared to a per-post average', () => {
  const html = renderDailyReport(report({ results: [{ channel: '틱톡', metric_date: '2026-10-27', posts: 3, views: 300, average_7d: 100 }] }), now);
  assert.match(html, /비교 자료 없음/); assert.doesNotMatch(html, /↑/);
});
test('partial versioned payload cannot falsely declare that there is no representative work', () => {
  const html = renderDailyReport({ ...base, sources: { daily: { version: 1 } } }, now);
  assert.match(html, /대표 할 일 확인 필요/);
});
test('empty blockers are hidden, unresolved blockers carry cause, owner and deadline', () => {
  assert.doesNotMatch(renderDailyReport(base, now), /D\. 막힌 것/);
  const html = renderDailyReport(report({ blockers: [{ reason: '한도 초과', owner: '대표', deadline: '2026-10-30' }, { reason: '해결됨', status: 'resolved' }] }), now);
  assert.match(html, /D\. 막힌 것/); assert.match(html, /한도 초과/); assert.match(html, /2026-10-30/);
  assert.doesNotMatch(html, /해결됨/);
});
test('scripts stay in closed details; unknown posting status never becomes scheduled', () => {
  const html = renderDailyReport(report({ posts: [{ channel: '틱톡', time: '18:00', title: '공연 퀴즈', post_script: '컷1\n컷2' }] }), now);
  assert.match(html, /<details class="mk-script">/); assert.match(html, /대본 보기·복사/);
  assert.match(html, /확인 필요/); assert.doesNotMatch(html, /<details[^>]* open|>예약됨</);
});
test('benchmark ranks only three reels and never turns report dates into fresh weekly checks', () => {
  const r = { ...base, top_reels: [10, 40, 30, 20].map((views, i) => ({ handle: `account${i}`, views, ratio: views / 100, caption: '퀴즈', permalink: 'javascript:alert(1)' })) };
  const html = renderDailyReport(r, '2026-11-06');
  assert.match(html, /지난 보고서/); assert.match(html, /갱신일 미확인/);
  assert.doesNotMatch(html, /account0|href="javascript:/);
});
test('untrusted titles, scripts, URLs and statuses cannot inject markup', () => {
  const html = renderDailyReport(report({ posts: [{ title: '<img src=x onerror=alert(1)>', post_script: '</pre><script>alert(1)</script>', url: 'javascript:alert(1)', status: '" onmouseover="x' }] }), now);
  assert.doesNotMatch(html, /<img|<script|href="javascript:|onmouseover="/);
  assert.match(html, /&lt;img/);
});
