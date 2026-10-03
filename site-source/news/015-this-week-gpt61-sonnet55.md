---
no: 15
slug: this-week-gpt61-sonnet55
date: 2026-10-03
category: 주간 소식
tags: 주간 AI 소식 · GPT-6.1 Sol · Claude Sonnet 5.5 · Gemini 4 Argon
title: 이번 주 AI 소식 — 두 회사는 「더 싸게」, 구글은 「더 강하게, 일부에게 먼저」
summary: 9월 마지막 주, OpenAI와 앤트로픽은 같은 일을 더 싸게 하는 모델을, 구글은 Gemini 4 Argon을 일부에게 먼저 공개했습니다. 무엇이 바뀌었고 일하는 사람에게 무슨 뜻인지 공식 자료로 확인해 정리했습니다.
---
> 이 글은 AI(Claude)와 함께 초안을 만들고 편집자가 검수했습니다. 앤트로픽은 이 글을 쓰는 데 쓴 Claude를 만든 회사입니다. 이해관계가 있을 수 있어 모든 수치를 「회사가 발표한 것」으로 표시하고, 다른 회사 소식도 같은 기준으로 다뤘습니다.

> **정정 (2026-10-03)** 처음 올린 글에는 「구글 공식 자료에서 Gemini 4 출시를 확인하지 못했다」고 적었습니다. 구글은 9월 30일 공식 블로그에서 Gemini 4 Argon을 발표했습니다. 제목, 첫 문단, 3번 항목을 바로잡고 출처를 추가했습니다.

이번 주(9월 28일~10월 3일) 큰 발표는 세 건이었습니다. OpenAI와 앤트로픽은 **성능을 올렸다는 말보다 값을 내렸다는 말이 먼저** 나왔고, 구글은 가장 강한 새 모델을 일부에게 먼저 여는 쪽을 택했습니다.

## 1. OpenAI — GPT-6.1 Sol

OpenAI는 GPT-6.1 Sol을 소개하며 「이전 최상위 모델(GPT-6 Astra)에 가까운 지능을 훨씬 낮은 비용으로」라고 설명합니다. 개발자 가격은 입력 100만 토큰당 2달러, 출력 10달러, 반복해서 쓰는 입력은 0.10달러입니다. OpenAI는 코딩·업무 자동화 평가에서 Astra와 비슷한 점수를 약 5분의 1 비용으로 냈다고 발표했습니다. 또 낮은 추론 강도에서 사실 오류율이 11.4%에서 7.7%로 줄었다고 합니다. (모두 OpenAI 발표 수치입니다.)

**알아둘 점:** OpenAI 페이지 기준으로 ChatGPT의 「Work」와 Codex에서 먼저 열렸고, 일반 채팅에는 아직 아닙니다. 유료 요금제(Plus·Pro·Business·Enterprise·Edu)가 대상입니다.

## 2. 앤트로픽 — Claude Sonnet 5.5

앤트로픽은 Sonnet 5.5를 「이전 Sonnet 5보다 30% 이상 빠르고, 대부분의 작업에서 비용이 최대 30% 적다」고 소개합니다. 토큰 단가는 그대로(입력 2달러, 출력 10달러)이고, 같은 일을 **더 적은 토큰으로** 끝내서 값이 줄어든다는 설명입니다. 같은 달 22일에는 상위 모델 Opus 5.5가 나왔는데, 앤트로픽은 이 모델이 「Opus 5보다 평소 작업 기준 40% 적은 비용으로 돈다」고 합니다. 앤트로픽은 Sonnet 5.5를 문서·슬라이드·스프레드시트 만들기, 버그 수정 같은 범위가 분명한 일상 작업용으로, Opus 5.5는 판단이 필요한 복잡한 일용으로 나눠 놓았습니다. 프랑스 IT 매체 Next.ink는 단가가 안 내려간 점을 짚으면서, 효율로 값이 내려가는 구조라고 정리했습니다.

## 3. 구글 — Gemini 4 Argon, 가장 강한 모델은 일부에게 먼저

구글은 9월 30일 공식 블로그에서 Gemini 4 Argon을 발표했습니다. 처음에는 구글의 Fairwind 프로그램을 통해 신뢰할 수 있는 사이버 보안 방어자에게만 열고, 안전장치를 다듬은 뒤 유료 API 고객과 Google AI Ultra 구독자부터 넓힌다고 밝혔습니다. 두 회사가 「값」을 앞세운 것과 달리 구글은 「가장 강한 모델을 조심스럽게 연다」를 앞세운 셈입니다. 성능 수치는 구글 발표 외의 독립 검증을 확인하지 못해 옮기지 않습니다.

**알아둘 점:** 10월 1일 갱신된 개발자 모델 문서에서 지금 바로 쓸 수 있는 안정판은 Gemini 3.8 Flash(장시간 개발 작업·에이전트용), 이미지용 Nano Banana Pro(4K·글자 표현), 음성용 Gemini 3.8 Live입니다. 사람 투표 순위 사이트 Arena에도 Gemini 4 Argon이 올라와 있습니다. 자세한 건 이번 주 함께 올린 「누가 많이 쓰이나」 편을 보세요.

## 우리의 해석

**사실:** 두 회사가 같은 주에 「같은 일을 더 싸게」를 내걸었습니다.

**해석:** 모델이 좋아져서가 아니라 **쓰는 값이 내려가서** 개인과 작은 회사의 선택지가 바뀝니다. 매일 돌리는 일이라면 성능 점수보다 「한 건 처리하는 데 드는 돈」이 더 중요해졌습니다.

**우리라면:** 지금 쓰는 도구를 바꾸기 전에, 매주 하는 일 세 가지를 골라 두 모델에 똑같이 시켜 보고 시간과 결과를 적어 둡니다. 방법은 「작업별로 어떤 AI를 쓸까」 편에 있습니다.

## 함께 읽은 글

이 글은 아래 공식 발표와 보도를 직접 열어 확인해 쓴 것입니다. 수치는 각 회사의 발표이며, 독립 검증을 거친 것이 아닙니다.

- [Introducing GPT-6.1 Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-1-sol/) — 영문
- [Claude Sonnet 5.5 (Anthropic)](https://www.anthropic.com/claude-sonnet-5-5) — 영문
- [Claude Opus 5.5 (Anthropic)](https://www.anthropic.com/claude-opus-5-5) — 영문
- [Claude Sonnet 5.5 : plus rapide, plus efficace, mais pas moins cher (Next.ink)](https://next.ink/brief-article/claude-sonnet-5-5-plus-rapide-plus-efficace-mais-pas-moins-cher/) — 프랑스어
- [Gemini models (Google AI for Developers)](https://ai.google.dev/gemini-api/docs/models) — 영문
- [Gemini 4 Argon: our next era of frontier intelligence (Google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) — 영문
