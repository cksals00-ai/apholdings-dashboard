---
no: 22
slug: meta-muse-wonder-whose-scorecard
date: 2026-10-15
category: 洞察
tags: Meta · Muse Wonder · 模型评测 · 独立评测 · 训练设置
title: Meta首个顶级模型Muse Wonder——分数是谁打的,使用前要看的三件事
summary: Meta于10月12日发布了首个前沿级模型。我们把公司自己公布的分数与独立评测机构的分数并排放在一起,再梳理价格、使用方式和训练设置——用在我们工作中之前要确认的三件事。
---
> 本文由AI(Claude)协助撰写,并经编辑审核。文中作为比较对象出现的Claude模型的开发者Anthropic,同时也是我们写作所用工具的提供方,因此我们存在利益关联。公司公布的数字标注为"公司公布",独立评测另行标注。本文不构成对任何公司或股票的投资意见。

10月12日(周一),Meta的Superintelligence Labs发布了Muse Wonder和Muse Wonder Full两个模型,Meta称之为自己的首批前沿级模型。这条消息值得关注的,与其说是分数本身,不如说是谁在什么条件下测的分数。

## 发布了什么(事实)

- Muse Wonder可通过Meta的模型API和编程工具Muse Code使用。API价格为每百万输入token 4美元、每百万输出token 20美元(缓存输入为0.20美元,据独立评测机构Artificial Analysis)。
- Muse Wonder Full仅限Muse Code订阅用户,不通过API提供(TechCrunch)。根据Meta的Muse Code订阅说明,Full包含在四档套餐中最高的两档(Power和Maximum)里,LetsDataScience和DataNorth报道称这两档套餐为每月50美元和200美元。
- 两个模型的上下文窗口均为100万token,输入支持文本、图像、视频和音频,输出为文本(Artificial Analysis)。
- 两个模型的权重能否下载,我们没能确认(说不能下载的只有LetsDataScience一家)。Decrypt指出,Meta实际上已经停止了曾公开权重的Llama系列。

## 如何读这张成绩单

**公司公布的。** Meta称,在自家的"Personal Superintelligence Index"上Wonder Full得59.1分,高于Opus 5.5(55.2)和GPT-6 Astra(54.5),在记忆测试MemoryBench上也以约85.5分领先(Decrypt转述的Meta说法,iThome和Latent Space的报道数字相同)。Decrypt指出,这两项指标都是Meta自己设计的,指数的计算公式未公开。

**独立评测。** 在Artificial Analysis的综合指数(v4.3,最高投入设置)上,Wonder Full为56分,Wonder为52分,Meta上一代模型Muse Spark 1.3为48分。同一指数上Opus 5.5为58分,Sonnet 5.5为56分,GPT-6 Astra为53分(在Artificial Analysis排行榜上直接确认,均为各模型的最高设置)。也就是说,按独立评测,它大约排在第三位上下,与公司指标所说的"领先"并不一致。

**再细看一点。** Artificial Analysis在同一篇文章中写道,在编程智能体指数上,Wonder Full为68分,与运行Sonnet 5.5的Claude Code持平,高于Opus 5.5(66)。但在知识测试AA-Omniscience上,Full为30分,Wonder为25分,明显低于Opus 5.5(46)和GPT-6 Astra(43)。它胡编乱造的比例(幻觉率)偏低——Full为23%,Wonder为27%——但在指数45分以上的模型中,最低的是Gemini 4 Argon的15%。

## 使用前要看的三件事(解读)

**1. 完成一件事的成本。** token单价相同,完成一件事的成本也可能不同。Artificial Analysis运行同一组任务的成本为:Wonder 4.52美元,Opus 5.5 5.98美元,Sonnet 5.5 5.46美元,GPT-6 Astra 3.26美元,Gemini 4 Argon 1.99美元,GPT-6.1 Sol 0.72美元。它认为Wonder比多数智能水平相近的模型更贵。有报道称其价格与Opus 5.5相当(Decrypt),但我们看的数字是每件事的成本,而不是单价。

**2. 能在哪里用。** 分数最高的Wonder Full只能在订阅内使用,无法通过API接入我们的自动化。能通过API使用的是分数低一档的Wonder。

**3. 我的代码和文章去了哪里。** 根据Meta的Muse Code订阅说明,订阅默认是"Contributor模式":Meta可以用你的提示词、代码、文件、上下文以及你收到的回答来训练今后的模型,作为交换你可以获得更多用量。说明中写道关闭后此后的内容不会用于训练,但没有说明已经发送的内容如何处理,因此我们没能确认。通过API使用的Wonder没有这个模式,标准模式下的内容据称不用于训练。我们没能自行打开Meta的使用条款原文,因此使用前需要在条款和设置界面确认。

## 我们没能确认的

我们没能直接打开Meta的官方发布和模型卡。上面"公司公布的"内容是通过TechCrunch、Decrypt、iThome等报道确认的。订阅与训练设置是我们直接打开Meta的Muse Code订阅说明页面确认的。Decrypt称,Meta承诺的完整安全报告尚未发布。实际使用者Simon Willison写道,Wonder有六档推理级别(minimal到max),画出的图似乎比上一代更好,但他自己说明这只是基于一种图画的非正式测试。不应把它当作分数来读。

## 我们的看法

**事实:** Meta发布了只能通过API和订阅使用的顶级模型;公司指标与独立指标呈现的画面不同;最高档模型仅限订阅;订阅的默认设置会把你的内容用于训练。

**解读:** 每次有新模型发布,"它是第一"和"它是第三"都会同时出现。两者可能都不假,因为测试的出题方和运行设置不同。

**如果是我们:** 不凭一个数字换模型。我们用自己的20件真实工作(脚本草稿、商品描述、评论分类)在相同条件下跑一遍,记录"每件成本"和"修改次数",经人工确认后才对外发布。客户信息和未公开资料不放进可能被用于训练的设置里。

## 一并阅读的文章

我们直接打开了不同性质的来源进行确认。数字以各来源为准。

- [Meta releases its first frontier model, Muse Wonder (TechCrunch)](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder) — 英文,新闻报道
- [Muse Wonder / Wonder Full evaluation (Artificial Analysis)](https://artificialanalysis.ai/articles/muse-wonder) — 英文,独立评测机构
- [Meta Muse Wonder and the frontier AI race (Decrypt)](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race) — 英文,新闻报道(公司指标与独立指标)
- [Meta's best model skips API, coding plan trains on your code (LetsDataScience)](https://letsdatascience.com/blog/metas-best-model-skips-api-coding-plan-trains-on-your-code) — 英文,订阅与训练设置
- [llm-meta-ai 0.2 (Simon Willison)](https://simonwillison.net/2026/Oct/12/llm-meta-ai/) — 英文,实际使用者的博客
- [Meta releases Muse Wonder, its first frontier-class AI model (AI Weekly)](https://aiweekly.co/alerts/meta-releases-muse-wonder-its-first-frontier-class-ai-model) — 英文,简报(转述其他媒体)
- [Muse Code Subscriptions (Meta)](https://dev.meta.ai/docs/muse-code/subscriptions) — 英文,Meta官方说明
- [Models Leaderboard (Artificial Analysis)](https://artificialanalysis.ai/leaderboards/models) — 英文,独立评测机构排行榜
- [Meta's Muse Wonder (DataNorth)](https://datanorth.ai/news/metas-muse-wonder) — 英文,分析(套餐与训练设置)
- [Muse Wonder报道 (iThome)](https://www.ithome.com.tw/news/179608) — 繁体中文,新闻报道
