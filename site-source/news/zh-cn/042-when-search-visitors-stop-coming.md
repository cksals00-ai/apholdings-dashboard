---
no: 42
slug: when-search-visitors-stop-coming
date: 2026-11-08
category: 洞察
tags: 搜索流量 · AI 概览 · 出版商业绩 · 亚马逊 Shop Direct · AI 购物代理 · 机器人防护 · robots.txt
title: 从搜索来的客人正在减少 — Ziff Davis 说“谷歌流量下降 37%，AI 引用是点击的 10 倍”，People Inc. 说“会话减少了 26%，收入只减少了 6%”，亚马逊开始把外部店铺免费放进自己的搜索
summary: 本周出现了三组计算“客人从哪里来”的数字。Ziff Davis（CNET·IGN·PCMag）在 11 月 6 日的业绩电话会上表示，第三季度来自谷歌的自然流量同比减少约 37%，同期自家文章在谷歌 AI 概览和 AI 模式中被引用约 27 亿次，约为搜索点击量的 10 倍。People Inc.（PEOPLE·Allrecipes·Investopedia）在 11 月 2 日的业绩中写道，核心会话从 21.7 亿降至 16.1 亿、减少 26%，而依赖会话的收入只减少了 6%，并把原因归于“面向 AI 的搜索与内容发现体验”。11 月 4 日，亚马逊开放了一个门户，不在亚马逊上销售的店铺只要接入商品目录，就能免费出现在亚马逊搜索和 Alexa 购物中；同一周，一项用自动化浏览器走访英美 200 家店铺的调查发现，每 7 家中有 1 家把进来的路堵住了，而这些店铺的 robots.txt 全都允许 AI 爬虫。我们整理了这三组数字的算法，以及运营应用和电商的小团队该在自己的表格里填哪些格。
---
> 本文与 AI（Claude）共同撰写，并经编辑审校。我们公司是 Claude 的开发者 Anthropic 以及 OpenAI 的付费客户，直接运营应用、电商和 AI 渠道。今天文章第 1 节出现的 Ziff Davis 正在与 OpenAI 进行版权诉讼，People Inc. 与 OpenAI、Meta、微软签有内容授权协议。第 3 节调查的 robots.txt 项目中，Anthropic 的爬虫（Claude）被列为“被允许的爬虫”。做该调查的 Blend Commerce 是一家 Shopify 专业代理机构，并自行披露了利益关系。公司发布的数字标注为“公司发布”，只有单一来源的内容一并注明了来源。文中出现三家上市公司（Ziff Davis·People Inc.·Cloudflare）的季度业绩，但这不是对特定企业的投资意见，也不是投资判断依据。

我们在 NO.38 中写过“AI 带客人进门的门廊变成了三个”。那是 ChatGPT 开始接收搜索型提问、AI 在 Shopify 店铺下单、苹果把 Siri 开放给应用的消息。本周的消息是它的背面。原本作为门廊的**搜索**带来的客人减少了多少，两家出版商用季度数字写了出来；**亚马逊**开始把外部店铺请进自己的搜索这个门廊；而在店铺一侧，一项调查发现，**AI 购物代理**进来的门之所以关着，不是因为政策，而是因为默认设置。我们在 NO.25 读过份额、在 NO.35 读过“实际做了什么”、在 NO.37 读过 robots.txt 的一行，这次接着往下读。分为事实、解读、换作我们三部分。

## 1. 两家出版商的第三季度 — 流量在减，引用在增（事实）

**Ziff Davis** 于 11 月 5 日发布第三季度业绩，11 月 6 日召开业绩电话会。CEO Vivek Shah 在电话会上说的数字（公司发布）如下。流入 CNET·IGN·PCMag 等自家网站的**谷歌自然流量同比减少约 37%**，一年前同一季度的降幅约为 23%，两年累计减少超过一半。同一季度，自家内容在谷歌 **AI 概览和 AI 模式的回答中被引用约 27 亿次**，据称这约为在谷歌搜索中获得的**点击量的 10 倍**。公司表示这一数字取自 Google Search Console，但没有公开点击的绝对值（PPC Land 简单反推为约 2.7 亿次点击，我们不采用这一反推）。营收为 2.893 亿美元，下降 5.6%；广告与效果营销营收为 1.86 亿美元，下降 7.7%。Shah 表示**“不打算规划搜索流量的恢复”**，即以流量持续减少为前提运营；对 AI 方面的内容授权协议持开放态度，并认为与 OpenAI 的诉讼（2025 年 4 月提起）将厘清这一领域。公司内部的数字也有。产品与工程团队的**拉取请求 90% 以上由 AI 编写**，预计到年底人员将减少 10%，同时补充说“并非全是因为 AI”。我们未能打开公司的新闻稿、公告和电话会记录原文，上述数字只搬运了整理该电话会的三家媒体（PPC Land·Stock Observer·Motley Fool）一致的部分。

**People Inc.**（原 IAC·Dotdash Meredith）于 11 月 2 日发布第三季度业绩，11 月 3 日召开电话会。以下是我们直接打开的公司新闻稿中的数字。**核心会话 21.68 亿 → 16.13 亿（−26%）**，总会话 23.77 亿 → 17.94 亿（−25%）。新闻稿把会话减少的原因写为**“主要是面向 AI 的搜索与内容发现体验”**，并称基于会话的收入“受其影响在季度内加速”、减少了 6%。同日投资者说明材料第 5 页写着“核心会话降幅加速至 26%，谷歌搜索减少 22%，AIO 渗透率 82%”（AIO 没有缩写解释，可读作 AI 概览）。电话会上，CFO Tim Quinn 表示公司追踪的搜索中**超过 90% 会出现 AI 概览**，CEO Neil Vogel 表示**“失去了近 70% 的谷歌搜索流量”**（PPC Land 写为“过去几年间”，AdExchanger 写为“两年间”，期间表述不一致）。但收入朝相反方向移动。数字营收为 2.885 亿美元，**增长 2%**，连续 12 个季度增长；广告为 1.619 亿（−8%）有所减少，但效果营销为 7,390 万（+2%），**授权及其他为 5,270 万（+49%）**，均有增长。授权增长的主要动力是 Apple News+ 等分发合作伙伴以及 2025 年第四季度签订的 Meta 内容协议，新闻稿写明这一项目包含“利用大型语言模型等 AI 相关活动”。不需要会话的**非会话收入占数字营收的 43%**（一年前为 39%）。Vogel 的一句话概括了这个季度。**“会话减少了 26%，但收入只减少了 6%。”**公司于 10 月 29 日裁员 195 人（约 6%），Quinn 表示“不期待会话会好转”。Vogel 在电话会上还提到公司内部造出并使用了“谷歌归零”这个说法（两家媒体）。

同一周其他出版商的数字只有 PPC Land 一家的整理，因此不写进正文。只记下一条单一来源的转述：广告平台 Teads 的 CEO 称“AI 摘要把出版商页面浏览量削减了 20~60%”。

## 2. 亚马逊 — 请进外部店铺，挡住外部代理（事实）

亚马逊于 11 月 4 日开放了 **Shop Direct Merchant Workspace**（Amazon News，公司发布）。这是一个免费的自助门户，店铺即使不在亚马逊上卖东西，只要接入自己的商品目录，商品就会**出现在亚马逊搜索结果和 Alexa 购物中**。注册分三步：创建卖家账户、验证自己的网站、共享商品目录。目录可以通过 Feedonomics、Salsify、CEDCommerce、VersaFeed 等 feed 服务商接入，或通过亚马逊的 Selling Partner API 直接导入，并且原样接受现有的购物 feed 格式。顾客看到商品上的“Shop Direct”标识后，可以前往该店铺网站，或者通过亚马逊的代理式购买功能 **Buy for Me**，让亚马逊 AI 代为在该店铺网站上完成结账（在顾客确认订单内容之后）。参与**免费**，放入哪些商品由店铺选择，**随时可以退出**，价格、库存、配送、退货、客服均由店铺按原有方式处理。覆盖对象是**全体美国顾客**（Amazon.com·应用·移动网页·Alexa）。公司写出的规模是“自去年推出以来，数千万顾客发现了其他店铺的数亿件商品”、“Shop Direct 商品每月出现在数亿次搜索中”，但没有“数千万”“数亿”的定义，也没有参与店铺的数量。资格标准、**Shop Direct 商品如何与付费卖家的商品混合排序、能否投放广告，发布中都没有提及。**亚马逊核心购物业务副总裁 Amanda Doerr 的话是“让店铺把自己的商品呈现给亚马逊顾客这件事变得简单”。

还有另一侧的门。PPC Land 在同一篇文章中整理道，亚马逊**一直在限制进入自家店铺的外部 AI 代理**。举的例子是针对 Perplexity 的诉讼以及今年 9 月对 Meta Muse 代理的屏蔽，但这两件事的原文我们这次没有打开（媒体整理）。亚马逊 3 月曾称通过 Shop Direct 展示“超过 40 万家店铺的 1 亿多件商品”，这也只是 PPC Land 一家的记录。

## 3. 每七家店铺中有一家在“不知情”地挡住 AI 购物代理（事实）

我们直接阅读了 Shopify 转化率代理机构 Blend Commerce 于 10 月 6 日发布的**“AI 购物审计 2026”**（作者为 CEO Adam Pearce）。调查于 9 月 8~15 日走访了 200 家零售商：英国 100 家、美国 100 家，20 个行业各 10 家（每个国家大型 2·中型 2·新兴 1）。使用的工具是**未经改动的 Chromium 浏览器和普通 HTTP 请求**，没有冒充特定 AI 公司的代理，请求从店铺所在国家的家庭宽带发出。被拒绝两次（第二次使用新连接）才计为“拒绝”，没有购买商品（购物车只到结账页面为止）。检查分四层 17 个项目，满分 100 分：能否触达（网站是否打得开）、能否找到（robots.txt 是否允许爬虫·是否有商品站点地图）、能否理解（商品 schema 中是否有价格·库存·GTIN·配送·退货）、能否交易（面向代理的结账端点·访客结账·快捷结账）。

结果（调查机构发布）如下。平均 **65 分**。按行业看，婴童用品最高为 88 分，时尚最低为 49 分。**200 家中有 29 家（约每 7 家中 1 家）两次都拒绝了浏览器**，被点名的有 Home Depot、Best Buy、Macy's、Tesco、Argos、Next。拒绝率为**大型 20%（80 家中 16 家）、中型 15%（80 家中 12 家）、新兴 2.5%（40 家中 1 家）**，规模越大挡得越多。Saks Fifth Avenue、Bergdorf Goodman、Anthropologie、JD Williams 四家连首页和 robots.txt 请求都全部拒绝，得 0 分。关键是下面这句话。在拒绝的 29 家中，能读到 robots.txt 的 **24 家全部允许 ChatGPT、Perplexity、Claude 的搜索爬虫**。因此报告认为拒绝的原因**不是要挡住 AI 的政策，而是机器人防护软件**。Pearce 的话是“这些店铺中的大多数大概已经告诉 AI 公司，它们的代理是受欢迎的”。在能读到商品页面的 171 家中，82% 具备商品 schema，但**配送信息只有 22%、退货政策 20%、GTIN 条码 18%**；商品站点地图 200 家中只有 107 家有。面向代理的结账端点处于可用状态的是 **200 家中的 38 家**，其中 37 家是 Shopify。37 家 Shopify 店铺的平均分为 91 分，其余为 59 分，而作者写明**自己是 Shopify 代理机构，对这一结果存在利益关系**。局限也写了：每个行业 10 家是小样本，英国和美国的线路类型不同，而且只是 9 月某一周的快照。我们要补充的局限还有一条。这项调查被挡住的不是“AI 代理”，而是**自动化的普通浏览器**，因此“挡住了 AI 购物代理”和“挡住了自动化浏览器”在这项调查中无法区分。

## 简讯 — Cloudflare“机器人扫过数百家，只回报一家”

Cloudflare 于 11 月 5 日在第三季度业绩（8-K 公告）中写下营收 7.825 亿美元（+39%），并在前瞻性陈述中提到“代理式 AI 优先的运营模式”和裁员。公告中没有关于机器人和爬虫的内容。CEO Matthew Prince 的发言只在 Techzine 一家看到：机器人扫过数百个网站，**只对其中一家以 AI 回答中的提及或商品推荐作为回报**，所以大多数网站从机器人访问中一无所获；7 月 1 日以来**约 5% 的网络**加入了该公司的内容保护产品（Meta 是客户）；屏蔽 AI 机器人免费，向爬虫收取访问费的 Pay per Crawl 处于非公开测试阶段。报道中没有说明发言的场合，因此仅作为**单一媒体的转述**保留。

## 把三组数字放在一起读（解读）

第一，**“曝光”和“访问”成了不同的数字。**Ziff Davis 的 27 亿次引用是点击的 10 倍。我们在 NO.38 数了 AI 带客人进门的三个门廊，而本季度的数字说明，AI 门廊**引用**文章，却不**带来**客人。People Inc. 展示的是接下来的一步：会话减少 26%，收入只减少 6%，授权增长 49%，非会话收入占到 43%。这是一个靠**每次访问的价值**和**不需要访问的收入**撑住的季度（解读）。“我们的文章在 AI 回答中被引用了多少次”不再是值得炫耀的数字，而是用来数有多少引用没有转化为访问的数字。

第二，**亚马逊的门有两扇。**在自己的搜索这个门廊，免费请进外部店铺；在自己的店铺这个门廊，挡住外部代理。NO.38 写过“锁握在平台手里”，这次又多看见一串钥匙。店铺得到的是曝光，亚马逊得到的是**顾客的搜索与购买流程，以及由 Buy for Me 完成的结账页面**。“免费”的代价不在手续费那一格，而在**空着的格子**里（排序标准·广告混入·资格标准）（解读）。我们把商品目录交给任何平台时该问的，正是那些空格。

第三，**挡住的不是政策，而是默认设置。**NO.37 说过，robots.txt 的一行要分开看“写了”和“被遵守了”。这次的调查是一面镜子。在 robots.txt 中写明“允许”AI 爬虫的 24 家，实际上挡住了自动化浏览器。“允许了”和**“实际进来了”**也要分开看（解读）。如果 Cloudflare 所说的“5% 的网络加入保护产品”属实，那么挡住一侧的默认设置还在增加。大型店铺挡住 20%、新兴店铺挡住 2.5% 的分布，既可能意味着越小的店铺越判断敞开门更有利，也可能意味着它们没买用来挡的软件。无论哪一种，像我们这样的团队要做的决定不是“挡不挡”，而是**“以什么条件放谁进来”**。

## 换作我们 — 运营应用·电商·AI 渠道的团队本周要做的三件事（实践）

1. **把流量表分成“搜索流量 / AI 引用曝光 / 直接访问”三行。**在官网（apholdings.kr）和电商的 Search Console 中记录按季度的谷歌点击趋势，并确认能否像 Ziff Davis 那样单独看到 AI 概览和 AI 模式的曝光（那家公司说是在 Search Console 里看到的，但我们的账户里这一区分如何呈现还没有确认）。然后按 People Inc. 的方式，把我们的收入分为**基于会话**（像电商营收那样必须有访问才产生的）和**非会话**（像应用订阅、联盟、授权那样没有访问也产生的），留出一格比例。理由与 NO.25 提出给份额数字附上测量方式相同。本周只填过去四个季度的数值。
2. **用 Blend 的四层直接检查我们的电商（不花钱）。**①用自动化的普通 Chromium 打开我们的商品页面，看机器人防护是否会拦 ②重新打开 robots.txt（连同 NO.37 中推迟的“三组决策表”）③数一数商品 schema 中是否有价格·库存·GTIN·配送·退货五个项目（调查中最空的三格是配送·退货·GTIN）④看访客结账和快捷结账能否在商品页面上完成。结果不记为“开/关”，而是记为**“在哪一层被挡住”**。如果被挡住了，不是去关掉机器人防护，而是朝着建立**允许名单**的方向走。我们属于新兴店铺一侧，按调查的分布来看，敞开门是对的。
3. **做一张“平台拿走我们商品目录的条件”六格表。**Shop Direct 仅限美国，不是我们的对象，但当 Shopify 的“默认代理就绪”（NO.38）或国内平台提出同样要求时，这张表就用得上。六格是**手续费 · 能否退出 · 排序标准是否公开 · 是否与广告混合 · 顾客数据归谁 · 结账在谁的页面上完成**。把亚马逊的发布填进这张表，前两格填上“免费·随时”，后四格是空的，而那些空格就是我们要问的问题。表中设“公司发布 / 我们确认的”两行，与 NO.34 时相同。

## 这次没有选的

Next.ink 报道，谷歌在 11 月 3~4 日夜间通过人工处置把法国 9 家 AI 生成新闻网站从 Discover 中移除（“大规模垃圾内容·伪装”邮件，这 9 家约占法国 Discover 文章的 2%）。监测机构 1492.vision 在 X 上的帖子是唯一的交叉来源，且报道后半部分为付费内容，留作下一篇的素材。Techzine 的 Kiro 自主构建、谷歌云安全代理的新控制措施（Help Net Security，NO.29·39 后续候选）、“99% 的仓库令牌永不过期”（BlueFlag 自有调查）、已废弃 MCP 服务器的安装问题（NO.32 后续候选），均未打开原文。AI Weekly 11 月 5 日刊“AI 对话是证据”、英格兰银行的“AI 占英国增长的五分之一”、Next.ink 的“欧洲法律将禁止聊天机器人转载付费文章”·“NYT 起诉 Brave”也只看了标题。OpenAI 的采购报道（SiliconANGLE）和 Palo Alto 收购 Clutch（Techzine）属于投资判断材料，不采用。USA Today、News Corp、BuzzFeed、Yelp 的季度数据只有 PPC Land 一家的整理，故剔除。GPT-6 Cyber 和 Linux 内核 948 件的报道（Techzine·Help Net Security）已在 NO.41 中讨论。

## 这则消息中未能确认的

- 未能打开 Ziff Davis 的新闻稿、公告和电话会记录原文。37%·27 亿次·“点击的 10 倍”·PR 90%·人员 10% 是整理该电话会的三家媒体一致的数字，点击绝对值公司未公开。一年前的 23% 来自两家媒体。Teads CEO 的“20~60%”只有 PPC Land 一家。
- People Inc. 的新闻稿和投资者材料我们直接读了，但没有读电话会记录。Quinn 的“90% 以上”和 Vogel 的“近 70%”由两家媒体转述，但 70% 的期间表述（几年/两年）不一致。“AIO 82%”的缩写解释和测量标准材料中没有，按季度的会话降幅（第一季度 −17%·第二季度 −22%）和每会话收入上升是 PPC Land 的整理与估算。
- 亚马逊的发布中没有资格标准、排序和广告条件。“不在亚马逊上销售的店铺”为对象这一表述是 PPC Land 的整理，官方文章对现有卖家另行以邮件通知。Perplexity 诉讼·Muse 屏蔽·3 月数字（40 万家店铺·1 亿件商品）是 PPC Land 一家的整理，未打开原文。
- Blend 的调查是 Shopify 代理机构的自有调查，拒绝的 29 家中有 5 家读不到 robots.txt，只确认了 24 家，而且被挡住的不是“AI 代理”而是自动化的普通浏览器，这是调查设计上的局限。
- Cloudflare CEO 的发言场合和“5% 的网络”只有 Techzine 一家。公告中没有相关内容。

## 一同阅读的文章

我们直接打开并确认了性质不同的来源。分为公司发布·公告、调查报告、媒体报道、我们之前的文章。

公司发布·公告：

- [People Incorporated Reports Q3 2026 Results（公司新闻稿，11 月 2 日）](https://ir.people-incorporated.com/static-files/4a7cd671-caaf-4f4a-b64b-95a69cc95e61) — 英文 PDF，核心会话 −26%·原因表述·分项营收数字
- [People Incorporated Q3 2026 Investor Presentation（11 月 2 日）](https://ir.people-incorporated.com/static-files/015c35ab-2f0a-4f21-a48c-abbd092f723f) — 英文 PDF，第 5 页“谷歌搜索减少 22%·AIO 渗透率 82%”
- [Amazon Shop Direct Merchant Workspace（Amazon News，11 月 4 日）](https://www.aboutamazon.com/news/retail/amazon-shop-direct-merchant-workspace) — 英文，免费·三步·Buy for Me·全美（公司发布）
- [Cloudflare Announces Third Quarter Fiscal 2026 Financial Results（8-K Exhibit 99.1，11 月 5 日）](https://www.sec.gov/Archives/edgar/data/0001477333/000147733326000060/q326exhibit991.htm) — 英文，营收·“代理式 AI 优先的运营模式”表述（公告）

调查报告：

- [AI Shopping Audit 2026（Blend Commerce，10 月 6 日）](https://blendcommerce.com/blogs/shopify/ai-shopping-audit-2026) — 英文，方法·17 个项目·结果·利益关系披露·局限

媒体报道：

- [Ziff Davis loses 37% of Google traffic as publishers count the AI bill（PPC Land，11 月 7 日）](https://ppc.land/ziff-davis-loses-37-of-google-traffic-as-publishers-count-the-ai-bill/) — 英文，多家出版商第三季度数字整理
- [Ziff Davis loses 37% of its Google search traffic in a year（PPC Land，11 月 6 日）](https://ppc.land/ziff-davis-loses-37-of-its-google-search-traffic-in-a-year/) — 英文，CEO Shah 发言·27 亿次·Search Console
- [Ziff Davis Q3 Earnings Call Highlights（Stock Observer，11 月 6 日）](https://www.thestockobserver.com/2026/11/06/ziff-davis-q3-earnings-call-highlights.html) — 英文，同一电话会的第二份整理（交叉确认）
- [Ziff Davis: 3 Key Takeaways for Long-Term Investors（Motley Fool，11 月 7 日）](https://www.fool.com/earnings/takeaways/2026/11/07/ziff-davis-3-key-takeaways-for-long-term-investors/) — 英文，CEO Shah 直接引语（用于核对引语，投资意见部分未采用）
- [People Inc. loses 26% of core web sessions as Google AI Overviews spread（PPC Land，11 月 6 日）](https://ppc.land/people-inc-loses-26-of-core-web-sessions-as-google-ai-overviews-spread/) — 英文，电话会发言·季度趋势·每会话收入估算
- [With Search Traffic Down 70%, People Inc. Bets On Revenue Beyond Site Visits（AdExchanger，11 月 3 日）](https://www.adexchanger.com/publishers/with-search-traffic-down-70-people-inc-bets-on-revenue-beyond-site-visits/) — 英文，同一电话会的第二份整理（交叉确认）
- [Amazon opens its search to outside stores as bots block AI shoppers（PPC Land，11 月 6 日）](https://ppc.land/amazon-opens-its-search-to-outside-stores-as-bots-block-ai-shoppers/) — 英文，Shop Direct·Blend 调查·亚马逊对外部代理的限制整理
- [Cloudflare CEO: Most websites are suffering from AI agents（Techzine，11 月 6 日）](https://www.techzine.eu/news/infrastructure/145614/cloudflare-ceo-most-websites-are-suffering-from-ai-agents/) — 英文，Prince 发言·5% 的网络（单一来源）

我们之前的文章：

- [AI 带客人进门的门廊变成了三个（AP News NO.38）](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
- [用 robots.txt 的一行说“不要用于 AI 训练”（AP News NO.37）](https://www.apholdings.kr/ko/news/one-robots-line-against-ai-training/)
- [计算 AI 实际在做什么的三组数字（AP News NO.35）](https://www.apholdings.kr/ko/news/what-ai-actually-does-three-counts/)
- [ChatGPT 网页份额再次上升 — 这个数字没有算进去的东西（AP News NO.25）](https://www.apholdings.kr/ko/news/chatgpt-share-rebound-what-web-misses/)
- [每周 AI 新闻 — Mistral 放下了 1 万亿参数（AP News NO.34）](https://www.apholdings.kr/ko/news/weekly-2026-10-31/)
