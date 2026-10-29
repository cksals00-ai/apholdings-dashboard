export const HOSTS=['www.apholdings.kr','apholdings.kr','edu.apholdings.kr','games.apholdings.kr','ent.apholdings.kr','shop.apholdings.kr','sports.apholdings.kr'];
export const ownerAllowed=user=>Boolean(user?.email_confirmed_at && user?.email?.toLowerCase()==='cksals00@gmail.com');
export const reportRequest=()=>({dateRanges:[{startDate:'28daysAgo',endDate:'today'}],dimensions:[{name:'hostName'},{name:'eventName'},{name:'date'}],metrics:[{name:'eventCount'}],dimensionFilter:{andGroup:{expressions:[{filter:{fieldName:'hostName',inListFilter:{values:HOSTS}}},{filter:{fieldName:'eventName',inListFilter:{values:['page_view','courtmate_blog_arrival']}}}]}},limit:10000,keepEmptyRows:false});
export function summarize(report){
 const raw=(report.rows||[]).map(r=>({host:r.dimensionValues?.[0]?.value,event:r.dimensionValues?.[1]?.value,day:r.dimensionValues?.[2]?.value,count:Number(r.metricValues?.[0]?.value)})).filter(r=>HOSTS.includes(r.host)&&Number.isFinite(r.count)&&r.count>=0);
 const sites=HOSTS.filter(h=>h!=='apholdings.kr').map(host=>{const rows=raw.filter(r=>r.event==='page_view'&&(r.host===host||(host==='www.apholdings.kr'&&r.host==='apholdings.kr')));return {host,views:rows.length?rows.reduce((n,r)=>n+r.count,0):null}});
 const arrival=raw.filter(r=>r.host==='sports.apholdings.kr'&&r.event==='courtmate_blog_arrival');
 return {status:raw.length?'connected':'waiting_data',sites,blogArrivals:arrival.length?arrival.reduce((n,r)=>n+r.count,0):null,daily:raw,period:{start:'28daysAgo',end:'today',timezone:'Asia/Seoul',todayPartial:true},thresholded:Boolean(report.metadata?.subjectToThresholding),sampled:Boolean(report.metadata?.samplingMetadatas?.length),source:'Google Analytics Data API',checkedAt:new Date().toISOString()};
}
