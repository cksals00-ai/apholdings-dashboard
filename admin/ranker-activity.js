const names={quiz:'퀴즈랭커',hotel:'호텔랭커',invest:'투자랭커'};
let timer=null,controller=null,generation=0;
export function stopRankerActivity(){generation++;clearInterval(timer);timer=null;controller?.abort();document.getElementById('ranker-activity')?.remove();}
export function refreshRankerActivity(sb){
 clearInterval(timer);const version=++generation;
 let root=document.getElementById('ranker-activity');
 if(!root){root=document.createElement('section');root.id='ranker-activity';root.className='panel';document.getElementById('app-message')?.before(root);}
 const number=v=>Number(v||0).toLocaleString('ko-KR');
 async function update(){
  if(document.hidden)return;
  controller?.abort();controller=new AbortController();
  try{const {data:{session}}=await sb.auth.getSession();if(!session){stopRankerActivity();return;}
   const r=await fetch('https://cgijpcimixaregbpvqbf.supabase.co/functions/v1/rankers-activity',{headers:{Authorization:'Bearer '+session.access_token},signal:controller.signal});
   if(!r.ok)throw new Error('unavailable');const d=await r.json();if(version!==generation)return;
   root.replaceChildren();const h=document.createElement('h2');h.textContent='RANKERS 접속 현황';root.append(h);
   const grid=document.createElement('div');grid.className='app-grid';
   for(const a of d.apps){const card=document.createElement('article');card.className='app-card';const heading=document.createElement('h3');heading.textContent=names[a.app]||a.app;card.append(heading);
    for(const [label,value]of [['현재 접속 · 최근 5분',a.current],['누적 로그인 이용자',a.accounts],['누적 체험 기기',a.guest_devices],['누적 접속 횟수',a.visits]]){const row=document.createElement('p');row.textContent=label+'  '+number(value);card.append(row);}
    for(const p of a.platforms){const row=document.createElement('small');row.style.display='block';row.textContent=p.platform.toUpperCase()+' · 현재 '+number(p.current)+' · 누적 '+number(p.cumulative);card.append(row);}grid.append(card);
   }root.append(grid);const note=document.createElement('p');note.className='muted';note.textContent=(d.collection_enabled===false?'새 접속 수집은 개인정보 안내 공개 승인 대기 중입니다. ':'')+'30초마다 갱신 · 같은 로그인 계정은 앱·웹 중복 제거. 체험은 기기 기준이며 로그인 이용자와 중복될 수 있습니다. 30분 이상 간격을 두고 돌아오면 새 접속으로 계산합니다. '+(d.since?'집계 시작: '+new Date(d.since).toLocaleString('ko-KR'):'아직 수집된 기록이 없습니다.')+' · 최신 갱신: '+new Date(d.checked_at).toLocaleString('ko-KR')+' · 새 집계 기능이 적용된 버전만 포함하며, 이전 기록은 소급하지 않습니다.';root.append(note);
  }catch(e){if(e.name!=='AbortError'&&version===generation)root.textContent='RANKERS 접속 현황을 불러오지 못했습니다. 잠시 후 다시 시도합니다.';}
 }update();timer=setInterval(update,30000);
}
