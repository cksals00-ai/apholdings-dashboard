---
no: 45
slug: united-blocks-agents-chatgpt-opens-storefronts
date: 2026-11-12
category: 洞察
tags: AI 智能体 · 美国联合航空 · 智能体商务 · ChatGPT · OpenAI · Gemini 4 Carbon · 谷歌 · Epoch AI · 模型选择
title: 拦下顾客的智能体，把店铺请进来，把模型开放给所有人 — 美联航宣布「禁止个人 AI 智能体订票」，OpenAI 同一天让商家把自己的智能体放进 ChatGPT，谷歌则把原本「先给少数人」的 Gemini 4 Carbon 开放给所有付费用户
summary: 11 月 11 日，美国联合航空宣布将在自家网站·应用以及旅行社·比价网站渠道上，拦下「未经授权的第三方个人 AI 智能体」的订票。理由是凭证泄露、意外购买与里程使用，以及「值机时必须由人确认行李中没有违禁物品」的航空规定。前一天，OpenAI 推出「Businesses in ChatGPT」测试版，让美国电商·在线服务商家把自己的智能体放进 ChatGPT，并查看自家店铺被 ChatGPT 提及和点击了多少次（尚无结账功能）。同一天，谷歌把两周前只给网络防御者的 Gemini 4 Carbon 开放给付费开发者·企业和 Ultra 订阅用户，11 月 30 日前与 Argon 同价。文末「简短一则」记录了独立评估机构 Epoch AI 给 Claude Fable 5.2 打的分数 — 那是撰写本文的 AI 的制造商的模型，因此我们申明利害关系，只转述数字与附加条件。
---
> 本文由 AI（Claude）协助撰写，并经编辑审核。我们公司是 Anthropic 和 OpenAI 两家公司的付费客户，第 2 项是 OpenAI 的发布，第 3 项是谷歌的发布。文末的「简短一则」是**独立评估机构给撰写本文的 AI 的制造商（Anthropic）的模型打的分数**，因此我们不加评价，只转述数字、区间和附加条件。公司发布的数据均标注为「公司发布」。美联航、达美等上市公司的业绩·股价以及 Anthropic 上市路演的报道属于投资判断材料，未予采用；本文不是对任何特定公司的投资意见。

在NO.43 中我们写过「顾客带不进自己的智能体」。亚马逊拦下了 Meta 的智能体并推出短信版 Alexa，爱彼迎说「外部智能体的预订极其微小」，并承诺 2027 年推出自己的智能体。本周，同一扇门**朝三个方向**动了。航空公司拦下顾客的智能体，ChatGPT 把店铺的智能体请进自己内部，谷歌则把最强的模型开放给所有付费的人。我们分事实·解读·如果是我们来写。

## 1. 美联航 — 禁止「未经授权的个人 AI 智能体」订票（事实）

美国联合航空于 11 月 11 日（周三）发表声明，公布了**「禁止未经授权的第三方个人 AI 智能体或助手使用」**的措施。Skift·PYOK·AirlineGeeks 三家媒体转述了同一份声明，我们没有找到美联航刊登声明原文的页面。范围有两层。在**自家网站·应用**上直接拦截，并与**在线旅行社（OTA）·比价网站**合作，在那些渠道也拦截对自家数据的访问。声明称为此「包括更新预订、出票和分销政策」，并将更新自家的「Digital Trust Center」页面以说明限制内容。三家媒体都没有生效日期和被拦截智能体的名称。

理由有三。第一，把账户凭证分享给第三方助手**可能暴露敏感信息。**第二，智能体的行为可能引发**意外购买、账户变更或里程（MileagePlus）的使用。**第三，「自动化的 AI 行为有可能违反 FAA·DOT 的规定」— 举的例子是**「航班值机需要由人确认行李中没有炸药等违禁物品」**这一项。声明称这一立场与银行·零售企业一致，并建议其他企业采取同样措施。Skift 称这是美国航空公司中首次明确表态；PYOK 补充了达美已在先行类似拦截的转述。两家媒体的「首家」「第二家」互相不一致。

背景从 10 月起就在累积。据 TechCrunch 10 月 6 日的整理，美联航当时已指向使用条款中**「不得使用机器人、爬虫、其他自动装置或人工流程监视或复制本网站」**的条款，但没有回答是否拦截特定智能体。达美说「没有允许第三方智能体订票的合作，若要开放会在考虑安全与顾客体验的前提下开放」，用户则贴出了被拒的案例。同一篇文章里，沃尔玛说 Meta Muse 用户被真人验证环节拦下**并非有意**（沃尔玛是 Muse 的合作方），eBay 说「不是拦截所有购物智能体，只拦未授权的智能体和抓取」，Yelp 说「只向购买了数据许可的运营者开放」。Meta 的话是**「把个人智能体赶走，就是把它背后的顾客赶走」。**OfficeChai 10 月 18 日整理的金融一侧 — 摩根大通拦截外部智能体交易、只开放余额等只读数据，嘉信 CEO 在彭博电视上说每周「数十次」拦下试图转账的智能体 — 属于二手整理，原始发言我们未能核实。据 Skift，美联航 CEO 斯科特·柯比在芝加哥的一场活动上说**「我不想再造一个中间商」**（经由 WSJ 转述），达美 CEO 埃德·巴斯蒂安则说对订票智能体「持谨慎态度」。

同样的两天里也有反方向的动作。OpenAI 于 11 月 10 日**收购了 AI 旅行智能体初创公司 Odessia**（TechCrunch·Skift）。条款未公开，服务已经关闭，创始人加入 OpenAI 协助「旅行领域的未来」。OpenAI 发言人称「每周有 12 亿人用 ChatGPT 处理包括旅行规划在内的日常事务」。Skift 写到西南航空推出了用于航班搜索的 ChatGPT 插件，这一点我们只在一处看到。

## 2. OpenAI — 店铺把自己的智能体放进 ChatGPT，结账尚无（事实）

OpenAI 于 11 月 10 日以测试版推出**「Businesses in ChatGPT」**（公司的发布文章在我们这边打不开，因此通过 TNW·PPC Land 两家媒体确认）。构成有两部分。在 **Business Hub** 中，商家认证自己的资料（蓝色对勾），修改说明·价格·库存，上传商品数据源。并能看到 **ChatGPT 提及自家店铺多少次、资料被查看多少次、被点击跳转到网站多少次、在哪些话题的对话中出现**，按 7 天·28 天统计。在 PPC Land 截取的画面上，点击栏附有**「点击并不确认网站访问或转化」**的附注。用户的对话不会分享给商家，数据只在超过未公开的阈值时才显示。「提及」没有定义。

**Business Agents** 只有美国的电商·在线服务商家才能创建。当店铺出现在 ChatGPT 的回答里，用户可以打开资料页与该店铺的智能体对话，智能体用店铺上传的商品信息作答。对话**带有标签，并与 ChatGPT 自身的回答分开。**想购买的人**会被引导到店铺的网站 — 结账尚无，OpenAI 正与 Visa 开发智能体支付**，TNW 这样写道。规则是「表明自己是 AI、准确标价、禁止施压销售、购买和分享个人信息需用户明确批准」。商家可以付费把自己的智能体设为 **ChatGPT 广告的落地点**（9 月 16 日开始的 Sponsored Agents 测试的延伸），并带有赞助标识。据 TNW 援引 Digiday，OpenAI 表示付费不会改变 ChatGPT 推荐该店铺的频率。认证方式为电话·短信·DNS 之一，修改或发布智能体需要身份证件，这是 PPC Land 援引 Search Engine Roundtable 的内容。美国以外的商家在上线当天被列入等候名单，没有写明费用。PPC Land 看到的第一批真实仪表盘之一显示 28 天内提及 690 次·点击 24 次（约 3.5%），但那是一家媒体看到的两家商家的画面，我们不做推广。OpenAI 写出的背景数字 — 每周 12 亿人、10 万广告主、8 月广告年化 10 亿美元 — 是公司发布的。

## 3. 谷歌 — 「先给少数人」两周后，Carbon 开放给所有付费用户（事实）

谷歌于 11 月 10 日开放了 **Gemini 4 Carbon**（公司发布）。这就是 NO.33 中写到「新记分表的第一名还不是谁都能调用」的那个模型。10 月 28 日通过 Fairwind 计划先给了网络防御者，两周后开放给**付费开发者·企业（Google AI Studio、Gemini for business）和 Google AI Ultra 订阅用户（Antigravity·Gemini 应用·搜索的 AI 模式）。**科学家经遴选后可免费使用 6 个月，网络防御者继续通过 Fairwind 获取。价格是 **11 月 30 日前每百万 token 输入 2 美元·输出 10 美元，与 Argon 相同，之后翻倍为 4·20 美元。**发布文章写道「Argon 面向大多数软件·知识工作，Carbon 面向复杂的多步调试·开放式研究等更难的任务，并在验证和推理上使用更多 token」。Antigravity 加入了预览版的 **/swarm**，把一个提示拆给一组协同的智能体运行。

基准测试全部是公司发布的，部分是发布前·内部结果。CursorBench 4.0·Perplexity WANDR·Zapier AutomationBench 第一，与 Artificial Analysis 共同制作的 MKA 第二，拦截自适应攻击智能体 99% 的路径，每次尝试的突破率 0.8%（Argon 3.1%），诚实性基准 92%（Argon 70%）等数字。在NO.44 转述 Anthropic 的表格时，我们写过 AutomationBench 上 Carbon 53.9% 领先 Fable 5.2 的 51.4% — 那个 Carbon 现在成了谁都能调用的模型。发布文章自己写道「提示注入的稳健性仍是有待改进的领域」，蛋白质·实验科学方面的结果「正在等待更广泛的基准测试」。

## 简短一则 — Epoch AI 给 Claude Fable 5.2 打的分数（事实，申明利害关系）

在NO.44 中我们写过「独立评估机构的分数尚无」。现在补上那第二行。11 月 12 日打开 Epoch AI 的模型页面，**Claude Fable 5.2 的 Epoch 能力指数（ECI）为 173，在追踪的 240 个模型中排第一**，其后是 Gemini 4 Carbon 170、GPT-6 Astra 169、Claude Opus 5.5 169。同一网站的基准测试页面写的是 174（两个页面的差异看起来是四舍五入或更新时点的不同，但我们未能确认）。据 FourWeekMBA 读取 11 月 9 日的数据文件，分数为 174.24，90% 区间为 170.1~178.8，与 Astra 的区间（166.2~172.5）**重叠。**同一整理还指出，Fable 5.2 的结果来自 10 个基准（Astra 为 24 个），全部为最高努力档位，是发布前仅用 Epoch 自家基准得出的值，可能会变化。模型页面没有区间·评估日期·努力档位。Epoch 的 ECI 页面有一句「方法论论文获得 Google DeepMind 资助，ECI 归 Epoch 所有」。分基准看，GPQA Diamond 上 Carbon 97%·Astra 96% 领先 Fable 5.2 的 94%，SpireClimb 上 Astra 34% 领先 Fable 5.2 的 20%。到此为止是数字，我们不加评价。今天没有打开 Artificial Analysis 的排行榜。

## 把三件事放在一起读（解读）

第一，**「门不是被打开，而是换了主人」（NO.43）的下一句是「主人有两个」。**美联航拦下顾客带来的智能体，同一天 OpenAI 买下了一家旅行智能体公司。航空公司想在自己的柜台留住顾客，平台想在自己内部留住顾客。柯比的「再造一个中间商」是夹在两者之间的话（解读）。可是看 OpenAI 请店铺进来的方式，**结账被送回店铺**，智能体只做到「用商品信息作答」。美联航举出的三个理由 — 凭证、不可撤销的行为（购买·里程）、需要人确认的规定 — 全都是**「智能体代办最后一步时会发生的事」**，而 OpenAI 的设计也还没把最后一步交出去。两者看似方向相反，却站在同一条线前。

第二，**平台开始亲自给出「曝光」数字。**在NO.42 中，我们看到 Ziff Davis 在 Search Console 里读到「AI 回答的引用是点击的十倍，访问却减少了」，如今 ChatGPT 直接向店铺展示「提及·查看·点击」。附注就贴在画面上 — **点击既不是访问也不是转化。**第一批画面上的 3.5% 是两家商家的数字，不能使用，但有一点很清楚：这一栏分成了四格（提及→点击→访问→转化）（解读）。而「付费也不改变推荐频率」是公司的话，还没有任何人在外部测量过。

第三，**模型的门从「先给少数人」走向「给所有人，两个月后价格翻倍」。**NO.15·33·NO.44 的形状相同。谷歌和 Anthropic 都自己写道「大多数工作用更便宜的模型（Argon·Opus 5.5）」。Epoch 的数字填上了第二行，但区间重叠、结果数量少。NO.40 的「1 分之差在区间之内」这次读作**4~5 分之差区间也会重叠**（解读）。今天依然没有理由因为一个分数而改动模型选择表。

## 如果是我们 — 运营应用·电商·AI 渠道的团队本周要做的三件事（实践）

1. **给「进入的智能体规则 3 行」（NO.43）加上「为什么」一栏。**把美联航的三个理由换成我们的话就是「接收凭证的环节」「不可撤销的环节（支付·退款·个人信息变更）」「必须由人确认的环节（SafeList 的成分判定只到「未看到需回避的项目」为止，最终判断归监护人）」。在我们的电商四层和应用界面中属于这三类的环节上标注**「智能体不能代办」**，并把理由写进条款段落（由代表决定）。不是拦截，而是写明「到哪里为止」。
2. **在流量表里加入「平台给出的曝光」一栏，但分成四格。**在NO.42 的流量三行（搜索/AI 引用/直接）旁边，放上「提及 / 点击 / 访问 / 转化」。Business Hub 仅限美国，我们现在无法注册；作为替代，每月一次向 ChatGPT·Gemini 询问我们的应用名称，手工记录「是否被提及」。等平台给出数字的那天，那就是它们该填的位置。
3. **把 11 月 30 日前同价的 Carbon 加入三项模型测试。**把 NO.17 的我们的测试（成分表判定·应用文案·Lia 脚本初稿）在 Argon·Opus 5.5 High 与 Carbon 上以相同努力档位运行，用「公司发布 / 我们确认」两行记录。在表头写明 12 月 1 日价格翻倍。Epoch 的分数填在第二行，写作「173~174，区间重叠，10 个结果」，第一名那一格留空。

## 这次没有选的

Anthropic 的上市路演（11 月 10 日）、The Information 报道的 OpenAI 季度营收、纽约市养老金与 AI 投资的报道属于投资领域，未予采用。The Hacker News 的「Fable 5.2 在多阶段网络攻击基准上胜过 GPT-6 Cyber」属于网络能力比较且涉及利害关系方的模型，只记录标题。Fireworks AI 泄露事件扩大与 Railway 的「74 万美元欺诈性 AI 计费」（BleepingComputer）是安全事故，只保留标题，后续也不写手法（Railway 是 NO.26 的后续候选）。TNW 的「澳大利亚在 OpenAI 智能体访问 Medicare 门户事件后计划设立 AI 安全监管机构」列为 NO.39 的后续候选（法案尚未通过）。Epoch 的「推理性能指数」（11 月 9 日）是「价格与成本」的后续候选。Learn:US 11 月 9 日的文章（读取投资者披露的交易员技能）属于投资领域，不作讨论。维基百科「Agentic commerce」词条只有定义和协议年表，没有拦截案例·航空公司，仅作背景阅读。

## 这条消息中未能确认的

- 没有找到美联航声明的原文页面（含 Digital Trust Center 的更新部分），只确认了三家媒体的引用彼此一致。生效日期、被拦截智能体的名称、OTA 一侧的具体做法在任何地方都没有。
- 柯比「再造一个中间商」（经由 WSJ）·巴斯蒂安「谨慎」·扎克伯格「旅行是最顶级的用途」·西南航空的 ChatGPT 插件只在 Skift 一处看到。摩根大通·嘉信的条目是 OfficeChai 的二手整理，原始发言（彭博电视）未能打开。
- OpenAI 的发布文章打不开。「尚无结账·正与 Visa 开发」「付费不改变推荐频率（Digiday）」只见于 TNW，「需要身份证件（SERoundtable）」「首个仪表盘 690/24」只见于 PPC Land。费用、「提及」的定义和阈值未公开。
- Carbon 的基准·安全数据全部是公司发布，独立评估尚未确认。12 月 1 日起的 4·20 美元价格是从发布文章的「11 月 30 日之后」转述而来。
- Epoch 模型页面 173 与基准页面 174 的差异、90% 区间（170.1~178.8）以及「10 个基准·最高努力档位」来自 FourWeekMBA 一处的数据文件整理。Epoch 的排行榜本身显示「Loading…」，未能直接比对。

## 一起读过的文章

我们直接打开并核对了性质不同的来源。分为公司发布、研究·评估机构、媒体报道、维基、我们之前的文章。

公司发布：

- [Gemini 4 Carbon now available（Google，11 月 10 日）](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) — 英文，开放范围·价格（11 月 30 日前 2/10，之后 4/20）·/swarm·基准与安全数据（公司发布）
- [Introducing Businesses in ChatGPT（OpenAI，11 月 10 日）](https://openai.com/index/introducing-businesses-chatgpt/) — 英文，发布文章（在我们这边打不开，通过下方两家媒体确认）

研究·评估机构：

- [Claude Fable 5.2 — Epoch AI 模型页面](https://epoch.ai/models/claude-fable-5-2) — 英文，ECI 173·第一·Carbon 170·Astra 169·分基准分数（无区间·评估日期）
- [Epoch Capabilities Index（Epoch AI）](https://epoch.ai/eci) — 英文，指数说明·数据 11 月 11 日更新·「方法论论文获 Google DeepMind 资助」一句

媒体报道：

- [United Airlines Moves to Block Personal AI Agents From Booking Flights（Skift，11 月 11 日）](https://skift.com/2026/11/11/united-airlines-moves-to-block-personal-ai-agents-from-booking-flights/) — 英文，声明引用·OTA 渠道·柯比发言（经由 WSJ）·Odessia·西南航空
- [United Airlines is Blocking AI Booking Agents: They Might Breach FAA And DOT Regulations（PYOK，11 月 11 日）](https://www.paddleyourownkanoo.com/2026/11/11/united-airlines-is-blocking-ai-booking-agents-they-might-breach-faa-and-dot-regulations/) — 英文，规定语句·值机示例·政策更新·达美转述
- [United Bans AI Agents From Booking Flights For Customers（AirlineGeeks，11 月 11 日）](https://airlinegeeks.com/2026/11/11/united-bans-ai-agents-from-booking-flights-for-customers/) — 英文，凭证·Digital Trust Center·呼吁其他企业跟进
- [The next hurdle for AI agents: getting websites to let them in（TechCrunch，10 月 6 日）](https://techcrunch.com/2026/10/06/the-next-hurdle-for-ai-agents-getting-websites-to-let-them-in/) — 英文，美联航条款·达美·沃尔玛·eBay·Yelp·Meta 发言
- [Amazon, JPMorgan, Schwab And Delta Are All Blocking AI Agents（OfficeChai，10 月 18 日）](https://officechai.com/ai/amazon-jpmorgan-schwab-and-delta-are-all-blocking-ai-agents-heres-why/) — 英文，金融一侧的拦截整理（二手整理）
- [OpenAI acquires Odessia, travel startup created by Sonder founder（TechCrunch，11 月 10 日）](https://techcrunch.com/2026/11/10/openai-acquires-odessia-travel-startup-created-by-sonder-founder/) — 英文，收购条款未公开·服务关闭·OpenAI 发言人发言
- [OpenAI lets businesses claim ChatGPT profiles and launch their own agents（TNW，11 月 10 日）](https://thenextweb.com/news/openai-businesses-in-chatgpt-business-agents) — 英文，Business Hub·Business Agents·无结账·规则·援引 Digiday
- [Businesses gain ChatGPT click and mention counts in OpenAI's Business Hub（PPC Land，11 月 10 日）](https://ppc.land/businesses-gain-chatgpt-click-and-mention-counts-in-openais-business-hub/) — 英文，四项指标·「点击≠访问」附注·认证方式·首个仪表盘（一处）
- [OpenAI tests Sponsored Agents in ChatGPT（TNW，9 月 16 日）](https://thenextweb.com/news/openai-chatgpt-sponsored-agents-ads-manager-hubspot-shopify) — 英文，Sponsored Agents 测试·Shopify·HubSpot·广告背景
- [Epoch: Claude Fable 5.2 Sets ECI Record at 174, Astra at 169（FourWeekMBA）](https://fourweekmba.com/ai-epoch-claude-fable-5-2-sets-eci-record-at-174-astra-at-169/) — 英文，11 月 9 日数据文件的 90% 区间·基准数量·努力档位（一处整理）

维基：

- [Agentic commerce（Wikipedia）](https://en.wikipedia.org/wiki/Agentic_commerce) — 英文，定义·争议点（责任·认证）·协议年表（无拦截案例）

我们之前的文章：

- [同一个模型，两扇门（AP News NO.44）](https://www.apholdings.kr/ko/news/fable-5-2-two-doors-and-sandbagging-logs/)
- [顾客带不进自己的智能体（AP News NO.43）](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [从搜索来的顾客在减少（AP News NO.42）](https://www.apholdings.kr/ko/news/when-search-visitors-stop-coming/)
- [记分表上加了概率（AP News NO.40）](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [AI 带来顾客的大门变成了三扇（AP News NO.38）](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
- [GitHub 十个拉取请求中有四个由智能体发起 — 新记分表的第一名还不是谁都能调用（AP News NO.33）](https://www.apholdings.kr/ko/news/agent-prs-40-percent-and-a-new-number-one/)
- [哪项工作用哪个 AI（AP News NO.17）](https://www.apholdings.kr/ko/news/which-ai-for-which-job/)
- [本周 AI 资讯 — 谷歌「更强，先给少数人」（AP News NO.15）](https://www.apholdings.kr/ko/news/this-week-gpt61-sonnet55/)
