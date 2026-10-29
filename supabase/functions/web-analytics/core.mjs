export const HOSTS=['www.apholdings.kr','apholdings.kr','edu.apholdings.kr','games.apholdings.kr','ent.apholdings.kr','shop.apholdings.kr','sports.apholdings.kr'];
// 머니 머지(/play) 이벤트 — 2026-10-29. 도착 경로는 ap-analytics.js 가 고정 목록 이름으로만 보낸다.
export const MM_ARRIVALS={instagram:'money_merge_arrival_instagram',tiktok:'money_merge_arrival_tiktok',youtube:'money_merge_arrival_youtube',share:'money_merge_arrival_share'};
export const MM_OTHER=['money_merge_arrival_lia_other','money_merge_arrival_other'];
export const MM_GAME={starts:'mm_start',gameOvers:'mm_game_over',loginClicks:'mm_login_click',loginBlocked:'mm_login_blocked_inapp',logins:'mm_login_success',submits:'mm_rank_submit',shares:'mm_share'};
export const MM_EVENTS=[...Object.values(MM_ARRIVALS),...MM_OTHER,...Object.values(MM_GAME)];
export const ownerAllowed=user=>Boolean(user?.email_confirmed_at && user?.email?.toLowerCase()==='cksals00@gmail.com');
export const reportRequest=()=>({dateRanges:[{startDate:'28daysAgo',endDate:'today'}],dimensions:[{name:'hostName'},{name:'eventName'},{name:'date'}],metrics:[{name:'eventCount'}],dimensionFilter:{andGroup:{expressions:[{filter:{fieldName:'hostName',inListFilter:{values:HOSTS}}},{filter:{fieldName:'eventName',inListFilter:{values:['page_view','courtmate_blog_arrival',...MM_EVENTS]}}}]}},limit:10000,keepEmptyRows:false});
export function summarize(report){
 const raw=(report.rows||[]).map(r=>({host:r.dimensionValues?.[0]?.value,event:r.dimensionValues?.[1]?.value,day:r.dimensionValues?.[2]?.value,count:Number(r.metricValues?.[0]?.value)})).filter(r=>HOSTS.includes(r.host)&&Number.isFinite(r.count)&&r.count>=0);
 const sites=HOSTS.filter(h=>h!=='apholdings.kr').map(host=>{const rows=raw.filter(r=>r.event==='page_view'&&(r.host===host||(host==='www.apholdings.kr'&&r.host==='apholdings.kr')));return {host,views:rows.length?rows.reduce((n,r)=>n+r.count,0):null}});
 const arrival=raw.filter(r=>r.host==='sports.apholdings.kr'&&r.event==='courtmate_blog_arrival');
 // 머니 머지: 메인 도메인의 이벤트만, 없는 수치는 null(0으로 바꾸지 않음)
 const mmRows=raw.filter(r=>['www.apholdings.kr','apholdings.kr'].includes(r.host));
 const sumOf=names=>{const rows=mmRows.filter(r=>names.includes(r.event));return rows.length?rows.reduce((n,r)=>n+r.count,0):null};
 const moneyMerge={arrivals:{instagram:sumOf([MM_ARRIVALS.instagram]),tiktok:sumOf([MM_ARRIVALS.tiktok]),youtube:sumOf([MM_ARRIVALS.youtube]),share:sumOf([MM_ARRIVALS.share]),other:sumOf(MM_OTHER)}};
 for(const [k,ev] of Object.entries(MM_GAME)) moneyMerge[k]=sumOf([ev]);
 return {status:raw.length?'connected':'waiting_data',sites,blogArrivals:arrival.length?arrival.reduce((n,r)=>n+r.count,0):null,moneyMerge,daily:raw,period:{start:'28daysAgo',end:'today',timezone:'Asia/Seoul',todayPartial:true},thresholded:Boolean(report.metadata?.subjectToThresholding),sampled:Boolean(report.metadata?.samplingMetadatas?.length),source:'Google Analytics Data API',checkedAt:new Date().toISOString()};
}
export function parseServiceAccount(raw){
 try{let value=JSON.parse(raw);if(typeof value==='string')value=JSON.parse(value);if(value?.type!=='service_account'||typeof value.client_email!=='string'||typeof value.private_key!=='string')throw Error();return value;}catch{throw Error('credential_format');}
}

export function aggregateSummary(rows){
 const data=summarize({rows:rows.filter(r=>['page_view','courtmate_blog_arrival'].includes(r.event)).map(r=>({dimensionValues:[{value:r.host},{value:r.event},{value:r.day.replace(/-/g,'')}],metricValues:[{value:String(r.count)}]}))});const healthy=new Set(rows.filter(r=>r.event==='ap_install_test').map(r=>r.host));for(const site of data.sites)if(site.views==null&&healthy.has(site.host))site.views=0;if(data.blogArrivals==null&&healthy.has('sports.apholdings.kr'))data.blogArrivals=0;return {...data,source:'AP 일별 익명 집계',installedDate:'2026-10-29'};
}
