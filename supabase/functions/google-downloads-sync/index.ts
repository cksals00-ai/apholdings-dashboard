import {createClient} from 'https://esm.sh/@supabase/supabase-js@2.116.0';
import {importPKCS8,SignJWT} from 'npm:jose@5.9.6';
import {readInstallReport,aggregateInstalls,validDate} from './core.mjs';

type ReportDiagnostic = Omit<NonNullable<Awaited<ReturnType<typeof readInstallReport>>['diagnostic']>, 'packageId'> & {
  packageId?: string;
};

// Google Play production releases verified on 2026-11-23. Used only for diagnostic metadata.
const verifiedGooglePackages = new Set([
  'com.apholdings.dawngrace',
  'com.apholdings.foldblock',
  'com.apholdings.irongrade',
  'com.apholdings.kconcerttrip',
  'com.apholdings.kranker',
  'com.apholdings.kscan',
  'com.apholdings.lightlist',
  'com.apholdings.moonshot',
  'com.apholdings.safelist',
  'com.apholdings.theotherhours',
  'com.aplocalift.hangeulcubs',
  'com.hotelranker',
  'kr.apholdings.hajeungbond',
  'kr.apholdings.investranker',
  'kr.apholdings.sonoinspect',
]);

type GoogleReleaseApp = {
  name: string;
  packageId: string;
  status: 'production' | 'internal' | 'draft';
};

const androidPackageId = /^[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)+$/;
const observationTimestamp = /^(\d{4}-\d{2}-\d{2})T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)$/;

function isValidObservationTimestamp(value: unknown): boolean {
  const date = typeof value === 'string' ? observationTimestamp.exec(value)?.[1] : undefined;
  return date !== undefined && validDate(date);
}

function parseVerifiedReleaseApps(detail: unknown): GoogleReleaseApp[] {
  let registry: unknown;
  try {
    registry = typeof detail === 'string' ? JSON.parse(detail) : detail;
  } catch {
    throw Error('registry_invalid');
  }
  if (typeof registry !== 'object' || registry === null) throw Error('registry_invalid');
  const {schemaVersion, kind, platform, observedAt, apps, counts} = registry as Record<string, unknown>;
  if (schemaVersion !== 1 || kind !== 'release_status_observation' || platform !== 'google' ||
      !isValidObservationTimestamp(observedAt) ||
      !Array.isArray(apps) || apps.length === 0 || typeof counts !== 'object' || counts === null) {
    throw Error('registry_invalid');
  }

  const packages = new Set<string>();
  const totals = {production: 0, internal: 0, draft: 0};
  const verifiedApps = apps.map((entry: unknown): GoogleReleaseApp => {
    if (typeof entry !== 'object' || entry === null) throw Error('registry_invalid');
    const {name, packageId, status} = entry as Record<string, unknown>;
    if (typeof name !== 'string' || !name.trim() ||
        typeof packageId !== 'string' || !androidPackageId.test(packageId) || packages.has(packageId) ||
        (status !== 'production' && status !== 'internal' && status !== 'draft')) {
      throw Error('registry_invalid');
    }
    packages.add(packageId);
    totals[status]++;
    return {name, packageId, status};
  });
  const registryCounts = counts as Record<string, unknown>;
  if (registryCounts.registered !== verifiedApps.length ||
      Object.entries(totals).some(([status, count]) => registryCounts[status] !== count)) {
    throw Error('registry_invalid');
  }
  return verifiedApps;
}

Deno.serve(async req=>{
 const send=(v:unknown,status=200)=>new Response(JSON.stringify(v),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
 const secret=Deno.env.get('GOOGLE_DOWNLOADS_CRON_SECRET');
 if(!secret||req.headers.get('x-sync-secret')!==secret)return send({error:'unauthorized'},401);
 if(req.method!=='POST')return send({error:'method'},405);
 const db=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false}});
 const now=new Date().toISOString();
 const failures: ReportDiagnostic[] = [];
 async function state(status:string,detail:unknown){
   const storedDetail = failures.length ? {...detail as object, failures} : detail;
   const {error}=await db.from('admin_app_sync_runtime').upsert({id:'google_downloads_sync',status,detail:JSON.stringify(storedDetail),checked_at:now});
   if(error)throw Error('state_write');
   return send({status,...detail as object});
 }
 try{
 const raw=Deno.env.get('GOOGLE_PLAY_SERVICE_ACCOUNT_JSON')||Deno.env.get('GA4_SERVICE_ACCOUNT_JSON');
 const sa=raw?JSON.parse(raw):null;const bucket=Deno.env.get('GOOGLE_PLAY_REPORT_BUCKET');
 if(!sa?.client_email||!bucket)return await state('configuration_required',{observedAt:now,serviceAccountEmail:sa?.client_email||null,bucketConfigured:Boolean(bucket),message:'공식 보고서 저장소 주소와 Google Play 읽기 권한 확인 필요'});
 if(bucket!=='pubsite_prod_7870440470636306408'&&!/^pubsite_prod_rev_[A-Za-z0-9_-]+$/.test(bucket))throw Error('bucket_format');
 const {data:registry,error}=await db.from('admin_app_sync_runtime').select('status,detail').eq('id','google_release_status').single();
 if(error)throw Error('registry_read');
 if(!registry)throw Error('registry_missing');
 if(registry.status!=='verified')throw Error('registry_invalid');
 const verifiedApps = parseVerifiedReleaseApps(registry.detail);
 const end=new Date(Date.now()+9*3600000).toISOString().slice(0,10);const start=new Date(Date.parse(end)-27*86400000).toISOString().slice(0,10);
 const months=[...new Set([start.slice(0,7),end.slice(0,7)])].map(s=>s.replace('-',''));
 const key=await importPKCS8(sa.private_key,'RS256');const assertion=await new SignJWT({scope:'https://www.googleapis.com/auth/devstorage.read_only'}).setProtectedHeader({alg:'RS256'}).setIssuer(sa.client_email).setAudience('https://oauth2.googleapis.com/token').setIssuedAt().setExpirationTime('1h').sign(key);
 const tokenResponse=await fetch('https://oauth2.googleapis.com/token',{method:'POST',body:new URLSearchParams({grant_type:'urn:ietf:params:oauth:grant-type:jwt-bearer',assertion})});if(!tokenResponse.ok)throw Error('google_auth');const {access_token}=await tokenResponse.json();if(!access_token)throw Error('google_auth');
 const fetchReport = (path: string) => fetch(path, {headers: {Authorization: `Bearer ${access_token}`}});
 const apps=[];let failed=0;
 for(const app of verifiedApps){
   const rows=[];let problem='';
   for(const month of months){
     const report = await readInstallReport(fetchReport, bucket, app.packageId, month);
     if(report.missing)continue;
     let diagnostic = report.diagnostic;
     if(!diagnostic){
       try{rows.push(...report.rows);}catch{
         diagnostic = {packageId: app.packageId, month, stage: 'parse', code: 'invalid_report'};
       }
     }
     if(diagnostic){
       const {packageId, ...failure} = diagnostic;
       failures.push(typeof packageId === 'string' && verifiedGooglePackages.has(packageId)
         ? {...failure, packageId}
         : failure);
       if(diagnostic.stage==='fetch')throw Error('fetch_error');
       problem=diagnostic.code;
       break;
     }
   }
   if(problem){failed++;apps.push({...app,installs:null,complete:false,sourceStatus:problem});}else{const result=aggregateInstalls(rows,start,end);apps.push({...app,...result,metric:'installed_users',sourceStatus:result.complete?'complete':result.installs===null?'waiting_report':'partial_report'});}
 }
 // Failed reads never replace the last successfully collected snapshot.
 if(failed)return await state('source_error',{observedAt:now,failedApps:failed,message:'일부 공식 보고서 조회 실패 · 이전 수집 결과 유지'});
 const collectionDetail={observedAt:now,message:'Google 공식 설치 보고서 자동 조회 · 보고서 반영에 3~7일 소요'};
 if(apps.every(a=>a.installs===null))return await state('waiting_report',collectionDetail);
 const snapshot={schemaVersion:1,platform:'google',collectionMode:'automatic_official',source:'Google Play monthly country installation CSV / Daily User Installs',periodStart:start,periodEnd:end,observedAt:now,apps};
 const {error:writeError}=await db.from('admin_app_sync_runtime').upsert({id:'google_downloads',status:'ok',detail:JSON.stringify(snapshot),checked_at:now});if(writeError)throw Error('snapshot_write');
 return await state('collected',collectionDetail);
 }catch(e){const code=e instanceof Error&&['bucket_format','google_auth','registry_invalid','registry_missing','registry_read','snapshot_write','state_write'].includes(e.message)?e.message:'collection_error';return await state('connection_error',{observedAt:now,diagnostic:code,message:'Google 설치 보고서 연결 확인 필요'});}
});
