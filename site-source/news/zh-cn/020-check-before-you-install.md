---
no: 20
slug: check-before-you-install
date: 2026-10-09
category: 实践
tags: 技能 · 插件 · 安装前检查 · 评论分析 · 标注来源
title: 在使用“复制粘贴就完事”的 AI 方法之前 — 一次检查评论分析、技能搜索、金融简报和 Reels 技能的步骤
summary: 我们把本周韩国资讯中出现的四种“装好就用”的方法放在一起,整理出我们安装前要做的四项检查及其依据。
---
> 本文由 AI(Claude)协助起草,并经编辑审核。文中涉及的部分工具来自 Claude 的开发公司 Anthropic,存在利益关联。本文不是投资或购买建议。对于参考的韩文文章,我们只读了无需登录即可看到的开头部分,后半部分未能核实。

韩国的 AI 实务资讯 Learn:US 本周又连续发布了几篇“复制这段话粘贴给 AI 就完成”形式的文章。按公开可见的开头部分来看,共有四种:从商品评论中找出尚无人解决的抱怨的三步方法;安装一个能帮你找其他技能的技能;用金融插件获得早晨市场简报;用 Instagram Reels 技能生成个人文风文件并产出脚本。它们的用处很明显。但安装和运行靠得越近,就越容易跳过中间的检查。我们会走四个步骤。

## 第 1 步. 装的是什么 — 查来源,读内容

Anthropic 的工程文章警告说,技能会给智能体增加指令和代码,所以恶意技能可能导致数据泄露或意外行为。建议只从可信来源安装;对不太可信的,先读其中的文件以及要求连接外部地址的指令。研究结果也指向同一方向。一篇分析了两个技能市场中 31,132 个技能的论文报告称,其中 26.1% 至少含有一个“需要审查的风险模式”(作者说明这并不等于恶意,且包含可执行脚本的技能被标记得更多;收集时间为 2025 年 12 月)。

我们的做法:安装前查看作者、许可证和文件列表,有脚本就读一遍。技能安装工具 vercel-labs/skills 仓库采用 MIT 许可证,文档中说明了关闭使用情况遥测的环境变量。我们优先选择有这类说明的工具。

## 第 2 步. 能访问什么 — 从最小权限开始

邮件、日历、云盘、支付信息先以只读方式连接,凡是发送或删除操作都由人来点按钮。这与我们之前的文章《连接之后,早晨变短》原则相同。

## 第 3 步. 结果怎么信 — 每个数字都标来源

金融插件的文章定了一条规则:简报中的每个数字都要附来源,无法核实的数字要标出。这是个好规则。Anthropic 的 financial-services 仓库(Apache-2.0)的 README 也写明,它不构成投资、法律或税务建议,结果是供专业人士审阅的草稿,不做投资推荐,也不执行交易。我们划同样的界线:这类简报是“收集阅读材料的工具”,而不是“决定买什么的工具”。

## 第 4 步. 适合我们的工作吗 — 评论分析先小范围试

把评论里的购买原因和不满整理成表,再把多个商品中反复出现却无人解决的抱怨归类,这一思路可直接用于电商。我们这样试:只用我们自己销售的一两件商品的评论,不允许对评论之外的内容做推测,并把得出的三个“空白候选”与真实的客户咨询对照。含有个人信息的评论事先清除。

## 我们的解读

**事实:** 四种方法都把安装和运行紧挨在一起,技能生态的风险在官方文章和研究论文中都被提及。

**解读:** “安装前看什么”比“怎么安装”更不容易过时。工具每周都在变,但检查顺序几乎可以原样沿用。

**我们会这样做:** 引入新工具时,把这四步做成一页清单,只有通过的才列入可用名单。

## 一并阅读的资料

以下是四篇韩文文章和四个性质不同的来源。

韩文文章(仅核实公开可见的开头部分):

- [用 Claude 做出能带来收入的数字商品的 3 个步骤 (Learn:US)](https://learn.bizni.us/learnus-review-to-product) — 韩文
- [安装能帮你找技能的技能并获得首次推荐的方法 (Learn:US)](https://learn.bizni.us/learnus-find-skills-guide) — 韩文
- [安装 Claude 金融插件并获得首份简报的方法 (Learn:US)](https://learn.bizni.us/learnus-claude-finance-plugin) — 韩文
- [安装 Instagram 智能体技能并生成首个 Reels 脚本的方法 (Learn:US)](https://learn.bizni.us/learnus-instagram-agent-skill) — 韩文

在其他来源核实的资料:

- [Equipping agents for the real world with Agent Skills (Anthropic Engineering)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — 英文,官方文章
- [Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale (arXiv)](https://arxiv.org/html/2601.10338v1) — 英文,研究论文
- [vercel-labs/skills (GitHub)](https://github.com/vercel-labs/skills) — 英文,开源仓库
- [anthropics/financial-services (GitHub)](https://github.com/anthropics/financial-services) — 英文,开源仓库与免责声明
