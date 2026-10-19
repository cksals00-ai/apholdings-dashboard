---
no: 24
slug: inspectors-inside-the-building
date: 2026-10-19
category: 洞察
tags: Anthropic · METR · 外部评估 · 独立验证 · 发布权限
title: 审计员走进了大楼 — Anthropic 向 METR 开放「员工级访问」一事，以及如何解读「无否决权」的范围
summary: Anthropic 于 10 月 15 日表示，已向外部评估机构 METR 的 6 名员工开放公司内部设备和工具的访问权限。本文分别梳理了什么是新的、「没有否决权」这句话附带哪些条件，以及哪些内容尚未得到确认。
---
> 本文由 AI（Claude）协助撰写，并经编辑审校。本文的主角 Anthropic 是我们撰写本文时所用 Claude 的开发公司，因此我们与其存在利害关系。Anthropic 自己披露的内容标注为「公司发布的内容」，第三方的解读则另行标注。本文不构成对任何特定企业的投资意见。

Anthropic 于 10 月 15 日在官方博客上发布了一篇关于「独立评估者（independent evaluators）」的更新（显示该文发布后，10 月 16 日对部分脚注作了修改）。核心是：外部评估机构 METR 的 6 名员工使用 Anthropic 内部设备和工具来检查风险的机制已经启动。本文将分别梳理这一发布中哪些内容得到了确认，哪些则见仁见智。

## Anthropic 披露的内容（公司发布的内容）

- **METR：** 非营利评估机构 METR 的 6 名员工像入职一样完成了入职引导，使用公司的设备和办公空间，并可访问与 Anthropic 内部风险评估团队水平相近的内部工具和系统。据称，除客户数据、律师-委托人保密信息和模型结构（架构）信息外，其余内容都鼓励这些员工与他们共享。
- **发布条件：** METR 会发布其对 Anthropic 风险水平、事件和做法的自行分析。Anthropic 表示「无法阻止发布」，同时写明可以要求删除属于上述三类的信息。哪些信息属于这些类别由 Anthropic 决定，METR 则有权就自己获得的访问水平发表意见。
- **隔离运作：** 这一合作在具有约束力的合同下限定于一个小团队，METR 中与 Anthropic 做其他项目的员工与该团队的工作相互隔离。据称 METR 在过去一年中曾多次审阅 Anthropic 的风险报告。
- **三阶段框架：** 第一阶段是范围较窄的检查，访问范围由 Anthropic 决定，评估者的发布需要 Anthropic 批准。第二阶段无需批准即可发布，且能看到更多信息，但可能会收到针对特定类别的删除要求，评估者可以公开就该删除是否正当发表意见。第三阶段是 METR 的方式，即把员工级访问与类似第二阶段的发布权限结合在一起。Anthropic 表示，长期来看希望让多个评估者进入第三阶段。
- **其他机构：** SecureBio 正在审阅 8 月风险报告中的化学和生物武器章节，据称其获得的信息和发布权限比 METR 更受限。Anthropic 正与 Accenture、Faculty 推进涵盖模型评估、红队测试和对齐评估的更广泛合作，对包括 Hugging Face 在内的多家机构则只写了「初步讨论」。Hugging Face 的协商范围和访问水平在该文中没有提及。

## 「无否决权」到底到哪一步（解读）

**1. 否决权和编辑权不同。** 无法阻止发布本身，与 Anthropic 可以让对方删除其划定类别的信息，是两回事。类别虽然只有三个、相对清楚，但其中包含什么，由 Anthropic 判断。不过也有一个机制：METR 可以就访问水平公开发表意见。

**2. 并非所有评估者的条件都相同。** 据 Benzinga 和 CellCog 报道，SecureBio 处于第一阶段，而第一阶段的发布需要 Anthropic 批准。「评估者可以随意发布」这句话只适用于第三阶段（和第二阶段）。

**3. 目前还没有成果。** Crypto Briefing 指出，在发布时，这一访问所产生的 METR 评估结果尚未出现。要等第一份报告出来，看被删除的部分有多少，才能知道这一结构有多实质。

**4. 资金和持续时间未能确认。** CellCog 指出，Anthropic 的文章将不依赖被评估公司的资金（财务独立）列为要求，但没有写明 METR 派驻团队的费用由谁承担。这一合作是否是永久性的、是否适用于今后的模型发布、评估者是否有权推迟发布，在官方文章中都没有找到（Tech-Insider 也指出了同一点）。

## 背景：同一周的动向

Benzinga 报道称，同一周美国 FTC 向 OpenAI 和 Anthropic 发出了民事调查要求函，并概述称 Anthropic 上个月承诺加强外部评估，并签署了「关于超级智能的白宫协议」。Tech-Insider 将这一结构与上述压力联系起来解读，但这种联系以及「其他公司会效仿」的预测是该媒体的推测，并非报道的事实。这与上一篇文章（NO.23）中谈到的 FTC 事件属于同一趋势，但 Anthropic 并未说过这次发布是因此而起。

## 这条消息中未能确认的内容

- 没有找到 METR 自己的说明。METR 博客列表只到 10 月 6 日的文章（「AI systems could cover up misbehavior」），没有看到说明这次合作的文章。因此，METR 的立场我们只能通过 Anthropic 的文章得知。
- 上述数字和条件全部来自 Anthropic 自己的发布，并未经过独立验证。各媒体报道大多是对这一发布的重复。Crypto Briefing 对评估阶段的划分与官方文章不同（把 Faculty 标为第二阶段），但官方文章中没有任何这样的划分，所以我们以官方文章为准。
- 此前检查中作为候选的斯坦福 HAI 的研究，这次检查中同样没有找到与本事件直接相关的最新研究。搜索中出现的 HAI 文章是 2021 年关于第三方审计的提议，因此没有放入本文。

## 我们的想法

**事实：** Anthropic 向 METR 的 6 名员工开放了员工级访问，并表示不阻止其发布，但可以要求删除既定类别的内容。各评估者的条件各不相同。

**解读：** 「外部在看」这句话之后，总会跟着几个问题：谁来划定访问范围，谁来批准发布，谁来出钱。这次发布回答了其中一部分，另一部分要等到第一份报告出来才有答案。

**如果是我们：** 我们使用的 AI 工具所说的「安全」「经过验证」，也用同样的问题来读。记下是谁测的、是不是公司挑选的案例、条件是什么，并且对我们自己的工作，按我们自己的标准再跑一遍。本简报同样会在文章开头说明存在利害关系的部分，对于没有亲自打开确认的内容，则写明未能确认。

## 一并阅读的文章

我们直接打开了性质不同的来源进行确认。数字和条件均以各来源为准。

公司官方资料：

- [An update on independent evaluators (Anthropic)](https://www.anthropic.com/news/an-update-on-independent-evaluators) — 英文，公司官方发布

报道·分析：

- [Anthropic Gives AI Watchdog Unprecedented Internal Access (Benzinga)](https://www.benzinga.com/markets/private-markets/26/10/62397762/anthropic-lets-outside-ai-evaluators-inside-its-systems-and-publish-findings-it-cant-block) — 英文，媒体（标注部分使用了 AI 工具）
- [Anthropic gives outside AI safety evaluators METR and SecureBio inside access (Crypto Briefing)](https://cryptobriefing.com/anthropic-metr-securebio-ai-safety-evaluation/) — 英文，媒体（阶段划分与官方文章不同）
- [Anthropic Gives METR Employee-Like Access: What It Means (CellCog)](https://cellcog.ai/blog/anthropic-metr-embedded-evaluators/) — 英文，企业博客（含自家 AI 服务的宣传）
- [Anthropic Gives METR 6 Staff AI System Access (Tech-Insider)](https://tech-insider.org/au/anthropic-metr-outside-evaluators-access-2026/) — 英文，媒体（展望为作者推测）
