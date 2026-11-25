---
no: 57
slug: approve-button-and-the-shape-of-permission
date: 2026-11-25
category: 인사이트
tags: 에이전트 · 승인정책 · Claude Ship · 구글검색 · 허깅페이스 · 하네스
title: 승인 버튼이 에이전트 손에 들어왔다 — 앤트로픽은 「누가 승인해야 하나」를 저장소 안 파일로 적게 하면서 「먼저 관찰 모드로, 저장소 하나·월 한도부터」라고 썼고, 구글은 검색 AI에 지갑을 「읽기만」으로 열었고, 허깅페이스는 모델을 그대로 두고 하네스에 맞춘 어댑터로 과제당 토큰을 절반 가까이 줄였다 — 권한의 모양 셋
summary: 11월 20~23일 소식 셋 — ①앤트로픽 Claude Ship(코드 리뷰·PR 스튜어드·승인 에이전트, 승인 정책은 .claude/approvals.yml, 관찰 모드부터, 문서의 「아무도 안 보고 병합될 수 있다」 경고) ②구글 검색 AI Mode의 Personal Intelligence가 Wallet(읽기 전용)·Drive·Gemini 앱으로 확장 ③허깅페이스 「하네스 어댑터」(모델 고정, 하네스별 LoRA, 저자 평가로 토큰 44~60% 감소). 권한을 「어디에, 어떤 모양으로」 적는지로 묶어 사실·해석·우리라면으로 나눠 적었습니다.
---

이 글은 AI(Claude)와 함께 작성했고 편집자가 검수했습니다. 이해관계를 먼저, 길게 적습니다 — **이 글의 1번은 이 글을 쓴 AI를 만든 앤트로픽 자신의 제품 발표(Claude Ship)입니다.** 우리 회사는 앤트로픽과 OpenAI 두 회사의 유료 고객이고 구글·메타 모델도 시험에 쓰지만, Claude Ship은 써 본 적이 없고 이 글은 제품 소개나 추천이 아닙니다. 그래서 1번에서는 회사가 적은 조건·경고·과금 문장을 그대로 옮기고, 「좋다」「낫다」는 평가는 한 줄도 보태지 않으며, 다른 회사의 비슷한 기능과 비교하지 않습니다. 회사가 발표한 수치는 「회사가 발표한 것」으로, 한 곳에서만 나온 내용은 그 출처를 함께 적었습니다. 3번의 수치는 허깅페이스 저자들의 자체 평가이고 제3자 검증은 없습니다. 이 글은 특정 기업에 대한 투자 의견이 아닙니다.

NO.50에서 「해도 되는 일」을 에이전트가 오기 전에 적어 두는 문서 셋을, NO.54에서 「에이전트 명부와 사고 일지」를, NO.56에서 「규칙은 어디에 적어야 지켜지나」를 적었습니다. 이번 주 소식 셋은 그 다음 칸에 닿습니다 — **권한을 어디에, 어떤 모양으로 적는가.** 앤트로픽은 「누가 승인해야 하나」를 저장소 안 파일로 적게 하고 「먼저 지켜보기만 하라」고 썼고, 구글은 검색 AI에 지갑을 열되 「읽기만」으로 모양을 정했고, 허깅페이스는 모델이 아니라 모델과 도구 사이(하네스)에 맞춘 어댑터를 내놓았습니다. 회사 발표 셋(앤트로픽 글·문서, 구글 글, 허깅페이스 글), 플랫폼 문서 하나(GitHub), 매체 둘(TechCrunch·The Hacker News), 공지 하나(OpenRouter)를 사실·해석·우리라면으로 나눠 적습니다.

## 1. 앤트로픽 Claude Ship — 승인 정책은 `.claude/approvals.yml`에, 먼저 관찰 모드로, 그리고 「아무도 안 보고 병합될 수 있다」는 경고 (사실, 회사 발표·공식 문서·매체)

앤트로픽의 발표 글 「Introducing Claude Ship」(11월 23일, claude.com)과 개발자 문서(code.claude.com)를 직접 읽었습니다. 뉴스룸(anthropic.com/news)에는 이 글이 없고 제품 사이트 쪽에 올라와 있습니다. Claude Ship은 GitHub 풀 리퀘스트(PR) 하나를 **검토 → 수정 → 승인 판정**까지 끌고 가는 에이전트 묶음이고, 셋으로 구성됩니다(회사가 적은 이름 그대로).

- **Code Review** — 이미 정식 제공(GA). PR을 여러 관점으로 읽어 발견 사항을 모으고, 반대 검증을 거쳐 분류한 뒤 PR에 댓글로 답니다. 저장소마다 Quick·Standard·Deep 세 단계 중 하나를 고릅니다.
- **PR Steward** — 베타. 실패한 CI 검사, 병합 충돌, 사람·리뷰 도구가 남긴 리뷰 의견을 받아 수정 커밋을 올립니다. 푸시할 때마다 「무엇을 바꿨고 어떻게 되돌리는지」를 댓글로 적고, 개발자는 `@claude`로 지시하거나 `@claude stop`으로 물러나게 할 수 있습니다. 회사는 이 에이전트가 「승인·병합은 하지 않도록 설계됐다」고 적었습니다.
- **Claude Approvals** — 베타. 팀이 저장소에 적은 **승인 정책 파일**을 적용합니다. 문서에 적힌 경로는 `.claude/approvals.yml`이고, 기본 브랜치에 이 파일이 올라가면 켜집니다. 정책에는 경로별로 「사람 몇 명의 승인이 필요한가」와 「Claude가 승인 리뷰를 달아도 되는 곳」을 적고, 신호로 Code Review의 발견 사항이나 팀이 **자연어로 쓴 분류기**를 걸 수 있습니다. 발표 글은 이것을 「더 똑똑한 CODEOWNERS 파일」이라고 불렀습니다. 회사의 권고 순서는 — 먼저 **관찰 모드(observe-only)**로 켜서 판정만 지켜보고, 믿음이 생기면 GitHub 브랜치 보호 규칙에 「이 검사 통과 필수」로 넣으라는 것입니다.

개발자 쪽에는 Claude Code의 `/ship` 명령이 생겼습니다 — 변경을 푸시하고 PR을 열고 검토하고 피드백·실패 검사를 처리하는 한 묶음. 무엇이 병합되는지는 그 개발자의 권한과 저장소의 브랜치 규칙이 정한다고 적혀 있습니다. 관리자 쪽은 조직 설정의 Claude Ship 화면(Owner 권한 필요)에서 **저장소 하나씩, 에이전트 하나씩** 켜라고 문서가 적었고, 순서도 적혀 있습니다 — Code Review → PR Steward(처음엔 「수동(@claude steward)」 트리거로, **지출 한도를 정하기 전에는 PR Steward에 한도가 없으므로**) → Claude Approvals(정책 파일이 켜고, 관찰 모드부터, **관찰 모드도 과금**). 발표 글의 문장으로는 「저장소 하나에서 시작하고, 월 지출 한도를 정하고, 정책은 신뢰가 생길 때까지 관찰 모드로」입니다.

제공 범위와 과금(회사가 적은 것). Claude Team·Enterprise 요금제, GitHub 저장소(GitLab은 문서에 「별도 CI 연동」으로만 나옴). 데이터 무보존(ZDR)·HIPAA 구성·고객 관리 암호화 키를 쓰는 조직은 쓸 수 없습니다. 비용은 토큰 사용량으로 조직의 사용 크레딧에서 나가며 요금제 포함분과 별도입니다. Claude Approvals는 기본 요금이 없지만 분류기 실행은 토큰으로 과금되고, 정책이 Claude의 리뷰를 요구하면 관찰 모드에서도 Code Review가 돌아 과금됩니다. 끄는 순서도 문서에 있습니다 — Approvals → PR Steward → Code Review 순으로, 정책이 리뷰를 불러 과금할 수 있기 때문입니다. 사용 크레딧을 꺼도 켜 둔 에이전트는 계속 돌고 과금되니 「요금을 멈추려면 에이전트를 꺼라」고 적었습니다.

경고도 문서에 있습니다. **GitHub의 자동 병합(auto-merge)이나 머지 큐를 「사람 승인을 요구하지 않는 정책」과 함께 쓰면, 아무도 손대지 않은 채 변경이 병합될 수 있다**는 문장과, 발표 글 이미지 설명의 「Claude Ship은 AI를 쓰므로 버그·보안 취약점·그 밖의 문제를 놓칠 수 있다」는 문장입니다. 정책이 모호하거나 변경이 정책 밖일 때 어떻게 되는지는 두 페이지에 적혀 있지 않습니다(하위 문서 미열람 — 아래 「확인하지 못한 것」).

회사가 발표한 수치는 자사 사례뿐입니다 — 「Claude Code 팀에서는 Claude가 우리 코드 대부분을 쓴다」, 같은 팀의 병합 PR이 6월에서 9월 사이 「2배 이상」, 되돌려진 PR 비율은 「40% 이상 감소」. 고객사 인용 둘(TELUS·카바나)은 회사가 고른 추천사입니다. TechCrunch(사라 페레스, 11월 23일)는 발표 글과 문서를 링크하고 같은 내용을 옮겼으며 새 수치는 없습니다.

비교 기준으로 GitHub 문서 「About code owners」를 열었습니다. CODEOWNERS는 저장소의 `.github/`·루트·`docs/` 중 한 곳에 두는 파일로, **파일 경로 패턴 → 담당자(@user·@org/team)** 한 줄씩이 전부입니다. PR이 그 경로를 건드리면 담당자에게 자동으로 리뷰가 요청되고, 브랜치 보호의 「Require review from Code Owners」를 켜면 담당자 중 **한 명**의 승인으로 요건이 채워집니다. 경로 외의 조건(변경 내용·크기·시간)은 문법에 없습니다. 즉 지금까지 저장소에 적을 수 있던 「승인 규칙」은 「어느 경로는 누가」까지였습니다.

## 2. 구글 검색 AI Mode의 Personal Intelligence — 지갑은 「읽기만」, 드라이브·Gemini 앱은 수주 내 (사실, 회사 발표·매체)

구글 검색 제품 부사장 로비 스타인의 글 「A more tailored Google Search that's uniquely yours」(11월 23일)를 직접 읽었습니다. 검색 AI Mode의 Personal Intelligence(사용자가 연결을 허락한 구글 앱의 정보로 답을 맞추는 기능, NO.55)에 이미 Gmail·캘린더·포토가 연결돼 있었고, 이번에 **Google Wallet이 「오늘부터」, Google Drive와 Gemini 앱이 「수주 내」** 더해집니다. 모두 옵트인이고, 「검색 개인화 → 연결된 앱」에서 앱별로 켜고 끌 수 있으며 개인화 전체도 끌 수 있습니다.

지갑 연결의 모양이 이 글이 이 소식을 고른 이유입니다. 글은 **「지갑을 연결하면 AI Mode는 계정 정보를 읽을 수만 있고, 돈을 옮기거나 관리하거나 투자할 수 없다」**고 적었습니다. 쓰임새로 든 것은 지출 흐름과 「재무 이정표」 보기, 일상 지출 줄일 곳 찾기, 연결된 카드의 혜택(캐시백 범주·여행 특전·포인트) 챙기기입니다. 드라이브 연결은 문서·시트·PDF를 읽어 「세금 신고 준비 계획」 같은 답을 만드는 예시이고, Gemini 앱과는 맥락을 서로 넘길 수 있게 됩니다. 「곧」 답 아래의 「Personalization」 아이콘으로 어떤 맥락이 쓰였는지 볼 수 있고, 틀린 맥락은 말로 고칩니다(「이제 채식 안 해」). 글에 없는 것 — 국가·요금제 조건, 수치, 그리고 **쇼핑·구매·결제 언급은 하나도 없습니다**(「쇼핑」은 사이트 메뉴에만 있음). 패스·멤버십 카드가 포함되는지도 적혀 있지 않습니다. TechCrunch(아이샤 말릭, 11월 23일)는 공식 글을 링크하고 「읽기 전용」을 같은 뜻으로 옮겼습니다. 9to5Google의 11월 13일 기사(Gemini 앱 쪽 Wallet 연결)는 「미국 한정」이라 적었는데, 검색 쪽 글에는 지역이 없어 이 글은 지역을 적지 않습니다.

NO.55에서 구글 검색의 Connected Apps(장보기 → 결제)와 메타 Muse의 「결제수단은 에이전트에게 안 보임」을 적었습니다. 이번 글은 그 옆 칸 — 같은 회사의 검색 AI가 **지갑을 「읽기」로만 여는** 선택입니다. 「결제까지」와 「읽기만」이 같은 회사 안에서 다른 제품에 다른 모양으로 붙어 있습니다.

## 3. 허깅페이스 「하네스 어댑터」 — 모델은 그대로, 하네스에 맞춘 LoRA 하나씩, 저자 평가로 토큰 44~60% 감소 (사실, 연구 블로그)

허깅페이스 블로그 「Introducing harness adapters」(11월 20일, 허깅페이스 소속 저자 10명)를 직접 읽었습니다. 생각은 단순합니다 — 에이전트의 성능은 모델만이 아니라 모델을 감싸는 **하네스**(도구 호출·컨텍스트 관리·프롬프트 — pi, OpenCode, Hermes Agent 같은 코딩 에이전트 틀)에 따라 달라지니, 모델 가중치는 고정해 두고 **하네스마다 작은 어댑터(LoRA)를 하네스 안에서 강화학습으로 훈련**하자는 것입니다. 기반 모델은 Qwen3.8-27B 하나, 하네스는 pi 1.5.2·OpenCode 2.2.7·Hermes Agent v0.22.6 셋, 어댑터는 하네스마다 하나씩 셋과 그 셋을 합친 「슈퍼 어댑터」 하나입니다. 훈련은 검증기가 채점하는 코딩 과제(공개 데이터셋 871개 중 「가끔 푸는」 171개를 골라 섞은 1,050개)에서 GRPO 방식으로, 추론(thinking) 모드는 끄고 돌렸습니다. 어댑터 하나당 B200 GPU 두 장이었다고 적혀 있습니다.

결과(모두 저자들의 자체 평가, pass@1 한 번 시도, thinking 끔). pi 하네스에서 Terminal-Bench 2.1은 **40.0% → 56.5%**(글 첫머리에는 39% → 55%, **과제당 토큰 2.9K → 1.5K**), SWE-bench Pro 어려운 51문제는 **40.0% → 64.0%**(본문 다른 곳에는 39.2% → 64.7% — 글 안에서 두 숫자가 일치하지 않고 저자가 설명하지 않았습니다). Hermes에서 Terminal-Bench 44.7% → 58.8%, OpenCode에서 47.6% → 52.4%. 셋을 합친 슈퍼 어댑터는 여섯 쌍 평균 **39.5% → 49.0%**(새로 푼 71개, 잃은 34개), 둘 다 푼 과제에서 **도구 호출 53~73%·토큰 44~60% 감소**. 저자들이 스스로 적은 한계 — 하네스마다 기본 설정이 달라 하네스 간 점수는 비교할 수 없다, 슈퍼 어댑터의 가중치를 Terminal-Bench에서 골랐으니 그 점수는 「약간 낙관적」이다, thinking을 켠 조건은 거의 시험하지 않았다. 학습에 없던 과제(AutomationBench 300개)에서는 23.0% → 27.0%(pi) 수준으로 **「소음 범위 안」**이라고 적었습니다(이 부분은 글 뒷부분 요약으로 읽음). 달러 비용 절감은 주장하지 않았고 토큰·도구 호출 수만 셌습니다. 어댑터·과제·궤적은 허깅페이스에 공개됐고 라이선스 표기는 본문에서 찾지 못했으며, 제3자 검증은 없습니다.

같은 블로그의 「How to build and maintain an agentic evaluation」(11월 23일, 아비짓 고시·벤 버튼쇼·아이린 솔라이만)은 이 숫자를 읽는 법을 줍니다 — 모델을 돌리기 전에 **과제부터 검증**(기준 해답은 통과하고, 「아무것도 안 하는 에이전트」와 「지름길」은 떨어지는지), 에이전트의 「끝냈다」가 아니라 **저장된 산출물을 채점**, 하네스 버전·컨테이너·모델 제공자를 **고정**, pass@k와 pass^k를 나란히. 글이 든 숫자(저자 인용) — 하네스를 바꾸자 같은 모델의 Terminal-Bench 정확도가 최대 29.9점 움직였고, Terminal-Bench 2.1은 공개 보고 뒤 89개 중 28개 과제를 고쳤으며, OpenAI의 SWE-bench Verified 감사에서는 살펴본 138문제의 59.4%에 실질적 결함이 있었습니다. NO.52·56의 「평가하는 쪽도 평가받는다」의 실무판입니다.

## 짧게 셋 (사실, 공식 공지·매체·회사 발표)

- **OpenRouter, 추론 제공자 3곳 제외·125개 엔드포인트의 「무보존」 자격 박탈(11월 22일)** — OpenRouter 공지와 The Hacker News(스와티 칸델왈)를 읽었습니다. 보안 회사 Dragos가 7월부터 11월까지 시험용 프롬프트를 심어 누가 꺼내 보는지 추적한 결과, 일부 추론 제공자가 데이터를 유출했거나 「무보존」 약속을 지키지 않았다는 것입니다. OpenRouter는 제공자 3곳을 내보내고 125개 엔드포인트를 무보존(ZDR) 자격에서 뺐으며 영향 가능 고객에게 알렸고, **자사 시스템의 침해는 없었다**고 적었습니다. 내보낸 3곳의 이름은 공지 본문에 없고(Atlas Cloud·Novita·Phala·Together의 자체 공지 링크만 있음), 되돌리려면 확인을 요구한다고 했습니다. NO.51에서 허깅페이스가 자기 추론 라우팅을 OpenRouter에 넘겼다고 적었는데, 그 라우터 뒤의 제공자 층에서 생긴 일입니다. 수법은 적지 않습니다.
- **OpenAI·시스코 「Shirudo」(11월 23일)** — 리눅스에서 돌아가는 프로그램에 패치가 준비될 때까지 임시 「방패」를 씌우는 런타임을 오픈소스(BSD 2-Clause)로 냈다는 회사 발표입니다. 회사는 통제된 시험에서 재시작 없이 공격 시도를 막았다고 적었고, 수치는 없습니다. 지난 글에서 「제목만」이라 적은 그 소식이고, 보안 글이라 동작 방식은 적지 않습니다.
- **과제당 비용, 개인 측정 1건** — 사이먼 윌리슨(11월 20일)이 자기 도구로 같은 프롬프트를 돌려 적은 값은 Gemini 4 Hydrogen high 3.99센트·19초, xhigh 23.61센트·2분 36초, Neon xhigh 39.83센트, Carbon high 20.31센트입니다. 한 사람의 한 프롬프트라 비교표에 넣지 않고, NO.46의 「과제당 비용은 단계에 따라 6배 벌어진다」의 사례로만 둡니다.

## 세 가지를 함께 읽으면 (해석)

첫째, **「승인」이 저장소 안의 파일이 됐고, 그 파일에 처음으로 경로 말고 조건이 들어갔습니다.** GitHub 문서대로 지금까지 저장소에 적을 수 있던 승인 규칙은 「이 경로는 이 사람」이 전부였고 한 명의 승인이면 됐습니다. 앤트로픽 문서의 정책 파일은 거기에 「몇 명」과 「어떤 조건이면 에이전트가 승인해도 되나(자연어 분류기)」를 더했습니다. 이것이 좋은지 나쁜지는 이 글이 판단하지 않습니다(이해관계 고지 참조). 우리가 읽은 것은 모양입니다 — NO.56에서 「규칙은 에이전트가 실제로 읽는 자리에 있어야 한다」고 적었는데, 이번 모양은 **규칙을 사람이 읽는 문서가 아니라 병합 경로가 반드시 지나가는 검사(check)로 옮긴 것**입니다. 그리고 그 회사가 같은 문서에 「자동 병합과 함께 쓰면 아무도 안 보고 병합될 수 있다」고 적어 둔 것이, 이 모양의 다른 면입니다 — 검사가 되는 순간 사람이 빠질 수 있습니다.

둘째, **권한의 모양이 「읽기/쓰기」로 갈리고 있고, 같은 회사 안에서도 제품마다 다릅니다.** 구글 검색 AI의 지갑은 「읽기만」, 같은 구글의 Connected Apps는 「결제까지」(NO.55), 메타 Muse는 「결제수단은 안 보이고 구매 전 확인」(NO.53). 셋 다 회사 발표문의 한 문장이고, 셋 다 우리가 가게나 앱에서 그대로 쓸 수 있는 선택지입니다. 우리 쪽 교훈은 「권한」을 한 덩어리로 주지 말고 읽기와 쓰기를 따로 적는 것 — 지갑처럼 「읽기만」으로도 쓸모가 있는 연결이 꽤 많습니다(재고 조회, 주문 상태 확인, 댓글 읽기).

셋째, **바꾸는 자리가 모델이 아닐 수 있습니다.** NO.48에서 「모델을 바꾸는 데 몇 주 걸린다」와 「모델 바깥에 둔 것만 넘어간다」를 적었습니다. 허깅페이스의 글은 그 반대편입니다 — 모델은 그대로 두고 모델과 도구 사이에 맞춘 작은 조각으로 토큰을 절반 가까이 줄였다는 저자 평가입니다. 숫자는 한 모델·세 하네스·저자 자체 평가이고 학습 밖 과제에선 소음 범위라서 「어댑터가 답」이라고 쓸 수 없습니다. 쓸 수 있는 것은 질문입니다 — 우리 에이전트 비용의 몇 퍼센트가 모델 단가이고 몇 퍼센트가 하네스(불필요한 도구 호출·긴 컨텍스트)인가. NO.46의 과제당 비용 표에 「도구 호출 수」 열이 없다면, 이번 주에 그 열부터 추가하는 것이 이 소식에서 공짜로 가져올 수 있는 것입니다.

## 우리라면 — 코드·가게·앱을 운영하는 작은 팀이 이번 주에 할 세 가지 (실전)

1. **승인 정책을 도구와 무관하게 사람 말로 한 장 먼저 적는다.** 우리 홈페이지 저장소(뉴스 빌드·반영 스크립트)와 앱 저장소 각각에 대해 「누가 승인해야 병합되나」를 경로별로 적되, 경로 옆에 **조건**을 붙입니다 — 「번역 파일만 바뀐 PR은 검사 통과면 됨」, 「결제·회원·발송 코드는 사람 둘」, 「스크립트·설정은 사람 하나 + 되돌리기 방법 댓글 필수」. 어떤 도구를 쓰든 이 한 장이 먼저이고, GitHub의 CODEOWNERS로 적을 수 있는 줄(경로 → 사람)은 지금 바로 적습니다. 자동 병합·머지 큐는 「사람 승인 없는 정책」과 함께 켜지 않는다는 줄을 맨 위에 둡니다 — 이 줄은 제품 문서가 아니라 우리 운영 규칙입니다. 에이전트가 승인 판정을 하게 될 날이 오더라도, NO.54의 명부에 「승인 에이전트」 한 줄과 월 한도·관찰 기간을 먼저 적은 뒤입니다.
2. **에이전트에게 주는 연결마다 「읽기/쓰기」를 갈라 적는다.** NO.55의 「문 표」(상품 정보·장바구니·결제·회원 정보)에 열을 하나 더 — 「읽기만 / 쓰기까지」. 한글컵스 주문 상태·코트메이트 게시판·리아 댓글은 「읽기만」으로 시작해도 에이전트가 할 일이 많고, 「쓰기」(발송·게시·환불)는 NO.56의 한도 칸과 같이 붙입니다. 구글 글의 문장을 우리 말로 바꾸면 「이 연결은 읽을 수만 있고 옮기거나 지울 수 없다」 — 이 한 줄이 스토어 설명·개인정보 안내에 들어갈 수 있는지 홍보와 정합니다.
3. **과제당 비용 표에 「도구 호출 수」 열을 넣고, 평가 과제 셋을 먼저 검증한다.** NO.46·52의 표(모델/단계/완료/토큰/과제당 비용/시간)에 도구 호출 수를 추가하고, 같은 모델·같은 과제를 하네스(우리 프롬프트·도구 구성) 두 가지로 돌려 토큰과 호출 수 차이를 적습니다 — 모델을 바꾸지 않고 줄일 수 있는 몫이 얼마인지 보는 것입니다. 그 전에 허깅페이스 평가 글의 세 검증을 우리 과제 셋(성분표 항목 추출·커머스 문의 분류·리아 대본 교정)에 합니다 — 기준 해답은 통과하는가, 「아무것도 안 하는 에이전트」는 떨어지는가, 지름길은 막히는가. 하나라도 통과하면 그 과제의 과거 점수는 지우고 다시 잽니다. 리아 대본에는 「승인 버튼을 에이전트에게 주는 회사가 먼저 적은 것은 『관찰 모드』였다」를 배우는 톤으로, 제품명과 수치는 reported로만 넣습니다.

## 이번에 고르지 않은 것

OpenAI의 「GPT-6 단백질 설계」·「Astra로 외계행성 탐색」(11월 24일)은 과학 사례라 제목만. 앤트로픽 뉴스룸은 11월 20일 상장 완료 뒤 새 글이 없고(투자 영역·제목만), 에폭의 「앤트로픽 컴퓨트 지출 연 4배」(11월 18일)도 투자·제조사 관련이라 제목만. 사이먼 윌리슨이 인용한 「Claude와 리만 가설」 주장(11월 20일)은 미검증·제조사 관련이라 지난 글과 같이 쓰지 않습니다. GLM-5.4(Z.ai 첫 루프 트랜스포머, 11월 23일, 오픈 웨이트 아님·수치 없음)와 Inkling 2 Mini(허깅페이스·Thinking Machines, 26B/활성 3B, 32GB에 들어감 — 회사 주장)는 NO.51 후속 후보로 둡니다. The Hacker News의 CERT-In 경보·Muse 웹페이지 시연(NebuSec, 수정 완료)·의료영상 소프트웨어 제로데이(아마존 발표 전언)·Cursor의 도난 API 키 사고(날짜 미확인)는 수법을 적지 않는 원칙과 1곳·미열람 때문에 제목만 둡니다. 「통신사·네이버, 외부 AI 에이전트의 고객센터 상담 차단」(ZDNet Korea 제목, promppy 요약)은 NO.45·55 「문을 닫는 쪽」의 국내 사례일 수 있어 원문을 열어 다음 회차에 확인합니다. 아마존 Decart 인수·Sierra·Supertake(TechCrunch)는 투자라 제목만. 구글 AI 블로그 RSS는 5월에서 멈춘 피드라 개별 글만 직접 열었습니다.

## 이 소식에서 확인하지 못한 것

- Claude Ship — 하위 문서(approvals-policy·approvals-classifiers·pr-steward-security 등)는 열지 않아, 정책이 모호하거나 변경이 정책 밖일 때 사람에게 넘기는지, 분류기 문법이 어떤지, 관찰 모드의 로그가 어디에 남는지는 모릅니다. 「2배 이상」「40% 이상 감소」「코드 대부분」은 회사 자사 팀의 수치이고 분모·기간 정의는 발표 글에 없습니다. 발표 글은 「관리자가 Code Review·PR Steward의 지출 한도를 정한다」고 적고 문서는 「PR Steward는 한도를 정하기 전엔 없다」고 적어, 기본값이 「없음」이라는 것만 문서 기준으로 옮겼습니다. 발표 글의 「더 똑똑한 CODEOWNERS」는 회사의 표현이고 우리의 평가가 아닙니다. 우리는 이 제품을 써 보지 않았습니다.
- 구글 글에는 국가·요금제·수치가 없습니다. 「미국 한정」은 Gemini 앱 쪽 9to5Google 11월 13일 기사(1곳)이고 검색 쪽에는 해당 문장이 없습니다. 패스·멤버십 포함 여부, 「Personalization」 아이콘의 시점(「곧」)은 확인하지 못했습니다.
- 허깅페이스 어댑터 글은 본문 뒷부분(학습 밖 과제 결과·한계 일부)을 요약으로 읽었습니다. 숫자는 저자 자체 평가·한 모델·세 하네스이고, 글 안에서 같은 지표의 숫자가 두 가지로 적힌 곳(40.0/39.2, 64.0/64.7, 47.6/46.4)이 있으며 저자가 설명하지 않았습니다. 라이선스는 본문에서 찾지 못했습니다. 평가 글의 「SWE-bench Pro 약 30% 결함」(OpenAI 추정)과 「29개 벤치마크 포화」는 요약 부분에서 읽어 본문에 적지 않았습니다.
- OpenRouter — 내보낸 3곳과 Dragos가 지목한 3곳이 같은지는 두 글 모두 적지 않았습니다. Dragos 원문은 열지 않았습니다.
- Shirudo — 회사 발표만 읽었고 저장소·시험 조건은 열지 않았습니다.
- 어느 회사의 시험도 우리가 재현한 것은 없습니다. 「우리라면」의 세 줄은 이번 주에 시작하고 결과는 다음 글에 적습니다.

## 함께 읽은 글

성격이 다른 출처를 직접 열어 확인했습니다. 회사 발표·공식 문서, 플랫폼 문서, 연구 블로그, 공지, 매체 보도, 개인 블로그, 우리 이전 글을 나눠 적습니다.

**회사 발표·공식 문서**

- [Introducing Claude Ship (Anthropic, 11월 23일)](https://claude.com/resources/articles/introducing-claude-ship) — 영문, Code Review GA·PR Steward·Claude Approvals 베타·관찰 모드·저장소 하나·월 한도·Team/Enterprise·GitHub·자사 팀 수치(2배 이상·40% 이상)
- [Claude Ship — 개발자 문서 (Anthropic)](https://code.claude.com/docs/en/claude-ship) — 영문, `.claude/approvals.yml`·경로별 승인 인원·`claude/code_review` 트리거·관찰 모드 과금·PR Steward 한도 기본 없음·끄는 순서·자동 병합 경고
- [A more tailored Google Search that's uniquely yours (Google, 로비 스타인, 11월 23일)](https://blog.google/products-and-platforms/products/search/google-search-personal-intelligence-apps/) — 영문, Wallet 오늘·Drive·Gemini 앱 수주 내·「읽을 수만 있고 옮기거나 관리하거나 투자할 수 없다」·옵트인·Personalization 아이콘
- [OpenAI and Cisco introduce Shirudo (OpenAI, 11월 23일)](https://openai.com/index/introducing-shirudo/) — 영문, 리눅스 런타임 「방패」·오픈소스 BSD 2-Clause·수치 없음

**플랫폼 문서**

- [About code owners (GitHub Docs)](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) — 영문, 경로 패턴 → 담당자·자동 리뷰 요청·「Require review from Code Owners」·한 명 승인으로 충족·경로 외 조건 없음

**연구 블로그**

- [Introducing harness adapters (Hugging Face, 11월 20일)](https://huggingface.co/blog/harness-adapters-at-scale) — 영문, Qwen3.8-27B 고정·pi/OpenCode/Hermes·GRPO·40.0→56.5%·2.9K→1.5K 토큰·슈퍼 어댑터 39.5→49.0%·토큰 44~60% 감소·학습 밖 과제 소음 범위
- [How to build and maintain an agentic evaluation (Hugging Face, 11월 23일)](https://huggingface.co/blog/agentic-evals) — 영문, 과제 검증 셋·산출물 채점·버전 고정·pass@k/pass^k·하네스 차이 29.9점·TB 2.1 28/89 수정·SWE-bench Verified 59.4%

**공지**

- [Data Processing Incidents on Inference Providers (OpenRouter, 11월 22일)](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/) — 영문, 제공자 3곳 제외·125개 엔드포인트 ZDR 제거·고객 통지·자사 침해 없음

**매체 보도**

- [Anthropic launches Claude Ship, letting AI agents review, fix, and approve code changes (TechCrunch, 11월 23일)](https://techcrunch.com/2026/11/23/anthropic-launches-claude-ship-letting-ai-agents-review-fix-and-approve-code-changes/) — 영문, 공식 글 링크·새 수치 없음
- [Google Search's AI Mode can now tap into Drive and Wallet for more personalized responses (TechCrunch, 11월 23일)](https://techcrunch.com/2026/11/23/google-searchs-ai-mode-can-now-tap-into-drive-and-wallet-for-more-personalized-responses/) — 영문, 읽기 전용·옵트인
- [OpenRouter Drops 3 Providers After Researchers Catch Months of Prompt Theft at AI Hosting Firms (The Hacker News, 11월 22일)](https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html) — 영문, Dragos 7~11월 추적·3곳·125개·이름 미공개

**개인 블로그**

- [llm-gemini 0.38.1 — Hydrogen·Neon·Carbon 과제당 비용 측정 (Simon Willison, 11월 20일)](https://simonwillison.net/2026/Nov/20/llm-gemini/) — 영문, 개인 측정 1건·3.99/23.61/39.83/20.31센트

**우리 이전 글**

- [「속도 제한」에 처음으로 숫자가 붙었다 — 규칙은 어디에 적어야 지켜지나 (AP News NO.56)](https://www.apholdings.kr/ko/news/perplexity-speed-limit-and-rules-written-then-broken/)
- [에이전트가 결제 버튼 앞까지 왔다 — 가게가 정할 것은 문의 종류 넷 중 하나다 (AP News NO.55)](https://www.apholdings.kr/ko/news/agent-doors-checkout-and-handback/)
- [에이전트 명부와 사고 일지, 두 장이 먼저다 (AP News NO.54)](https://www.apholdings.kr/ko/news/agent-roster-and-incident-log/)
- [주간 AI 소식 — 값은 내리고 한계는 적고, 에이전트는 데스크톱과 장바구니에 (AP News NO.53)](https://www.apholdings.kr/ko/news/weekly-2026-11-21/)
- [「중간 칸」 Gemini 4 Neon — 점수표 하나로는 모자란 세 가지 이유 (AP News NO.52)](https://www.apholdings.kr/ko/news/neon-same-score-seventeen-points-apart/)
- [토큰 열 개 중 일곱은 오픈 웨이트 모델로 간다 (AP News NO.51)](https://www.apholdings.kr/ko/news/open-weights-take-seven-in-ten-tokens/)
- [「해도 되는 일」을 에이전트가 오기 전에 적어 두는 세 문서 (AP News NO.50)](https://www.apholdings.kr/ko/news/allowed-list-before-the-agent-arrives/)
- [모델을 바꾸는 데 몇 주가 걸린다 — 모델 바깥에 둔 것만 넘어간다 (AP News NO.48)](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [「매일 쓰는 모델」 칸이 생겼다 — 과제당 비용으로 읽는 법 (AP News NO.46)](https://www.apholdings.kr/ko/news/hydrogen-daily-driver-price-per-task/)
- [손님의 에이전트는 막고, 가게는 들이고, 모델은 모두에게 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [에이전트는 「믿을 수 없는 내부자」다 (AP News NO.29)](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
