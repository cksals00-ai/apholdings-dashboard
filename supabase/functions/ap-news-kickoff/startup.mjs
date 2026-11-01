// Decisions use UTC timestamps; daily identity is Korean calendar date.
export function decide(timestamp,runs,receipt){
 const now=new Date(timestamp);if(!Number.isFinite(+now)||!Array.isArray(runs))throw Error('unknown_startup_state');
 const kst=new Date(+now+9*3600000),day=kst.toISOString().slice(0,10),minute=kst.getUTCHours()*60+kst.getUTCMinutes();
 if(minute<185||minute>420)return {kind:'outside',day};
 const today=runs.filter(r=>r.head_branch==='main'&&['schedule','workflow_dispatch'].includes(r.event)&&new Date(new Date(r.created_at).getTime()+9*3600000).toISOString().slice(0,10)===day);
 if(today.some(r=>r.status==='in_progress'||r.conclusion==='success'))return {kind:'observed',day};
 if(today.some(r=>r.status!=='completed'))return {kind:'queued',day};
 if(today.length)return {kind:'failure',day};
 if(receipt?.attempts>=3)return {kind:'exhausted',day};
 if(receipt&&+now-+new Date(receipt.updated_at)<15*60000)return {kind:'waiting',day};
 return {kind:'start',day};
}
