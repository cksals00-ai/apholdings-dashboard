---
no: 46
slug: hydrogen-daily-driver-price-per-task
date: 2026-11-13
category: 洞察
tags: Gemini 4 Hydrogen · 谷歌 · 模型价格 · Artificial Analysis · Epoch AI · 推理成本 · 模型选择 · AlphaProof Code
title: 「每天用的模型」这一格出现了 — 谷歌把 Gemini 4 Hydrogen 定在 Flash 两倍的价格，独立评测机构测得「比 Argon 高 1 分、每个任务 1.87 美元」，Epoch 则数了一块芯片能同时接多少请求
summary: 11 月 12 日，谷歌发布 Gemini 4 Hydrogen。定位是「Carbon 和 Argon 负责深度思考，Hydrogen 把每天的活儿快速干完」，价格为每百万 token 输入 1.50 美元、输出 7.50 美元，是 Gemini 3.8 Flash 的两倍（VentureBeat 整理称 Flash 本身也将在 2027 年 1 月 1 日涨到同样价格）。它同时进入 API、应用和搜索，并通过自动模型选择触达免费用户。独立评测机构 Artificial Analysis 在默认设置下测得智能指数 51（Argon 50）、每个任务成本 1.87 美元。Epoch AI 于 11 月 9 日发布「推理性能指数」，数的是一块芯片能同时服务多少请求，并写道最新芯片按 FLOP/s 算是 2.5 倍，按这个算法却是 25 倍。我们把三件事归为「按任务而不是按 token 读价格的方法」，结尾用「简短」记下谷歌 DeepMind 宣布在四周内对 Signal 协议代码完成形式化验证。
---
> 本文由 AI（Claude）协助撰写，并经编辑审核。我们公司是 Anthropic 和 OpenAI 两家的付费客户，也在测试中使用谷歌模型。第 1 条和「简短」是谷歌的发布，而谷歌与撰写本文的 AI 的制造商（Anthropic）存在竞争关系。第 2 条的独立评测榜首是 Anthropic 的模型，因此**我们不加评价，只搬数字。** 公司发布的数值标注为「公司发布」，本文不是对任何公司的投资意见。

在 NO.45 中我们写过「模型的门先向一部分人打开，两个月后价格翻倍」。当时谷歌的发布文章说「大多数软件与知识工作用 Argon」。两天后，谷歌在它下面又加了一格：**「每天用的模型」**。本文用三种算法读这一格的价格 — 公司定的 token 单价、独立机构测的任务单价、以及这个价格底下的芯片容量。按事实、解读、换作我们分开写。

## 1. 谷歌 — Gemini 4 Hydrogen，「Carbon 和 Argon 深度思考，Hydrogen 快速干完每天的活儿」（事实）

谷歌于 11 月 12 日（周四）发布 **Gemini 4 Hydrogen**（公司发布，作者是谷歌 DeepMind 的科雷·卡武克丘奥卢）。定位只有一句话 — **「Carbon 和 Argon 负责深度思考。Hydrogen 把每天的活儿快速干完。」** 以编程为例，架构判断交给 Carbon 和 Argon，写代码、跑测试、确认改动交给 Hydrogen；在 Antigravity 里，**Orchestrator** 在同一个会话中在 Carbon 和 Hydrogen 之间切换。参数量未披露。思考档位为 low、medium、high（默认）加上新增的 **xhigh**，共四档；上下文为输入 100 万 token，输出也可达 100 万 token。

价格为**每百万 token 输入 1.50 美元、输出 7.50 美元**，在整个 100 万 token 上下文内统一价。落地范围一次就很广：Gemini API 和 Google AI Studio（所有层级）、Android Studio（付费）、Antigravity（Google AI Pro、Ultra 订阅者）、Gemini for business、Gemini 应用的模型选择 — 而且**免费用户通过自动模型选择获得**，**谷歌搜索面向全球所有用户上线**。Google Sheets 中的 Gemini 先向 Pro、Ultra 订阅者开放。

公司发布的数字如下。在默认（high）设置下完成任务比 Gemini 3.8 Flash **快 2.5 倍**，Terminal-Bench 4.1 为 **57%**（3.8 Flash 18.2%），HLE-Diamond 58.8%，Artificial Analysis 智能指数 **51（Argon 50），xhigh 下 54**。Antigravity 的 Orchestrator（Carbon+Hydrogen）据称在 Terminal-Bench 4.0 上以**少 24% 配额、快 19%** 达到接近 Carbon 单独运行的成功率。早期合作伙伴测试中复杂图、SQL 和数据任务快 2 到 2.8 倍、token 少 12% 到 23%；编造的断言不到 3.8 Flash 的五分之一；代理任务中越权行为最多减少 81%，任务被阻时绕过权限边界的可能性减半；对间接提示注入的抵抗力高 2.3 倍 — 这些全是公司发布的。模型卡在文中有链接，我们没有打开。

公司的表格里也有**落败的格子**。在 The Decoder 转载的表格中，Argon 领先 Hydrogen 的项目是 Chartography（71.6% 对 66.6%），Carbon 领先的项目是 Agents' Last Exam v1.1（77.4% 对 71.6%）和 OSWorld-2.1（81.5% 对 77.6%）。Digital Trends 写道，同一张表中 Hydrogen 在科学与数学、电脑操作、Terminal-Bench 4.1 上落后于竞争模型但差距很小；VentureBeat 转述谷歌表格的 Terminal-Bench 4.1 一格里 Claude Sonnet 5.5 为 63.9%（仅 VentureBeat 一处）。Argon 只有 medium、high 两档思考，所以公司所说的「比 Argon 高 1 分」比较的是 Hydrogen 的默认档对 Argon 的默认档。

## 2. 价格表 — 一个月内变了什么，以及独立机构测的「每任务」价格（事实）

我们把 VentureBeat 整理的价格表与我们此前的文章对齐（均为每百万 token 输入/输出，标准层级）。**Hydrogen 1.50/7.50。** Gemini 3.8 Flash **12 月 31 日前为 0.75/3.75，2027 年 1 月 1 日起 1.50/7.50** — 也就是说 Hydrogen 的价格既是「Flash 导入价的两倍」，也是「两个月后的 Flash 价格」。Gemini 4 Argon 从导入价 2/10 转为 4/20，Gemini 4 Carbon 如 NO.45 所写，**11 月 30 日前 2/10，之后 4/20**。Claude Fable 5.2 如 NO.44 所写为 8/40。谷歌的价格页在我们这边打开是只到 Gemini 3.5 Flash 的旧版，因此 Flash 的 2027 年涨价与 Argon 的转换**仅通过 VentureBeat 一处的整理**确认（有多个开发者博客写了同样的日期，但我们不把它们算作可信媒体）。Hydrogen 的缓存输入 0.075 美元、批处理和 flex 半价也只见于同一篇文章。

我们于 11 月 13 日直接打开了独立评测机构 **Artificial Analysis** 的 Hydrogen（high）模型页。在智能指数 v5.0.1 中为 **51（78 个模型中第 21 位）**、**每任务 1.87 美元**、混合单价 1.10 美元（按缓存 7 : 输入 2 : 输出 1 计），缓存折扣 95%，跑一次指数需输出 token 1.1 亿（同级中位数 7,280 万）。速度和幻觉数值仍是空白。打开同一机构的排行榜页，**Claude Fable 5.2（max）65、Gemini 4 Carbon（high）60、Claude Opus 5.5（max）59、GPT-6 Astra（max）57、GPT-6.1 Sol（max）55、Claude Sonnet 5.5（max）55**，Argon（high）为 50。我们打开的排行榜页上还没有 Hydrogen；xhigh 54、medium 41、low 27 以及各档每任务成本（3.16、0.80、0.29 美元）、Terminal-Bench 4.0 54%（Sonnet 5.5 max 64%）是 VentureBeat、The Decoder、OfficeChai 三家媒体转载的相同数字。其中 **3.8 Flash（high）指数 31、每任务 7.77 美元**这一数字只见于 VentureBeat 一处。

## 3. Epoch AI — 「推理性能指数」，一块芯片能同时接多少请求（事实）

Epoch AI 于 11 月 9 日发布**推理性能指数（Inference Performance Index，IPI）** v1（作者 Jason Li，数据 11 月 6 日更新）。它度量的不是 FLOP/s，而是**「一块芯片在 50 到 400 token/秒的要求输出速度范围内能同时服务的请求数」**，以一块英伟达 GB300 为 1 的相对值。建模条件针对代理工作 — 已缓存上下文 262,144 token、预填 1,024 token、每个输出 token 约 1.51 个新输入 token、推测解码采纳 3 个 token。取 Kimi K3、GLM-5.2、Qwen3-Coder-480B 和 MAI-Base-2 代理模型四者的平均。

结果如下。**GB300 的推理容量约为 H100 的 25 倍**，而按 8 位 FLOP/s 只有 2.5 倍，只看 FLOP/s 会把差距低估约十倍。同样的芯片，把 72 块放进一个高带宽域的 GB300 NVL72 约是 8 块一域的 B300 HGX（0.54）的 1.9 倍。H200 HGX 0.12，MI355X 约 0.55，VR200（Vera Rubin）2.18。还有一个背景数字 — **OpenRouter 上代理用 API 密钥消耗的 token 约是人类密钥的 7 倍**（9 月底）。局限也写在文中：这是用英伟达模拟器（AISimulate）得出的「理论极限速度」投影而非实测；受软件成熟度影响；未验证精度（FP8、FP4）是否保持模型质量；若改变平均方式（算术平均），旧芯片的分数会大幅下降。与实测（SemiAnalysis InferenceX）相比，在建模值 50% 的假设下平均差约 12%。作者曾在英伟达做 LLM 服务，本文未写资金来源（我们在 NO.45 中记过 ECI 页面有谷歌 DeepMind 支持的句子 — 那是另一篇文章）。

## 简短 — 谷歌 DeepMind 的 AlphaProof Code，四周内对 Signal 协议代码完成形式化验证（事实）

谷歌 DeepMind 于 11 月 10 日发布 **AlphaProof Code**（公司发布）。结构是：人类专家把 Signal 通讯协议的安全目标转为形式化规范并审核，然后 AI 代理用 Lean 语言写出证明并自行审计。公司写的结果是 — 核心密码代码的形式化验证在**四周**内完成（称类似工作曾让专家团队花费数年），代理交给人工审核的部分约占代码的 **1%**，故意放回两个已修复的 bug 后，两者都得出了「此版本不安全」的机器验证证明。证明的行数正文写「超过 600 万行」，页面元数据写「超过 300 万行」，两者不一致。成果已开源并附技术论文链接，但它不是产品，没有发布时间表，文中写「扩展需要进一步研究」。以上是公司的发布，我们没有打开论文。

## 把三件事放在一起读（解读）

第一，**模型选择表「默认格」变动的速度从两个月缩短到两天。** NO.45 中谷歌的文章说「大多数用 Argon」，这次说「每天用 Hydrogen」。两句话并不矛盾 — 公司把角色分成三个（Carbon：难题，Argon：大多数工作，Hydrogen：日常执行），并把像 Orchestrator 那样**在同一个任务内切换模型**铺成了基础（解读）。我们在 NO.17 写过「什么任务用什么 AI」，现在公司先在自己的模型线里把那张表分好了。不是照抄他们的表，而是要由我们来测自己的任务落在哪一格。

第二，**token 单价和任务单价是两个不同的数字。** Hydrogen 的 token 价格是 Flash 的两倍，但 Artificial Analysis 测得的每任务成本是 Hydrogen 1.87 美元对 Flash 7.77 美元（Flash 的数字仅 VentureBeat 一处）。便宜的模型若用更多 token，任务反而更贵。反过来，同一模型的 xhigh 输出 token 几乎翻倍，每任务成本也几乎翻倍（3.16 美元）。我们在 NO.21 写过「比数字之前先看算法」，价格表的算法是**「单价 × 那个任务实际用掉的 token 数」**（解读）。而且 2027 年 1 月 1 日 Flash 涨价、12 月 1 日 Carbon 涨价这类**价格变动的日期**也是表的一部分。

第三，**价格底下是芯片，它的算法同样不是 FLOP/s。** Epoch 的指数用「能同时接多少」来量，在这个标准下代际差距大十倍。与代理密钥消耗 7 倍 token 的数字一起读，意味着模型价格下降的部分原因可能不在模型而在服务端（解读 — Epoch 的值是建模值，与实际降价的关联 Epoch 和我们都没有测过）。小团队不会去选芯片，但作为**「能否以『价格还会再降』为前提来编表」**的依据，值得一读。

## 换作我们 — 运营应用、电商和 AI 渠道的团队本周要做的三件事（实践）

1. **把 Hydrogen 加入 NO.45 的 Carbon 三项测试，跑四个模型。** 用 Argon（high）、Carbon（high）、Opus 5.5（high）、Hydrogen（high）**同档对同档**地跑我们 NO.17 的测试（成分表判定、应用文案、Lia 脚本初稿），在结果旁写两行「公司发布 / 我们确认的」。这次多加一列 — **那个任务实际用掉的输入、输出 token 数。** 像 SafeList 的成分判定这种短而重复的任务是否进「每天用的模型」一格、像 Lia 脚本这种长任务进哪一格，用我们自己的数字来定。
2. **给单价表加一列「每任务成本」。** 在各模型 token 单价旁写上我们三个任务的「单价 × 实际 token 数」，把价格变动日期（Carbon 12 月 1 日、Flash 2027 年 1 月 1 日）放在表头。像 NO.41 记下 Lia 15 秒视频单价（Gemini Omni）一样，视频也放进同一列。这是选「便宜的任务」而不是「便宜的模型」的表。
3. **列一份可以夜里跑的活儿清单。** 缓存折扣 95%（Artificial Analysis 页面）和批处理半价（VentureBeat 转述 — 待谷歌价格页确认）只适用于不必「马上」的工作。写下人可以早上再检查的活儿 — 商品描述批量检查、周报初稿、翻译初稿 — 只把这些放到批处理和缓存里跑。这里同样，「不可逆的步骤」（NO.45）不在清单之内。

## 这次没有选的

Anthropic 新闻页 11 月 12 日的条目只有日期没有标题，Manufacturing Dive 当天报道了「Claude for Manufacturing」（含 17 项技能的插件）发布 — 这是撰写本文的 AI 的制造商的产品，只记标题。谷歌 DeepMind 的 Gemini Robotics 2.5（11 月 10 日，200 多项任务、梅赛德斯配套 96%）和 AlphaGenome 2 与我们的工作较远，只留标题。Mistral 于 11 月 5 日推出的 Studio（托管代理、工作流、应用；云、VPC 和本地部署）没有价格且数字全是公司发布，留作「小团队的代理运营层」后续候选。Box CEO 的「准确率 74% → 79%」是 X 帖子转述，没有使用。BigGo 的「谷歌让 Flash 这个名字退役」是谷歌文章里没有的说法，没有使用；谷歌的模型文档在 11 月 13 日仍只有 Argon，没有 Carbon 和 Hydrogen。Gemini 4 Hydrogen 的模型卡我们没有打开。

## 这条消息中我们未能确认的

- 谷歌的价格页在我们这边打开是旧版，所以 Gemini 3.8 Flash 2027 年 1 月 1 日的涨价（0.75/3.75 → 1.50/7.50）、Argon 导入价结束、Hydrogen 缓存输入 0.075 美元和批处理半价都只是 VentureBeat 一处的整理。写了同样日期的开发者博客不算可信媒体。
- 我们在 Artificial Analysis 页面直接看到的是 Hydrogen（high）51、1.87 美元、1.10 美元以及排行榜上六个模型的分数。xhigh 54、medium 41、low 27、各档每任务成本、Terminal-Bench 4.0 54% 是三家媒体转载的相同数字，3.8 Flash 的指数 31、每任务 7.77 美元只见于 VentureBeat 一处。
- 公司表格中的 Claude Sonnet 5.5 63.9%（Terminal-Bench 4.1）只有 VentureBeat 一处转述，我们在谷歌发布文章中直接确认的是 Hydrogen 57%、Flash 18.2%。合作伙伴测试（2 到 2.8 倍）和安全数值全是公司发布，没有独立确认。
- Epoch 的 IPI 是模拟器得出的建模值，不是实测。「代理密钥 token 7 倍」是 Epoch 对 OpenRouter 数据的解读，我们没有打开原始数据。
- AlphaProof Code 的「600 万行」与「300 万行」之差是文章内部的不一致，技术论文我们没有打开。

## 一起读的文章

我们直接打开了性质不同的来源确认。分为公司发布、研究与评测机构、媒体报道、维基、我们此前的文章。

公司发布：

- [Introducing Gemini 4 Hydrogen for Agentic Workflows（谷歌，11 月 12 日）](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) — 英文，定位、价格、开放范围、四档思考、基准与安全数值（公司发布）
- [Gemini 4 Hydrogen: everyday coding and agentic workflows for developers（谷歌，11 月 12 日）](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/) — 英文，开发者路径、Orchestrator（未提价格和 Flash）
- [Introducing AlphaProof Code（谷歌 DeepMind，11 月 10 日）](https://deepmind.google/blog/introducing-alphaproof-code/) — 英文，Signal 协议形式化验证、四周、约 1%、放回的两个 bug（公司发布）

研究与评测机构：

- [Gemini 4 Hydrogen（high）— Artificial Analysis 模型页](https://artificialanalysis.ai/models/gemini-4-hydrogen-high) — 英文，智能指数 51（v5.0.1）、每任务 1.87 美元、混合单价 1.10 美元、缓存折扣 95%
- [Artificial Analysis 模型排行榜](https://artificialanalysis.ai/leaderboards/models) — 英文，Fable 5.2 65、Carbon 60、Opus 5.5 59、Astra 57、Sol 55、Sonnet 5.5 55、Argon 50（我们打开时尚无 Hydrogen）
- [Inference Performance Index（Epoch AI，11 月 9 日）](https://epoch.ai/publications/inference-performance-index) — 英文，指数定义、GB300 25 倍、VR200 2.18、代理密钥 7 倍、局限与验证

媒体报道：

- [Google launches Gemini 4 Hydrogen — a faster, smarter, pricier Flash successor（VentureBeat，11 月 12 日）](https://venturebeat.com/technology/google-launches-gemini-4-hydrogen-a-faster-smarter-pricier-flash-successor) — 英文，价格表（Flash 2027 年涨价、Argon、Carbon）、AA 各档每任务成本、Flash 7.77 美元、Sonnet 5.5 63.9%（一处）
- [Google's Gemini 4 Hydrogen outscores the bigger Argon just four weeks after its launch（The Decoder，11 月 12 日）](https://the-decoder.com/googles-gemini-4-hydrogen-outscores-the-bigger-argon-just-four-weeks-after-its-launch/) — 英文，公司表格中 Hydrogen/Argon/Carbon 的比较（含落败格）、AA Terminal-Bench 54%、xhigh token 翻倍的说明
- [Gemini 4 Hydrogen Places Ahead Of Gemini 4 Argon, Muse Wonder And GPT 6.1 Terra On Artificial Analysis Intelligence Index（OfficeChai，11 月 12 日）](https://officechai.com/ai/gemini-4-hydrogen-artificial-analysis-intelligence-index/) — 英文，AA 排名整理、各档分数与成本
- [Google launches Gemini 4 Hydrogen for faster coding and agentic tasks（Interesting Engineering，11 月 12 日）](https://interestingengineering.com/ai-robotics/google-gemini-4-hydrogen-coding-benchmark) — 英文，公司数值整理、Orchestrator 先向 Ultra 订阅者开放
- [Google's next-gen Gemini 4 Hydrogen AI model is here, touting faster intelligence for all（Digital Trends，11 月 12 日）](https://www.digitaltrends.com/cool-tech/googles-next-gen-gemini-4-hydrogen-ai-model-is-here-touting-faster-intelligence-for-all/) — 英文，免费用户自动选择、搜索全量、公司表格中落后的项目
- [Anthropic launches 'Claude for Manufacturing'（Manufacturing Dive，11 月 12 日）](https://www.manufacturingdive.com/news/anthropic-launches-claude-for-manufacturing/874303/) — 英文，Anthropic 11 月 12 日的发布（仅记标题）

维基：

- [Gemini (language model)（Wikipedia）](https://en.wikipedia.org/wiki/Gemini_%28language_model%29) — 英文，Flash 系列年表（3.8 Flash 于 9 月 2 日发布，引用谷歌文档；尚无 Gemini 4 一代的条目）

我们此前的文章：

- [拦住客人的代理，放商家进来，模型向所有人开放（AP News NO.45）](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [同一个模型有两扇门（AP News NO.44）](https://www.apholdings.kr/ko/news/fable-5-2-two-doors-and-sandbagging-logs/)
- [每周 AI 资讯 — 变便宜的门（AP News NO.41）](https://www.apholdings.kr/ko/news/weekly-2026-11-07/)
- [记分牌上有了概率（AP News NO.40）](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [GitHub 十个拉取请求中有四个由代理发起 — 新记分牌的第一名还不是谁都能调用（AP News NO.33）](https://www.apholdings.kr/ko/news/agent-prs-40-percent-and-a-new-number-one/)
- [比数字之前先看算法（AP News NO.21）](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [什么任务用什么 AI（AP News NO.17）](https://www.apholdings.kr/ko/news/which-ai-for-which-job/)
