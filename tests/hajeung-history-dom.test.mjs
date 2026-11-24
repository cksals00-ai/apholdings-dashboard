import {test} from 'node:test';import assert from 'node:assert/strict';import {JSDOM} from 'jsdom';import {createChangeHistory} from '../hajeung/change-history.mjs';
test('history form saves once, shows readback, preserves existing and clears on logout',async()=>{
 const dom=new JSDOM('<div id="history"></div>',{url:'https://www.apholdings.kr/hajeung/'});globalThis.document=dom.window.document;
 const rows=[{id:'old',occurred_on:'2026-10-29',status:'customer_check',title:'기준 버전',detail:'<script>not html</script>',kind:'release',platform:'both',created_at:new Date().toISOString(),actor:'owner'}],notices=[];let saved,current=true;
 const client={from:()=>({select:()=>({order:()=>({limit:async()=>({data:[...rows]})})})}),rpc:async(name,{p})=>{saved=p;rows.unshift({...p,id:'new',created_at:new Date().toISOString(),actor:'owner'});return{data:'new'}}};
 const root=document.querySelector('#history'),ui=createChangeHistory(root,client,()=>current,(...x)=>notices.push(x));await ui.load();assert.equal(root.querySelector('script'),null);let form=root.querySelector('form');
 form.elements.title.value='변경 기록';form.elements.detail.value='고객 요청에 따른 수정 내용';form.elements.status.value='done';await form.onsubmit({preventDefault(){}});assert.equal(saved,undefined);assert.equal(notices.at(-1)[1],true);
 form.elements.status.value='customer_check';form.elements.apple_version.value='1.0(6)';await form.onsubmit({preventDefault(){}});assert.equal(saved.apple_version,'1.0(6)');assert.equal(rows.length,2);assert.match(root.textContent,/변경 기록/);assert.match(notices.at(-1)[0],/저장/);
 current=false;ui.clear();assert.equal(root.childElementCount,0);dom.window.close();
});
