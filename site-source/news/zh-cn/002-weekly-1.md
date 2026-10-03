---
no: 2
slug: weekly-2026-10-03
date: 2026-10-03
category: 每周资讯
tags: Gemini 4 · 网络安全 AI · 模型价格
title: 每周 AI 资讯 #1——谷歌推出 Gemini 4，最强模型为何不给所有人用
summary: 9 月 30 日谷歌发布了 Gemini 4 Argon，9 月初三家公司的安全专用模型也都只向“经过验证的防御者”开放。模型越快，开放方式就越不一样。
---
> 本文由 AI 协助起草，编辑已核对出处。所有数字均以下方出处为准，不构成投资建议。

## 本周一句话

最强的模型如今不再是“人人可用的应用”，而是“先向获得许可的机构开放”。而在这之下，模型发布速度和价格竞争仍在不断加快。

## 1. 谷歌发布 Gemini 4 Argon（9 月 30 日）

**事实。** 据 Axios 报道，谷歌于 9 月 30 日发布了 Gemini 4 Argon。这是一款面向软件工程、金融、法律、网络安全等漫长而复杂工作的模型，谷歌称其在编程和知识工作基准测试中领先于 OpenAI 的 GPT-6 Astra。它起初只限量开放给部分网络安全合作伙伴，经过进一步测试后计划扩大到付费订阅用户。同一篇报道引述彭博社称，部分员工在内部测试中指出其性能不足，谷歌对此予以否认。

**解读。** 基准测试上的优势，是发布方自己挑选的标准下的说法。在独立评测出现之前，把它当作“主张”来读更稳妥。

**如果是我们。** 不换模型。我们会用自己在用的任务（文章、图片描述、数据整理）输入相同内容做一次对比，只有出现明显差异时才更换。

## 2. 三家公司的安全专用模型，都“优先面向经过验证的防御者”

**事实。** 据 The Hacker News 报道，9 月初谷歌（Gemini 3.8 Flash Cyber）、Anthropic（Claude Mythos 5.1 与 Fable 5.1）、OpenAI（Astra）各自推出了网络安全用途的接入计划。谷歌表示，将与 650 多家合作伙伴一起提供给政府、医疗、电信等可信赖的防御者；Anthropic 表示，把限制最少的模型只开放给可信接入计划，同时引入了针对恶意请求和提示词注入的防御，以及对沙箱逃逸尝试的检测。OpenAI 向测试者群体提供，并增加了防滥用分类器，给出的越狱请求拒绝率为 91.5%。

**解读。** 发现漏洞的能力既可用于防御，也可用于攻击。三家公司做出了同样的选择，即“先给防御方，之后再扩大”，这可以解读为：能力越强，开放方式本身就成了产品设计。

**如果是我们。** 直接影响不大，但有两件事可以马上落实。在 AI 阅读外部文档或网页的工作中，设定规则，让它不执行其中的指令性文字；在 AI 所做的事情里，对无法挽回的操作（删除、发送、支付），要经过人工确认。

## 3. 模型泛滥，价格触底竞争

**事实。** 一家独立汇总博客整理称，9 月 12 日至 25 日的两周内有 20 多个模型发布，最贵与最便宜模型的 token 价格相差约 119 倍。CNBC 在 9 月 6 日以“模型疲劳”一词报道了业界对快速发布节奏感到厌倦的氛围。

**解读。** 汇总数字是个人博客整理的，需要与各厂商的官方价目表核对。不过方向很明确：同样的事情用便宜得多的模型来做也可以的区间正在变宽。

**如果是我们。** 不用“最好的模型”这一个去做所有事，而是把任务分成困难的和重复性的，重复性工作交给便宜的模型。这一标准会在下一篇洞察文章中详细讨论。

## 下周关注

- Gemini 4 的独立评测和全面开放的时间
- 安全专用模型接入计划是否扩大
- 主要 API 价格调整

## 出处

- [Google unveils Gemini 4, long-awaited answer to OpenAI and Anthropic — Axios (2026.09.30)](https://www.axios.com/2026/09/30/google-gemini-4)
- [Google, Anthropic, and OpenAI Unveil Cyber AI Models, Safeguards, and Access Programs — The Hacker News (2026.09)](https://thehackernews.com/2026/09/google-anthropic-and-openai-unveil.html)
- [‘Model fatigue’ sets in as AI labs race to roll out new versions at frenetic pace — CNBC (2026.09.06)](https://www.cnbc.com/2026/09/06/meta-google-openai-anthropic-ai-model-fatigue.html)
- [September 2026 AI Model Updates — local-ai-zone（汇总博客，数字仅供参考）](https://local-ai-zone.github.io/blog/September_2026_AI_Model_Updates.html)
