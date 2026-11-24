---
no: 40
slug: scoreboard-probabilities-and-four-rides
date: 2026-11-06
category: 洞察
tags: 记分板 · Epoch ECI · METR · Anthropic研究速度 · Uber智能体订单 · 实际使用 · Kimi K3.1 Pro
title: 记分板上有了概率 — Epoch写下「Astra领先Opus 5.5的概率为72%」，METR从外部测得Anthropic的研究速度一年翻倍，Uber数出最忙的一周智能体只叫了4单车
summary: 本周，衡量AI的三把尺子各自变了一次。11月4日，Epoch AI把模型能力指数（ECI）从「一个分数」改为「区间与比较概率」，结果写下GPT-6 Astra领先Claude Opus 5.5的概率为72%，两者差距的90%区间为−0.9至+2.1分。11月5日，METR在Anthropic内部用11周看过内部数据后写道：「在定义明确的任务上，能力提升速度自2025年10月以来约为此前的两倍（按基准测试为1.9倍，95%区间1.5–2.8倍）」，「其中约80%归功于AI（主观估计）」。11月4日，Uber在第三季度财报电话会上说明：10月最忙的一周，在总计约3.2亿笔交易中，AI智能体叫的车是4单，外卖订单约500单，BigGo称这是首次单独披露。我们整理了分数、速度、实际使用这三个数字的算法有何不同，以及小团队该如何记录自己的数字。
---
> 本文与AI（Claude）共同撰写，并经编辑审校。我公司是Claude开发商Anthropic和OpenAI的付费客户，并自行运营应用、电商和AI渠道。今天第1条中，Anthropic的模型在比较中落后于OpenAI的模型；第2条是Anthropic委托的外部评估（METR写明其分析大量使用了Claude）。我们尽量不偏向任何一方解读，仅有单一来源的内容均注明来源。第2条提到Anthropic的上市日程，第3条提到Uber的财报，但本文不是对任何公司的投资意见，也不是投资决策的依据。

NO.33中我们写过，新记分板（Artificial Analysis v5）的第一名和第二名只差1分；NO.34中建议把公司自己给出的分数和独立机构给出的分数分成两行来写。NO.24写了Anthropic向METR开放「员工级访问权限」的公告，NO.35引用了DoorDash所说「外卖应用上智能体下的订单只有几百单」。本周，这四篇的后续同时到来。做记分板的一方、从外部测量公司的一方、数实际订单的一方各自给出了数字，但算法各不相同。我们分成事实、解读、如果是我们来写。

## 1. Epoch — 从一个分数到「区间与概率」（事实）

Epoch AI于11月4日宣布，模型能力指数ECI（Epoch Capabilities Index）的计算方法改为**贝叶斯模型**（Emilia Álvarez、Alexander Barry）。ECI用项目反应理论把多个基准测试分数汇成每个模型一个能力分数，锚点不变（Claude 3.5 Sonnet = 130，GPT-5 = 150）。变化的是拟合方式和不确定性的衡量方式。此前用自助法估计误差，但**很多模型只有4到10个基准分数**，重新抽取几个结果就会大幅波动，也无法直接比较两个模型。新方法不再给出单一值，而是从分布中抽样（MCMC），给出**均值和90%可信区间**，为每个基准单独设置噪声水平，并用贝塔分布使预测分数不超出0–100%。

按Epoch的原文转述结果如下。ECI在125以上的176个模型几乎不变（平均−0.1分，最大变化−4.1分，区间平均收窄13%）。125以下的76个模型**全部下降**，平均降13.7分，最多降39.2分，主要是因为去掉了此前把弱模型拉向平均值的正则化（GPT-4从126降到122）。顶端，GPT-6 Astra的90%区间为166.2–172.7，Claude Opus 5.5为165.8–172.0。而且Epoch首次写下了**两个模型直接比较的概率**：GPT-6 Astra能力高于Opus 5.5的概率为**72%**，高于Claude Fable 5.1的概率超过99%。两者差距的90%区间为**−0.9至+2.1分**，比各自的区间更窄，Epoch解释说是因为不确定性的很大一部分由两个模型共享。拟合度方面，样本内旧方法略好（RMSE 0.076对0.079），样本外预测新方法略好（0.092对0.094，90%区间覆盖实际分数的比例89.6%对84.2%）。局限也写明了：接近0%的分数区间覆盖不佳（80.5%），极弱的模型依赖少数已饱和的基准，估计最不稳定，且所有分数都是相对于两个锚点模型的相对值。

这是研究机构更改自家指数方法的一手资料，没有媒体交叉印证。指数页面的分数文件标注为11月5日更新，但我们打开时排行榜本身只显示「加载中」，因此顶端分数只转述了公告中的数字。

## 2. METR — 从外部测量Anthropic的研究速度（事实）

11月5日，METR发布了**《2026年10月Anthropic的AI研发加速独立评估》**。8月12日至10月29日约11周，约2.5名全职当量人员在Anthropic的设备上工作，合同**双方均不收费**，Anthropic免费提供分析用的token。METR拿到的有：内部基准分数和AECI（Epoch指数的Anthropic内部版本）、算法效率与模型强度的历史、人员数、训练算力、代码行数、「AI让你快了多少」的内部调查、推理支出、关于自主研究的内部文件，以及约15名员工的访谈。没拿到的也写明了：无法直接试用未公开模型；Anthropic可以隐去非公开信息，并且**隐去了METR认为最有价值的大部分证据**（Anthropic解释为「旨在去除可能加速其他AI开发者的机密信息」）。合同中原有的「核实算力在能力与安全之间如何分配」一项，在METR得出结论前被Anthropic中途撤掉。

结论如下。截至2026年10月，Anthropic在**「定义明确的任务」**（可自动评分或由语言模型评分的任务）上的能力提升速度约为2024年3月至2025年10月的**两倍**，METR表示即便是1.3倍或3倍也不会意外。按基准测试，2025年10月以来AECI的增速是此前的**1.9倍**（95%区间1.5–2.8倍），意味着过去两年的进展在一年内发生；换其他方法重算则在1.1–2.9倍之间。加速中**约80%归功于AI**是METR的主观估计，不确定性很大。METR确信这一加速**不是**由训练算力增长更快造成的。访谈集中在「AI带来约2倍」附近，内部Slack投票中有人自报用最强内部模型快了最多12倍，但METR称其为「非常松散的证据」。未来12个月内，在算法、训练算力、实验算力、数据方面没有找到明确瓶颈，但这一判断在工作中多次改变，信心有限。AI在最重要的训练工作中**完全自主**的贡献尚不显著，研究人员形容为「看到了苗头」。

同一天，METR还发布了对Anthropic 8月《风险报告》中「自动化研发风险」一节的审阅。METR同意截至7月15日的模型带来的灾难性风险较低，但称公开报告中「未越过2倍加速门槛」的说法是**过于自信的表述**。非公开报告中的数值约为1.97，METR自己的估计为1.3–2.8，因此门槛当时可能已经越过。美联社报道这一评估时提到，CEO Dario Amodei在9月12日的文章中呼吁行业放慢速度，并提议**把外部评估者放进实验室内部**，以METR为例；Sam Altman也表达了类似立场；Anthropic未立即回应置评请求。METR的文章还有利益冲突披露：一名团队成员曾与Anthropic讨论过职位并拒绝，且持有前雇主（竞争对手）的股权，因此其工作由无利益冲突的同事审核。

## 3. Uber — 3.2亿笔中，智能体占504笔（事实）

11月4日Uber第三季度财报电话会上，CFO Balaji Krishnamurthy单独说明了智能体带来的交易量（TechCrunch、BigGo）。BigGo称这是首次单独披露，TechCrunch没有「首次」一词，因此这只是BigGo一家的说法。10月的**万圣节周**是该季度最忙的一周，那一周AI智能体叫的**车是4单**，Uber Eats的**订单约500单**，而同一周Uber和Uber Eats合计**约3.2亿**次出行和订单。CEO Dara Khosrowshahi的原话是「非常、非常早期，牵引力非常有限」。他说在应用里叫车平均**约50秒**，重新点一份常吃的餐**约90秒**，目前主要AI助手约有8个，今后会超过10个。但他仍把智能体视为「触达我们平台的另一条路」，认为对需求是净增量，并说**「每一家AI系统公司都在和我们谈」**。报道点名的对象有Meta的Muse、OpenAI、Anthropic、Google、SpaceXAI的Grok和Instinct。这与一周前DoorDash所说「合计几百单」（NO.35）处在同一个位置。

BigGo还补充了Meta宣布Muse用户超过1,000万，以及Instinct的估值；两者都只见于我们核对过的一家媒体，后者又涉及投资判断，因此不写入正文。Uber第三季度整体业绩不在本文范围内。

## 简讯 — 月之暗面公开Kimi K3.1 Pro权重

月之暗面（Moonshot AI）把**Kimi K3.1 Pro**的权重上传到了Hugging Face（AI Times 11月5日报道，模型卡上没有发布日期）。据模型卡，这是总参数2.8万亿、每个token**激活1,040亿**的混合专家结构（896个专家中选16个，加2个共享专家），上下文100万token，支持文本和图像输入，许可证不是标准开源许可，而是**自定义的「Kimi K3.1 Pro许可证」**。基准测试全部为公司自报（例如Terminal-Bench 4.0得65.7，同一表格中Claude Opus 5.5为66.4），模型卡自己也写明对比模型是在不同的工具环境下运行的。在独立评估分数出来之前，按NO.34的做法，只放在「公司分数」一行。

## 把三个数字放在一起读（解读）

第一，**单一分数不再是答案。** NO.33中我们写过新记分板第一名和第二名是59对58。Epoch这次展示的是，顶端两个模型的差距90%区间为−0.9至+2.1分。1分的差距落在这个区间之内。Epoch自己写「Astra领先的概率72%」，和写「Astra第一」是两回事。意思是有28%是反过来的，两个模型实际上在同一行。今后看到「第一名」的报道，我们先要问「区间是否重叠」（解读）。

第二，**测量者在内还是在外，会改变数字。** Anthropic的公开报告写「不到2倍」，从外部进去的METR写「可能已经越过」。同一份数据出来的两句话。这就是NO.34主张把「公司分数」和「独立分数」分成两行的原因。但METR的数字也写明了自身局限：最有价值的证据被隐去，80%是主观估计，而且只测了「定义明确的任务」。独立评估不是给出「更准确的数字」，而是**给公司写下的那句话标注可信程度**，这样理解更准确（解读）。

第三，**实际使用的计数单位不同。** Epoch和METR的数字测的是「能做什么」，Uber的数字测的是「实际做了什么」。能力分数接近170的模型有好几个，最忙的一周叫车却只有4单。Khosrowshahi说的「50秒」是关键。顾客自己做50秒就能完成的事，如果智能体不能做得更快或更省事，能力再高也不会被使用。这和NO.35把「外卖应用上的几百单」放在每季度10亿单旁边来读是同一个位置。AI带顾客进来的大门（NO.38）开了，但眼下顾客自己走进来还是更快（解读）。

## 如果是我们 — 运营应用、电商和AI渠道的团队本周要做的三件事（实践）

1. **在模型选择表里加一栏「区间是否重叠」。** NO.17和NO.33写过按任务选模型的表，NO.34建议把公司分数和独立分数分成两行。这里再加一栏。从Epoch指数页面下载的分数文件里每个模型都有可信区间，两个候选模型的区间重叠就记为「同一行」，这时就不按分数，而按**价格、速度和我们自己的测试**来定。我们这边，先看应用里的成分说明、电商的商品描述、Ria剧本初稿这三项工作，现用模型和低一个价位的模型区间是否重叠。重叠就换成便宜的跑一周，再根据我们的测试结果决定是否换回。
2. **我们自己的「AI带来的速度」也用记录而不是自报来测。** METR把Slack投票的「12倍」归为松散证据，因为那是自报。我们是小团队，但有记录。把AP News的篇数、Ria剧本数、商品上架数、咨询回复数，以「打开定时任务的那一天」为分界点，前后各数相同长度的时段。像METR那样设一个分界点，比较斜率即可。然后在数字旁边像METR那样写上「其中AI占几成是估计」。本周先从AP News做起：把10月15日（开始每日发布）前三周和后三周的篇数、语种数、到上线的天数做成表，人工投入的时间另作估计。
3. **智能体渠道的数字要写在「顾客自己做要几秒」旁边。** 在NO.35做的「智能体渠道 — 开着，0单」表里再加一列。实际测一下顾客在我们应用里查一次成分、在电商里重新下一单各要几秒并记下来。如果智能体路径（Siri预览版、Shopify的智能体结账、聊天机器人对接）缩短不了这个时间，该渠道就「开着但不宣传」。这和Uber一边说「每家AI公司都在和我们谈」、一边说「我们的直接服务会是最省事的」是同样的姿态。数字开始离开0的时候，再连同算法一起写进NO.38的「AI路径三格」。

## 这次没有选的

OpenAI宣布用自动化流水线为948个Linux内核提权漏洞生成了可用的利用程序，以及「GPT-6 Cyber」的发布（评级「Critical」，通过Daybreak Red计划限制提供），都是大新闻，但原文（openai.com）打不开，而且题材是攻击能力，所以只留到以结果和措施为限的后续。OpenAI对齐团队关于「GPT-6 Astra在被框定为安全研究的任务上达成隐藏评分项的比例更低（约10%对16%）」的报告是NO.29的后续候选，但我们尚未打开原文。彭博关于苹果把部分工程师每日AI使用预算从300美元降到200美元的报道，原文被拦截，留到「价格与成本」的后续。Adweek关于Anthropic与美联社达成首个付费授权协议的报道依据两名匿名消息人士，双方未确认，且与我们有利益关系。Meta收购Conductor、OpenAI收购Pierre、Epoch的「博通TPU出货量环比翻倍（约197万个H100当量，Epoch估计）」、Learn:US 11月2日和5日的三篇新文章（在搜索和AI回答中曝光的手册、Firecrawl连接器、复刻技能）留作后续题材。Anthropic新闻页11月5日的「Announcements」条目看不到标题，无法确认是什么。

## 这条新闻中未能确认的

- 没有找到其他媒体对Epoch新方法的报道（作为研究机构的一手发布处理）。我们打开时排行榜是空的，顶端分数只用了公告里的数字，公告也没有说「Astra对Opus 5.5，72%」是基于哪一天的分数文件。
- METR的文章只读了前约10万字，后半部分（附录、详细方法）没有读。「约80%」是METR自己称为主观估计的值，1.9倍所依据的内部基准分数没有公开，我们无法重算。截至美联社报道时，Anthropic没有官方回应。
- Uber的4单、500单、3.2亿笔来自TechCrunch和BigGo两家转述同一场电话会的媒体，电话会文字记录和公司财报材料我们没能打开。「500单」是精确数还是四舍五入，4单车是通过哪些助手叫的，两篇报道都没有写。「首次单独披露」的说法只出现在BigGo。
- Kimi K3.1 Pro的发布日期不在模型卡上，只见于AI Times的报道（11月5日），基准测试为公司自报。独立评估分数尚未确认。

## 一起读过的文章

我们直接打开并核对了不同性质的来源。分为研究与评估机构的一手发布、公司发布与模型卡、媒体报道、我们此前的文章。

研究与评估机构：

- [Updating the Epoch Capabilities Index methodology to use a Bayesian model（Epoch AI，11月4日）](https://epoch.ai/publications/eci-bayesian-methodology) — 英文，方法变更的原因、结果、比较概率、局限
- [Epoch Capabilities Index（Epoch AI指数页面）](https://epoch.ai/benchmarks/eci) — 英文，可下载分数文件（含可信区间），标注11月5日更新
- [Independent Assessment of AI R&D Acceleration at Anthropic in October 2026（METR，11月5日）](https://metr.org/blog/2026-11-05-anthropic-ai-rd-acceleration-assessment/) — 英文，访问范围、数值、局限、利益冲突披露
- [Review of the "Risks from automated R&D" section in Anthropic's Risk Report（METR，11月5日）](https://metr.org/blog/2026-11-05-rd-section-anthropic-risk-report-august-2026-review/) — 英文，关于「2倍门槛」的分歧

公司发布与模型卡：

- [Kimi K3.1 Pro模型卡（moonshotai，Hugging Face）](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) — 英文，结构、上下文、许可证、公司自报基准

媒体报道：

- [Anthropic is rapidly accelerating AI development amid slowdown calls, outside research group says（美联社，ClickOrlando转载）](https://www.clickorlando.com/business/2026/11/05/anthropic-is-rapidly-accelerating-ai-development-amid-slowdown-calls-outside-research-group-says/) — 英文，METR评估摘要、Amodei的9月文章、Anthropic未置评
- [Almost no one uses AI agents to book their Uber, company says（TechCrunch）](https://techcrunch.com/2026/11/04/almost-no-one-uses-ai-agents-to-book-their-uber-company-says/) — 英文，4单、500单、3.2亿、50秒、90秒、Khosrowshahi的发言
- [Uber Says AI Agents Booked Just 4 Rides in Its Busiest Week of October（BigGo Finance）](https://finance.biggo.com/news/e8f7454e-1d52-4061-9de6-e1ccd47c8bc4) — 英文，相同数值、「CFO首次单独披露」的说法（仅BigGo）、Muse 1,000万（单一来源）

我们此前的文章：

- [GitHub上每十个拉取请求有四个是智能体发起的 — 新记分板的第一名还不是谁都能调用（AP News NO.33）](https://www.apholdings.kr/ko/news/agent-prs-40-percent-and-a-new-number-one/)
- [每周AI资讯 — Mistral放下了一万亿参数（AP News NO.34）](https://www.apholdings.kr/ko/news/weekly-2026-10-31/)
- [审计员走进了大楼 — Anthropic向METR开放「员工级访问权限」（AP News NO.24）](https://www.apholdings.kr/ko/news/inspectors-inside-the-building/)
- [数出AI实际在做什么的三个数字 — 外卖应用上智能体下的订单是「几百单」（AP News NO.35）](https://www.apholdings.kr/ko/news/what-ai-actually-does-three-counts/)
- [AI带顾客进来的大门变成了三扇（AP News NO.38）](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
