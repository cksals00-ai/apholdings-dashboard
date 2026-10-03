---
no: 17
slug: which-ai-for-which-job
date: 2026-10-03
category: 实践
tags: 选模型 · 按任务推荐 · 成本 · 亲自测试
title: 按任务选用哪种 AI——各公司自己公布的用途和我们使用的测试方法
summary: 从文档、编码、语音、图像到批量处理。汇总各公司在官方资料中写明的推荐用途，并整理出 30 分钟判断是否适合自己工作的方法。
---
> 本文由 AI（Claude）协助起草，编辑已审校。由于也涉及开发 Claude 的 Anthropic，我们只以**各公司关于自家产品所写的文档**为依据，这不是相互比较的独立测试结果。我们不会说哪一方更好。

“这件事用哪个 AI 好？”很难用一句话回答。不过，**各公司推荐什么用途**，官方文档里都写着。我们按任务把它们汇总了起来。

## 各公司按任务推荐的内容

- **日常文档、幻灯片、电子表格，范围明确的 bug 修复：** Anthropic 将 Claude Sonnet 5.5 推荐用于这类用途。它是更快、更便宜的一方。
- **长而复杂的开发工作（大规模代码迁移、检查）：** Anthropic 推荐 Opus 5.5，OpenAI 推荐 GPT-6.1 Sol（编码、计算机操作、专业业务）。两家都以自家发布的形式给出了这一用途的分数。
- **长时间开发工作、自动执行任务的智能体：** 谷歌文档把 Gemini 3.8 Flash 介绍为适合这一用途。
- **语音助手、语音合成：** 谷歌推荐低延迟语音对话用 Gemini 3.8 Live，富有表现力的语音合成用 Gemini 3.8 Flash TTS。
- **图像：** 谷歌推荐 Nano Banana Pro 用于 4K 分辨率和含文字的复杂构图，Nano Banana 2 用于快速批量制作。
- **成本最重要且量大的工作：** Anthropic 文档建议从 Haiku 级的小模型开始，不够再升级；谷歌则推荐 Gemini 3.1 Flash-Lite。

## 降低成本，不只是换模型

Anthropic 文档建议，在更换模型之前，先试试用**“effort（投入程度）设置”来调节智能与速度、成本**。此外，两家公司都提供“缓存”，重复使用相同输入时费用会大幅下降（OpenAI 为 0.10 美元，Anthropic 为 0.20 美元，均为每 100 万 token）。如果每次都要附上同样的指令，效果会很明显。

## 30 分钟测试法

我们按自己的方式精简了 Anthropic 文档建议的步骤。

1. 选出每周都做的三件事（例如整理会议纪要、起草客户回复、整理表格）。
2. 各准备一份去掉个人信息的真实资料。
3. 把同样的指令原样输入两个工具。
4. 记下准确度、需要修改的地方数量、所用时间这三项。
5. 分数相近就选便宜的一方；如果是一次都不能出错的工作，就选分数高的一方。

## 我们的解读

**事实：** 各公司按用途分开介绍，分数取自自家的评测。

**解读：** 不存在“最好的 AI”，只有“适合我工作的最便宜的 AI”。公司发布的分数只是起点，标准是用我自己的资料验证出的结果。

**如果是我们：** 不把所有工作都压在一个工具上，轻松的工作交给小模型，只有难的工作交给大模型。并且每三个月把同样的测试重新跑一遍。因为模型更新的速度很快。

## 一同阅读的文章

所有内容都是我们直接打开下列官方文档核实的。分数和用途均为各公司的主张。

- [Choosing a model (Anthropic Docs)](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) — 英文
- [Claude Sonnet 5.5 (Anthropic)](https://www.anthropic.com/claude-sonnet-5-5) — 英文
- [Introducing GPT-6.1 Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-1-sol/) — 英文
- [Gemini models (Google AI for Developers)](https://ai.google.dev/gemini-api/docs/models) — 英文
