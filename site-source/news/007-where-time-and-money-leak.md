---
no: 7
slug: where-time-and-money-leak
date: 2026-10-03
category: 실전
tags: 메모리 · 비용 · 업무 효율
title: AI로 일할 때 시간과 돈이 새는 세 군데
summary: 매번 같은 설명을 반복하고, 끝나길 기다리고, 읽지도 않는 데이터에 돈을 냅니다. 새는 곳 세 군데와 막는 방법입니다.
---
> 이 글은 AI와 함께 초안을 만들고 편집자가 검수했습니다. 외부 글을 참고했고, 참고한 글은 맨 아래에 밝혔습니다.

AI 도구는 대개 느려서가 아니라 **쓰는 방식 때문에** 시간과 돈이 샙니다. 우리가 점검하는 세 군데입니다.

## 1. 같은 설명의 반복

새 대화를 열 때마다 프로젝트 소개를 처음부터 다시 쓰고 있다면 첫 번째 누수입니다. 해법은 간단합니다. 항상 먼저 읽히는 **안내 문서 한 장**에 프로젝트의 목적, 금지 사항, 용어를 적어 둡니다. 이 문서는 짧아야 합니다. 길어지면 앞의 글에서 말했듯 오히려 흐려집니다. 우리는 프로젝트 문서함과 안내 문서로 이 일을 하고, 한 장을 넘기지 않으려 합니다.

## 2. 기다리는 시간

빌드, 배포, 대량 변환처럼 오래 걸리는 일을 시켜 놓고 화면을 지켜보고 있다면 두 번째 누수입니다. 오래 걸리는 일은 **백그라운드로 돌리고 그동안 다른 일을 시키는 것**이 기본입니다. 같은 일을 순서대로 하면 합계만큼, 동시에 하면 가장 긴 것만큼 걸립니다. 조사처럼 결과가 길게 쏟아지는 일은 별도 작업자에게 맡기고 **요약만 받아 오게** 하면 내 작업 화면이 어지러워지지 않습니다.

## 3. 읽지도 않는 데이터에 내는 비용

참고한 글은 코딩 에이전트에 로그 파일이나 대용량 덤프를 통째로 넣으면 대부분이 모델에게 필요 없는 반복·공백이라 비용만 든다고 지적합니다. 그 글이 소개한 도구가 실제로 얼마나 줄여 주는지는 우리가 검증하지 못했으니 효과는 약속하지 않습니다. 그러나 원칙은 도구 없이도 적용됩니다. **기계가 뱉은 긴 텍스트는 사람이 먼저 필요한 부분만 잘라서 넣습니다.** 오류 로그라면 오류가 난 앞뒤 스무 줄이면 충분한 경우가 많습니다.

## 점검표

- 이번 주 같은 설명을 몇 번 반복했는가
- 오래 걸리는 일을 기다리느라 멈춘 적이 있는가
- 긴 로그·표를 통째로 넣은 적이 있는가

세 질문에 하나라도 「예」라면 그 줄부터 고칩니다.

## 함께 읽은 글

이 글은 아래 글들의 문제의식을 참고해, 우리 팀의 관점과 기준으로 다시 썼습니다. 문장과 구성은 따르지 않았고, 원 글이 인용한 수치는 우리가 원자료까지 직접 확인하지 못한 것은 그렇게 표시했습니다. 일부 원 글은 로그인 후 전문이 열려, 공개된 부분 기준으로 읽었습니다.

- [클로드 대기 시간 없애는 세 가지, 복붙하면 끝납니다 (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-wait)
- [코딩 에이전트 요금, 눈 뜨고 코 베이고 계십니다 (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-headroom)

다른 출처에서 함께 확인한 자료:

- [Prompt caching (Claude Platform Docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — 영문
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 영문
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — 영문
