---
no: 48
slug: model-swap-takes-weeks-keep-knowledge-outside
date: 2026-11-15
category: 洞察
tags: 模型更换 · VB Pulse · Ramp AI 指数 · PayPal · 知识层 · 提示词习惯 · Claude Opus 5.5 · MathArena · eBay 用户协议
title: 更换模型要花几周 — 换过的公司十家有七家回答“几周以上”，Ramp 统计“9 月有 8% 的企业更换了供应商”，而 PayPal 没动模型就把正确率从 43% 提到了 95%
summary: 在 VentureBeat Intelligence 于 11 月 12 日发布的 10 月调查中，回答“过去一年内更换过运行中应用的 AI 模型”的公司占 47%，而在换过的人当中，69% 表示除了改模型名之外还花了“几周以上”的工程工作（有更换经验者为 45 人，样本很小）。更换后性能下降、不得不修改应用或退回原模型的比例为 44%。Ramp 在 10 月 6 日写道“更换 AI 模型供应商的企业比例在 9 月达到 8%，为历史最高”；PayPal 则在活动上表示，模型保持不变，而是把业务定义、查询规则、分析流程放在模型之外，使内部助手的正确率从 43% 提高到 95%（仅 VentureBeat 一处来源）。同一周，Anthropic 发文称“深入思考”之类的旧提示词习惯会让 Opus 5.5 变慢 — 这是撰写本文的 AI 的制造商自己写的文章，因此我们不加评价。我们把这三件事归入“绑在模型上的东西与放在模型之外的东西”，并在文末用两条“简讯”记下 MathArena 的新排名（第 1 名与第 3 名分差 4.8 分、成本差 15 倍）以及 eBay 用户协议中“禁止无人工审核的自动下单”的条文。
---
> 本文由 AI（Claude）协助撰写，并经编辑审核。我们公司是 Anthropic 和 OpenAI 两家公司的付费客户，也在测试中使用谷歌的模型。**第 3 节是撰写本文的 AI 的制造商（Anthropic）关于自家模型所写的文章**；第 2 节 Ramp 的文章中有一句提到 Anthropic 份额上升；“简讯”的排名表里 Anthropic 的模型排在第 2 位；PayPal 案例页面中的助手以 Claude 作为前端。因此我们**对任何一方都不加评价，只搬运数字和原文。**公司发布的数值标注为“公司发布的数据”，只有单一来源的内容则一并注明该来源。本文不构成对任何特定企业的投资意见。

我们在 NO.04 中写过“当模型每周都在变时，小团队工作的五条准则”，在 NO.46 中写过“日常使用的模型”一栏两天就换了的速度。本周出来的数字在它的另一面 — **不是模型变化的速度，而是我们更换模型所要付出的代价**。我们把一份调查、一份支付数据、一个公司案例，以及模型制造商写的一篇“请放弃这个习惯”的文章，按“绑在模型上的东西 / 放在模型之外的东西”来分开阅读。按事实、解读、如果是我们三部分来写。

## 1. VB Pulse — 更换过运行中模型的公司占 47%，换过的人中 69% 说“几周以上”（事实）

VentureBeat 的调查部门 VentureBeat Intelligence 于 11 月 12 日以报道和报告页面的形式发布了 10 月调查（“VB Pulse — 智能体编排”）。样本很小。**106 名受访者中有 100 人通过资格筛选**（在员工 100 人以上的组织从事 AI 工作的人占 72%，服务此类组织的顾问占 28%；88% 来自调查面板渠道），组织规模方面，超过 1 万人的占 31%、100~250 人的占 23%，同一组织多人作答的有 18 家，报告自己也写道“由于是自选样本，难以推广到所有企业”。

数字如下。**过去 12 个月内更换了运行中 AI 系统的模型、但应用保持不变的公司占 47%。**在换过的 **45 名**受访者中，除改模型名之外所花的工程工作是 — “几乎没有，仅配置变更”13%、“几天”9%、**“几周”33%、“一个月以上”36%**、“不知道”9%。几周以上合计为 **69%**（报道正文四舍五入为 70%，报告为 69% — 本文采用报告的数字）。结果是**“新模型相同或更好”56%、“性能下降，修改了应用”33%、“退回原模型”11%** — 修改或退回的比例为 44%（报道为 45%）。与 9 月调查相比，“一个月以上”从 12% 增至 36%，但报道称受访者构成不同，**只能看方向**，并写道 44% 与 9 月（58%）的差异在统计上不显著。

调查没有问“为什么换”“改了什么”。报道举了四个例子。①提示词、工具、测试都针对某一个模型调好了，必须重新修改（包括决定可以调用哪些工具的“harness”）。②评估集必须用真实请求来构建，而收集这些数据是最难的事（Box 的 Ben Kus）。③微调不会延续到下一个模型 — PayPal 的 Ren Zhang 说“新模型出来后，必须用那个模型重新微调”。④同一个模型，harness 不同结果差异也很大 — 报道举的一个基准测试中，Kimi K3 的“每个通过任务的中位成本”在一个编码 harness 下为 18.34 美元，在另一个下为 3.28 美元，而通过率同为 63.3%（报道单一来源的例子）。文中写道，摩根大通在每个新 Claude 模型发布时，都要先通过内部审批才让员工使用；Upwork 的 Sudhanshu Bist 说，如果是运营中的系统，“大概会继续用现有模型”。在让更换更容易的方面，文中列出：网关·路由器（一行即可切换，但应用需单独检查）、把业务知识放在模型之外（第 2 节的 PayPal）、在实际要运行的 harness 中测试、以**“每个良好结果的成本”**来衡量，以及像 T-Mobile 那样把旧版和新版在真实通话中并行运行、只扩大更好的一方。

## 2. Ramp“9 月有 8% 更换了供应商”，PayPal“模型不变，43%→95%”，Uber“每次清理的成本↓90%”（事实）

**Ramp**（美国企业卡·支出管理公司）的数据团队于 10 月 6 日发布了一篇题为“企业更换 AI 模型供应商的频率在上升”的文章（作者 Ryan Stevens，应用科学总监）。**更换 AI 模型供应商的企业比例在 9 月达到 8%，为有记录以来最高**，该数值是 3 个月平均的月比例。文章写的脉络有两条 — 2025 年 5 月 Anthropic 发布 Opus 4·Sonnet 4 后份额大幅上升，此后一年更换减少；2026 年 6 月 OpenAI 的降价和新模型发布打破了这一平衡。文中写道，6 月以来两家公司的模型发布公告在 9 件以上。作者以可能性的口吻写道“这可能是模型正在成为商品（commodity）的早期信号”。这篇文章没有写样本规模、“更换”的判定标准、样本构成（Ramp 11 月版 AI 指数自己写道“客户偏向科技·金融领域” — NO.47）。Anthropic 份额上升这句话是照搬 Ramp 所写，我们不加评价。

**PayPal** 的数字仅来自 VentureBeat 11 月 10 日的一篇报道 — 这是对 10 月 8 日和 10 月 28 日 VentureBeat 活动上 PayPal 两位高管发言的整理，不是 PayPal 的官方文章。Ren Zhang（AI 产品负责人、副总裁）说，**内部数据科学助手**（回答原本要交给数据科学团队的业务问题的助手）的内部正确率从 **43% 提高到 95%**，而“LLM 保持不变”。改变的是模型之外的**知识层** — 规定为什么目的、如何提取哪些数据的“黄金查询”，写明如何深挖登录失败或密钥使用等问题的“分析手册”，以及**不让模型从数据中推断、而是作为知识直接给出的业务定义**，比如“什么是新账户”。43% 和 95% 是如何测量的、是哪个时期，报道中没有（10 周内 1,000 多个问题、估计节省 1,600 小时是另外的句子，报道也补充说“问题数量不能证明生产力”）。同一报道中，PayPal 为面向客户的商务智能体测试了 4~5 个模型 — 大模型延迟约 15 秒，80 亿参数模型快但正确率低，用微调提高了但仍不够 — 并表示**因为每次模型更换都要重新训练的成本，减少了对微调的依赖**（并非完全放弃）。作为参考，Google Cloud 的 PayPal 客户案例页面（无日期）描述了同一类助手 — 把 Looker 的 MCP 服务器放在内部 MCP 中心、在 Claude Desktop 中用自然语言提问的结构，用户约 5,000 人，指标定义由 Looker 的语义层固定。该页面的“相对于已定义指标接近 100% 准确”是供应商一方的说法，没有标准和方法，43%→95% 这个数字也不在那里。两篇文章是否指同一个助手，我们也未能确认。

**Uber** 出现在 VentureBeat 11 月 10 日的另一篇报道中（VB Pulse 基础设施调查 — 156 名受访者，“因成本超支而推迟、缩减或取消 AI 项目”38% 对“计算资源不足”12%）。Uber 的 Uday Kiran Medisetty（副总裁·杰出工程师）说，对托管智能体**以真实任务做基准测试来选模型之后**，“每次清理（cleanup）的成本”降低了 90%，质量以回滚（revert）·事故数衡量，成本以“每完成一次审查·清理”衡量。报道写道，这个 90% 是仅限于 Uber 任务的数字。

## 3. Anthropic — “请放弃七个旧提示词习惯”，其中一个源自 2022 年的论文（事实，存在利害关系）

Anthropic 于 11 月 12 日在 claude.com 发布了一篇题为“把 Claude Opus 5.5 用作知识工作的日常模型”的文章（作者 Aleksandra Todorova；The Decoder 于 11 月 14 日做了整理）。**这是撰写本文的 AI 的制造商关于自家模型所写的文章**，因此这里只搬运清单和公司所写的数值。Opus 5.5 是 Pro·Max·Ultra·Team 套餐的默认模型，文章要求“改掉”的习惯有七个 — ①加上“深入思考（think hard）”之类的语句（称该模型总是在思考，所以没有必要）②从 High 开始设置努力等级（应从默认的 Medium 开始，不够时再提高）③一次只下一步指令（应把目标、产出格式、何时反问一次说清）④在成品之前先要草稿·大纲 ⑤手动抄写图表数字（应以图像·文件粘贴）⑥像“避免通用的设计”那样含糊地禁止（应具体说明要避免的要素）⑦只把复杂工作交给 Opus、其余交给 Sonnet 的分工（称如果把 Sonnet 用在高努力等级，每任务成本会接近 Opus 5.5）。

公司所写的数值如下，且全部为**公司的内部测试**。Opus 5.5 的 Medium 在自家编码·知识工作评估中与 Opus 5 的 High 相同或更好；去掉“思考”语句后回答开始得更快，质量下降不明显；最低努力等级读密集图表比 Opus 5 的最高等级更准确；用保存的网页快照做的 18 份报告中有 16 份通过了“编造数值·引用”的自动检查；在并购模型任务中用 63 分钟（Opus 5 为 93 分钟）、一半成本完成。外部公司 Factory 称“在 Medium 下得到与 Opus 5 High 相同的结果，输出 token 少 20~25%”，这也是公司文章引用的话。文中所列价目表为 Haiku 5.5 0.10/0.50、Sonnet 5.5 2/10、Opus 5.5 4/20、Fable 5.2 8/40（每百万 token 输入/输出）。

①号习惯的出处我们另行做了确认。根据维基百科“提示工程”条目，让模型使用中间推理步骤的“思维链”，是 2022 年 Google Brain 作为附带示例的 few-shot 技巧报告的，而**只加一句“Let's think step by step”也有效**，则来自同年谷歌·东京大学研究团队（Kojima 等，NeurIPS 2022）的论文。同一条目还写道，汇集了 100 多篇论文的元分析显示，收益集中在数学·逻辑·符号推理上，在其他任务上较小、在部分任务上准确率反而下降；以及随着指令遵循·推理能力的提高，“精细提示词构造的边际价值正在减少”。也就是说，2022 年论文造成的习惯，到 2026 年制造商说“去掉”，而**去掉之后会更好的数值，到目前为止只有该制造商的测试。**

## 简讯两条（事实）

**MathArena。**由 ETH 苏黎世 SRI 实验室和 INSAIT 运营的数学竞赛评测网站于 11 月 13 日添加了 Gemini 4 Carbon 和 Claude Fable 5.2 的结果（我们于 11 月 15 日直接打开，The Decoder 同日也记录了同一张表）。综合“预期表现”（未弃用的各竞赛归一化分数的平均值）为 **Gemini 4 Carbon(high) 85.4%±3.0、Claude Fable 5.2(max) 82.8%±5.3、GPT-6.1 Sol(max) 80.6%±2.7**，最高的开源模型是 Kimi K3.1 Pro(max) 54.3%±5.8。成本以**“解一道题一次的平均成本”**计，分别为 15.70 美元·40.20 美元·**1.07 美元**·3.70 美元。第 1 名与第 3 名的差为 4.8 分，成本约 15 倍，第 1 名与第 2 名的区间（±3.0 与 ±5.3）重叠。The Decoder 写道，Carbon 最常见的失败是“超时”，在一个案例中脚本运行超过 11 小时却没有检查进度（The Decoder 的一手资料是评测者的 X 帖子，我们以网站的表格做了确认）。由于第 2 名是 Anthropic 的模型，我们对排名不加评价。

**eBay。**我们直接打开了 eBay 的用户协议（当前版本对现有用户自 2026 年 6 月 28 日生效）。第 3 条禁止在**“未经事先明示许可”**的情况下使用机器人、爬虫、抓取器等自动化手段，并在括号内以**“buy-for-me 智能体、LLM 驱动的机器人，或任何试图在无人工审核的情况下下单的端到端自动化流程”**为例。据 PPC Land（11 月 14 日），这段文字并非新增，而是从 1 月 20 日的修订（2 月 20 日生效）起就有；11 月初 Meta Muse 对 eBay 的访问变得不稳定，是 The Verge 11 月 10 日报道（我们这边无法打开）的转述。PPC Land 转述的 eBay 发言人的话是“包括未经授权的抓取、用我们的数据训练等情况，我们在部分情况下限制了智能体访问”，而**获得许可的智能体名单和申请方法并未公开。**这是与 United（NO.45·47）放在同一行的句子。

## 把三件事放在一起读（解读）

第一，**更换模型的代价不是模型的价格，而是它周边的代价。**在网关里模型名一行就能改，而调查中换过的人十个有七个回答“几周以上”，原因正如报道所举的例子 — 提示词、工具、测试、微调都**针对那个模型**调好了。所以“频繁更换模型的公司增至 8%”（Ramp）和“换一次要花几周”（VB）并不矛盾，而是**从两边看到的同一笔成本**（解读）。不过这两个数字的样本都很小或构成不明，所以我们用它们来读“什么被绑住了”，而不是“有多少”。

第二，**能延续到下一个模型的，只有放在模型之外的东西。**PayPal 提高的不是模型，而是“新账户的定义”“这个问题这样深挖”，那是即使模型更换也能照用的资产。相反，微调是随模型一起消失的成本，所以 PayPal 减少了依赖。我们在 NO.05 中写过“给 AI 的指令不是资产而是负债”，这次的数字让我们把这句话再切一刀 — **刻着模型名的指令是负债，业务定义、正确答案示例、测试集是资产**（解读）。Uber 的 90% 也不是出自“模型选得好”，而是出自**拥有由真实任务构成的基准测试**（仅限 Uber 的限定语照报道原文）。

第三，**习惯也会绑在模型上。**“一步一步思考”是 2022 年论文造出来的句子，4 年后制造商写道这句话会让自家模型变慢。这是否属实，需要我们自己来测 — 制造商文章中的数值全是制造商的测试，而那家公司就是撰写本文的 AI 的公司。但是**“刻在提示词里的习惯当中，哪些是因为某个模型而产生的”**这个问题本身，与模型无关地成立（解读）。MathArena 的表是这个问题的成本一侧 — 分数差 4.8 分、成本差 15 倍，第 1 名与第 2 名区间重叠。NO.40 的“1 分之差在区间之内”、NO.46 的“不是 token 的价格而是任务的价格”，在数学题上也以同样的形状出现。

## 如果是我们 — 运营应用·电商·AI 渠道的团队本周要做的三件事（实践）

1. **做一次“模型更换演练”，记下所花的时间。**把 NO.17·46 的三项测试（成分表判定·应用文案·Ria 脚本）从现在的默认模型**实际切换**到另一个模型运行，把所花时间分成“改模型名 / 修提示词 / 修工具调用 / 重新对齐测试”四栏记录。不必做到底 — 哪一栏花得最久，就是我们“被绑住的东西”的清单。结果旁边按 VB 报道的算法记下**“每个良好结果的成本”**。
2. **建一个放在模型之外的盒子。**把 SafeList 的判定标准（只说到“没有看到要避免的项目” — NO.03）、我们电商的术语定义（“新客户”“取消”“退货”是什么）、成分表判定的 20 个正确答案示例，分离为**独立文件而不是提示词**，并把提示词改成只指向该文件。在 NO.05 的“每季度删除指令”检查中加一行 — **标记“以模型名或特定模型的脾性为前提的句子”**，更换时先删除这些句子。
3. **用我们自己的数字测试去掉“思考”语句的版本。**制造商的建议只是建议，所以把三项测试的提示词中去掉“深入思考”类句子的版本和保留的版本，在**同一努力等级**下各运行 20 次，记录正确率、首个 token 时间、输出 token 数。无论结果如何，都在我们的表里以“公司发布 / 我们确认”两行留下。电商方面只有一行 — 对照 eBay·United 的条文，确认**我们的用户协议里是否有“无人工审核的端到端自动下单”条款，如果有，是否写明了许可申请路径**，并附到 NO.45 的“为什么”一栏草稿中。

## 这次没有选的内容

The Decoder 11 月 13~14 日关于 Anthropic 上市路演、CEO 发言、前研究员主张的三篇文章属于投资判断材料且存在利害关系，因此没有使用。英伟达高管更换的分析（The Decoder·VentureBeat）在我们的主题之外。Runway 公开 Praxis-1 权重（Apache 2.0，机器人控制）和 OpenAI 机器人团队的重新安排只有 The Decoder 一处来源，只留标题。Anthropic 的 Claude in Google Meet（VentureBeat 11 月 12 日）和自托管 Claude Managed Agents（Help Net Security 11 月 12 日）因存在利害关系，只记标题。Help Net Security 的“固定的 MCP 服务器可能并不固定”（11 月 13 日）和“被盗 Claude API 密钥”报道属于安全事件，只留标题 — 待官方公告发布后，作为 NO.32 的后续、不涉及手法地处理。PPC Land 所写的“欧盟提议对付费 AI 推荐处以全球营收 6% 的罚款”，由于未能打开官方文件而暂缓。Skift 11 月 11 日的两篇文章（酒店集团 MCR CEO“禁止 AI 机器人预订”、花旗“预订出错应由 AI 公司承担”）和 11 月 9 日的“检查 50 家旅游网站的 AI 爬虫指令”没有打开正文，作为 NO.37·45 的后续候选。VB Pulse 的另一份 10 月报告标题 — “智能体自信的错误回答中 78% 来自业务定义的缺失·冲突” — 与第 2 节方向一致，但没有打开正文，只记标题。Meta 新闻室在 11 月 15 日仍没有关于 Muse 电话功能的文章（NO.47）。

## 这则消息中我们未能确认的内容

- VB Pulse 有更换经验者的样本为 45 人。“几周以上 69%”“一个月以上 36%”是这 45 人之内的比例，与 9 月的差异报告写的是“只看方向”“不显著”。报道的 70%·45%·55% 与报告的 69%·44%·56% 四舍五入方式不同。
- 因 harness 不同、每任务成本分为 18.34 美元和 3.28 美元的 Kimi K3 例子，是 VentureBeat 报道所举的一个基准测试，我们没有打开该基准测试。
- Ramp 的“9 月 8%”在文中没有样本规模、判定标准、样本构成。Ramp 的数据是企业卡支付记录，这是另一篇 Ramp 文章（NO.43·47）的说明，本文中没有写。
- PayPal 的 43%→95% 仅来自一篇转述 VentureBeat 活动发言的报道（除转载网站外没有其他媒体确认），没有测量方式、时期、测试集。Google Cloud 案例页面的“接近 100%”是供应商一方的说法，两篇文章是否为同一助手未能确认。
- Anthropic 文章的数值全部为公司内部测试，没有独立确认。Factory 的 20~25% 是公司文章引用的外部公司的话。
- MathArena 的表我们直接看了，但各模型以哪个努力等级、哪种设置运行的细节以及“超时 11 小时”案例只有 The Decoder（评测者 X 帖子的转述）一处。
- eBay 用户协议只读了前 10 万字（后 2.7 万字未读），Muse 访问不稳定是 PPC Land 对 The Verge 报道的转述。获得许可的智能体名单哪里都没有。

## 一起读过的文章

我们直接打开并确认了性质不同的来源。按公司发布·官方文件、调查·评测机构·数据、媒体报道、维基、我们以前的文章分开记录。

公司发布·官方文件：

- [Using Claude Opus 5.5 as your daily driver for knowledge work (Anthropic, 11月 12日)](https://claude.com/resources/articles/using-claude-opus-5-5-as-your-daily-driver-for-knowledge-work) — 英文，7 个旧习惯·公司内部测试数值·价目表（存在利害关系）
- [PayPal — conversational analytics with Looker MCP Server (Google Cloud 客户案例，无日期)](https://cloud.google.com/customers/paypal-looker-mcp) — 英文，内部 MCP 中心·Claude Desktop·约 5,000 人·语义层（“接近 100%”为供应商说法）
- [eBay User Agreement (2026年 6月 28日生效版)](https://www.ebay.com/help/policies/member-behaviour-policies/user-agreement?id=4259) — 英文，第 3 条“buy-for-me agents, LLM-driven bots, or any end-to-end flow that attempts to place orders without human review”条文

调查·评测机构·数据：

- [VB Pulse — Agentic Orchestration, October 2026 (VentureBeat Intelligence)](https://venturebeat.com/vb-pulse-agentic-orchestration-report) — 英文，100 名受访者·更换 47%·45 人中几周 33%·一个月以上 36%·相同或更好 56%·重做 33%·退回 11%·样本限定
- [Businesses are changing AI model providers more often (Ramp Economics Lab, 10月 6日)](https://ramp.com/data/businesses-are-changing-ai-model-providers-more-often) — 英文，9 月 8%（3 个月平均）·2025 年 5 月与 2026 年 6 月的两次转折·“可能是商品化信号”
- [MathArena 排行榜 (ETH Zurich SRI Lab · INSAIT, 11月 13日更新)](https://matharena.ai/) — 英文，预期表现·每题成本定义·Carbon 85.4/15.70·Fable 5.2 82.8/40.20·Sol 80.6/1.07·Kimi K3.1 Pro 54.3/3.70

媒体报道：

- [Swapping AI models is easier said than done: for most companies, it takes weeks, VB Intelligence finds (VentureBeat, 11月 12日)](https://venturebeat.com/infrastructure/swapping-ai-models-is-easier-said-than-done-for-most-companies-it-takes-weeks-vb-intelligence-finds) — 英文，调查整理·提示词/工具/测试/微调·harness 例子（单一来源）·摩根大通·Upwork·Box·T-Mobile
- [PayPal says its AI assistant went from 43% to 95% accuracy without changing the model (VentureBeat, 11月 10日)](https://venturebeat.com/orchestration/paypal-says-its-ai-assistant-went-from-43-to-95-accuracy-without-changing-the-model) — 英文，活动发言整理（单一来源）·黄金查询·手册·业务定义·减少微调依赖
- [AI's biggest bottleneck is cost: companies blame stalled projects on overruns three times as often as on compute shortages (VentureBeat, 11月 10日)](https://venturebeat.com/infrastructure/ais-biggest-bottleneck-is-cost-companies-blame-stalled-projects-on-overruns-three-times-as-often-as-on-compute-shortages) — 英文，VB Pulse 基础设施调查（156 人）·Uber 每次清理成本↓90%（仅限 Uber）
- [Anthropic says outdated prompting habits are slowing down Claude Opus 5.5 (The Decoder, 11月 14日)](https://the-decoder.com/anthropic-says-outdated-prompting-habits-are-slowing-down-claude-opus-5-5/) — 英文，Anthropic 文章整理
- [Gemini 4 Carbon takes the MathArena crown but costs 15 times more than GPT-6.1 Sol (The Decoder, 11月 14日)](https://the-decoder.com/gemini-4-carbon-takes-the-matharena-crown-but-costs-15-times-more-than-gpt-6-1-sol/) — 英文，排行榜整理·“超时”失败案例（评测者 X 帖子转述）
- [Microsoft's Exchange outage stalls offices as eBay shuts out robot shoppers (PPC Land, 11月 14日)](https://ppc.land/microsofts-exchange-outage-stalls-offices-as-ebay-shuts-out-robot-shoppers/) — 英文，eBay 用户协议时间线（1 月 20 日修订·2 月 20 日生效）·Muse 访问不稳定（The Verge 转述）·发言人发言

维基：

- [Prompt engineering (Wikipedia)](https://en.wikipedia.org/wiki/Prompt_engineering) — 英文，思维链（2022，Google Brain）·“Let's think step by step”（Kojima 等，NeurIPS 2022）·元分析·“精细提示词的边际价值减少”

我们以前的文章：

- [每周 AI 消息 — 谷歌在五天内换了三个模型和搜索 (AP News NO.47)](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [“日常使用的模型”一栏出现了 — Hydrogen 与每任务价格 (AP News NO.46)](https://www.apholdings.kr/ko/news/hydrogen-daily-driver-price-per-task/)
- [拦住顾客的智能体，放进店家，模型则给所有人 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [顾客不能带自己的智能体来 (AP News NO.43)](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [计分表上有了概率 (AP News NO.40)](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [按任务用哪个 AI — 我们使用的测试法 (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/)
- [给 AI 的指令不是资产而是负债 (AP News NO.05)](https://www.apholdings.kr/ko/news/instructions-are-debt/)
- [当模型每周都在变时，小团队工作的五条准则 (AP News NO.04)](https://www.apholdings.kr/ko/news/when-models-change-weekly/)
- [当 AI 代替你读成分表时 (AP News NO.03)](https://www.apholdings.kr/ko/news/ai-reads-the-label/)
