import {test} from 'node:test';
import assert from 'node:assert/strict';
import {application,request,attachment,statusLabel} from '../hajeung/model.mjs';
test('company application trims required fields but does not accept invented identity',()=>{
 assert.deepEqual(application({name:' 담당자 ',company:' 회사 ',device:'ios'}),{name:'담당자',company:'회사',device:'ios'});
 for(const x of [{name:'',company:'회사',device:'ios'},{name:'A',company:'',device:'ios'},{name:'A',company:'B',device:'admin'}]) assert.throws(()=>application(x));
});
test('request limits and plain text survive without HTML interpolation',()=>{
 const d=request({kind:'bug',title:'<script>',body:'오류가 발생했습니다',screen:'목록',version:'1.0',device:'iPhone'});assert.equal(d.title,'<script>');
 assert.throws(()=>request({...d,body:''})); assert.throws(()=>request({...d,kind:'approved'}));
});
test('attachments are size limited raster images; empty, SVG and fake extensions are rejected',()=>{
 assert.equal(attachment({type:'image/png',size:1024}).type,'image/png');
 for(const x of [{type:'image/svg+xml',size:20},{type:'image/png',size:0},{type:'image/jpeg',size:6*1024*1024}]) assert.throws(()=>attachment(x));
});
test('approval and issuance are distinct user facing states',()=>{
 assert.equal(statusLabel('approved'),'승인 · 앱 코드 발급 대기');assert.equal(statusLabel('issued'),'앱 코드 발급됨');assert.equal(statusLabel('not-loaded'),'확인 필요');
});
