// Pure policy: no AI, content generation, subscriber mutation or mail dispatch.
export function decideRecovery(day,now,publication,runs,attempts,done){
 if(!Array.isArray(runs)||!Number.isInteger(attempts)||attempts<0)throw Error('recovery_state_unknown');
 const kst=new Date(+new Date(now)+9*3600000),minute=kst.getUTCHours()*60+kst.getUTCMinutes();
 if(kst.toISOString().slice(0,10)!==day)throw Error('recovery_day_mismatch');
 if(done||minute<460||minute>=600)return {kind:'quiet'};
 const today=runs.filter(r=>r.head_branch==='main'&&['workflow_dispatch','schedule'].includes(r.event)&&new Date(+new Date(r.created_at)+9*3600000).toISOString().slice(0,10)===day&&/ (reservation|publication)$/.test(r.display_title||''));
 if(today.some(r=>r.status!=='completed'))return {kind:'wait'};
 if(!publication?.ready_verified_at)return {kind:minute>=480?'terminal':'wait',reason:'완성본 서버 검증 기록이 없습니다. 오래된 호를 대신 발행하지 않았습니다.'};
 if(attempts>=3)return {kind:'terminal',reason:'기존 완성본으로 서버 복구를 3회 요청했지만 공개·전원 메일 접수가 완료되지 않았습니다.'};
 return {kind:'dispatch'};
}
export function notificationKey(day,detail){return detail?.terminal===true?day+':terminal-failure':null;}
