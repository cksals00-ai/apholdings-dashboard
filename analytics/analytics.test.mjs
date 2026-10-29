import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=()=>readFileSync(new URL('./ap-analytics.js',import.meta.url),'utf8');
function run(url,ref='https://blog.naver.com/cksals00/224457592380') {
 const scripts=[],nodes=[]; const doc={referrer:ref,head:{appendChild:x=>scripts.push(x)},body:{appendChild:x=>nodes.push(x)},createElement:()=>({setAttribute(){},appendChild(){},style:{}}),querySelector:()=>null};
 const w={URL,location:new URL(url),document:doc,navigator:{globalPrivacyControl:false},setTimeout:()=>{},addEventListener(){}};w.window=w;
 vm.runInNewContext(source(),w);return {w,scripts,nodes,calls:(w.dataLayer||[]).map(x=>Array.from(x))};
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
