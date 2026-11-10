// Deploy exactly the archive's commit. github.sha can predate a long reservation.
function deploymentPayload(sha,id,token){
 if(!/^[a-f0-9]{40}$/.test(sha)||!Number.isSafeInteger(id)||id<1||!token)throw Error('Invalid Pages deployment provenance');
 return {artifact_id:id,pages_build_version:sha,oidc_token:token};
}
function selectArtifact(artifacts,name){const rows=artifacts.filter(a=>a.name===name&&!a.expired);if(rows.length!==1)throw Error('Missing or ambiguous Pages artifact');return rows[0].id;}
async function deploy({github,core,context,sha,artifactName,sleep=ms=>new Promise(r=>setTimeout(r,ms))}){
 const repo=context.repo,run_id=context.runId;
 const artifacts=await github.paginate(github.rest.actions.listWorkflowRunArtifacts,{...repo,run_id,per_page:100});
 const artifact=selectArtifact(artifacts,artifactName),token=await core.getIDToken();
 const response=await github.request('POST /repos/{owner}/{repo}/pages/deployments',{...repo,...deploymentPayload(sha,artifact,token)});
 const id=response.data.id||response.data.status_url?.split('/').pop();if(!id)throw Error('Missing Pages deployment ID');
 core.info(`Deploying packaged commit ${sha}; deployment ${id}`);
 for(let attempt=0;attempt<60;attempt++){
  await sleep(5000);
  const {data}=await github.request('GET /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}',{...repo,pages_deployment_id:id});
  if(data.status==='succeed'){core.setOutput('page_url',response.data.page_url);return;}
  if(['deployment_failed','deployment_content_failed','deployment_cancelled','deployment_lost'].includes(data.status))throw Error('Pages '+data.status);
 }
 try{await github.request('POST /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}/cancel',{...repo,pages_deployment_id:id});}catch{}
 throw Error('Pages deployment timed out');
}
module.exports={deploymentPayload,selectArtifact,deploy};
