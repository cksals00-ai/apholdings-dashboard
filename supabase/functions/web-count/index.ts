import {createClient} from 'https://esm.sh/@supabase/supabase-js@2.116.0';
import {validateCount} from './core.mjs';
Deno.serve(async req=>{
 const origin=req.headers.get('origin')||'';
 const probe=validateCount(origin,{host:(()=>{try{return new URL(origin).hostname}catch{return ''}})(),event:'ap_install_test'});
 const headers={'Access-Control-Allow-Origin':probe?origin:'https://www.apholdings.kr','Vary':'Origin','Cache-Control':'no-store','Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'content-type'};
 if(!probe)return new Response(null,{status:403,headers});
 if(req.method==='OPTIONS')return new Response(null,{status:204,headers});
 if(req.method!=='POST')return new Response(null,{status:405,headers});
 try{const text=await req.text();if(text.length>256)return new Response(null,{status:413,headers});const safe=validateCount(origin,JSON.parse(text));if(!safe)return new Response(null,{status:400,headers});
 const db=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false}});
 const {error}=await db.rpc('record_web_aggregate',{p_host:safe.host,p_event:safe.event});return new Response(null,{status:error?503:204,headers});
 }catch{return new Response(null,{status:400,headers});}
});
