---
no: 21
slug: count-before-you-compare
date: 2026-10-09
category: 洞察
tags: 读懂数字 · 收入会计处理 · token 价格 · 单件成本
title: 比较数字之前先看怎么数 — 700 亿美元为何变成 500 亿美元,以及 token 价格的陷阱
summary: 同样的“年化收入”和同样的“每 token 价格”,因统计对象不同,含义可能不同。借本周两篇报道,整理读数字的方法。
---
> 本文由 AI(Claude)协助起草,并经编辑审核。Anthropic 和 OpenAI 都出现在文中,Anthropic 是 Claude 的开发公司,因此存在利益关联。本文不是对任何公司或股票的投资意见,所有数字均转引自报道和公司发布。

本周 AI 行业最引人注意的数字话题,不是性能,而是“怎么数”。

## 案例 1. 同一家公司的收入为何从 700 亿美元变成 500 亿美元

Axios 在 10 月 8 日报道称,OpenAI 的年化收入是 500 亿美元,而不是上个月被广泛报道的 700 亿美元。700 亿美元源自向投资者分享的资料,是为了便于与 Anthropic 更直接地比较而“上调(gross up)”计算的数字。差别在于如何记录通过云合作伙伴实现的销售。据 Axios 引用的一位会计学教授所说,客户通过云服务商支付 100 时,Anthropic 可以把整个 100 记为收入,把服务商的分成记为费用;而 OpenAI 在部分合作伙伴销售中只把自己的份额记为收入。两家都被认为符合会计准则(GAAP)。

路透社也在 10 月 9 日报道,OpenAI 向投资者透露的 9 月年化收入略低于 500 亿美元。与此前接近 700 亿美元的说法之间的差距,源于想与 Anthropic 直接比较;与 Anthropic 不同,OpenAI 不把通过 AWS、Google Cloud 等云合作伙伴实现的销售计入收入(最早由《金融时报》报道)。

年化收入是把某一时期的销售额按一年延伸来看的硅谷式指标,Axios 还补充说,公开市场的投资者通常更看重实际收入(依据 Axios 和路透社报道,我们没有看过两家公司的会计资料)。

## 案例 2. 每 token 价格下降,每件事的成本不一定下降

Anthropic 宣布 Haiku 5.5 平均比 Haiku 4.5 便宜约 75%(公司数据)。但 Next.ink 引用外部分析机构报道称,该模型回答更长,节省幅度取决于 effort 设置,并指出超过 10 万 token 的请求每 token 单价高出五倍。AI Weekly 通讯也报道了企业因成本压力转向更便宜的模型,并建议衡量“每完成一项任务的成本”(该期内容是对其他媒体报道的概述,我们没有核对原始报道)。

## 读数字的三个问题

1. **数的是什么?** 总额还是净额;是 token,还是一件完成的工作。
2. **谁给出的数字?** 公司自己,还是独立第三方;如果两者不同,测量条件是什么。
3. **条件变了会怎样?** 最高 effort 下的得分在默认档位可能不同,长请求的单价也可能不同。

## 我们的解读

**事实:** 同一家公司的年化收入因统计方式不同,被报道为 700 亿和 500 亿美元;本周还有人指出,token 价格下降与单件成本下降未必是一回事。

**解读:** 只有单位和统计方式一致,数字才能比较。这既适用于比较不同公司,也适用于看我们自己的数字。

**我们会这样做:** 在我们的收入报告中区分总额和净额,AI 工作按“每篇文章、每条视频、每个订单”的成本记录,而不是按 token。引用其他公司的数字时,一律同时写明来源和统计方式。

## 一并阅读的资料

我们直接打开核实了五个性质不同的来源。

- [OpenAI annualized revenue $20 billion less than previously reported (Axios)](https://www.axios.com/2026/10/08/openai-50-billion-arr-anthropic-revenue-accounting) — 英文,新闻报道
- [OpenAI's September annualized revenue nears $50 bln, less than previously indicated (Reuters,刊于 Zawya)](https://www.zawya.com/en/special-coverage/openais-september-annualized-revenue-nears-50bln-less-than-previously-indicated-source-says-1586243) — 英文,通讯社报道
- [Introducing Claude Haiku 5.5 (Anthropic)](https://www.anthropic.com/claude-haiku-5-5) — 英文,公司官方发布
- [Chez Anthropic, Haiku 5.5 prend la relève des petits modèles rapides (Next.ink)](https://next.ink/260659/chez-anthropic-haiku-5-5-prend-la-releve-des-petits-modeles-rapides/) — 法文,媒体分析
- [AI got too expensive, so companies are moving to cheaper models (AI Weekly #535)](https://aiweekly.co/issues/ai-got-too-expensive-so-companies-are-moving-to-cheaper) — 英文,通讯
