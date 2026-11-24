---
no: 8
slug: when-skills-reach-ten-thousand
date: 2026-10-03
category: 洞察
tags: 技能 · 安全 · 工具选择
title: 当技能多达一万个——挑选、验证、安装前先检查
summary: 可接入 AI 的技能呈爆发式增长。数量多不是选择，而是供应链风险。这是我们使用的三步标准。
---
> 本文由 AI 协助起草，编辑已审校。参考了外部文章，参考的文章列于文末。

给 AI 助手添加功能的“技能”正在快速增加。所参考的文章介绍说，已登记的技能从数千个发展到百万级的安装量，其中排名靠前的技能是“替你找技能的技能”和“打包了代码质量流程的技能包”。这些数字也是相关文章的统计口径，我们没有核实。但趋势很明确：**挑选成了最大的一件事，而下载的文件会在我的电脑上运行，这一点没有变。**

## 第 1 步——挑选：先定下工作，再找工具

不按“人气排行”挑选。先写下“这件事一天做几次”。一周做不到一次的事，就不挂技能。配置成本大于收益。即使使用帮你查找的技能，最终选择也由人来做。

## 第 2 步——验证：看出处与权限

- **谁做的**：是官方账号，还是知名开发者
- **要求什么**：只是读取文件，还是连命令执行、网络访问都要
- **有多新**：最后更新如果很久以前，可能与现在的模型不匹配

## 第 3 步——安装前先检查

所参考的文章介绍了一种在安装前检查技能文件风险程度的检查工具。我们不为某个特定工具背书，但采纳这一流程。**先阅读 → 用检查工具或肉眼查看有无可疑命令 → 先在没有重要资料的地方试用 → 没问题再用于正式工作。** 下载来的指令文档里“请执行这条命令”之类的句子，也不当作发给我的指示，而是当作**待审查的数据**。

## 小结

技能越多，竞争力就不在于“知道得多”，而在于“用得少而安全”。

## 一同阅读的文章

本文参考了下列文章的问题意识，并以我们团队的视角和标准重新写成。我们没有沿用其语句和结构；原文所引用的数字，凡是我们未能亲自核实原始资料的，均已如此标明。部分原文需登录后才能看到全文，因此我们是依据公开部分阅读的。

- [Claude 技能 9,654 个，别去挑，让它帮你找（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-find-skills)
- [AI 写的代码，帮你检查是否做好的 24 个技能（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-agent-skills-24)
- [不要在不知道下载的技能是否安全的情况下安装，而是安装前检查一次的方法（BIZNIUS LEARN:US）（韩文）](https://learn.bizni.us/learnus-skill-scanner-body)

同时对照的其他来源:

- [Agent Skills overview (Claude Platform Docs)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — 英文
- [Model Context Protocol — Introduction (modelcontextprotocol.io)](https://modelcontextprotocol.io/introduction) — 英文
- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — 英文
- [AI Risk Management Framework (NIST)](https://www.nist.gov/itl/ai-risk-management-framework) — 英文
