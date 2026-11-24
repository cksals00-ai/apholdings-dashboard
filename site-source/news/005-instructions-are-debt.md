---
no: 5
slug: instructions-are-debt
date: 2026-10-03
category: 인사이트
tags: 지침 · 프롬프트 · 정리
title: AI에게 주는 지침은 자산이 아니라 부채입니다 — 분기마다 지워 보는 이유
summary: 규칙을 쌓을수록 AI가 똑똑해진다는 믿음은 틀렸을 수 있습니다. 지침을 줄이고, 줄여도 문제없는지 측정하는 방법을 정리했습니다.
---
> 이 글은 AI와 함께 초안을 만들고 편집자가 검수했습니다. 외부 글을 참고했고, 참고한 글은 맨 아래에 밝혔습니다.

AI에게 일을 시킬 때 우리는 틀릴 때마다 규칙을 한 줄씩 보탭니다. 「표는 쓰지 마」, 「존댓말로」, 「출처를 붙여」. 몇 달이 지나면 지침 문서는 스무 줄, 서른 줄이 되고, 우리는 그것을 자산이라고 부릅니다. 그런데 이 규칙들이 정말 일을 하고 있는지 확인해 본 적은 거의 없습니다.

## 규칙은 늘리기 쉽고, 효과는 확인하기 어렵다

참고한 글은 이런 주장을 합니다. 모델이 좋아지면 예전에 필요했던 규칙이 이미 필요 없어지고, 필요 없는 규칙은 해를 끼치지 않는 게 아니라 **지켜야 할 것의 총량을 늘려 중요한 규칙까지 흐리게 만든다**는 것입니다. 이 글은 지시 개수가 많아질수록 준수율이 떨어진다는 벤치마크 연구를 근거로 듭니다. 다만 그 수치는 우리가 원문까지 확인하지 못했으니, 「그런 연구가 있다」는 정도로만 받아들입니다. 실무에서 더 중요한 것은 방향입니다. **규칙이 많을수록 AI는 말없이 일부를 빼먹을 수 있고, 우리는 무엇이 빠졌는지 모릅니다.**

## 우리가 정한 정리 기준

1. **분기에 한 번, 지침을 통째로 비워 봅니다.** 같은 작업을 지침 없이 돌려 결과를 봅니다.
2. **한 줄씩 다시 넣으며 차이를 봅니다.** 넣어도 결과가 안 달라지면 그 줄은 지웁니다.
3. **「왜」가 적혀 있지 않은 규칙은 의심합니다.** 이유를 설명하지 못하는 규칙은 사고 한 번의 흔적일 때가 많습니다.
4. **금지보다 기준을 둡니다.** 「~하지 마」 열 줄보다 「이 글의 독자는 누구다」 한 줄이 더 많이 바꿉니다.
5. **되돌릴 수 없는 행동에 대한 규칙은 지우지 않습니다.** 삭제·결제·발송·공개 게시 규칙은 성능과 무관하게 남깁니다.

## 정리

지침은 쌓아 두는 재산이 아니라 유지비가 드는 설비입니다. 줄여 보고, 차이가 없으면 줄인 채로 가는 편이 가볍고 안전합니다.

## 함께 읽은 글

이 글은 아래 글들의 문제의식을 참고해, 우리 팀의 관점과 기준으로 다시 썼습니다. 문장과 구성은 따르지 않았고, 원 글이 인용한 수치는 우리가 원자료까지 직접 확인하지 못한 것은 그렇게 표시했습니다. 일부 원 글은 로그인 후 전문이 열려, 공개된 부분 기준으로 읽었습니다.

- [AI가 멍청해진 게 아닙니다 — 반년 전에 쓴 지침이 발목을 잡는 겁니다 (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-claude-md-rules)

다른 출처에서 함께 확인한 자료:

- [How Many Instructions Can LLMs Follow at Once? (IFScale, arXiv)](https://arxiv.org/abs/2507.11538) — 영문
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — 영문
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 영문
- [Lost in the Middle: How Language Models Use Long Contexts (arXiv)](https://arxiv.org/abs/2307.03172) — 영문
