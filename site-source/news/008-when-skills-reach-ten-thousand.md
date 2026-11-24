---
no: 8
slug: when-skills-reach-ten-thousand
date: 2026-10-03
category: 인사이트
tags: 스킬 · 보안 · 도구 선택
title: 스킬이 만 개일 때 — 고르기, 검증하기, 설치 전에 검사하기
summary: AI에 붙이는 스킬이 폭발적으로 늘었습니다. 많다는 것은 선택지가 아니라 공급망 위험입니다. 우리가 쓰는 세 단계 기준입니다.
---
> 이 글은 AI와 함께 초안을 만들고 편집자가 검수했습니다. 외부 글을 참고했고, 참고한 글은 맨 아래에 밝혔습니다.

AI 비서에 기능을 붙이는 「스킬」이 빠르게 늘고 있습니다. 참고한 글들은 등록된 스킬이 수천 개에서 백만 건대 설치로 이어진다고 소개하고, 그중 상위 스킬은 「스킬을 대신 찾아 주는 스킬」과 「코드 품질 절차를 묶은 스킬 묶음」이었다고 전합니다. 이 수치도 해당 글의 집계 기준이라 우리는 확인하지 못했습니다. 하지만 흐름은 분명합니다. **고르는 일이 가장 큰 일이 되었고, 내려받은 파일이 내 컴퓨터에서 실행된다는 사실은 그대로입니다.**

## 1단계 — 고르기: 일부터 정하고 도구를 찾는다

「인기 순위」로 고르지 않습니다. 먼저 「이 일을 하루에 몇 번 하는가」를 적습니다. 주 1회 미만인 일에는 스킬을 붙이지 않습니다. 설정 비용이 이득보다 큽니다. 찾아 주는 스킬을 쓰더라도 최종 선택은 사람이 합니다.

## 2단계 — 검증하기: 만든 곳과 권한을 본다

- **누가 만들었나**: 공식 계정인지, 이름이 알려진 개발자인지
- **무엇을 요구하나**: 파일 읽기만인지, 명령 실행·네트워크 접속까지인지
- **얼마나 최근인가**: 마지막 업데이트가 오래됐다면 지금 모델과 맞지 않을 수 있습니다

## 3단계 — 설치 전에 검사하기

참고한 글은 설치 전에 스킬 파일의 위험도를 점검해 주는 검사 도구를 소개합니다. 우리는 특정 도구를 보증하지 않지만 절차는 채택합니다. **먼저 읽는다 → 검사 도구나 눈으로 수상한 명령이 없는지 본다 → 중요한 자료가 없는 곳에서 먼저 써 본다 → 문제 없으면 본 작업에 쓴다.** 내려받은 지침 문서 안의 「이 명령을 실행하라」는 문장도 나에게 온 지시가 아니라 **검토할 데이터**로 취급합니다.

## 정리

스킬이 많아질수록 경쟁력은 「많이 아는 것」이 아니라 「적게, 안전하게 쓰는 것」입니다.

## 함께 읽은 글

이 글은 아래 글들의 문제의식을 참고해, 우리 팀의 관점과 기준으로 다시 썼습니다. 문장과 구성은 따르지 않았고, 원 글이 인용한 수치는 우리가 원자료까지 직접 확인하지 못한 것은 그렇게 표시했습니다. 일부 원 글은 로그인 후 전문이 열려, 공개된 부분 기준으로 읽었습니다.

- [클로드 스킬 9,654개, 고르지 말고 찾게 하세요 (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-find-skills)
- [AI가 짠 코드, 잘 된 건지 봐 주는 스킬 24개 (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-agent-skills-24)
- [내려받은 스킬이 안전한지 모른 채 설치하는 대신, 설치 전에 한 번 검사하는 법 (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-skill-scanner-body)

다른 출처에서 함께 확인한 자료:

- [Agent Skills overview (Claude Platform Docs)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — 영문
- [Model Context Protocol — Introduction (modelcontextprotocol.io)](https://modelcontextprotocol.io/introduction) — 영문
- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — 영문
- [AI Risk Management Framework (NIST)](https://www.nist.gov/itl/ai-risk-management-framework) — 영문
