import assert from 'node:assert/strict';
import {beforeEach,test} from 'node:test';
import {downloadSummary,renderDownloads} from '../admin/app-downloads.mjs';
import {androidApps as registry} from '../admin/android-app-registry.mjs';
const apps=[{id:'one',name:'One',status:'live'}],androidApps=[{id:'one',name:'One',package_id:'com.one'}];
const snap={schemaVersion:1,platform:'google',periodStart:'2026-10-07',periodEnd:'2026-11-03',observedAt:'2026-11-03T02:00:00Z',apps:[{packageId:'com.one',status:'production',installs:0,metric:'installed_users',complete:true}]};
const metrics=Array.from({length:28},(_,i)=>({app_id:'one',day:new Date(Date.UTC(2026,9,7+i)).toISOString().slice(0,10),downloads:1}));
const opts={apps,androidApps,metrics,today:'2026-11-03',runtime:[{id:'google_downloads',detail:JSON.stringify(snap)}]};
assert.equal(downloadSummary(opts).total,28);
assert.equal(downloadSummary({...opts,metrics:[]}).total,null);
assert.equal(downloadSummary({...opts,metrics:[metrics[0]]}).apple,1);
assert.equal(downloadSummary({...opts,metrics:[metrics[0]]}).total,null);
assert.equal(downloadSummary({...opts,runtime:[]}).google,null);
assert.equal(downloadSummary({...opts,runtime:[{id:'google_downloads',detail:JSON.stringify({...snap,periodEnd:'2026-11-02'})}]}).total,null);
const missing=structuredClone(snap); missing.apps[0].installs=null;
assert.equal(downloadSummary({...opts,runtime:[{id:'google_downloads',detail:JSON.stringify(missing)}]}).total,null);
const duplicate=structuredClone(snap);duplicate.apps.push({...duplicate.apps[0]});
assert.equal(downloadSummary({...opts,runtime:[{id:'google_downloads',detail:JSON.stringify(duplicate)}]}).google,null);
assert.equal(downloadSummary({...opts,runtime:[{id:'google_downloads',detail:'null'}]}).total,null);
assert.equal(downloadSummary({...opts,metricsError:true}).apple,null);
assert.equal(downloadSummary({...opts,metrics:metrics.map(r=>({...r,platform:'google'}))}).apple,null);
assert.ok(renderDownloads({...opts,runtime:[]}).includes('전체 합계 미확정'));
assert.ok(renderDownloads(opts).includes('고유 사용자 수가 아닙니다'));
const bad=structuredClone(snap);bad.apps[0].installs=-1;
assert.equal(downloadSummary({...opts,runtime:[{id:'google_downloads',detail:JSON.stringify(bad)}]}).google,null);
console.log('download aggregation and missingness assertions passed');

assert.ok(!renderDownloads({...opts,androidApps:[{...androidApps[0],name:'<script>alert(1)</script>'}]}).includes('<script>'));

const observedAt='2026-11-20T05:05:06.712Z';
const readAt=Date.parse('2026-11-22T00:00:00Z');
beforeEach(({mock})=>mock.method(Date,'now',()=>readAt));
const observation={schemaVersion:1,kind:'release_status_observation',platform:'google',observedAt,apps:[
  {packageId:'com.one',status:'draft'},
]};
const observationRow=(detail=observation)=>({id:'google_release_status',detail:JSON.stringify(detail)});
const withRelease=(detail=observation)=>({...opts,runtime:[...opts.runtime,observationRow(detail)]});

test('newer Play Console observation supplies the 17 current release labels while the Nov 3 report stays stale',()=>{
  const production=[
    'kr.apholdings.hajeungbond','com.apholdings.dawngrace','com.aplocalift.hangeulcubs',
    'com.apholdings.irongrade','com.apholdings.kconcerttrip','com.apholdings.kranker',
    'com.apholdings.kscan','com.apholdings.theotherhours','com.apholdings.moonshot',
    'com.apholdings.lightlist','com.apholdings.safelist','kr.apholdings.sonoinspect',
    'kr.apholdings.investranker','com.hotelranker','com.apholdings.foldblock',
  ].map(packageId=>({packageId,status:'production'}));
  const report={...snap,apps:[
    {packageId:'com.apholdings.foldblock',status:'not_created',installs:null,sourceStatus:'quota_blocked'},
    {packageId:'com.apholdings.seunggyuandme',status:'production',installs:9,metric:'installed_users',complete:true},
    {packageId:'com.quizarena',status:'in_review',installs:0,metric:'installed_users',complete:true},
  ]};
  const current={today:'2026-11-20',androidApps:registry,runtime:[
    {id:'google_downloads',detail:JSON.stringify(report)},
    {id:'google_downloads_sync',status:'source_error'},
    observationRow({...observation,apps:[...production,
      {packageId:'com.quizarena',status:'internal'},
      {packageId:'com.apholdings.dadandme',status:'draft'},
    ]}),
  ]};
  const summary=downloadSummary(current);
  assert.equal(summary.googleRows.length,17);
  assert.equal(summary.googleRows.filter(row=>row.releaseStatus==='production').length,15);
  assert.equal(summary.googleRows.find(row=>row.releaseStatus==='internal')?.id,'QuizRanker');
  const draft=summary.googleRows.find(row=>row.releaseStatus==='draft');
  assert.equal(draft?.id,'SeunggyuAndMe');
  assert.equal(draft?.package_id,'com.apholdings.dadandme');
  assert.equal(summary.releaseStatusObservedAt,observedAt);
  assert.deepEqual(summary.snapshot,report);
  assert.equal(summary.samePeriod,false);
  assert.equal(summary.google,null);
  assert.equal(summary.total,null);
  assert.ok(summary.googleRows.every(row=>row.value===null && !row.complete));
  const html=renderDownloads(current);
  assert.match(html,/<td>초안<\/td><td>집계 대기<\/td>/);
  assert.match(html,/Google Play 출시 상태 확인/);
  for(const time of [observedAt,report.observedAt]) {
    assert.ok(html.includes(new Date(time).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})));
  }
  assert.match(html,/자동 수집 오류 · 이전 수집 결과 유지/);
  assert.match(html,/Google 집계 대기/);
});

test('release observations cannot change install facts, including zero and raw registration eligibility',()=>{
  const rawOnly=downloadSummary(opts);
  const withFakeMetrics=withRelease({...observation,apps:[{
    ...observation.apps[0],installs:123,metric:'installed_users',complete:false,sourceStatus:'source_error',
  }]});
  const summary=downloadSummary(withFakeMetrics);
  assert.equal(summary.googleRows[0].releaseStatus,'draft');
  for(const key of ['value','complete','sourceStatus']) {
    assert.equal(summary.googleRows[0][key],rawOnly.googleRows[0][key]);
  }
  assert.equal(summary.google,0);
  assert.equal(summary.total,28);
  assert.match(renderDownloads(withFakeMetrics),/<td>초안<\/td><td>0건<\/td>/);
  const nowUnregistered=withRelease({...observation,apps:[{packageId:'com.one',status:'not_created'}]});
  assert.equal(downloadSummary(nowUnregistered).total,28);
  assert.match(renderDownloads(nowUnregistered),/<td>미생성 · 주간 한도<\/td><td>0건<\/td>/);

  const missingSnapshot={...withFakeMetrics,runtime:withFakeMetrics.runtime.slice(1)};
  const missingSummary=downloadSummary(missingSnapshot);
  assert.equal(missingSummary.googleRows[0].releaseStatus,'draft');
  assert.equal(missingSummary.googleRows[0].value,null);
  assert.equal(missingSummary.googleRows[0].complete,false);
  assert.equal(missingSummary.googleRows[0].sourceStatus,'uncollected');
  assert.equal(missingSummary.google,null);
  assert.equal(missingSummary.total,null);

  const extraApp={id:'two',name:'Two',package_id:'com.two'};
  const rawWithUnregistered={...snap,apps:[...snap.apps,{packageId:'com.two',status:'not_created'}]};
  const current={...opts,androidApps:[...androidApps,extraApp],runtime:[
    {id:'google_downloads',detail:JSON.stringify(rawWithUnregistered)},
    observationRow({...observation,apps:[{packageId:'com.two',status:'production'}]}),
  ]};
  assert.equal(downloadSummary(current).googleRows[1].releaseStatus,'production');
  assert.equal(downloadSummary(current).total,28);
});

test('an automatically collected install timestamp does not refresh copied release statuses',()=>{
  const report={...snap,periodStart:'2026-10-25',periodEnd:'2026-11-21',collectionMode:'automatic_official',observedAt:'2026-11-21T01:00:00Z'};
  const current={today:report.periodEnd,androidApps,runtime:[
    {id:'google_downloads',detail:JSON.stringify(report)},
    observationRow(),
  ]};
  const summary=downloadSummary(current);
  assert.equal(summary.googleRows[0].releaseStatus,'draft');
  assert.equal(summary.releaseStatusObservedAt,observedAt);
  assert.equal(summary.google,0);
  assert.equal(summary.samePeriod,true);
  assert.equal(summary.googleRows[0].complete,true);
});

test('a release observation after the reading clock uses the raw status and leaves installs pending',()=>{
  const atReadTime=new Date(readAt).toISOString();
  const latest=withRelease({...observation,observedAt:atReadTime});
  assert.equal(downloadSummary(latest).releaseStatusObservedAt,atReadTime);

  const future={...withRelease({...observation,observedAt:new Date(readAt+1).toISOString(),apps:[
    {...observation.apps[0],installs:500,metric:'installed_users',complete:true},
  ]}),today:'2026-11-23'};
  const summary=downloadSummary(future);
  assert.equal(summary.googleRows[0].releaseStatus,'production');
  assert.equal(summary.releaseStatusObservedAt,null);
  assert.equal(summary.googleRows[0].value,null);
  assert.equal(summary.google,null);
  assert.equal(summary.total,null);
  const html=renderDownloads(future);
  assert.match(html,/<td>정식 공개<\/td><td>집계 대기<\/td>/);
  assert.doesNotMatch(html,/Google Play 출시 상태 확인/);
});

test('ambiguous, malformed, older, and inexact release observations retain the raw release fallback',()=>{
  const invalid=[
    null,
    {...observation,schemaVersion:2},
    {...observation,kind:'install_snapshot'},
    {...observation,platform:'apple'},
    {...observation,observedAt:'2026-11-02T00:00:00Z'},
    {...observation,observedAt:snap.observedAt},
    {...observation,observedAt:'2026-11-20'},
    {...observation,observedAt:'2026-11-31T02:00:00Z'},
    {...observation,observedAt:'<script>alert(1)</script>'},
    {...observation,apps:{}},
    {...observation,apps:[{packageId:'com.One',status:'draft'}]},
    {...observation,apps:[{packageId:'com.one',status:' draft'}]},
    {...observation,apps:[{packageId:'com.one',status:'constructor'}]},
    {...observation,apps:[{packageId:'com.one',status:'<script>alert(1)</script>'}]},
    {...observation,apps:[...observation.apps,{packageId:'com.one',status:'internal'}]},
  ].map(withRelease);
  invalid.push({...opts,runtime:[...opts.runtime,{id:'google_release_status',detail:'bad JSON'}]});
  invalid.push({...opts,runtime:[...opts.runtime,observationRow(),observationRow({...observation,apps:[]})]});
  for(const current of invalid) {
    const summary=downloadSummary(current);
    assert.equal(summary.googleRows[0].releaseStatus,'production',JSON.stringify(current.runtime.slice(1)));
    assert.equal(summary.releaseStatusObservedAt,null);
    assert.equal(summary.total,28);
  }
});

test('valid observations match only exact packages and leave the input and untrusted display text untouched',()=>{
  const current=withRelease({...observation,source:'<script>source</script>',apps:[
    null,
    {...observation.apps[0],name:'<script>observation</script>'},
    {packageId:'com.apholdings.seunggyuandme',status:'production'},
  ]});
  const apps=[...current.androidApps,registry.find(app=>app.id==='SeunggyuAndMe')];
  current.androidApps=apps;
  const before=structuredClone(current);
  const summary=downloadSummary(current);
  assert.equal(summary.googleRows[0].releaseStatus,'draft');
  assert.equal(summary.googleRows[1].releaseStatus,null);
  assert.doesNotMatch(renderDownloads(current),/<script>|&lt;script&gt;/);
  assert.deepEqual(current,before);
});
