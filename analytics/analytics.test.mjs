import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=()=>readFileSync(new URL('./ap-analytics.js',import.meta.url),'utf8');
function run(url,ref='https://blog.naver.com/cksals00/224457592380') {
 const scripts=[],nodes=[],counts=[]; const doc={referrer:ref,head:{appendChild:x=>scripts.push(x)},body:{appendChild:x=>nodes.push(x)},createElement:()=>({setAttribute(){},appendChild(){},style:{}}),querySelector:()=>null};
 const w={URL,fetch:async (url,options)=>{counts.push({url,options});},location:new URL(url),document:doc,navigator:{globalPrivacyControl:false},setTimeout:()=>{},addEventListener(){}};w.window=w;
 vm.runInNewContext(source(),w);return {w,scripts,nodes,counts,calls:(w.dataLayer||[]).map(x=>Array.from(x))};
}
test('consent denied is queued before loading the tag and no automatic page view',()=>{
 const r=run('https://www.apholdings.kr/ko/?email=private@example.com');
 assert.equal(r.calls[0][0],'consent');assert.equal(r.calls[0][2].analytics_storage,'denied');
 const config=r.calls.find(x=>x[0]==='config');assert.equal(config[2].send_page_view,false);assert.equal(config[2].allow_google_signals,false);
 assert.equal(r.scripts.length,1); const event=r.calls.find(x=>x[1]==='page_view');assert.equal(event[2].page_location,'https://www.apholdings.kr/ko/'); assert.equal(event[2].page_referrer,'https://blog.naver.com/');assert.ok(!JSON.stringify(r.calls).includes('private@example'));
});
test('only exact promotion marks an arrival; no unique people claim or storage',()=>{
 const r=run('https://sports.apholdings.kr/?utm_source=naver&utm_medium=blog&utm_campaign=courtmate_intro_20261029&utm_content=224457592380');
 assert.equal(r.calls.filter(x=>x[1]==='courtmate_blog_arrival').length,1);
 assert.equal(run('https://sports.apholdings.kr/').calls.filter(x=>x[1]==='courtmate_blog_arrival').length,0);
 assert.ok(!/localStorage|sessionStorage|document\.cookie/.test(source()));
});
test('private, submission, unknown hosts, opt-out and install-test traffic do not count as public views',()=>{
 for(const u of ['https://www.apholdings.kr/admin/','https://www.apholdings.kr/hajeung/','https://sports.apholdings.kr/submit/','https://sports.apholdings.kr/qna/','https://evil.example/']) assert.equal(run(u).scripts.length,0);
 const r=run('https://www.apholdings.kr/ko/?_ap_analytics_test=1');assert.equal(r.calls.filter(x=>x[1]==='page_view').length,0);assert.equal(r.calls.filter(x=>x[1]==='ap_install_test').length,1);
});
test('머니 머지(/play)는 공개 조회로 세고, 도착 경로는 고정 목록 이름으로만 보낸다',()=>{
 const r=run('https://www.apholdings.kr/play/?utm_source=lia&utm_medium=instagram&utm_campaign=money_merge_launch');
 assert.equal(r.calls.filter(x=>x[1]==='page_view').length,1);
 assert.equal(r.calls.filter(x=>x[1]==='money_merge_arrival_instagram').length,1);
 const pv=r.calls.find(x=>x[1]==='page_view');assert.equal(pv[2].page_location,'https://www.apholdings.kr/play/');
 assert.equal(run('https://www.apholdings.kr/play/?utm_source=share&utm_medium=social').calls.filter(x=>x[1]==='money_merge_arrival_share').length,1);
 assert.equal(run('https://www.apholdings.kr/play/?utm_source=<b>x</b>').calls.filter(x=>x[1]==='money_merge_arrival_other').length,1);
 assert.equal(run('https://www.apholdings.kr/play/').calls.filter(x=>/money_merge_arrival/.test(x[1])).length,0);
 assert.equal(run('https://www.apholdings.kr/playground/').calls.filter(x=>x[1]==='page_view').length,0);
});

test('own count payload has only a fixed host and event, never URL input or identifiers',()=>{const r=run('https://sports.apholdings.kr/?utm_source=naver&utm_medium=blog&utm_campaign=courtmate_intro_20261029&utm_content=224457592380&email=secret@example.com');assert.equal(r.counts.length,2);assert.deepEqual(Object.keys(JSON.parse(r.counts[0].options.body)).sort(),['event','host']);assert.equal(r.counts[0].options.credentials,'omit');assert.equal(r.counts[0].options.referrerPolicy,'no-referrer');assert.ok(!JSON.stringify(r.counts).includes('secret@example'));});
