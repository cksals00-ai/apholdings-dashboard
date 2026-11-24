const test=require('node:test'),assert=require('node:assert/strict');
const {deploymentPayload,selectArtifact}=require('./newsletter_pages.cjs');
test('uses packaged commit rather than stale workflow event SHA',()=>{assert.equal(deploymentPayload('a'.repeat(40),42,'oidc').pages_build_version,'a'.repeat(40));assert.throws(()=>deploymentPayload('main',42,'oidc'));});
test('selects one attempt-specific artifact and rejects missing or ambiguous artifacts',()=>{const a={id:42,name:'pages-123-2',expired:false};assert.equal(selectArtifact([a,{id:43,name:'pages-123-1'}],'pages-123-2'),42);assert.throws(()=>selectArtifact([a,a],'pages-123-2'));assert.throws(()=>selectArtifact([{...a,expired:true}],'pages-123-2'));});
const {deploy}=require('./newsletter_pages.cjs');
test('deployment submits actual artifact commit and polls that deployment to success',async()=>{
 const calls=[],github={rest:{actions:{listWorkflowRunArtifacts(){}}},paginate:async()=>[{id:42,name:'pages-1-1',expired:false}],request:async(route,args)=>{calls.push([route,args]);return route.startsWith('POST')?{data:{id:'new-deployment',page_url:'https://www.apholdings.kr'}}:{data:{status:'succeed'}};}};
 const outputs={},core={getIDToken:async()=>'test-oidc',info(){},setOutput:(k,v)=>outputs[k]=v};
 await deploy({github,core,context:{repo:{owner:'owner',repo:'repo'},runId:1},sha:'b'.repeat(40),artifactName:'pages-1-1',sleep:async()=>{}});
 assert.equal(calls[0][1].pages_build_version,'b'.repeat(40));assert.equal(calls[1][1].pages_deployment_id,'new-deployment');assert.equal(outputs.page_url,'https://www.apholdings.kr');
});
test('failed Pages state cannot be reported as success',async()=>{
 const github={rest:{actions:{listWorkflowRunArtifacts(){}}},paginate:async()=>[{id:42,name:'p'}],request:async route=>route.startsWith('POST')?{data:{id:'d'}}:{data:{status:'deployment_failed'}}};
 await assert.rejects(deploy({github,core:{getIDToken:async()=>'oidc',info(){},setOutput(){throw Error('false success');}},context:{repo:{},runId:1},sha:'c'.repeat(40),artifactName:'p',sleep:async()=>{}}),/deployment_failed/);
});
