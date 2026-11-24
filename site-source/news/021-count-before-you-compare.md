---
no: 21
slug: count-before-you-compare
date: 2026-10-09
category: 인사이트
tags: 숫자 읽기 · 매출 회계 · 토큰 가격 · 건당 비용
title: 숫자를 비교하기 전에 셈법부터 — 매출 700억 달러가 500억 달러가 된 이유와 토큰 값의 함정
summary: 같은 「연환산 매출」과 같은 「토큰당 가격」도 무엇을 세느냐에 따라 달라집니다. 이번 주 보도 두 건으로 숫자를 읽는 법을 정리했습니다.
---
> 이 글은 AI(Claude)와 함께 초안을 만들고 편집자가 검수했습니다. 앤트로픽과 OpenAI가 모두 등장하고, 앤트로픽은 Claude를 만든 회사라 이해관계가 있습니다. 어느 회사나 종목에 대한 투자 의견이 아니며, 숫자는 모두 보도와 회사 발표에서 옮긴 것입니다.

이번 주 AI 업계에서 가장 눈에 띈 숫자 이야기는 성능이 아니라 「셈법」이었습니다.

## 사례 1. 같은 회사의 매출이 700억에서 500억 달러가 된 이유

Axios는 10월 8일, OpenAI의 연환산 매출이 지난달 널리 보도된 700억 달러가 아니라 500억 달러라고 전했습니다. 700억 달러는 투자자에게 공유된 자료에서 나온 숫자로, 앤트로픽과 더 바로 비교하려고 「부풀려(gross up)」 계산한 것이라고 합니다. 차이는 클라우드 파트너를 통해 팔리는 몫을 어떻게 기록하느냐입니다. Axios가 인용한 회계학 교수에 따르면 앤트로픽은 고객이 클라우드 사업자를 통해 100을 내면 100 전체를 매출로 잡고 사업자 몫을 비용으로 적을 수 있고, OpenAI는 일부 파트너 판매에서 자기 몫만 매출로 잡습니다. 두 회사 모두 회계기준(GAAP)에는 맞는다고 합니다.

로이터도 10월 9일, OpenAI가 투자자에게 밝힌 9월 연환산 매출이 500억 달러에 조금 못 미친다고 전했습니다. 앞서 700억 달러에 가깝다고 내비친 숫자와의 차이는 앤트로픽과 바로 비교하려던 데서 나왔고, OpenAI는 앤트로픽과 달리 AWS·구글 클라우드 같은 클라우드 파트너를 통한 판매를 매출에 넣지 않는다는 설명입니다(파이낸셜타임스가 먼저 보도).

연환산 매출은 한 기간의 판매를 1년으로 늘려 본 실리콘밸리식 지표이고, Axios는 공개 시장 투자자들은 보통 실제 매출을 더 선호한다고 덧붙였습니다(Axios·로이터 보도 기준이며, 우리는 두 회사의 회계 자료를 직접 보지 못했습니다).

## 사례 2. 토큰당 값이 내려가도 건당 값은 다를 수 있다

앤트로픽은 Haiku 5.5의 값을 이전 Haiku 4.5보다 평균 약 75% 낮췄다고 발표했습니다(회사 발표). 그런데 Next.ink는 외부 분석 기관의 결과를 인용해 이 모델이 더 길게 답하는 편이라 절감폭이 노력 설정에 달린다고 전했고, 10만 토큰을 넘는 요청은 단가가 5배 높아진다는 점도 짚었습니다. AI Weekly 뉴스레터도 비용 부담으로 더 싼 모델로 옮기는 회사들을 다루며 「완료한 작업 한 건당 비용」을 재라고 조언합니다(이 이슈는 다른 매체 보도를 요약한 것이라 우리가 원보도를 확인하지는 못했습니다).

## 숫자를 읽는 세 가지 질문

1. **무엇을 센 숫자인가?** 총액인가 순액인가, 토큰인가 완료한 일 한 건인가.
2. **누가 낸 숫자인가?** 회사가 직접 발표한 것인가, 독립 기관이 잰 것인가, 둘이 다르면 측정 조건은 무엇인가.
3. **조건을 바꾸면 어떻게 되나?** 최고 노력 단계 기준 점수는 기본 단계에서 달라질 수 있고, 긴 요청에서는 단가가 바뀔 수 있다.

## 우리의 해석

**사실:** 같은 회사의 연환산 매출이 셈법에 따라 700억 달러와 500억 달러로 달리 보고됐고, 토큰 단가의 하락률과 건당 비용의 하락률은 반드시 같지 않다는 지적이 이번 주 나왔습니다.

**해석:** 숫자는 단위와 셈법이 같을 때만 비교할 수 있습니다. 회사 사이를 비교할 때뿐 아니라 우리 자신의 숫자를 볼 때도 마찬가지입니다.

**우리라면:** 우리 수익 보고에서 총액·순액을 구분해 쓰고, AI 작업은 토큰이 아니라 「글 한 편, 영상 한 편, 주문 한 건」당 비용으로 기록합니다. 다른 회사 숫자를 인용할 때는 항상 출처와 셈법을 같이 적습니다.

## 함께 읽은 글

성격이 다른 다섯 가지 출처를 직접 열어 확인했습니다.

- [OpenAI annualized revenue $20 billion less than previously reported (Axios)](https://www.axios.com/2026/10/08/openai-50-billion-arr-anthropic-revenue-accounting) — 영문, 보도
- [OpenAI's September annualized revenue nears $50 bln, less than previously indicated (Reuters, Zawya 게재)](https://www.zawya.com/en/special-coverage/openais-september-annualized-revenue-nears-50bln-less-than-previously-indicated-source-says-1586243) — 영문, 통신 보도
- [Introducing Claude Haiku 5.5 (Anthropic)](https://www.anthropic.com/claude-haiku-5-5) — 영문, 회사 공식 발표
- [Chez Anthropic, Haiku 5.5 prend la relève des petits modèles rapides (Next.ink)](https://next.ink/260659/chez-anthropic-haiku-5-5-prend-la-releve-des-petits-modeles-rapides/) — 프랑스어, 매체 분석
- [AI got too expensive, so companies are moving to cheaper models (AI Weekly #535)](https://aiweekly.co/issues/ai-got-too-expensive-so-companies-are-moving-to-cheaper) — 영문, 뉴스레터
