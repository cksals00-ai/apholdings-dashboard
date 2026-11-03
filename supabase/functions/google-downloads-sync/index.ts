import {createClient} from 'https://esm.sh/@supabase/supabase-js@2.116.0';
import {importPKCS8,SignJWT} from 'npm:jose@5.9.6';
import {decodeReport,parseInstallCsv,aggregateInstalls} from './core.mjs';
Deno.serve(async req=>{
 const send=(v:unknown,status=200)=>new Response(JSON.stringify(v),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
 const secret=Deno.env.get('GOOGLE_DOWNLOADS_CRON_SECRET');
 if(!secret||req.headers.get('x-sync-secret')!==secret)return send({error:'unauthorized'},401);
 if(req.method!=='POST')return send({error:'method'},405);
 const db=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false}});
 const now=new Date().toISOString();
 async function state(status:string,detail:unknown){const {error}=await db.from('admin_app_sync_runtime').upsert({id:'google_downloads_sync',status,detail:JSON.stringify(detail),checked_at:now});if(error)throw Error('state_write');return send({status,...detail as object});}
 try{
 const raw=Deno.env.get('GOOGLE_PLAY_SERVICE_ACCOUNT_JSON')||Deno.env.get('GA4_SERVICE_ACCOUNT_JSON');
 const sa=raw?JSON.parse(raw):null;const bucket=Deno.env.get('GOOGLE_PLAY_REPORT_BUCKET');
 if(!sa?.client_email||!bucket)return await state('configuration_required',{observedAt:now,serviceAccountEmail:sa?.client_email||null,bucketConfigured:Boolean(bucket),message:'공식 보고서 저장소 주소와 Google Play 읽기 권한 확인 필요'});
 if(!/^pubsite_prod_rev_[A-Za-z0-9_-]+$/.test(bucket))throw Error('bucket_format');
 const {data:previous,error}=await db.from('admin_app_sync_runtime').select('detail').eq('id','google_downloads').single();if(error)throw Error('snapshot_read');const old=JSON.parse(previous.detail);if(!Array.isArray(old.apps)||old.apps.length<1)throw Error('registry_missing');
 const end=new Date(Date.now()+9*3600000).toISOString().slice(0,10);const start=new Date(Date.parse(end)-27*86400000).toISOString().slice(0,10);
 const months=[...new Set([start.slice(0,7),end.slice(0,7)])].map(s=>s.replace('-',''));
 const key=await importPKCS8(sa.private_key,'RS256');const assertion=await new SignJWT({scope:'https://www.googleapis.com/auth/devstorage.read_only'}).setProtectedHeader({alg:'RS256'}).setIssuer(sa.client_email).setAudience('https://oauth2.googleapis.com/token').setIssuedAt().setExpirationTime('1h').sign(key);
 const tokenResponse=await fetch('https://oauth2.googleapis.com/token',{method:'POST',body:new URLSearchParams({grant_type:'urn:ietf:params:oauth:grant-type:jwt-bearer',assertion})});if(!tokenResponse.ok)throw Error('google_auth');const {access_token}=await tokenResponse.json();if(!access_token)throw Error('google_auth');
 const apps=[];let failed=0;
 for(const app of old.apps){if(app.status==='not_created'){apps.push({...app,installs:null,complete:false});continue;}const rows=[];let problem='';for(const month of months){const path=`stats/installs/installs_${app.packageId}_${month}_country.csv`;const r=await fetch(`https://storage.googleapis.com/storage/v1/b/${encodeURIComponent(bucket)}/o/${encodeURIComponent(path)}?alt=media`,{headers:{Authorization:`Bearer ${access_token}`}});if(r.status===404)continue;if(!r.ok){problem=r.status===403?'permission_required':'source_error';break;}try{rows.push(...parseInstallCsv(decodeReport(new Uint8Array(await r.arrayBuffer())),app.packageId));}catch{problem='invalid_report';break;}}
 if(problem){failed++;apps.push({...app,installs:null,complete:false,sourceStatus:problem});}else{const result=aggregateInstalls(rows,start,end);apps.push({...app,...result,metric:'installed_users',sourceStatus:result.complete?'complete':result.installs===null?'waiting_report':'partial_report'});}}
 // Failed reads never replace the last successfully collected snapshot.
 if(failed)return await state('source_error',{observedAt:now,failedApps:failed,message:'일부 공식 보고서 조회 실패 · 이전 수집 결과 유지'});
 const snapshot={schemaVersion:1,platform:'google',collectionMode:'automatic_official',source:'Google Play monthly country installation CSV / Daily User Installs',periodStart:start,periodEnd:end,observedAt:now,apps};
 const {error:writeError}=await db.from('admin_app_sync_runtime').upsert({id:'google_downloads',status:'ok',detail:JSON.stringify(snapshot),checked_at:now});if(writeError)throw Error('snapshot_write');
 return await state(apps.some(a=>a.installs!==null)?'collected':'waiting_report',{observedAt:now,message:'Google 공식 설치 보고서 자동 조회 · 보고서 반영에 3~7일 소요'});
 }catch(e){const code=e instanceof Error&&['bucket_format','google_auth','registry_missing','snapshot_read','snapshot_write','state_write'].includes(e.message)?e.message:'collection_error';return await state('connection_error',{observedAt:now,diagnostic:code,message:'Google 설치 보고서 연결 확인 필요'});}
});
