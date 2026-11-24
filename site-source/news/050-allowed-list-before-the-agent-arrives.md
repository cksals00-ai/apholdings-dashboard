---
no: 50
slug: allowed-list-before-the-agent-arrives
date: 2026-11-17
category: 인사이트
tags: 에이전트 · Poppy · 쇼피파이 · 메타 Muse · 우버 · 에이전트 보안 · 애플 · 건강 AI · OpenEvidence · 커머스
title: 「해도 되는 일」을 에이전트가 오기 전에 적어 두는 세 문서 — 쇼피파이 전 매장은 11월 13일부터 /.well-known/poppy.json 한 장으로 「우리 가게에서 에이전트가 할 수 있는 일」을 자동 게시하고, 우버는 자기 에이전트 하나하나에 「허용 의도·제약·위험 등급」을 등록한 뒤에만 돌리고, 애플은 건강 AI 답변에 「임상 인용·우려 질문 감지·학습 미사용」을 붙여 20만 명에게 평가를 맡겼다
summary: 시에라와 메타가 만든 개인 에이전트 규격 「Poppy」 1.0이 11월 13일 나왔습니다. 회사가 자기 도메인의 /.well-known/poppy.json 한 파일에 「우리는 누구고, 에이전트가 어느 길로 들어와 무엇을 해도 되는지」를 적어 두면 손님의 에이전트가 그것을 먼저 읽는 방식이고, 쇼피파이는 모든 매장에 이 파일을 자동으로 게시하기 시작했고 메타의 Muse는 모든 사이트에서 이 파일을 먼저 찾습니다(회사 발표). 우버는 11월 6일 엔지니어링 블로그에 「신원 확인은 「누가」만 답하고 「이 행동이 맥락에 맞나」는 못 답한다」며 에이전트마다 신원·소유자·허용 의도·제약·위험 등급을 등록하고 실행 순간 검문하는 구조를 적었습니다(수치 없음). 애플은 11월 15일 OpenEvidence와 함께 「건강 AI 사용 연구」 앱을 열어 미국 21세 이상 최대 20만 명이 임상 출처가 붙은 답을 받고 평가하게 했고, 「연구 데이터는 AI 학습에 쓰지 않는다」「우려되는 질문은 감지해 의료진으로 안내한다」고 적었습니다. 셋을 「행동이 일어나기 전에 허용 범위를 문서로 적는 방식」으로 묶었습니다.
---
> 이 글은 AI(Claude)와 함께 작성했고 편집자가 검수했습니다. 우리 회사는 앤트로픽과 OpenAI 두 회사의 유료 고객이고 구글 모델도 시험에 씁니다. 1번의 Poppy는 앤트로픽이 처음 만든 규격 MCP 위에 얹혀 있어 그 점을 밝힙니다. **우리는 커머스·앱·AI 인플루언서를 직접 운영하므로 세 소식 모두에서 「문서를 써야 하는 쪽」에 서 있습니다** — 그래서 어느 회사의 방식에도 평가를 보태지 않고 문서에 적힌 것과 적히지 않은 것만 옮겼습니다. 회사가 발표한 수치는 「회사가 발표한 것」으로 표시했고, 출처가 한 곳뿐인 내용은 그 출처를 함께 적었습니다. 3번의 건강 관련 서술은 의료 조언이 아닙니다. 이 글은 특정 기업에 대한 투자 의견이 아닙니다.

NO.43에서 「손님은 자기 에이전트를 데려오지 못한다」고 적었고, NO.45에서는 유나이티드가 「개인 에이전트의 예약 금지」를 발표한 것을, NO.49에서는 AT&T가 「정확도 90%대 중후반 전에는 자율권 없음」이라는 문턱을 둔 것을 적었습니다. 이번 주 소식 셋은 그 다음 단계 — **「해도 되는 일」을 행동이 일어나기 전에 문서로 적어 두는 방식**입니다. 가게는 에이전트가 오기 전에 파일 한 장을, 회사는 에이전트를 돌리기 전에 등록부 한 줄을, 애플은 답이 나가기 전에 조건 세 개를 적었습니다. 사실·해석·우리라면으로 나눠 적습니다.

## 1. Poppy 1.0 — 가게가 「우리 집에서 에이전트가 해도 되는 일」을 파일 한 장에 적는다 (사실, 회사 발표)

시에라(Sierra, 전 세일즈포스 공동 CEO 브렛 테일러가 이끄는 AI 고객 응대 회사)는 11월 13일 공식 블로그(브렛 테일러·클레이 베이버 공동 집필)에 **「Personal Agent Protocol」 — 애칭 Poppy — 1.0**을 냈습니다. 10월 6일 메타와 함께 처음 발표하고 10월 9일 초안을 낸 뒤 「5주 동안 실제 웹사이트·API·에이전트에 초안을 시험했다」고 적었습니다. 규격 원문(personalagentprotocol.org)을 직접 읽었습니다. 방식은 이렇습니다 — **회사가 자기 도메인의 `/.well-known/poppy.json`에 JSON 문서 하나를 올려 둡니다.** 그 안에 `organization`(이름·도메인·로고), 에이전트가 들어올 수 있는 길(`agent.protocols` 대화 창구, `apis` — OpenAPI나 MCP, `web` — 브라우저 세션 창구, `tasks`, `extensions`), 그리고 정책(`auth.disabled` 로그인 끄기, `web.disabled` 「우리 사이트를 브라우징하지 말라」, `web.unscoped` 브라우저 로그인이 계정 전체 접근인지)을 적습니다. 범위마다 **`irreversible`(되돌릴 수 없는 행동)·`personal_data`(개인정보 포함)** 표시를 붙이는 `scope_hints` 칸이 있습니다. 로그인은 OAuth 2.0(PKCE·기기 로그인 RFC 8628), 세션은 서명된 `Poppy-Session` 토큰입니다. 규격은 「1.0은 0.4에 수정을 더한 것」이라고 스스로 적고, 아직 안 다룬 영역은 로드맵 페이지로 넘깁니다. 시에라 글은 Poppy가 MCP·OpenAPI·UCP 같은 기존 규격 위에 얹혀 있고, 커머스 확장은 쇼피파이가 공동 저작했으며, 검증기가 든 구현 키트가 있다고 적었습니다.

참여 회사는 회사 발표입니다. 10월의 초기 설계 파트너 8곳(메타·제네시스·Instinct·NiCE·로켓·쇼피파이·스트라이프·월마트)에 60곳이 더해져 **100곳 이상**(어펌·델타항공·세일즈포스·트윌리오·웨이페어·줌 등)이고, 실제로 켠 곳은 머큐리(은행 — 결제 요청은 계정의 승인 정책을 거침)·싱크로니·터키항공(마일리지 회원이 비즈니스 좌석 업그레이드를 결제 전에 승인)입니다. 두 문장이 이 글의 중심입니다. **「모든 쇼피파이 매장이 이제 Poppy 파일을 자동으로 게시하므로 판매자는 따로 할 일이 없다」**(시에라) — 쇼피파이는 175개국 이상의 가게를 돌리고, 장바구니·결제는 UCP가, 그 앞의 「누구냐·무엇을 해도 되냐」는 Poppy가 맡습니다. 그리고 **「메타의 Muse는 방문하는 모든 사이트에서 Poppy를 먼저 찾는다」**. TNW(11월 13일)는 Muse 이용자를 「1,000만 명 이상」으로 적었고(매체 한 곳), 1.0이라는 번호에도 규격이 「초안」으로 표기돼 호환이 깨지는 변경이 올 수 있다는 점, 비자·마스터카드가 별도의 에이전트 신원 확인을 만들고 있다는 점, 아마존은 손님이 Muse 대신 자기 에이전트를 쓰길 원한다는 점을 함께 적었습니다.

배경을 두 줄 둡니다. Practical Ecommerce(9월 24일)에 따르면 쇼피파이는 9월 8일 — Muse가 나온 날 — 메타를 「Agentic Storefronts」에 추가해 판매자 상품을 기본으로 메타에 공유했고(판매자가 끌 수 있음), 아마존은 같은 Muse에 「허가받지 않은 AI 에이전트의 접속은 이용 약관 위반」이라는 문구를 띄워 막았습니다(NO.43). CMSWire(10월 7일)가 옮긴 시에라 공동창업자의 말은 **「소비자가 어떤 접근을 줄지 정하고, 회사가 에이전트가 할 수 있는 일의 한도를 정한다」**이고, 메타는 「이메일처럼 누구도 소유하지 않는 규격」이라고 했지만 거버넌스 모델은 공개되지 않았고 두 회사의 파트너 목록도 서로 달랐습니다. 규격 사이트 바닥글에 **Apache License 2.0**이 적혀 있습니다(personalagentprotocol.org, 11월 18일 직접 확인). 표준화 기구·거버넌스 주체는 명시돼 있지 않습니다. 결제는 아직 핵심이 아니라 「확장 후보」입니다.

## 2. 우버 — 「신원은 「누가」만 답한다」, 에이전트마다 허용 의도와 위험 등급을 등록한 뒤 실행 순간 검문 (사실, 회사 발표)

우버 엔지니어링 블로그(11월 6일, 션 타우트·맥스 주로비치·아디 라가벤드라)의 글 「Securing AI Agents: Lessons From Real-World Deployment」를 직접 읽었고, InfoQ(11월 15일)가 정리했습니다. 출발점 문장은 이것입니다 — **「전통적 권한 부여는 「누가」 행동할 수 있는지는 정할 수 있지만, 에이전트가 하려는 행동이 맥락상 적절한지는 판단할 수 없다.」** 막으려는 것은 프롬프트 주입·도구와 메모리 오염·목표 탈취·행동 드리프트·환각에서 나온 행동입니다(수법은 글에도 없고 우리도 쓰지 않습니다). 구조는 세 층입니다. **①배포 전**: 모든 에이전트를 「AI Registry」에 등록해 신원·소유자·페르소나·**허용 의도(intents)·제약·의존성·위험 등급**을 적고, 「Argus」라는 자동 분석기가 코드·프롬프트·설정·의존성·엔드포인트·도구 호출 경로를 훑어 약점을 찾고 페르소나·의도 초안을 미리 만들어 개발자가 검토합니다(MCP 서버와 도구도 같은 절차). **②실행 중**: 「AI Guard」가 정책 판단 지점으로 **로컬에 둔 작은 전용 모델**로 돌며, 「Agent Guard」 훅이 에이전트와 도구 실행의 경계에서 행동을 가로채 판단을 적용합니다. 보는 것은 행동이 페르소나·허용 의도·의미 제약에 맞는지, 사용자의 요청과 역할에 맞는지, 세션 전체 맥락에서 말이 되는지입니다. **③배포 후**: 에이전트 행동·도구 호출·판단을 한 줄로 묶은 실행 추적(민감 정보는 가리고 필요할 때만 내용 포함)과, 기록된 상호작용을 새 정책에 **「재생」**해 적용 전에 시험하는 장치입니다.

겪은 어려움도 적혀 있습니다 — **오차단과 오허용의 균형**(막지 않고 기록만 하는 섀도 모드·재생·에이전트별 보정으로 다룸), 지연 시간(병렬 실행·큰 범용 모델 대신 작은 전용 모델), 개발자 마찰(Argus 자동화), 그리고 「모든 에이전트에 같은 규칙」이 목적과 위험이 다른 에이전트에 맞지 않았다는 것. 글은 **「보안·정확도·지연·비용·자율성·개발자 경험은 따로따로 최적화할 수 없다」**로 맺고, 후속 글(페르소나·맥락 가드레일·관측·의도 필터링)을 예고했습니다. **수치는 하나도 없습니다** — 오차단율·지연·비용·에이전트 수 모두. 오픈소스 여부도 적혀 있지 않습니다. 참고로 우버는 8월에 별도 도구 「ADR」을 공개했다는 보도(Techstrong, 8월 10일 — 에이전트 5만 개 이상·10개월 운영·「자격 증명 노출이 프롬프트 주입보다 많았다」는 회사 발표)가 있는데, 그 기사도 11월 글도 서로를 언급하지 않아 **둘의 관계는 우리가 확인하지 못했습니다.** InfoQ 기사의 독자 질문 하나를 그대로 옮깁니다 — 「내가 만들지 않은 에이전트에는 이게 어떻게 적용되나.」

## 3. 애플 — 건강 AI 답변에 「임상 인용·우려 질문 감지·학습 미사용」을 붙여 20만 명에게 평가를 맡긴다 (사실, 회사 발표)

애플은 11월 15일 뉴스룸에 **「Apple Health AI Usage Study」**를 발표했고 같은 날 미국 앱스토어에 「Apple Health AI Study App」(개발자 Apple Inc., 무료, iPhone 전용, iOS 26.0 이상)을 올렸습니다. 두 페이지를 직접 읽었습니다. 협력사는 **OpenEvidence** — 2022년 설립된 마이애미의 의사용 LLM 의학 검색 회사로, 위키피디아에 따르면 2025년 12월 기준 미국 의사 약 76만 명이 등록하고 월 1,800만 건의 임상 상담에 쓰이며(회사 발표), NEJM·JAMA와 콘텐츠 라이선스를 맺고 있습니다(자금 조달 내용은 이 글에서 다루지 않습니다). 참가 조건은 **미국 거주 21세 이상, Apple Intelligence가 켜진 iPhone 15 Pro 이상, iOS 26 이상, 최대 20만 명**입니다. 참가자는 일상의 건강 질문을 하고, 복잡한 의학 정보를 쉬운 말로 읽고, 설문에서 답의 품질을 평가합니다. 답은 **NEJM·JAMA·Nature 같은 의학 출처에서 끌어오고 각 답에 동료 검토를 거친 임상 인용 링크가 붙습니다.** 원하면 Health 앱의 안정시 심박·활동·수면·검사 결과를 공유해 개인 데이터가 답의 적절성을 얼마나 바꾸는지 보게 합니다. 조건 세 개가 글에 적혀 있습니다 — **「연구 데이터는 AI 모델 학습에 쓰지 않는다」**, 앱에는 **「특정한 우려되는 질문을 감지해 참가자에게 의료진이나 다른 자원으로 후속 조치를 권하는」** 가드레일이 있다, 그리고 **「이 앱은 진단·치료를 하지 않고 전문가의 조언을 대신하지 않는다」**. 섬불 데사이 애플 건강·피트니스 부사장은 「건강은 깊이 개인적인 것」이라며 이 연구가 「사람들이 건강 AI를 어떻게 쓰고 이해하고 평가하는지 알아보는 가장 신중한 방법」이라고 했습니다. 연구 기간은 뉴스룸에 없습니다.

매체가 더한 것은 한 곳씩입니다. TechCrunch(11월 15일)는 연구가 **12개월 이상**이고, Health 데이터는 익명화돼 「안전한 제3자 클라우드」로 가며, **OpenEvidence가 질문·답변 데이터를 24시간 뒤 삭제한다**고 적었습니다(이 세 가지는 애플 뉴스룸에 없어 TechCrunch 한 곳). 같은 기사는 OpenAI가 올해 초 「주당 3억 건 이상의 건강 관련 질문」을 받는다고 밝혔다고 덧붙였습니다(OpenAI 원문은 우리 쪽에서 열리지 않아 미확인). TechCrunch는 기기 조건을 「iPhone 15 이상」으로 적었는데 애플 뉴스룸과 Business Standard(11월 16일)는 「iPhone 15 Pro 이상」이라 우리는 애플 표기를 따랐습니다. iGeeksBlog(11월 16일)는 애플이 「LLM 기반 소비자 건강 도구는 때로 불완전하거나 불명확한 답을 낼 수 있다」고 적었다고 인용했는데, 우리가 읽은 뉴스룸 본문에서 그 문장을 찾지 못해 매체 한 곳으로 둡니다. 앱스토어 개인정보 라벨은 「User ID — 이용자에게 연결됨(분석·앱 기능)」, 연령 등급 18+였습니다.

## 세 가지를 함께 읽으면 (해석)

첫째, **셋 다 「행동 전」에 적힌 문서입니다.** NO.39의 「멈춤 버튼」은 행동 뒤에 누르는 것이고, NO.49의 AT&T 「정확도 90%대 중후반」은 행동을 하면서 재는 문턱입니다. 이번 셋은 그 앞 — 에이전트가 오기 전에(poppy.json), 에이전트를 돌리기 전에(레지스트리), 답이 나가기 전에(인용·감지·고지) 적습니다. 순서가 뒤에서 앞으로 옮겨 오는 것이 올해 하반기의 방향으로 보입니다(해석). 세 문서의 공통 칸은 **「되돌릴 수 없는 행동」**입니다 — Poppy는 범위에 `irreversible` 표시를 붙이고, 우버는 「특권 행동을 사용자가 실제로 요청한 것에 묶는」 증거 사슬을 말하고, 애플은 우려 질문을 사람(의료진)으로 넘깁니다. NO.39에서 「되돌릴 수 없는 행동은 애초에 에이전트 손 밖」이라고 적었는데, 그 문장이 프로토콜의 필드 이름이 됐습니다.

둘째, **「막는 것」과 「여는 것」이 같은 파일에 적힙니다.** poppy.json에는 「우리 사이트를 브라우징하지 말라」(`web.disabled`)와 「API로 들어와라」(`apis`)가 나란히 있습니다. 유나이티드의 금지(NO.45)와 쇼피파이의 개방이 같은 형식의 문장이 될 수 있다는 뜻이고, 그래서 손님의 에이전트는 「막혔다」가 아니라 「이 길은 닫혔고 저 길은 열렸다」를 읽습니다(해석). 다만 읽을 때 조심할 것이 셋입니다 — 규격이 「1.0이지만 초안」이라 깨지는 변경이 예고돼 있고, 라이선스는 Apache License 2.0으로 적혀 있으나 거버넌스 주체는 명시돼 있지 않고, CMSWire가 적은 질문 「가게의 문을 어느 회사 에이전트가 지키나」(시에라도 고객 응대 에이전트를 파는 회사입니다)가 열려 있습니다. 「100곳 이상」은 설계 파트너 수이고 「켰다」는 곳은 셋이라, 숫자를 옮길 때 두 칸을 나눕니다(NO.21).

셋째, **우버와 애플은 「사람을 빼는 문서」가 아니라 「사람에게 넘기는 조건을 적은 문서」입니다.** 우버의 레지스트리는 자율권을 주기 위한 서류처럼 보이지만, 핵심은 「맥락에 안 맞는 행동을 실행 직전에 막는다」와 「새 규칙은 먼저 기록만 하는 섀도 모드로 돌린다」입니다. 애플은 20만 명에게 답을 평가하게 하면서 「진단·치료 아님」「우려 질문은 의료진으로」를 먼저 적었습니다. NO.03에서 우리 성분표 앱이 「안전하다」고 말하지 않게 만든 방법을 적었는데, 애플의 문서는 그것의 큰 판입니다 — 다른 점은 **답마다 인용 링크가 붙고, 그 답을 평가하는 사람이 이용자 자신**이라는 것(해석). 수치가 없는 점도 같습니다 — 우버는 오차단율을, 애플은 기간을, 시에라는 실제 세션 수를 적지 않았습니다. 이 글의 숫자 가운데 회사 밖에서 센 것은 하나도 없습니다.

## 우리라면 — 커머스·앱·AI 인플루언서를 운영하는 팀이 이번 주에 할 세 가지 (실전)

1. **우리 커머스 도메인의 `/.well-known/poppy.json`을 「게시하지 않고」 먼저 채워 본다.** NO.43의 「들어오는 에이전트 규칙 3줄」과 NO.45의 「왜」 칸을 이 파일의 필드로 옮기면 빈칸이 바로 보입니다 — `organization`, 어느 길을 열지(`web`만인지 `apis`도인지), `web.disabled`를 켤지, `scope_hints`에 주문·결제를 `irreversible`로, 배송지를 `personal_data`로 표시할지. 규격이 초안이라 **게시는 대표 결정 뒤**이고, 표 머리에 「1.0 = 초안, 깨지는 변경 가능」을 적어 둡니다. 우리 상품이 올라간 외부 채널 중 쇼피파이 기반이 있으면 그 매장은 이미 파일이 자동 게시됐으니 무엇이 적혔는지 한 번 읽어 봅니다.
2. **우리 에이전트 등록부 한 장을 우버식 일곱 칸으로 적는다.** 리아 대본 생성, 성분표 판정(NO.03), 커머스 문의 답변, 그리고 AP News를 수집해 쓰는 이 세션까지 — 각각에 신원·소유자·페르소나·허용 의도·제약·의존성(어떤 MCP 서버·도구를 쓰나)·위험 등급을 적습니다. NO.49의 「사람을 빼는 문턱 N%」 옆 칸에 둡니다. 새 제약을 넣을 때는 우버처럼 **2주간 섀도 모드**(막지 않고 기록만)로 돌린 뒤 오차단·오허용 건수를 보고 켭니다.
3. **세이프리스트(성분표 앱) 답변에 애플식 세 줄을 붙인다.** ①답마다 근거 링크(우리는 식약처 고시·원재료 DB가 인용), ②「우려 질문」 목록(알레르기 반응·약과의 상호작용·영유아 섭취 등은 답 대신 「전문가에게」로), ③약관에 「이용자 질문은 모델 학습에 쓰지 않는다」 문장이 실제로 있는지와 보관 기간(TechCrunch가 적은 「24시간」처럼 숫자로). 그리고 답 아래 평가 버튼 하나(「맞음 / 모르겠음 / 틀림」) — 20만 명은 아니어도 20건부터 세기 시작합니다.

## 이번에 고르지 않은 것

엔비디아 젠슨 황 CEO의 사임과 복귀설, 그에 따른 주가·공급망·수출 규제 보도는 개인 사안과 투자 영역이라 쓰지 않습니다. 앤트로픽 상장 관련 보도(블룸버그)는 투자 영역이고 이해관계가 있어 쓰지 않습니다. 연준 금융안정 설문의 「AI 리스크 응답 87%」(로이터)도 같은 이유로 제목만 둡니다. 디즈니의 AI 확대(블룸버그)는 원문을 열지 못했습니다. 메이투안 LongCat-2.5(1.6조 파라미터 오픈 웨이트, The Decoder)와 Edge0-145B는 공식 모델 카드를 확인하지 못해 토요일 주간 소식 후보로 둡니다. FAA의 항공 관제 보조 도구 SMART 전국 확대(기즈모도, 「사람 관제사가 최종 권한」)는 「사람 감독」 후속 후보지만 원자료를 열지 않았습니다. promppy에 보인 「백악관, AI 보안 사고 자진 신고 시 1년간 규제 책임 완화」(AI타임스)는 원문 주소를 확보하지 못했습니다. OpenAI의 과학 블로그 개설과 GPT-6 Astra와 쓴 표준모형 논문은 openai.com이 우리 쪽에서 열리지 않아 제목만 둡니다. Anthropic 모델 문서 페이지는 이번엔 Claude 4.x 모델만 보이는 구버전으로 열려 인용을 보류했습니다(11월 14일 확인한 Fable 5.1 표와 다름). 앤트로픽 뉴스룸에는 11월 16일에도 새 글이 없고, OpenAI 뉴스 목록은 이번에도 열리지 않았습니다.

## 이 소식에서 확인하지 못한 것

- Poppy 규격 사이트 바닥글에는 Apache License 2.0이 적혀 있으나(11월 18일 직접 확인), 표준화 기구·거버넌스 주체는 명시돼 있지 않습니다. 「100곳 이상」은 설계 파트너 수(회사 발표)이고 실제 켠 곳은 머큐리·싱크로니·터키항공 셋입니다. Muse 이용자 「1,000만 명 이상」은 TNW 한 곳입니다. 쇼피파이 자신의 발표 페이지는 찾지 않았고 시에라 글의 「전 매장 자동 게시」 문장으로 적었습니다.
- Poppy를 통해 실제로 오간 세션 수·주문 수는 어디에도 없습니다. 결제는 「확장 후보」로만 적혀 있습니다.
- 우버 글에는 수치가 없고(오차단율·지연·비용·에이전트 수), 오픈소스 여부도 없습니다. 8월 ADR 공개 보도(Techstrong 한 곳)와 11월 글의 관계는 확인하지 못했습니다. 우버가 어떤 모델 회사의 모델을 쓰는지도 글에 없습니다.
- 애플 연구의 기간은 뉴스룸에 없고 「12개월 이상」·「익명화 뒤 제3자 클라우드」·「OpenEvidence 24시간 뒤 삭제」는 TechCrunch 한 곳입니다. 기기 조건은 TechCrunch(「iPhone 15 이상」)와 애플(「iPhone 15 Pro 이상」)이 달라 애플을 따랐습니다. 「불완전하거나 불명확한 답」 문장은 iGeeksBlog가 애플 글을 인용한 것으로, 우리는 뉴스룸 본문에서 찾지 못했습니다.
- OpenEvidence의 의사 76만 명·월 1,800만 건은 위키피디아가 옮긴 회사 발표입니다. OpenAI의 「주당 3억 건 건강 질문」은 TechCrunch가 적은 것으로 OpenAI 원문은 열지 못했습니다.
- 어느 회사의 발표도 우리가 직접 시험하거나 세어 본 것은 없습니다.

## 함께 읽은 글

성격이 다른 출처를 직접 열어 확인했습니다. 회사 발표·공식 문서, 규격 원문, 매체 보도, 위키, 우리 이전 글을 나눠 적습니다.

회사 발표·공식 문서:

- [Releasing Poppy 1.0 (Sierra 블로그, 브렛 테일러·클레이 베이버, 11월 13일)](https://sierra.ai/blog/releasing-poppy) — 영문, MCP·OpenAPI·UCP 위 OAuth·5주 시험·커머스 확장 쇼피파이 공동 저작·파트너 100곳↑·머큐리·싱크로니·터키항공·「모든 쇼피파이 매장이 Poppy 파일 자동 게시」·Muse 전원 적용
- [Securing AI Agents: Lessons From Real-World Deployment (Uber Engineering, 11월 6일)](https://www.uber.com/blog/securing-ai-agents/) — 영문, AI Registry·Argus·AI Guard·Agent Guard·실행 추적·재생, 세 층 구조, 어려움 목록, 수치 없음
- [Apple launches research study to explore the use of AI for health (Apple Newsroom, 11월 15일)](https://www.apple.com/newsroom/2026/11/apple-launches-research-study-to-explore-the-use-of-ai-for-health/) — 영문, OpenEvidence·21세↑·iPhone 15 Pro↑·iOS 26·최대 20만 명·NEJM/JAMA/Nature 인용·우려 질문 감지·학습 미사용·진단 아님·데사이 발언
- [Apple Health AI Study App (App Store)](https://apps.apple.com/us/app/apple-health-ai-study-app/id6800060365) — 영문, 개발자 Apple Inc.·무료·iPhone 전용·iOS 26.0↑·「의료 조언·진단·치료 제공 안 함」·개인정보 라벨

규격 원문:

- [Personal Agent Protocol 1.0 Specification](https://personalagentprotocol.org/docs/1.0/spec) — 영문, `/.well-known/poppy.json`·organization·agent.protocols·apis·web·tasks·extensions·auth.disabled·web.disabled·scope_hints(irreversible·personal_data)·OAuth 2.0 PKCE·RFC 8628·Poppy-Session·「1.0 = 0.4 + 수정」(앞 10만 자 읽음)

매체 보도:

- [Sierra's Poppy 1.0: Shopify turns it on for every store, Meta's Muse looks for it first (TNW, 11월 13일)](https://thenextweb.com/news/sierra-poppy-1-0-shopify-meta-muse-personal-agents) — 영문, Muse 1,000만 명↑(한 곳)·「1.0이지만 초안」·터키항공·머큐리 사례·비자·마스터카드·아마존
- [Sierra and Meta unveil Personal Agent Protocol (TNW, 10월 6일)](https://thenextweb.com/news/personal-agent-protocol-sierra-meta) — 영문, 첫 발표·파트너 6곳·OAuth·손님이 읽기/쓰기 결정·회사가 경로 결정·결제는 미래 작업
- [Sierra's Poppy draft spells out how AI agents can access businesses (NeoTeo, 10월 9일)](https://www.neoteo.com/en/sierras-poppy-draft-spells-out-how-ai-agents-can-access-businesses) — 영문, 초안·/.well-known/poppy.json·설계 파트너 35곳 추가·로켓 데모(시에라 자체 설명)
- [Genesys joins Sierra, Meta on open standard for personal AI agents (CMSWire, 10월 7일)](https://www.cmswire.com/contact-center/genesys-joins-sierra-meta-on-open-standard-for-personal-ai-agents-01/) — 영문, 「소비자가 접근을 정하고 회사가 한도를 정한다」·거버넌스 미공개·파트너 목록 차이·열린 질문
- [Meta Muse, Shopify, Amazon and the race to own AI shopping (Practical Ecommerce, 9월 24일)](https://www.practicalecommerce.com/?p=1567232) — 영문, 배경: 9/8 쇼피파이 Agentic Storefronts에 메타 추가·아마존의 Muse 차단 문구
- [Uber's Secure AI framework for autonomous agents (InfoQ, 11월 15일)](https://www.infoq.com/news/2026/11/uber-secure-ai-framework/) — 영문, 우버 글 정리·독자 질문 「내가 만들지 않은 에이전트엔」
- [Uber open-sources ADR to catch agentic blunders (Techstrong.ai, 8월 10일)](https://techstrong.ai/articles/uber-open-sources-tool-to-catch-agentic-blunders-legacy-security-misses/) — 영문, 8월 별도 도구(회사 발표 수치, 한 곳) — 11월 글과의 관계 미확인
- [Apple launches new app to study how people use AI for health (TechCrunch, 11월 15일)](https://techcrunch.com/2026/11/15/apple-launches-new-app-to-study-how-people-use-ai-for-health/) — 영문, 12개월↑·익명화·제3자 클라우드·24시간 삭제(한 곳)·OpenAI 주당 3억 건(전언)
- [Apple launches app to study how people use AI for health queries (Business Standard, 11월 16일)](https://www.business-standard.com/technology/tech-news/apple-launches-app-to-study-how-people-use-ai-for-health-queries-details-126111600875_1.html) — 영문, iPhone 15 Pro↑·미국 한정·기간·보상 없음
- [Apple's AI health study is open to up to 200,000 U.S. iPhone users (iGeeksBlog, 11월 16일)](https://www.igeeksblog.com/apple-health-ai-usage-study-app/) — 영문, 「불완전하거나 불명확한 답」 인용(한 곳)·기간 미공개·개인정보 라벨

위키:

- [OpenEvidence (Wikipedia)](https://en.wikipedia.org/wiki/OpenEvidence) — 영문, 2022년 설립·마이애미·의사 76만 명·월 1,800만 건(회사 발표)·NEJM·JAMA 라이선스

우리 이전 글:

- [쇼호스트도 카메라도 없는 방송이 정규 편성됐다 (AP News NO.49)](https://www.apholdings.kr/ko/news/no-host-ai-broadcast-and-who-must-disclose/)
- [주간 AI 소식 — OpenAI는 에이전트에게 지갑을 쥐여 줬고, 유나이티드는 「손님의 에이전트」를 문 밖에 세웠다 (AP News NO.47)](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [손님의 에이전트는 막고, 가게는 들이고, 모델은 모두에게 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [손님은 자기 에이전트를 데려오지 못한다 (AP News NO.43)](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [「에이전트가 권한을 넘을 수 있다」가 공시에 적히기 시작했다 (AP News NO.39)](https://www.apholdings.kr/ko/news/agent-risk-goes-into-the-filings/)
- [확인 코드가 에이전트 손에 닿으면 (AP News NO.36)](https://www.apholdings.kr/ko/news/agents-raised-their-own-spending-caps/)
- [에이전트는 「믿을 수 없는 내부자」다 (AP News NO.29)](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
- [숫자를 비교하기 전에 셈법부터 (AP News NO.21)](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [AI가 성분표를 대신 읽을 때 (AP News NO.03)](https://www.apholdings.kr/ko/news/ai-reads-the-label/)
