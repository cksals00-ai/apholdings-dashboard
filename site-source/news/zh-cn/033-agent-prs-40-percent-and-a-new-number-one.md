---
no: 33
slug: agent-prs-40-percent-and-a-new-number-one
date: 2026-10-30
category: 洞察
tags: GitHub Octoverse · 智能体 PR · 模型选择 · Gemini 4 Carbon · Artificial Analysis
title: GitHub 每十个拉取请求中有四个由智能体发起 — 只用一个模型的开发者变少了，而新榜单的第一名还没人能调用
summary: 10 月 28 日，GitHub 在年度报告《Octoverse 2026》中表示，「9 月有超过 40% 的拉取请求由智能体发起」。3 月时是 17%。同一份报告显示，自己挑选模型的 Copilot 用户中有 61% 在一个月内使用了两个以上的模型，没有任何一个模型超过请求总量的 25%。同一天，谷歌在发布 Argon 四周后推出了「最强模型」Gemini 4 Carbon，但这一次仍然是先给一部分网络防御者。Carbon 拿到第一的那张榜单在前一天被整体重做，无法与旧分数比较。我们把使用方的数字(GitHub)和制造方的数字(谷歌与评测机构)并排放在一起，写下小团队在挑选模型的方式上应该改写什么。
---
> 本文由 AI(Claude)协助撰写，并经编辑审核。制造 Claude 的 Anthropic 是本文中出现的谷歌、OpenAI 的竞争对手，Anthropic 的模型在本文讨论的排行榜上位列第二。GitHub 是微软旗下公司，我们公司是这些公司 AI 工具的付费客户。公司发布的数字标注为「公司发布」，独立评测机构的数字标注了所属榜单的版本。本文不构成买卖任何公司股票的建议。

我们在 NO.16 写过「哪个 AI 用得最多」，在 NO.17 写过「什么工作用什么 AI」。当时的答案是「不同调查数字不同，各公司公布了自己的用途」。本周，两组性质不同的数字在同一天出现。一组来自**使用方**：GitHub 统计一整年活动的年度报告，里面有 2.25 亿开发者实际上传了什么、选了哪些模型。另一组来自**制造方**：谷歌又推出了一款「最强模型」，并在独立评测机构的榜单上排名第一。把两组数字放在一起，看到的不是「哪个最好」，而是「人们实际怎么选」。

## 1. GitHub Octoverse 2026 — 40% 的拉取请求由智能体发起 (事实)

GitHub 于 10 月 28 日发布年度报告 Octoverse 2026(公司发布，统计区间为 2025 年 10 月 1 日至 2026 年 9 月 30 日)。以下是我们直接阅读官方文章得到的数字。

- **由智能体发起的拉取请求。**「截至 9 月，开发者有超过 40% 的拉取请求由智能体发起。3 月时是 17%。」9 月单月 1.1 亿件，约为 3 月的 6 倍。报告写明这个数字是**「下限」**，因为并非所有智能体使用都能被检测到。
- **这些 PR 的结果。**智能体发起的 PR 中修改多个文件的比例约 87%(没有智能体痕迹的 PR 为 79%)，两周内合并的比例从 2 月的 83% 升至 9 月的 90%。对照组维持在约 86%。
- **整体规模。**12 个月内推送 179 亿次、提交 343 亿次、合并 PR 13 亿件(每天约 350 万件)、Actions 任务 454 亿次。提交数从上一年的 129 亿增至 343 亿。报告说明今年统计窗口和口径有变，2024、2025 年的数字也重新计算过。在现场的开发者 Simon Willison 记录的舞台发布数字是「每月合并 PR 2.2 亿件，不到一年翻了三倍」。
- **语言。**按贡献者人数，TypeScript 第一，Python 第二，JavaScript 第三，Rust 一年内翻倍，增速最快。带有 AI 痕迹的已合并 PR 比例：TypeScript 约 44.1%，Python 41.1%，Rust 40.4%，Java 21.2%。
- **开发者。**超过 2.25 亿人。美国 3,830 万，印度 3,200 万，两国今年都增加了 1,000 万以上。

## 2. 同一份报告 — 只用一个模型的人变少了 (事实)

Octoverse 2026 首次收录了 GitHub Copilot 中用户**自己选择**的模型统计(公司发布)。排除了自动选择、员工使用和自带密钥的请求，只统计周活跃用户 1,000 人以上的模型，报告明确指出这些数字「描述的是观察到的使用，而不是模型质量」。

- **用两个以上。**9 月自己选择模型的用户中，**61% 使用了两个以上的模型**。四个月前是 50%。
- **种类增多。**付费用户使用的模型种类从 5 月的 29 个增至 9 月的 47 个，**没有任何一个模型超过请求总量的 25%。**报告没有公布按模型名称的占比。
- **用途分化。**用户选择的每 100 个请求中，通用模型 38 个，深度推理与规划 37 个，快速轻量模型 25 个。63% 的付费用户 9 月至少使用过一次自动模型选择。
- **Copilot 本身。**月活跃用户中 55% 使用智能体功能(一年前 35%)，云端智能体同比增长 230%。

同一周，OpenAI 一方也出现了「怎么选」的说法。在讨论 GPT-6.1 Terra 的 Hacker News 帖子里，OpenAI 员工 Ted Sanders 解释说，公司的模型名称**按规模排序(Luna < Terra < Sol < Astra)**，规模主要决定可靠性、每 token 成本和对冷门事实的记忆，而版本号(6.1)表示改进幅度——「还不是大到可以叫 7 的飞跃」。他还给出建议：只看质量选 Astra，稍微在意价格选 Sol，非常在意价格选 Terra 或 Luna。讨论的主流是抱怨：模型一个一个单独发布，很难判断哪个更好，又没有按任务的指引，只能各自评测。Simon Willison 转介了这条评论，我们直接打开原帖进行了确认。这是员工个人的评论，不是公司文件。

## 3. 谷歌 Gemini 4 Carbon — 又是「最强模型」，又是先给一部分人 (事实)

谷歌于 10 月 28 日发布了《Gemini 4 Carbon: our next frontier model》(署名 Google DeepMind 的 Koray Kavukcuoglu，公司发布)。距 Argon 上线 Gemini 应用两周。

- **它说自己是什么。**「在网络安全和长程任务(long horizon)上达到最高水平」，公司表示内部团队让它**连续数日**处理在大型代码库中定位并修复 bug 的多步任务。说明中称编码、智能体、科学、全栈 Web 和多模态都有提升。
- **谁先用。**本周是**一部分网络防御者**，接下来是 Fairwind 计划的可信伙伴(政府、关键基础设施、核心平台、防御研究学术机构，审核后获得访问)，同时参与美国政府的自愿预发布测试，对开发者、企业和消费者则是「尽快」。**没有日期、产品或套餐。**我们阅读时，Fairwind 计划页面只写了 Argon。9to5Google 和 Mashable 都把公开时间理解为「未定」。
- **价格。**公司博客写的价格与 Argon 相同：导入价(每百万输入 token 2 美元、输出 10 美元，缓存输入 95% 折扣)和之后的价格(4 美元、20 美元)。只是这是一张还调用不了的模型的价目表。
- **公司数字。**WebDev Arena +89 Elo 排第四(1,768)，漏洞发现 SEC-bench Pro 88.2%，利用 ExploitGym 54.8%，修补 CWE-bench 71.0%，Gray Swan 间接提示注入基准攻击成功率 0.0%(Argon 0.7%)，Terminal-Bench 4.0 上作弊成功 0.0%、尝试 0.4%，内部编码环境的高风险失准警报减少约 80%，无依据断言约减半。全部为公司发布，公司称网络安全基准是在关闭护栏的状态下测的。Mashable 读了公司的表格，称「17 项基准中 15 项第一，FrontierSWE 2 由 GPT-6 Astra 领先，OSWorld-2.1 由 Claude Opus 5.5 领先」。
- **独立榜单。**在 Artificial Analysis 智能指数 **v5.0** 上，Carbon(High)以 **59 分排第一**。我们直接打开的该机构模型页面显示：54 个模型中第一，每道任务成本 7.76 美元(53 个中第 47 位)，整个指数消耗输出 token 2 亿(中位数 7,000 万，冗长度 53 个中第 51 位)，首个 token 耗时 97.9 秒(中位数 3.37 秒)。在该机构自己的排行榜上(已直接核实)，第二名是 Claude Opus 5.5(Max)58 分；Argon 的 50 分来自 Mashable 的报道。模型页面写明可通过一家 API 提供商(谷歌)调用(我们此前看到的「无公开 API」标记，重新打开时已不存在)，但谷歌的文章没有给出公开发布时间。

重要的是榜单本身变了。Artificial Analysis 于 10 月 27 日将指数**改版为 v5.0**(直接确认了该机构的变更记录和方法论页面)。9 项评测被分到知识工作、编码、科学、通用四个领域，各占 25%，其中 5 项(AA-Briefcase、AutomationBench-AA、FrontierCode 2.0、CritPt v2、AA-Omniscience v1.1)是**不公开题目的私有评测**。GDPval 被移出指数。方法论页面写明不同版本的分数不能直接比较。Argon 在旧版本是 53，在 v5 是 50。同一个模型掉了 3 分，不是模型变差了，而是尺子变了。

## 怎样并排读这两组数字 (解读)

第一，**「40%」是「由智能体发起」，不是「由智能体写的」。**GitHub 统计的是被检测到的痕迹，而且说那还是下限。人从头看到尾的 PR 和智能体独自开的 PR 混在一个数字里。即便如此，我们关注的是合并比例。智能体发起的 PR 两周内合并率(90%)高于其余 PR(86%)，意味着审查者**开始接受它们**。走向不是拒绝率上升。不过这是 Copilot 深度嵌入的 GitHub 内部观察，使用其他工具的团队的数字不在其中。

第二，**对于「哪个模型最好」这个问题，用户的回答是「好几个」。**61% 用两个以上，47 种，没有超过 25% 的。NO.16 里我们写过「不同调查数字不同」，GitHub 的数字又给出了一个原因：人们不是挑一个模型，而是**按用途分栏**来挑(通用 38、推理 37、轻量 25)。而公司内部的人直接说「我们的模型名按规模排，按你对价格的敏感程度来选」，是公司在官方文件里很少说的话。我们不把这条评论当作「公司指引」，而是当作「选择的坐标轴是规模、价格、速度」的提示。

第三，**「新第一」要同时看三件事。**是不是尺子刚换就拿的第一(v5 前一天才发布)、差几分(领先第二名 1 分)、能不能调用(还不能)。再加上成本和冗长度：每道任务 7.76 美元，53 个中第 47 位；输出 token 约为中位数的 3 倍；首个 token 要等一分半以上。一个高 1 分的模型是否适合我们的工作，这些数字说得更多。我们在 NO.15 把 Argon 写成「更强，先给一部分人」，在 NO.22 问过「分数是谁打的」。Carbon 是那两篇文章的重复。不同的是，这次「先给」的对象不是付费订阅者，而是**网络防御者**。公司把这款模型的首个用途定为安全，所以我们认为公开时间也因此更保守(解读)。

第四，我们补充的解读。使用方的数字和制造方的数字互相解释。模型每两周就换一个「最强」，用户就不会绑定在一个模型上；用户用多个模型，自动选择(63% 使用)和路由就成了默认值。NO.4 写「模型每周变化时的工作准则」时还是假设，现在 GitHub 的数字支撑了这个假设。

## 如果是我们 — 改写模型选择文档里的三行 (实践)

我们团队在应用后端、电商对接和 Ria 视频脚本上混用三四个模型。用本周的数字修改 NO.17 的「按任务模型表」，是三行。

1. **也数我们自己的 PR。**给智能体(Claude Code、Codex 等)开的 PR 加标签，每月记录三个数字：「智能体发起 PR 比例、两周内合并率、回滚(revert)率」。GitHub 整体是 40%、90%。如果我们的数字更低，是工具问题或审查瓶颈；如果合并率高但回滚变多，是审查松了。GitHub 报告里没有的第三个数字(回滚)，正是我们额外要看的原因。
2. **分成三栏。**按 GitHub 用户实际划分的比例(38、37、25)，以通用、深度推理、轻量三栏重写任务表。「Ria 脚本初稿」是通用，「SafeList 成分判定规则审查」是深度推理，「100 条商品描述分类」是轻量。每栏写下首选和**备用模型**，新模型出来时只在**那一栏**试，不是全盘换。把任务对价格的敏感程度作为每栏的第二标准。这和 Sanders 说的坐标轴一样。
3. **新第一名要先过三行确认再试。**①是否在同一版本的榜单上比较(不把 v4 和 v5 的分数混在一起)②能否通过 API 调用(不能就在表上写「等待」，不测试)③每道任务成本、输出长度、首个 token 时间与现用模型差多少。填完三行，才在第 2 条的某一栏里试。不因 1 分之差换模型。

## 这次没选的

Artificial Analysis 变更记录里的「Mistral Large 4(10 月 29 日评测)」因找不到 Mistral 官方发布而没有涉及(AI Weekly 10 月 10 日的文章以 Hugging Face 模型页面为依据写「预计 10 月 31 日开放权重」，我们没有直接打开那个页面)。安全公司 GitGuardian 在解读 Octoverse 时附上的自家数字(暴露的密钥 2,865 万条、某款编码工具辅助的提交中含密钥的比例等)尚未交叉核实，没有使用。Mashable 文章中提到的 Google DeepMind 管理层变动只有一家媒体，没有使用。Hugging Face 的三篇新文章(NVIDIA 多语言转写模型、LiquidAI 的 LFM3、AI2 的「能否信任 LLM 判断研究想法是否新颖」)尚未阅读正文。Anthropic 10 月 27、28 日的发布(新药研发、AI for Science)利益关系较大，交叉核实后另行处理。

## 这条消息中我们未能确认的

- Octoverse 的所有数字都是 GitHub 发布的，没有独立验证。智能体比例公司自称是「下限」，模型统计只计 Copilot 内用户自选的请求。按模型名称的占比没有公布。
- Simon Willison 记下的「每月合并 PR 2.2 亿件」是舞台发布的转述，我们读到的官方文章只有 12 个月合计(13 亿件)。在 GitHub Universe 的回顾页面上我们也没有找到这个数字。
- Carbon 的安全基准和安全性数字是公司发布，独立评测机构的确认只有智能指数。「17 项中 15 项第一」是 Mashable 对公司表格的解读，我们没有直接确认整张表。Argon 在 v5 上的 50 分同样来自 Mashable。
- Artificial Analysis 模型页面写明 Carbon 可通过一家 API 提供商(谷歌)调用，但谷歌的文章没有公开发布时间，所以目前谁能调用我们无法确认。某家网关公司文章里 Carbon 的幻觉率、准确率数字在该机构页面上无法确认，没有使用。
- Carbon 的公开时间、产品和套餐不在公司文章里。Ted Sanders 的说明是员工个人评论，不是 OpenAI 官方文件。

## 一起读过的文章

我们直接打开并核实了性质不同的来源。按公司官方文件、独立评测机构、个人博客与社区、媒体报道、安全公司、我们此前的文章分列。

公司官方文件：

- [Octoverse: Commits, pushes, reach new highs in 2026 as developers build with agents (GitHub)](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/) — 英文，年度报告原文(智能体 PR、模型选择统计、方法论注释)
- [Gemini 4 Carbon: our next frontier model (Google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) — 英文，公司发布原文(公开顺序、价格、公司数字)
- [Fairwind Program (Google DeepMind)](https://deepmind.google/fairwind-program) — 英文，可信伙伴计划说明(我们阅读时只列了 Argon)

独立评测机构：

- [Intelligence Benchmarking Methodology (Artificial Analysis)](https://artificialanalysis.ai/methodology/intelligence-benchmarking) — 英文，指数 v5.0 构成、私有评测、版本间不可比较的说明
- [Gemini 4 Carbon (Artificial Analysis 模型页面)](https://artificialanalysis.ai/models/gemini-4-carbon) — 英文，指数 59、每道任务成本、输出 token、首个 token 时间
- [Models (Artificial Analysis 排行榜)](https://artificialanalysis.ai/models) — 英文，v5 排行榜(第一 Carbon 59，第二 Claude Opus 5.5 Max 58)

个人博客与社区：

- [Simon Willison's Weblog, 2026-10-28](https://simonwillison.net/2026/oct/28/) — 英文，GitHub Universe 现场记录与 OpenAI 模型命名说明的转介
- [GPT-6.1 Terra — Hacker News 讨论](https://news.ycombinator.com/item?id=50248124) — 英文，OpenAI 员工 Ted Sanders 关于模型命名与选择标准的评论(个人评论)

媒体报道：

- [Google announces Gemini 4 Carbon with 'significant' coding gains (9to5Google)](https://9to5google.com/2026/10/28/gemini-4-carbon-announcement/) — 英文，IT 媒体(交叉核实用)
- [Google announces Gemini 4 Carbon, its new frontier AI model (Mashable，Yahoo 转载)](https://tech.yahoo.com/ai/gemini/articles/google-announces-gemini-4-carbon-193050677.html) — 英文，对公司基准表格的解读、Argon 分数、公开范围

安全公司：

- [GitHub Octoverse 2026: AI Agents, Citizen Developers, and the New Security Reality (GitGuardian，Security Boulevard)](https://securityboulevard.com/2026/10/github-octoverse-2026-ai-agents-citizen-developers-and-the-new-security-reality/) — 英文，用于交叉核实 Octoverse 数字(其自家统计数字未在正文使用)

我们此前的文章：

- [什么工作用什么 AI — 各公司公布的用途与我们的测试方法 (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — 韩文，本文改写的按任务模型表
- [哪个 AI 用得最多 — 数字为何不一致 (AP News NO.16)](https://www.apholdings.kr/ko/news/who-uses-which-ai/) — 韩文，不同调查数字不同的原因
- [Meta 的首个前沿模型 Muse Wonder — 分数是谁打的 (AP News NO.22)](https://www.apholdings.kr/ko/news/meta-muse-wonder-whose-scorecard/) — 韩文，榜单的读法
- [本周 AI 消息 — 两家公司「更便宜」，谷歌「更强，先给一部分人」 (AP News NO.15)](https://www.apholdings.kr/ko/news/this-week-gpt61-sonnet55/) — 韩文，Argon 发布时的相同模式
