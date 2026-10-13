import test from 'node:test';
import assert from 'node:assert/strict';
import {createNewsletter} from './newsletter.js';
test('신청자와 최신호를 축약하고 더보기 안에 목록을 표시하며 로그아웃 시 지운다',async()=>{
 const host={innerHTML:'',querySelector(){return {addEventListener(){}};},addEventListener(){},removeEventListener(){}};
 globalThis.document={querySelector(){return host;}};
 globalThis.fetch=async()=>({ok:true,json:async()=>({mail_ready:false,counts:{pending:1,active:0,unsubscribed:0},subscribers:[{id:'s',email:'person@example.com',name:'<script>alert(1)</script>',status:'pending',created_at:'2026-10-13T00:00:00Z'}],issues:[],deliveries:[{subscriber_id:'s',kind:'confirmation',state:'pending',attempts:0}],runtime:{}})});
 const module=createNewsletter({auth:{getSession:async()=>({data:{session:{access_token:'test'}}})}},()=>({id:'owner'}));
 await module.load();
 assert.match(host.innerHTML,/person@example.com/);
 assert.match(host.innerHTML,/&lt;script&gt;/);
 assert.doesNotMatch(host.innerHTML,/<script>/);
 assert.match(host.innerHTML,/<details/);
 assert.match(host.innerHTML,/data-news-search/);
 assert.match(host.innerHTML,/data-news-history/);
 module.clear();assert.equal(host.innerHTML,'');
});
