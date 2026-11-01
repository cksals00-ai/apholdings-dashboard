import {decide} from './startup.mjs';
const URL=Deno.env.get('SUPABASE_URL')!,KEY=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const REPO='cksals00-ai/apholdings-dashboard',WORKFLOW='ap-news-production.yml';
async function db(path:string,method='GET',body?:unknown){
 const r=await fetch(`${URL}/rest/v1/${path}`,{method,headers:{apikey:KEY,Authorization:`Bearer ${KEY}`,'Content-Type':'application/json',Prefer:'return=representation'},body:body===undefined?undefined:JSON.stringify(body),signal:AbortSignal.timeout(15000)});
 if(!r.ok)throw Error('database_'+r.status);return await r.json();
}
async function github(path:string,method='GET',body?:unknown){
 const token=Deno.env.get('AP_NEWS_GITHUB_DISPATCH_TOKEN');if(!token)throw Error('dispatch_credential_missing');
 const r=await fetch('https://api.github.com/repos/'+REPO+'/'+path,{method,headers:{Authorization:`Bearer ${token}`,Accept:'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body),signal:AbortSignal.timeout(15000)});
 if(!r.ok)throw Error('github_'+r.status);return r.status===204?null:await r.json();
}
async function alert(day:string,message:string,token:string,code='failure'){
 const r=await fetch(URL+'/functions/v1/ap-news-ops',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({key:day+':startup-'+code,event:'ops_alert',detail:{subject:'[AP News 제작 시작 장애] '+day,message}}),signal:AbortSignal.timeout(20000)});
 if(!r.ok)throw Error('startup_alert_'+r.status);
}
Deno.serve(async req=>{
 if(req.method!=='POST')return new Response('POST required',{status:405});
 const token=req.headers.get('authorization')?.replace(/^Bearer /,'')||'';let authenticated=false;
 try{
  const expected=(await db('ap_news_scheduler_auth?id=eq.scheduler&select=token_hash'))?.[0]?.token_hash;
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(token)))).map(v=>v.toString(16).padStart(2,'0')).join('');
  // Existing scheduler and authenticated service role only. No caller chooses repository or workflow.
  if(!token||!(token===KEY||(/^[a-f0-9]{64}$/.test(token)&&hash===expected)))return new Response('Unauthorized',{status:401});
  authenticated=true;
  const now=new Date(),day=new Date(+now+9*3600000).toISOString().slice(0,10),body=await req.json();
  const minute=new Date(+now+9*3600000).getUTCHours()*60+new Date(+now+9*3600000).getUTCMinutes();
  if(!body.observe&&(minute<185||minute>420))return Response.json({status:'outside_window',day});
  const runs=await github('actions/workflows/'+WORKFLOW+'/runs?per_page=30');
  const prior=(await db('ap_news_startup_receipts?issue_date=eq.'+day+'&select=attempts,updated_at'))?.[0];
  const decision=decide(now.toISOString(),runs.workflow_runs,prior);
  if(body.observe)return Response.json({day,status:decision.kind,read_only:true,today_runs:runs.workflow_runs.filter((r:{created_at:string})=>new Date(+new Date(r.created_at)+9*3600000).toISOString().slice(0,10)===day).map((r:{html_url:string,status:string,conclusion:string})=>({url:r.html_url,status:r.status,conclusion:r.conclusion}))});
  if(['queued','waiting'].includes(decision.kind)&&minute>=190)await alert(day,'03:05 제작 요청 이후 아직 실제 제작 실행을 확인하지 못했습니다. 기존 요청을 중복 생성하지 않고 서버에서 추적 중입니다.',KEY,'pending');
  if(['failure','exhausted'].includes(decision.kind))await alert(day,'서버 제작 시작 또는 복구 실패를 감지했습니다. 기존 GitHub 실행을 확인하며 중복 제작은 시작하지 않습니다.',KEY);
  if(decision.kind!=='start')return Response.json({day,status:decision.kind});
  const claimed=await db('rpc/ap_news_startup_claim','POST',{p_day:day});
  if(!claimed)return Response.json({day,status:'claimed_elsewhere'});
  try{
   await github('actions/workflows/'+WORKFLOW+'/dispatches','POST',{ref:'main'});
   await db('ap_news_startup_receipts?issue_date=eq.'+day,'PATCH',{state:'requested',last_error:null});
   return Response.json({day,status:'requested',execution_confirmed:false});
  }catch(e){await db('ap_news_startup_receipts?issue_date=eq.'+day,'PATCH',{state:'retry',last_error:String(e).slice(0,100)});throw e;}
 }catch(e){
  const day=new Date(Date.now()+9*3600000).toISOString().slice(0,10);
  if(authenticated){try{await alert(day,'독립 제작 예약 점검이 실패했습니다: '+String(e).slice(0,100),KEY);}catch{}}
  return Response.json({error:String(e).slice(0,120)},{status:503});
 }
});
