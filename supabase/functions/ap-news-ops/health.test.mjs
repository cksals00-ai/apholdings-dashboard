import test from 'node:test';
import assert from 'node:assert/strict';
import {complete,assess} from './health.mjs';
const mail={active:3,accepted:3,pending:0,processing:0,retry:0,failed:0,uncertain:0,unconfirmed:0,eligible_missing:0};
const run={ready_verified_at:'2026-10-30T06:00:00+09:00',public_verified_at:'2026-10-30T08:02:00+09:00'};
const issue={status:'published',verified:true};
test('unknown, partial, uncertain and missing eligible recipients never mean complete',()=>{
 assert.throws(()=>complete({accepted:3}));
 for(const key of ['pending','processing','retry','failed','uncertain','unconfirmed','eligible_missing'])assert.equal(complete({...mail,[key]:1}),false);
 assert.equal(complete({...mail,accepted:2}),false);assert.equal(complete(mail),true);
});
test('08:00 progress is separate from final successful report',()=>{
 const a=assess('2026-10-30',new Date('2026-10-29T23:00:00Z'),{},undefined,{...mail,accepted:0,eligible_missing:3});
 assert.equal(a.kind,'progress');assert.match(a.message,/미접수 대상3/);
 const b=assess('2026-10-30',new Date('2026-10-29T23:03:00Z'),run,issue,mail);
 assert.equal(b.kind,'complete');assert.match(b.message,/받은편지함/);
});
test('failed/late stages are reported before recovery finishes',()=>{
 assert.equal(assess('2026-10-30',new Date('2026-10-29T22:15:00Z'),{},undefined,mail).code,'ready_goal');
 assert.equal(assess('2026-10-30',new Date('2026-10-29T23:00:00Z'),{last_error:'source unavailable'},undefined,mail).code,'server_error');
 assert.equal(assess('2026-10-30',new Date('2026-10-29T23:05:00Z'),{},undefined,mail).code,'public_late');
 assert.equal(assess('2026-10-30',new Date('2026-10-29T23:10:00Z'),run,issue,{...mail,eligible_missing:1}).code,'mail_late');
});
