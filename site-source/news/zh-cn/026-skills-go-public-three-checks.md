---
no: 26
slug: skills-go-public-three-checks
date: 2026-10-23
category: 洞察
tags: Agent Skills · Anthropic · Linux基金会 · AAIF · API版本 · Railway · API密钥
title: 技能成了"公共规范"——Agent Skills捐给基金会、三年来首个API新版本、被盗的钥匙：我们检查的三件事
summary: 10月22日，Anthropic将Agent Skills标准移交给Linux基金会旗下的AAIF；前一天，Claude API发布了2023年以来的首个新版本；同一天，托管服务商Railway公告称，存有客户API密钥的环境变量可能已泄露。我们从"一个技能文件夹"的视角把三条不同的消息放在一起读，并记录了自己检查的顺序。
---
> 本文由AI(Claude)协助撰写，并经编辑审核。本文的核心公司Anthropic是我们撰文所用Claude的开发商，而我们公司也自己制作并使用多个内部技能，因此存在利害关系。为此，公司公布的数字一律标注为"公司公布"，我们不做好坏评价，只记录自己实际检查的顺序。本文不构成对任何公司的投资意见。

本周三天之内出了三条关于"AI智能体零部件"的消息。一条关于规范(技能格式离开了一家公司，交给了基金会)，一条关于版本(Claude API三年来首次发布新版本)，一条关于钥匙(托管在服务商处的API密钥可能已泄露)。分开看是三条不同的新闻；但站在运营一个技能文件夹的立场上看，三条都汇聚到同一个问题：我的文件夹里有什么，它依赖什么。请把本文当作NO.8(当技能达到一万个)和NO.20(安装前的检查顺序)的后续来读。

## 1. 规范——技能格式交给了基金会(事实)

10月22日，Anthropic宣布将Agent Skills标准捐赠给Linux基金会旗下的Agentic AI Foundation(AAIF)。据公告，捐赠对象包括标准本身、"Agent Skills"的名称与标志、GitHub组织以及agentskills.io域名。AAIF是Anthropic与Block、OpenAI共同创立的基金会，Anthropic此前已把MCP(Model Context Protocol)交给了它。

Linux基金会的新闻稿称，同一天一次性接收了四个项目：Anthropic的Agent Skills、OpenAI的Open Responses(跨多家供应商的模型调用规范)、Hugging Face的OpenEnv(强化学习环境共享)和阿里巴巴的OpenSandbox(面向智能体的沙箱)。基金会管理的项目数量从2025年12月成立时的3个增加到10个。

技能是什么，规范网站(agentskills.io)给出了简短定义。**技能就是一个包含SKILL.md文件的文件夹。** 这个文件里有名称和描述(最低要求的字段)以及指令，需要时把脚本、参考文档、模板放在同一个文件夹里。智能体启动时只读取名称和描述，遇到匹配的任务时再读取完整指令，执行过程中打开脚本或参考文件。规范把这三步称为"渐进式披露"(progressive disclosure)。

规模数据是Anthropic公布的：70多个智能体产品已采用该格式(举例为ChatGPT、Cursor、GitHub Copilot、VS Code)，已发布的技能约100万个，安装约2.8亿次。德国媒体MIXED补充说，这些是公司自己的统计，不是经过独立核实的用户数。我们持同样立场。

运营方式也写在公告里。来自Anthropic、Google、OpenAI等公司的工程师将以个人身份而非公司代表身份维护标准，首席维护者是David Soria Parra和Mahesh Murag两人。不是基金会成员也可以使用和贡献。公告还列出了三项"接下来要做的事"：带版本号的正式发布、提议规范变更的正式流程，以及**面向编写和安装技能者的安全指南**。正如MIXED指出的，这三项目前仍是提案，还没有落地。

## 2. 版本——Claude API三年来首发新版本(事实)

早一天的10月21日，Claude API发布了新版本"2026-10-21"。Anthropic文档的版本列表里只有2023-01-01、2023-06-01和这次的2026-10-21三个条目，也就是时隔三年四个月的新版本。开发者账号(@ClaudeDevs)表示新的SDK和CLI默认使用该版本(我们未能直接打开X上的帖子，而是通过韩国聚合网站promppy的摘要和Anthropic官方文档确认的)。

迁移文档列出的变更中，小团队最可能马上碰到的有：

- **temperature、top_p、top_k三个参数被移除。** 即使按默认值发送也会返回400错误。文档写道，"依赖较低temperature获得稳定回答的代码将失去这一效果，且没有其他设置可以替代"。
- **认证请求头改变。** 新SDK以Authorization: Bearer的形式发送密钥，而不再是X-Api-Key。如果中间的代理或网关在读取旧请求头，就需要修改。
- 在assistant消息中直接放入document块，或在user消息的text块中放入citations，会返回400错误。
- 管理API的多个响应字段名改变(roles → role_ids、name → display_name等)。
- Python SDK从2.0.0起使用新版本。SDK和CLI的许可证改为Apache 2.0。

重要的是，**旧版本不会立刻停用**。文档写道，现有SDK会继续发送2023-06-01请求头，因此可以停留在当前版本，而2023-06-01的终止日期在任何地方都没有写明。"没有终止日期"和"永久保留"是两回事，所以我们只把前者记为已确认。

## 3. 钥匙——托管在服务商处的API密钥可能已泄露(事实)

同样在10月21日，应用托管服务商Railway在官方博客发布了安全公告。要点如下：当天早上在存储客户环境变量的系统中检测到异常活动，调查显示**未经授权的第三方可能访问了加密的环境变量，其中一部分甚至可能获取了解密后的内容**。环境变量通常包含API密钥以及数据库和镜像仓库的访问凭据。Railway写道，它把这起事件视为"近期针对平台公司的一系列攻击的一部分"，目的是攻破AI推理服务商。

公司采取了三项措施：通知上游服务商主动吊销密钥、暂停所有部署、确认受影响账户后以电子邮件通知。对用户，尽管初步分析显示影响可能仅限于部分用户，Railway仍强烈建议**立即更换所有环境变量(包括API密钥和私有镜像仓库凭据)，并检查相关服务的日志是否有异常使用**。公告中没有受影响账户数或泄露变量数之类的数字。

围绕这起事件，社交媒体和部分媒体流传着"被盗的密钥在黑市上立刻变现"、"有人需要生成用于蒸馏的训练数据"、"加密货币钱包被转走数十万美元"等说法。我们没能从Railway或调查机构的资料中确认其中任何一条，因此本文只写到"存在这样的说法"为止。

## 三条消息在同一个文件夹里相遇的地方(解读)

技能文件夹很轻：一份SKILL.md加几个脚本。但这个轻巧的文件夹依赖着三样东西。

第一，**格式**。文件夹结构和名称、描述字段必须遵循规范，其他智能体产品才能读取。规范在一家公司手里时，规则是"它改了你就跟着改"；交给基金会之后，变成"看版本和提案流程再跟进"。在基金会承诺的版本发布和安全指南真正出来之前，实际上和现在没有太大区别。

第二，**脚本调用的API版本**。如果技能里的脚本在传递temperature，或者经过一个读取X-Api-Key请求头的代理，那么在升级SDK的那一刻，这个技能就会悄悄坏掉。技能不是"安装时跑通了"就结束的东西，而是每当底层API版本变化时都要重新跑一遍的东西。

第三，**脚本使用的钥匙放在哪里**。即使你从未把密钥写进技能本身，只要密钥放在运行该技能的服务器的环境变量里，而那台服务器在托管服务商那里，钥匙就可能像这次Railway事件一样，从与你的文件夹无关的地方泄露。我们认为，这也是基金会把"面向编写和安装技能者的安全指南"列为首要任务的原因(这一联系是我们的解读，不是基金会阐明的理由)。

## 如果是我们——在技能文件夹里检查的三件事(实践)

我们公司用SKILL.md格式制作并使用内部技能(应用界面政策、资料分析流程、文章检查等)。以下是收到本周消息后我们实际检查的顺序。

1. **格式检查。** 我们确认了每个技能的SKILL.md都有name和description，并且描述能用一句话说明"什么时候拿出这个技能"。这两项是规范要求的最低字段，也是智能体启动时唯一读取的两项。基金会发布带版本号的版本后，我们决定把该版本号写进每个技能文件夹内的参考文档。
2. **版本检查。** 我们在技能文件夹的脚本里搜索了temperature、top_p、top_k和X-Api-Key这几个字符串。只要出现任何一个，该技能就进入"升级SDK前要修"的清单。我们不会立刻升级SDK，而是在待修清单清空后再升级。如果旧版本的终止日期公布了，就把日程提前。
3. **钥匙检查。** 我们再次搜索确认技能文件夹和代码仓库里任何地方都没有写入密钥，并列出密钥存放的位置(托管服务商的环境变量、密钥管理工具)。交给外部服务商的密钥被归类为"该服务商被攻破就会一起泄露的密钥"，并确认已设置用量提醒和支出上限。我们认为，Railway公告中建议的"检查日志中的异常使用"只有在平时以提醒方式收到才有用，而不是在事故发生之后。

即使没有新消息，这三项检查也值得每个季度跑一次。我们在NO.5中写过"指令是负债而不是资产"，技能文件夹也一样。文件夹越多，格式、版本、钥匙这三个轴上需要检查的东西也随之增加。

## 这条消息中我们未能确认的事

- Anthropic公布的70多个平台、约100万个技能、约2.8亿次安装是公司自己的统计，我们没有找到独立核实的资料。
- 我们未能直接打开@ClaudeDevs的X原帖，API新版本是通过Anthropic官方文档(版本列表、迁移指南)确认的。Python以外其他语言SDK的确切新主版本号未能从文档中确认。
- 文档中没有2023-06-01版本的终止日期。我们只确认到"没有"为止。
- Railway事件的影响规模(账户数、变量数)、攻击者以及与其他平台入侵事件的关联未写在Railway公告中，媒体和社交媒体的数字(钱包损失额等)未能确认。
- 参考网站Learn:US 10月20日的文章(如何安全安装他人制作的技能)我们只读到了公开的列表摘要，未能打开正文。

## 一起读过的文章

我们直接打开并确认了性质不同的来源。公司与基金会公告、官方文档、媒体、个人博客分开列出。

公司与基金会公告：

- [Donating Agent Skills to the Agentic AI Foundation (Anthropic)](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) — 英文，公司公告(数字为公司统计)
- [Agentic AI Foundation Announces Four New Projects: Agent Skills, Open Responses, OpenEnv, and OpenSandbox (Linux Foundation)](https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox) — 英文，基金会新闻稿
- [Security Disclosure: Wednesday October 21st (Railway)](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) — 英文，公司公告

官方文档与规范：

- [Agent Skills Overview (agentskills.io)](https://agentskills.io/) — 英文，规范网站
- [Versions (Claude Platform Docs)](https://platform.claude.com/docs/en/api/versioning) — 英文，官方文档
- [Migrating to API version 2026-10-21 (Claude Platform Docs)](https://platform.claude.com/docs/en/api/migration-2026-10-21) — 英文，官方文档

报道与摘要：

- [Anthropic hands its widely used AI skills standard to an independent foundation (MIXED)](https://mixed-news.com/en/anthropic-agent-skills-agentic-ai-foundation/) — 英文，媒体(指出公司数字的局限)
- [Anthropic发布Claude API新版本2026-10-21 (promppy)](https://www.promppy.com/item/2535081) — 韩文，AI摘要聚合网站(原始来源为X帖子)
- [Railway入侵事件，AI API密钥被盗 (promppy)](https://www.promppy.com/item/2535863) — 韩文，AI摘要聚合网站(原始来源为X帖子，含未经确认的说法)

个人博客与实务网站：

- [Donating Agent Skills to the Agentic AI Foundation (Simon Willison)](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) — 英文，个人博客(回顾2025年12月的预测文章)
- [开工前放进Claude的三个技能 (Learn:US)](https://learn.bizni.us/) — 韩文，实务网站(仅确认公开摘要)
