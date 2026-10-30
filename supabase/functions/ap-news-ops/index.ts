import {assess} from './health.mjs';
// Operational mail only: fixed owner recipient, no subscriber queue mutation.
const URL=Deno.env.get('SUPABASE_URL')!,KEY=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const FROM='AP News <alfred.park@apholdings.kr>',TO='cksals00@naver.com';
const esc=(s:unknown)=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
async function db(path:string,method='GET',body?:unknown,token=KEY){
 const r=await fetch(`${URL}/rest/v1/${path}`,{method,headers:{apikey:KEY,Authorization:`Bearer ${token}`,'Content-Type':'application/json',Prefer:'return=representation'},body:body===undefined?undefined:JSON.stringify(body)});
 if(!r.ok)throw Error(`db_${r.status}`);return await r.json();
}
async function send(key:string,event:string,detail:Record<string,unknown>,html?:string,inject=false){
 const row=await db('rpc/ap_news_ops_claim','POST',{p_key:key,p_event:event,p_detail:detail});
 if(row.provider_id)return {accepted:true,id:row.provider_id,reused:true};
 if(!row.claimed)throw Error('operation_busy_or_exhausted');
 const patch=(data:unknown)=>db(`ap_news_ops_events?event_key=eq.${encodeURIComponent(key)}`,'PATCH',data);
 try{
  if(inject&&row.attempts===1)throw Error('injected_mail_failure');
  const person=await db('ap_news_subscribers?email=eq.cksals00%40naver.com&select=status,confirmed_at');
  if(person?.[0]?.status!=='active'||!person?.[0]?.confirmed_at)throw Error('owner_recipient_not_active');
  if(Deno.env.get('AP_NEWS_MAIL_ENABLED')!=='true')throw Error('mail_disabled');
  const subject=String(detail.subject||'[AP News 운영 알림]').slice(0,180);
  const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(key)))).map(v=>v.toString(16).padStart(2,'0')).join('');
  const r=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${Deno.env.get('RESEND_API_KEY')}`,'Content-Type':'application/json','Idempotency-Key':digest},body:JSON.stringify({from:FROM,to:[TO],reply_to:'alfred.park@apholdings.kr',subject,html:html||`<div style="font:15px Arial;max-width:600px;padding:28px;color:#172338"><h2>${esc(subject)}</h2><p>${esc(detail.message)}</p><p><a href="https://www.apholdings.kr/admin/">관리자 상태 확인</a></p><p>${esc(detail.run_url||'')}</p></div>`}),signal:AbortSignal.timeout(15000)});
  const result=await r.json();if(!r.ok||!result.id)throw Error(`mail_${r.status}`);
  await patch({state:'sent',provider_id:result.id,last_error:null,updated_at:new Date().toISOString()});return {accepted:true,id:result.id};
 }catch(e){await patch({state:'retry',last_error:String(e).slice(0,120),updated_at:new Date().toISOString()});throw e;}
}
async function watch(){
 const pending=await db('ap_news_ops_events?state=in.(retry,processing)&attempts=lt.5&event=in.(ops_alert,ops_recovery,ops_status)&created_at=gt.'+new Date(Date.now()-23*3600000).toISOString()+'&select=event_key,event,detail');
 for(const row of pending){try{await send(row.event_key,row.event,row.detail);}catch{/* Next server tick retries bounded operational alerts. */}}
 const now=new Date(),kst=new Date(now.getTime()+9*3600000),day=kst.toISOString().slice(0,10),h=kst.getUTCHours(),m=kst.getUTCMinutes();
 if(h<7)return {status:'outside_window'};
 const issues=await db(`ap_news_issues?issue_date=eq.${day}&select=status,verified`);
 const runs=await db(`ap_news_publication_runs?issue_date=eq.${day}&select=ready_verified_at,public_verified_at,last_error,workflow_url`);
 const mail=await db('rpc/ap_news_delivery_health','POST',{p_day:day});
 const decision=assess(day,now,runs?.[0],issues?.[0],mail);
 if(decision.kind==='alert'){
  const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(decision.code==='server_error'?String(runs?.[0]?.last_error):decision.code)))).slice(0,6).map(v=>v.toString(16).padStart(2,'0')).join('');
  return await send(day+':ops-'+decision.code+'-'+digest,'ops_alert',{subject:'[AP News 운영 경보] '+day,message:decision.message,run_url:runs?.[0]?.workflow_url});
 }
 if(decision.kind==='progress')return await send(day+':ops-0800-status','ops_status',{subject:'[AP News08:00 상태] '+day,message:decision.message,run_url:runs?.[0]?.workflow_url});
 if(decision.kind==='complete'){
  const previous=await db(`ap_news_ops_events?event_key=like.${day}*&event=in.(ops_alert,ops_recovery)&select=event,provider_id`);
  if(previous?.some((r:{event:string;provider_id?:string})=>r.event==='ops_recovery'&&r.provider_id))return {status:'legacy_completion_already_reported'};
  const recovered=previous?.some((r:{event:string;provider_id?:string})=>r.event==='ops_alert'&&r.provider_id);
  return await send(day+':ops-complete','ops_status',{subject:(recovered?'[AP News 복구·발행·메일 결과] ':'[AP News 발행·메일 결과] ')+day,message:decision.message,run_url:runs?.[0]?.workflow_url});
 }
 return {status:'healthy_or_preparing'};
}
Deno.serve(async req=>{
 if(req.method!=='POST')return new Response('POST required',{status:405});
 try{
  const token=req.headers.get('authorization')?.replace(/^Bearer /,'')||'';let scheduler=false;
  if(!token)return new Response('Unauthorized',{status:401});
  if(/^[a-f0-9]{64}$/.test(token)){
   const expected=(await db('ap_news_scheduler_auth?id=eq.scheduler&select=token_hash'))?.[0]?.token_hash;
   const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(token)))).map(v=>v.toString(16).padStart(2,'0')).join('');scheduler=hash===expected;
  }
  if(!scheduler){try{await db('rpc/ap_news_admin_pipeline','POST',{},token);}catch{return new Response('Unauthorized',{status:401});}}
  const body=await req.json();
  if(body.watch)return Response.json(await watch());
  if(scheduler)return new Response('Scheduler watch only',{status:403});
  if(!/^(test-[0-9]+|[0-9]{4}-[0-9]{2}-[0-9]{2}):[a-z0-9_-]+$/.test(body.key||'')||typeof body.detail!=='object')return new Response('Invalid event',{status:400});
  if(body.html&&(typeof body.html!=='string'||body.html.length>180000))return new Response('Invalid html',{status:400});
  return Response.json(await send(body.key,body.event,body.detail,body.html,body.inject_failure===true));
 }catch(e){return Response.json({error:String(e).slice(0,160)},{status:503});}
});
