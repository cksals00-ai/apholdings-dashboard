---
no: 37
slug: one-robots-line-against-ai-training
date: 2026-11-03
category: 실전
tags: robots.txt · AI 학습 거부 · IETF AI 선호 · 구글 · 마이크로소프트 빙 · OpenAI · 앤트로픽 · 사이트 운영
title: robots.txt 한 줄로 「AI 학습에 쓰지 말라」 — 구글·마이크로소프트·OpenAI·앤트로픽이 같은 토큰을 받기로 했고, 빙은 「학습」과 「답변 인용」을 갈랐다. 우리 사이트가 이번 주에 정할 세 가지
summary: 10월 30일 네 회사가 같은 날 같은 약속을 했습니다. 사이트 운영자가 robots.txt에 「__usage_ai-training」이라는 공통 이름 한 줄을 적으면, 구글·마이크로소프트·OpenAI·앤트로픽이 그 사이트의 글을 생성형 AI 학습에 쓰지 말라는 뜻으로 읽겠다는 것입니다. 지금까지는 회사마다 다른 크롤러 이름을 하나씩 막아야 했습니다. 같은 날 마이크로소프트 빙은 한 걸음 더 가서 「학습에 쓰는 것」과 「AI 답변을 만들 때 인용하는 것」을 갈라 따로 고르게 했고, 2027년 2월 1일부터 적용한다고 했습니다. 다만 이 한 줄은 잠금장치가 아니라 선언이고, 아직 표준도 아닙니다. 우리 홈페이지의 robots.txt를 직접 열어 보니 이 선호를 아무것도 표현하지 않은 상태였습니다. 사이트를 운영하는 작은 팀이 이번 주에 정할 세 가지를 적었습니다. 끝에 같은 날 나온 앤트로픽의 상장 서류 수정본을 짧게 붙였습니다.
---
> 이 글은 AI(Claude)와 함께 작성했고 편집자가 검수했습니다. 첫 소식의 표준 초안을 쓴 사람은 Claude를 만든 앤트로픽 소속이고, 앤트로픽은 약속한 네 회사 가운데 하나입니다. 끝의 「짧게」는 앤트로픽의 상장 서류를 다룹니다. 우리 회사는 앤트로픽과 OpenAI의 유료 고객입니다. 회사 문서의 표현은 「회사 문서가 적은 것」으로 옮겼고, 출처가 한 곳뿐인 내용은 그 출처를 함께 적었습니다. 특정 기업에 대한 투자 의견이 아니며 투자 판단 자료가 아닙니다.

사이트를 운영하는 팀은 지난 3년 동안 「우리 글이 AI 학습에 쓰이는 것을 막으려면 어디에 무엇을 적어야 하나」를 회사별로 따로 찾아야 했습니다. 구글은 Google-Extended, OpenAI는 GPTBot, 앤트로픽은 ClaudeBot, 애플은 Applebot-Extended. 이름이 다르고, 막는 범위도 달랐습니다. NO.28에서 상업 검색의 88%에 AI 요약이 뜬다는 조사를, NO.25에서 웹 점유율이 세지 않는 것을 썼습니다. 이번 주 소식은 그 반대편, **「내 글을 AI가 어떻게 써도 되는지」를 사이트 쪽에서 적는 방법**이 처음으로 한 줄로 모였다는 것입니다. 다만 한 줄이 생긴 것과 그 한 줄이 지켜지는 것은 다른 문제여서, 사실과 한계를 나눠 적습니다.

## 1. 네 회사가 같은 토큰을 받기로 했다 — IETF 초안 「__usage_ai-training」 (사실)

10월 30일, 앤트로픽의 표준 담당 기술 책임자 케빈 켈리가 IETF에 **「기계가 읽는 학습 선호 신호(Machine-Readable Training Preference Signal)」** 초안을 올렸습니다. 문서 번호는 draft-kelley-aipref-training-preference-signal-00이고, 2027년 5월 3일에 만료되는 **개인 초안**입니다. 문서 머리에 「IETF가 승인한 것이 아니고 공식 지위가 없다」고 적혀 있습니다. 초안이 정하는 것은 하나입니다. robots.txt의 User-Agent 그룹 이름 자리에 쓰는 **정책 토큰 `__usage_ai-training`**입니다. 이 그룹 아래에 Disallow를 적으면 「그 경로의 콘텐츠를 AI 학습에 쓰지 말아 달라」는 선호, Allow를 적으면 「써도 된다」는 선호가 됩니다. 「학습」의 뜻은 IETF AI 선호 작업반의 용어 초안을 따라 **「생성형 AI 모델의 학습된 파라미터를 바꾸는 데 자산을 쓰는 것」**입니다.

같은 날 네 회사가 이 토큰을 지키겠다고 밝혔습니다. 우리가 직접 확인한 것은 세 곳입니다. **마이크로소프트**는 빙 블로그에 「업계 동료들과 함께 robots.txt의 공통 AI 학습 선호를 발표한다」고 적고 **2027년 2월 1일**부터 적용한다고 했습니다. **구글**은 검색 센트럴 블로그에 「IETF에서 검토 중인 제안을 자발적으로 채택할 계획」이라며 「여러 AI 제공자에 대한 학습 선호를 한 번에 표현할 수 있게 된다」고 적었고(본문은 우리 fetch에 목차만 보여 Search Engine Roundtable·PPC Land가 옮긴 문장으로 확인), 크롤러 문서의 Google-Extended 항목에 **「2027년 초」** 지원 예정이라는 주석을 달았습니다. **앤트로픽**은 초안 저자가 IETF 메일링 리스트에 「이미 지원 구현을 시작했다」고 알렸는데, 어느 크롤러에 언제 적용되는지는 적지 않았고 「몇 달 걸릴 것」「기존 크롤러 제어를 대체하지 않고 보완한다」「해석은 바뀔 수 있다」는 단서를 달았습니다. **OpenAI**의 공식 글은 우리 fetch가 차단돼 열지 못했고, Engadget은 「몇 달 안에」 구현하겠다고 했다고 전했으며 PPC Land는 「시점은 없었다」고 적었습니다.

초안에는 운영자가 알아야 할 규칙이 몇 가지 더 있습니다. 첫째, **이 토큰은 크롤링 지시가 아닙니다.** 「콘텐츠 사용 선호와 크롤러 통행 규칙은 서로 독립」이라고 적혀 있습니다. 둘째, **`User-Agent: *` 와일드카드는 이 토큰에 적용되지 않습니다.** 토큰 이름을 직접 쓴 그룹만 선호로 읽습니다. 셋째, 구체적 표현이 일반 표현보다 우선하고, 「사적 계약이 이 선호를 덮어쓸 수 있다」고 적혀 있습니다. 넷째, 선호는 「자산을 가져온 시점의 robots.txt」 기준입니다. Engadget은 이 점을 「이미 수집된 것은 되돌리지 못한다」고 풀었고, 「크롤링 자체나 구글 검색 노출을 막는 것은 아니다」라고도 적었습니다.

구글의 해석은 구글 검색 담당 존 뮬러가 설명했습니다(Search Engine Roundtable·PPC Land). 사이트가 Google-Extended를 따로 적지 않고 **공통 토큰만 막으면 「Google-Extended를 막은 것처럼」 해석**한다는 것입니다. 구글 크롤러 문서에 따르면 Google-Extended는 자체 크롤러가 아니라 「제어 역할」만 하는 토큰이고, **Gemini 모델 학습**과 **Gemini 앱·Vertex AI의 그라운딩**(답변 시점에 검색 색인의 내용을 모델에 주는 것)을 함께 제어하며, **구글 검색 포함 여부나 순위에는 영향이 없다**고 적혀 있습니다. 구글 쪽 반론도 매체에 함께 나왔습니다. 구글의 게리 일리스는 robots.txt가 「제안이지 보안 통제가 아니다」라며 「누구든 30초면 Googlebot을 사칭할 수 있다」고 했고(PPC Land가 옮긴 팟캐스트 발언), IETF 참가자 네이트 헤이크는 「IETF 차원에선 아직 끝난 것이 아니고 큰 쟁점이 남아 있다」, 「초안이 사용자가 하는 행위를 사실상 예외로 둔다」고 했습니다(Search Engine Roundtable).

## 2. 빙은 「학습」과 「답변 인용」을 갈랐다 — 세 가지 설정과 네 개의 날짜 (사실)

같은 10월 30일, 마이크로소프트 빙은 공통 토큰 지원에 더해 자체 설정을 내놓았습니다(크리슈나 마다반, 빙 블로그). 핵심은 **두 가지 쓰임을 가른 것**입니다. 회사 문서의 정의로 **「학습(training)」은 생성형 AI 모델의 학습된 파라미터를 바꾸는 사용**, **「그라운딩(grounding)」은 AI가 답을 만들 때 참고 자료로 콘텐츠를 넣는 사용**입니다. 문서는 전통적인 색인·순위는 그라운딩이 아니라고 적습니다.

설정은 이렇습니다. **학습**은 Allow/Disallow 두 값이고, 사이트 전체는 robots.txt의 `__usage_ai-training` 그룹으로, 페이지 단위는 `<meta name="Bingbot" content="ai-training:disallow">` 또는 같은 내용의 X-Robots-Tag 헤더로 적습니다. 페이지 단위가 robots.txt보다 우선합니다. **그라운딩**은 Allow / DisallowExtended / Disallow 세 값이고, **페이지 단위(meta·헤더)로만** 적습니다. 사이트 전체용 robots.txt 설정은 없습니다. DisallowExtended는 마이크로소프트가 직접 운영하는 경험(AI 모드·AI 오버뷰·코파일럿·마이크로소프트 365)에서만 인용을 허용하고, 제3자에게 파는 그라운딩 서비스에서는 막는 값입니다. **아무것도 적지 않으면 둘 다 Allow**입니다. 회사 문서는 이 선호가 「전통적인 빙 검색 결과 자격을 바꾸지 않는다」고 적으면서, 동시에 그라운딩을 Disallow나 DisallowExtended로 두면 「AI가 만든 경험에서의 노출이 크게 줄어든다」고 적었습니다. 어느 쪽을 골라도 노출·트래픽·대가를 보장하지 않는다는 문장도 있습니다.

날짜는 네 개입니다. **2026년 12월 15일** 빙 웹마스터 도구에 임시 그라운딩 설정이 열립니다(그날 기준으로 NoArchive·NoCache를 쓰는 사이트만). **2027년 2월 1일** 새 선호가 크롤링되는 대로 적용됩니다. **2027년 3월 1일**이 지나면 2023년부터 쓰던 NoArchive·NoCache를 더는 학습·그라운딩 선호로 읽지 않습니다. **2027년 9월 30일** 임시 그라운딩 설정이 끝납니다. 문서는 IndexNow로 재크롤링을 요청할 수 있지만 날짜를 보장하지는 않는다고 덧붙였습니다.

## 짧게 — 앤트로픽 상장 서류 수정본 (사실)

11월 2일 앤트로픽은 S-1 수정본에 3분기 숫자를 넣었습니다. 우리는 EDGAR 원문이 이번엔 fetch 차단으로 열리지 않아 **매체 네 곳(포천·비즈니스 인사이더·SiliconANGLE·Investing.com)이 서류를 인용한 수치**를 옮깁니다. 3분기(7~9월) 매출 약 **170억 달러**(2분기 116억, 전년 같은 분기 14억 — 포천), 영업비용 175억, **영업손실 5억 6,700만 달러**(2분기는 영업이익 9억 7,400만; SiliconANGLE만 5억 3,600만으로 적어 매체 간 차이가 있음), 순손실 233억 달러는 대부분 전환사채 공정가치 변동에 따른 회계 비용입니다. 영업손실의 주된 이유로 서류가 적은 것은 **「단기 약정으로 산 컴퓨팅 50억 달러」**(비즈니스 인사이더·SiliconANGLE)와 임직원 기부 매칭 프로그램의 비현금 비용 20억 달러입니다. 2분기에서 3분기 사이 **가격 인하로 매출이 약 6억 달러 줄었다**는 문장은 포천 한 곳이 전했습니다. 컴퓨팅·인프라 구매·리스 약정 합계는 **8,954억 달러**(네 곳 일치)이고, 그중 2030년까지 4,475억·12개월 안 698억은 Investing.com 한 곳의 정리입니다. NO.30에서 「쓰는 값은 반으로, 만드는 비용은 달마다 수십억」이라고 썼는데, 이번 서류는 그 둘이 같은 분기에 한 회사 안에서 만났다는 것을 보여 줍니다(해석). 투자 판단 자료가 아니며, 공모 규모·가격·시점은 적지 않습니다. 원문을 직접 읽은 뒤 「값과 비용」 후속으로 다시 다루겠습니다.

## 두 소식을 함께 읽으면 (해석)

첫째, **한 줄은 잠금장치가 아니라 선언입니다.** 초안 스스로 「크롤링 지시가 아니다」라고 적고, 구글 직원은 「30초면 사칭」이라고 말합니다. 이 한 줄이 하는 일은 「우리 글을 학습에 쓰지 말아 달라」는 뜻을 네 회사가 같은 방식으로 읽게 하는 것까지입니다. 지키는지는 각 회사의 약속에 달려 있고, 지켰는지 사이트 쪽에서 확인할 방법은 지금 없습니다. 그래도 지난 3년처럼 회사별 이름을 따로 찾는 일은 줄어듭니다. 특히 작은 팀에는 **「새 AI 회사가 나타날 때마다 robots.txt를 고치는 일」이 「토큰 하나를 그 회사가 받는지 확인하는 일」로 바뀌는 것**이 실질적인 변화입니다(해석).

둘째, **학습과 인용은 다른 질문입니다.** 빙만 둘을 갈랐고, 공통 토큰은 학습만 다룹니다. 구글은 토큰을 Google-Extended 차단으로 해석하는데, 구글 문서에 따르면 Google-Extended는 학습뿐 아니라 Gemini 앱·Vertex의 그라운딩도 함께 제어합니다. 그러면 공통 토큰 하나로 「학습은 거부, Gemini 답변 인용은 허용」을 구글에서 어떻게 표현하는지가 비어 있습니다. 우리는 이 부분을 구글 문서에서 확인하지 못했고, 구글이 2027년 지원을 시작할 때 채워질 질문으로 둡니다. 빙이 「인용을 막으면 AI 경험 노출이 크게 줄어든다」고 적은 것은 솔직한 문장이고, NO.28에서 본 「상업 검색의 88%에 AI 요약」과 같은 방향입니다. **학습을 거부하는 것과 인용을 거부하는 것은 사이트에 다른 비용**이 듭니다(해석).

셋째, **「사람이 시킨 행위」는 바깥에 있습니다.** 헤이크의 지적대로 초안은 사용자가 직접 요청해 가져오는 것을 사실상 예외로 두고, 켈리의 메일도 「해석은 바뀔 수 있다」고 적습니다. 우리 글이 AI 챗에서 누군가의 질문에 답하며 읽히는 일은 이 토큰과 별개로 계속됩니다. 이것을 막을지는 다른 결정이고, 우리는 막지 않는 쪽입니다. AP News는 읽히기 위해 쓰는 글이기 때문입니다(해석).

## 우리라면 — 이번 주에 정할 세 가지 (실전)

1. **콘텐츠를 세 묶음으로 나눠 「학습/인용」 두 칸을 채운다.** 우리 홈페이지 robots.txt를 직접 열어 보니 `User-agent: *` 한 그룹에 Allow와 폴더 Disallow(소스·스크립트·백업·문서, 검수 전 네 어권)만 있고, AI 토큰은 하나도 없었습니다. 초안 규칙상 `*`는 토큰에 적용되지 않으니 **우리는 지금 아무 선호도 표현하지 않은 상태**이고, 빙 기준으로는 둘 다 Allow입니다. 그래서 먼저 결정표를 만듭니다. ①AP News·제품 소개·회사 소개는 「학습 허용·인용 허용」 — 읽히기 위해 쓰는 글이라 그렇습니다. ②소스·스크립트·백업·내부 문서 폴더는 이미 크롤링을 막고 있는데, 이것은 통행 규칙이고 학습 선호는 아니니 토큰 그룹에도 같은 경로를 Disallow로 적어 둡니다. ③이용자 글이 섞이는 페이지(후기·게시판·문의)는 「학습 거부」로 적고, 인용은 빙에서 DisallowExtended로 둡니다. 결정표는 NO.29의 권한 표 옆에 두고, 분기마다 다시 봅니다.
2. **적을 때는 토큰 그룹을 따로, 회사별 이름도 그대로 둔다.** 초안·구글·앤트로픽 모두 「기존 제어는 계속 작동한다」고 했으니 `__usage_ai-training` 그룹을 **추가**하고 Google-Extended·GPTBot·ClaudeBot 같은 기존 그룹은 지우지 않습니다. `*`에 적은 것이 토큰에 적용된다고 기대하지 않습니다. 빙의 그라운딩 선호는 robots.txt에 없고 페이지 단위 meta·헤더만 되니, ③묶음 페이지 템플릿에만 넣습니다. 달력에는 **2027년 2월 1일**(빙 적용)과 **3월 1일**(NoArchive·NoCache를 더는 선호로 읽지 않음)을 적고, 2월 첫 주에 구글·OpenAI가 실제로 지원을 시작했는지 각 회사 문서를 다시 열어 봅니다. 공식 문서를 못 열면 매체 두 곳 교차로 확인합니다.
3. **「적었다」와 「지켜졌다」를 다른 칸에 둔다.** 이 토큰은 지켜졌는지를 사이트 쪽에서 알 방법이 없습니다. 그래서 할 수 있는 것만 합니다. 서버 로그에서 AI 크롤러 이름(GPTBot·ClaudeBot·Bingbot 등)의 방문을 **월 1회** 집계하고, Google-Extended는 자체 크롤러 이름이 없어 로그에 안 잡힌다는 점을 표에 적어 둡니다. 구글 서치 콘솔의 AI 성과 보고에 클릭 데이터가 안 들어올 수 있다는 이야기(일리스 발언, Search Engine Roundtable 11월 2일 요약 한 곳)는 단서를 붙여 참고만 합니다. 3개월 뒤 각 회사 문서에서 「학습」의 정의가 바뀌었는지 다시 확인합니다. 선호를 적었다는 사실을 「AI가 우리 글을 안 쓴다」로 보고하지 않습니다.

## 이번에 고르지 않은 것

레딧 CEO가 구글 검색 트래픽 감소를 확인했다는 보도(11월 2일, Search Engine Roundtable)는 발언 원문과 실적 콜 자료를 열지 못해 다음으로 미뤘습니다. SemiAnalysis가 11월 2일 낸 에이전트 벤치마크 GDPx(11개 영역, 최고 모델도 12%, 금융·법률은 이진 채점에서 전부 0)는 앤트로픽 모델이 1위로 나와 이해관계가 크고 다른 매체 교차가 아직 적어, NO.33·34의 「점수표가 재는 것」 후속으로 따로 다룹니다. 알파벳의 60억 유로 채권·오라클의 200억 달러 조달(TNW가 로이터를 인용)은 「짧게」의 약정 숫자와 같은 계열이지만 투자 판단 자료로 읽힐 수 있어 「값과 비용」 후속에서 함께 봅니다. OpenAI가 데이터센터를 「컴퓨트 캠퍼스」로 부르겠다는 보도(Axios·비즈니스 인사이더)는 본문을 열지 않았습니다. 유출·소문으로 돌던 모델 이야기와 커널 결함 익스플로잇 이야기는 공식 확인이 없거나 공격 서술이어서 쓰지 않습니다.

## 이 소식에서 확인하지 못한 것

- OpenAI의 공식 글(「Helping websites express AI training preferences」)은 fetch 차단으로 열지 못했습니다. 「몇 달 안」은 Engadget 한 곳의 전언이고 PPC Land는 시점이 없었다고 적었습니다. GPTBot 등 어느 크롤러가 토큰을 읽을지도 확인하지 못했습니다.
- 구글 검색 센트럴 블로그 본문은 우리 fetch에 목차만 보여 매체 두 곳이 옮긴 문장으로 확인했습니다. 공통 토큰만 막았을 때 Gemini 앱 그라운딩까지 막히는지는 구글 문서에서 찾지 못했습니다.
- 앤트로픽의 「이미 구현 시작」은 저자 메일 한 통이고, 적용 크롤러·시점은 없습니다. 앤트로픽 공식 문서(크롤러 안내)에 반영됐는지는 확인하지 않았습니다.
- 빙 문서의 날짜·설정은 직접 확인했지만, 「전통 검색 자격을 바꾸지 않는다」는 회사의 말이고 독립 검증은 없습니다.
- 「짧게」의 수치는 전부 매체가 서류를 인용한 것입니다. 영업손실(5.67억 vs 5.36억)은 매체 간 차이가 있고, 가격 인하 6억·2030년까지 4,475억·12개월 698억·컴퓨팅 비용 99억은 각각 한 곳입니다. EDGAR 원문이 열리면 대조합니다.

## 함께 읽은 글

성격이 다른 출처를 직접 열어 확인했습니다. 표준 문서, 회사 공식 문서·발언, 매체 보도를 나눠 적습니다.

표준 문서:

- [Machine-Readable Training Preference Signal, draft-kelley-aipref-training-preference-signal-00 (IETF Datatracker)](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/) — 영문, 토큰 정의·「크롤링 지시 아님」·와일드카드 규칙·사적 계약 조항

회사 공식 문서·발언:

- [Your content, your choice: clearer preferences for training and grounding (Microsoft Bing 블로그)](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/) — 영문, 학습·그라운딩 정의, 세 설정, 구문, 날짜 네 개
- [Supporting a shared AI training control for websites (Google Search Central 블로그)](https://developers.google.com/search/blog/2026/10/ai-training-control) — 영문, 구글의 채택 선언(본문은 매체 인용으로 확인)
- [Google의 공통 크롤러 문서 — Google-Extended 항목 (Google 개발자 문서)](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended) — 영문, Google-Extended의 범위(학습·그라운딩), 검색 순위 무관, 「2027년 초」 지원 주석
- [케빈 켈리의 IETF ai-control 메일 — 앤트로픽 지원 구현 시작 (IETF Mail Archive)](https://mailarchive.ietf.org/arch/msg/ai-control/mddjatOxSR0h6GmLRBWlc839c7w/) — 영문, 「이미 시작」·「몇 달」·「보완」·「해석은 바뀔 수 있음」

매체 보도:

- [Google joins OpenAI and Anthropic in promising new scraping controls (Engadget)](https://www.engadget.com/2303225/google-openai-anthropic-ai-crawling-controls/) — 영문, 네 회사 약속과 시점, 「과거 수집은 되돌리지 못함」
- [Google and Bing back one robots.txt rule to opt out of AI training (PPC Land)](https://ppc.land/google-and-bing-back-one-robots-txt-rule-to-opt-out-of-ai-training/) — 영문, 뮬러·일리스·헤이크 발언, 회사별 기존 크롤러 이름
- [Google Also Adopts New AI Training Control (Search Engine Roundtable)](https://www.seroundtable.com/google-ai-training-control-42430.html) — 영문, 구글 문장 인용, 뮬러의 Google-Extended 해석, 헤이크의 「사용자 행위 예외」 지적
- [Anthropic's growth slowed and costs jumped in the third quarter, updated IPO filing shows (Fortune)](https://fortune.com/2026/11/02/anthropics-growth-slowed-and-costs-jumped-in-the-third-quarter-updated-ipo-filing-shows/) — 영문, 「짧게」의 매출·영업손실·유동성·가격 인하(한 곳)
- [Anthropic's amended IPO paperwork reveals soaring Q3 revenue and a stunning compute bill (Business Insider, 야후 파이낸스 재게시)](https://uk.finance.yahoo.com/news/anthropics-amended-ipo-paperwork-reveals-153730799.html) — 영문, 「단기 약정 컴퓨팅 50억」 서류 인용, 컴퓨팅 비용 99억(한 곳)
- [Anthropic's quarterly revenue jumps to $17B, losses grow ahead of IPO (SiliconANGLE)](https://siliconangle.com/2026/11/02/anthropics-quarterly-revenue-jumps-to-17b-losses-grow-ahead-of-ipo/) — 영문, 영업손실 표기 차이(5.36억), 단기 컴퓨팅 50억
- [Anthropic posts $17B third-quarter revenue as landmark AI debut nears (Investing.com)](https://www.investing.com/news/stock-market-news/anthropic-posts-17b-thirdquarter-revenue-as-landmark-ai-debut-nears-4992371) — 영문, 영업비용 175억, 약정의 연도별 분포(한 곳)

우리 이전 글:

- [AI가 광고 문구를 대신 고쳐 쓰기 시작한다 — 상업 검색의 88%에는 AI 요약이 뜬다 (AP News NO.28)](https://www.apholdings.kr/ko/news/ai-rewrites-your-ads-what-to-check/)
- [ChatGPT 웹 점유율이 다시 올랐다 — 이 숫자가 세지 않는 것 (AP News NO.25)](https://www.apholdings.kr/ko/news/chatgpt-share-rebound-what-web-misses/)
- [에이전트는 「믿을 수 없는 내부자」다 — 「권한 0에서 시작」 제안 (AP News NO.29)](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
- [쓰는 값은 반으로, 만드는 비용은 달마다 수십억 달러 — 앤트로픽은 S-1에 컴퓨팅 비용을 적었다 (AP News NO.30)](https://www.apholdings.kr/ko/news/half-price-terra-and-the-s1-compute-bill/)
