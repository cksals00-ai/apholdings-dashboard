import { calculatePlan, MODEL_VERSION } from './business-plan-model.mjs?v=1.0.0';

const esc = (v='') => String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num = (v,d=0) => Number(v).toLocaleString('ko-KR',{maximumFractionDigits:d,minimumFractionDigits:d});
const money = v => Math.abs(v)>=1e8 ? `${num(v/1e8,1)}억원` : `${num(v/1e4,Math.abs(v)<1e5?1:0)}만원`;
const million = v => num(v/1e6,1);
const pct = v => `${num(v*100,1)}%`;
const range = (lo,hi) => `${money(lo)} – ${money(hi)}`;
const url = v => {try {const u=new URL(v);return u.protocol==='https:'?u.href:'#';}catch{return '#';}};
const card = (label,value,note,tone='') => `<article class="bp-kpi ${tone}"><span>${esc(label)}</span><strong>${esc(value)}</strong><p>${esc(note)}</p></article>`;
const box = (title,content,sub='') => `<section class="bp-panel"><header><h2>${esc(title)}</h2>${sub?`<p>${esc(sub)}</p>`:''}</header>${content}</section>`;

// Use the existing admin's native DOM bar pattern. Signed values share one scale;
// labels and the accompanying table preserve exact values without color reliance.
function bars(rows, series, title, subtitle) {
  const values=rows.flatMap(row=>series.map(s=>row[s.key]));
  const min=Math.min(0,...values), max=Math.max(1,...values), span=max-min, zero=-min/span*100;
  const legend=series.map((s,i)=>`<span><i class="bp-swatch bp-s${i}"></i>${esc(s.label)}</span>`).join('');
  const marks=rows.map(row=>`<div class="bp-bar-group"><b>${esc(row.label??row.year)}</b><div>${series.map((s,i)=>{
    const value=row[s.key], left=(Math.min(0,value)-min)/span*100, width=Math.abs(value)/span*100;
    return `<div class="bp-bar-row"><span class="bp-series-name">${esc(s.label)}</span><div class="bp-track" aria-hidden="true"><i class="bp-zero" style="left:${zero}%"></i><i class="bp-mark bp-s${i}" style="left:${left}%;width:${width}%"></i></div><span class="bp-bar-value">${million(value)}</span></div>`;
  }).join('')}</div></div>`).join('');
  return box(title,`<div class="bp-legend">${legend}<span>백만원 · 0 기준 공통 축</span></div><div class="bp-bars" role="img" aria-label="${esc(title)}. ${esc(rows.map(r=>`${r.label??r.year}: ${series.map(s=>`${s.label} ${million(r[s.key])}백만원`).join(', ')}`).join('; '))}">${marks}</div>`,subtitle);
}

function financialTable(rows, specs, label='연간 손익·현금흐름') {
  return `<div class="bp-table-wrap" tabindex="0" role="region" aria-label="${esc(label)}"><table class="bp-table"><caption>${esc(label)} · 백만원, 소수점 반올림</caption><thead><tr><th scope="col">항목</th>${rows.map(r=>`<th scope="col">${esc(r.label??r.year)}</th>`).join('')}</tr></thead><tbody>${specs.map(([title,key,major])=>`<tr class="${major?'bp-total':''}"><th scope="row">${esc(title)}</th>${rows.map(r=>`<td class="${r[key]<0?'bp-negative':''}">${million(r[key])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}

export function createBusinessPlan(supabase,getUser) {
  const root=document.getElementById('plan-section');
  let payload=null, scenario='base', tab='october', generation=0, loading=false;
  const tabs=[['october','10월 실행'],['finance','5년 손익·현금'],['value','기업가치'],['evidence','근거·가정']];

  function render() {
    if (!payload || !getUser()) return;
    const model=calculatePlan(payload,scenario), annual=model.years.filter(y=>y.months===12), selected=payload.scenarios[scenario];
    root.innerHTML=`<div class="bp-shell">
      <div class="bp-heading"><div><p class="eyebrow">BUSINESS PLAN · OWNER ONLY</p><h2>${esc(payload.title)}</h2><p>${esc(payload.summary)}</p></div><button type="button" class="secondary" data-bp="refresh">다시 불러오기</button></div>
      <div class="bp-toolbar"><div class="bp-scenarios" role="group" aria-label="계획 시나리오">${Object.entries(payload.scenarios).map(([key,s])=>`<button type="button" data-bp-scenario="${esc(key)}" aria-pressed="${key===scenario}">${esc(s.label)}</button>`).join('')}</div><span class="bp-caption">검토 기준 ${esc(payload.asOf)} · 모든 미래 수치는 가정</span></div>
      <p class="bp-scenario-note" role="status">${esc(selected.label)}안 · ${esc(selected.description)}</p>
      <nav class="bp-tabs" aria-label="사업계획 보기">${tabs.map(([key,label])=>`<button type="button" data-bp-tab="${key}" aria-current="${key===tab?'page':'false'}">${label}</button>`).join('')}</nav>
      <div class="bp-content">${tab==='october'?october(model):tab==='finance'?finance(model,annual):tab==='value'?valuation(model,annual):evidence(model)}</div>
      <footer class="bp-footer"><span>실제 실적과 계획 가정 분리 · ${esc(payload.version)} · 계산 ${MODEL_VERSION}</span><button class="secondary" type="button" data-bp="csv">월별 계산 CSV</button><button class="secondary" type="button" data-bp="json">가정·근거 JSON</button></footer>
    </div>`;
  }

  function october(model) {
    const oct=model.months[0], stage=payload.scenarios[scenario].stages[0], a=payload.actuals;
    const q4=model.months.filter(m=>m.year===oct.year);
    const q4Liquidity=payload.assumptions.cashBuffer-Math.min(0,...q4.map(m=>m.cumulativeCash));
    return `<div class="bp-factline"><b>현재 확인된 실적</b><span>앱 수익금 ${num(a.appProceedsKRW)}원</span><span>다운로드 ${num(a.downloads)}건</span><span>IAP ${num(a.iapUnits)}건</span><small>${esc(a.appMetricFrom)}~${esc(a.appMetricTo)} 수집 보고서 · 수익금은 입금액이 아니며 일부 본인 구매 가능</small></div>
      <div class="bp-kpis">${card('10월 매출 목표',money(oct.revenue),'미계약 목표 · 부가세 제외 · 환불 차감')}${card('10월 입금 목표',money(oct.cashReceipts),'서비스 대금 50% 회수 · 앱 정산 미포함','bp-emphasis')}${card('10월 순현금증감',money(oct.freeCashFlow),`대표 보수·비용·장비 반영 / 영업이익 ${money(oct.operatingProfit)}`,oct.freeCashFlow<0?'bp-warning':'')}</div>
      <div class="bp-callout"><b>매출보다 먼저 볼 것: 운영자금</b><p>10~12월 계획에 필요한 시작 유동성은 ${money(q4Liquidity)}입니다(안전 현금 ${money(payload.assumptions.cashBuffer)} 포함). 회사 통장 잔액이 미확인이라 추가 조달액은 아직 정할 수 없습니다.</p></div>
      <div class="bp-offers">${payload.offers.map((offer,i)=>{
        const qty=i===0?stage.projectsPerMonth:i===1?stage.contentPerMonth:stage.paidOrdersPerMonth;
        return `<article class="bp-offer"><p class="eyebrow">${esc(offer.priority)}</p><h3>${esc(offer.title)}</h3><div class="bp-offer-number">${i===2?'평균 ':''}${money(offer.unitPrice)} <span>× ${num(qty)}${i===2?'건':'개 고객'}</span></div><p>${esc(offer.buyer)}</p><p class="bp-deliverable">${esc(offer.deliverable)}</p><details><summary>판매 조건·중단 기준</summary><p><b>판매 전</b> ${esc(offer.gate)}</p><p><b>실행</b> ${esc(offer.next)} (접촉·계약 수는 기준안)</p><p><b>중단</b> ${esc(offer.stop)}</p><p><b>다음</b> ${esc(offer.after)}</p></details></article>`;
      }).join('')}</div>
      ${box('10월에는 이 네 가지만',`<ol class="bp-roadmap">${payload.roadmap.map(r=>`<li><time>${esc(r.date)}</time><div><h3>${esc(r.title)}</h3><p>${esc(r.action)}</p><small>${esc(r.owner)}</small></div></li>`).join('')}</ol>`)}
      <div class="bp-callout bp-muted"><b>AI가 맡을 수 있는 일</b><p>샘플·표준 리포트·제품 개선·테스트·손익 대사까지 지원합니다. 고객의 구매, 계약 체결, 자금 조달과 매출 성장은 보장할 수 없습니다. 본업의 고객·데이터·권한은 전용하지 않습니다.</p></div>`;
  }

  function finance(model,annual) {
    const last=annual.at(-1);
    const summarySpecs=[['매출','revenue',true],['영업이익','operatingProfit',true],['계획 세후이익','netProfit'],['영업현금흐름','operatingCashFlow'],['설비 지출','capex'],['순현금증감','freeCashFlow',true],['누적 현금증감','cumulativeCash',true]];
    const detailed=[['반복 구독','recurringRevenue'],['표준 파일럿','projectRevenue'],['콘텐츠 제작','contentRevenue'],['앱 결제(환불 차감)','appRevenue'],['총매출','revenue',true],['직접원가·사용량 비용','deliveryCosts'],['앱 플랫폼 수수료','platformFees'],['대표·팀 인건비','payroll'],['서버·AI·관리비','overhead'],['마케팅','marketing'],['EBITDA','ebitda'],['감가상각','depreciation'],['영업이익','operatingProfit',true],['세금 적립 가정','taxReserve'],['계획 세후이익','netProfit',true],['실제 회수 가정','cashReceipts'],['현금 운영비','cashCosts'],['영업현금흐름','operatingCashFlow',true],['설비 지출','capex'],['순현금증감','freeCashFlow',true],['기말 미수금·정산대기','receivables']];
    return `<div class="bp-kpis">${card(`${last.year} 매출 목표`,money(last.revenue),`연말 유료 고객 ${num(last.clients)}개 · 앱 월 이용자 ${num(last.requiredMAU)}명 필요`)}${card(`${last.year} 영업이익`,money(last.operatingProfit),'대표 대체 보수·직원·외주 비용 포함')}${card('계획 시작 유동성',money(model.totalOpeningLiquidityRequired),'전체 기간 최저 누적현금 + 안전 현금. 실제 보유 현금 차감 전.','bp-emphasis')}</div>
      <div class="bp-chart-grid">${bars(annual,[{key:'revenue',label:'매출'},{key:'operatingProfit',label:'영업이익'}],'성장보다 이익이 남는지',`${annual[0].year}–${last.year} · ${payload.scenarios[scenario].label}안 · 모두 계획`)}${bars(annual,[{key:'cumulativeCash',label:'누적 현금증감'}],'성장에 필요한 현금',`계획 시작부터 각 연말까지 · 통장 잔액 아님 · 기존 현금·채무 미반영`)}</div>
      ${box('5년 핵심 숫자',financialTable(annual,summarySpecs))}
      <details class="bp-panel"><summary>매출 구성·전체 손익·현금 대사</summary>${financialTable(annual,detailed,'5년 상세 모델')}<p class="bp-caption">영업현금 = 계획 세후이익 + 감가상각 − 미수금 증가. 순현금 = 영업현금 − 설비 지출. 반올림 전 최대 대사 차이 ${num(model.maxReconciliationError,6)}원.</p></details>
      <details class="bp-panel"><summary>올해 10~12월 연결 계획</summary>${financialTable(model.months.filter(m=>m.year===model.months[0].year).map(m=>({...m,label:`${m.month}월`})),summarySpecs,'2026년 4분기 · 연간 합계가 아님')}</details>
      ${box('숫자를 만들기 위한 조건',`<div class="bp-table-wrap" tabindex="0" role="region" aria-label="매출 동인"><table class="bp-table"><caption>고객·전환·인력 가정 · 예상 환산 수량</caption><thead><tr><th>동인</th>${annual.map(y=>`<th>${y.year}</th>`).join('')}</tr></thead><tbody>${[
        ['연말 유료 고객',y=>num(y.clients)],['연평균 유료 고객',y=>num(y.averageClients,1)],['매월 신규 계약 필요',y=>num(y.newClients/12,1)],['매월 적합 고객 접촉 필요',y=>num(Math.ceil(y.requiredProspects/12))],['앱 월 결제 건수',y=>num(y.paidOrders/12)],['앱 월 이용자 필요',y=>num(y.requiredMAU)],['대표 외 인력(명 환산)',y=>num(payload.scenarios[scenario].stages.find(s=>s.year===y.year).staffFte,2)]
      ].map(([label,fn])=>`<tr><th scope="row">${label}</th>${annual.map(y=>`<td>${fn(y)}</td>`).join('')}</tr>`).join('')}</tbody></table></div><p class="bp-caption">월 해지율 ${pct(payload.scenarios[scenario].monthlyChurn)}, 적합 고객→계약 ${pct(payload.scenarios[scenario].prospectCloseRate)}, 앱 월 유료 전환 ${pct(payload.assumptions.paidConversionRate)} 가정. 접촉 필요량은 반복 구독만 계산하며 파일럿·제작 영업은 별도. 현재 앱 MAU는 미확인입니다.</p>`)}
      ${model.months.some(m=>m.capacityGap>0)?'<div class="bp-callout bp-warning"><b>인력 계획 부족</b><p>일부 월의 납품 필요 시간이 투입 가능 시간을 초과합니다. 해당 목표는 인력 조정 전 실행 불가입니다.</p></div>':''}
      ${box('연도마다 통과해야 할 문턱',`<div class="bp-gates">${payload.yearGates.map(g=>`<article><b>${g.year}</b><h3>${esc(g.title)}</h3><p>${esc(g.text)}</p></article>`).join('')}</div>`,'기준안 실행 기준 · 보수·도전안은 같은 통제 아래 규모 조정')}
      <p class="bp-caption">현재 잔액·기존 채무·기존 고정비 확인 전의 신규 사업 범위 모델입니다. 대출·투자금·보조금·주식 매매손익은 제외했습니다.</p>`;
  }

  function valuation(model,annual) {
    const current=payload.currentValue, last=annual.at(-1);
    const all=Object.entries(payload.scenarios).map(([key,s])=>({label:s.label,...calculatePlan(payload,key)}));
    return `<div class="bp-kpis">${card('현재 사업가치 가설',range(current.indicativeLow,current.indicativeHigh),'권리·양도·회수 가능성 검증 전. 확정 평가액 아님.','bp-warning')}${card(`${last.year} 기업가치 목표`,range(model.valuationLow,model.valuationHigh),`${payload.scenarios[scenario].label}안 달성 시 · 해당 연도 말 가치`,'bp-emphasis')}${card('현재 지분가치','산정 유보','회사 현금·부채·소유권 자료가 필요합니다.')}</div>
      ${box('지금은 자산, 앞으로는 반복 이익',`<p class="bp-body">${esc(current.explanation)}</p><div class="bp-value-formula"><span>미래 영업이익<br><b>${money(last.operatingProfit)}</b></span><span aria-hidden="true">×</span><span>내부 가정 배수<br><b>${num(payload.assumptions.valuationMultipleLow)}–${num(payload.assumptions.valuationMultipleHigh)}배</b></span><span aria-hidden="true">=</span><span>${last.year} 사업가치<br><b>${range(model.valuationLow,model.valuationHigh)}</b></span></div><p class="bp-caption">현재 재구축 자산가치와 미래 이익가치는 합산하지 않습니다. 미래 가치는 현재가치로 할인한 가격이 아닙니다. 초기기업의 실제 매각가는 0원이 될 수도 있습니다.</p>`)}
      ${box('5개년 기업가치 경로',`<div class="bp-table-wrap" tabindex="0" role="region" aria-label="연도별 기업가치"><table class="bp-table"><caption>${esc(payload.scenarios[scenario].label)}안 · 영업이익 0 이하이면 이익가치 0</caption><thead><tr><th>연도</th><th>영업이익</th><th>사업가치 가정 범위</th></tr></thead><tbody>${annual.map(y=>`<tr><th scope="row">${y.year}</th><td>${money(y.operatingProfit)}</td><td>${range(Math.max(0,y.operatingProfit)*payload.assumptions.valuationMultipleLow,Math.max(0,y.operatingProfit)*payload.assumptions.valuationMultipleHigh)}</td></tr>`).join('')}</tbody></table></div>`)}
      ${box(`${last.year} 세 가지 결과`, `<div class="bp-sensitivity">${all.map(m=>`<article><span>${esc(m.label)}안</span><strong>${range(m.valuationLow,m.valuationHigh)}</strong><p>매출 ${money(m.years.at(-1).revenue)} · 유료 고객 ${num(m.years.at(-1).clients)}개</p></article>`).join('')}</div><p class="bp-caption">범위는 성공 확률이나 신뢰구간이 아닙니다. 앱 유입·고객 유지·가격·인력 가정 변화가 결과를 크게 바꿉니다. 계약과 입금으로 매월 다시 평가해야 합니다.</p>`)}
      <div class="bp-callout"><b>가치를 높이는 순서</b><p>외부 유료 고객 → 실제 갱신 → 대표 없이 납품 가능한 운영 → 양도 가능한 IP·계약과 회계 증빙. AI 기능이나 공공 데이터 양만으로 기업가치가 생기지는 않습니다.</p></div>`;
  }

  function evidence(model) {
    const p=payload.assumptions;
    return `${box('무엇을 확인했고, 무엇이 아직 없는가',`<div class="bp-audit">${payload.audit.map(a=>`<details><summary><span>${esc(a.area)}</span><em>${esc(a.status)}</em></summary><p><b>확인</b> ${esc(a.evidence)}</p><p><b>판단</b> ${esc(a.decision)}</p><small>출처: ${esc(a.source)}</small></details>`).join('')}</div>`)}
      ${box('아직 입력하지 않은 실제 숫자',`<ul class="bp-list">${payload.missing.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><p class="bp-caption">빈 값을 0원 실적으로 표시하지 않습니다. 확인되면 비공개 계획 데이터를 수정해야 하며, 현재 수치는 실시간 자동 실적 갱신이 아닌 검토일 스냅샷입니다.</p>`)}
      ${box('계산에 사용한 가정',`<div class="bp-assumptions">${[['구독 직접원가',pct(p.recurringCostRate)],['파일럿 직접원가',pct(p.projectCostRate)],['콘텐츠 직접원가',pct(p.contentCostRate)],['앱 사용량 비용',pct(p.appCostRate)],['앱 플랫폼 가정',pct(p.platformFeeRate)],['앱 환불 가정',pct(p.refundRate)],['세금 적립 가정',pct(p.taxReserveRate)],['서비스 당월 회수',pct(p.serviceSameMonthReceipt)],['앱 정산 지연',`${p.appSettlementMonths}개월`],['안전 현금',money(p.cashBuffer)]].map(([k,v])=>`<div><span>${k}</span><b>${v}</b></div>`).join('')}</div><details><summary>전체 원칙·회계 범위</summary><ol class="bp-list">${payload.rules.map(r=>`<li>${esc(r)}</li>`).join('')}</ol></details><details><summary>인건비·단가·광고비 연도별 입력</summary><div class="bp-table-wrap" tabindex="0" role="region" aria-label="원시 가정"><table class="bp-table"><caption>모두 계획 가정 · 백만원, 인력은 FTE 환산</caption><thead><tr><th>기간</th><th>월 구독 단가</th><th>파일럿/월</th><th>단가</th><th>제작/월</th><th>단가</th><th>대표/월</th><th>인력</th><th>1인 연 총원가</th><th>운영/월</th><th>광고/월</th></tr></thead><tbody>${payload.scenarios[scenario].stages.map(s=>`<tr><th>${s.year}${s.months<12?'.'+s.startMonth:''}</th>${[s.arpu/1e6,s.projectsPerMonth,s.projectPrice/1e6,s.contentPerMonth,s.contentPrice/1e6,s.founderPayMonthly/1e6,s.staffFte,s.loadedStaffAnnual/1e6,s.overheadMonthly/1e6,s.marketingMonthly/1e6].map(v=>`<td>${num(v,2)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></details>`)}
      ${box('근거와 한계',`<ul class="bp-sources">${payload.sources.map(s=>`<li><a href="${esc(url(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><p>${esc(s.detail)}</p></li>`).join('')}</ul><details><summary>실적 집계 주의점</summary>${payload.actuals.notes.map(n=>`<p>${esc(n)}</p>`).join('')}<p>광고: ${esc(payload.actuals.adsFrom)}~${esc(payload.actuals.adsTo)}, $${num(payload.actuals.adsSpendUSD,2)} / 귀속 설치 ${payload.actuals.adsInstalls}건. 유료 전환·회수기간 검증 전 확대 근거가 아닙니다.</p></details>`)}
      <p class="bp-caption">계산 검증: ${model.months.length}개월 · 손익–현금 대사 통과 ${model.maxReconciliationError<.01?'✓':'실패 — 사용 중지'}. 사업·가치평가 가정의 타당성을 보증하는 검사는 아닙니다.</p>`;
  }

  function download(kind) {
    if (!payload || !getUser()) return;
    const model=calculatePlan(payload,scenario);
    const keys=['period','revenue','operatingProfit','netProfit','cashReceipts','cashCosts','taxReserve','operatingCashFlow','capex','freeCashFlow','cumulativeCash','receivables','clients','newClients','requiredProspects','requiredMAU','requiredHours','capacityHours'];
    const content=kind==='json'?JSON.stringify(payload,null,2):'\uFEFF'+[keys.join(','),...model.months.map(m=>keys.map(k=>typeof m[k]==='number'?m[k].toFixed(4):m[k]).join(','))].join('\r\n');
    const objectUrl=URL.createObjectURL(new Blob([content],{type:kind==='json'?'application/json':'text/csv;charset=utf-8'}));
    const a=document.createElement('a');a.href=objectUrl;a.download=`ap-business-plan-${scenario}.${kind}`;a.click();setTimeout(()=>URL.revokeObjectURL(objectUrl),1000);
  }
  root.addEventListener('click',event=>{
    const target=event.target.closest('button');if(!target)return;
    const focusKey=target.dataset.bpScenario?`[data-bp-scenario="${target.dataset.bpScenario}"]`:target.dataset.bpTab?`[data-bp-tab="${target.dataset.bpTab}"]`:null;
    if(target.dataset.bpScenario && payload?.scenarios[target.dataset.bpScenario]){scenario=target.dataset.bpScenario;render();}
    if(target.dataset.bpTab && tabs.some(([k])=>k===target.dataset.bpTab)){tab=target.dataset.bpTab;render();}
    if(target.dataset.bp==='refresh')load(true);
    if(['csv','json'].includes(target.dataset.bp))download(target.dataset.bp);
    if(focusKey)root.querySelector(focusKey)?.focus({preventScroll:true});
  });
  async function load(force=false) {
    if(!getUser()||loading)return;
    if(payload&&!force){render();return;}
    const token=++generation;loading=true;
    root.innerHTML='<p class="bp-loading" role="status">비공개 사업계획을 불러오는 중…</p>';
    try {
      const {data,error}=await supabase.from('admin_business_plans').select('payload,updated_at').eq('id','2026-10-five-year').maybeSingle();
      if(token!==generation||!getUser())return;
      if(error||!data?.payload)throw new Error('Unavailable');
      // Validate every scenario before promoting the snapshot to the UI.
      for(const key of Object.keys(data.payload.scenarios)){const m=calculatePlan(data.payload,key);if(m.maxReconciliationError>.01)throw new Error('Reconciliation failed');}
      payload=data.payload;render();
    }catch{
      if(token===generation&&getUser())root.innerHTML='<div class="bp-callout" role="alert"><b>사업계획을 불러오지 못했습니다.</b><p>관리자 권한·연결·계획 데이터 상태를 확인해 주세요. 가짜 숫자로 대체하지 않습니다.</p><button class="secondary" data-bp="refresh" type="button">다시 시도</button></div>';
    }finally{if(token===generation)loading=false;}
  }
  function clear(){generation++;payload=null;loading=false;scenario='base';tab='october';root.replaceChildren();}
  return {load,clear};
}
