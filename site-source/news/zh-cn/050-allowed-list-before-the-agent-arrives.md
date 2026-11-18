---
no: 50
slug: allowed-list-before-the-agent-arrives
date: 2026-11-17
category: 洞察
tags: 智能体 · Poppy · Shopify · Meta Muse · Uber · 智能体安全 · Apple · 健康AI · OpenEvidence · 电商
title: 在智能体到来之前写好"允许做什么"的三份文件 — 从11月13日起，所有Shopify店铺自动发布一份 /.well-known/poppy.json，写明"智能体在我们店里可以做什么"；Uber 只在为每个自家智能体登记了"允许的意图·约束·风险等级"之后才让它运行；Apple 则给健康AI的回答加上"临床引用·可疑问题检测·不用于训练"，交给20万人评价
summary: Sierra 与 Meta 制定的个人智能体规范"Poppy"1.0 于11月13日发布。公司在自己域名下的 /.well-known/poppy.json 这一个文件里写明"我们是谁、智能体可以从哪个门进来、可以做什么"，顾客的智能体会先读这个文件；Shopify 已开始为所有店铺自动发布该文件，Meta 的 Muse 在访问的每个网站上都会先找这个文件（公司发布）。Uber 于11月6日在工程博客中写道"身份验证只能回答'是谁'，无法回答'这个行动是否符合语境'"，并描述了为每个智能体登记身份·所有者·允许的意图·约束·风险等级、在执行瞬间进行检查的结构（无数字）。Apple 于11月15日与 OpenEvidence 一起开放"健康AI使用研究"应用，让美国21岁以上、最多20万名参与者获得附有临床出处的回答并进行评价，并写明"研究数据不用于训练AI模型""检测到可疑问题会引导至医疗人员"。我们把三件事归为"在行动发生之前把允许范围写成文件的方式"。
---
> 本文由AI（Claude）协助撰写，并经编辑审核。我们公司是 Anthropic 和 OpenAI 两家公司的付费客户，也在测试中使用 Google 的模型。第1条的 Poppy 建立在 Anthropic 最初制定的规范 MCP 之上，我们在此说明。**我们自己运营电商、应用和AI网红，因此在这三条消息中都站在"必须写文件的一方"** — 所以我们不对任何公司的做法添加评价，只转述文件里写了什么、没写什么。公司发布的数字标注为"公司发布"，仅有一处来源的内容附上该来源。第3条中与健康相关的叙述不是医疗建议。本文不是对任何企业的投资意见。

我们在 NO.43 写过"顾客带不来自己的智能体"，在 NO.45 写过美联航宣布"禁止个人智能体预订"，在NO.49写过 AT&T 设下"准确率达到95%以上之前不给自主权"的门槛。本周的三条消息是下一步 — **在行动发生之前，把"允许做什么"写成文件。**店铺在智能体到来之前写一个文件，公司在运行智能体之前写一行登记，Apple 在回答发出之前写三个条件。我们分成事实·解读·如果是我们来写。

## 1. Poppy 1.0 — 店铺把"智能体在我们家可以做什么"写进一个文件（事实，公司发布）

Sierra（由前 Salesforce 联席CEO布雷特·泰勒领导的AI客服公司）于11月13日在官方博客（布雷特·泰勒与克莱·贝弗合写）发布了**"Personal Agent Protocol"— 昵称 Poppy — 1.0**。他们于10月6日与 Meta 首次宣布，10月9日发布草案，并写道"用五周时间在真实网站、API 和智能体上测试了草案"。我们直接阅读了规范原文（personalagentprotocol.org）。方式是这样的 — **公司在自己域名下的 `/.well-known/poppy.json` 放一份 JSON 文档。**里面写有 `organization`（名称·域名·标志）、智能体可以进入的门（`agent.protocols` 对话入口、`apis` — OpenAPI 或 MCP、`web` — 浏览器会话入口、`tasks`、`extensions`），以及策略（`auth.disabled` 关闭登录、`web.disabled`"请勿浏览我们的网站"、`web.unscoped` 浏览器登录是否意味着整个账户的访问权）。每个范围都可以用 `scope_hints` 字段标注 **`irreversible`（不可撤销的行动）· `personal_data`（涉及个人信息）**。登录使用 OAuth 2.0（PKCE·设备登录 RFC 8628），会话使用带签名的 `Poppy-Session` 令牌。规范自称"1.0 是 0.4 加上修正"，尚未覆盖的领域转到路线图页面。Sierra 的文章写道，Poppy 建立在 MCP·OpenAPI·UCP 等现有规范之上，电商扩展由 Shopify 共同撰写，并有带校验器的实施工具包。

参与公司是公司发布的数字。在10月的8家初始设计伙伴（Meta·Genesys·Instinct·NiCE·Rocket·Shopify·Stripe·Walmart）之外又加入60家，共**100家以上**（含 Affirm·达美航空·Salesforce·Twilio·Wayfair·Zoom 等），实际开启的是 Mercury（银行 — 支付请求要经过账户的审批策略）·Synchrony·土耳其航空（里程会员在付款前批准商务舱升级）。两句话是本文的中心。**"所有 Shopify 店铺现在都会自动发布 Poppy 文件，商家无需额外做任何事"**（Sierra）— Shopify 在175个以上国家运营店铺；购物车·结账由 UCP 负责，之前的"是谁·可以做什么"由 Poppy 负责。还有**"Meta 的 Muse 在访问的每个网站上都会先找 Poppy"**。TNW（11月13日）把 Muse 用户写为"1000万人以上"（一家媒体），并一同写道：尽管编号是1.0，规范仍标为"草案"，可能出现破坏兼容性的变更；Visa·Mastercard 正在构建单独的智能体身份验证；Amazon 希望顾客使用自家智能体而不是 Muse。

放两行背景。据 Practical Ecommerce（9月24日），Shopify 于9月8日 — Muse 发布当天 — 把 Meta 加入"Agentic Storefronts"，默认把商家商品共享给 Meta（商家可以关闭），而 Amazon 对同一个 Muse 弹出"未经授权的AI智能体继续访问违反使用条款"的提示加以阻止（NO.43）。CMSWire（10月7日）转述的 Sierra 联合创始人的话是**"消费者决定给予哪些访问权，公司决定智能体可以做什么的上限"**，Meta 则称其为"像电子邮件一样没有任何一方拥有的规范"，但治理模式未公开，两家公司的伙伴名单也彼此不同。规范网站页脚标有 **Apache License 2.0**（personalagentprotocol.org，11月18日直接确认）；未注明标准化组织或治理主体。支付尚不是核心，而是"扩展候选"。

## 2. Uber — "身份只能回答'是谁'"，为每个智能体登记允许的意图和风险等级，再在执行瞬间检查（事实，公司发布）

我们直接阅读了 Uber 工程博客（11月6日，肖恩·陶特·马克斯·朱罗维奇·阿迪·拉加文德拉）的文章《Securing AI Agents: Lessons From Real-World Deployment》，InfoQ（11月15日）做了整理。出发点是这句话 — **"传统授权可以决定'谁'可以行动，但无法判断智能体要做的行动在语境中是否合适。"**要防范的是提示注入·工具与记忆投毒·目标劫持·行为漂移·由幻觉产生的行动（手法文章中没有，我们也不写）。结构分三层。**①部署前**：所有智能体登记到"AI Registry"，写明身份·所有者·人格·**允许的意图（intents）·约束·依赖·风险等级**，名为"Argus"的自动分析器扫描代码·提示·配置·依赖·端点·工具调用路径以寻找弱点，并预先生成人格·意图草稿供开发者审阅（MCP 服务器和工具走同样的流程）。**②运行中**："AI Guard"作为策略判定点，运行在**本地部署的小型专用模型**上，"Agent Guard"钩子在智能体与工具执行的边界截获行动并应用判定。检查的是：行动是否符合人格·允许的意图·语义约束，是否符合用户的请求和角色，在整个会话语境中是否说得通。**③部署后**：把智能体行动·工具调用·判定串成一条线的执行追踪（屏蔽敏感信息，仅在需要时包含内容），以及把已记录的交互对新策略**"回放"**、在应用之前先测试的机制。

遇到的困难也写了出来 — **误拦截与误放行的平衡**（用只记录不拦截的影子模式·回放·按智能体校准来处理）、延迟（并行执行·用小型专用模型替代大型通用模型）、开发者摩擦（Argus 自动化），以及"所有智能体同一套规则"不适合目的和风险各异的智能体。文章以**"安全·准确率·延迟·成本·自主性·开发者体验无法各自单独优化"**收尾，并预告了后续文章（人格·语境护栏·可观测性·意图过滤）。**没有一个数字** — 误拦截率·延迟·成本·智能体数量都没有。也没有写是否开源。作为参考，有报道（Techstrong，8月10日）称 Uber 在8月公开了另一个工具"ADR"— 5万个以上智能体·运行10个月·"凭据泄露比提示注入更常见"，均为公司发布 — 但那篇报道和11月的文章彼此都没有提及，所以**两者的关系我们未能确认。**我们照原样转述 InfoQ 文章中一位读者的提问 — "对于不是我自己构建的智能体，这要怎么适用。"

## 3. Apple — 给健康AI的回答加上"临床引用·可疑问题检测·不用于训练"，交给20万人评价（事实，公司发布）

Apple 于11月15日在 Newsroom 发布**"Apple Health AI Usage Study"**，同日在美国 App Store 上线"Apple Health AI Study App"（开发者 Apple Inc.，免费，仅限 iPhone，iOS 26.0 以上）。我们直接阅读了两个页面。合作方是 **OpenEvidence** — 2022年成立于迈阿密的公司，运营面向医生的 LLM 医学检索；据维基百科，截至2025年12月约有76万名美国医生注册，每月用于1800万次临床咨询（公司发布），并与 NEJM·JAMA 签有内容许可（融资内容本文不涉及）。参与条件是**居住在美国、21岁以上、已启用 Apple Intelligence 的 iPhone 15 Pro 或更新机型、iOS 26 以上、最多20万人。**参与者提出日常健康问题，用通俗语言阅读复杂的医学信息，并在问卷中评价回答质量。回答**取自 NEJM·JAMA·Nature 等医学出处，每条回答附有经同行评审的临床引用链接。**愿意的话可以共享健康应用中的静息心率·活动·睡眠·检验结果，看个人数据会在多大程度上改变回答的适切性。文章中写了三个条件 — **"研究数据不会用于训练AI模型"**，应用有**"旨在检测某些可疑问题并建议参与者向医疗人员或其他资源跟进"**的护栏，以及**"本应用不做诊断·治疗，不替代专业人员的建议"**。Apple 健康与健身副总裁、医学博士苏姆布尔·德赛说"健康是极其个人的事"，称这项研究是"了解人们如何使用、理解和评价健康AI的最审慎的方式"。研究期限 Newsroom 中没有。

媒体补充的各有一处。TechCrunch（11月15日）写道研究为期**12个月以上**，健康数据匿名化后送往"安全的第三方云服务商"，且 **OpenEvidence 在24小时后删除问答数据**（这三点 Apple Newsroom 中没有，仅 TechCrunch 一处）。同一篇文章补充说 OpenAI 今年早些时候表示每周收到"3亿次以上与健康相关的提问"（OpenAI 原文在我们这边打不开，未确认）。TechCrunch 把设备条件写为"iPhone 15 或更新"，而 Apple Newsroom 和 Business Standard（11月16日）写为"iPhone 15 Pro 或更新"，我们采用 Apple 的写法。iGeeksBlog（11月16日）引用 Apple 写道"基于LLM的消费者健康工具有时可能给出不完整或不清晰的回答"，但我们在所读的 Newsroom 正文中没有找到这句话，故作为一家媒体处理。App Store 的隐私标签为"User ID — 与用户关联（分析·应用功能）"，年龄分级18+。

## 把三件事放在一起读（解读）

第一，**三份都是在"行动之前"写下的文件。**NO.39 的"停止按钮"是在行动之后按的，NO.49中 AT&T 的"准确率95%以上"是在行动的同时测量的门槛。这次的三件事在它们之前 — 在智能体到来之前（poppy.json）、在运行智能体之前（登记簿）、在回答发出之前（引用·检测·告知）写下。顺序从后往前移，看起来是今年下半年的方向（解读）。三份文件共同的栏目是**"不可撤销的行动"**— Poppy 给范围标上 `irreversible`，Uber 谈到"把特权行动绑定到用户实际请求"的证据链，Apple 把可疑问题交给人（医疗人员）。我们在 NO.39 写过"不可撤销的行动从一开始就应在智能体手之外"，这句话成了协议里的字段名。

第二，**"阻挡"与"开放"写在同一个文件里。**poppy.json 里，"请勿浏览我们的网站"（`web.disabled`）与"从 API 进来"（`apis`）并排放着。这意味着美联航的禁令（NO.45）与 Shopify 的开放可以成为同一形式的句子，于是顾客的智能体读到的不是"被挡住了"，而是"这扇门关着，那扇门开着"（解读）。但阅读时有三点要留意 — 规范"虽是1.0但仍是草案"，已预告会有破坏性变更；许可证标为 Apache License 2.0，但未注明治理主体；CMSWire 提出的问题"店铺的门由哪家公司的智能体来守"（Sierra 自己也是卖客服智能体的公司）仍然悬而未决。"100家以上"是设计伙伴数，"已开启"的是三家，所以转述数字时我们分成两栏（NO.21）。

第三，**Uber 和 Apple 不是"去掉人的文件"，而是"写下交给人的条件的文件"。**Uber 的登记簿看起来像授予自主权的手续，但核心是"在执行前一刻拦下不符合语境的行动"和"新规则先以只记录的影子模式运行"。Apple 让20万人评价回答，却先写下"不做诊断·治疗""可疑问题交给医疗人员"。我们在 NO.03 写过如何让我们的成分表应用不说"安全"；Apple 的文件是它的放大版 — 不同之处在于**每条回答都附引用链接，评价回答的人是用户本人**（解读）。没有数字这一点也相同 — Uber 没写误拦截率，Apple 没写期限，Sierra 没写实际会话数。本文的数字中，没有一个是在公司之外数出来的。

## 如果是我们 — 运营电商·应用·AI网红的团队本周要做的三件事（实践）

1. **先"不发布"地填一填我们电商域名的 `/.well-known/poppy.json`。**把 NO.43 的"进来的智能体规则三行"和 NO.45 的"为什么"一栏搬到这个文件的字段里，空白立刻可见 — `organization`、开哪些门（只有 `web` 还是也有 `apis`）、是否开启 `web.disabled`、在 `scope_hints` 里是否把下单·支付标为 `irreversible`、把收货地址标为 `personal_data`。因为规范还是草案，**发布要等代表决定之后**，并在表头写上"1.0＝草案，可能有破坏性变更"。如果我们商品所在的外部渠道有基于 Shopify 的，那家店已经自动发布了文件，去读一遍里面写了什么。
2. **用 Uber 式的七栏把我们的智能体登记簿写在一页上。**Lia 的脚本生成、成分表判定（NO.03）、电商咨询回复，以及收集并撰写 AP News 的这个会话本身 — 每一项都写上身份·所有者·人格·允许的意图·约束·依赖（使用哪些 MCP 服务器·工具）·风险等级。放在NO.49"去掉人的门槛N%"那一栏旁边。加入新约束时，像 Uber 那样先以**影子模式运行两周**（只记录不拦截），看误拦截·误放行的件数后再开启。
3. **给 SafeList（成分表应用）的回答加上 Apple 式的三行。**①每条回答附依据链接（对我们来说，MFDS 公告·原材料数据库就是引用），②"可疑问题"清单（过敏反应·与药物的相互作用·婴幼儿摄入等，不作回答而改为"请咨询专业人士"），③条款里是否真的有"用户提问不用于模型训练"这句话，以及保留期限以数字写出（像 TechCrunch 写的"24小时"）。再在回答下方放一个评价按钮（"正确／不确定／错误"）— 不是20万人，但从20条开始计数。

## 这次没有选的

英伟达CEO黄仁勋辞职及回归传闻，以及随之而来的股价·供应链·出口管制报道属于个人事务和投资领域，我们不写。关于 Anthropic 上市的报道（Bloomberg）属于投资领域且存在利益关系，不采用。美联储金融稳定调查中"87%提及AI相关风险"（Reuters）出于同样理由只留标题。迪士尼扩大AI应用（Bloomberg）我们未能打开原文。美团的 LongCat-2.5（1.6万亿参数开放权重，The Decoder）和 Edge0-145B 未能确认官方模型卡，留作周六每周资讯的候选。FAA 在全国推广空管辅助工具 SMART（Gizmodo，"人类管制员保留最终权限"）是"人的监督"的后续候选，但我们没有打开原始资料。在 promppy 上看到的"白宫：自愿报告AI安全事件可获一年监管责任减免"（AI Times）— 未能获得原文地址。OpenAI 开设科学博客以及与 GPT-6 Astra 共同撰写的标准模型论文，因 openai.com 在我们这边打不开而只留标题。Anthropic 的模型文档页面这次打开的是只显示 Claude 4.x 模型的旧版本，我们暂缓引用（与11月14日确认的 Fable 5.1 表格不同）。Anthropic 新闻室11月16日也没有新文章，OpenAI 的新闻列表这次仍然打不开。

## 这条消息中我们未能确认的

- Poppy 规范网站页脚标有 Apache License 2.0（11月18日直接确认），但未注明标准化组织或治理主体。"100家以上"是设计伙伴数（公司发布），实际开启的是 Mercury·Synchrony·土耳其航空三家。Muse 用户"1000万人以上"仅见于 TNW。我们没有去找 Shopify 自己的发布页面，而是按 Sierra 文章中"所有店铺自动发布"这句话来写。
- 实际通过 Poppy 发生的会话数·订单数哪里都没有。支付只写为"扩展候选"。
- Uber 的文章没有数字（误拦截率·延迟·成本·智能体数量），也没有开源与否。8月 ADR 公开的报道（仅 Techstrong）与11月文章的关系未能确认。文章也没写 Uber 使用哪家模型公司的模型。
- Apple 研究的期限 Newsroom 中没有，"12个月以上"·"匿名化后送往第三方云"·"OpenEvidence 24小时后删除"仅 TechCrunch 一处。设备条件 TechCrunch（"iPhone 15 或更新"）与 Apple（"iPhone 15 Pro 或更新"）不同，我们采用 Apple。"不完整或不清晰的回答"这句话是 iGeeksBlog 引用 Apple 的文章，我们在 Newsroom 正文中没有找到。
- OpenEvidence 的76万名医生·每月1800万次是维基百科转述的公司发布。OpenAI 的"每周3亿次健康提问"是 TechCrunch 所写，OpenAI 原文我们打不开。
- 任何一家公司的发布，我们都没有亲自测试或计数。

## 一起读过的文章

我们直接打开并核对了性质不同的来源。分为公司发布·官方文件、规范原文、媒体报道、维基、我们之前的文章。

公司发布·官方文件：

- [Releasing Poppy 1.0（Sierra 博客，布雷特·泰勒·克莱·贝弗，11月13日）](https://sierra.ai/blog/releasing-poppy) — 英文，MCP·OpenAPI·UCP 之上的 OAuth·5周测试·电商扩展由 Shopify 共同撰写·伙伴100家以上·Mercury·Synchrony·土耳其航空·"所有 Shopify 店铺自动发布 Poppy 文件"·对全部 Muse 用户开启
- [Securing AI Agents: Lessons From Real-World Deployment（Uber Engineering，11月6日）](https://www.uber.com/blog/securing-ai-agents/) — 英文，AI Registry·Argus·AI Guard·Agent Guard·执行追踪·回放，三层结构，困难清单，无数字
- [Apple launches research study to explore the use of AI for health（Apple Newsroom，11月15日）](https://www.apple.com/newsroom/2026/11/apple-launches-research-study-to-explore-the-use-of-ai-for-health/) — 英文，OpenEvidence·21岁以上·iPhone 15 Pro 以上·iOS 26·最多20万人·NEJM/JAMA/Nature 引用·可疑问题检测·不用于训练·非诊断·德赛发言
- [Apple Health AI Study App（App Store）](https://apps.apple.com/us/app/apple-health-ai-study-app/id6800060365) — 英文，开发者 Apple Inc.·免费·仅限 iPhone·iOS 26.0 以上·"不提供医疗建议·诊断·治疗"·隐私标签

规范原文：

- [Personal Agent Protocol 1.0 Specification](https://personalagentprotocol.org/docs/1.0/spec) — 英文，`/.well-known/poppy.json`·organization·agent.protocols·apis·web·tasks·extensions·auth.disabled·web.disabled·scope_hints（irreversible·personal_data）·OAuth 2.0 PKCE·RFC 8628·Poppy-Session·"1.0＝0.4＋修正"（读了前10万字）

媒体报道：

- [Sierra's Poppy 1.0: Shopify turns it on for every store, Meta's Muse looks for it first（TNW，11月13日）](https://thenextweb.com/news/sierra-poppy-1-0-shopify-meta-muse-personal-agents) — 英文，Muse 1000万人以上（一处）·"虽是1.0但仍是草案"·土耳其航空·Mercury 案例·Visa·Mastercard·Amazon
- [Sierra and Meta unveil Personal Agent Protocol（TNW，10月6日）](https://thenextweb.com/news/personal-agent-protocol-sierra-meta) — 英文，首次发布·伙伴6家·OAuth·顾客决定读/写·公司决定路径·支付是未来工作
- [Sierra's Poppy draft spells out how AI agents can access businesses（NeoTeo，10月9日）](https://www.neoteo.com/en/sierras-poppy-draft-spells-out-how-ai-agents-can-access-businesses) — 英文，草案·/.well-known/poppy.json·新增35家设计伙伴·Rocket 演示（Sierra 自述）
- [Genesys joins Sierra, Meta on open standard for personal AI agents（CMSWire，10月7日）](https://www.cmswire.com/contact-center/genesys-joins-sierra-meta-on-open-standard-for-personal-ai-agents-01/) — 英文，"消费者决定访问权，公司决定上限"·治理未公开·伙伴名单差异·开放问题
- [Meta Muse, Shopify, Amazon and the race to own AI shopping（Practical Ecommerce，9月24日）](https://www.practicalecommerce.com/?p=1567232) — 英文，背景：9/8 Shopify 的 Agentic Storefronts 加入 Meta·Amazon 阻止 Muse 的提示语
- [Uber's Secure AI framework for autonomous agents（InfoQ，11月15日）](https://www.infoq.com/news/2026/11/uber-secure-ai-framework/) — 英文，Uber 文章整理·读者提问"对不是我构建的智能体"
- [Uber open-sources ADR to catch agentic blunders（Techstrong.ai，8月10日）](https://techstrong.ai/articles/uber-open-sources-tool-to-catch-agentic-blunders-legacy-security-misses/) — 英文，8月的另一个工具（公司发布数字，一处）— 与11月文章的关系未确认
- [Apple launches new app to study how people use AI for health（TechCrunch，11月15日）](https://techcrunch.com/2026/11/15/apple-launches-new-app-to-study-how-people-use-ai-for-health/) — 英文，12个月以上·匿名化·第三方云·24小时删除（一处）·OpenAI 每周3亿次（转述）
- [Apple launches app to study how people use AI for health queries（Business Standard，11月16日）](https://www.business-standard.com/technology/tech-news/apple-launches-app-to-study-how-people-use-ai-for-health-queries-details-126111600875_1.html) — 英文，iPhone 15 Pro 以上·仅限美国·无期限·无报酬
- [Apple's AI health study is open to up to 200,000 U.S. iPhone users（iGeeksBlog，11月16日）](https://www.igeeksblog.com/apple-health-ai-usage-study-app/) — 英文，"不完整或不清晰的回答"引用（一处）·期限未公开·隐私标签

维基：

- [OpenEvidence（Wikipedia）](https://en.wikipedia.org/wiki/OpenEvidence) — 英文，2022年成立·迈阿密·医生76万人·每月1800万次（公司发布）·NEJM·JAMA 许可

我们之前的文章：

- [没有主持人也没有摄像机的节目进入了固定编排（AP News NO.49）](https://www.apholdings.kr/ko/news/no-host-ai-broadcast-and-who-must-disclose/)
- [每周AI资讯 — OpenAI 把钱包交到智能体手里，美联航把"顾客的智能体"挡在门外（AP News NO.47）](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [挡住顾客的智能体，迎进店铺，把模型给所有人（AP News NO.45）](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [顾客带不来自己的智能体（AP News NO.43）](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- ["智能体可能越权"开始写进披露文件（AP News NO.39）](https://www.apholdings.kr/ko/news/agent-risk-goes-into-the-filings/)
- [当验证码落到智能体手里（AP News NO.36）](https://www.apholdings.kr/ko/news/agents-raised-their-own-spending-caps/)
- [智能体是"不可信的内部人"（AP News NO.29）](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
- [比较数字之前先看算法（AP News NO.21）](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [当AI替你读成分表（AP News NO.03）](https://www.apholdings.kr/ko/news/ai-reads-the-label/)
