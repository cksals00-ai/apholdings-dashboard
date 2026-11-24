---
no: 51
slug: open-weights-take-seven-in-ten-tokens
date: 2026-11-18
category: 洞察
tags: 开放权重 · OpenRouter · Hugging Face · token占比 · Meta Muse Ember · 小型模型 · 每任务成本 · llama.cpp · 本地运行 · Stripe · 英伟达
title: 每十个token中有七个流向开放权重模型 — Hugging Face将自己的推理路由交给OpenRouter，同时公布了路由器统计“开放权重占比26.8%→71.7%，价格是闭源模型的四分之一”；Meta带着“同样的价格，每任务成本只有三分之一”进入最小模型这一格；本地运行器llama.cpp在三年半后迎来1.0
summary: Hugging Face于11月16日在官方博客写道，将语言模型推理路由迁移至OpenRouter，并公布了OpenRouter统计的数字 — 开放权重模型占token的比重从2025年10月的26.8%升至2026年9月末的71.7%，平均单价约为闭源模型的四分之一（公司测量）。我们直接打开OpenRouter排行榜，确认本周token前4名全部是中国公司的模型。不过，这两家公司都是今年夏天和初秋分别宣布Stripe（OpenRouter）、英伟达（Hugging Face）同意收购的公司，而11月16日的文章中没有写到这一事实。Meta于11月9日以每100万token 0.10/0.50美元推出了“最小模型”Muse Ember，独立评测（Artificial Analysis）的每任务成本为0.14美元，约为同一价目表上Claude Haiku 5.5（0.41美元）的三分之一。本地运行器llama.cpp于11月13日发布1.0.0，并承诺“API破坏兼容就升主版本号”。我们把三条消息归为“token沿着价目表流动 — 但那张价目表由谁测量、由谁所有”。
---
> 本文由AI（Claude）协助撰写，并经编辑审核。我们公司是Anthropic和OpenAI两家公司的付费客户，也在测试中使用谷歌的模型。**开发了撰写本文的AI的Anthropic，其模型在本期消息中三次作为比较基准出现** — Hugging Face的文章将Kimi K3.1 Pro的分数与成本和Claude Fable 5.2并列，Meta将Muse Ember与Claude Haiku 5.5比较，OpenRouter排行榜第6位是Claude Opus 5.5。因此我们不对任何模型附加评价，只转述已公布的数字和表述。公司公布的数值标为“公司公布的数据”，平台在自己流量中统计的数值标为“该平台自身的测量”，仅有单一来源的内容则一并注明来源。文中出现的收购消息只转述已报道的事实，本文不构成对任何特定企业的投资建议。

我们在NO.48写过“更换模型需要几周”，在NO.46写过“不要读token价格，要读每任务价格”，在NO.41写过“‘开放权重’这一个词下面有三种许可条件”。本期三条消息展示了这些数字流向了哪里 — **经过路由器的每十个token中有七个流向开放权重模型**，最小模型那一格里来了一位拿着同样价目表的新选手，而在自己电脑上运行这些模型的工具到了1.0。我们分事实、解读、“如果是我们”三部分来写。

## 1. Hugging Face → OpenRouter — 移交路由的同时公布的“开放权重71.7%”（事实·公司公布·平台测量）

Hugging Face于11月16日在官方博客发布了**“Hugging Face and OpenRouter join forces to make open-weight models easy to run”**。我们直接读了原文。内容有两部分。一是产品变更 — Hugging Face的“Inference Providers”**将语言模型请求的路由从自家路由器迁移到OpenRouter的路由器。**Hub上的开放权重模型无论由哪家供应商提供服务，都可以用一个Hugging Face token调用；每次请求由OpenRouter按价格、速度、稳定性选择供应商，失败时转发给另一家供应商（文章写道，此前该供应商的错误会原样返回）。可以在模型名后加`:fastest`、`:cheapest`或供应商名称来指定，每轮对话用请求头（`X-HF-Session-Id`）发送相同ID，就会固定到持有提示缓存的供应商。支持OpenAI的Chat Completions、Responses格式以及Anthropic的Messages格式，并附有Claude Code、Codex、OpenCode等编码工具的配置指南。**有一项破坏性变更 — 语言模型不再能使用自己的供应商API密钥**（图像、视频密钥不受影响）。文章写道价格按供应商原价、Hugging Face方面不加收费用，在设置中关闭某个供应商后，路由器就不会再向其发送请求。图像、视频、音频生成不在本次变更范围内。

另一部分是数字。全部是**OpenRouter在自己流量中统计的数据**。开放权重模型占token的比重从**2025年10月的26.8% → 2026年9月末的71.7%**（7月最高77.5%），同期开放权重的每周token量增长60倍以上，闭源模型增长约10倍。本周使用最多的模型是DeepSeek V4.1 Flash 1017，59.2万亿token。平均单价方面，开放权重每100万token输入0.28、输出1.62美元，闭源模型为1.27、6.36美元 — **约4倍差距**。文章引用Artificial Analysis智能指数，将开放权重第一的Kimi K3.1 Pro（46分、每任务3.68美元）与总榜第一的Claude Fable 5.2（65分、26.54美元）并列（我们11月18日直接打开AA排行榜确认了相同数字 — 相差19分，成本约7倍）。OpenRouter的规模为**每月800万亿token以上、用户1,000万以上、模型600个以上、供应商80家以上**，重写路由器后容量错误减少46%、首token时间改善16.9%、吞吐量提升16.3%（OpenRouter测量）。文章没有直接引语，以多名Hugging Face员工的名义发布。

我们于11月18日**直接打开了OpenRouter排行榜（openrouter.ai/rankings）。**截至11月16日的每周token前10名为：DeepSeek V4.1 Flash 1017（61.2万亿）、腾讯Hy4（16万亿）、DeepSeek V4.1 Flash（15.5万亿）、Z.ai GLM 5.3 Flash（11.8万亿）、GPT-6 Luna（8.08万亿）、Claude Opus 5.5（7.37万亿）、StepFun Step 5 Preview（6.36万亿）、小米MiMo-V2.6-Flash（4.16万亿）、GLM 5.3（3.74万亿）、GPT-6.1 Sol（3.71万亿）。**前4名全部是中国公司的模型**，美国模型位于第5、6、10位。第1名的数字在博客文章（59.2万亿）和排行榜（61.2万亿）中略有不同，看来是统计时点的差异，但我们未能确认。排行榜文本中没有总量和开放/闭源占比的数字。作为背景，OfficeChai（6月26日）转载的彭博图表（数据来自OpenRouter、Exponential View）显示，谷歌、OpenAI、Anthropic三家公司的token占比从2025年6月约70% → 2026年6月约30%（近似值，无方法论说明）。

这里有一点需要记下。**这两家公司今年都有过收购公告。**路透社（8月19日）报道Stripe已同意收购OpenRouter（价格未公开，消息人士称“略高于80亿美元”；维基百科转引彭博、WSJ的“70亿美元以上”），Stripe CEO表示“token是用AI创造价值的公司的核心货币”。英伟达（Nvidia）于9月4日宣布以129亿美元收购Hugging Face（《财富》、Advanced Television报道为“达成协议”阶段，是否已完成交割我们未能确认），黄仁勋在博客中写道“Hugging Face将继续作为面向整个AI生态的开放平台，并非必须使用英伟达的算力”（Advanced Television引用）。**11月16日的文章对这两起收购均未提及。**路透社报道中的OpenRouter规模（每天10万亿token、开发者1,000万）和维基百科上的公司主张（每月400万亿token）与11月的文章（每月800万亿）时点不同，我们照原样保留。

## 2. Meta Muse Ember — 最小的一格里“同样的价格，每任务三分之一”（事实·公司公布·独立评测）

我们直接读了Meta AI研究博客（11月9日）的**“Introducing Our Smallest, Most Efficient Model: Muse Ember”**。用途是“复杂推理的执行和智能体整天重复的工作” — 工具调用、编码子任务、路由、抽取、长文档解析。价格为**每100万token输入0.10、缓存输入0.004、输出0.50美元**，超过20万token的提示为0.30、0.012、1.50美元。上下文100万token，输出最多51万2,000token。可通过Meta Model API（`muse-ember-1.0`）、Muse Code、谷歌云、甲骨文云使用。公司的表格以最高推理档位为基准与GPT-6 Luna、Claude Haiku 5.5比较 — AutomationBench-AA 37.8% vs 20.2%/13.9%，Terminal-Bench 4.0 40.9% vs 16.4%/39.2%，OSWorld 2.1 69.5% vs 50.5%/68.9%，**FrontierCode 2.0-AA为27.2% vs 25.2%/34.9%，Haiku领先。**Artificial Analysis智能指数36分“与Haiku 5.5持平，高于Luna（28）”，而**“以约三分之一的成本追平了Haiku 5.5的最高分”**是公司的总结语句。与自家上位模型Muse Spark 1.3（指数37、每任务约2.39美元）相比低1分、成本约为十七分之一。文章自己写道，多项基准为内部测量，部分使用了特定测试框架或部分分数。发布前通过“Meta Superintelligence Scaling Framework”评估了化学、生物、网络安全、失控风险，均低于高风险门槛，并经过了智能体行为评估（拒绝网页、工具输出中隐藏的指令，在高影响行动前询问人类）。**没有提及开放权重。**

我们直接打开了独立评测方。**Artificial Analysis的Muse Ember页面**写道：智能指数（v5.0.1）最高档位36（同级36个中第2位）、xhigh 34，**每任务0.14美元**，输出速度449token/秒，每任务3.1分钟（同级中位数为智能24、单价0.24/0.83美元）。**AA总排行榜**（11月18日）：Claude Haiku 5.5 Max 36分、每任务0.41美元，GPT-6 Luna Max 28分、0.15美元，DeepSeek V4.1 Flash 1017 Max 33分、0.60美元，Muse Ember Max 36分、0.14美元 — Meta的“三分之一”与该表的0.14对0.41相符。Simon Willison（11月10日）指出的是价目表 — **Ember、Luna、Haiku 5.5三者的短提示价格同为0.10/0.50美元**，不同的是“长提示”的门槛（20万/27万2,000/10万token）和之后的价格（Haiku为0.50/2.50美元）。因此他写道“token单价是一种弱比较 — 同一任务所消耗的token数因模型而异”，并把AA的每任务成本（Ember xhigh约0.12、max 0.14，Haiku xhigh约0.25，Luna xhigh约0.10美元）转为图表。在他的测试中，六个推理档位中“high”没能完整输出SVG，而且档位并不能干净地预测结果质量。**Ember是否公开权重，在Meta的文章、AA页面、Willison的文章中都没有提到。**

## 3. llama.cpp 1.0.0 — 本地运行器承诺“破坏兼容就升版本号”（事实·项目公告）

我们直接读了ggml-org在Hugging Face博客（11月13日）发布的**“Hot llama.cpp v1.0.0: A stronger foundation for the local AI ecosystem”**。llama.cpp是在自己的电脑（笔记本、服务器、移动设备）上运行LLM的C/C++运行器，从首次提交起**约三年半**后，为两个库（`libllama`、`libggml`）标上了1.0.0。承诺是**语义化版本** — 破坏公开C API的变更升主版本号，兼容的功能和新模型支持升次版本号，bug修复升补丁号。支持的模型架构150种以上，支持主流推测解码方法，分发渠道有Docker、Debian、Homebrew、conda-forge、MacPorts、Winget、XCFramework，CI运行在Hugging Face Buckets、Jobs以及**英伟达、AMD、高通、Arm、IBM、英特尔**提供的自托管运行器上。文章中没有GitHub星数、下载量、贡献者数和许可证（我们没有打开代码仓库），评论区有人指出极长提示的处理速度仍是课题，也有人问“没有Linux桌面应用吗”（文章提到的桌面应用是macOS、Windows）。

## 三条消息一起读（解读）

第一，**token不是沿着分数表、而是沿着价目表流动 — 但必须写明“经过哪道门的token”。**71.7%是经过OpenRouter这一个路由器的token占比。与模型公司直接签约的企业的token、在云内部运行的token都不在这个数字里。NO.16写过“哪款AI用得最多 — 为什么数字各不相同”，Ramp的企业卡支付数据（NO.47：按美国企业的支付计，Anthropic 44.8%、OpenAI 40.6%）和OpenRouter的token数据（前4名是中国模型）是从不同的门看同一个月的同一个市场。两者可以都对 — 一个是“谁在付钱”，一个是“哪个模型在吃token”。而且token量和钱是两回事（NO.43的“token量↑37%、支出↑9%”）。把Hugging Face文章写的平均单价（开放0.28/1.62、闭源1.27/6.36美元）原样放进去非常粗略地算一下，即使71.7%的token是开放权重，**按金额算很可能不到一半**（我们的计算，不知道输入、输出比例，只看数量级的程度 — 请勿照搬这个数字）。也就是说，“七成”是量的七成，不是营收的七成。

第二，**最小的一格因为价目表相同，变成了无法凭价目表挑选的一格。**Ember、Luna、Haiku 5.5的短提示价格三者都是0.10/0.50美元。不同的是每任务成本（0.14、0.15、0.41美元，AA）、长提示门槛（20万、27万2,000、10万token）和分数（36、28、36）。NO.46用Hydrogen和Flash写过“token价格≠任务价格”，这次是**价格相同的三个模型在每任务成本上相差3倍** — 因为同一件事所消耗的token数不同，而这个数字只能来自独立评测和我们自己的记录，而非制造商。Meta的“三分之一”与AA的表相符是好信号，但AA的每任务成本是在AA自己的评测集上的值，并不意味着在我们的工作中会出现同样的比例（NO.21）。公司的表格保留了“FrontierCode是Haiku领先”这个输掉的格子，这一点也记下来 — 像NO.44的Anthropic表格一样，有输掉格子的表比没有的更值得读（解读）。

第三，**出数字的平台换了主人。**统计出开放权重71.7%的OpenRouter，是一家支付公司宣布同意收购的公司；公布这个数字的Hugging Face，是一家芯片公司宣布同意收购的公司。没有任何证据表明两家公司中的任何一方扭曲了这个数字，我们也不这样写 — 只是“因为是中立市场所以是干净的信号”（OfficeChai 6月文章的表述）这一解释，现在需要多加一行：“由支付公司所有的市场”。黄仁勋写的“继续作为开放平台、并非必须使用英伟达算力”是对这个问题的回答，而Hugging Face文章中的破坏性变更（“不再能使用自己的供应商密钥”）和“可以关闭供应商”的开关，是同一个问题的缩小版 — **让路由器来选很方便，代价是我看不到谁在选。**在它的对面是llama.cpp 1.0。NO.48写过“只有放在模型之外的东西才能带到下一个模型”，运行模型的运行器也是“放在外面的东西”，而1.0是一个承诺：这个外面的盒子的API至少在同一主版本号内不会被破坏。三条消息归根结底是同样的三个选项 — 交给路由器、直接调用制造商API、在自己的电脑上运行 — 三者的差别不在价格，而在**“谁来选、数据去哪里、坏了谁来修”**。

## 如果是我们 — 运营电商、应用和AI网红的团队本周要做的三件事（实践）

1. **在模型成本表中加入“路径”列。**在NO.46做的“每任务成本”列旁边，写上该模型是通过哪道门调用的 — 制造商API直连 / 路由器（OpenRouter、Hugging Face Inference Providers等） / 本地（llama.cpp） — 并为每条路径附上三格：供应商由谁选（我们·路由器），提示和响应经过哪家公司的服务器（路由器则记下供应商列表），能否使用自己的密钥（Hugging Face自11月16日起语言模型不可）。如果有使用路由器的工作，就把**“关闭的供应商”列表**在设置中实际保存下来并记上日期。像成分表判定（NO.03）那样含有顾客数据的请求，不发送到“供应商不由我们选择的路径” — 用一行规则写下来。
2. **用同样的20件任务测一测最小一格的三个模型。**从Lia（我们的AI网红）脚本的简短校对、电商咨询分类、成分表条目抽取中，选出重复度高的20件任务，用**同样的推理档位**跑Muse Ember、Claude Haiku 5.5、GPT-6 Luna，记录完成件数、实际输入/输出token数、每任务成本、耗时（与NO.48“模型更换演练”的4格同一张表）。在表头写上三个模型的长提示门槛（20万/10万/27万2,000），就能立刻看出我们的提示会越过哪道门槛。AA的0.14/0.41/0.15美元放在“参考值”一格 — 我们的数字出来后放在旁边。
3. **定一个本地1.0测试。**用llama.cpp 1.0.0在办公电脑上跑起一个开放权重小型模型，看成分表判定中**掺有个人信息的问题（过敏、正在服用的药物）**20件能否在不外传的情况下处理 — 记录判定质量、响应时间、我们能承担的设备配置。在NO.48的“模型外的盒子”中加入**运行器名称和版本一格**（llama.cpp 1.0.x）。结果不好就写不好 — 这个测试的目的不是迁移到本地，而是用数字掌握“能迁和不能迁的工作”的边界。

## 本期没有选的内容

OpenAI于11月16日发布的三篇文章 — 学术研究者试点分析（1,819人、58万186条消息、“没有AI会多花1.9倍时间”的自我报告）、研究者计划扩大到20万人（11月23日5万份资助）、ChatGPT for Healthcare（医生盲评1,300件以上） — 我们只通过AI-Weekly（11月17日）的摘要看到，openai.com在我们这边打不开，因此没有写（与NO.40的METR“1.9倍”出现相同数字这一点是后续候选）。英伟达第三季度财报（11月17日）和CEO更换的相关报道属于投资、个人领域，不写。Anthropic新闻室11月17日的条目没有显示标题，搜索中能看到的同日消息与上市有关，不写（利益关系、投资）。Simon Willison的llm 0.37.2（修复API密钥泄露到其他供应商的缺陷）属于安全事项，只留标题。Fireworks AI、Notion安全事件（AI-Weekly）也只留标题。奥克兰市工会的“因AI而岗位变动时，以再培训、再安置代替解雇”条款（AI-Weekly）我们没有打开原文。Hugging Face新增的“Decision Models”类别（11月10日）作为NO.47 Decisions API的后续候选保留。OpenAI新闻列表这次也打不开，Google AI Blog、Axios仍然是旧版列表。

## 本期消息中我们未能确认的内容

- 71.7%、4倍、800万亿、1,000万、46%、16.9%、16.3%全部是OpenRouter在自己流量中统计的数值，没有独立验证。“本周第1名59.2万亿”（博客）与排行榜的61.2万亿为何不同，我们未能确认。排行榜的总量和开放/闭源占比数字不在文本中。
- Stripe–OpenRouter的收购价格未公开，“略高于80亿美元”来自路透社消息人士，“70亿美元以上”来自彭博、WSJ（经维基百科转引）。英伟达–Hugging Face的129亿美元是公告数值，两起交易是否已完成交割我们未能确认。黄仁勋的“开放平台”语句是Advanced Television引用其博客，我们没有打开博客原文。
- 彭博图表的“70%→30%”是OfficeChai转载的近似值，我们没有看到方法论。
- Meta的基准数值是公司的表格，部分是内部基准、特定测试框架、部分分数。“三分之一”与AA的表相符，但AA的每任务成本以AA评测集为基准。Ember是否公开权重，哪里都没有写。Willison的Haiku xhigh 0.25美元与AA排行榜的Haiku Max 0.41美元因推理档位不同，我们照原样保留。
- llama.cpp的文章中没有星数、下载量、贡献者数、许可证，我们没有打开代码仓库。
- 解读中的“按金额算很可能不到一半”是我们用Hugging Face文章的平均单价做的粗略计算，是不知道输入、输出比例的估算。
- 任何公司的公告，我们都没有直接测试或统计过。

## 一起读的文章

我们直接打开并确认了性质不同的来源。分为公司公告·官方文档、独立评测·数据、媒体报道、个人博客、维基、我们之前的文章。

公司公告·官方文档：

- [Hugging Face and OpenRouter join forces to make open-weight models easy to run（Hugging Face博客，11月16日）](https://huggingface.co/blog/openrouter) — 英文，路由迁移·`:fastest`·`:cheapest`·缓存请求头·不可用自己的密钥·开放权重26.8%→71.7%·单价4倍·Kimi 46/3.68 vs Fable 65/26.54·每月800万亿·用户1,000万（OpenRouter测量）
- [Introducing Our Smallest, Most Efficient Model: Muse Ember（Meta AI，11月9日）](https://research.meta.ai/blog/muse-ember) — 英文，0.10/0.50美元·1M上下文·公司基准表（FrontierCode为Haiku领先）·“Haiku三分之一成本”·安全评估·未提及开放权重
- [Hot llama.cpp v1.0.0: A stronger foundation for the local AI ecosystem（ggml-org，Hugging Face博客，11月13日）](https://huggingface.co/blog/ggml-org/llama-cpp-v1) — 英文，语义化版本·150+架构·分发渠道·6家硬件公司的CI运行器

独立评测·数据：

- [OpenRouter Rankings — 每周token使用量（截至11月16日）](https://openrouter.ai/rankings) — 英文，前10名模型·token数（11月18日直接确认）
- [Muse Ember — Artificial Analysis模型页面](https://artificialanalysis.ai/models/releases/muse-ember) — 英文，智能指数v5.0.1 36（max）·34（xhigh）·每任务0.14美元·449token/秒·同级中位数
- [Artificial Analysis Intelligence Index排行榜](https://artificialanalysis.ai/leaderboards/models) — 英文，Fable 5.2 65/26.54·Kimi K3.1 Pro 46/3.68·Haiku 5.5 36/0.41·Ember 36/0.14·Luna 28/0.15·DeepSeek V4.1 Flash 1017 33/0.60（11月18日直接确认）

媒体报道：

- [Payments firm Stripe to buy marketplace OpenRouter in AI push（路透社，The Star刊载，8月20日）](https://www.thestar.com.my/tech/tech-news/2026/08/20/payments-firm-stripe-to-buy-ai-developer-platform-openrouter) — 英文，8月19日达成协议·价格未公开（消息人士80亿美元↑）·每天10万亿token·Collison“token是核心货币”
- [It's official: Nvidia to acquire Hugging Face for $12.9 billion（《财富》，9月4日）](https://fortune.com/2026/09/04/its-official-nvidia-acquire-hugging-face-12-9-billion/) — 英文，公告阶段·Delangue发言·用户1,800万·企业20万（公司数值）
- [Nvidia acquires Hugging Face for $12.9bn（Advanced Television，9月4日）](https://www.advanced-television.com/2026/09/04/nvidia-acquires-hugging-face-for-12-9bn/) — 英文，119亿+员工激励10亿·黄仁勋“继续作为开放平台·并非必须使用英伟达算力”（引用博客）
- [Share Of US Models Being Used On OpenRouter Has Collapsed From 70% To 30%（OfficeChai，6月26日）](https://officechai.com/ai/share-of-us) — 英文，引用彭博图表（OpenRouter·Exponential View）·近似值·“中立市场”表述（背景）

个人博客：

- [Introducing Our Smallest, Most Efficient Model: Muse Ember（Simon Willison，11月10日）](https://simonwillison.net/2026/Nov/10/muse-ember/) — 英文，三个模型同样的价目表·长提示门槛差异·“token单价是弱比较”·AA效率边界图·六个推理档位测试

维基：

- [OpenRouter（Wikipedia）](https://en.wikipedia.org/wiki/OpenRouter) — 英文，2023年成立·所有者Stripe·彭博/WSJ“70亿美元↑”·公司主张每月400万亿token·1,000万MAU
- [Hugging Face（Wikipedia）](https://en.wikipedia.org/wiki/Hugging_Face) — 英文，2016年成立·2026-08-26报道英伟达收购协议129亿美元（交割未确认）·2025年拒绝英伟达5亿美元

我们之前的文章：

- [在智能体到来之前写下“可以做的事”的三份文档（AP News NO.50）](https://www.apholdings.kr/ko/news/allowed-list-before-the-agent-arrives/)
- [更换模型需要几周 — 只有放在模型之外的东西才能带走（AP News NO.48）](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [每周AI消息 — 谷歌在五天内更换了三个模型和搜索，OpenAI把钱包交到了智能体手里（AP News NO.47）](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [“每天用的模型”这一格出现了 — 用每任务成本来读的方法（AP News NO.46）](https://www.apholdings.kr/ko/news/hydrogen-daily-driver-price-per-task/)
- [同一个模型有两道门 — Fable 5.2与Mythos 5.2（AP News NO.44）](https://www.apholdings.kr/ko/news/fable-5-2-two-doors-and-sandbagging-logs/)
- [顾客无法带来自己的智能体（AP News NO.43）](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [每周AI消息 — 2.8万亿、2,800亿、5,940亿参数的三个模型放出或预告了权重（AP News NO.41）](https://www.apholdings.kr/ko/news/weekly-2026-11-07/)
- [比较数字之前先看算法（AP News NO.21）](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [哪款AI用得最多 — 为什么数字各不相同（AP News NO.16）](https://www.apholdings.kr/ko/news/who-uses-which-ai/)
- [当AI代替我们读成分表时（AP News NO.03）](https://www.apholdings.kr/ko/news/ai-reads-the-label/)
