import{mailDraft,mailExample}from'./mail-admin-model.mjs';
const check=r=>{if(r.error)throw r.error;return r.data;};
export function createMailAdmin(root,client,isCurrent,{notify=()=>{}}={}){
 let epoch=0,state,pending;const $=s=>root.querySelector(s);
 function clear(){epoch++;state=null;pending=null;root.querySelector('dialog')?.close();root.replaceChildren();}
 async function load(){clear();const tick=epoch;if(!isCurrent())return;root.innerHTML=`
 <div class="section-heading"><div><p class="eyebrow">AP HOLDINGS · ADMIN</p><h2>하자증권 운영 관리</h2><p>기존 AP 관리자 전용입니다. 설정은 Apple·Android 앱에 함께 적용됩니다.</p></div></div>
 <nav class="guide-links"><a href="#mail-settings">자동메일 설정</a><a href="#admin-guide">관리자 사용 가이드</a><a href="#b2b-section">계정 신청·수정 요청</a><a href="#guide">사용자 가이드 보기</a></nav>
 <p data-status role="status" aria-live="polite">운영 설정을 불러오는 중입니다.</p>
 <article class="card" id="mail-settings"><h3>자동메일 날짜·수신자·문구</h3><p>종료일에서 몇 일 전부터 안내할지 정합니다. 기본은 60일이며 달력의 두 달과 날짜 수가 다를 수 있습니다.</p>
 <form data-settings hidden><div class="admin-fields">
 <label>종료일까지 남은 기준일수<input name="days" type="number" min="1" max="365" step="1" required inputmode="numeric"><small>예: 60 → 종료일까지 60일 이내인 유효·점검중 증권. 1~365일을 입력하세요.</small></label>
 <label>처리 방식<select name="mode"><option value="자동">자동 발송</option><option value="승인">승인 후 발송</option></select><small>자동: 평일 08시 서버가 처리합니다. 승인: 앱 발송함에 쌓인 메일을 확인하고 승인합니다.</small></label>
 <label>기본 수신 이메일<input name="recipient" type="email" multiple required maxlength="500" autocomplete="off"><small>여러 명은 쉼표로 구분합니다. 지정 수신자를 쓰면 업체·참조 주소를 자동으로 덧붙이지 않습니다.</small></label>
 <label>수신자 표시 이름<input name="name" maxlength="100" autocomplete="off"><small>{수신자}에 들어갈 이름입니다. 예: 김재윤 매니저</small></label></div>
 <label>메일 제목<input name="subject" required maxlength="300"></label>
 <label>메일 본문<textarea name="body" required maxlength="10000" rows="12"></textarea></label>
 <p class="quiet">{기준일수}는 설정한 날짜 수, {수신자}·{업체}·{공사}·{증권번호}·{금액}·{종료일}·{D}는 각 자료로 바뀝니다. {서명}은 실제 발송 시 채워집니다.</p>
 <div class="notice"><b>저장 전 꼭 확인해 주세요</b><p>변경은 이후 새로 생성하는 메일에 적용됩니다. 이미 대기 중이거나 발송된 메일은 자동으로 바뀌지 않습니다. 저장 버튼은 메일을 즉시 보내지 않습니다. 기존 발송 건은 반복 발송하지 않으며, 30일 추가 자동 안내와 미회신 재안내는 꺼진 상태로 유지합니다.</p></div>
 <p data-dirty class="quiet">현재 저장된 설정입니다.</p><div class="actions"><button class="button dark" type="submit">변경 내용 확인</button><button class="text-button" type="button" data-reload>저장된 설정 다시 불러오기</button></div>
 </form></article>
 <article class="card"><h3>최근 설정 변경 이력</h3><div data-history></div></article>
 <section id="admin-guide" class="admin-guide"><p class="eyebrow">ADMIN GUIDE</p><h2>관리자 사용 가이드</h2><p>처음 운영할 때는 아래 순서대로 한 단계씩 확인해 주세요. 실제 고객에게 시험 메일을 보내며 확인하지 않아도 됩니다.</p>
 <div class="cards admin-guide-shots"><figure class="card"><a href="/hajeung/screens/admin-mail-settings.png" target="_blank" rel="noopener"><img src="/hajeung/screens/admin-mail-settings.png" loading="lazy" alt="실제 관리자 설정 UI의 가상 예시: 날짜·수신자·문구 입력란"></a><figcaption>실제 관리자 UI · 가상 자료로 90일 변경 예시를 촬영했습니다. 운영 기본값은 60일이며 예시 이메일은 실제 수신자가 아닙니다. 누르면 확대됩니다.</figcaption></figure><figure class="card"><a href="/hajeung/screens/admin-mail-confirm.png" target="_blank" rel="noopener"><img src="/hajeung/screens/admin-mail-confirm.png" loading="lazy" alt="설정 저장 전 날짜 변경 요약과 가상 메일 미리보기"></a><figcaption>저장 전 확인 화면 · 운영 서버와 연결되지 않은 가상 검증 캡처입니다. 실제 발송 성공을 뜻하지 않습니다.</figcaption></figure></div><div class="cards"><article class="card"><h3>1. 한 번 로그인하고 관리자 화면 열기</h3><ol><li>이 페이지의 <b>로그인 · 신청과 문의</b>에서 기존 AP 관리자 이메일로 확인 링크를 요청합니다.</li><li>받은 메일의 링크를 같은 브라우저에서 엽니다. 로그인되면 이 운영 관리 화면이 나타납니다.</li><li>일반 고객은 자신의 신청·문의만 보며, 관리자 설정은 보이지 않습니다. 관리자 화면이 없으면 이메일과 기존 권한을 먼저 확인하세요.</li></ol></article>
 <article class="card"><h3>2. 자동메일 날짜 바꾸기</h3><ol><li>위 <b>종료일까지 남은 기준일수</b>에 숫자를 입력합니다. 예를 들어 60을 90으로 바꾸면 종료 90일 이내부터 안내 대상입니다.</li><li>제목·본문에는 <b>{기준일수}</b>를 넣어 주세요. 숫자가 자동 반영되므로 날짜를 바꿀 때 ‘2개월’ 같은 옛 문구가 남지 않습니다.</li><li>30일 안내를 별도로 켤 필요가 없습니다. 한 증권에 대해 기준 안내는 한 번만 생성합니다.</li></ol></article>
 <article class="card"><h3>3. 수신자와 문구 바꾸기</h3><ol><li>기본 수신 이메일을 확인합니다. 다른 담당자 주소로 바꾸려면 정확히 입력하고 이름도 함께 고칩니다.</li><li>제목·본문은 고객에게 보낼 말투로 작성합니다. {업체}처럼 중괄호로 된 변수 이름은 바꾸지 마세요.</li><li><b>변경 내용 확인</b>을 누르면 변경 전후와 가상 증권 예시가 나옵니다. 수신자·날짜·오탈자를 읽고 <b>확인하고 설정 저장</b>을 누릅니다.</li></ol></article>
 <article class="card"><h3>4. 저장 결과 확인하기</h3><ol><li>‘저장했습니다’ 안내와 다시 불러온 기준일수·수신자를 확인합니다.</li><li>아래 변경 이력에 시간·관리자·기준일수가 기록됩니다. 저장 실패를 완료로 해석하지 마세요.</li><li>동시에 다른 화면에서 변경했다는 안내가 나오면 새로고침하고 최신 값으로 다시 작성합니다.</li></ol><p>기존 대기 메일은 앱의 발송함에서 별도로 확인·수정합니다. 이미 보낸 메일은 수정할 수 없습니다.</p></article>
 <article class="card"><h3>5. 신청·수정 요청 처리하기</h3><ol><li>아래 <b>계정 신청·수정 요청</b>에서 회사·이름·요청 내용을 확인합니다.</li><li>계정 신청은 검토 후 승인합니다. 개인 앱 코드는 발급 버튼을 직접 눌렀을 때 한 번만 표시됩니다. 해당 담당자에게만 전달하고 화면을 닫습니다.</li><li>수정 요청은 접수→검토→작업→추가 정보 필요→완료 상태로 관리하고, 비공개 답변으로 처리 내용을 남깁니다.</li></ol><p>답변 저장 자체는 고객 이메일을 보내지 않습니다. 타인의 문서·사진·코드를 다른 고객에게 복사하지 마세요.</p></article>
 <article class="card"><h3>6. 발송·장애와 로그아웃</h3><ol><li>자동 모드의 메일은 앱을 닫아도 평일 08시에 서버가 처리합니다. 주말에는 다음 평일 작업을 기다려 주세요.</li><li>발송 결과는 앱의 발송함·메일 이력에서 성공/실패를 확인합니다. 발송 표시와 상대방 수신 확인은 다릅니다.</li><li>지난 증권은 자동 소급 발송하지 않습니다. 상세 화면에서 개별 미리보기 후 수동 발송합니다.</li><li>공용 기기에서는 페이지 상단의 로그아웃을 누릅니다. 앱 로그인 코드와 이 웹 이메일 확인 링크는 서로 다른 인증 수단입니다.</li></ol></article></div>
 </section><div id="b2b-section"></div>
 <dialog data-confirm aria-labelledby="mail-confirm-title"><h2 id="mail-confirm-title">운영 설정 변경을 확인해 주세요</h2><p>아래는 저장할 설정과 가상 자료로 만든 문구 예시입니다. 실제 메일은 발송하지 않습니다.</p><pre data-summary></pre><h3>메일 예시 · 가상 자료</h3><pre data-example></pre><div class="actions"><button type="button" class="button dark" data-save>확인하고 설정 저장</button><button type="button" class="text-button" data-cancel>돌아가서 수정</button></div><p data-dialog-status role="status"></p></dialog>`;
 const status=$('[data-status]'),form=$('[data-settings]'),dialog=$('[data-confirm]');
 const notice=(text,error=false)=>{status.textContent=text;status.classList.toggle('error',error);};
 const paint=x=>{state=x;for(const key of ['days','mode','recipient','name','subject','body'])form.elements[key].value=x[key]??'';form.hidden=false;$('[data-dirty]').textContent='현재 저장된 설정입니다.';const history=$('[data-history]');history.replaceChildren();if(!x.history?.length)history.textContent='이 웹 화면에서 저장한 변경 이력이 아직 없습니다.';for(const row of x.history||[]){const p=document.createElement('p');p.textContent=`${new Date(row.at).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})} · ${row.actor} · ${row.days}일 · ${row.mode}`;history.append(p);}};
 try{const x=check(await client.rpc('hajeung_web_settings'));if(tick!==epoch||!isCurrent())return;paint(x);notice('운영 설정을 불러왔습니다.');}catch(e){if(tick===epoch&&isCurrent())notice(e.message||'설정을 불러오지 못했습니다.',true);}
 form.oninput=()=>{$('[data-dirty]').textContent='아직 저장하지 않은 변경이 있습니다.';};
 form.onsubmit=e=>{e.preventDefault();try{pending=mailDraft({...Object.fromEntries(new FormData(form)),revision:state.revision});const ex=mailExample(pending);$('[data-summary]').textContent=`발송 기준: ${state.days}일 → ${pending.days}일\n처리 방식: ${state.mode} → ${pending.mode}\n수신자: ${state.recipient} → ${pending.recipient}\n표시 이름: ${pending.name||'담당자'}\n적용: 이후 새로 생성하는 메일만`;$('[data-example]').textContent=`제목: ${ex.subject}\n\n${ex.body}`;$('[data-dialog-status]').textContent='';dialog.showModal();}catch(e){notice(e.message,true);}};
 $('[data-cancel]').onclick=()=>{pending=null;dialog.close();};
 $('[data-reload]').onclick=async e=>{if($('[data-dirty]').textContent.includes('아직')&&!window.confirm('저장하지 않은 변경을 버리고 다시 불러올까요?'))return;if(!isCurrent()||e.target.disabled)return;e.target.disabled=true;try{const x=check(await client.rpc('hajeung_web_settings'));if(tick!==epoch||!isCurrent())return;paint(x);notice('저장된 운영 설정을 다시 불러왔습니다.');notify('저장된 운영 설정을 다시 불러왔습니다.');}catch(error){if(tick===epoch&&isCurrent()){notice(error.message||'설정을 불러오지 못했습니다.',true);notify(error.message||'설정을 불러오지 못했습니다.',true);}}finally{e.target.disabled=false;}};
 $('[data-save]').onclick=async e=>{if(!pending||!isCurrent()||e.target.disabled)return;e.target.disabled=true;try{const x=check(await client.rpc('hajeung_web_save',{p:pending}));if(tick!==epoch||!isCurrent())return;pending=null;dialog.close();paint(x);notice('저장했습니다. 서버에서 다시 불러온 설정입니다. Apple·Android에 함께 적용됩니다.');notify('운영 설정을 저장했습니다. Apple·Android에 함께 적용되며, 이후 새로 생성되는 메일부터 사용합니다.');}catch(error){if(tick===epoch&&isCurrent())$('[data-dialog-status]').textContent=error.message||'저장하지 못했습니다. 다시 확인해 주세요.';}finally{e.target.disabled=false;}};
 }
 return{load,clear};
}
