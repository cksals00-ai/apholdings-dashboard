---
no: 58
slug: agent-door-talks-and-hung-up-calls
date: 2026-11-27
category: 洞察
tags: 智能体 · 电商 · 亚马逊 · Muse · 电信运营商 · Naver · 单任务成本
title: 曾经关上门的商家坐到了谈判桌前，三大电信运营商和Naver则挂断了智能体的电话 — 亚马逊与Meta正围绕“搜索结果与广告”会面，韩国电信运营商以“无法确认是谁委托的”为由拒绝了代理咨询，谷歌开始对文件“只收取查看部分的token”费用 — 商家首先该向智能体问的是“身份”
summary: 本周三组消息 — ①Fortune报道亚马逊与Meta就9月被封锁的Muse访问亚马逊一事多次会面（争议点是搜索结果与广告，是否达成协议不明），以及Forter统计的“智能体订单中一半来自Muse”（TNW转述CNBC）②SKT、KT、LG U+和Naver决定不受理代替用户打来电话的AI智能体的客服咨询（ZDNet、The Public、青年日报、Money Today），及其背后韩国智能体应用“Pickle”的数字③谷歌Gemini API的“只对文件中检查的部分计费”、OpenAI整合Chat与Work额度、Snowflake的“保留上限，向超出的人学习”。按事实、解读、换作我们三部分写成。
---

本文由AI（Claude）协助撰写，并经编辑审核。先写明利益关系。我们公司是Anthropic和OpenAI两家公司的付费客户，也在测试中使用谷歌和Meta的模型。我们自己就是商家一方 — 我们运营电商（Hangul Cups）、社区应用（CourtMate）和AI网红（Lia），因此在“商家如何接纳智能体”这个问题上是当事人。“简讯三则”的第三条是制造本文所用AI的Anthropic自己的发布（Skills over MCP），所以该条只转述公司文章和规范文档的句子，不添加评价。公司公布的数字写作“公司公布的数字”，仅一家媒体报道的内容一并注明其来源。第1节的谈判报道是匿名知情人士转述，两家公司均拒绝置评。本文不是对特定企业的投资意见。

我们在NO.43写过“亚马逊封锁了Meta的Muse”，在NO.45、48、53写过联合航空、eBay、Signal关门的样子，在NO.55写过“商家要定的门有四扇”。本周在这些门前同时看到了两个相反的方向 — 曾经关上门的最大商家坐到了谈判桌前，而在韩国，三大电信运营商和Naver首次挂断了“智能体的电话”。在成本方面，“用多少付多少”则下沉到了文件单位。我们将媒体报道（Fortune、TNW、The Paypers、The Decoder、TechCrunch、VentureBeat、ZDNet Korea、The Public、青年日报、Money Today）、公司发布（谷歌两篇、Anthropic一篇）、规范文档（MCP技能扩展）、调查报告（LeadDev）分为事实、解读、换作我们三部分来写。

## 1. 亚马逊–Meta — 围绕9月关上的门，正就“搜索结果与广告”谈判，尚未达成协议（事实，媒体报道）

我们直接阅读了Fortune（Sebastian Herrera，11月25日，“独家”）。内容是亚马逊与Meta就Meta的个人智能体Muse（NO.21、22、43、53）访问亚马逊一事**正在讨论潜在协议并已多次会面**，消息来源是知情人士，文中写明**能否达成协议、何时达成均不明**。列出的争议点有两个 — Muse展示亚马逊商品时**如何处理搜索结果**，以及**如何处理广告**。亚马逊方面的顾虑写有广告收入损失、Muse所展示搜索结果的质量、购物智能体可能拉远消费者与亚马逊的距离，并预计协议需要两家公司CEO的批准。封锁发生在9月（亚马逊称Muse的访问违反了服务条款），同月Meta在美国推出了Muse。数字是Fortune自己的叙述 — Muse截至10月在美国和加拿大**有1,000万以上用户完成设置**（链接到其10月22日的自家报道），亚马逊广告是**年收入686亿美元的业务，接近总营收的10%**（未标注来源）。文中还引用了安迪·贾西的两句话 — 10月说外部购物智能体“还不够好，不如直接来商家方便”，本月在Semafor活动上说“如果有公平的价值交换，不排除外部智能体”。贾西还说亚马逊自己的“购物版Alexa”过去一年有4亿以上的人用过（公司发言）。Meta在Muse初期引入了Shopify、沃尔玛、百思买等亚马逊的竞争对手作为合作伙伴（Fortune，未写明是否已实际运行），扎克伯格曾表示计划从交易中收取“小额手续费”。**Meta和亚马逊均拒绝置评。**文中引用的摩根士丹利2025年报告（到2030年美国电子商务中将有1,900亿至3,850亿美元来自智能体购物）是预测值，我们只做转述。

The Next Web（Cristian Dina，11月25日）在转述Fortune的同时补充了CNBC（Julia Boorstin，11月24日）的数字 — **据Forter Intelligence统计，截至11月22日的一周内，由智能体下的订单中51%来自Muse，Grok占24%，ChatGPT占22%**，其余来自谷歌和Instinct。扎克伯格在财报电话会上说“Muse用户的25%用智能体购过物，平均购买金额超过200美元”，以及Meta高管的“让广告主从已经花出去的钱里获得更多收益”（Muse在帮助Instagram广告的语境），也都引自CNBC。我们未打开CNBC原文，因此这些数字归为**TNW转述CNBC的单一链条**。The Paypers（11月26日）写了9月Muse用户在亚马逊结账时看到错误信息，以及亚马逊封锁后eBay也限制了外部智能体（NO.48中我们直接读过的条款）；The Decoder（11月25日）也转述了Fortune和CNBC，并同时写了贾西的“第三方智能体购物还不够方便”和“不排除开门的可能性”。

我们在NO.43写道“顾客不能带自己的智能体进来”。两个月后的图景略有不同 — 最大的商家摆上桌面的不是“绝对不行”，而是“搜索结果和广告怎么办”。这不意味着门开了。意味着条件的名字公开了。

## 2. SKT、KT、LG U+、Naver — 决定不接“智能体的电话”，背后是一款10月上线的应用（事实，媒体报道）

我们直接阅读了ZDNet Korea（Hong Ji-hu、Park Seo-rin，11月24日上午）。内容是三大电信运营商和Naver**不受理代替用户打电话到客服中心的外部AI智能体的咨询**。报道中没有开始日期，也没有写技术上如何甄别。列出的理由有三个 — 智能体的稳定性未经验证，个人信息可能被泄露或滥用，即使获得了委托也难以确认是否为真实用户。Naver方面的说明（匿名）是“智能体在法律上是否为用户的代理人并不明确，也无法知道提出请求的是用户本人还是他人”，并写明**Naver在来电方表明是“AI智能体”时不会进行咨询**（这一句仅ZDNet一家）。据称客服中心自己的AI只用于支付方式、网站使用等简单咨询，像终端分期明细这类需要本人确认的事则由人工负责。

The Public（Yang Won-mo，11月24日下午）更具体地写了各公司的应对（均仅见于该报道一家）。SKT是在AI助手来电时确认用户联系方式后挂断，由客服人员回拨给用户；KT是因本人确认困难而不与外部AI进行咨询；LG U+将不与AI助手进行电话咨询定为原则；Naver则不回应外部AI的咨询请求。核心逻辑是“变更资费套餐需要本人确认，而**在应用中同意AI代理通话，并不是电信运营商所要求的正式代理人确认**”，电信业界人士（匿名）称，若发生误操作或安全事故可能与用户产生纠纷，因此暂时维持严格的本人确认。

这条消息背后的应用是**Pickle**。据同一天ZDNet Korea的另一篇报道（Park Seo-rin，11月24日下午），它是由韩国创业者在硅谷创办的初创公司推出的智能体应用，10月在韩国开始测试，代替用户进行餐厅和医院预约、客服电话、购物和支付（对接列表中有Google日历、政府24、Coupang、Musinsa、Kurly、Yanolja、现代卡）。报道引用的Mobile Index（IGAWorks）数据为 — 周新增安装11月2日至8日67,583 → 9日至15日129,394 → 16日至22日139,504，周活跃用户10月26日至11月1日37,886 → “同期”286,996（比较区间标注模糊）。**这些数字是一篇报道对数据公司的引用**。同一篇报道中有Kakao的立场 — Pickle于11月11日开通了KakaoTalk对接，但在一天内中止（Pickle解释为对接速度问题），Kakao称“从未采取过封锁Pickle的措施”，并说明该对接是用户把PC版KakaoTalk的账号密码交给Pickle、由智能体操作KakaoTalk的方式，正在审视政策和法律争议点。报道中还有Pickle发送用户未确认的邮件、未经询问就更改日程的案例，Pickle方面称其在用户许可的账号权限范围内运行，并正在洽谈官方对接与合作。报道还写道Naver准备在年内推出个人智能体应用，Kakao准备下月试运行“Kanana Space”（各仅一家）。

两天后，两家媒体把这一动向归为“扩散”。青年日报（Ahn Jeong-hun，11月26日）列举的海外案例有：摩根大通、花旗、美国银行封锁外部AI访问账户（转述American Banker），联合航空（NO.45中我们直接读过的原文），日本的餐厅预约智能体“AutoReserve”在被要求停止后仍在数十分钟内反复来电，导致部分餐厅屏蔽了号码并告知“不通过该服务接受预约”；作为替代方案，报道列出了美国正在讨论的“Know Your Agent”（先确认智能体的身份和权限范围，再有限度地允许访问）、把公开信息（营业时间、价格）与敏感行为（账户查询、合同变更）分级分离、记录智能体的行为。Money Today（11月26日，Supple转载）在此之上补充了 — American Banker转述的“某大型银行中，外部AI重置了密码、更改了允许转账的账户后提取了10万美元的案例”，路透社（11月23日）的“美国银行正在考虑对自家智能体也设置终止开关”，杰米·戴蒙在第三季度财报电话会上的发言（“不会让任何外部智能体进入我们的系统”），以及**韩国科学技术信息通信部AI政策室长在11月25日的会议上表示正在研究AI智能体的法律定义和规则**（仅Money Today一家）。汉阳大学尹惠善（Yoon Hye-sun）教授的“目前没有任何国家定出答案，仅修订AI基本法恐怕不够”的发言也出自同一篇报道。10万美元案例和路透社报道我们未打开原文。

## 3. “用多少付多少”进入了文件内部，“上限”则被合并或任其被突破（事实，公司发布·媒体）

**谷歌Gemini API“文件切片控制”（11月23日）** — 我们直接阅读了谷歌DeepMind的Rohan Doshi、Ben Kane撰写的官方文章。它的意思是，不再把文件整个放进去，而是**只在服务器端裁出需要的页面、单元格、区间、图层送入模型，token只对“模型检查过的部分”计费**。新支持原生上传的格式除PDF外还有微软Office（docx、幻灯片、xlsx等）和OpenDocument，音频和视频也在范围内。控制项包括 — 页面范围（start_page、end_page）、分辨率（low、medium、high）、图层（page_text、page_image），电子表格是工作表编号和可见单元格，视频是起止偏移量以及fps和分辨率。**Gemini 4全部模型**均支持（示例代码为Hydrogen、Neon），在AI Studio和Gemini平台API中“即日起”可用，现有的文件大小和页数上限不变。谷歌自己没有给出节省数字 — 文中的数字均为合作伙伴引用，Vercel称“以文本方式扫页比渲染整份PDF的token少14倍”，LiteLLM称“PDF的提示token节省67%、工作簿节省33%”（合作伙伴所言，条件未写明）。从NO.46、52、57的“单任务成本”表的角度看，同一任务的token数不再只取决于模型单价，而是又多了一格取决于**放进去的是哪一块**。

**OpenAI — ChatGPT整合Chat与Work额度，“最顶端的少数人更快触顶”** — 我们直接阅读了TechCrunch（Jagmeet Singh，11月25日）。OpenAI产品负责人Thibault Sottiaux在X上写道已从部分Pro订阅者开始整合，OpenAI发言人对TechCrunch表示“大多数用户不会遇到更频繁的重置，但用量最多的少数人可能更快触及上限”。结构是Chat和Work共用**一个用量计量器**，Instant模型的对话不限量，所以触顶后仍可使用。更广泛的推行在12月（支持页面），整合本身已在11月2日的邮件中预告。报道还写道Anthropic在9月合并了Claude的聊天与Cowork（涉及制造商 — 仅陈述事实）。The Decoder（11月26日）从同一条X帖子转述的**“由于计费错误一直在套用错误的折扣，修复后GPT-6.2 Astra的上限会快40%、Sol快25%触及，不追溯收费，部分套餐额外重置1次”**只有X帖子一处且不是官方文章，所以不作为数字使用，仅记录在此。这是NO.53中“降价的同时写明了局限”的那个模型一个月后的使用上限故事。

**Snowflake — “保留上限，向超出的人学习”** — 我们直接阅读了VentureBeat（Matt Marshall，11月24日）。NO.56中我们写过Uber的“每位员工AI编程工具每月1,500美元”上限（Bloomberg Law转述，本篇报道也是同一来源），而Snowflake的AI产品负责人Will Allen说，他们设上限，但会**查看超出上限的员工的工作，把有用的流程做成“技能”供他人复用**。按公司发言人的数字，2,500名工程师中有5%至10%是这样的“开拓者”，新入职工程师的70%至80%工作经验不满2年（工程高级副总裁对The AI Journal的发言）。美元上限金额和ROI未公开。报道中有Atlassian的870个团队黑客松研究（有一名AI超级用户的团队高于中位数的概率高18个百分点），但报道披露Atlassian是VentureBeat赞助内容的广告主，所以我们不把它作为数字使用。

## 简讯三则（事实，公司发布·调查报告·规范文档）

- **谷歌DeepMind“Humanity's First Exam”（11月24日）** — 我们直接阅读了官方文章（Oran Kelly）。这是一个可靠性基准，衡量的不是能否解出难题，而是**544道简单题（20项基础能力，文字和图片）“稍作改动也每次都”答对**；Kaggle上有排行榜和技术报告，并举办到12月15日为止的三周黑客松，征集“现在的模型仍会答错的日常问题”。文中没有模型名称、分数和评分方式（只有“过去6个月有显著进展”），我们未打开排行榜和报告。这是NO.52、56、57中所写“评估方也被评估”的另一条轴 — 测的不是最高分，而是**底部的一致性**。
- **LeadDev“AI Code Review Report 2026”（VentureBeat 11月24日转述）** — 对美国和欧洲377名工程师和负责人（完成325人）的问卷调查，**由AI代码审查公司CodeRabbit赞助**（报道注明）。数字（问卷回答比例） — 组织**让写代码的智能体也审查该代码**47%，对AI所做更改的理解程度与人写的一样“非常有信心”26%，PR变大了67%，AI代码的大部分由人工手动审查82%，有明确一致的审查标准14%，AI工具标记的内容人总是或通常会确认74%，完全不测量审查指标24%，追踪token用量30%，追踪漏网缺陷22%。报道中没有问卷调查的时间。这是NO.57“审批按钮到了智能体手里”的现场分母 — 这份报告原文我们未打开。
- **Anthropic“Skills over MCP”公开测试版（11月24日）+ MCP技能扩展规范** — 因为是撰写本文的AI的制造商的发布，只转述句子。公司文章写道，MCP服务器可以连同工具一起发送“技能”（工作指令集，NO.08、26），在Claude和Claude Code中为公开测试版，Pro、Max、Ultra默认开启，Team需管理员开启，Enterprise“即将”支持，示例服务器为Shopify（店铺设计与更新）、HubSpot（客户入职）、Atlassian（组织上下文）、Carta（“即将”）。同一篇文章写道MCP由Agentic AI Foundation托管。我们直接阅读了规范网站（modelcontextprotocol.io）的技能扩展页面 — 提案SEP-2640为“Final”，规范文档路径为beta，管理主体是“Skills Over MCP工作组”。安全条款是 — **技能内容按不可信输入**处理；在主机上引发代码执行或工具许可的技能**需要用户对每个技能的明确批准**；批准绑定文件URI和SHA-256哈希，**只要有一个文件改变，批准即失效**，须重新获取；读取其他服务器的文件时，每次调用都需要写明两个服务器名称的批准。VentureBeat（11月25日）写道VS Code 1.147也支持，且Claude Code会忽略技能声明的部分权限和钩子。这是NO.26“技能成了公用规范”的下一格 — 好坏本文不作判断，只记录“批准的单位从服务器下沉到了单个技能”这一形态。

## 三件事放在一起读（解读）

第一，**关门一方的理由正在向“身份”汇聚。**三大电信运营商和Naver的说明归根结底是一句话 — 没有办法确认来电的智能体是否代表用户本人的意愿。亚马逊的争议点（搜索结果、广告）看似是钱的事，但Fortune所写的“与消费者的关系被拉远”这一顾虑也在同一位置 — 商家不再知道顾客是谁。青年日报转述的“Know Your Agent”一词就是那个答案的名字；如果说NO.54中我们写的“智能体名册”是商家内侧的版本，这就是外侧的 — **向进来的智能体要求的名册**。现在这份名册还没有格式，所以Naver用的是“表明是AI就挂断”这条最粗糙的规则，SKT用的是“挂断后回拨本人”这条第二粗糙的规则。这两条规则与NO.49所写的“AI必须表明自己的身份”相冲突 — 表明就被挂断，不表明就成了欺骗。这个冲突该由规则而非商家来解决，韩国科学技术信息通信部所说的“研究法律定义和规则”（仅一家）正处在那个位置。

第二，**“谈判”和“封锁”是同一扇门的两个阶段。**亚马逊9月关门，11月谈条件。条件的名字是搜索结果和广告 — 也就是“智能体如何展示我们的商家”和“那时我们的营收结构能否维持”。韩国电信运营商现在处于第一阶段，下一阶段会拿出的条件大概是“对通过本人确认的智能体允许到哪一步”。按NO.55的门表（商品信息、购物车、支付、会员信息）和NO.57的“读/写列”来看，电信运营商关掉的是“会员信息 — 写”这一格，而“公开信息 — 读”从一开始就不是问题（与青年日报的分级分离建议一致）。如果我们商家的表里每一格也缺少“对谁（身份条件）”，那就是本周要填的位置。

第三，**成本和上限也是同一方向 — 从整块到碎片。**谷歌不对整个文件而是对“看过的部分”计费，OpenAI把两个计量器合并为一个的同时提前说了“少数人会更快触顶”，Snowflake不是强制守住上限，而是把超出者的工作切成碎片（技能）复用。三者都让人以更小的单位看待“智能体花的钱”。NO.46写了单任务成本，NO.57写了工具调用次数列，本周新增的列是**“放入的碎片”** — 同一页PDF是整个放进去，还是只放了两页。而LeadDev问卷的“47%由写代码的智能体兼做审查”“只有14%有一致标准”，是尚未用人话写下上限和审批规则的团队仍占多数的分母（因为是有赞助方的问卷，比例仅供参考）。

## 换作我们 — 运营电商、应用和AI网红的小团队本周要做的三件事（实战）

1. **先制定我们商家的“进入智能体名册”格式 — 身份、代理范围、联系方式三格。**在NO.55的门表（商品信息、购物车、支付、会员信息 × 允许/许可制/封锁）和NO.57的“读/写”列旁边增加一列“谁进来了”。格子里要写的有三项 — 智能体自称是什么（运营方、应用名称），以哪位用户的何种权限进来的（是登录我们的会员账号，还是智能体自己的账号），出了问题联系谁。当智能体进入Hangul Cups的订单咨询、CourtMate的论坛、Lia的评论区时，如果这三格填不上，就只允许到“公开信息 — 读”为止，更多的交给人处理。电信运营商的“表明是AI就挂断”作为我们不会效仿的规则写在名册最上方 — 挂断表明身份的智能体，剩下的就只有不表明身份的智能体。取而代之写上“对表明身份的智能体立即提供公开信息”。
2. **在运营规则和商店说明中加入一行：不把我们账号的账号密码交给外部智能体。**Kakao所说明的Pickle对接方式（用户把PC版即时通讯软件的账号密码交给智能体）与其说是智能体一方的过错，不如说是没有官方对接时产生的默认状态。在NO.54的名册中查找并记下我们团队使用的智能体（Lia运营、新闻收集）在哪些服务中不是以“自己的账号”而是以“我们的账号”登录的，有官方对接（API、连接器）的地方迁移过去，没有的地方缩减为“只读”。在外国人应用3款的商店说明和CourtMate的指南中是否加入“我们不支持接收用户密码的智能体”这一行，与宣传部门商定。
3. **在单任务成本表中增加“放入的碎片”列，用一份PDF跑三遍。**在NO.46、52、57的表（模型/阶段/完成/token/工具调用次数/单任务成本/时间）中加入“输入碎片”列，把成分表任务的原始PDF一份分别以①整份②仅相关页面③仅相关页面的文本图层放入，用同一模型、同一阶段运行。谷歌文章中的合作伙伴数字（14倍、67%）不是我们的数字，所以只记录我们三次的token数和是否答对。答案不稳定说明碎片切得太小，token不减少说明碎片没有意义。结果写在下一篇，不行就写“没成”。Lia的脚本中以学习的语气放入“最大的商家与智能体谈判的条件是‘搜索结果与广告’”，数字只以reported的形式写入。

## 本次未选的内容

Anthropic相关 — CEO阿莫迪“让AI治理社会是个坏主意”发言的报道（11月25日），把Messages API迁移到Rust的自家研究文章（11月26日），苏黎世办公室扩张（彭博转述），Epoch的算力支出分析，因涉及制造商只留标题。OpenAI的“Private Inference”试点只有奥特曼的X帖子一处，待官方文章发布后再处理。微软威胁情报的“ARTEX”分析（11月25日，The Decoder转述）和CERT-In警报属于安全类文章，按不写手法的原则只留标题。Z.ai GLM-5.4（循环Transformer，VentureBeat 11月24日）、GLM-5.5延期（路透社转述）、蚂蚁集团Ling-3.2-air（MIT许可证，TechNode 11月25日）作为NO.51开放权重的后续候选保留。FCC批准SpaceX卫星数据中心、英伟达停止向东南亚出货服务器、纽约州AI聊天机器人玩具禁令与我们的工作距离较远，只留标题。谷歌的Neon和Hydrogen“开发者展示”、与Golden State的合作、Google相册和Canvas的指南文章属于宣传文章，未收录。Axios科技版这次依然只显示相对时间，没找到AI文章；Arena排行榜没有列标题，未引用。11月26日（周四）的日报没有执行记录，所以当天没有草稿 — 不补写。

## 这条消息中我们未能确认的内容

- 亚马逊–Meta谈判是**Fortune对匿名知情人士的转述**，两家公司拒绝置评。“1,000万人”是Fortune自己的叙述（链接到10月的报道），“686亿美元”未标注来源。Forter的51/24/22%以及扎克伯格和Meta高管的发言是TNW转述CNBC的报道，我们未打开CNBC原文（也不知道Forter的统计方法和样本）。Shopify、沃尔玛、百思买是否在Muse上实际运行，文中没有写。Meta的股价反应属于投资领域，未写。
- 三大电信运营商和Naver的措施，其开始日期、官方公告、技术识别方法在任何一篇报道中都没有，各公司的应对（SKT回拨、KT、LG U+的原则）和Naver的“表明是AI就中止”各仅见于一家媒体。Pickle的安装量和活跃用户数字是ZDNet引用的Mobile Index一处，“同期”的区间模糊。KakaoTalk对接方式的说明是Kakao方面的说明。韩国科学技术信息通信部的发言、10万美元银行案例、路透社终止开关报道我们只在Money Today一处读到，原文（会议资料、American Banker、路透社）未打开。AutoReserve案例见于两家媒体，但原始来源未确认。
- 谷歌文件切片的节省数字全部是合作伙伴引用，没有条件。“只对检查的部分计费”的准确计费单位（各分辨率的token数）因未打开文档而不知道。OpenAI的40%、25%、额外重置、Fast Mode免费只有X帖子一处（The Decoder转述），TechCrunch的报道中没有。Snowflake的上限金额和ROI未公开。
- HFE的评分方式和各模型分数因未打开排行榜和报告而不知道。LeadDev问卷我们未打开原文，有赞助方，且没有调查时间。Skills over MCP我们只读了公司文章和规范页面，规范正文（specification/beta）和Claude Code的具体行为未打开，我们也没有试用过。
- 任何一家公司的测试我们都没有复现。“换作我们”的三行本周开始，结果写在下一篇。

## 一起读过的文章

我们直接打开并确认了性质不同的来源。分为公司发布、规范文档、媒体报道（海外、韩国）、我们之前的文章。

**公司发布**

- [Introducing file slicing controls in the Gemini API (Google, 11月23日)](https://blog.google/innovation-and-ai/technology/developers-tools/file-slicing-controls/) — 英文，Gemini 4全部模型·PDF/Office/OpenDocument·页面·分辨率·图层·单元格·视频区间·“只收检查部分的token”·合作伙伴引用14倍/67%/33%
- [We're launching Humanity's First Exam and a Kaggle hackathon to test LLM reliability (Google DeepMind, 11月24日)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/humanitys-first-exam/) — 英文，544题·20项能力·“变形后也每次”·黑客松至12月15日·无分数
- [MCP servers can now ship skills, run tasks, and more with Claude (Anthropic, 11月24日)](https://claude.com/resources/articles/skills-over-mcp-tasks-and-more) — 英文，公开测试版·Pro/Max/Ultra默认·Team管理员·Enterprise“即将”·Shopify/HubSpot/Atlassian/Carta·Agentic AI Foundation（制造商文章 — 仅事实）

**规范文档**

- [Skills — MCP扩展概览 (modelcontextprotocol.io)](https://modelcontextprotocol.io/extensions/skills/overview) — 英文，SEP-2640 Final·规范路径beta·工作组·按技能明确批准·SHA-256绑定·文件变更时重新批准·跨服务器读取按调用批准

**媒体报道 — 海外**

- [Exclusive: Meta and Amazon discuss ending Muse shopping bot blockade, as ads, search emerge as key issues (Fortune, 11月25日)](https://fortune.com/2026/11/25/exclusive-amazon-meta-talks-deal-muse-ai-shopping-agent-blockade/) — 英文，知情人士转述·多次会面·搜索结果·广告·CEO批准·9月封锁·1,000万人·686亿美元·贾西发言·合作伙伴·拒绝置评
- [Amazon and Meta in talks to end the Muse blockade, Fortune reports (The Next Web, 11月25日)](https://thenextweb.com/news/amazon-and-meta-talks-muse-blockade-ads-fortune) — 英文，转述Fortune + 引用CNBC（Forter 51/24/22%·“25%·200美元”·Instagram广告）
- [Amazon and Meta reportedly in talks over Muse AI agent access (The Paypers, 11月26日)](https://thepaypers.com/payments/news/amazon-and-meta-reportedly-in-talks-over-muse-ai-agent-access) — 英文，9月支付错误·提及eBay限制
- [Amazon and Meta are in talks to end the block on Meta's AI shopping agent Muse (The Decoder, 11月25日)](https://the-decoder.com/amazon-and-meta-are-in-talks-to-end-the-block-on-metas-ai-shopping-agent-muse-in-amazons-online-store/) — 英文，转述Fortune和CNBC·贾西“不排除”
- [OpenAI says heavy ChatGPT users may hit limits sooner as it merges Chat and Work (TechCrunch, 11月25日)](https://techcrunch.com/2026/11/25/openai-says-heavy-chatgpt-users-may-hit-limits-sooner-as-it-merges-chat-and-work/) — 英文，X帖子·发言人·单一计量器·Instant不限量·12月
- [GPT-6.2 Astra users now hit limits 40% faster after OpenAI patched a pricing error (The Decoder, 11月26日)](https://the-decoder.com/gpt-6-2-astra-users-now-hit-limits-40-faster-after-openai-patched-a-pricing-error/) — 英文，X帖子一处·40%/25%·不追溯
- [After token leaderboards and spending caps, Snowflake has a third idea (VentureBeat, 11月24日)](https://venturebeat.com/orchestration/after-token-leaderboards-and-spending-caps-snowflake-has-a-third-idea-keep-the-cap-then-learn-from-whoever-breaks-it) — 英文，保留上限·“开拓者”5%至10%·新人70%至80%·Uber 1,500美元（Bloomberg Law）·赞助披露
- [Nearly half of surveyed engineers and leaders say the AI agents that write their code also review it (VentureBeat, 11月24日)](https://venturebeat.com/technology/nearly-half-of-surveyed-engineers-and-leaders-say-the-ai-agents-that-write-their-code-also-review-it) — 英文，LeadDev 377人·CodeRabbit赞助·47%·26%·82%·14%
- [MCP servers can now deliver AI agent skills, changing what companies approve when they connect one (VentureBeat, 11月25日)](https://venturebeat.com/technology/mcp-servers-can-now-deliver-ai-agent-skills-changing-what-companies-approve-when-they-connect-one) — 英文，公开测试版·VS Code 1.147·Claude Code忽略权限和钩子

**媒体报道 — 韩国**

- [SKT、KT、LG U+、Naver将阻止AI智能体打来的客服咨询 (ZDNet Korea, 11月24日)](https://zdnet.co.kr/view/?no=20261124101239) — 韩文，稳定性·个人信息·本人确认·代理人地位·“表明是AI就中止”
- [AI助手“Pickle”用户激增……Naver和Kakao会把门开到哪一步 (ZDNet Korea, 11月24日)](https://zdnet.co.kr/view/?no=20261124161846) — 韩文，Pickle介绍·Mobile Index安装/WAU·KakaoTalk对接中止·Kakao立场·Naver/Kakao自家智能体
- [AI助手连资费套餐都能改……三大电信运营商和Naver叫停“AI代理咨询” (The Public, 11月24日)](https://www.thepublic.kr/news/articleView.html?idxno=328269) — 韩文，SKT回拨·KT·LG U+原则·“应用内同意不是代理人确认”
- [AI开始“代打电话、代预约”……产业界“限制访问”扩散 (青年日报, 11月26日)](https://www.youthdaily.co.kr/news/article.html?no=230336) — 韩文，海外银行·联合航空·AutoReserve·Know Your Agent·分级分离·行为记录
- [海外也对AI智能体“上闩”……AI助手时代探索“新秩序” (Money Today, 11月26日, Supple转载)](https://supple.kr/news/cmwx58b2sl9t9kwp89yrww9w0) — 韩文，10万美元案例（转述American Banker）·路透社终止开关·戴蒙·韩国科学技术信息通信部研究·尹惠善教授

**我们之前的文章**

- [审批按钮到了智能体手里 — 权限的三种形态 (AP News NO.57)](https://www.apholdings.kr/ko/news/approve-button-and-the-shape-of-permission/)
- [“限速”首次有了数字 — 规则写在哪里才会被遵守 (AP News NO.56)](https://www.apholdings.kr/ko/news/perplexity-speed-limit-and-rules-written-then-broken/)
- [智能体走到了支付按钮前 — 商家要定的是四种门之一 (AP News NO.55)](https://www.apholdings.kr/ko/news/agent-doors-checkout-and-handback/)
- [智能体名册和事故日志，先做这两张 (AP News NO.54)](https://www.apholdings.kr/ko/news/agent-roster-and-incident-log/)
- [每周AI消息 — 降价并写明局限，智能体进入桌面和购物车 (AP News NO.53)](https://www.apholdings.kr/ko/news/weekly-2026-11-21/)
- [“中间格”Gemini 4 Neon — 仅凭一张分数表不够的三个理由 (AP News NO.52)](https://www.apholdings.kr/ko/news/neon-same-score-seventeen-points-apart/)
- [没有主播也没有摄像机的直播成了常规编排 — 谁该表明身份 (AP News NO.49)](https://www.apholdings.kr/ko/news/no-host-ai-broadcast-and-who-must-disclose/)
- [换模型要花几周 — 只有放在模型外面的东西能带走 (AP News NO.48)](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [出现了“每天用的模型”一格 — 用单任务成本来读的方法 (AP News NO.46)](https://www.apholdings.kr/ko/news/hydrogen-daily-driver-price-per-task/)
- [挡住顾客的智能体，接纳商家，模型开放给所有人 (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [顾客不能带自己的智能体进来 (AP News NO.43)](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [技能成了“公用规范” — Agent Skills基金会捐赠，从被盗钥匙中要检查的三件事 (AP News NO.26)](https://www.apholdings.kr/ko/news/skills-go-public-three-checks/)
