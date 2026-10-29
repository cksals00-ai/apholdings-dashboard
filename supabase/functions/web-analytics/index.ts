import { corsHeaders } from 'https://esm.sh/@supabase/supabase-js@2.116.0/cors';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.116.0';
import { ownerAllowed, reportRequest, summarize, parseServiceAccount } from './core.mjs';
const origins=new Set(['https://www.apholdings.kr','https://apholdings.kr']);
let cached:any=null, cacheUntil=0, tokenCache={value:'',expires:0};
const b64=(s:Uint8Array|string)=>btoa(typeof s==='string'?s:String.fromCharCode(...s)).replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
async function googleToken(raw:string){
 if(tokenCache.expires>Date.now())return tokenCache.value;
 const sa=parseServiceAccount(raw);
 const now=Math.floor(Date.now()/1000), enc=new TextEncoder();
 const payload=b64(JSON.stringify({alg:'RS256',typ:'JWT'}))+'.'+b64(JSON.stringify({iss:sa.client_email,scope:'https://www.googleapis.com/auth/analytics.readonly',aud:'https://oauth2.googleapis.com/token',iat:now,exp:now+3600}));
 const der=Uint8Array.from(atob(sa.private_key.replace(/-----[^-]+-----|\s/g,'')),c=>c.charCodeAt(0));
 const key=await crypto.subtle.importKey('pkcs8',der,{name:'RSASSA-PKCS1-v1_5',hash:'SHA-256'},false,['sign']);
 const sig=await crypto.subtle.sign('RSASSA-PKCS1-v1_5',key,enc.encode(payload));
 const r=await fetch('https://oauth2.googleapis.com/token',{method:'POST',body:new URLSearchParams({grant_type:'urn:ietf:params:oauth:grant-type:jwt-bearer',assertion:payload+'.'+b64(new Uint8Array(sig))})});
 if(!r.ok)throw Error('credentials');const t=await r.json();if(!t.access_token)throw Error('credentials');tokenCache={value:t.access_token,expires:Date.now()+3000000};return t.access_token;
}
Deno.serve(async req=>{
 const origin=req.headers.get('origin')||'';const headers={'Access-Control-Allow-Origin':origins.has(origin)?origin:'https://www.apholdings.kr','Access-Control-Allow-Headers':corsHeaders['Access-Control-Allow-Headers'],'Access-Control-Allow-Methods':'POST, OPTIONS','Content-Type':'application/json','Cache-Control':'no-store','Vary':'Origin'};
 const send=(data:unknown,status=200)=>new Response(JSON.stringify(data),{status,headers});
 if(origin&&!origins.has(origin))return send({error:'forbidden'},403);
 if(req.method==='OPTIONS')return new Response(null,{status:204,headers});
 if(req.method!=='POST')return send({error:'method'},405);
 const auth=req.headers.get('authorization');if(!auth?.startsWith('Bearer '))return send({error:'unauthorized'},401);
 try{
 const db=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_ANON_KEY')!,{auth:{persistSession:false}});
 const {data,error}=await db.auth.getUser(auth.slice(7));if(error||!ownerAllowed(data.user))return send({error:'forbidden'},403);
 const raw=Deno.env.get('GA4_SERVICE_ACCOUNT_JSON');if(!raw)return send({status:'credentials_required',checkedAt:new Date().toISOString(),message:'Google 통계 읽기 전용 연결 대기'});
 if(cached&&Date.now()<cacheUntil)return send({...cached,cached:true});
 const token=await googleToken(raw);const r=await fetch('https://analyticsdata.googleapis.com/v1beta/properties/561381925:runReport',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify(reportRequest())});
 if(!r.ok)return send({status:r.status===403?'permission_required':'upstream_error',checkedAt:new Date().toISOString(),message:'Google 통계 권한·API 연결 확인 필요'});
 cached=summarize(await r.json());cacheUntil=Date.now()+300000;return send(cached);
 }catch(e){const code=e instanceof Error&&['credential_format','credentials'].includes(e.message)?e.message:'connection_failed';console.warn('GA4_REPORT_CONNECTION',code);return send({status:'connection_error',diagnostic:code,checkedAt:new Date().toISOString(),message:'통계 연결 확인 필요'});}
});
