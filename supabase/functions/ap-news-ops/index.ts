import {complete} from './health.mjs';
import {decideRecovery,notificationKey} from './recovery.mjs';
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
async function github(path:string,method='GET',body?:unknown){
 const token=Deno.env.get('AP_NEWS_GITHUB_DISPATCH_TOKEN');if(!token)throw Error('dispatch_credential_missing');
 const r=await fetch('https://api.github.com/repos/cksals00-ai/apholdings-dashboard/'+path,{method,headers:{Authorization:`Bearer ${token}`,Accept:'application/vnd.github+json','Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body),signal:AbortSignal.timeout(15000)});
 if(!r.ok)throw Error('github_'+r.status);return r.status===204?null:await r.json();
}
async function watch(){
 const now=new Date(),kst=new Date(+now+9*3600000),day=kst.toISOString().slice(0,10),minute=kst.getUTCHours()*60+kst.getUTCMinutes();
 if(minute<460||minute>=600)return {status:'outside_window'};
 // Retry only the one terminal notification. Old progress/attempt notices stay silent.
 const pending=await db(`ap_news_ops_events?event_key=eq.${day}:terminal-failure&state=in.(retry,processing)&attempts=lt.5&select=event_key,event,detail`);
 for(const row of pending){try{await send(row.event_key,row.event,row.detail);}catch{}}
 const issues=await db(`ap_news_issues?issue_date=eq.${day}&select=status,verified`);
 const runs=await db(`ap_news_publication_runs?issue_date=eq.${day}&select=ready_verified_at,public_verified_at,last_error,workflow_url`);
 const mail=await db('rpc/ap_news_delivery_health','POST',{p_day:day});
 const done=issues?.[0]?.status==='published'&&issues[0].verified===true&&!!runs?.[0]?.public_verified_at&&complete(mail);
 if(done)return {status:'complete',day,mail};
 const since=new Date(day+'T00:00:00+09:00').toISOString();
 const history=await github('actions/workflows/ap-news-daily.yml/runs?per_page=100&created='+encodeURIComponent('>='+since));
 if(!Array.isArray(history.workflow_runs)||history.total_count!==history.workflow_runs.length)throw Error('workflow_inventory_unknown');
 const receipt=(await db(`ap_news_publication_recovery?issue_date=eq.${day}&select=attempts,updated_at`))?.[0];
 // A dispatch can be briefly invisible; the durable lease avoids races between minute ticks.
 if(receipt&&+now-+new Date(receipt.updated_at)<120000)return {status:'recovery_lease_active'};
 const decision=decideRecovery(day,now.toISOString(),runs?.[0],history.workflow_runs,receipt?.attempts||0,!!done);
 if(decision.kind==='dispatch'){
  if(!await db('rpc/ap_news_publication_recovery_claim','POST',{p_day:day}))return {status:'claimed_elsewhere'};
  await github('actions/workflows/ap-news-daily.yml/dispatches','POST',{ref:'main',inputs:{reserve_publication:true,edition_date:day}});
  return {status:'recovery_requested',day};
 }
 if(decision.kind==='terminal')return await send(day+':terminal-failure','ops_alert',{terminal:true,subject:'[AP News 자동복구 실패] '+day,message:decision.reason+' 공개 검증 및 전체 active 제공사 접수는 완료로 표시하지 않았습니다.',run_url:runs?.[0]?.workflow_url});
 return {status:decision.kind,day};
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
  if(body.watch){
   try{return Response.json(await watch());}
   catch(error){
    const now=new Date(),kst=new Date(+now+9*3600000),minute=kst.getUTCHours()*60+kst.getUTCMinutes(),day=kst.toISOString().slice(0,10);
    // Repeated minute-level server retries have15 minutes to recover unknown health/API state.
    if(minute>=495&&minute<600){
     try{return Response.json(await send(day+':terminal-failure','ops_alert',{terminal:true,subject:'[AP News 상태 확인 복구 실패] '+day,message:'서버의 반복 재시도 후에도 발행·메일 접수 상태를 확인하지 못했습니다: '+String(error).slice(0,100)+'. 미확인을0으로 처리하지 않았습니다.'}));}catch{}
    }
    throw error;
   }
  }
  if(scheduler)return new Response('Scheduler watch only',{status:403});
  if(!/^(test-[0-9]+|[0-9]{4}-[0-9]{2}-[0-9]{2}):[a-z0-9_-]+$/.test(body.key||'')||typeof body.detail!=='object')return new Response('Invalid event',{status:400});
  if(body.html&&(typeof body.html!=='string'||body.html.length>180000))return new Response('Invalid html',{status:400});
  if(String(body.event).startsWith('ops_')){
   const day=new Date(Date.now()+9*3600000).toISOString().slice(0,10);
   const key=notificationKey(day,body.detail);
   if(!key)return Response.json({accepted:true,suppressed:true});
   return Response.json(await send(key,'ops_alert',body.detail));
  }
  return Response.json(await send(body.key,body.event,body.detail,body.html,body.inject_failure===true));
 }catch(e){return Response.json({error:String(e).slice(0,160)},{status:503});}
});
