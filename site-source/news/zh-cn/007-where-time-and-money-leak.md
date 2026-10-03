---
no: 7
slug: where-time-and-money-leak
date: 2026-10-03
category: 实践
tags: 记忆 · 成本 · 工作效率
title: 用 AI 工作时，时间和金钱流失的三个地方
summary: 每次重复同样的说明，干等着任务完成，还为根本不会读的数据付费。这是流失的三个地方及堵住它们的方法。
---
> 本文由 AI 协助起草，编辑已审校。参考了外部文章，参考的文章列于文末。

AI 工具上的时间和金钱流失，通常不是因为慢，而是**因为使用方式**。以下是我们检查的三个地方。

## 1. 重复同样的说明

如果每次新开对话都要从头重写项目介绍，这就是第一个漏洞。解法很简单：在总会被最先读取的**一页说明文档**里，写下项目的目的、禁止事项和术语。这份文档必须简短。变长了，就像前一篇文章所说，反而会变淡。我们用项目文档库和说明文档来做这件事，并尽量不超过一页。

## 2. 等待的时间

构建、部署、批量转换这类耗时的工作，交代下去后就盯着屏幕看，这是第二个漏洞。耗时的工作，基本做法是**放到后台运行，同时让它做别的事**。同样的事按顺序做，耗时是各项之和；同时做，则只取决于最长的一项。像调研这样结果会大量涌出的工作，交给单独的执行者，**只拿回摘要**，我的工作界面就不会变得杂乱。

## 3. 为根本不会读的数据付费

所参考的文章指出，把日志文件或大体量转储整个丢给编码代理，其中大部分对模型来说是不必要的重复和空白，只是徒增成本。该文所介绍的工具究竟能节省多少，我们没有验证，因此不承诺其效果。但这一原则即使没有工具也适用。**机器吐出的长文本，由人先截取需要的部分再放进去。** 如果是错误日志，出错位置前后二十行往往就足够了。

## 检查清单

- 这周同样的说明重复了几次
- 有没有因为等待耗时的工作而停下来过
- 有没有把长日志、长表格整个塞进去过

三个问题中只要有一个回答“是”，就从那一条开始改。

## 一同阅读的文章

本文参考了下列文章的问题意识，并以我们团队的视角和标准重新写成。我们没有沿用其语句和结构；原文所引用的数字，凡是我们未能亲自核实原始资料的，均已如此标明。部分原文需登录后才能看到全文，因此我们是依据公开部分阅读的。

- [消除 Claude 等待时间的三个办法，复制粘贴就行（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-wait)
- [编码代理的费用，你正睁着眼睛吃大亏（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-headroom)

同时对照的其他来源:

- [Prompt caching (Claude Platform Docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — 英文
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 英文
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — 英文
