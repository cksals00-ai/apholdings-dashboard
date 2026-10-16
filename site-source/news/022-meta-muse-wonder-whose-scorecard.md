---
no: 22
slug: meta-muse-wonder-whose-scorecard
date: 2026-10-15
category: 인사이트
tags: Meta · Muse Wonder · 모델 평가 · 독립 평가 · 학습 설정
title: 메타의 첫 최상위 모델 Muse Wonder — 점수는 누가 매겼나, 쓰기 전에 볼 세 가지
summary: 메타가 10월 12일 첫 최상위 모델을 내놨다. 회사가 발표한 점수와 독립 평가기관의 점수를 나란히 놓고, 가격·접근 방식·학습 설정까지 우리 일에 쓰기 전에 확인할 세 가지를 정리했다.
---
> 이 글은 AI(Claude)와 함께 작성했고 편집자가 검수했습니다. 글에 비교 대상으로 나오는 Claude 모델을 만든 앤트로픽이 이 글을 쓴 도구의 제작사이기도 해서, 우리에게 이해관계가 있습니다. 회사가 발표한 수치는 「회사가 발표한 것」으로, 독립 평가는 따로 표시했습니다. 특정 기업·종목에 대한 투자 의견이 아닙니다.

10월 12일 월요일, 메타의 슈퍼인텔리전스 랩이 Muse Wonder와 Muse Wonder Full 두 모델을 공개했다. 메타가 「첫 최상위(프런티어)급 모델」이라고 부르는 모델이다. 이번 소식에서 눈여겨볼 것은 점수 자체보다, 그 점수를 누가 어떤 조건으로 매겼는가다.

## 무엇이 나왔나 (사실)

- Muse Wonder는 메타의 모델 API와 코딩 도구 Muse Code에서 쓸 수 있다. API 가격은 입력 100만 토큰당 4달러, 출력 100만 토큰당 20달러다(독립 평가기관 Artificial Analysis 기준 캐시된 입력은 0.20달러).
- Muse Wonder Full은 Muse Code 구독자 전용이다. API로는 제공되지 않는다(TechCrunch). 메타의 Muse Code 구독 안내에 따르면 Full은 네 요금제 가운데 위의 두 요금제(Power·Maximum)에 들어 있고, 이 두 요금제가 월 50달러와 200달러라고 LetsDataScience와 DataNorth가 전했다.
- 두 모델 모두 컨텍스트 100만 토큰, 입력은 글·이미지·영상·음성, 출력은 글이다(Artificial Analysis).
- 두 모델의 가중치를 내려받을 수 있는지는 확인하지 못했다(내려받을 수 없다고 적은 곳은 LetsDataScience 한 곳). Decrypt는 메타가 가중치를 공개하던 Llama 계열을 사실상 접었다고 짚었다.

## 점수표 읽기

**회사가 발표한 것.** 메타는 자체 지표 「Personal Superintelligence Index」에서 Wonder Full이 59.1점으로 Opus 5.5(55.2), GPT-6 Astra(54.5)보다 높다고 밝혔고, 기억력 시험 MemoryBench에서도 약 85.5점으로 앞선다고 했다(Decrypt가 전한 메타 발표, iThome·Latent Space 보도와 같은 수치). 이 두 지표는 메타가 만든 것이고 계산 방식이 공개되지 않았다고 Decrypt는 적었다.

**독립 평가.** Artificial Analysis의 종합 지수(v4.3, 최고 노력 설정)에서 Wonder Full은 56점, Wonder는 52점, 메타의 이전 모델 Muse Spark 1.3은 48점이다. 같은 지수에서 Opus 5.5는 58점, Sonnet 5.5는 56점, GPT-6 Astra는 53점이다(Artificial Analysis 순위표에서 직접 확인, 각 모델의 최고 설정 기준). 즉 독립 평가에서는 「세 번째 안팎」이지, 회사 지표가 말하는 「앞선다」와는 결이 다르다.

**조금 더 들여다보면.** Artificial Analysis는 같은 글에서 이렇게 적었다. 코딩 에이전트 지수에서 Wonder Full은 68점으로 Claude Code(Sonnet 5.5)와 같고, Opus 5.5(66)보다 높다. 반면 지식 문항 AA-Omniscience에서는 Full이 30점, Wonder가 25점으로 Opus 5.5(46)·GPT-6 Astra(43)보다 많이 낮다. 지어내는 비율(환각률)은 Full 23%, Wonder 27%로 낮은 편이지만, 지수 45점 이상 모델 가운데 가장 낮은 것은 Gemini 4 Argon의 15%다.

## 쓰기 전에 볼 세 가지 (해석)

**1. 한 번 도는 비용.** 토큰 단가가 같아도 일 하나를 끝내는 비용은 다르다. Artificial Analysis가 같은 과제 묶음을 돌린 비용은 Wonder 4.52달러, Opus 5.5 5.98달러, Sonnet 5.5 5.46달러, GPT-6 Astra 3.26달러, Gemini 4 Argon 1.99달러, GPT-6.1 Sol 0.72달러다. Wonder는 비슷한 수준의 다른 모델보다 비싼 편이라는 평가였다. 「가격이 Opus 5.5와 같다」는 보도가 있지만(Decrypt), 우리가 볼 숫자는 단가가 아니라 한 건당 비용이다.

**2. 어디서 쓸 수 있나.** 가장 점수가 높은 Wonder Full은 구독 안에서만 쓸 수 있어, 우리 자동화에 API로 붙일 수 없다. API로 쓸 수 있는 것은 점수가 한 단계 낮은 Wonder다.

**3. 내 코드와 글이 어디로 가나.** 메타의 Muse Code 구독 안내에 따르면 구독은 기본값이 「Contributor 모드」로, 내 프롬프트·코드·파일·맥락과 받은 답을 메타가 앞으로의 모델 학습에 쓰는 대신 사용량을 더 준다. 끄면 그 뒤의 내용은 학습에 쓰이지 않는다고 안내에 적혀 있지만, 이미 보낸 내용이 어떻게 되는지는 안내에 없어 확인하지 못했다. API로 쓰는 Wonder에는 이 모드가 없고, 표준 모드의 내용은 학습에 쓰이지 않는다고 한다. 메타의 이용 약관 원문은 직접 열어 보지 못했으므로, 쓰기 전에 약관과 설정 화면에서 확인해야 한다.

## 이 소식에서 확인하지 못한 것

메타의 공식 발표 글과 모델 카드는 직접 열지 못했다. 위 「회사가 발표한 것」은 TechCrunch·Decrypt·iThome 등 보도를 통해 확인한 내용이다. 구독과 학습 설정은 메타의 Muse Code 구독 안내 페이지를 직접 열어 확인했다. 메타가 약속한 전체 안전 보고서는 아직 나오지 않았다고 Decrypt는 전했다. 실사용자 Simon Willison은 Wonder에 추론 수준 여섯 단계(minimal~max)가 있고 이전 모델보다 그림이 나아진 것 같다고 적었지만, 그림 하나로 본 비공식 시험이라고 스스로 밝혔다. 이 정도를 점수로 읽으면 안 된다.

## 우리 생각

**사실:** 메타가 API와 구독으로만 쓰는 최상위 모델을 냈고, 회사 지표와 독립 지표의 그림이 다르며, 가장 높은 모델은 구독 전용이고, 구독의 기본 설정은 내 콘텐츠를 학습에 쓴다.

**해석:** 새 모델이 나올 때마다 「1등이다」와 「3등이다」가 동시에 나온다. 둘 다 거짓이 아닐 수 있다. 누가 만든 시험인지, 어떤 설정에서 쟀는지가 다르기 때문이다.

**우리라면:** 숫자로 갈아타지 않는다. 우리 일 20건(대본 초안, 상품 설명, 댓글 분류)을 같은 조건으로 돌려 「한 건당 비용」과 「고친 횟수」를 적고, 사람이 확인한 뒤에만 내보낸다. 고객 정보와 미공개 자료는 학습에 쓰일 수 있는 설정에는 넣지 않는다.

## 함께 읽은 글

성격이 다른 출처를 직접 열어 확인했다. 수치는 각 출처 기준이다.

- [Meta releases its first frontier model, Muse Wonder (TechCrunch)](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder) — 영어, 보도
- [Muse Wonder / Wonder Full 평가 (Artificial Analysis)](https://artificialanalysis.ai/articles/muse-wonder) — 영어, 독립 평가기관
- [Meta Muse Wonder and the frontier AI race (Decrypt)](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race) — 영어, 보도(회사 지표 대 독립 지표)
- [Meta's best model skips API, coding plan trains on your code (LetsDataScience)](https://letsdatascience.com/blog/metas-best-model-skips-api-coding-plan-trains-on-your-code) — 영어, 구독·학습 설정
- [llm-meta-ai 0.2 (Simon Willison)](https://simonwillison.net/2026/Oct/12/llm-meta-ai/) — 영어, 실사용자 블로그
- [Meta releases Muse Wonder, its first frontier-class AI model (AI Weekly)](https://aiweekly.co/alerts/meta-releases-muse-wonder-its-first-frontier-class-ai-model) — 영어, 뉴스레터(타 매체 요약)
- [Muse Code Subscriptions (Meta)](https://dev.meta.ai/docs/muse-code/subscriptions) — 영어, 메타 공식 안내
- [Models Leaderboard (Artificial Analysis)](https://artificialanalysis.ai/leaderboards/models) — 영어, 독립 평가기관 순위표
- [Meta's Muse Wonder (DataNorth)](https://datanorth.ai/news/metas-muse-wonder) — 영어, 분석(요금제·학습 설정)
- [Muse Wonder 보도 (iThome)](https://www.ithome.com.tw/news/179608) — 중국어(번체), 보도
