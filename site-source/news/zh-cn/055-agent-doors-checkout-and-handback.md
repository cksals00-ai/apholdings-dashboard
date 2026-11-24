---
no: 55
slug: agent-doors-checkout-and-handback
date: 2026-11-23
category: 实践
tags: AI 代理 · 代理式商务 · 谷歌 Connected Apps · Universal Commerce Protocol · Booking Holdings Vayo · 结算移交 · Sabre MCP · Grok · 美联航 · 追加销售 · 代理渠道价格 · 商品信息
title: 代理已走到结账按钮前 — 谷歌在搜索内打开了杂货购物结账，Booking Holdings 的代理写道“对不允许的供应商，把结算页交给顾客”，Sabre 称“顾客不会翻页浏览结果，只看一两个”并把交易引擎先接入 Grok，酒店 CEO 则以“代理不会冲动消费”为由表示要关门 — 商家本周要决定的，是四种门中的哪一种
summary: 谷歌于11月20日宣布，在美国已开放通过搜索和 Gemini 应用的 Connected Apps 创建 Albertsons·Safeway·Shaw's·Target 的杂货订单并完成结账的功能(基于 Universal Commerce Protocol·无价格·无数字)。Booking Holdings 的 AI 旅游代理 Vayo 于11月17日在新闻稿中写道“有直接对接的走对接，没有的则浏览预订网站完成预订，若供应商不允许代理预订，则在确认价格后把结算页交给旅行者”(非公开测试)。旅游分销系统公司 Sabre 于11月16日在 Grok Bot 市场上架首个旅游插件，并宣布“正在试点·运营 MCP 服务的合作方有80家以上”，其 CEO 对媒体表示“顾客不会翻页浏览结果，只看一两个，最多三个”。另一边，酒店连锁 CEO 以“人会被促销打动，但代理不会”为由表示将阻止自己酒店的代理预订，Booking Holdings 则称经 LLM 的预订“远不及1%”，均为 Skift 报道。我们把这四条归为“门的种类·门把手·只能看到一两个的货架·仍然很小的数字”，为运营电商·应用·AI 网红的小团队写下本周要决定的一页(门表)。这是 NO.45·47·50·53“代理之门”的实践篇。
---
> 本文由 AI(Claude)协助撰写，并经编辑审核。我们公司是 Anthropic 和 OpenAI 两家公司的付费客户，也在测试中使用谷歌、Meta 的模型。先说明利害关系 — **本文的主题“商家一方的决定”正是我们自己的事。** 我们直接运营电商(Hangeul Cubs)、应用(CourtMate 等)和 AI 网红(Lia)，因此“如果是我们”一节写的是我们实际会做的事，本文并非推荐某一平台。第1条谷歌消息是我们在测试中使用的公司的发布，第3条 Sabre 向媒体提到的2027年扩展对象平台名单中，包括撰写本文的 AI 的制造商 Anthropic 的 Claude(新闻稿中没有这个名字)。因此我们不对任何公司添加评价，只转述已发布的数字与原话；公司公布的数字标为“公司公布的数字”，仅一处来源的内容附上该出处。本文不是对特定企业的投资意见。

我们在 NO.45 写了美联航把“顾客的代理”挡在门外的同一天 OpenAI 把商家请进 ChatGPT 的事，在 NO.47 写了 OpenAI 把钱包交到代理手上的事，在 NO.50 写了 Shopify 商家开始把“代理可以做的事”自动发布为一页的事，在 NO.53 写了 Meta 的代理在加拿大杂货购物中走到结账的事。本周的四条消息展示了那些门**正在凝固成什么形状** — 谷歌在搜索内打开了结账之门，Booking Holdings 的代理写下了“在不允许的商家，把结算页交给顾客”这道中间门，Sabre 想占据商家与代理之间“交易引擎”的位置，而酒店连锁则用数字说出关门的理由。我们把三份公司发布(谷歌·Vayo·Sabre)和媒体报道·专栏(Skift·PhocusWire)分成事实、解读、如果是我们三部分来写。

## 1. 谷歌“用 Connected Apps 完成年末事务” — 在搜索内完成杂货购物结账 (事实·公司发布)

我们直接阅读了谷歌官方博客文章 **“Get your year-end tasks done with new Connected Apps”**(11月20日，未标注作者)。这是一则宣布**在美国可通过搜索和 Gemini 应用的 Connected Apps 创建 Albertsons·Safeway·Shaw's·Target 的杂货订单并完成结账**的发布。文章写明这些杂货应用**“基于 Universal Commerce Protocol(UCP)”**，并链接到另一篇商务专文。金融方面，**Experian** 已在 Gemini 应用中，现扩展到搜索，可查看信用评分、比较个人贷款；税务方面，可在搜索中调用 **H&R Block** 进行税额计算和退税估算；**Angi·Thumbtack**(本地维修·装饰人工服务)将在“几周内”接入搜索。**价格、手续费、使用数据、确切上线日期、美国以外的日程均未见于文中。** 这是一则没有任何数字的发布。

我们一并读了两份背景材料。第一，10月28日谷歌开发者文章 **“Build and manage Connected Apps in one place”**(署名搜索·Gemini 应用两位产品负责人)。Connected Apps Platform 以预览版开放，开发者可**通过云端 MCP 服务器或 Android MCP(AppFunctions API)对接**，在 **Google Connected Console** 注册、测试、提交，选择上线于搜索还是 Gemini 应用，上线后管理流量、延迟、错误率以及已认证的标志和账户。文中写到已有“50个以上的 Connected Apps”(生产力·票务·健康·健身)，Adobe·Experian·Localiza·Peloton 已在 Gemini 中，并将在“几周内”进入搜索。这篇文章没有 UCP、手续费、审核周期、国家名单。第二，Target 的官方资料 **“How Target is Shaping Shopping Experiences in Conversational AI”**(6月18日更新)。Target 自称是在谷歌搜索(含 AI Mode)·Gemini 应用、微软 Copilot、OpenAI ChatGPT **三个平台上均可结账的首家大型零售商**，并把谷歌端的流程写为“提问 → 选项 → ‘Buy’ → 登录 Target 账户 → 确认”，支付方式为 Google Pay 中的信用卡或 Target Circle 卡，以及**“一次结算多件商品正在准备中”**(6月时点)。一个数字 — **“AI 带来的流量在第一季度同比增长2,000%”**(Target 公布的数字，零售整体约400% — 引用 Adobe 资料)。从7月第一批 Connected Apps(Instacart·Canva·YouTube Music，美国·选择加入·购买需用户批准 — eWeek 7月17日)到这次11月的杂货购物结账，用了四个月。

## 2. Booking Holdings 的 Vayo“预订整趟旅程” — 对接·浏览·以及“把结算页交给顾客” (事实·公司发布·媒体)

我们阅读了 Booking Holdings 旗下 AI 旅游初创公司 **Vayo 的新闻稿**(11月17日，西雅图，PR Newswire — 我们读的是 finviz 转载本，其中附有原文地址)以及 PhocusWire·Skift(科技记者 Adriana Lee，11月17日)的报道。这是一则宣布 Vayo 在上线一个月后即可预订**航班、酒店、度假住宿、餐厅、活动、演出门票、租车、火车、巴士、渡轮、机场接送乃至停车**的发布(当日向非公开测试会员提供，有候补名单)。

方法是本文的核心。新闻稿写道**“有直接对接的地方走对接，没有的地方则浏览预订网站，代旅行者完成预订”**，并写道**“若供应商不支持代理预订，Vayo 会找出最佳选项、确认价格后，把可立即完成的结算页交给旅行者”**。所有预订都需要旅行者批准，且**只有在收到供应商确认后才标为“已确认”**。登录通过 **1Password for Agents** 完成，不查看也不保存密码；支付通过 **Stripe 的 Link 代理钱包**完成，不接触支付信息。价格方面 — **当 Booking.com 是最佳选项时，所有 Vayo 旅行者都享受 Booking.com 最高等级的 Genius Level 3 价格(部分住宿最高20%折扣)**。Vayo 自身的收费、供应商名单、预订件数均未见于新闻稿。PhocusWire 转述 Vayo CEO(迈克·弗里根(Mike Fridgen))的话：**“在像美联航那样不允许的地方，我们会交出结算页，并欢迎通过获许可的渠道合作的机会”**，并写道 Booking Holdings 在上线时表示**“以产品进展和市场状况为条件，计划投资1亿美元”**，对纽约的 Lola(KAYAK 创始人们)也宣布了相同金额(1亿美元出自 PhocusWire·Skift 两家媒体，新闻稿中没有)。Skift 写道，直接对接的是 Booking.com(酒店·租车·活动)·OpenTable·SeatGeek，航班、火车等则是浏览获许可的供应商网站；指出 Genius 价格可能在比较中让 Booking 自有库存占优(Skift 的分析)；并附上**Skift Research 10月调查中仅27%的美国旅行者表示对 AI 预订感到放心，AI 的占比为“灵感”阶段21%对“预订”阶段6%**的数字。预订件数、交出结算页的比例，公司未公开。

## 3. Sabre“交易引擎” — Grok Bot 上的首个旅游插件、“MCP 合作方80家以上”、“顾客只看一两个” (事实·公司发布·媒体)

我们阅读了旅游分销系统(GDS)公司 Sabre 的**新闻稿**(11月16日，得克萨斯州绍斯莱克，PR Newswire — finviz 转载本)以及 PhocusWire、Skift(11月19日，同一记者)的报道。Sabre 在11月17日纽约投资者日上预展了**将上架 Grok Bot 市场的“首个全球旅游插件”**，并宣布对话式预订·管理窗口 **Mosaic Travel Connector“即将进入测试”**。它建在2025年推出的 MCP 服务器和面向代理的 API 之上，文中写道**“正在试点或运营 MCP 服务的合作方有80家以上”**(公司公布的数字·未区分试点/运营，未列名字)。新发布的**“事件驱动 API”**监控航班取消·延误信号，识别受影响的旅行者，并向与旅行社系统相连的 AI 工具推送通知；应对方式有三条路径：**人工顾问处理、连接器在对话内呈现合规选项供一键批准、自主代理直接处理**。价格监控处于测试阶段，计划是“在2027年内扩展到主要对话模型和旅行社工作流”，**费用、收益条件、手续费均未见于新闻稿。** 新闻稿中也没有 Grok 以外的平台名称。

媒体补充的内容。PhocusWire 转述 Sabre CEO 库尔特·埃克特(Kurt Ekert)在第三季度财报电话会上说**“LLM 平台目前仍更专注于企业端而非消费者端的机会”**；Skift 转述埃克特的话**“消费者不会翻页浏览结果，而是会收到一个、两个、最多三个选项”**，并把 **ChatGPT·Claude·Gemini** 列为2027年的扩展对象(这三个名字出自 Skift 报道，新闻稿中没有)。Skift 的摘要中有埃克特“现在给旅行社的激励可能会转变为与 LLM 的收益分成形式”的想法，以及 Skift 的评价“经济性尚未得到证明，且大体上未被纳入多年期展望”，但这一段不在正文而在文章摘要块中，因此标为 **Skift 摘要·仅一处来源**。

## 4. 另一边 — “代理不会冲动消费”与“经 LLM 的预订远不及1%” (事实·媒体专栏·公司发言)

我们阅读了 Skift 创始人拉法特·阿里(Rafat Ali)的专栏 **“The AI Agent Is Travel's Ad Blocker”**(11月18日) — **前五段可读，之后是付费墙**，后半部分我们只通过文章的摘要块读到。可读正文的要点如下：旅游公司的收益来自结账环节的冲动消费(好座位·客房升级)，而**代旅行者预订的代理不会冲动消费** — 因此追加销售(upsell)的利润面临风险。酒店连锁 MCR 的 CEO 泰勒·莫尔斯本月初在 Skift 商务峰会上说出了这一担忧，据摘要块，他表示**“人会被促销打动，但代理不会”，因此想阻止自己酒店的代理预订**。分析机构 Citizens 11月15日的报告用两个代理(Instinct·Meta Muse)测试了预订，称“并不令人印象深刻”，但仍认为在线旅行社面临较大的长期风险，并把曝光排序写为 Expedia·Booking Holdings·爱彼迎(最少)(Skift 转述·方法未经确认)。

仅见于摘要块的数字标为 **Skift 摘要·仅一处来源** — 航空附加收入2025年1,570亿美元·约占总收入16%(2016年为674亿·9.1%，IdeaWorksCompany 估算)，Expedia 第三季度广告收入2亿600万美元，爱彼迎 CEO 的“广告10亿美元机会”发言，Skift 问 Instinct“广告位置是否影响推荐”时得到的回答“位置不是我使用的信号”，**Booking Holdings 称经 LLM 的预订在全部间夜中“远不及1%”**，以及**温德姆(Wyndham)称自家 AI 电话客服以比公示价格平均高15%的价格完成预订**(专栏作为“代理也能卖”的例子举出)。摘要中还提到，美联航的代理限制(NO.45)于同一天发布，理由不是营收而是“安全·监管风险”。

## 简短两条 (事实·公司发布)

- **谷歌“把其他 AI 应用的记录迁移到 Gemini”**(11月19日) — 分五步：在 Gemini 的导入设置中复制提示词 → 粘贴到之前的 AI 工具中获取偏好摘要 → 把该回答粘贴到 Gemini → 在之前的提供商账户中导出对话记录 ZIP → 上传到 Gemini 设置。支持哪些提供商、容量上限、资费方案、保存条件，文中没有。这是**“换乘之门”** — NO.48“换一个模型要花几周”的消费者版。
- **谷歌 Gemini API“Tool Retrieval”**(11月19日，预览版) — 当代理挂载数十、数百个工具时，不必每次发送所有工具的参数规范，而只保留名称·说明，需要时再调取规范的功能(`tool_search` 工具 + 对要延后的工具加 `defer_loading`)。也可以延迟加载整个远程 MCP 服务器，没有额外计费(调取的规范随后按输入 token 计费)，**节省数据文中没有，写的是“用自己的流量去测量”**。这与第1条的 Connected Apps 通过 MCP 对接处于同一位置 — 是商家推出的“工具”变多时的技术。

## 四条放在一起读 (解读)

第一，**门分成了四种 — 直接对接、允许浏览、结算移交、禁止。** 在 NO.45 写成“挡住顾客的代理、请进商家”的两者之间，Vayo 写下了两道中间门。“允许浏览”是代理像人一样在商家网站上走动并完成预订，“结算移交”是代理**把价格确认等一切做完，只把最后的结账按钮留给顾客按**。重要的是，**即便通过“结算移交”这道门，代理也会来到我们结算页的门前** — 商家什么都不决定，代理也能读取网站、装满购物车、把顾客带到结算页前。所以不存在“我们商家与代理无关”这个选项，**剩下的只是决定是四种门中的哪一种。** 我们也记下美联航(安全·监管)与 MCR(追加销售)选择“禁止”的理由并不相同 — 禁止也有两种理由。

第二，**门把手是规格，小商家不是选规格的一方，而是跟随的一方。** 谷歌的杂货购物结账建在 UCP 之上，Connected Apps 平台建在 MCP 之上，Sabre 的交易引擎也在 MCP 之上，Shopify 商家则在 poppy.json(NO.50)之上。看起来三种规格在竞争，但从商家一侧看，共同点更大 — **把商品、价格、库存、条件以机器可读的格式提供出来，写明“可以做的事”，支付由钱包(Stripe Link·Google Pay)代为承担。** Sabre 的“80家以上”是未区分试点和运营的数字(公司公布的数字)，谷歌的“50个以上”是应用数而非交易量。有几种规格能存活不是我们能决定的，但**把一页商品信息做准确**这件事，无论哪种规格胜出都需要 — NO.53 的“供代理阅读的一页商品信息”是本周最便宜的准备。

第三，**“只能看到一两个”改变了货架。** 埃克特所说的“消费者不会翻页，只收到一个、两个、三个”，意味着搜索广告时代“10个结果中排前列”的竞争，变成了**“是否进入代理的选择标准”的竞争**。而 Vayo 的 Genius Level 3 展示了**“代理渠道价格”这一新栏目** — 同一间房，人在网站上买的价格和代理代买的价格可能不同，而这种差异可能影响选择哪一家库存，这一点 Skift 也指出了。拉法特·阿里的“广告拦截器”论点在另一边 — 代理不会购买追加销售，所以结算页“再推一次”的收益可能减少。温德姆的“AI 电话客服卖得高15%”(Skift 摘要·仅一处来源)是专栏举出的反例，说明**商家一侧的代理能卖**。综合起来，商家要定两件事：**向顾客一侧的代理展示的价格·条件，以及我们一侧的代理要推荐什么。**

第四，**数字还很小 — 所以现在决定是便宜的。** Booking Holdings 的“远不及1%”(Skift 摘要·仅一处来源)、Skift Research 的“预订阶段6%”、埃克特的“LLM 平台目前仍在企业端”、Citizens 的“并不令人印象深刻”，再加上 NO.43 的爱彼迎“极其微小”·NO.40 的优步“最繁忙的一周4单” — 顾客一侧的代理真正走到结账的比例，按任何一家公司的数字都还在个位数以下。谷歌没有公布任何数字。所以本周要做的**不是对接开发，而是写下门的种类** — 不花钱，而且比代理多起来之后再改要便宜得多。而且，交出去的结算页若坏了(登录墙·过期的购物车·验证码)，按 Vayo 的规则**“已确认”只在供应商确认后才显示**，坏掉的结算页最终不是销售额，而是“未预订”。

## 如果是我们 — 运营电商·应用·AI 网红的团队本周要写的一页 (实践)

1. **一张门表 — 为我们的每个商品·服务写下四种之一。** Hangeul Cubs 的商品、CourtMate 的付费功能、Lia 频道的合作咨询、应用订阅 — 每一行写下**直接对接 / 允许浏览 / 结算移交 / 禁止**之一及理由(支付·退款风险、库存、监管)。默认值设为**“结算移交”** — 代理把购物车做好、结账按钮由人来按的流程。然后由人走一遍，**确认我们的结算页不会打断这个流程**：登录墙、过短的会话过期、验证码、购物车链接是否可共享。Vayo 的两条规则原样借用 — **订单必须有我们系统的确认才算“已确认”**，**批准按件进行**(与[NO.54](https://www.apholdings.kr/ko/news/agent-roster-and-incident-log/)“代理名册·事故日志”中的“涉及金钱的句子必须有出处”同一行)。选择“禁止”的行，写明理由是美联航式(安全)还是 MCR 式(追加销售)。
2. **门把手从一页商品信息开始 — 规格以后再选。** Shopify 商家已经有 poppy.json(NO.50)，谷歌 Connected Apps 控制台和 UCP 仅限美国，所以我们现在能做的是**让代理“确认价格”时不会卡住的信息** — 价格、库存、配送日期、退款条件、尺码规格放在一处，机器可读(结构化数据·商品 feed)，并且**网站两处不能出现不同价格。** Vayo 写明“确认价格后”再交出结算页，原因就在这里 — 不一致在代理那里以“不选”收场。Sabre 的“80家”·谷歌的“50个”不是我们决定的依据，只当作“有三种以上规格在运转”的信号来读。
3. **进入“只能看到一两个的货架”的两行条件，和一行代理渠道价格。** 当代理把选项缩减到一两个时，我们的商品要想进入，必须写有**可比较的条件**(配送日期·退款·总价) — Hangeul Cubs 套装、每篇篮球鞋推荐文章都加上这两行。然后像 Genius Level 3 那样，用一行决定**是否对经代理的订单设置不同的价格·条件**(我们的答案从“同一价格，无追加销售”开始 — 按拉法特·阿里的论点，结算页的“再来一次”对代理不起作用，所以不做追加销售，而是把套装组合本身作为商品)。Lia 的脚本用学习“代理替顾客做选择的时代”的语气，数字只以“reported”形式写入。在我们自身的 AI 使用方面，走一遍“换乘之门” — 试着导出对话记录，若有无法导出的知识，按 NO.48 的原则转移到模型之外的文档中。

## 本次未选的内容

OpenAI 首席科学家的 **“Perplexity and Intelligence”**(11月22日 — 公开内部困惑度数据并提出各研究所共同的“上限”建议)是本周最大的评测·安全消息，但与本文主题(商家的门)不同路，**将在下一篇另行处理**(NO.52·54 的后续，与 OpenAI 对齐·部署安全页面的检查一并)。NAVER AI Lab 的 **Unfinished-Bench**(“代理写下规则后又违反 89%”，AI Weekly 转述·arXiv 原文未阅)和 **SimAudit**(机器人基准评分器缺陷61处，转述)也是同一篇下一篇的材料。Lean·Mathlib 社区的**“黎曼猜想证明认证”**联合声明(11月21日)我们直接打开了，但**文中没有提及 AI 工具**，AI Weekly 标题中的“Claude 协助”未能确认，且涉及撰写本文的 AI 的制造商，故不写。Anthropic 上市完成·“承销商条件”(路透标题)·Next.ink 的上市报道属于投资，仅看标题。美国全国州长协会的“联邦 AI 规则·保留州法”声明(11月22日)是 NO.39 的后续候选。OVHcloud 的开放权重模型 Olala(Next.ink)是 NO.51 的后续候选。费加罗报–OpenAI 内容协议(Next.ink 标题)是 NO.42 的后续候选。谷歌 RSS 的 Watch Duty 山火警报·量子·清洁能源文章，以及加拿大网络安全中心的 Oracle Java 警报，不是 AI 消息或距离较远，已剔除。Learn:US 第42期(Claude 交易员技能)属于投资领域，仅看标题。Kayak 的28项 AI 功能(仅 Skift 标题)·Lola CEO 对 Muse 的批评(仅标题)·OpenAI 招聘 ChatGPT 旅游人员(仅摘录)未打开正文，故不写。11月20日的草稿(Olive Young“Define:Omni”·GPT-6.2 降价)尚未上线主页，故未链接。

## 本则消息中未能确认的内容

- 谷歌 Connected Apps 杂货购物结账为公司发布，没有价格、手续费、使用数据、确切上线日期。“基于 UCP”的说明文章(商务侧另一篇)和 Connected Apps 支持应用列表页面未打开。10月28日文章的“50个以上”是应用数，没有交易数据。Target 资料的“2,000%”是 Target 公布的第一季度数字，测量方法资料中没有；且为6月资料，11月的杂货购物结账流程(是否支持多件结算)无法由该资料确认。两家媒体(MediaPost·Search Engine Land)的相关报道未能打开。
- Vayo 新闻稿读的不是 PR Newswire 原文而是 finviz 转载本(有原文地址标注)。供应商名单·直接对接范围(Booking.com·OpenTable·SeatGeek)出自 Skift 报道，新闻稿中没有。预订件数·交出结算页的比例·Vayo 收费未公开。“1亿美元”出自 PhocusWire·Skift 两家媒体，新闻稿中没有，条件(产品进展·市场状况)是 PhocusWire 的表述。Skift Research 的27%·21%·6%是 Skift 自身调查，样本量文中没有。
- Sabre 新闻稿同样是 finviz 转载本。“80家以上”是未区分试点·运营的公司数字。“2027年扩展到 ChatGPT·Claude·Gemini”·“收益分成”·“经济性未证明”出自 Skift 报道(部分在摘要块)，新闻稿中除 Grok 外没有平台名称。新闻稿引语中出现“SpaceXSI”，但其角色没有说明，故未写。在 Sabre IR 网站打开的新闻稿是2025年9月的，未用于确认本次发布。
- Skift 专栏只打开了前五段，Booking Holdings“远低于1%”·温德姆“15%”·IdeaWorks 1,570亿·Expedia 2亿600万·Instinct 回答·美联航理由仅在**文章摘要块**中读到(未能与正文对照)。Citizens 报告的方法·样本未能确认。MCR CEO 发言为 Skift 转述。
- 谷歌记录迁移文章没有支持的提供商·上限·资费方案，Tool Retrieval 文章没有节省数据(公司写的是“自行测量”)。
- 任何一家公司的发布我们都没有直接测试过。我们的“门表”是本周开始做的，结算页走一遍的结果写在下一篇。

## 一并阅读的文章

我们直接打开并确认了性质不同的来源。分为公司发布·官方文档、媒体报道·专栏、我们之前的文章三类。

公司发布·官方文档：

- [Get your year-end tasks done with new Connected Apps (Google, 11月20日)](https://blog.google/products-and-platforms/products/search/connected-apps-holiday-errands/) — 英文，Albertsons·Safeway·Shaw's·Target 杂货购物结账·UCP·Experian·H&R Block·Angi·Thumbtack·无数字
- [Build and manage Connected Apps in one place (Google, 10月28日)](https://blog.google/innovation-and-ai/technology/developers-tools/connected-apps-one-place/) — 英文，Connected Apps Platform 预览版·MCP 服务器/Android MCP·Connected Console·50个以上
- [How to transfer your chat history into Gemini (Google, 11月19日)](https://blog.google/innovation-and-ai/products/gemini-app/switch-ai-assistants-transfer-history/) — 英文，5步·ZIP 导入
- [Introducing Tool Retrieval in the Gemini API (Google, 11月19日)](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/) — 英文，tool_search·defer_loading·远程 MCP 延迟加载·无额外计费·无节省数据
- [How Target is Shaping Shopping Experiences in Conversational AI (Target, 6月18日更新)](https://corporate.target.com/press/fact-sheet/2026/06/conversational-ai) — 英文，三平台结账·UCP·Buy→登录→确认·Google Pay·“多件结算准备中”·AI 流量2,000%(公司)
- [Booking Holdings' Vayo Now Books the Entire Trip (Vayo 新闻稿, 11月17日 — PR Newswire, finviz 转载)](https://finviz.com/news/424035/booking-holdings-vayo-now-books-the-entire-trip) — 英文，对接/浏览/结算移交·批准·供应商确认·1Password for Agents·Stripe Link·Genius Level 3 最高20%·非公开测试
- [Sabre Accelerates Agentic Travel Leadership with First-Mover Travel Experience within Grok Bot and Next-Gen Proactive Travel APIs (Sabre 新闻稿, 11月16日 — PR Newswire, finviz 转载)](https://finviz.com/news/423683/sabre-accelerates-agentic-travel-leadership-with-first-mover-travel-experience-within-grok-bot-and-next-gen-proactive-travel-apis) — 英文，Mosaic Travel Connector 测试·Grok Bot 首个插件·MCP 合作方80家以上·事件驱动 API·2027扩展·无费用

媒体报道·专栏：

- [Booking Holdings' AI Agent Vayo Can Now Reserve Flights and Hotels (Skift, 11月17日)](https://skift.com/2026/11/17/booking-holdings-ai-agent-vayo-can-now-reserve-flights-and-hotels/) — 英文，直接对接 Booking.com·OpenTable·SeatGeek·Skift Research 27%/21%/6%·Genius 价格对比较的影响
- [AI agent Vayo adds travel booking (PhocusWire, 11月)](https://www.phocuswire.com/news/startups/ai-agent-vayo-adds-travel-booking) — 英文，1亿美元投资条件·Lola·CEO“像美联航那样不允许的地方就交出结算页”
- [Sabre Wants to Be the Transaction Engine Behind AI Travel Bookings (Skift, 11月19日)](https://skift.com/2026/11/19/sabre-wants-to-be-the-transaction-engine-behind-ai-travel-bookings/) — 英文，CEO“一个·两个·三个”·ChatGPT·Claude·Gemini 2027·收益分成(摘要块)·经济性未证明
- [Sabre brings conversational travel booking to Grok (PhocusWire, 11月)](https://www.phocuswire.com/sabre-brings-conversational-travel-booking-grok) — 英文，投资者日11/17·CEO“LLM 平台目前仍在企业端”
- [The AI Agent Is Travel's Ad Blocker (Skift, 拉法特·阿里专栏, 11月18日 — 仅前半部分免费)](https://skift.com/2026/11/18/the-ai-agent-is-travels-ad-blocker/) — 英文，冲动消费·MCR CEO·Citizens 11/15·Booking“远低于1%”·温德姆15%(摘要块)
- [Google Brings Third-Party Apps Into Search AI Mode for Everyday Tasks (eWeek, 7月17日)](https://eweek.com/news/google-ai-mode-connected-apps) — 英文，7月第一批 Connected Apps(Instacart·Canva·YouTube Music)·美国·选择加入

我们之前的文章：

- [AI 周报 — 价格下降、写明局限，代理走进桌面与购物车 (AP News NO.53)](https://www.apholdings.kr/ko/news/weekly-2026-11-21/)
- [在代理到来之前写下“可以做的事”的三份文档 (AP News NO.50)](https://www.apholdings.kr/ko/news/allowed-list-before-the-agent-arrives/)
- [换一个模型要花几周 (AP News NO.48)](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [AI 周报 — 谷歌五天内换了三个模型和搜索，OpenAI 把钱包交到代理手上，美联航把“顾客的代理”挡在门外 (AP News NO.47)](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [挡住顾客的代理，请进商家，模型给所有人 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [顾客带不来自己的代理 (AP News NO.43)](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [计分表上加了概率 — 优步统计最繁忙的一周代理完成的叫车只有4单 (AP News NO.40)](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [AI 带来顾客的门厅变成了三个 (AP News NO.38)](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
- [当确认码落入代理之手 (AP News NO.36)](https://www.apholdings.kr/ko/news/agents-raised-their-own-spending-caps/)
