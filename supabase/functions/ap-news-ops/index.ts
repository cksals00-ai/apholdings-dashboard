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
  const person=await db('ap_news_subscribers?email=eq.cksals00%40naver.com&select=status');
  if(person?.[0]?.status!=='active')throw Error('owner_recipient_not_active');
  if(Deno.env.get('AP_NEWS_MAIL_ENABLED')!=='true')throw Error('mail_disabled');
  const subject=String(detail.subject||'[AP News 운영 알림]').slice(0,180);
  const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(key)))).map(v=>v.toString(16).padStart(2,'0')).join('');
  const r=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${Deno.env.get('RESEND_API_KEY')}`,'Content-Type':'application/json','Idempotency-Key':digest},body:JSON.stringify({from:FROM,to:[TO],reply_to:'alfred.park@apholdings.kr',subject,html:html||`<div style="font:15px Arial;max-width:600px;padding:28px;color:#172338"><h2>${esc(subject)}</h2><p>${esc(detail.message)}</p><p><a href="https://www.apholdings.kr/admin/">관리자 상태 확인</a></p><p>${esc(detail.run_url||'')}</p></div>`}),signal:AbortSignal.timeout(15000)});
  const result=await r.json();if(!r.ok||!result.id)throw Error(`mail_${r.status}`);
  await patch({state:'sent',provider_id:result.id,last_error:null,updated_at:new Date().toISOString()});return {accepted:true,id:result.id};
 }catch(e){await patch({state:'retry',last_error:String(e).slice(0,120),updated_at:new Date().toISOString()});throw e;}
}
async function watch(){
 const now=new Date(),kst=new Date(now.getTime()+9*3600000),day=kst.toISOString().slice(0,10),h=kst.getUTCHours(),m=kst.getUTCMinutes();
 if(h<7||h>10)return {status:'outside_window'};
 const issues=await db(`ap_news_issues?issue_date=eq.${day}&select=status,verified`);
 const runs=await db(`ap_news_publication_runs?issue_date=eq.${day}&select=ready_verified_at,public_verified_at,last_error,workflow_url`);
 const mail=(await db(`ap_news_delivery_summary?issue_date=eq.${day}`))?.[0];
 const active=await db('ap_news_subscribers?status=eq.active&confirmed_at=not.is.null&select=id');
 let problem='';
 if((h===7&&m>=46)&&!runs?.[0]?.ready_verified_at)problem='준비 마감07:45 이후에도 완성본의 서버 검증 기록이 없습니다.';
 if(h>=8&&runs?.[0]?.last_error)problem=String(runs[0].last_error);
 if((h>8||h===8&&m>=5)&&(!issues?.[0]?.verified||!runs?.[0]?.public_verified_at))problem='08:05까지 오늘자 공개 검증이 완료되지 않았습니다.';
 if((h>8||h===8&&m>=10)&&issues?.[0]?.verified&&(!mail||mail.accepted<active.length||mail.failed||mail.uncertain))problem='오늘자 메일 접수가 완료되지 않았거나 발송 오류가 있습니다.';
 if(problem)return await send(day+':ops-alert','ops_alert',{subject:'[AP News 운영 경보] '+day,message:problem,run_url:runs?.[0]?.workflow_url});
 const previous=await db(`ap_news_ops_events?event_key=eq.${day}%3Aops-alert&select=provider_id`);
 if(previous?.[0]?.provider_id&&runs?.[0]?.public_verified_at&&mail?.accepted>=active.length&&!mail.pending&&!mail.retry&&!mail.failed&&!mail.uncertain)return await send(day+':ops-recovery','ops_recovery',{subject:'[AP News 복구 확인] '+day,message:`공개 검증 완료, 메일 접수${mail.accepted}건·대기0·실패0. 받은편지함 도착을 의미하지는 않습니다.`});
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
