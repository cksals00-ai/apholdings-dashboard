---
no: 57
slug: approve-button-and-the-shape-of-permission
date: 2026-11-25
category: 洞察
tags: 智能体 · 审批策略 · Claude Ship · 谷歌搜索 · Hugging Face · harness
title: 审批按钮交到了智能体手里 — Anthropic 让“谁必须审批”写进仓库里的一个文件，同时写道“先用观察模式，从一个仓库、一个月度上限开始”；谷歌向搜索 AI 打开了钱包，但只限“只读”；Hugging Face 不动模型，用贴合 harness 的适配器把每个任务的 token 减少了近一半 — 权限的三种形状
summary: 11月20日至23日的三则消息 — ①Anthropic Claude Ship（代码审查、PR Steward、审批智能体；审批策略写在 .claude/approvals.yml，从观察模式开始，文档中有“可能在无人查看的情况下被合并”的警告）②谷歌搜索 AI Mode 的 Personal Intelligence 扩展到 Wallet（只读）、Drive、Gemini 应用 ③Hugging Face“harness 适配器”（模型固定，按 harness 各训练一个 LoRA，作者自评 token 减少 44~60%）。我们以“把权限写在哪里、写成什么形状”为线索，分事实、解读、换作我们三部分来写。
---

本文由 AI（Claude）协助撰写，并经编辑审核。利益关系先写、写长 — **本文第 1 条是开发了撰写本文的 AI 的 Anthropic 自己的产品发布（Claude Ship）。** 我们公司是 Anthropic 和 OpenAI 两家公司的付费客户，也在测试中使用谷歌、Meta 的模型，但从未用过 Claude Ship，本文也不是产品介绍或推荐。因此在第 1 条中，我们原样转述公司写下的条件、警告和计费语句，不添加一句“好”“更好”之类的评价，也不与其他公司的类似功能做比较。公司公布的数据标为“公司公布的数据”，只有一个来源的内容一并注明其出处。第 3 条的数据是 Hugging Face 作者的自我评估，没有第三方验证。本文不是对特定企业的投资意见。

我们在 NO.50 写了在智能体到来之前先写下“可以做的事”的三份文件，在 NO.54 写了“智能体名册与事故日志”，在 NO.56 写了“规则写在哪里才会被遵守”。本周的三则消息触及的是下一格 — **把权限写在哪里、写成什么形状。** Anthropic 让“谁必须审批”写进仓库里的一个文件，并写道“先只观察”；谷歌向搜索 AI 打开了钱包，但把形状定为“只读”；Hugging Face 推出的不是模型，而是贴合模型与工具之间那一层（harness）的适配器。我们把三份公司发布（Anthropic 的文章与文档、谷歌的文章、Hugging Face 的文章）、一份平台文档（GitHub）、两家媒体（TechCrunch、The Hacker News）、一则公告（OpenRouter）分事实、解读、换作我们三部分来写。

## 1. Anthropic Claude Ship — 审批策略写在 `.claude/approvals.yml`，先用观察模式，以及“可能在无人查看的情况下被合并”的警告（事实，公司发布、官方文档、媒体）

我们直接阅读了 Anthropic 的发布文章“Introducing Claude Ship”（11月23日，claude.com）和开发者文档（code.claude.com）。新闻室（anthropic.com/news）没有这篇文章，它发布在产品网站一侧。Claude Ship 是把一个 GitHub 拉取请求（PR）从**审查 → 修改 → 审批判定**一路推进的一组智能体，由三个部分组成（名称按公司所写原样保留）。

- **Code Review** — 已正式提供（GA）。从多个视角阅读 PR、收集发现项，经反向验证后分类，再以评论形式写到 PR 上。每个仓库从 Quick、Standard、Deep 三档中选一档。
- **PR Steward** — 测试版。接收失败的 CI 检查、合并冲突、人类与审查工具留下的审查意见，然后提交修复提交。每次推送时都会以评论写明“改了什么、如何回滚”，开发者可以用 `@claude` 下达指示，或用 `@claude stop` 让它退出。公司写道，这个智能体“设计上不做审批与合并”。
- **Claude Approvals** — 测试版。应用团队写在仓库里的**审批策略文件**。文档中写明的路径是 `.claude/approvals.yml`，该文件进入默认分支后即启用。策略中按路径写明“需要几位人类审批”和“Claude 可以给出审批性审查的地方”，并可挂上 Code Review 的发现项或团队**用自然语言写的分类器**作为信号。发布文章把它称为“更聪明的 CODEOWNERS 文件”。公司建议的顺序是 — 先以**观察模式（observe-only）**开启、只观察其判定，建立信任后再把它作为“必须通过此检查”加入 GitHub 分支保护规则。

开发者一侧新增了 Claude Code 的 `/ship` 命令 — 推送变更、打开 PR、审查、处理反馈与失败检查，打包成一套。文档写道，什么会被合并由该开发者的权限和仓库的分支规则决定。管理员一侧，文档要求在组织设置的 Claude Ship 页面（需要 Owner 权限）**一次开一个仓库、一次开一个智能体**，顺序也写明了 — Code Review → PR Steward（起初用“手动（@claude steward）”触发，**因为在设定支出上限之前 PR Steward 没有上限**）→ Claude Approvals（由策略文件开启，从观察模式开始，**观察模式也计费**）。用发布文章的话说是“从一个仓库开始，设定月度支出上限，策略在建立信任之前保持观察模式”。

提供范围与计费（公司所写）。Claude Team、Enterprise 套餐，GitHub 仓库（GitLab 在文档中只以“单独的 CI 集成”出现）。使用数据零保留（ZDR）、HIPAA 配置、客户管理加密密钥的组织不能使用。费用按 token 用量从组织的使用额度中扣除，与套餐包含部分分开。Claude Approvals 没有基础费用，但分类器的运行按 token 计费；如果策略要求 Claude 的审查，即使在观察模式下 Code Review 也会运行并计费。关闭顺序也在文档里 — 按 Approvals → PR Steward → Code Review 的顺序，因为策略可能调用审查并产生费用。即使关闭使用额度，已开启的智能体仍会继续运行并计费，所以文档写道“要停止收费，就关掉智能体”。

警告也在文档里。一句是**如果把 GitHub 的自动合并（auto-merge）或合并队列与“不要求人类审批的策略”一起使用，变更可能在无人经手的情况下被合并**，另一句是发布文章图片说明中的“Claude Ship 使用 AI，因此可能漏掉 bug、安全漏洞及其他问题”。策略含糊或变更超出策略范围时会怎样，这两个页面没有写（下级文档未查阅 — 见下文“未能确认的事”）。

公司公布的数据只有自家案例 — “在 Claude Code 团队，我们的大部分代码由 Claude 编写”，同一团队的合并 PR 在 6 月到 9 月之间“增长 2 倍以上”，被回滚的 PR 比例“减少 40% 以上”。两条客户引用（TELUS、Carvana）是公司挑选的推荐语。TechCrunch（莎拉·佩雷斯，11月23日）链接了发布文章和文档并转述了相同内容，没有新数据。

作为比较基准，我们打开了 GitHub 文档“About code owners”。CODEOWNERS 是放在仓库的 `.github/`、根目录、`docs/` 三处之一的文件，内容全部是一行一条的**文件路径模式 → 负责人（@user、@org/team）**。PR 触及该路径时会自动向负责人请求审查，开启分支保护的“Require review from Code Owners”后，负责人中**一人**的批准即可满足要求。路径以外的条件（变更内容、大小、时间）在语法中不存在。也就是说，到目前为止能写进仓库的“审批规则”只到“哪个路径由谁”为止。

## 2. 谷歌搜索 AI Mode 的 Personal Intelligence — 钱包“只读”，Drive、Gemini 应用数周内接入（事实，公司发布、媒体）

我们直接阅读了谷歌搜索产品副总裁罗比·斯坦因（Robby Stein）的文章“A more tailored Google Search that's uniquely yours”（11月23日）。搜索 AI Mode 的 Personal Intelligence（用用户允许连接的谷歌应用中的信息来调整回答的功能，NO.55）此前已连接 Gmail、日历、相册，这次新增 **Google Wallet“从今天起”，Google Drive 与 Gemini 应用“数周内”**。全部为选择加入（opt-in），可在“搜索个性化 → 已连接的应用”中逐个应用开关，也可以整体关闭个性化。

钱包连接的形状，是本文选中这则消息的原因。文章写道：**“连接钱包后，AI Mode 只能读取账户信息，不能转移、管理或投资资金”**。列举的用途是查看支出流向和“财务里程碑”、找出日常支出可削减之处、用好已连接卡片的权益（返现类别、旅行特权、积分）。Drive 连接的示例是读取文档、表格、PDF 来生成“报税准备计划”之类的回答，与 Gemini 应用之间则可以互相传递上下文。“不久后”可以通过回答下方的“Personalization”图标查看用了哪些上下文，错误的上下文用一句话纠正（“我现在不吃素了”）。文章里没有的 — 国家、套餐条件，数据，以及**购物、购买、支付一处都没有提及**（“购物”只出现在网站菜单里）。是否包含通行证、会员卡也没有写。TechCrunch（艾莎·马利克，11月23日）链接了官方文章，并以相同含义转述了“只读”。9to5Google 11月13日的报道（Gemini 应用一侧的 Wallet 连接）写了“仅限美国”，但搜索一侧的文章没有地区信息，因此本文不写地区。

我们在 NO.55 写过谷歌搜索的 Connected Apps（买菜 → 支付）和 Meta Muse 的“支付方式对智能体不可见”。本文写的是旁边那一格 — 同一家公司的搜索 AI **只以“读取”打开钱包**的选择。“直到支付”和“只读”在同一家公司内，以不同形状附在不同产品上。

## 3. Hugging Face“harness 适配器” — 模型不动，每个 harness 一个贴合的 LoRA，作者自评 token 减少 44~60%（事实，研究博客）

我们直接阅读了 Hugging Face 博客“Introducing harness adapters”（11月20日，Hugging Face 所属作者 10 人）。想法很简单 — 智能体的性能不只取决于模型，还取决于包裹模型的 **harness**（工具调用、上下文管理、提示词 — pi、OpenCode、Hermes Agent 这类编码智能体框架），所以固定模型权重，**为每个 harness 在该 harness 内部用强化学习训练一个小适配器（LoRA）**。基础模型只有 Qwen3.8-27B 一个，harness 是 pi 1.5.2、OpenCode 2.2.7、Hermes Agent v0.22.6 三个，适配器是每个 harness 一个共三个，外加把三者合并的一个“超级适配器”。训练在由验证器评分的编码任务上（从公开数据集的 871 个中挑出“偶尔能解”的 171 个、混合而成的 1,050 个）以 GRPO 方式进行，关闭了推理（thinking）模式。文中写道每个适配器用了两张 B200 GPU。

结果（全部为作者自我评估，pass@1 单次尝试，关闭 thinking）。在 pi harness 上，Terminal-Bench 2.1 为 **40.0% → 56.5%**（文章开头写的是 39% → 55%，**每个任务的 token 2.9K → 1.5K**），SWE-bench Pro 的 51 道难题为 **40.0% → 64.0%**（正文其他地方写的是 39.2% → 64.7% — 文内两组数字不一致，作者没有解释）。在 Hermes 上 Terminal-Bench 44.7% → 58.8%，在 OpenCode 上 47.6% → 52.4%。合并三者的超级适配器在六组配对上平均 **39.5% → 49.0%**（新解出 71 个，丢失 34 个），在两者都解出的任务上**工具调用减少 53~73%、token 减少 44~60%**。作者自己写下的局限 — 各 harness 默认设置不同，harness 之间的分数不能比较；超级适配器的权重是在 Terminal-Bench 上挑选的，所以该分数“略为乐观”；开启 thinking 的条件几乎没有测试。在训练中没有的任务（AutomationBench 300 个）上为 23.0% → 27.0%（pi）的水平，作者写的是“**在噪声范围内**”（这部分是按文章后半部分的摘要读的）。没有主张美元成本的节省，只统计了 token 与工具调用次数。适配器、任务、轨迹已在 Hugging Face 公开，许可证标注在正文中没有找到，也没有第三方验证。

同一博客的“How to build and maintain an agentic evaluation”（11月23日，阿维吉特·戈什、本·伯滕肖、艾琳·索莱曼）给出了读这些数字的方法 — 在运行模型之前**先验证任务**（参考答案能通过，“什么都不做的智能体”和“抄近路”会失败），**给保存下来的产出物评分**而不是看智能体的“我做完了”，**固定** harness 版本、容器、模型提供方，把 pass@k 和 pass^k 并排放。文章举的数字（作者引用） — 换了 harness 后同一模型的 Terminal-Bench 准确率最多移动了 29.9 分，Terminal-Bench 2.1 在公开报告后修正了 89 个任务中的 28 个，OpenAI 对 SWE-bench Verified 的审计中，查看的 138 道题里 59.4% 存在实质性缺陷。这是 NO.52、56 的“评估者也要被评估”的实务版。

## 简短三则（事实，官方公告、媒体、公司发布）

- **OpenRouter 移除 3 家推理提供方、取消 125 个端点的“零保留”资格（11月22日）** — 我们读了 OpenRouter 的公告和 The Hacker News（斯瓦蒂·坎德尔瓦尔）。安全公司 Dragos 从 7 月到 11 月植入测试用提示词、追踪谁会取出查看，结果显示部分推理提供方泄露了数据或没有遵守“零保留”承诺。OpenRouter 移除了 3 家提供方，把 125 个端点从零保留（ZDR）资格中剔除，通知了可能受影响的客户，并写道**自家系统没有被入侵**。被移除的 3 家名字不在公告正文里（只有 Atlas Cloud、Novita、Phala、Together 各自公告的链接），恢复资格需要经过确认。我们在 NO.51 写过 Hugging Face 把自己的推理路由交给了 OpenRouter，这件事发生在那个路由器背后的提供方层。手法不写。
- **OpenAI、思科“Shirudo”（11月23日）** — 公司发布称，以开源（BSD 2-Clause）形式推出了一个运行时，在补丁就绪之前给在 Linux 上运行的程序套上临时“盾牌”。公司写道在受控测试中无需重启就拦住了攻击尝试，没有数据。这是上一篇里写为“仅列标题”的那则消息，因为是安全类文章，不写运作方式。
- **每个任务的成本，个人测量 1 例** — 西蒙·威利森（11月20日）用自己的工具跑同一提示词记下的数值是：Gemini 4 Hydrogen high 3.99 美分、19 秒，xhigh 23.61 美分、2 分 36 秒，Neon xhigh 39.83 美分，Carbon high 20.31 美分。因为是一个人的一条提示词，不放进比较表，只作为 NO.46“每个任务的成本按档位相差 6 倍”的例子。

## 把三件事放在一起读（解读）

第一，**“审批”变成了仓库里的一个文件，而且这个文件第一次装进了路径以外的条件。** 按 GitHub 文档，到目前为止能写进仓库的审批规则只有“这个路径归这个人”，一个人批准即可。Anthropic 文档的策略文件在此之上加了“几个人”和“在什么条件下智能体可以审批（自然语言分类器）”。这是好是坏，本文不做判断（见利益关系声明）。我们读到的是形状 — NO.56 写过“规则必须放在智能体实际会读的位置”，这次的形状是**把规则从人读的文档，搬进了合并路径必定经过的检查（check）**。而这家公司在同一份文档里写下“与自动合并一起使用时可能在无人查看的情况下被合并”，是这个形状的另一面 — 一旦变成检查，人就可能被略过。

第二，**权限的形状正在按“读/写”分开，而且同一家公司内部各产品也不一样。** 谷歌搜索 AI 的钱包是“只读”，同是谷歌的 Connected Apps 是“直到支付”（NO.55），Meta Muse 是“支付方式不可见、购买前确认”（NO.53）。三者都是公司发布稿里的一句话，三者也都是我们在店铺或应用里可以直接采用的选项。我们这边的教训是，不要把“权限”作为一整块给出去，而是把读和写分开写 — 像钱包那样“只读”也有用处的连接相当多（库存查询、订单状态确认、评论阅读）。

第三，**要改的地方可能不是模型。** 我们在 NO.48 写过“换模型要花几周”和“只有放在模型之外的东西能带走”。Hugging Face 的文章在它的对面 — 模型不动，用贴合模型与工具之间的一小块把 token 减少了近一半，这是作者评估。数字是一个模型、三个 harness、作者自评，在训练之外的任务上处于噪声范围，所以不能写“适配器就是答案”。能写的是问题 — 我们的智能体成本中，有百分之几是模型单价，有百分之几是 harness（不必要的工具调用、过长的上下文）。如果 NO.46 的每任务成本表里没有“工具调用次数”这一列，本周先加上这一列，就是从这则消息里可以免费拿走的东西。

## 换作我们 — 运营代码、店铺、应用的小团队本周要做的三件事（实战）

1. **先不分工具、用人话把审批策略写成一页。** 针对我们的官网仓库（新闻构建、上线脚本）和应用仓库各自，按路径写下“谁审批后才能合并”，并在路径旁加上**条件** — “只改了翻译文件的 PR，检查通过即可”，“支付、会员、发送代码需两人”，“脚本、配置需一人 + 必须有写明回滚方法的评论”。无论用什么工具，这一页都在先；能用 GitHub 的 CODEOWNERS 写的行（路径 → 人）现在就写。把“自动合并、合并队列不与‘没有人类审批的策略’一起开启”这一行放在最上面 — 这一行不是产品文档，而是我们的运营规则。即使有一天智能体要做审批判定，也要先在 NO.54 的名册里写上“审批智能体”一行以及月度上限、观察期之后。
2. **给智能体的每一个连接都分开写“读/写”。** 在 NO.55 的“门表”（商品信息、购物车、支付、会员信息）上再加一列 — “只读 / 可写”。Hangul Cups(韩文杯)订单状态、CourtMate 论坛、Lia 评论即使从“只读”开始，智能体也有很多事可做；“写”（发送、发布、退款）则与 NO.56 的上限栏一起附上。把谷歌文章的那句话换成我们的话是“这个连接只能读，不能转移或删除” — 这一行能否写进商店说明、个人信息告知，与宣传部门一起定下来。
3. **在每任务成本表里加入“工具调用次数”一列，并先验证三个评估任务。** 在 NO.46、52 的表（模型/档位/完成/token/每任务成本/时间）中加入工具调用次数，把同一模型、同一任务用两种 harness（我们的提示词、工具配置）各跑一遍，记下 token 和调用次数的差异 — 看看不换模型就能省下的份额有多少。在此之前，把 Hugging Face 评估文章的三项验证用在我们的三个任务上（成分表项目提取、电商咨询分类、Lia 脚本校对） — 参考答案能否通过，“什么都不做的智能体”是否会失败，抄近路是否被堵住。只要其中有一项通过了，就把该任务的过去分数清掉重新测量。Lia 脚本以学习“把审批按钮交给智能体的公司最先写下的是‘观察模式’”的语气来写，产品名和数据只以 reported 形式放入。

## 这次没有选的

OpenAI 的“GPT-6 蛋白质设计”、“用 Astra 探索系外行星”（11月24日）是科学案例，仅列标题。Anthropic 新闻室在 11月20日完成上市后没有新文章（投资领域，仅列标题），Epoch 的“Anthropic 算力支出年增 4 倍”（11月18日）也涉及投资与厂商，仅列标题。西蒙·威利森引用的“Claude 与黎曼猜想”主张（11月20日）未经验证且涉及厂商，与上一篇一样不写。GLM-5.4（Z.ai 首个循环 Transformer，11月23日，非开放权重、无数据）和 Inkling 2 Mini（Hugging Face、Thinking Machines，26B/激活 3B，能装进 32GB — 公司主张）作为 NO.51 的后续候选保留。The Hacker News 的 CERT-In 警报、Muse 网页演示（NebuSec，已修复）、医学影像软件零日漏洞（转述亚马逊发布）、Cursor 的 API 密钥被盗事件（日期未确认），因不写手法的原则以及单一来源、未查阅，仅列标题。“电信公司、Naver 屏蔽外部 AI 智能体的客服咨询”（ZDNet Korea 标题，promppy 摘要）可能是 NO.45、55“关门的一方”的韩国国内案例，将打开原文在下一期确认。亚马逊收购 Decart、Sierra、Supertake（TechCrunch）属于投资，仅列标题。谷歌 AI 博客的 RSS 是停在 5 月的订阅源，所以只直接打开了单篇文章。

## 这些消息中未能确认的事

- Claude Ship — 没有打开下级文档（approvals-policy、approvals-classifiers、pr-steward-security 等），所以不知道策略含糊或变更超出策略范围时是否会交给人、分类器的语法是什么样、观察模式的日志留在哪里。“2 倍以上”“减少 40% 以上”“大部分代码”是公司自家团队的数据，分母和期间的定义在发布文章中没有。发布文章写“管理员设定 Code Review、PR Steward 的支出上限”，文档写“PR Steward 在设定上限之前没有上限”，我们只按文档转述了默认值为“无”这一点。发布文章的“更聪明的 CODEOWNERS”是公司的表述，不是我们的评价。我们没有用过这个产品。
- 谷歌的文章里没有国家、套餐、数据。“仅限美国”来自 Gemini 应用一侧 9to5Google 11月13日的报道（单一来源），搜索一侧没有这句话。是否包含通行证、会员卡，以及“Personalization”图标的时间点（“不久后”），未能确认。
- Hugging Face 适配器文章的正文后半部分（训练外任务结果、部分局限）是按摘要读的。数字是作者自评、一个模型、三个 harness，文内同一指标有两处写了两种数字（40.0/39.2、64.0/64.7、47.6/46.4），作者没有解释。许可证在正文中没有找到。评估文章的“SWE-bench Pro 约 30% 缺陷”（OpenAI 估计）和“29 个基准饱和”是在摘要部分读到的，没有写进正文。
- OpenRouter — 被移除的 3 家与 Dragos 点名的 3 家是否相同，两篇文章都没有写。Dragos 的原文没有打开。
- Shirudo — 只读了公司发布，仓库和测试条件没有打开。
- 任何一家公司的测试我们都没有复现。“换作我们”的三行本周开始，结果写在下一篇。

## 一并阅读的文章

我们直接打开并确认了性质不同的来源。分为公司发布与官方文档、平台文档、研究博客、公告、媒体报道、个人博客、我们之前的文章来写。

**公司发布与官方文档**

- [Introducing Claude Ship（Anthropic，11月23日）](https://claude.com/resources/articles/introducing-claude-ship) — 英文，Code Review GA、PR Steward、Claude Approvals 测试版、观察模式、一个仓库、月度上限、Team/Enterprise、GitHub、自家团队数据（2 倍以上、40% 以上）
- [Claude Ship — 开发者文档（Anthropic）](https://code.claude.com/docs/en/claude-ship) — 英文，`.claude/approvals.yml`、按路径的审批人数、`claude/code_review` 触发器、观察模式计费、PR Steward 默认无上限、关闭顺序、自动合并警告
- [A more tailored Google Search that's uniquely yours（Google，罗比·斯坦因，11月23日）](https://blog.google/products-and-platforms/products/search/google-search-personal-intelligence-apps/) — 英文，Wallet 今日、Drive 与 Gemini 应用数周内、“只能读取，不能转移、管理或投资”、选择加入、Personalization 图标
- [OpenAI and Cisco introduce Shirudo（OpenAI，11月23日）](https://openai.com/index/introducing-shirudo/) — 英文，Linux 运行时“盾牌”、开源 BSD 2-Clause、无数据

**平台文档**

- [About code owners（GitHub Docs）](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) — 英文，路径模式 → 负责人、自动请求审查、“Require review from Code Owners”、一人批准即满足、无路径以外的条件

**研究博客**

- [Introducing harness adapters（Hugging Face，11月20日）](https://huggingface.co/blog/harness-adapters-at-scale) — 英文，Qwen3.8-27B 固定、pi/OpenCode/Hermes、GRPO、40.0→56.5%、2.9K→1.5K token、超级适配器 39.5→49.0%、token 减少 44~60%、训练外任务处于噪声范围
- [How to build and maintain an agentic evaluation（Hugging Face，11月23日）](https://huggingface.co/blog/agentic-evals) — 英文，三项任务验证、产出物评分、版本固定、pass@k/pass^k、harness 差异 29.9 分、TB 2.1 修正 28/89、SWE-bench Verified 59.4%

**公告**

- [Data Processing Incidents on Inference Providers（OpenRouter，11月22日）](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/) — 英文，移除 3 家提供方、125 个端点移出 ZDR、通知客户、自家未被入侵

**媒体报道**

- [Anthropic launches Claude Ship, letting AI agents review, fix, and approve code changes（TechCrunch，11月23日）](https://techcrunch.com/2026/11/23/anthropic-launches-claude-ship-letting-ai-agents-review-fix-and-approve-code-changes/) — 英文，链接官方文章、无新数据
- [Google Search's AI Mode can now tap into Drive and Wallet for more personalized responses（TechCrunch，11月23日）](https://techcrunch.com/2026/11/23/google-searchs-ai-mode-can-now-tap-into-drive-and-wallet-for-more-personalized-responses/) — 英文，只读、选择加入
- [OpenRouter Drops 3 Providers After Researchers Catch Months of Prompt Theft at AI Hosting Firms（The Hacker News，11月22日）](https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html) — 英文，Dragos 7~11 月追踪、3 家、125 个、名字未公开

**个人博客**

- [llm-gemini 0.38.1 — Hydrogen、Neon、Carbon 每任务成本测量（Simon Willison，11月20日）](https://simonwillison.net/2026/Nov/20/llm-gemini/) — 英文，个人测量 1 例、3.99/23.61/39.83/20.31 美分

**我们之前的文章**

- [“速度限制”第一次有了数字 — 规则写在哪里才会被遵守（AP News NO.56）](https://www.apholdings.kr/ko/news/perplexity-speed-limit-and-rules-written-then-broken/)
- [智能体来到了支付按钮前 — 店铺要定的是四种门中的一种（AP News NO.55）](https://www.apholdings.kr/ko/news/agent-doors-checkout-and-handback/)
- [智能体名册与事故日志，这两页先行（AP News NO.54）](https://www.apholdings.kr/ko/news/agent-roster-and-incident-log/)
- [每周 AI 消息 — 价格下调、写明局限，智能体进入桌面和购物车（AP News NO.53）](https://www.apholdings.kr/ko/news/weekly-2026-11-21/)
- [“中间格”Gemini 4 Neon — 一张分数表不够用的三个理由（AP News NO.52）](https://www.apholdings.kr/ko/news/neon-same-score-seventeen-points-apart/)
- [十个 token 里有七个流向开放权重模型（AP News NO.51）](https://www.apholdings.kr/ko/news/open-weights-take-seven-in-ten-tokens/)
- [在智能体到来之前先写下“可以做的事”的三份文件（AP News NO.50）](https://www.apholdings.kr/ko/news/allowed-list-before-the-agent-arrives/)
- [换模型要花几周 — 只有放在模型之外的东西能带走（AP News NO.48）](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [有了“每天用的模型”这一格 — 用每任务成本来读的方法（AP News NO.46）](https://www.apholdings.kr/ko/news/hydrogen-daily-driver-price-per-task/)
- [挡住顾客的智能体，迎进店铺，模型给所有人（AP News NO.45）](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [智能体是“不可信的内部人”（AP News NO.29）](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
