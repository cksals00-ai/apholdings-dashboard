import test from 'node:test';
import assert from 'node:assert/strict';
import * as module from './newsletter.js';

const data=()=>({mail_ready:true,counts:{active:3,confirmed_active:3},issues:[{issue_date:'2026-10-27',number:19,title:'오늘 호',status:'published',verified:true,web_url:'https://www.apholdings.kr/ko/news/daily/2026-10-27/'}],pipeline:{today:'2026-10-27',checked_at:'2026-10-27T05:00:00Z',runs:[{issue_date:'2026-10-27',title:'오늘 호',ready_at:'2026-10-27T04:00:00Z',ready_verified_at:'2026-10-27T04:01:00Z',registered_at:'2026-10-27T04:02:00Z',public_verified_at:'2026-10-27T04:02:00Z',last_state:'published'}],delivery_summary:[{issue_date:'2026-10-27',accepted:3,pending:0,processing:0,retry:0,failed:0,uncertain:0,unconfirmed:0,cancelled:0,total:3}]}});
function summary(d,now){assert.equal(typeof module.pipelineSummary,'function','Milestone status renderer is missing');return module.pipelineSummary(d,now);}

test('검증된 전달·공개와 실제 전송 서비스 접수 건수를 표시한다',()=>{
 const s=summary(data());
 assert.equal(s.day,'2026-10-27');assert.equal(s.ready.tone,'ok');assert.equal(s.publication.tone,'ok');assert.equal(s.mail.tone,'ok');
 assert.match(s.mail.label,/3건/);assert.doesNotMatch(s.mail.label,/도착|수신 완료/);
});

test('내일 완성본이 있어도 오늘 상태를 대체하지 않는다',()=>{
 const d=data();d.pipeline.runs.unshift({issue_date:'2026-10-28',ready_at:'2026-10-27T04:00:00Z',ready_verified_at:'2026-10-27T04:01:00Z'});
 assert.equal(summary(d).title,'오늘 호');
});

test('공개 URL이나 DB 등록만으로 공개 검증 완료를 주장하지 않는다',()=>{
 const d=data();d.pipeline.runs=[];
 assert.notEqual(summary(d).publication.tone,'ok');assert.notEqual(summary(d).ready.tone,'ok');
});

test('전달된 미발행 호는 예약 대기이고 메일 접수를 주장하지 않는다',()=>{
 const d=data();d.issues=[];delete d.pipeline.runs[0].registered_at;delete d.pipeline.runs[0].public_verified_at;d.pipeline.delivery_summary=[];
 const s=summary(d);assert.match(s.publication.label,/예약 대기/);assert.notEqual(s.mail.tone,'ok');
});

test('실패·재시도·결과 불명과 mail_ready=false를 완료로 축약하지 않는다',()=>{
 for(const state of ['failed','retry','uncertain','unconfirmed','pending','processing']){
  const d=data();d.pipeline.delivery_summary[0][state]=1;d.pipeline.delivery_summary[0].total=4;
  assert.notEqual(summary(d).mail.tone,'ok',state);
 }
 const d=data();d.mail_ready=false;d.pipeline.delivery_summary=[];assert.match(summary(d).mail.label,/연결/);
});

test('날짜 기본값은 한국시간을 사용한다',()=>{
 const d=data();delete d.pipeline.today;
 assert.equal(summary(d,new Date('2026-10-27T15:10:00Z')).day,'2026-10-28');
});

test('화면은 제목과 오류를 이스케이프하고 상세 기록을 접는다',()=>{
 const d=data();d.pipeline.runs[0].title='<img src=x onerror=alert(1)>';d.pipeline.runs[0].last_error='<script>bad()</script>';
 assert.equal(typeof module.renderPipeline,'function','Compact pipeline panel is missing');
 const html=module.renderPipeline(d);assert.match(html,/&lt;img/);assert.doesNotMatch(html,/<script>|onerror=alert\(1\)>/);
 assert.match(html,/<details/);assert.match(html,/서버 전달/);assert.match(html,/홈페이지 발행/);assert.match(html,/메일 발송/);
});
