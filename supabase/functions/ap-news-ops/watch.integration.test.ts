// @ts-nocheck -- deterministic boundary fakes; no real network or credentials.
import {strictEqual as assertEquals} from 'node:assert/strict';
Deno.test('server recovers without AI and emits only one exhausted daily failure',async()=>{
 const realDate=Date,realFetch=fetch,realServe=Deno.serve;let clock=+new realDate('2026-11-10T07:45:00+09:00'),handler;
 let attempts=0,requestedAt=null,dispatches=0,mails=0,provider=null,live=true,done=false;
 const reply=x=>new Response(JSON.stringify(x),{headers:{'Content-Type':'application/json'}});
 Deno.env.set('SUPABASE_URL','https://db.invalid');Deno.env.set('SUPABASE_SERVICE_ROLE_KEY','synthetic-service');Deno.env.set('AP_NEWS_GITHUB_DISPATCH_TOKEN','synthetic-github');Deno.env.set('AP_NEWS_MAIL_ENABLED','true');Deno.env.set('RESEND_API_KEY','synthetic-mail');
 globalThis.Date=class extends realDate {constructor(v){super(v===undefined?clock:v);}static now(){return clock;}};
 Deno.serve=h=>{handler=h;return {};};
 globalThis.fetch=async(input,init={})=>{
  const u=String(input),body=init.body?JSON.parse(init.body):{};
  if(u.includes('api.resend.com')){mails++;return reply({id:'one-provider-receipt'});}
  if(u.includes('api.github.com')){
   if(u.endsWith('/dispatches')){dispatches++;return new Response(null,{status:204});}
   return reply({total_count:1,workflow_runs:[{head_branch:'main',event:'workflow_dispatch',created_at:'2026-11-09T22:40:00Z',display_title:'AP News 2026-11-10 reservation',status:live?'in_progress':'completed',conclusion:'failure'}]});
  }
  if(u.includes('rpc/ap_news_admin_pipeline'))return reply({});
  if(u.includes('rpc/ap_news_delivery_health'))return reply({active:3,accepted:done?3:0,pending:0,processing:0,retry:0,failed:0,uncertain:0,unconfirmed:0,eligible_missing:done?0:3});
  if(u.includes('rpc/ap_news_publication_recovery_claim')){attempts++;requestedAt=new Date().toISOString();return reply(true);}
  if(u.includes('rpc/ap_news_ops_claim'))return reply(provider?{provider_id:provider,claimed:false}:{claimed:true,attempts:1});
  if(u.includes('ap_news_ops_events')&&init.method==='PATCH'){provider=body.provider_id;return reply([]);}
  if(u.includes('ap_news_ops_events'))return reply([]);
  if(u.includes('ap_news_publication_recovery'))return reply(attempts?[{attempts,updated_at:requestedAt}]:[]);
  if(u.includes('ap_news_publication_runs'))return reply([{ready_verified_at:'2026-11-10T07:00:00+09:00',public_verified_at:done?'2026-11-10T07:50:00+09:00':null}]);
  if(u.includes('ap_news_issues'))return reply(done?[{status:'published',verified:true}]:[]);
  if(u.includes('ap_news_subscribers'))return reply([{status:'active',confirmed_at:'2026-01-01'}]);
  throw Error('Unexpected network request '+u);
 };
 try{
  await import('./index.ts?integration');
  const tick=()=>handler(new Request('https://fn.invalid',{method:'POST',headers:{Authorization:'Bearer synthetic-admin'},body:'{"watch":true}'}));
  assertEquals((await tick()).status,200);assertEquals(dispatches,0);assertEquals(mails,0);
  live=false;
  for(let i=0;i<3;i++){clock+=180000;assertEquals((await tick()).status,200);}
  assertEquals(dispatches,3);assertEquals(mails,0);
  clock+=180000;await tick();await tick();assertEquals(mails,1);assertEquals(dispatches,3);
  done=true;clock+=180000;const r=await (await tick()).json();assertEquals(r.status,'complete');assertEquals(mails,1);assertEquals(dispatches,3);
 }finally{globalThis.Date=realDate;globalThis.fetch=realFetch;Deno.serve=realServe;}
});
