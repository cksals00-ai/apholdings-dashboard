import{test}from'node:test';import assert from'node:assert/strict';import{handle}from'../supabase/functions/b2b-login/core.mjs';
const req=(x={},origin='https://www.apholdings.kr')=>new Request('https://example.test',{method:'POST',headers:{origin,'content-type':'application/json'},body:JSON.stringify({email:'staff@example.test',consent:true,...x})});
test('login email only after same-origin explicit consent, and with one-time token in fragment',async()=>{
let sent;const deps={ready:()=>true,limit:async()=>true,generate:async()=>({hashed_token:'test-hash',verification_type:'magiclink'}),send:async x=>{sent=x;}};
assert.equal((await handle(req({},'https://evil.test'),deps)).status,403);assert.equal((await handle(req({consent:false}),deps)).status,400);assert.equal(sent,undefined);
assert.equal((await handle(req(),deps)).status,202);assert.equal(sent.email,'staff@example.test');assert.equal(new URL(sent.link).hash,'#token_hash=test-hash&type=magiclink');assert.equal(new URL(sent.link).search,'');
});
test('rate limit and mail failure never claim success or expose token',async()=>{let generated=false;const deps={ready:()=>true,limit:async()=>false,generate:async()=>{generated=true;},send:async()=>{}};assert.equal((await handle(req(),deps)).status,429);assert.equal(generated,false);deps.limit=async()=>true;deps.generate=async()=>({hashed_token:'secret'});deps.send=async()=>{throw Error('secret provider details');};const r=await handle(req(),deps);assert.equal(r.status,503);assert.doesNotMatch(await r.text(),/secret/);});
