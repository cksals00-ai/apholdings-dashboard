import { validateSubscription, escapeHtml, canDeliver, validateToken, freezeRequest } from './core.mjs';

const URL = Deno.env.get('SUPABASE_URL')!;
const KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const ORIGIN = 'https://www.apholdings.kr';
const OWNER_ID = '94f18e51-cc1e-46c5-b2e0-235bf9221761';
const FROM = 'AP News <alfred.park@apholdings.kr>';
const READY = () => Boolean(Deno.env.get('RESEND_API_KEY')) && Deno.env.get('AP_NEWS_MAIL_ENABLED') === 'true';
const hex = (b: ArrayBuffer) => [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const sha = async (s: string) => hex(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)));
async function hmac(id: string) {
  const rows=await db('ap_news_scheduler_auth?id=eq.scheduler&select=token_hash');
  const secret=rows?.[0]?.token_hash;if(!secret)throw new Error('token_configuration_required');
  const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
  return hex(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode('ap-news-unsubscribe:'+id)));
}
async function db(path: string, method='GET', body?: unknown) {
  const r=await fetch(`${URL}/rest/v1/${path}`,{method,headers:{apikey:KEY,Authorization:`Bearer ${KEY}`,'Content-Type':'application/json',Prefer:'return=representation'},body:body===undefined?undefined:JSON.stringify(body),signal:AbortSignal.timeout(15000)});
  if(!r.ok)throw new Error(`database_${r.status}`);
  const t=await r.text();return t?JSON.parse(t):null;
}
const rpc=(name:string,body={})=>db(`rpc/${name}`,'POST',body);
const manage=(action:string,id:string,token:string)=>`${ORIGIN}/ko/news/daily/manage/#action=${action}&id=${encodeURIComponent(id)}&token=${token}`;

async function isOwner(req:Request) {
  const a=req.headers.get('authorization');if(!a)return false;
  const r=await fetch(`${URL}/auth/v1/user`,{headers:{apikey:KEY,Authorization:a},signal:AbortSignal.timeout(10000)});
  if(!r.ok)return false;const user=await r.json();return user.id===OWNER_ID;
}
async function scheduler(req:Request) {
  const token=req.headers.get('authorization')?.replace(/^Bearer /,'');if(!validateToken(token))return false;
  const rows=await db('ap_news_scheduler_auth?id=eq.scheduler&select=token_hash');
  return rows?.[0]?.token_hash===await sha(token!);
}
async function dispatch() {
  if(!READY()) {
    await db('ap_news_runtime?id=eq.mail','PATCH',{mail_ready:false,status:'setup_required',last_run:new Date().toISOString(),last_error:null});
    return {status:'setup_required',mail_ready:false,processed:0};
  }
  await rpc('ap_news_refresh_confirmations');
  await rpc('ap_news_enqueue');
  const deliveries=await rpc('ap_news_claim',{p_limit:10});let accepted=0,failed=0;
  for(const d of deliveries) {
    try {
      const s=(await db(`ap_news_subscribers?id=eq.${d.subscriber_id}&select=*`))?.[0];
      let subject:string,html:string,headers:Record<string,string>={};
      if(d.kind==='confirmation') {
        if(s?.status!=='pending'||!validateToken(d.payload?.token)||Date.parse(s.confirmation_expires)<=Date.now()) {await db(`ap_news_deliveries?id=eq.${d.id}`,'PATCH',{state:'cancelled',payload:{}});continue;}
        const link=manage('confirm',s.id,d.payload.token);
        subject='[AP News] 이메일을 확인하고 구독을 시작하세요';
        html=`<div style="max-width:600px;padding:32px;background:#f7f4ed;color:#172338;font-family:Arial,sans-serif"><img src="${ORIGIN}/img/ap_mark.png" width="44" style="background:#172338;padding:8px" alt="AP Holdings"><h1 style="font-family:Georgia,serif">AP <i>News</i></h1><p>AI 소식을 오늘의 판단으로.</p><p>아래 링크를 열고 확인 버튼을 누르면 무료 일일 구독이 시작됩니다. 링크는 48시간 동안 유효합니다.</p><p><a href="${escapeHtml(link)}">이메일 확인하고 구독 시작 →</a></p><p style="font-size:12px">신청하지 않으셨다면 이 메일을 무시해주세요. 확인 전에는 뉴스레터를 보내지 않습니다.<br>문의 alfred.park@apholdings.kr</p></div>`;
      } else {
        const i=(await db(`ap_news_issues?issue_date=eq.${d.issue_date}&select=*`))?.[0];
        if(!canDeliver(s,i)){await db(`ap_news_deliveries?id=eq.${d.id}`,'PATCH',{state:'cancelled'});continue;}
        const link=manage('unsubscribe',s.id,await hmac(s.id));
        subject=`[AP News] ${i.issue_date} · ${i.title}`;html=i.email_html.replaceAll('{{unsubscribe_url}}',escapeHtml(link));
        // The website performs explicit POST confirmation; no GET changes subscription state.
        headers={'List-Unsubscribe':`<mailto:alfred.park@apholdings.kr?subject=AP%20News%20unsubscribe>`};
      }
      const mail=freezeRequest(d,{from:FROM,to:[s.email],reply_to:'alfred.park@apholdings.kr',subject,html,headers});
      if(!d.payload?.mail) {
        const saved=await db(`ap_news_deliveries?id=eq.${d.id}&state=eq.processing`,'PATCH',{payload:{...d.payload,mail}});
        if(!saved?.length)continue;
      }
      if(!await rpc('ap_news_authorize_delivery',{p_id:d.id}))continue;
      // Requests submitted after this authorization are in flight. Completion
      // updates cannot resurrect a delivery cancelled by a concurrent opt-out.
      const r=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${Deno.env.get('RESEND_API_KEY')}`,'Content-Type':'application/json','Idempotency-Key':d.id},body:JSON.stringify(mail),signal:AbortSignal.timeout(10000)});
      const result=await r.json();
      if(!r.ok||!result.id)throw new Error(`mail_provider_${r.status}`);
      const saved=await db(`ap_news_deliveries?id=eq.${d.id}&state=eq.processing`,'PATCH',{state:'sent',provider_id:result.id,last_error:null,payload:{}});
      if(!saved?.length)await db(`ap_news_deliveries?id=eq.${d.id}&state=eq.cancelled`,'PATCH',{provider_id:result.id,last_error:'in_flight_before_unsubscribe'});
      accepted++;
    } catch(error) {
      failed++;
      const detail=error instanceof Error&&/^mail_provider_\d+$|^database_\d+$/.test(error.message)?error.message:'mail_transport_error';
      await db(`ap_news_deliveries?id=eq.${d.id}&state=eq.processing`,'PATCH',{state:d.attempts>=5?'failed':'retry',last_error:detail,next_attempt_at:new Date(Date.now()+Math.min(3600000,300000*2**d.attempts)).toISOString()});
    }
  }
  await db('ap_news_runtime?id=eq.mail','PATCH',{mail_ready:true,status:failed?'delivery_error':'ready',last_run:new Date().toISOString(),last_error:failed?'발송 오류가 있습니다. 재시도 상태를 확인하세요.':null});
  return {status:failed?'delivery_error':'ready',processed:deliveries.length,accepted,failed};
}

Deno.serve(async req=>{
  const origin=req.headers.get('origin');
  const allowed=new Set([ORIGIN,'https://apholdings.kr','https://cksals00-ai.github.io']);
  const cors={'Access-Control-Allow-Origin':origin&&allowed.has(origin)?origin:ORIGIN,'Access-Control-Allow-Headers':'authorization,content-type','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Vary':'Origin'};
  const reply=(data:unknown,status=200)=>new Response(JSON.stringify(data),{status,headers:{...cors,'Content-Type':'application/json','Cache-Control':'no-store'}});
  const action=new globalThis.URL(req.url).pathname.split('/').filter(Boolean).at(-1);
  if(origin&&!allowed.has(origin))return reply({message:'허용되지 않은 요청입니다.'},403);
  if(req.method==='OPTIONS')return new Response(null,{status:204,headers:cors});
  try {
    if(req.method==='GET'&&action==='status') {
      let storage_ready=false;try{storage_ready=Boolean((await db('ap_news_runtime?id=eq.mail&select=id'))?.length);}catch{}
      return reply({storage_ready,mail_ready:storage_ready&&READY(),sender:'alfred.park@apholdings.kr',edition_language:'ko'});
    }
    if(req.method==='GET'&&action==='admin') {
      if(!await isOwner(req))return reply({message:'관리자 로그인이 필요합니다.'},401);
      const [subscribers,issues,deliveries,runtime]=await Promise.all([
        db('ap_news_subscribers?select=id,status,consent_at,confirmed_at,unsubscribed_at'),
        db('ap_news_issues?select=issue_date,number,title,status,verified,web_url,pdf_url&order=issue_date.desc&limit=30'),
        db('ap_news_deliveries?select=id,issue_date,kind,state,attempts,last_error,created_at&order=created_at.desc&limit=100'),
        db('ap_news_runtime?id=eq.mail&select=*')]);
      return reply({mail_ready:READY(),counts:{active:subscribers.filter((s:any)=>s.status==='active').length,pending:subscribers.filter((s:any)=>s.status==='pending').length,unsubscribed:subscribers.filter((s:any)=>s.status==='unsubscribed').length},issues,deliveries,runtime:runtime[0]});
    }
    if(req.method!=='POST')return reply({message:'지원하지 않는 요청입니다.'},405);
    if(action==='dispatch') {if(!await scheduler(req)&&!await isOwner(req))return reply({message:'인증이 필요합니다.'},401);return reply(await dispatch());}
    if(Number(req.headers.get('content-length')||0)>4096)return reply({message:'요청이 너무 큽니다.'},413);
    const raw=await req.text();if(raw.length>4096)return reply({message:'요청이 너무 큽니다.'},413);
    let body;try{body=JSON.parse(raw);}catch{return reply({message:'요청 형식을 확인해주세요.'},400);}
    if(action==='subscribe') {
      if(body.website)return reply({message:'신청을 접수했습니다.'},202);
      let input;try{input=validateSubscription(body);}catch(e){return reply({message:(e as Error).message},400);}
      const ip=req.headers.get('cf-connecting-ip')||req.headers.get('x-forwarded-for')?.split(',')[0]||'unknown';
      const ipKey=await sha(`ip:${ip}:${KEY}`),emailKey=await sha(`email:${input.email}:${KEY}`);
      if(!await rpc('ap_news_rate_limit',{p_key:ipKey,p_limit:40})||!await rpc('ap_news_rate_limit',{p_key:emailKey,p_limit:3}))return reply({message:'신청이 반복되어 잠시 쉬고 있습니다. 한 시간 후 다시 시도해주세요.'},429);
      await rpc('ap_news_request_subscription',{p_email:input.email,p_name:input.name});
      return reply({status:'pending_confirmation',message:READY()?'신청을 접수했습니다. 확인 메일은 약 5분 안에 도착합니다. 이미 구독 중이면 기존 구독이 유지됩니다.':'신청을 접수했습니다. 이메일 발송 준비 후 확인 메일을 드립니다. 확인 후 구독이 시작됩니다.'},202);
    }
    if(action==='confirm') {
      if(!validateToken(body.token))return reply({message:'확인 링크가 유효하지 않습니다.'},400);
      const ok=await rpc('ap_news_confirm',{p_hash:await sha(body.token)});
      return ok?reply({message:'이메일 확인이 완료됐습니다. AP News 구독이 시작됩니다.'}):reply({message:'만료되었거나 이미 사용한 링크입니다. 구독 신청을 다시 해주세요.'},400);
    }
    if(action==='unsubscribe') {
      if(!validateToken(body.token)||typeof body.id!=='string'||!/^[a-f0-9-]{36}$/.test(body.id)||body.token!==await hmac(body.id))return reply({message:'해지 링크가 유효하지 않습니다.'},400);
      await rpc('ap_news_unsubscribe',{p_id:body.id});
      return reply({message:'구독이 해지됐습니다. 앞으로 뉴스레터를 보내지 않습니다.'});
    }
    return reply({message:'지원하지 않는 요청입니다.'},404);
  } catch {return reply({message:'일시적으로 처리하지 못했습니다. 잠시 후 다시 시도해주세요.'},503);}
});
