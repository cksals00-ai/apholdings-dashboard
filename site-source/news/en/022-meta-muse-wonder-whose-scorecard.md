---
no: 22
slug: meta-muse-wonder-whose-scorecard
date: 2026-10-15
category: Insight
tags: Meta · Muse Wonder · Model evaluation · Independent testing · Training settings
title: Meta's first top-tier model, Muse Wonder — who graded it, and three things to check before you use it
summary: Meta released its first frontier-class model on October 12. We put the company's own scores next to an independent evaluator's, then go through price, access and training settings — three things to check before using it in our work.
---
> This article was drafted with AI (Claude) and reviewed by an editor. Anthropic, which makes the Claude models that appear here as comparisons, also makes the tool we used to write it, so we have a stake. Figures announced by companies are labeled as such, and independent evaluations are marked separately. This is not an investment opinion on any company or stock.

On Monday, October 12, Meta's Superintelligence Labs released two models, Muse Wonder and Muse Wonder Full — what Meta calls its first frontier-class models. What stands out in this news is less the scores themselves than who measured them and under what conditions.

## What came out (fact)

- Muse Wonder is available through Meta's model API and Muse Code, its coding tool. API pricing is $4 per million input tokens and $20 per million output tokens (cached input is $0.20, per the independent evaluator Artificial Analysis).
- Muse Wonder Full is only for Muse Code subscribers. It is not offered through the API (TechCrunch). According to Meta's Muse Code subscription page, Full is included in the top two of four plans (Power and Maximum), and LetsDataScience and DataNorth reported that those two plans cost $50 and $200 a month.
- Both models have a 1-million-token context window, accept text, image, video and audio as input, and output text (Artificial Analysis).
- We could not confirm whether the weights of either model can be downloaded (only LetsDataScience says they cannot). Decrypt pointed out that Meta has effectively ended its Llama line, which published its weights.

## Reading the scorecard

**Announced by the company.** On its own "Personal Superintelligence Index," Meta says Wonder Full scores 59.1, ahead of Opus 5.5 (55.2) and GPT-6 Astra (54.5), and that it also leads on the memory test MemoryBench with about 85.5 (Meta's claims as reported by Decrypt; iThome and Latent Space report the same figures). Decrypt noted that both measures were created by Meta and that the Index formula is unpublished.

**Independent evaluation.** On Artificial Analysis's overall index (v4.3, maximum effort), Wonder Full scores 56, Wonder 52, and Meta's previous model Muse Spark 1.3 scores 48. On the same index Opus 5.5 scores 58, Sonnet 5.5 scores 56 and GPT-6 Astra scores 53 (checked directly on the Artificial Analysis leaderboard, each model at its highest setting). So on the independent measure the model lands around third place — a different picture from the company's "ahead."

**A closer look.** In the same article Artificial Analysis wrote that on its coding-agents index Wonder Full scores 68, level with Claude Code running Sonnet 5.5 and above Opus 5.5 (66). On the knowledge test AA-Omniscience, however, Full scores 30 and Wonder 25, well below Opus 5.5 (46) and GPT-6 Astra (43). The rate at which it makes things up (hallucination rate) is on the low side — 23% for Full and 27% for Wonder — but among models scoring 45 or higher on the index the lowest is Gemini 4 Argon at 15%.

## Three things to check before using it (interpretation)

**1. Cost per finished job.** The same token price can still mean different costs per job. Artificial Analysis's cost for running the same task set was $4.52 for Wonder, $5.98 for Opus 5.5, $5.46 for Sonnet 5.5, $3.26 for GPT-6 Astra, $1.99 for Gemini 4 Argon and $0.72 for GPT-6.1 Sol. It judged Wonder to be pricier than most models of similar intelligence. Reports say its price matches Opus 5.5 (Decrypt), but the number we look at is cost per job, not unit price.

**2. Where you can use it.** The highest-scoring model, Wonder Full, works only inside a subscription, so it cannot be plugged into our automations through an API. What you can reach by API is Wonder, one step lower in score.

**3. Where your code and writing go.** According to Meta's Muse Code subscription page, subscriptions default to "Contributor mode": Meta may use your prompts, code, files and context, and the responses you receive, to train future models, in exchange for more usage. The page says that once you turn it off your future content is not used for training, but it does not say what happens to content already sent, so we could not confirm that. Contributor mode does not exist for Wonder on the API, and content in standard mode is said not to be used for training. We could not open Meta's terms of use ourselves, so check the terms and the settings screen before you use it.

## What we could not confirm

We could not directly open Meta's official announcement or model card. The "announced by the company" items above were confirmed through reports from TechCrunch, Decrypt, iThome and others. We checked the subscription and training settings by opening Meta's Muse Code subscription page directly. Decrypt reported that the full safety report Meta promised has not yet been published. Simon Willison, a hands-on user, wrote that Wonder offers six reasoning levels (minimal to max) and that its drawings seem better than the previous model's, but he said himself that this is an informal test based on one kind of drawing. It should not be read as a score.

## Our take

**Fact:** Meta released a top-tier model available only through its API and subscriptions; the company's metrics and the independent metrics paint different pictures; the highest model is subscription-only; and the subscription's default setting uses your content for training.

**Interpretation:** Every time a new model comes out, "it's number one" and "it's number three" appear at the same time. Both can be true, because the tests differ in who built them and which settings they were run at.

**What we would do:** We don't switch on a number. We run 20 of our own jobs (script drafts, product descriptions, comment sorting) under the same conditions, record "cost per job" and "number of fixes," and publish only after a person checks. Customer information and unpublished material do not go into any setting that may be used for training.

## Read together

We opened sources of different kinds directly. Figures are as given by each source.

- [Meta releases its first frontier model, Muse Wonder (TechCrunch)](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder) — English, news report
- [Muse Wonder / Wonder Full evaluation (Artificial Analysis)](https://artificialanalysis.ai/articles/muse-wonder) — English, independent evaluator
- [Meta Muse Wonder and the frontier AI race (Decrypt)](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race) — English, news report (company metrics vs. independent metrics)
- [Meta's best model skips API, coding plan trains on your code (LetsDataScience)](https://letsdatascience.com/blog/metas-best-model-skips-api-coding-plan-trains-on-your-code) — English, subscriptions and training settings
- [llm-meta-ai 0.2 (Simon Willison)](https://simonwillison.net/2026/Oct/12/llm-meta-ai/) — English, hands-on user's blog
- [Meta releases Muse Wonder, its first frontier-class AI model (AI Weekly)](https://aiweekly.co/alerts/meta-releases-muse-wonder-its-first-frontier-class-ai-model) — English, newsletter (summary of other outlets)
- [Muse Code Subscriptions (Meta)](https://dev.meta.ai/docs/muse-code/subscriptions) — English, Meta's official page
- [Models Leaderboard (Artificial Analysis)](https://artificialanalysis.ai/leaderboards/models) — English, independent evaluator's leaderboard
- [Meta's Muse Wonder (DataNorth)](https://datanorth.ai/news/metas-muse-wonder) — English, analysis (plans and training settings)
- [Muse Wonder report (iThome)](https://www.ithome.com.tw/news/179608) — Traditional Chinese, news report
