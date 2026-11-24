---
no: 14
slug: before-you-copy-a-prompt
date: 2026-10-03
category: 实践
tags: 提示词 · 填空 · 核实出处
title: 拿来提示词之前——核实出处与六行空格
summary: 别人发来的提示词原样粘贴，为什么不行？这里讲如何挑选官方资料，以及适用于任何提示词的六行前置信息。
---
> 本文由 AI 协助起草，编辑已审校。参考了外部文章，参考的文章列于文末。

通过社交媒体评论拿来提示词使用的情况很常见。拿来用本身是个好习惯，但**原样粘贴行不通**的情况很多。这是我们的标准。

## 先看出处

可能的话，先看制作工具的公司发布的官方资料。所参考的文章介绍说，它打开了 Anthropic 公开的官方提示词库，并分成了在聊天窗口里直接可用的、需要粘贴资料的、需要开发工具的三类。这个分类思路很有用。要先分清**这是不是在我的环境里能用的提示词**，才能节省时间。

## 翻译、转述途中消失的前提

把海外的提示词翻译成韩语的过程中，“这个工具已经了解我”这一前提有时会消失。新对话窗口里的 AI 并不认识我。这样一来，AI 要么反问，要么铺陈平庸的泛泛之谈。所参考的文章说明，这个问题是它亲自运行时发现的。我们也可能遇到同样的问题，所以**在写提示词之前，先把 AI 不知道的内容补上。**

## 适用于任何提示词的六行前置信息

如果是处理商业点子的提示词，请先填好下面六行。

1. 收过钱、实际做过的事（不是头衔，而是具体工作）
2. 别人经常来问我的事
3. 每周可用的时间
4. 现在可用的资金
5. 已经联系得上的人
6. 目标金额和期限

## 明确要求“只留一个”

向 AI 大范围提问，它就大范围罗列。罗列是安全的，而选择要担责任。所以在每个步骤的末尾，要求它**“只留一个，并用一句话说明理由”。** 候选从五个缩减为一个，才能进入下一步。

## 最后检查

不要把我的个人信息放进拿来的提示词，结果中的数字和事实要另行核实出处。

## 一同阅读的文章

本文参考了下列文章的问题意识，并以我们团队的视角和标准重新写成。我们没有沿用其语句和结构；原文所引用的数字，凡是我们未能亲自核实原始资料的，均已如此标明。部分原文需登录后才能看到全文，因此我们是依据公开部分阅读的。

- [Claude 开发公司的 52 个官方提示词，全部打开并分好类了（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-prompt-library)
- [说“让我赚钱”，Claude 会反问你（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-money-chain)

同时对照的其他来源:

- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — 英文
- [Prompt injection (Wikipedia)](https://en.wikipedia.org/wiki/Prompt_injection) — 英文
- [Prompt engineering overview (Anthropic Docs)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 英文
