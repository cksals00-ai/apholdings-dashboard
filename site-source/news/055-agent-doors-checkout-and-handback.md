---
no: 55
slug: agent-doors-checkout-and-handback
date: 2026-11-23
category: 실전
tags: AI 에이전트 · 에이전틱 커머스 · 구글 Connected Apps · Universal Commerce Protocol · 부킹홀딩스 Vayo · 결제 넘김 · 세이버 MCP · Grok · 유나이티드 · 업셀 · 에이전트 경유 가격 · 상품 정보
title: 에이전트가 결제 버튼 앞까지 왔다 — 구글은 검색 안에서 장보기 결제를 열었고, 부킹홀딩스의 에이전트는 「허용하지 않는 공급사에선 결제창을 손님에게 넘긴다」고 적었고, 세이버는 「손님은 결과를 넘겨 보지 않고 한두 개만 본다」며 거래 엔진을 그록에 먼저 꽂았고, 호텔 CEO는 「에이전트는 충동구매를 안 한다」며 문을 닫겠다고 했다 — 가게가 이번 주에 정할 것은 문의 종류 넷 중 하나다
summary: 구글은 11월 20일 미국에서 검색과 Gemini 앱의 Connected Apps로 Albertsons·Safeway·Shaw's·Target의 장보기 주문을 만들고 결제까지 끝내는 기능을 열었다고 발표했습니다(Universal Commerce Protocol 기반·가격·수치 없음). 부킹홀딩스의 AI 여행 에이전트 Vayo는 11월 17일 「직접 연동이 있으면 연동으로, 없으면 예약 사이트를 탐색해 예약하고, 공급사가 에이전트 예약을 허용하지 않으면 가격을 확인한 뒤 결제창을 여행자에게 넘긴다」고 보도자료에 적었습니다(비공개 베타). 여행 유통망 회사 세이버는 11월 16일 Grok Bot 마켓플레이스에 첫 여행 플러그인을 올리고 「MCP 서비스를 시범·운영 중인 파트너 80곳 이상」이라고 발표했으며, CEO는 매체에 「손님은 결과를 넘겨 보지 않고 한두 개, 많으면 세 개만 본다」고 말했습니다. 반대편에서는 호텔 체인 CEO가 「사람은 판촉에 흔들리지만 에이전트는 아니다」며 자기 호텔의 에이전트 예약을 막겠다고 했고, 부킹홀딩스는 LLM 경유 예약이 「1%에 훨씬 못 미친다」고 말했다고 Skift가 전했습니다. 넷을 「문의 종류·손잡이·한두 개만 보이는 진열대·아직 작은 숫자」로 묶어, 커머스·앱·AI 인플루언서를 운영하는 작은 팀이 이번 주에 정할 한 장(문 표)을 적습니다. NO.45·47·50·53의 「에이전트 문」 실전편입니다.
---
> 이 글은 AI(Claude)와 함께 작성했고 편집자가 검수했습니다. 우리 회사는 앤트로픽과 OpenAI 두 회사의 유료 고객이고 구글·메타 모델도 시험에 씁니다. 이해관계를 먼저 적습니다 — **이 글의 주제인 「가게 쪽 결정」은 우리 자신의 일입니다.** 우리는 커머스(한글컵스)·앱(코트메이트 등)·AI 인플루언서(리아)를 직접 운영하므로 「우리라면」 절은 우리가 실제로 할 일을 적은 것이고, 어느 플랫폼을 권하는 글이 아닙니다. 1번 구글 소식은 우리가 시험에 쓰는 회사의 발표이고, 3번 세이버가 2027년 확장 대상으로 매체에 말한 플랫폼 목록에는 이 글을 쓴 AI를 만든 앤트로픽의 Claude가 들어 있습니다(보도자료에는 이름이 없습니다). 그래서 어느 회사에도 평가를 보태지 않고 발표된 숫자와 문장만 옮기며, 회사가 발표한 수치는 「회사가 발표한 것」으로, 한 곳에서만 나온 내용은 그 출처를 함께 적었습니다. 이 글은 특정 기업에 대한 투자 의견이 아닙니다.

NO.45에서 유나이티드가 「손님의 에이전트」를 문 밖에 세운 날 OpenAI가 가게들을 ChatGPT 안으로 들인 일을, NO.47에서 OpenAI가 에이전트에게 지갑을 쥐여 준 일을, NO.50에서 쇼피파이 가게들이 「에이전트가 해도 되는 일」을 한 장으로 자동 게시하기 시작한 일을, NO.53에서 메타의 에이전트가 캐나다 장보기에서 결제까지 들어간 일을 적었습니다. 이번 주 소식 넷은 그 문들이 **어떤 모양으로 굳어 가는지**를 보여 줍니다 — 구글은 검색 안에 결제 문을 열었고, 부킹홀딩스의 에이전트는 「허용하지 않는 가게에서는 결제창을 손님에게 넘긴다」는 중간 문을 적었고, 세이버는 가게와 에이전트 사이의 「거래 엔진」 자리를 잡으려 하고, 호텔 체인은 문을 닫는 이유를 숫자로 말합니다. 회사 발표 셋(구글·Vayo·세이버)과 매체 보도·칼럼(Skift·PhocusWire)을 사실·해석·우리라면으로 나눠 적습니다.

## 1. 구글 「연말 할 일을 Connected Apps로」 — 검색 안에서 장보기 결제까지 (사실, 회사 발표)

구글 공식 블로그 글 **「Get your year-end tasks done with new Connected Apps」**(11월 20일, 필자 표기 없음)를 직접 읽었습니다. 미국에서 **검색과 Gemini 앱의 Connected Apps로 Albertsons·Safeway·Shaw's·Target의 장보기 주문을 만들고 결제까지 끝낼 수 있다**는 발표입니다. 글은 이 장보기 앱들이 **「Universal Commerce Protocol(UCP) 기반」**이라고 적고 별도 커머스 글로 연결합니다. 금융은 **Experian**이 Gemini 앱에 이미 있고 이제 검색으로 확대돼 신용 등급 확인과 개인 대출 비교를 할 수 있고, 세금은 **H&R Block**을 검색에서 불러 세금 계산·환급 추정을 할 수 있고, **Angi·Thumbtack**(동네 수리·장식 인력)은 「몇 주 안」에 검색에 연결된다고 적었습니다. **가격·수수료·이용 수치·정확한 출시일·미국 밖 일정은 글에 없습니다.** 수치는 하나도 없는 발표입니다.

배경 둘을 함께 읽었습니다. 첫째, 10월 28일 구글 개발자 글 **「Build and manage Connected Apps in one place」**(검색·Gemini 앱 제품 책임자 두 명 이름). Connected Apps Platform을 미리보기로 열었고, 개발자는 **클라우드 MCP 서버 또는 Android MCP(AppFunctions API)로 연동**해 **Google Connected Console**에서 등록·시험·제출하고 검색·Gemini 앱 어디에 올릴지 고르며, 출시 뒤 트래픽·지연·오류율과 인증된 로고·계정을 관리합니다. 「50개 이상의 Connected Apps」가 이미 나왔고(생산성·티켓·건강·피트니스), Adobe·Experian·Localiza·Peloton이 Gemini에 있고 검색으로 「몇 주 안」에 온다고 적었습니다. 이 글에는 UCP·수수료·심사 기간·국가 목록이 없습니다. 둘째, 타깃의 공식 자료 **「How Target is Shaping Shopping Experiences in Conversational AI」**(6월 18일 갱신). 타깃은 구글 검색(AI Mode 포함)·Gemini 앱, 마이크로소프트 Copilot, OpenAI ChatGPT **세 플랫폼에서 결제가 되는 첫 대형 소매점**이라 적고, 구글에서의 흐름을 「질문 → 선택지 → 「Buy」 → 타깃 계정 로그인 → 확인」, 결제는 Google Pay의 신용카드나 Target Circle 카드, 그리고 **「한 번에 여러 상품 결제는 준비 중」**(6월 시점)이라고 적었습니다. 수치 하나 — **「AI가 데려온 트래픽이 1분기에 전년 대비 2,000% 늘었다」**(타깃이 발표한 것, 소매 전체는 약 400% — 어도비 자료 인용). 7월의 1차 Connected Apps(Instacart·Canva·YouTube Music, 미국·옵트인·구매는 사용자 승인 — eWeek 7월 17일)에서 이번 11월 장보기 결제까지 넉 달입니다.

## 2. 부킹홀딩스 Vayo 「여행 전부를 예약한다」 — 연동·탐색·그리고 「결제창을 손님에게 넘긴다」 (사실, 회사 발표·매체)

부킹홀딩스 산하 AI 여행 스타트업 **Vayo의 보도자료**(11월 17일, 시애틀, PR Newswire — 우리는 finviz 전재본으로 읽었고 원문 주소가 함께 적혀 있습니다)와 PhocusWire·Skift(테크 담당 애드리아나 리 기자, 11월 17일) 기사를 읽었습니다. 출시 한 달 만에 Vayo가 **항공·호텔·휴가 숙소·식당·액티비티·공연 티켓·렌터카·기차·버스·페리·공항 이동·주차까지** 예약한다는 발표입니다(비공개 베타 회원에게 당일 제공, 대기 명단 있음).

방법이 이 글의 핵심입니다. 보도자료는 **「직접 연동이 있는 곳은 연동으로, 없는 곳은 예약 사이트를 탐색해 여행자 대신 예약을 완료한다」**고 적고, **「공급사가 에이전트 예약을 지원하지 않으면 Vayo는 최선의 선택지를 찾아 가격을 확인한 뒤, 바로 끝낼 수 있게 준비된 결제창을 여행자에게 건넨다」**고 적었습니다. 모든 예약은 여행자 승인이 필요하고, **공급사의 확정을 받은 뒤에만 「확정」으로 표시**합니다. 로그인은 **1Password for Agents**로 비밀번호를 보거나 저장하지 않고, 결제는 **Stripe의 Link 에이전트 지갑**으로 결제 정보를 보지 않고 끝낸다고 적었습니다. 가격 — **Booking.com이 최선의 선택지일 때 모든 Vayo 여행자는 Booking.com의 최고 등급 Genius Level 3 가격(일부 숙소 최대 20% 할인)**을 받습니다. Vayo 자체 요금·공급사 목록·예약 건수는 보도자료에 없습니다. PhocusWire는 Vayo CEO(마이크 프리젠) 말로 **「유나이티드처럼 허용하지 않는 곳에서는 결제창을 넘기며, 허가된 경로로 협력할 기회를 환영한다」**를 전했고, 부킹홀딩스가 출시 때 **「제품 진전과 시장 상황을 조건으로 1억 달러 투자 계획」**을 밝혔으며 뉴욕의 Lola(KAYAK 창업자들)에도 같은 금액을 발표했다고 적었습니다(1억 달러는 PhocusWire·Skift 두 매체, 보도자료에는 없음). Skift는 직접 연동이 Booking.com(호텔·렌터카·액티비티)·OpenTable·SeatGeek이고 항공·기차 등은 허용된 공급사 사이트 탐색이라 적었고, Genius 가격이 비교에서 Booking 자체 재고를 유리하게 할 수 있다는 점(Skift의 분석), 그리고 **Skift Research 10월 조사에서 미국 여행자 27%만 AI 예약이 편하다고 답했고 AI의 비중이 「영감」 단계 21% 대 「예약」 단계 6%**라는 숫자를 붙였습니다. 예약 건수·결제창을 넘긴 비율은 회사가 공개하지 않았습니다.

## 3. 세이버 「거래 엔진」 — Grok Bot에 첫 여행 플러그인, 「MCP 파트너 80곳 이상」, 「손님은 한두 개만 본다」 (사실, 회사 발표·매체)

여행 유통망(GDS) 회사 세이버의 **보도자료**(11월 16일, 텍사스 사우스레이크, PR Newswire — finviz 전재본)와 PhocusWire, Skift(11월 19일, 같은 기자)를 읽었습니다. 세이버는 11월 17일 뉴욕 투자자 데이에서 **Grok Bot 마켓플레이스에 올라갈 「첫 글로벌 여행 플러그인」**을 미리 보였고, 대화형 예약·관리 창구 **Mosaic Travel Connector를 「곧 베타」**로 낸다고 발표했습니다. 2025년에 낸 MCP 서버와 에이전트용 API 위에 올라가며, **「MCP 서비스를 시범 또는 운영 중인 파트너가 80곳 이상」**(회사 발표·시범/운영 구분과 이름 없음)이라고 적었습니다. 새로 발표한 **「이벤트 구동 API」**는 결항·지연 신호를 감시해 영향받는 여행자를 짚고 여행사 시스템과 연결된 AI 도구에 알림을 밀어 넣으며, 대응은 **사람 상담사·커넥터가 대화 안에 규정에 맞는 선택지를 띄워 한 번 탭으로 승인·자율 에이전트가 직접 처리**의 세 경로라고 설명합니다. 가격 모니터링은 베타, 「2027년 동안 주요 대화형 모델과 여행사 워크플로로 확장」이 계획이고, **요금·수익 조건·수수료는 보도자료에 없습니다.** Grok 외의 플랫폼 이름도 보도자료에는 없습니다.

매체가 더한 것. PhocusWire는 세이버 CEO 커트 에커트가 3분기 실적 발표에서 **「LLM 플랫폼들은 아직 소비자보다 기업 쪽 기회에 더 집중한다」**고 말했다고 전했고, Skift는 에커트의 말로 **「소비자는 결과를 페이지 넘겨 보지 않을 것이고, 한 개·두 개·많으면 세 개의 선택지를 받을 것」**을 옮기며 2027년 확장 대상으로 **ChatGPT·Claude·Gemini**를 적었습니다(이 세 이름은 Skift 보도, 보도자료엔 없음). Skift의 요약에는 「지금 여행사에 주는 인센티브가 LLM과의 수익 공유 형태로 바뀔 수 있다」는 에커트의 생각과 「경제성은 입증되지 않았고 다년 전망에서 대체로 빠져 있다」는 Skift의 평가가 있는데, 이 대목은 본문이 아니라 기사 요약 블록에 있어 **Skift 요약 1곳**으로 둡니다.

## 4. 반대편 — 「에이전트는 충동구매를 안 한다」와 「LLM 경유 예약은 1%에 훨씬 못 미친다」 (사실, 매체 칼럼·회사 발언)

Skift 창업자 라파트 알리의 칼럼 **「The AI Agent Is Travel's Ad Blocker」**(11월 18일)를 읽었습니다 — **앞 다섯 문단까지 열리고 그 뒤는 유료 벽**이라 뒷부분은 기사의 요약 블록으로만 읽었습니다. 열린 본문의 요지는 이렇습니다. 여행 회사의 수익은 결제 단계의 충동구매(좋은 좌석·객실 업그레이드)에서 나오는데, **여행자 대신 예약하는 에이전트는 충동구매를 하지 않는다** — 그래서 업셀 이익이 위험하다는 것입니다. 호텔 체인 MCR의 CEO 타일러 모스가 이달 초 Skift 커머스 서밋에서 이 걱정을 말했고, 요약 블록에 따르면 **「사람은 판촉에 흔들리지만 에이전트는 아니다」며 자기 호텔의 에이전트 예약을 막고 싶다**고 했습니다. 애널리스트 Citizens의 11월 15일 보고는 에이전트 둘(Instinct·메타 Muse)로 예약을 시험해 「인상적이지 않았다」면서도 온라인 여행사에 장기 위험이 크다고 봤고, 노출 순위를 Expedia·부킹홀딩스·에어비앤비(가장 덜) 순으로 적었습니다(Skift 전언·방법 미확인).

요약 블록에만 있는 숫자들은 **Skift 요약 1곳**으로 적습니다 — 항공 부가 수익 2025년 1,570억 달러·전체의 약 16%(2016년 674억·9.1%, IdeaWorksCompany 추정), Expedia 3분기 광고 매출 2억 600만 달러, 에어비앤비 CEO의 「광고 10억 달러 기회」 발언, Skift가 Instinct에 「광고 배치가 추천에 영향을 주나」 물었을 때의 답 「배치는 내가 쓰는 신호가 아니다」, **부킹홀딩스가 LLM 경유 예약을 전체 룸나이트의 「1%에 훨씬 못 미친다」고 말한 것**, 그리고 **윈덤이 자기 AI 전화 상담원은 공시 요금보다 평균 15% 높은 요금으로 예약한다고 말한 것**(「에이전트도 팔 수 있다」의 예로 칼럼이 든 것). 유나이티드의 에이전트 제한(NO.45)이 같은 날 발표됐고 그 이유는 매출이 아니라 「보안·규제 위험」이었다는 점도 요약에 있습니다.

## 짧게 둘 (사실, 회사 발표)

- **구글 「다른 AI 앱의 기록을 Gemini로 옮기기」**(11월 19일) — 다섯 단계입니다: Gemini 가져오기 설정에서 프롬프트를 복사 → 이전 AI 도구에 붙여 선호 요약을 받음 → 그 답을 Gemini에 붙임 → 이전 제공사 계정에서 대화 기록 ZIP 내보내기 → Gemini 설정에 업로드. 어느 제공사가 지원되는지·용량 한도·요금제·보관 조건은 글에 없습니다. **「갈아타는 문」**입니다 — NO.48 「모델을 바꾸는 데 몇 주가 걸린다」의 소비자 쪽 판입니다.
- **구글 Gemini API 「Tool Retrieval」**(11월 19일, 미리보기) — 에이전트가 도구를 수십·수백 개 달 때 모든 도구의 매개변수 명세를 매번 보내지 않고, 이름·설명만 두고 필요할 때 명세를 불러오게 하는 기능입니다(`tool_search` 도구 + 보류할 도구에 `defer_loading`). 원격 MCP 서버 전체를 지연 로드할 수도 있고, 별도 과금은 없으며(불러온 명세는 그 뒤 입력 토큰으로 과금), **절감 수치는 글에 없고 「자기 트래픽으로 측정하라」**고 적었습니다. 1번의 Connected Apps가 MCP로 연동되는 것과 같은 자리입니다 — 가게가 내놓는 「도구」가 많아질 때의 기술입니다.

## 네 가지를 함께 읽으면 (해석)

첫째, **문은 넷으로 갈라졌습니다 — 직접 연동, 탐색 허용, 결제 넘김, 금지.** NO.45에서 「손님의 에이전트는 막고 가게는 들이고」로 적었던 둘 사이에 Vayo가 중간 문 둘을 적었습니다. 「탐색 허용」은 에이전트가 가게 사이트를 사람처럼 돌아다녀 예약을 끝내는 것이고, 「결제 넘김」은 에이전트가 **가격 확인까지 다 해 두고 마지막 결제 버튼만 손님이 누르는** 것입니다. 중요한 것은 **에이전트가 「결제 넘김」 문으로도 우리 결제 페이지 앞까지 온다**는 점입니다 — 가게가 아무것도 정하지 않아도, 에이전트는 사이트를 읽고 장바구니를 채우고 손님을 결제창 앞에 세울 수 있습니다. 그러니 「우리 가게는 에이전트와 무관하다」는 선택지는 없고, **넷 중 어느 문인지 정하는 일만 남습니다.** 유나이티드(보안·규제)와 MCR(업셀)이 「금지」를 고른 이유가 서로 다르다는 점도 적어 둡니다 — 금지도 이유가 두 종류입니다.

둘째, **손잡이는 규격이고, 작은 가게는 규격을 고르는 쪽이 아니라 따라가는 쪽입니다.** 구글의 장보기 결제는 UCP 위에, Connected Apps 플랫폼은 MCP 위에, 세이버의 거래 엔진도 MCP 위에, 쇼피파이 가게들은 poppy.json(NO.50) 위에 있습니다. 세 규격이 경쟁하는 것처럼 보이지만 가게 쪽에서 보면 공통점이 더 큽니다 — **상품·가격·재고·조건을 기계가 읽을 형식으로 내놓고, 「해도 되는 일」을 적고, 결제는 지갑(Stripe Link·Google Pay)이 대신 든다.** 세이버의 「80곳 이상」은 시범과 운영을 가르지 않은 숫자이고(회사 발표), 구글의 「50개 이상」은 앱 수이지 거래량이 아닙니다. 규격이 몇 개 살아남을지는 우리가 정할 수 없지만, **상품 정보 1장을 정확하게 만드는 일**은 어느 규격이 이겨도 필요합니다 — NO.53의 「에이전트가 읽을 상품 정보 1장」이 이번 주 가장 싼 준비입니다.

셋째, **「한두 개만 보인다」가 진열대를 바꿉니다.** 에커트의 「소비자는 페이지를 넘기지 않고 한 개·두 개·세 개만 받는다」는 말은 검색 광고 시대의 「10개 결과 중 상위」 경쟁이 **「에이전트의 선택 기준에 들어가는가」 경쟁**으로 바뀐다는 뜻입니다. 그리고 Vayo의 Genius Level 3는 **「에이전트 경유 가격」이라는 새 칸**을 보여 줍니다 — 같은 방을 사람이 사이트에서 사는 값과 에이전트가 사 주는 값이 다를 수 있고, 그 차이가 어느 재고를 고를지에 영향을 줄 수 있다는 점은 Skift도 지적했습니다. 라파트 알리의 「광고 차단기」 논점은 그 반대편입니다 — 에이전트는 업셀을 사지 않으니 결제창의 「한 번 더 권하기」 수익이 줄 수 있다는 것. 윈덤의 「AI 전화 상담원은 15% 높게 판다」(Skift 요약 1곳)는 **가게 쪽 에이전트는 팔 수 있다**는 반례로 칼럼이 든 것입니다. 종합하면 가게는 두 가지를 정해야 합니다: **손님 쪽 에이전트에게 보여 줄 가격·조건, 그리고 우리 쪽 에이전트가 권할 것.**

넷째, **숫자는 아직 작습니다 — 그래서 지금 정하는 것이 싸다.** 부킹홀딩스의 「1%에 훨씬 못 미친다」(Skift 요약 1곳), Skift Research의 「예약 단계 6%」, 에커트의 「LLM 플랫폼은 아직 기업 쪽」, Citizens의 「인상적이지 않았다」, 그리고 NO.43의 에어비앤비 「극히 미미」·NO.40의 우버 「가장 바쁜 주에 4건」 — 손님 쪽 에이전트가 실제로 결제까지 가는 비율은 어느 회사 숫자로도 아직 한 자릿수 아래입니다. 구글은 수치를 하나도 발표하지 않았습니다. 그러니 이번 주에 할 일은 **연동 개발이 아니라 문의 종류를 적는 것**입니다 — 돈이 들지 않고, 에이전트가 많아진 뒤에 고치는 것보다 훨씬 쌉니다. 그리고 넘긴 결제창이 깨지면(로그인 벽·만료된 장바구니·캡차) Vayo의 규칙대로 **「확정」은 공급사 확정 뒤에만** 뜨니, 깨진 결제창은 매출이 아니라 「예약 안 됨」으로 끝납니다.

## 우리라면 — 커머스·앱·AI 인플루언서를 운영하는 팀이 이번 주에 쓸 한 장 (실전)

1. **문 표 한 장 — 우리 상품·서비스마다 넷 중 하나를 적는다.** 한글컵스 상품, 코트메이트의 유료 기능, 리아 채널의 협업 문의, 앱 구독 — 줄마다 **직접 연동 / 탐색 허용 / 결제 넘김 / 금지** 중 하나와 이유(결제·환불 위험, 재고, 규제)를 적습니다. 기본값은 **「결제 넘김」**으로 둡니다 — 에이전트가 장바구니까지 만들고 결제 버튼은 사람이 누르는 흐름입니다. 그다음 **우리 결제 페이지가 그 흐름을 깨뜨리지 않는지** 사람이 한 번 걸어 봅니다: 로그인 벽, 짧은 세션 만료, 캡차, 장바구니 링크가 공유되는지. Vayo의 규칙 둘을 그대로 빌립니다 — **주문은 우리 시스템의 확정이 있어야 「확정」**, **승인은 건마다**([NO.54](https://www.apholdings.kr/ko/news/agent-roster-and-incident-log/) 「에이전트 명부·사고 일지」의 「돈을 말하는 문장 출처 필수」와 같은 줄). 「금지」를 고른 줄에는 유나이티드식(보안)인지 MCR식(업셀)인지 이유를 적습니다.
2. **손잡이는 상품 정보 1장부터 — 규격은 나중에 고른다.** 쇼피파이 가게는 poppy.json(NO.50)이 이미 있고, 구글 Connected Apps 콘솔과 UCP는 미국 한정이라 지금 우리가 할 수 있는 것은 **에이전트가 「가격을 확인」할 때 걸리지 않을 정보**입니다 — 가격·재고·배송일·환불 조건·사이즈 규격을 한 곳에, 기계가 읽을 수 있게(구조화 데이터·상품 피드), 그리고 **사이트 두 곳에 다른 가격이 없게.** Vayo가 「가격을 확인한 뒤」 결제창을 넘긴다고 적은 이유가 여기 있습니다 — 불일치는 에이전트에서 「고르지 않음」으로 끝납니다. 세이버의 「80곳」·구글의 「50개」는 우리 결정의 근거가 아니라 「규격이 셋 이상 돌고 있다」는 신호로만 읽습니다.
3. **「한두 개만 보이는 진열대」에 들어갈 조건 두 줄과 에이전트 경유 가격 한 줄.** 에이전트가 선택지를 한두 개로 줄일 때 우리 상품이 들어가려면 **비교 가능한 조건**(배송일·환불·총액)이 적혀 있어야 합니다 — 한글컵스 세트, 농구화 추천 글마다 그 두 줄을 넣습니다. 그리고 Genius Level 3처럼 **에이전트 경유 주문에 다른 가격·조건을 둘 것인지**를 한 줄로 정합니다(우리 답은 「같은 가격, 업셀 없음」으로 시작 — 라파트 알리의 논점대로 결제창의 「한 번 더」는 에이전트에게 통하지 않으니, 업셀 대신 세트 구성 자체를 상품으로 둡니다). 리아 대본에는 「에이전트가 손님 대신 고르는 시대」를 배우는 톤으로, 수치는 「reported」로만 넣습니다. 우리 자신의 AI 사용 쪽에서는 「갈아타는 문」을 한 번 걸어 봅니다 — 대화 기록을 내보내 보고, 내보낼 수 없는 지식이 있으면 NO.48의 원칙대로 모델 밖 문서로 옮깁니다.

## 이번에 고르지 않은 것

OpenAI 수석과학자의 **「Perplexity and Intelligence」**(11월 22일 — 내부 퍼플렉시티 수치 공개와 연구소 공통 「한도」 제안)는 이번 주 가장 큰 평가·안전 소식이지만 이 글의 주제(가게의 문)와 결이 달라 **다음 글에서 따로 다룹니다**(NO.52·54 후속, OpenAI 정렬·배포 안전 페이지 점검과 함께). 네이버 AI Lab의 **Unfinished-Bench**(「에이전트가 규칙을 적은 뒤 어겼다 89%」, AI Weekly 전언·arXiv 원문 미열람)와 **SimAudit**(로봇 벤치마크 채점기 결함 61건, 전언)도 같은 다음 글의 자료입니다. Lean·Mathlib 커뮤니티의 **「리만 가설 증명 인증」** 공동 성명(11월 21일)은 직접 열었는데 **글에 AI 도구 언급이 없어** AI Weekly 제목의 「Claude 도움」은 확인되지 않았고, 이 글을 쓴 AI의 제조사 관련이라 쓰지 않습니다. 앤트로픽 상장 종결·「주관사 조건」(로이터 제목)·Next.ink의 상장 기사는 투자라 제목만. 전미주지사협회의 「연방 AI 규칙·주법 유지」 성명(11월 22일)은 NO.39 후속 후보. OVHcloud의 오픈 웨이트 모델 Olala(Next.ink)는 NO.51 후속 후보. 르피가로–OpenAI 콘텐츠 계약(Next.ink 제목)은 NO.42 후속 후보. 구글 RSS의 Watch Duty 산불 경보·양자·클린 에너지 글, 캐나다 사이버센터의 Oracle Java 경보는 AI 소식이 아니거나 거리가 있어 뺐습니다. Learn:US 42호(클로드 트레이더 스킬)는 투자 영역이라 제목만. Kayak의 AI 기능 28개(Skift 제목만)·Lola CEO의 Muse 비판(제목만)·OpenAI의 ChatGPT 여행 인력 채용(발췌만)은 본문을 열지 않아 쓰지 않았습니다. 11월 20일 초안(올리브영 「디파인:옴니」·GPT-6.2 인하)은 아직 홈페이지에 없어 링크하지 않았습니다.

## 이 소식에서 확인하지 못한 것

- 구글 Connected Apps 장보기 결제는 회사 발표이고 가격·수수료·이용 수치·정확한 출시일이 없습니다. 「UCP 기반」 설명 글(커머스 쪽 별도 글)과 Connected Apps 지원 앱 목록 페이지는 열지 않았습니다. 10월 28일 글의 「50개 이상」은 앱 수이고 거래 수치는 없습니다. 타깃 자료의 「2,000%」는 타깃이 발표한 1분기 수치이고 측정 방식은 자료에 없으며, 6월 자료라 11월의 장보기 결제 흐름(다품목 결제 여부)은 그 자료로 확인할 수 없습니다. 미디어 두 곳(MediaPost·Search Engine Land)의 관련 기사는 열리지 않았습니다.
- Vayo 보도자료는 PR Newswire 원문이 아니라 finviz 전재본으로 읽었습니다(원문 주소 표기 있음). 공급사 목록·직접 연동 범위(Booking.com·OpenTable·SeatGeek)는 Skift 보도이고 보도자료에는 없습니다. 예약 건수·결제창을 넘긴 비율·Vayo 요금은 공개되지 않았습니다. 「1억 달러」는 PhocusWire·Skift 두 매체이고 보도자료에는 없으며 조건(제품 진전·시장 상황)은 PhocusWire 표현입니다. Skift Research의 27%·21%·6%는 Skift 자체 조사이고 표본은 기사에 없습니다.
- 세이버 보도자료도 finviz 전재본입니다. 「80곳 이상」은 시범·운영 구분 없는 회사 수치입니다. 「ChatGPT·Claude·Gemini로 2027년 확장」·「수익 공유」·「경제성 미입증」은 Skift 기사(일부는 요약 블록)이고 보도자료에는 플랫폼 이름이 Grok 외에 없습니다. 「SpaceXSI」가 보도자료 인용문에 나오는데 그 역할은 설명이 없어 적지 않았습니다. 세이버 IR 사이트에서 연 보도자료는 2025년 9월 것이어서 이번 발표 확인에는 쓰지 않았습니다.
- Skift 칼럼은 앞 다섯 문단만 열렸고, 부킹홀딩스 「1% 훨씬 아래」·윈덤 「15%」·IdeaWorks 1,570억·Expedia 2억 600만·Instinct 답변·유나이티드 이유는 **기사 요약 블록**에서만 읽었습니다(본문 대조 못 함). Citizens 보고의 방법·표본은 확인하지 못했습니다. MCR CEO 발언은 Skift 전언입니다.
- 구글 기록 이전 글은 지원 제공사·한도·요금제가 없고, Tool Retrieval 글은 절감 수치가 없습니다(회사가 「측정하라」고 적음).
- 어느 회사의 발표도 우리가 직접 시험한 것은 없습니다. 우리 「문 표」는 이번 주에 시작하는 것이고, 결제 페이지 걸어 보기 결과는 다음 글에 적습니다.

## 함께 읽은 글

성격이 다른 출처를 직접 열어 확인했습니다. 회사 발표·공식 문서, 매체 보도·칼럼, 우리 이전 글을 나눠 적습니다.

회사 발표·공식 문서:

- [Get your year-end tasks done with new Connected Apps (Google, 11월 20일)](https://blog.google/products-and-platforms/products/search/connected-apps-holiday-errands/) — 영문, Albertsons·Safeway·Shaw's·Target 장보기 결제·UCP·Experian·H&R Block·Angi·Thumbtack·수치 없음
- [Build and manage Connected Apps in one place (Google, 10월 28일)](https://blog.google/innovation-and-ai/technology/developers-tools/connected-apps-one-place/) — 영문, Connected Apps Platform 미리보기·MCP 서버/Android MCP·Connected Console·50개 이상
- [How to transfer your chat history into Gemini (Google, 11월 19일)](https://blog.google/innovation-and-ai/products/gemini-app/switch-ai-assistants-transfer-history/) — 영문, 5단계·ZIP 가져오기
- [Introducing Tool Retrieval in the Gemini API (Google, 11월 19일)](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/) — 영문, tool_search·defer_loading·원격 MCP 지연 로드·별도 과금 없음·절감 수치 없음
- [How Target is Shaping Shopping Experiences in Conversational AI (Target, 6월 18일 갱신)](https://corporate.target.com/press/fact-sheet/2026/06/conversational-ai) — 영문, 세 플랫폼 결제·UCP·Buy→로그인→확인·Google Pay·「다품목 결제 준비 중」·AI 트래픽 2,000%(회사)
- [Booking Holdings' Vayo Now Books the Entire Trip (Vayo 보도자료, 11월 17일 — PR Newswire, finviz 전재)](https://finviz.com/news/424035/booking-holdings-vayo-now-books-the-entire-trip) — 영문, 연동/탐색/결제 넘김·승인·공급사 확정·1Password for Agents·Stripe Link·Genius Level 3 최대 20%·비공개 베타
- [Sabre Accelerates Agentic Travel Leadership with First-Mover Travel Experience within Grok Bot and Next-Gen Proactive Travel APIs (Sabre 보도자료, 11월 16일 — PR Newswire, finviz 전재)](https://finviz.com/news/423683/sabre-accelerates-agentic-travel-leadership-with-first-mover-travel-experience-within-grok-bot-and-next-gen-proactive-travel-apis) — 영문, Mosaic Travel Connector 베타·Grok Bot 첫 플러그인·MCP 파트너 80곳 이상·이벤트 구동 API·2027 확장·요금 없음

매체 보도·칼럼:

- [Booking Holdings' AI Agent Vayo Can Now Reserve Flights and Hotels (Skift, 11월 17일)](https://skift.com/2026/11/17/booking-holdings-ai-agent-vayo-can-now-reserve-flights-and-hotels/) — 영문, 직접 연동 Booking.com·OpenTable·SeatGeek·Skift Research 27%/21%/6%·Genius 가격의 비교 영향
- [AI agent Vayo adds travel booking (PhocusWire, 11월)](https://www.phocuswire.com/news/startups/ai-agent-vayo-adds-travel-booking) — 영문, 1억 달러 투자 조건·Lola·CEO 「유나이티드처럼 허용하지 않는 곳은 결제창을 넘긴다」
- [Sabre Wants to Be the Transaction Engine Behind AI Travel Bookings (Skift, 11월 19일)](https://skift.com/2026/11/19/sabre-wants-to-be-the-transaction-engine-behind-ai-travel-bookings/) — 영문, CEO 「한 개·두 개·세 개」·ChatGPT·Claude·Gemini 2027·수익 공유(요약 블록)·경제성 미입증
- [Sabre brings conversational travel booking to Grok (PhocusWire, 11월)](https://www.phocuswire.com/sabre-brings-conversational-travel-booking-grok) — 영문, 투자자 데이 11/17·CEO 「LLM 플랫폼은 아직 기업 쪽」
- [The AI Agent Is Travel's Ad Blocker (Skift, 라파트 알리 칼럼, 11월 18일 — 앞부분만 무료)](https://skift.com/2026/11/18/the-ai-agent-is-travels-ad-blocker/) — 영문, 충동구매·MCR CEO·Citizens 11/15·부킹 「1% 훨씬 아래」·윈덤 15%(요약 블록)
- [Google Brings Third-Party Apps Into Search AI Mode for Everyday Tasks (eWeek, 7월 17일)](https://eweek.com/news/google-ai-mode-connected-apps) — 영문, 7월 1차 Connected Apps(Instacart·Canva·YouTube Music)·미국·옵트인

우리 이전 글:

- [주간 AI 소식 — 값은 내리고 한계는 적고, 에이전트는 데스크톱과 장바구니에 (AP News NO.53)](https://www.apholdings.kr/ko/news/weekly-2026-11-21/)
- [「해도 되는 일」을 에이전트가 오기 전에 적어 두는 세 문서 (AP News NO.50)](https://www.apholdings.kr/ko/news/allowed-list-before-the-agent-arrives/)
- [모델을 바꾸는 데 몇 주가 걸린다 (AP News NO.48)](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [주간 AI 소식 — 구글은 닷새 동안 모델 셋과 검색을 바꿨고, OpenAI는 에이전트에게 지갑을 쥐여 줬고, 유나이티드는 「손님의 에이전트」를 문 밖에 세웠다 (AP News NO.47)](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [손님의 에이전트는 막고, 가게는 들이고, 모델은 모두에게 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [손님은 자기 에이전트를 데려오지 못한다 (AP News NO.43)](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [점수표에 확률이 붙었다 — 우버는 가장 바쁜 주에 에이전트가 잡은 호출이 4건이라고 셌다 (AP News NO.40)](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [AI가 손님을 데려오는 현관이 셋이 됐다 (AP News NO.38)](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
- [확인 코드가 에이전트 손에 닿으면 (AP News NO.36)](https://www.apholdings.kr/ko/news/agents-raised-their-own-spending-caps/)
