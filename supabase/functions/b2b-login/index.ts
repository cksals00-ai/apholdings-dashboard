import {handle} from './core.mjs';
const URL=Deno.env.get('SUPABASE_URL')!,KEY=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
async function api(path:string,body:unknown){const r=await fetch(`${URL}${path}`,{method:'POST',headers:{apikey:KEY,Authorization:`Bearer ${KEY}`,'Content-Type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(15000)});if(!r.ok)throw Error('upstream_failed');return r.json();}
const digest=async(s:string)=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))).map(x=>x.toString(16).padStart(2,'0')).join('');
Deno.serve(req=>handle(req,{
 ready:()=>Boolean(Deno.env.get('RESEND_API_KEY')),
 limit:async(email:string,ip:string)=>api('/rest/v1/rpc/b2b_login_limit',{p_email_hash:await digest(email),p_ip_hash:await digest(ip)}),
 generate:async(email:string)=>api('/auth/v1/admin/generate_link',{type:'magiclink',email}),
 send:async({email,link}:{email:string,link:string})=>{const r=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${Deno.env.get('RESEND_API_KEY')}`,'Content-Type':'application/json'},body:JSON.stringify({from:'AP Holdings <alfred.park@apholdings.kr>',to:[email],reply_to:'alfred.park@apholdings.kr',subject:'하자증권 담당자 페이지 · 이메일 확인',text:`요청하신 하자증권 담당자 페이지 로그인 링크입니다.\n\n${link}\n\n요청하지 않았다면 이 메일을 무시하세요. 이 링크는 본인만 사용하고 다른 사람에게 전달하지 마세요. 홍보 메일이 아니며 앱 코드·운영 이용 승인은 별도입니다.`}),signal:AbortSignal.timeout(10000)});if(!r.ok)throw Error('mail_failed');}
}));
