// A run being in progress only proves preparation. Jobs must be from its latest attempt.
export function decide(timestamp,runs,receipt){
 const now=new Date(timestamp);if(!Number.isFinite(+now)||!Array.isArray(runs))throw Error('unknown_startup_state');
 const kst=new Date(+now+9*3600000),day=kst.toISOString().slice(0,10),minute=kst.getUTCHours()*60+kst.getUTCMinutes();
 if(minute<165||minute>420)return {kind:'outside',day};
 const today=runs.filter(r=>{
  if(!Number.isFinite(+new Date(r.created_at)))throw Error('unknown_run_date');
  return r.head_branch==='main'&&['schedule','workflow_dispatch'].includes(r.event)&&new Date(+new Date(r.created_at)+9*3600000).toISOString().slice(0,10)===day;
 });
 for(const r of today){
  if(!['queued','waiting','pending','requested','in_progress','completed'].includes(r.status))throw Error('unknown_run_status');
  if(!Array.isArray(r.jobs))throw Error('unknown_latest_attempt_jobs');
  if(r.jobs.some(j=>!Array.isArray(j.steps)))throw Error('unknown_job_steps');
 }
 const actual=today.filter(r=>r.jobs.some(j=>j.steps.some(s=>s.name==='Supervise credential-free source, copy, art and document production'&&typeof s.started_at==='string'&&Number.isFinite(+new Date(s.started_at))&&+new Date(s.started_at)<=+now&&(s.status==='in_progress'||(s.status==='completed'&&s.conclusion==='success')))));
 if(actual.some(r=>r.status==='in_progress'))return {kind:'generating',day};
 if(actual.some(r=>r.conclusion==='success'))return {kind:'observed',day};
 if(today.some(r=>r.status==='in_progress'))return {kind:'preparing',day};
 if(today.some(r=>r.status!=='completed'))return {kind:'queued',day};
 if(today.length)return {kind:'failure',day};
 if(receipt&&(!Number.isInteger(receipt.attempts)||!Number.isFinite(+new Date(receipt.updated_at))))throw Error('unknown_claim_receipt');
 if(receipt?.attempts>=3)return {kind:'exhausted',day};
 if(receipt&&+now-+new Date(receipt.updated_at)<15*60000)return {kind:'waiting',day};
 return {kind:'start',day};
}
