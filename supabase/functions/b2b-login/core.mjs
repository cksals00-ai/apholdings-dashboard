const ORIGIN='https://www.apholdings.kr';
const headers={'Content-Type':'application/json','Access-Control-Allow-Origin':ORIGIN,'Access-Control-Allow-Headers':'content-type,apikey','Access-Control-Allow-Methods':'POST,OPTIONS','Cache-Control':'no-store','Vary':'Origin'};
const reply=(status,message)=>new Response(JSON.stringify({message}),{status,headers});
export async function handle(req,deps){
 if(req.headers.get('origin')!==ORIGIN)return reply(403,'허용되지 않은 요청입니다.');
 if(req.method==='OPTIONS')return new Response(null,{status:204,headers});if(req.method!=='POST')return reply(405,'POST 요청만 지원합니다.');
 try{const raw=await req.text();if(raw.length>1024)return reply(400,'입력을 확인해 주세요.');const x=JSON.parse(raw),email=String(x.email||'').trim().toLowerCase();
 if(x.consent!==true||email.length>254||!/^\S+@[^\s@]+\.[^\s@]+$/.test(email))return reply(400,'회사 이메일과 개인정보 동의를 확인해 주세요.');
 if(!deps.ready())return reply(503,'이메일 연결을 준비하고 있습니다.');
 if(!await deps.limit(email,req.headers.get('cf-connecting-ip')||req.headers.get('x-forwarded-for')||'unknown'))return reply(429,'요청이 많습니다. 잠시 후 다시 시도해 주세요.');
 const generated=await deps.generate(email);if(!generated.hashed_token)throw Error('token_missing');
 const link=`${ORIGIN}/hajeung/#token_hash=${encodeURIComponent(generated.hashed_token)}&type=magiclink`;
 await deps.send({email,link});return reply(202,'이메일의 확인 링크를 열어주세요.');
 }catch{return reply(503,'확인 메일을 보내지 못했습니다. 잠시 후 다시 시도해 주세요.');}
}
