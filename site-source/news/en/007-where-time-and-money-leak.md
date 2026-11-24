---
no: 7
slug: where-time-and-money-leak
date: 2026-10-03
category: Practice
tags: Memory · Cost · Work efficiency
title: Three Places Where Time and Money Leak When You Work With AI
summary: You repeat the same explanation every time, you wait for jobs to finish, and you pay for data nobody reads. Here are the three leaks and how to plug them.
---
> This article was drafted together with AI and reviewed by an editor. It draws on an external article, which is credited at the bottom.

With AI tools, time and money usually leak not because the tools are slow but **because of how we use them**. Here are the three places we check.

## 1. Repeating the same explanation

If you rewrite the project introduction from scratch every time you open a new conversation, that is the first leak. The fix is simple: put the project's purpose, prohibitions and terminology in **a single guide document** that is always read first. This document must be short. If it gets long, as noted in an earlier article, it actually becomes blurred. We do this with a project document store and a guide document, and we try not to go beyond one page.

## 2. Waiting time

If you assign something long-running, like a build, a deployment or a bulk conversion, and then sit watching the screen, that is the second leak. For long jobs, the default is **to run them in the background and give other work in the meantime**. Doing things in sequence takes the sum of their times; doing them at once takes only as long as the longest. For work like research that produces a long stream of results, hand it to a separate worker and **have it bring back only a summary**, so your own working screen does not get cluttered.

## 3. Paying for data nobody reads

The article we referred to points out that when you feed a coding agent a log file or a large dump whole, most of it is repetition and blank space the model does not need, so it only adds cost. We could not verify how much the tool that article introduced actually reduces, so we do not promise any effect. The principle, though, applies even without a tool. **For long machine-generated text, a person first cuts out only the parts that are needed before feeding it in.** For an error log, the twenty lines before and after the error are often enough.

## Checklist

- How many times did you repeat the same explanation this week?
- Have you ever stopped to wait for a long-running job?
- Have you ever fed in a long log or table whole?

If even one of the three is a "yes," fix that line first.

## Further reading

This article was rewritten from our own team's perspective and standards, drawing on the concerns raised in the articles below. We did not follow their wording or structure, and where we could not verify a figure an original article cited against the primary data, we marked it as such. For some of the original articles, the full text opens only after logging in, so we read them based on the publicly available portion.

- [Three Ways to End Claude's Waiting Time — Just Copy and Paste (Korean) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-wait)
- [Your Coding Agent Bill: You're Getting Fleeced With Your Eyes Open (Korean) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-headroom)

Also checked against other sources:

- [Prompt caching (Claude Platform Docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — English
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — English
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — English
