const localTime=value=>new Date(new Date(value).getTime()+9*3600000).toISOString().replace('Z','+09:00');
const blockers=['pending','processing','retry','failed','uncertain','unconfirmed','eligible_missing'];
export function complete(mail){
 for(const key of ['active','accepted',...blockers])if(!Number.isInteger(mail?.[key])||mail[key]<0)throw Error('mail_health_unknown_'+key);
 return mail.accepted>=mail.active&&blockers.every(key=>mail[key]===0);
}
export function assess(day,now,run={},issue,mail){
 const done=complete(mail),kst=new Date(now.getTime()+9*3600000),h=kst.getUTCHours(),m=kst.getUTCMinutes();
 const published=issue?.status==='published'&&issue?.verified===true&&!!run?.public_verified_at;
 const counts=`메일 제공사 접수${mail.accepted}건·대기${mail.pending}·처리중${mail.processing}·재시도${mail.retry}·실패${mail.failed}·결과불명${mail.uncertain}·접수미확인${mail.unconfirmed}·미접수 대상${mail.eligible_missing}`;
 if(h>=8&&published&&done)return {kind:'complete',code:'complete',message:`${day} 공개 검증 기록${localTime(run.public_verified_at)}. 확인 시각${kst.toISOString().replace('Z','+09:00')}. ${counts}. 전체 확인완료 active 대상 접수를 확인했습니다. 받은편지함 도착 확인을 의미하지는 않습니다.`};
 if(h>=7&&run?.last_error)return {kind:'alert',code:'server_error',message:`현재 서버 오류: ${run.last_error}. 복구 완료 전 상태를 먼저 보고합니다. ${counts}.`};
 if(h>8||h===8&&m>=5){
  if(!published)return {kind:'alert',code:'public_late',message:`08:05까지 오늘자 공개 검증이 완료되지 않았습니다. 복구 완료를 기다리지 않고 먼저 알립니다. ${counts}.`};
  if((h>8||m>=10)&&!done)return {kind:'alert',code:'mail_late',message:`08:10 이후에도 전체 대상 메일 제공사 접수가 완료되지 않았습니다. ${counts}.`};
 }
 if(h===7&&!run?.ready_verified_at){
  if(m>=46)return {kind:'alert',code:'ready_deadline',message:'07:45 준비 마감 이후에도 완성본 서버 검증 기록이 없습니다. 제작·전달 장애 가능성을 먼저 알립니다.'};
  if(m>=15)return {kind:'alert',code:'ready_goal',message:'07:15 제작·검증·서버 전달 목표까지 완성본 검증 기록이 없습니다. 준비 지연을 먼저 알립니다.'};
 }
 if(h===8&&m<5)return {kind:'progress',code:'0800',message:`오전8시 첫 상태입니다. 완성본 서버 검증${run?.ready_verified_at?'완료':'미확인'}, 홈페이지 공개${published?'검증 완료':'아직 미완료'}. ${counts}. 진행 중이며 정시 완료로 표시하지 않습니다.`};
 return {kind:'quiet'};
}
