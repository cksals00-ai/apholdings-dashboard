// Dependency-free component integration: not a substitute for visual browser QA.
import assert from 'node:assert/strict';
import fs from 'node:fs';
const path=process.argv[2];
if(!path)throw new Error('Pass an authorized private snapshot path (never commit it).');
const input=JSON.parse(fs.readFileSync(path,'utf8'));
const root={innerHTML:'',listener:null,addEventListener(event,fn){this.listener=fn;},replaceChildren(){this.innerHTML='';},querySelector(){return {focus(){}};}};
globalThis.document={getElementById:id=>{assert.equal(id,'plan-section');return root;}};
const {createBusinessPlan}=await import('../admin/business-plan.js');
let signedIn=true,resolvePending;
let queryCount=0;
const pending={
  from(table){
    assert.equal(table,'admin_business_plans');
    return {
      select(){return {
        eq(key,id){
          assert.equal(key,'id');assert.equal(id,'2026-10-five-year');
          return {maybeSingle(){queryCount++;return new Promise(resolve=>{resolvePending=resolve;});}};
        }
      };}
    };
  }
};
const widget=createBusinessPlan(pending,()=>signedIn?{id:'test-only'}:null);
const loading=widget.load();
assert.match(root.innerHTML,/불러오는 중/);
resolvePending({data:{payload:input},error:null});await loading;
assert.match(root.innerHTML,/10월 매출 목표/);assert.doesNotMatch(root.innerHTML,/NaN|undefined|Infinity/);
for(const key of Object.keys(input.scenarios))for(const tab of ['october','finance','value','evidence']){
  root.listener({target:{closest:()=>({dataset:{bpScenario:key}})}});
  root.listener({target:{closest:()=>({dataset:{bpTab:tab}})}});
  assert.doesNotMatch(root.innerHTML,/NaN|undefined|Infinity/);
  assert.match(root.innerHTML,/bp-footer/);
}
assert.equal(queryCount,1,'Tab/scenario changes use one authorized snapshot');
const refresh=widget.load(true);signedIn=false;widget.clear();
resolvePending({data:{payload:input},error:null});await refresh;
assert.equal(root.innerHTML,'','Late response must not restore private content after logout');
await widget.load();assert.equal(queryCount,2,'No query without authenticated user');
signedIn=true;const bad=widget.load();resolvePending({data:null,error:{message:'denied'}});await bad;
assert.match(root.innerHTML,/불러오지 못했습니다/);assert.doesNotMatch(root.innerHTML,/10월 매출 목표/);
const xss=structuredClone(input);xss.title='<img src=x onerror=alert(1)>';
const retry=widget.load(true);resolvePending({data:{payload:xss},error:null});await retry;
assert.ok(root.innerHTML.includes('&lt;img src=x onerror=alert(1)&gt;'));assert.ok(!root.innerHTML.includes('<img src=x'));
console.log('PASS: 12 scenario/tab states, no unauthorized query, denied access, retry, XSS escaping and logout race');
