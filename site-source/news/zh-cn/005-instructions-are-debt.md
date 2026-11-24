---
no: 5
slug: instructions-are-debt
date: 2026-10-03
category: 洞察
tags: 指令 · 提示词 · 整理
title: 给 AI 的指令不是资产而是负债——我们为何每季度清空一次
summary: “规则越积越多，AI 就越聪明”这种想法可能是错的。这里整理了精简指令，并衡量精简后是否仍无问题的方法。
---
> 本文由 AI 协助起草，编辑已审校。参考了外部文章，参考的文章列于文末。

让 AI 干活时，每次出错我们都会添一行规则。“不要用表格”“用敬语”“附上出处”。几个月后，指令文档变成二十行、三十行，我们把它称为资产。可是，这些规则是否真的在起作用，我们几乎从未确认过。

## 规则容易增加，效果却难以确认

所参考的文章提出这样的主张：模型变好之后，以前必需的规则已经不再需要；不需要的规则并非无害，而是**增加了需要遵守的总量，连重要的规则也被冲淡**。该文以“指令数量越多，遵从率越低”的基准研究为依据。不过那个数字我们没能核实到原文，所以只当作“有这样的研究”来接受。在实务中更重要的是方向。**规则越多，AI 就越可能悄悄漏掉一部分，而我们不知道漏掉了什么。**

## 我们定下的整理标准

1. **每季度一次，把指令整个清空。** 在没有指令的情况下运行同样的任务，看结果。
2. **一行一行重新加回去，观察差异。** 加了结果也没变的那一行，就删掉。
3. **没写“为什么”的规则要存疑。** 说不出理由的规则，往往只是一次事故留下的痕迹。
4. **立标准，而不是立禁令。** 比起十行“不要……”，一行“这篇文章的读者是谁”改变得更多。
5. **关于无法挽回的操作的规则，不删。** 删除、支付、发送、公开发布的规则，与性能无关，一律保留。

## 小结

指令不是存起来的财产，而是需要维护成本的设备。试着精简，没有差别就保持精简后的状态，这样更轻便也更安全。

## 一同阅读的文章

本文参考了下列文章的问题意识，并以我们团队的视角和标准重新写成。我们没有沿用其语句和结构；原文所引用的数字，凡是我们未能亲自核实原始资料的，均已如此标明。部分原文需登录后才能看到全文，因此我们是依据公开部分阅读的。

- [AI 不是变笨了——是半年前写的指令在拖后腿（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-claude-md-rules)

同时对照的其他来源:

- [How Many Instructions Can LLMs Follow at Once? (IFScale, arXiv)](https://arxiv.org/abs/2507.11538) — 英文
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — 英文
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 英文
- [Lost in the Middle: How Language Models Use Long Contexts (arXiv)](https://arxiv.org/abs/2307.03172) — 英文
