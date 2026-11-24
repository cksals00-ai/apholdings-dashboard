import test from 'node:test';
import assert from 'node:assert/strict';
import { adViewState, renderYouTubeAdCard, createYouTubeAdsPanel } from './youtube-ads.mjs';

const now=Date.parse('2026-10-27T08:00:00Z');
const observation={promotion_id:'123',video_id:'abcdefghijk',ad_title:'A lesson',source:'youtube_studio',observed_at:'2026-10-27T07:00:00Z',succeeded:true,status:'활성',cost_krw:0,impressions:0,views:null,subscribers:0,follow_on_views:null,ad_budget_krw:45000,start_date:'2026-10-27',end_date:'2026-10-31'};

test('unknown views stay unknown while verified zero spend and impressions display zero',()=>{
  const html=renderYouTubeAdCard(adViewState([observation],[],now));
  assert.match(html,/광고 지출[\s\S]*?₩0/);
  assert.match(html,/노출수[\s\S]*?>0</);
  assert.match(html,/광고 조회수[\s\S]*?미확인/);
  assert.doesNotMatch(html,/NaN|undefined/);
});
test('a failed newer check retains successful data with failure and stale warnings',()=>{
  const old={...observation,observed_at:'2026-10-27T01:00:00Z',cost_krw:1200,impressions:315,views:41};
  const failure={...observation,observed_at:'2026-10-27T07:30:00Z',succeeded:false,status:null,cost_krw:null,impressions:null,views:null};
  const state=adViewState([old,failure],[],now);
  assert.equal(state.observation.views,41);
  assert.equal(state.studioFailed,true);
  assert.equal(state.stale,true);
  const html=renderYouTubeAdCard(state);
  assert.match(html,/₩1,200/);assert.match(html,/최근 점검 실패/);assert.match(html,/4시간 이상/);
});
test('successful API connection with unavailable campaign does not supply or zero Studio metrics',()=>{
  const api={promotion_id:'123',observed_at:'2026-10-27T07:40:00Z',ok:true,report_state:'campaign_unavailable',currency:'KRW',account_time_zone:'Asia/Seoul'};
  const html=renderYouTubeAdCard(adViewState([{...observation,views:23}], [api],now));
  assert.match(html,/연결 확인 성공/);assert.match(html,/이번 Studio 프로모션의 캠페인 보고는 API에서 반환되지 않았습니다/);assert.match(html,/광고 조회수[\s\S]*?>23</);
  const empty=renderYouTubeAdCard(adViewState([], [api],now));
  assert.match(empty,/성과 확인 대기/);assert.doesNotMatch(empty,/₩0/);
});
test('sorting never sums cumulative snapshots or combines a different promotion API check',()=>{
  const state=adViewState([{...observation,views:8}, {...observation,observed_at:'2026-10-27T07:45:00Z',views:12}], [{promotion_id:'999',observed_at:'2026-10-27T07:50:00Z',ok:true}],now);
  assert.equal(state.observation.views,12);assert.equal(state.api,null);
});
test('HTML injection and malformed video identities cannot become executable links',()=>{
  const html=renderYouTubeAdCard(adViewState([{...observation,ad_title:'<img src=x onerror=alert(1)>',status:'<script>evil()</script>',video_id:'javascript:alert(1)'}],[],now));
  assert.doesNotMatch(html,/<img|<script|href="javascript:/);assert.match(html,/&lt;img/);
});
test('actual spend over the recorded budget is visible as a warning',()=>{
  assert.match(renderYouTubeAdCard(adViewState([{...observation,cost_krw:45001}],[],now)),/기록된 광고 예산 초과/);
});
function dbWith(read){return {from(table){return {select(){return this;},order(){return this;},limit(){return read(table);}};}};}
test('database failure preserves last loaded values instead of replacing them with zeros',async()=>{
  let fail=false;const root={innerHTML:'',querySelector(){return {set textContent(value){root.innerHTML+=value;}};}};
  const panel=createYouTubeAdsPanel(dbWith(t=>Promise.resolve(fail?{error:{message:'offline'}}:{data:t.endsWith('observations')?[{...observation,views:27}]:[]})),()=>({id:'owner'}),root);
  assert.equal(await panel.load(),true);fail=true;
  assert.equal(await panel.load(true),false);
  assert.match(root.innerHTML,/광고 조회수[\s\S]*?>27</);assert.match(root.innerHTML,/저장된 기록을 불러오지 못했습니다/);
});
test('logout clears private content and a late response cannot restore it',async()=>{
  let user={id:'owner'},resolve;const pending=new Promise(r=>{resolve=r;});const root={innerHTML:''};
  const panel=createYouTubeAdsPanel(dbWith(()=>pending),()=>user,root);
  const request=panel.load();user=null;panel.clear();resolve({data:[observation]});
  assert.equal(await request,false);assert.equal(root.innerHTML,'');
});
test('opening the panel again fetches newer stored observations without requiring a forced refresh',async()=>{
  let views=27;const root={innerHTML:''};
  const panel=createYouTubeAdsPanel(dbWith(t=>Promise.resolve({data:t.endsWith('observations')?[{...observation,views}]:[]})),()=>({id:'owner'}),root);
  await panel.load();views=28;await panel.load();
  assert.match(root.innerHTML,/광고 조회수[\s\S]*?>28</);
});
