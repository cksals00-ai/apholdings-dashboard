import test from 'node:test';import assert from 'node:assert/strict';import {decide} from './startup.mjs';
const now='2026-11-01T18:10:00Z';
const run=(extra={})=>({event:'schedule',head_branch:'main',created_at:now,status:'in_progress',jobs:[],...extra});
const step=(extra={})=>({name:'Supervise credential-free source, copy, art and document production',status:'in_progress',started_at:now,...extra});
test('prewarm starts at 02:45 inclusive through 07:00',()=>{for(const t of ['2026-11-01T17:45:00Z','2026-11-01T22:00:59Z'])assert.equal(decide(t,[],null).kind,'start');for(const t of ['2026-11-01T17:44:59Z','2026-11-01T22:01:00Z'])assert.equal(decide(t,[],null).kind,'outside')});
test('preparing runner is not generation',()=>assert.equal(decide(now,[run()],null).kind,'preparing'));
test('waiting queued runner never duplicates',()=>assert.equal(decide(now,[run({status:'queued'})],null).kind,'queued'));
test('actual supervisor step proves generation',()=>assert.equal(decide(now,[run({jobs:[{steps:[step()]}]})],null).kind,'generating'));
test('skipped supervisor does not count',()=>assert.equal(decide(now,[run({jobs:[{steps:[step({status:'completed',conclusion:'skipped'})]}]})],null).kind,'preparing'));
test('success without actual step cannot count',()=>assert.equal(decide(now,[run({status:'completed',conclusion:'success'})],null).kind,'failure'));
test('completed real generation counts',()=>assert.equal(decide(now,[run({status:'completed',conclusion:'success',jobs:[{steps:[step({status:'completed',conclusion:'success'})]}]})],null).kind,'observed'));
test('wrong branch and rollout smoke cannot suppress edition',()=>{for(const extra of [{head_branch:'test'},{event:'workflow_run'}])assert.equal(decide(now,[run(extra)],null).kind,'start')});
test('unknown responses fail closed',()=>{assert.throws(()=>decide(now,null,null));assert.throws(()=>decide(now,[run({jobs:undefined})],null));assert.throws(()=>decide(now,[run({created_at:'broken'})],null))});
test('claims preserve cooldown and attempt limit',()=>{assert.equal(decide(now,[],{attempts:1,updated_at:now}).kind,'waiting');assert.equal(decide(now,[],{attempts:3,updated_at:now}).kind,'exhausted')});

test('missing actual start timestamp cannot prove generation',()=>assert.equal(decide(now,[run({jobs:[{steps:[step({started_at:null})]}]})],null).kind,'preparing'));
