---
no: 46
slug: hydrogen-daily-driver-price-per-task
date: 2026-11-13
category: 인사이트
tags: Gemini 4 Hydrogen · 구글 · 모델 가격 · Artificial Analysis · 에폭 AI · 추론 비용 · 모델 선택 · AlphaProof Code
title: 「매일 쓰는 모델」 칸이 생겼다 — 구글은 Gemini 4 Hydrogen을 Flash 두 배 값에 냈고, 독립 평가는 「Argon보다 1점 위, 과제당 1.87달러」로 쟀고, 에폭은 칩 한 개가 동시에 받는 요청 수를 셌다
summary: 11월 12일 구글은 Gemini 4 Hydrogen을 냈습니다. 「Carbon과 Argon은 깊이 생각하고, Hydrogen은 매일의 일을 빨리 끝낸다」는 자리이고, 값은 백만 토큰당 입력 1.50달러·출력 7.50달러로 Gemini 3.8 Flash의 두 배입니다(Flash도 2027년 1월 1일에 같은 값이 된다고 VentureBeat는 정리했습니다). API·앱·검색에 한꺼번에 들어갔고, 무료 이용자에게도 자동 선택으로 갑니다. 독립 평가 기관 Artificial Analysis는 기본 설정에서 지능 지수 51(Argon 50), 과제당 비용 1.87달러로 쟀습니다. 에폭 AI는 11월 9일 「추론 성능 지수」를 내 칩 한 개가 동시에 받을 수 있는 요청 수를 셌고, 최신 칩이 FLOP/s로는 2.5배인데 이 셈법으로는 25배라고 적었습니다. 셋을 「토큰 값이 아니라 과제 값으로 읽는 법」으로 묶고, 끝에 「짧게」로 구글 딥마인드가 Signal 프로토콜 코드를 4주 만에 형식 검증했다는 발표를 적었습니다.
---
> 이 글은 AI(Claude)와 함께 작성했고 편집자가 검수했습니다. 우리 회사는 앤트로픽과 OpenAI 두 회사의 유료 고객이고 구글 모델도 시험에 씁니다. 1번과 「짧게」는 구글의 발표이고, 구글은 글을 쓴 AI의 제조사(앤트로픽)와 경쟁합니다. 2번의 독립 평가 순위표 맨 위에 앤트로픽 모델이 있어 **평가는 보태지 않고 숫자만 옮겼습니다.** 회사가 발표한 수치는 「회사가 발표한 것」으로 표시했고, 이 글은 특정 기업에 대한 투자 의견이 아닙니다.

NO.45에서 「모델의 문은 일부에게 먼저 열리고, 두 달 뒤 값이 두 배가 된다」고 적었습니다. 그때 구글의 발표 글은 「대부분의 소프트웨어·지식 작업은 Argon으로」라고 했습니다. 이틀 뒤 구글은 그 아래 칸을 하나 더 만들었습니다. **「매일 쓰는 모델」** 칸입니다. 이번 글은 그 칸의 값을 세 가지 셈법 — 회사가 붙인 토큰 값, 독립 기관이 잰 과제 값, 그리고 그 값의 바닥에 있는 칩의 용량 — 으로 읽습니다. 사실·해석·우리라면으로 나눠 적습니다.

## 1. 구글 — Gemini 4 Hydrogen, 「Carbon과 Argon은 깊이 생각하고, Hydrogen은 매일의 일을 빨리」 (사실)

구글은 11월 12일(목) **Gemini 4 Hydrogen**을 냈습니다(회사 발표, 글쓴이는 구글 딥마인드의 코라이 카부크추올루). 발표 글의 자리매김은 한 문장입니다 — **「Carbon과 Argon은 깊이 생각하고, Hydrogen은 매일의 일을 빨리 끝낸다.」** 코딩으로 치면 설계 판단은 Carbon·Argon이, 코드를 쓰고 테스트를 돌리고 바뀐 것을 확인하는 일은 Hydrogen이 맡는 그림이고, Antigravity 안에서는 **Orchestrator**가 한 세션 안에서 Carbon과 Hydrogen을 오가며 씁니다. 파라미터 수는 적혀 있지 않습니다. 생각하는 단계는 low·medium·high(기본)에 **xhigh**가 새로 붙어 넷이고, 문맥은 입력 100만 토큰에 출력도 100만 토큰까지입니다.

값은 **백만 토큰당 입력 1.50달러·출력 7.50달러**이고 100만 토큰 문맥 전체에 같은 값입니다. 들어간 곳은 한꺼번에 넓습니다. Gemini API와 Google AI Studio(모든 등급), Android Studio(유료), Antigravity(Google AI Pro·Ultra 구독자), Gemini for business, Gemini 앱의 모델 선택 — 그리고 **무료 이용자에게는 자동 모델 선택으로**, **구글 검색에는 전 세계 모든 이용자에게** 들어갑니다. Google Sheets의 Gemini에는 Pro·Ultra 구독자부터입니다.

회사가 발표한 숫자는 다음과 같습니다. 기본(high) 설정에서 Gemini 3.8 Flash보다 **2.5배 빠르게** 과제를 끝내고, Terminal-Bench 4.1은 **57%**(3.8 Flash 18.2%), HLE-Diamond 58.8%, Artificial Analysis 지능 지수 **51(Argon 50), xhigh에서 54**입니다. Antigravity의 Orchestrator(Carbon+Hydrogen)는 Terminal-Bench 4.0에서 Carbon 단독에 가까운 성공률을 **쿼터 24% 적게, 19% 빨리** 냈다고 합니다. 초기 파트너 시험에서 복잡한 그래프·SQL·데이터 작업이 2~2.8배 빨라지고 토큰은 12~23% 줄었다는 것, 지어낸 주장이 3.8 Flash의 1/5 이하라는 것, 에이전트 과제에서 권한을 넘는 행동이 최대 81% 줄고 막힌 과제에서 권한 경계를 우회할 가능성이 절반이라는 것, 간접 프롬프트 주입에 2.3배 강하다는 것도 모두 회사가 발표한 것입니다. 모델 카드는 글에 링크돼 있고 우리는 열지 않았습니다.

회사 표에는 **지는 칸**도 있습니다. The Decoder가 옮긴 표에서 Argon이 Hydrogen을 앞서는 항목은 Chartography(71.6% 대 66.6%)이고, Carbon이 앞서는 항목은 Agents' Last Exam v1.1(77.4% 대 71.6%)과 OSWorld-2.1(81.5% 대 77.6%)입니다. Digital Trends는 같은 표에서 과학·수학, 컴퓨터 사용, Terminal-Bench 4.1에서 Hydrogen이 경쟁 모델에 뒤지지만 격차는 작다고 적었고, VentureBeat는 구글 표의 Terminal-Bench 4.1 칸에 Claude Sonnet 5.5가 63.9%로 적혀 있다고 옮겼습니다(VentureBeat 한 곳). Argon은 생각하는 단계가 medium·high 둘뿐이라, 회사가 「Argon보다 1점 위」라고 한 비교는 Hydrogen의 기본 단계 대 Argon의 기본 단계입니다.

## 2. 값표 — 한 달 사이 바뀐 것, 그리고 독립 기관이 잰 「과제당」 값 (사실)

VentureBeat가 정리한 값표를 우리 이전 글과 맞춰 적습니다(모두 백만 토큰당 입력/출력, 표준 등급). **Hydrogen 1.50/7.50.** Gemini 3.8 Flash는 **12월 31일까지 0.75/3.75, 2027년 1월 1일부터 1.50/7.50** — 즉 Hydrogen의 값은 「Flash 도입가의 두 배」이자 「두 달 뒤 Flash 값과 같음」입니다. Gemini 4 Argon은 도입가 2/10에서 4/20으로, Gemini 4 Carbon은 NO.45에서 적은 대로 **11월 30일까지 2/10, 그 뒤 4/20**입니다. Claude Fable 5.2는 NO.44에서 적은 대로 8/40입니다. 구글의 가격 페이지는 우리 쪽에서 열면 Gemini 3.5 Flash까지만 보이는 구버전이라 Flash의 2027년 인상과 Argon의 전환은 **VentureBeat 한 곳의 정리**로만 확인했습니다(같은 날짜를 적은 개발자 블로그가 여럿 있지만 신뢰 매체로 치지 않았습니다). Hydrogen의 캐시 입력 0.075달러, 배치·플렉스 반값도 같은 글에만 있습니다.

독립 평가 기관 **Artificial Analysis**의 Hydrogen(high) 모델 페이지를 11월 13일에 직접 열었습니다. 지능 지수 v5.0.1에서 **51(78개 모델 가운데 21위)**, **과제당 비용 1.87달러**, 혼합 단가 1.10달러(캐시 7 : 입력 2 : 출력 1 기준), 캐시 할인 95%, 지수를 한 번 돌리는 데 출력 토큰 1억 1,000만 개(같은 급 중앙값 7,280만 개)입니다. 속도·환각 수치는 아직 비어 있습니다. 같은 기관의 순위표 페이지를 열면 **Claude Fable 5.2(max) 65, Gemini 4 Carbon(high) 60, Claude Opus 5.5(max) 59, GPT-6 Astra(max) 57, GPT-6.1 Sol(max) 55, Claude Sonnet 5.5(max) 55**이고, Argon(high)은 50입니다. 우리가 연 순위표 페이지에는 Hydrogen이 아직 없었고, xhigh 54·medium 41·low 27과 단계별 과제당 비용(3.16·0.80·0.29달러), Terminal-Bench 4.0 54%(Sonnet 5.5 max 64%)는 VentureBeat·The Decoder·OfficeChai 세 매체가 같은 숫자를 옮긴 것입니다. 그 가운데 **3.8 Flash(high)가 지수 31에 과제당 7.77달러**라는 숫자는 VentureBeat 한 곳에만 있습니다.

## 3. 에폭 AI — 「추론 성능 지수」, 칩 한 개가 동시에 받는 요청 수 (사실)

에폭 AI는 11월 9일 **추론 성능 지수(Inference Performance Index, IPI)** v1을 냈습니다(글쓴이 제이슨 리, 데이터 11월 6일 갱신). 재는 것은 FLOP/s가 아니라 **「칩 한 개가 요구 출력 속도 50~400토큰/초 범위에서 동시에 받을 수 있는 요청 수」**이고, 엔비디아 GB300 한 개를 1로 둔 상대값입니다. 모델링 조건은 에이전트 작업에 맞췄습니다 — 캐시된 문맥 26만 2,144토큰, 프리필 1,024토큰, 출력 토큰 1개당 새 입력 약 1.51개, 추측 디코딩 3토큰 채택. Kimi K3·GLM-5.2·Qwen3-Coder-480B·MAI-Base-2 대리 모델 넷의 평균입니다.

결과는 이렇습니다. **GB300은 H100의 약 25배**의 추론 용량을 내는데 8비트 FLOP/s로는 2.5배라, FLOP/s만 보면 격차를 약 열 배 작게 본다는 것. 같은 칩이라도 72개를 한 고대역 묶음으로 두는 GB300 NVL72가 8개 묶음의 B300 HGX(0.54)보다 약 1.9배라는 것. H200 HGX 0.12, MI355X 약 0.55, VR200(베라 루빈) 2.18. 그리고 배경 숫자 하나 — **OpenRouter에서 에이전트용 API 키가 쓴 토큰이 사람 키의 약 7배**(9월 말)였다는 것. 한계도 글에 적혀 있습니다. 엔비디아의 시뮬레이터(AISimulate)로 낸 「이론상 최고 속도」 투영이라 실측이 아니고, 소프트웨어 성숙도에 따라 달라지며, 정밀도(FP8·FP4)가 모델 품질을 지키는지는 확인하지 않았고, 평균 방식(산술평균)을 바꾸면 옛 칩의 점수가 크게 내려간다고 합니다. 실측(SemiAnalysis InferenceX)과 비교하면 모델링 값의 50% 가정에서 평균 약 12% 차이였습니다. 글쓴이는 엔비디아에서 LLM 서빙을 하던 사람이고, 이 글에는 자금 출처가 적혀 있지 않습니다(ECI 페이지에는 구글 딥마인드 지원 문장이 있다고 NO.45에서 적었습니다 — 이 글은 다른 글입니다).

## 짧게 — 구글 딥마인드 AlphaProof Code, Signal 프로토콜 코드를 4주 만에 형식 검증 (사실)

구글 딥마인드는 11월 10일 **AlphaProof Code**를 발표했습니다(회사 발표). 사람 전문가가 Signal 메신저 프로토콜의 보안 목표를 형식 명세로 옮기고 검토하면, AI 에이전트가 Lean 언어로 그 증명을 쓰고 스스로 감사하는 구조입니다. 회사가 적은 결과는 — 핵심 암호 코드의 형식 검증을 **4주**에 끝냈고(비슷한 일에 전문가 팀이 몇 년을 썼다고 함), 에이전트가 사람 검토로 넘긴 부분은 코드의 **약 1%**, 이미 고쳐진 버그 2개를 일부러 되살려 넣자 둘 다 「이 버전은 안전하지 않다」는 기계 검증 증명이 나왔다는 것입니다. 증명의 줄 수는 본문이 「600만 줄 이상」, 페이지 메타데이터가 「300만 줄 이상」으로 서로 다릅니다. 산출물은 공개됐고 기술 논문이 링크돼 있지만, 제품이 아니고 출시 일정도 없으며 「확장에는 연구가 더 필요하다」고 적혀 있습니다. 여기까지가 회사의 발표이고, 우리는 논문을 열지 않았습니다.

## 세 가지를 함께 읽으면 (해석)

첫째, **모델 선택표의 「기본 칸」이 바뀌는 속도가 두 달에서 이틀로 줄었습니다.** NO.45의 구글 글은 「대부분은 Argon」이었고, 이번 글은 「매일은 Hydrogen」입니다. 두 말은 모순이 아닙니다 — 회사는 자리를 셋으로 나눴고(Carbon: 어려운 과제, Argon: 대부분의 작업, Hydrogen: 매일의 실행), Orchestrator처럼 **한 과제 안에서 모델을 바꿔 쓰는 것**을 기본으로 깔았습니다(해석). NO.17에서 「작업별로 어떤 AI」를 적었는데, 이제 회사들이 그 표를 자기 모델 안에서 먼저 나눠 줍니다. 표를 받아 적는 게 아니라, 우리 과제가 어느 칸에 들어가는지를 우리가 재야 합니다.

둘째, **토큰 값과 과제 값은 다른 숫자입니다.** Hydrogen의 토큰 값은 Flash의 두 배인데, Artificial Analysis가 잰 과제당 비용은 Hydrogen 1.87달러 대 Flash 7.77달러입니다(Flash 수치는 VentureBeat 한 곳). 싼 모델이 토큰을 더 쓰면 과제는 더 비싸집니다. 반대로 같은 모델의 xhigh는 출력 토큰을 거의 두 배 쓰니 과제당 비용도 거의 두 배(3.16달러)입니다. NO.21에서 「숫자를 비교하기 전에 셈법부터」라고 적었는데, 값표의 셈법은 **「단가 × 그 과제에 실제로 쓴 토큰 수」**입니다(해석). 그리고 2027년 1월 1일 Flash 인상, 12월 1일 Carbon 인상처럼 **값이 바뀌는 날짜**가 표의 일부입니다.

셋째, **값의 바닥에는 칩이 있고, 그 셈법도 FLOP/s가 아닙니다.** 에폭의 지수는 「동시에 몇 개를 받느냐」로 쟀고, 그 기준에서는 세대 차이가 열 배 더 큽니다. 에이전트 키가 사람 키의 7배 토큰을 쓴다는 숫자와 붙여 읽으면, 모델 값이 내려가는 이유의 한 부분은 모델이 아니라 서빙 쪽에 있을 수 있다는 뜻입니다(해석 — 에폭의 값은 모델링이고, 실제 값 인하와의 연결은 에폭도 우리도 재지 않았습니다). 작은 팀이 칩을 고를 일은 없지만, **「값은 더 내려갈 수 있다」를 전제로 표를 짜도 되는지**의 근거로는 읽을 만합니다.

## 우리라면 — 앱·커머스·AI 채널을 운영하는 팀이 이번 주에 할 세 가지 (실전)

1. **NO.45의 Carbon 시험 3건에 Hydrogen을 넣어 네 모델로 돌린다.** NO.17의 우리 시험(성분표 판정·앱 문구·리아 대본 초안)을 Argon(high)·Carbon(high)·Opus 5.5(high)·Hydrogen(high)로 **같은 단계끼리** 돌리고, 결과 옆에 「회사 발표 / 우리가 확인한 것」 두 줄을 적습니다. 이번엔 한 칸을 더 둡니다 — **그 과제에 실제로 쓴 입력·출력 토큰 수.** 세이프리스트의 성분 판정처럼 짧고 반복되는 과제가 「매일 쓰는 모델」 칸에 들어가는지, 리아 대본처럼 긴 과제는 어느 칸인지를 우리 숫자로 정합니다.
2. **단가표에 「과제당 비용」 열을 붙인다.** 모델별 토큰 값 옆에 우리 과제 세 개의 「단가 × 실제 토큰 수」를 적고, 값이 바뀌는 날짜(Carbon 12월 1일, Flash 2027년 1월 1일)를 표 머리에 둡니다. NO.41에서 리아 15초 영상 단가(Gemini Omni)를 적었듯, 영상도 같은 열에 둡니다. 「싼 모델」이 아니라 「싼 과제」를 고르는 표입니다.
3. **밤에 돌려도 되는 일 목록을 만든다.** 캐시 할인 95%(Artificial Analysis 페이지)와 배치 반값(VentureBeat 전언 — 구글 가격 페이지에서 확인되면)은 「지금 당장」이 아닌 일에만 적용됩니다. 상품 설명 일괄 점검, 주간 보고 초안, 번역 초벌처럼 사람이 아침에 확인해도 되는 일을 적어 두고, 그 일만 배치·캐시로 돌립니다. 여기서도 「되돌릴 수 없는 단계」(NO.45)는 목록 밖입니다.

## 이번에 고르지 않은 것

앤트로픽 뉴스 페이지의 11월 12일 항목은 제목 없이 날짜만 보였고, Manufacturing Dive는 같은 날 「Claude for Manufacturing」(스킬 17개 플러그인) 발표를 전했습니다 — 글을 쓴 AI의 제조사 제품이라 제목만 적습니다. 구글 딥마인드의 Gemini Robotics 2.5(11월 10일, 200여 과제·메르세데스 키팅 96%)와 AlphaGenome 2는 우리 일과 멀어 제목만 둡니다. 미스트랄이 11월 5일 낸 Studio(관리형 에이전트·워크플로·앱, 클라우드·VPC·온프레미스)는 가격이 없고 수치가 전부 회사 발표라 「작은 팀의 에이전트 운영 층」 후속 후보로 둡니다. Box CEO의 「정확도 74%→79%」는 X 게시글 전언이라 쓰지 않았습니다. BigGo의 「구글이 Flash 이름을 은퇴시켰다」는 구글 글에 없는 표현이라 쓰지 않았고, 구글의 모델 문서에는 11월 13일에도 Argon만 있고 Carbon·Hydrogen이 없습니다. Gemini 4 Hydrogen의 모델 카드는 열지 않았습니다.

## 이 소식에서 확인하지 못한 것

- 구글의 가격 페이지가 우리 쪽에서 구버전으로 열려, Gemini 3.8 Flash의 2027년 1월 1일 인상(0.75/3.75→1.50/7.50), Argon의 도입가 종료, Hydrogen 캐시 입력 0.075달러·배치 반값은 VentureBeat 한 곳의 정리입니다. 같은 날짜를 적은 개발자 블로그는 신뢰 매체로 치지 않았습니다.
- Artificial Analysis 페이지에서 직접 본 것은 Hydrogen(high) 51·1.87달러·1.10달러와 순위표의 여섯 모델 점수입니다. xhigh 54·medium 41·low 27, 단계별 과제당 비용, Terminal-Bench 4.0 54%는 매체 세 곳이 같은 숫자를 옮긴 것이고, 3.8 Flash의 지수 31·과제당 7.77달러는 VentureBeat 한 곳입니다.
- 회사 표의 Claude Sonnet 5.5 63.9%(Terminal-Bench 4.1)는 VentureBeat 한 곳이 옮긴 것이고, 구글 발표 글에서 우리가 직접 확인한 것은 Hydrogen 57%·Flash 18.2%입니다. 파트너 시험(2~2.8배)과 안전 수치는 모두 회사 발표이고 독립 확인은 없습니다.
- 에폭의 IPI는 시뮬레이터로 낸 모델링 값이고 실측이 아닙니다. 「에이전트 키 토큰 7배」는 에폭이 OpenRouter 데이터를 읽은 것이고 우리는 원자료를 열지 않았습니다.
- AlphaProof Code의 「600만 줄」과 「300만 줄」 차이는 글 안의 불일치이고, 기술 논문은 열지 않았습니다.

## 함께 읽은 글

성격이 다른 출처를 직접 열어 확인했습니다. 회사 발표, 연구·평가 기관, 매체 보도, 위키, 우리 이전 글을 나눠 적습니다.

회사 발표:

- [Introducing Gemini 4 Hydrogen for Agentic Workflows (Google, 11월 12일)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) — 영문, 자리매김·값·공개 범위·사고 단계 4개·벤치마크와 안전 수치(회사 발표)
- [Gemini 4 Hydrogen: everyday coding and agentic workflows for developers (Google, 11월 12일)](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/) — 영문, 개발자 경로·Orchestrator(값·Flash 언급 없음)
- [Introducing AlphaProof Code (Google DeepMind, 11월 10일)](https://deepmind.google/blog/introducing-alphaproof-code/) — 영문, Signal 프로토콜 형식 검증·4주·약 1%·되살린 버그 2개(회사 발표)

연구·평가 기관:

- [Gemini 4 Hydrogen (high) — Artificial Analysis 모델 페이지](https://artificialanalysis.ai/models/gemini-4-hydrogen-high) — 영문, 지능 지수 51(v5.0.1)·과제당 1.87달러·혼합 단가 1.10달러·캐시 할인 95%
- [Artificial Analysis 모델 순위표](https://artificialanalysis.ai/leaderboards/models) — 영문, Fable 5.2 65·Carbon 60·Opus 5.5 59·Astra 57·Sol 55·Sonnet 5.5 55·Argon 50(우리가 연 시점엔 Hydrogen 없음)
- [Inference Performance Index (Epoch AI, 11월 9일)](https://epoch.ai/publications/inference-performance-index) — 영문, 지수 정의·GB300 25배·VR200 2.18·에이전트 키 7배·한계와 검증

매체 보도:

- [Google launches Gemini 4 Hydrogen — a faster, smarter, pricier Flash successor (VentureBeat, 11월 12일)](https://venturebeat.com/technology/google-launches-gemini-4-hydrogen-a-faster-smarter-pricier-flash-successor) — 영문, 값표(Flash 2027년 인상·Argon·Carbon)·AA 단계별 과제당 비용·Flash 7.77달러·Sonnet 5.5 63.9%(한 곳)
- [Google's Gemini 4 Hydrogen outscores the bigger Argon just four weeks after its launch (The Decoder, 11월 12일)](https://the-decoder.com/googles-gemini-4-hydrogen-outscores-the-bigger-argon-just-four-weeks-after-its-launch/) — 영문, 회사 표의 Hydrogen/Argon/Carbon 비교(지는 칸 포함)·AA Terminal-Bench 54%·xhigh 토큰 2배 단서
- [Gemini 4 Hydrogen Places Ahead Of Gemini 4 Argon, Muse Wonder And GPT 6.1 Terra On Artificial Analysis Intelligence Index (OfficeChai, 11월 12일)](https://officechai.com/ai/gemini-4-hydrogen-artificial-analysis-intelligence-index/) — 영문, AA 순위 정리·단계별 점수와 비용
- [Google launches Gemini 4 Hydrogen for faster coding and agentic tasks (Interesting Engineering, 11월 12일)](https://interestingengineering.com/ai-robotics/google-gemini-4-hydrogen-coding-benchmark) — 영문, 회사 수치 정리·Orchestrator는 Ultra 구독자부터
- [Google's next-gen Gemini 4 Hydrogen AI model is here, touting faster intelligence for all (Digital Trends, 11월 12일)](https://www.digitaltrends.com/cool-tech/googles-next-gen-gemini-4-hydrogen-ai-model-is-here-touting-faster-intelligence-for-all/) — 영문, 무료 이용자 자동 선택·검색 전체·회사 표에서 뒤지는 항목
- [Anthropic launches 'Claude for Manufacturing' (Manufacturing Dive, 11월 12일)](https://www.manufacturingdive.com/news/anthropic-launches-claude-for-manufacturing/874303/) — 영문, 앤트로픽 11월 12일 발표(제목만 기록)

위키:

- [Gemini (language model) (Wikipedia)](https://en.wikipedia.org/wiki/Gemini_%28language_model%29) — 영문, Flash 계열 연표(3.8 Flash 9월 2일 공개, 구글 문서 인용; Gemini 4 세대 항목은 아직 없음)

우리 이전 글:

- [손님의 에이전트는 막고, 가게는 들이고, 모델은 모두에게 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [같은 모델에 문이 둘 (AP News NO.44)](https://www.apholdings.kr/ko/news/fable-5-2-two-doors-and-sandbagging-logs/)
- [주간 AI 소식 — 싸진 문 (AP News NO.41)](https://www.apholdings.kr/ko/news/weekly-2026-11-07/)
- [점수표에 확률이 붙었다 (AP News NO.40)](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [깃허브 풀 리퀘스트 열 건 중 넷은 에이전트가 연다 — 새 점수표의 1등은 아직 아무나 부를 수 없다 (AP News NO.33)](https://www.apholdings.kr/ko/news/agent-prs-40-percent-and-a-new-number-one/)
- [숫자를 비교하기 전에 셈법부터 (AP News NO.21)](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [작업별로 어떤 AI를 쓸까 (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/)
