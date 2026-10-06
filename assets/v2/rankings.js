(() => {
'use strict';
const root=document.querySelector('[data-rankings]'); if(!root)return;
const ko=root.dataset.locale==='ko',cat=document.getElementById('rank-category'),period=document.getElementById('rank-period'),status=document.getElementById('rank-status'),rows=document.getElementById('rank-rows'),empty=document.getElementById('rank-empty'),refresh=document.getElementById('rank-refresh');
const motion=document.getElementById('rank-motion'),page=document.querySelector('.rankers-page');
if(motion&&page)motion.addEventListener('click',()=>{const paused=page.classList.toggle('motion-paused');motion.setAttribute('aria-pressed',String(paused));motion.textContent=ko?(paused?'효과 재생':'효과 멈추기'):(paused?'Play effects':'Pause effects');});
let controller;
const categories=new Set([...cat.options].map(o=>o.value));
const initial=new URL(location.href);if(categories.has(initial.searchParams.get('category')))cat.value=initial.searchParams.get('category');if(['week','all'].includes(initial.searchParams.get('period')))period.value=initial.searchParams.get('period');
async function load(){
if(controller)controller.abort();const current=controller=new AbortController();const timeout=setTimeout(()=>current.abort(),12000);
status.textContent=ko?'순위를 불러오는 중…':'Loading rankings…';rows.replaceChildren();empty.hidden=true;refresh.disabled=true;
document.getElementById('rank-caption').textContent=cat.selectedOptions[0].textContent+' · '+(ko?'공개 참여자 순위':'opted-in players');
const url=new URL(location.href);url.searchParams.set('category',cat.value);url.searchParams.set('period',period.value);history.replaceState(null,'',url);
try{
const res=await fetch('https://cxwdrlrqhxpnpepzrths.supabase.co/rest/v1/rpc/quiz_public_category_ranks',{method:'POST',headers:{'Content-Type':'application/json','apikey':"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4d2RybHJxaHhwbnBlcHpydGhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODkzMTgxNjUsImV4cCI6MjEwNDg5NDE2NX0.wRxgeJlHaMWiIgacOwGVMoSQ1gbpCxKZ8D6EBI8OL_8"},body:JSON.stringify({p_category:cat.value,p_period:period.value}),signal:current.signal});
if(!res.ok)throw Error('fetch');const data=await res.json();if(!Array.isArray(data.entries)||data.entries.length>50)throw Error('schema');
for(const entry of data.entries){if(!Number.isInteger(entry.rank)||typeof entry.alias!=='string'||!Number.isFinite(entry.points)||!Number.isFinite(Number(entry.accuracy)))throw Error('schema');}
for(const entry of data.entries){const tr=document.createElement('tr');for(const value of [entry.rank,entry.alias,entry.points.toLocaleString(ko?'ko-KR':'en-US'),Number(entry.accuracy).toFixed(1)+'%',entry.matches]){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}rows.append(tr);}
empty.hidden=data.entries.length>0;
const updated=new Date(data.updated_at);if(!Number.isFinite(updated.getTime()))throw Error('date');
status.textContent=(ko?'서버 집계 · 확인 시각 ':'Server totals · checked ')+updated.toLocaleString(ko?'ko-KR':'en-US',{timeZone:'Asia/Seoul'})+' KST';
}catch(error){if(current!==controller)return;rows.replaceChildren();empty.hidden=true;status.textContent=ko?'순위를 불러오지 못했습니다. 잠시 후 새로고침해 주세요.':'Could not load rankings. Please refresh in a moment.';}
finally{clearTimeout(timeout);if(current===controller)refresh.disabled=false;}
}
cat.addEventListener('change',load);period.addEventListener('change',load);refresh.addEventListener('click',load);load();
})();
