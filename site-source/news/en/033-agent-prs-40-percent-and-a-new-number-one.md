---
no: 33
slug: agent-prs-40-percent-and-a-new-number-one
date: 2026-10-30
category: Insight
tags: GitHub Octoverse · agent PRs · model selection · Gemini 4 Carbon · Artificial Analysis
title: Four in Ten GitHub Pull Requests Now Start with an Agent — Fewer Developers Use Just One Model, and the New No. 1 on the Scoreboard Can't Be Called Yet
summary: On October 28, GitHub's annual Octoverse 2026 report said that "more than 40% of pull requests in September were started with an agent." In March it was 17%. In the same report, 61% of Copilot users who pick their own model used two or more in a month, and no single model exceeded 25% of requests. The same day, four weeks after announcing Argon, Google released its "strongest model," Gemini 4 Carbon — again to a subset of cyber defenders first. The scoreboard where Carbon took first place was rebuilt the day before, so its scores cannot be compared with the old ones. We put the numbers from the users' side (GitHub) next to the numbers from the makers' side (Google and an evaluation firm), and wrote down what a small team should change in how it picks models.
---
> This article was written with AI (Claude) and reviewed by an editor. Anthropic, the company that makes Claude, competes with Google and OpenAI, which appear in this article, and an Anthropic model appears in second place on the ranking discussed here. GitHub is a Microsoft company, and our company is a paying customer of these companies' AI tools. Figures published by companies are marked as "company-reported," and figures from an independent evaluator are labeled with the version of the scoreboard they come from. This article is not a recommendation to buy or sell any company's stock.

In NO.16 we wrote "Which AI Do People Use Most?" and in NO.17 "Which AI for Which Job?" The answer then was: "the numbers differ by survey, and the companies have stated their intended uses." This week, two very different sets of numbers came out on the same day. One is from the **users' side**: GitHub's annual report, which counted a year of activity and shows what 225 million developers actually pushed and which models they chose. The other is from the **makers' side**: Google released yet another "strongest model," and it took first place on an independent evaluator's scoreboard. Put side by side, the two sets show less about "which is best" and more about "how people actually choose."

## 1. GitHub Octoverse 2026 — 40% of pull requests start with an agent (facts)

GitHub published its annual Octoverse 2026 report on October 28 (company-reported; covers October 1, 2025 to September 30, 2026). The figures below are from the official post, which we read directly.

- **Pull requests started by agents.** "As of September, developers start more than 40% of pull requests with an agent. In March, it was 17%." That is 110 million in September alone, about 6x March's volume. The report calls this figure **"a floor,"** since not all agent use is detected.
- **What happens to those PRs.** About 87% of agent-started PRs touch multiple files (79% for PRs with no detected agent involvement), and the share merged within two weeks rose from 83% in February to 90% in September. The comparison group held at about 86%.
- **Overall scale.** Over 12 months: 17.9 billion pushes, 34.3 billion commits, 1.3 billion merged PRs (about 3.5 million a day), and 45.4 billion Actions jobs. Commits rose from 12.9 billion the year before to 34.3 billion. The report notes that the counting window and basis changed this year, so the 2024 and 2025 figures were recalculated. Developer Simon Willison, who was at the event, recorded the on-stage figure of "220 million merged PRs per month, tripled in less than a year."
- **Languages.** By contributor count, TypeScript is first, Python second, JavaScript third, and Rust doubled in a year, the fastest growth. The share of merged PRs with detected AI involvement: TypeScript about 44.1%, Python 41.1%, Rust 40.4%, Java 21.2%.
- **Developers.** More than 225 million. The US has 38.3 million and India 32.0 million, and both added more than 10 million this year.

## 2. Same report — fewer people use just one model (facts)

Octoverse 2026 is the first to include statistics on models that users **explicitly chose** inside GitHub Copilot (company-reported). It excludes auto selection, staff usage, and bring-your-own-key requests, counts only models with at least 1,000 weekly active users, and the report states plainly that the figures "describe observed use, not model quality."

- **Two or more.** In September, **61% of users who picked a model used more than one**. Four months earlier it was 50%.
- **More kinds.** The number of distinct models used by paid users grew from 29 in May to 47 in September, and **no single model exceeded 25% of requests.** The report did not publish shares by model name.
- **Uses split.** Of every 100 user-selected requests, 38 went to general-purpose models, 37 to deep reasoning and planning, and 25 to fast, lightweight models. 63% of paying users used auto model selection at least once in September.
- **Copilot itself.** 55% of monthly active users use agentic features (35% a year ago), and the cloud agent grew 230% year over year.

The same week, a "how to choose" also came from the OpenAI side. In a Hacker News thread about GPT-6.1 Terra, OpenAI employee Ted Sanders explained that the company's model names run **in size order (Luna < Terra < Sol < Astra)**, that size mostly determines reliability, per-token cost, and recall of obscure facts, and that the version number (6.1) signals the size of the improvement — "not a giant enough leap" to be called a 7. He also offered a rule of thumb: Astra for quality alone, Sol if price matters somewhat, Terra or Luna if price matters a lot. The main thread of the discussion was a complaint: models come out one at a time so it is hard to tell which is better, and there is no task-based guidance, so everyone has to evaluate for themselves. Simon Willison highlighted the comment, and we opened the original thread to confirm it. It is an individual employee's comment, not a company document.

## 3. Google Gemini 4 Carbon — again the "strongest model," again for some people first (facts)

On October 28 Google published "Gemini 4 Carbon: our next frontier model" (under the name of Google DeepMind's Koray Kavukcuoglu; company-reported). That is two weeks after Argon reached the Gemini app.

- **What it claims.** "State-of-the-art cybersecurity and long horizon capabilities," and the company says internal teams had it work **for days** on multi-step tasks such as finding and patching bugs across large codebases. It says coding, agentic, scientific, full-stack web, and multimodal work improved.
- **Who gets it first.** This week, **a subset of cyber defenders**; next, trusted partners in the Fairwind Program (governments, critical infrastructure, core platforms, and defensive research labs, after vetting); it is also in the US government's voluntary pre-release testing; and for developers, businesses, and consumers, "as soon as possible." **No date, product, or plan is given.** When we read it, the Fairwind Program page listed only Argon. Both 9to5Google and Mashable read the general release date as undetermined.
- **Price.** The company blog lists the same introductory price as Argon ($2 per million input tokens, $10 per million output, 95% off cached input) and the price after that ($4 and $20). A price list for a model you cannot call yet.
- **Company figures.** WebDev Arena +89 Elo to fourth place (1,768); SEC-bench Pro (vulnerability finding) 88.2%; ExploitGym 54.8%; CWE-bench (patching) 71.0%; Gray Swan indirect prompt injection benchmark 0.0% attack success (Argon 0.7%); on Terminal-Bench 4.0, 0.0% successful cheating and 0.4% attempts; high-severity misalignment alerts in internal coding environments down about 80%; unsupported claims cut roughly in half. All company-reported, and the company says the cybersecurity benchmarks were run without guardrails. Mashable read the company's table as "first on 15 of 17 benchmarks, with GPT-6 Astra ahead on FrontierSWE 2 and Claude Opus 5.5 ahead on OSWorld-2.1."
- **Independent scoreboard.** On Artificial Analysis Intelligence Index **v5.0**, Carbon (High) is **first with 59**. The evaluator's model page, which we opened directly, lists it first of 54 models, with a cost of $7.76 per index task (47th of 53), 200 million output tokens used across the index (median 70 million; 51st of 53 for verbosity), and 97.9 seconds to first token (median 3.37 seconds). On the same evaluator's leaderboard (checked directly), second place is Claude Opus 5.5 (Max) at 58; Argon's 50 is Mashable's report. The model page says it can be called through one API provider, Google's (a "No publicly available API" label we saw earlier was not there when we reopened it), but Google's post gives no general release date.

The point is that the scoreboard itself changed. Artificial Analysis **rebuilt the index as v5.0 on October 27** (confirmed directly in the evaluator's changelog and methodology page). Nine evaluations are grouped into four areas — knowledge work, coding, science, and general — at 25% each, and five of them (AA-Briefcase, AutomationBench-AA, FrontierCode 2.0, CritPt v2, AA-Omniscience v1.1) are **private evaluations whose questions are not published**. GDPval was dropped from the index. The methodology page says scores from different versions cannot be compared directly. Argon was 53 on the old version and is 50 on v5. The same model's score fell three points — not because the model got worse, but because the ruler changed.

## How to read the two sets of numbers side by side (interpretation)

First, **"40%" means "started with an agent," not "written by an agent."** GitHub counted detected signals and called even that a floor. PRs that a person watched from start to finish and PRs an agent opened on its own are mixed in one number. What we paid attention to is the merge share. That agent-started PRs are now merged within two weeks at a higher rate (90%) than the rest (86%) means reviewers have **started accepting them**. The rejection rate did not go up. Still, this is an observation inside GitHub, where Copilot is deeply embedded; teams using other tools are not in these numbers.

Second, **asked "which model is best," users are answering "several."** 61% use two or more, 47 kinds, none above 25%. In NO.16 we wrote that the numbers differ by survey, and GitHub's numbers add one more reason: people don't pick a model, they **divide the work into lanes** and pick per lane (general 38, reasoning 37, lightweight 25). And a company insider saying outright "our model names are in size order; choose by how price-sensitive you are" is something companies rarely say in official documents. We read the comment not as "company guidance" but as "a hint that the axes of choice are size, price, and speed."

Third, **a "new No. 1" has to be read on three counts.** Is it first right after the ruler changed (v5 came out the day before)? By how much (one point over second place)? Can you call it (not yet)? Then add cost and verbosity: $7.76 per task, 47th of 53; output tokens about three times the median; more than a minute and a half to the first token. Whether a model one point higher suits our work is told more by these numbers than by the score. In NO.15 we described Argon as "stronger, for some people first," and in NO.22 we asked "who graded the scores." Carbon repeats both articles. The difference this time is that "first" means not paying subscribers but **cyber defenders**. The company has made security this model's first use, and we read that as the reason it is being more conservative about the public release date (interpretation).

Fourth, our own interpretation. The users' numbers and the makers' numbers explain each other. When the "strongest" model changes every two weeks, users don't tie themselves to one, and when users run several, auto selection (used by 63%) and routing become the default. When we wrote "how to work when models change weekly" in NO.4, that was an assumption; now GitHub's numbers support it.

## If it were us — change three lines in the model-selection document (practice)

Our team mixes three or four models across the app backend, commerce integrations, and Ria's video scripts. Rewriting the "model-by-task table" from NO.17 with this week's numbers comes to three lines.

1. **Count our own PRs.** Label PRs opened by agents (Claude Code, Codex, and so on) and record three numbers monthly: share of agent-started PRs, two-week merge rate, and revert rate. GitHub overall is at 40% and 90%. If ours are lower, it's a tooling problem or a review bottleneck; if the merge rate is high but reverts rise, review has gotten loose. The third number (reverts) isn't in GitHub's report, which is why we add it.
2. **Divide into three lanes.** Rewrite the task table in the same three lanes GitHub users actually divided into (38/37/25): general, deep reasoning, lightweight. "First draft of a Ria script" is general; "reviewing SafeList ingredient-judgment rules" is deep reasoning; "classifying 100 product descriptions" is lightweight. Write a first choice and a **fallback model** for each lane, and when a new model appears, test it in **that one lane** only, not everywhere. Make how price-sensitive the task is the lane's second criterion — the same axis Sanders described.
3. **Test a new No. 1 only after a three-line check.** (1) Was the comparison made on the same version of the scoreboard (don't mix v4 and v5 scores)? (2) Can it be called via API (if not, mark it "waiting" in the table and don't test it)? (3) How do cost per task, output length, and time to first token compare with what we use now? Only after filling in those three lines does it get tested in one lane from step 2. We don't switch models over a one-point difference.

## What we didn't pick this time

"Mistral Large 4 (evaluated October 29)" in the Artificial Analysis changelog is not covered because we could not find an official Mistral announcement (an AI Weekly article from October 10, citing a Hugging Face model page, said "open weights planned for October 31," and we did not open that page). The security vendor GitGuardian's own figures attached to its reading of Octoverse (28.65 million exposed secrets, the secret rate in commits assisted by a particular coding tool, and so on) are unverified and not used. A mention of a leadership change at Google DeepMind in the Mashable article comes from a single outlet and is not used. Three new Hugging Face posts (NVIDIA's multilingual transcription model, LiquidAI's LFM3, and AI2's "Can we trust LLMs to judge whether a research idea is novel?") have not been read yet. Anthropic's October 27 and 28 announcements (drug development, AI for Science) involve a strong conflict of interest and will be covered separately after cross-checking.

## What we could not confirm

- All Octoverse figures are GitHub's own and have no independent verification. The company itself called the agent share "a floor," and the model statistics count only explicitly selected requests inside Copilot. Shares by model name were not published.
- Simon Willison's "220 million merged PRs per month" is a figure from the stage; the official post we read gives only the 12-month total (1.3 billion). We also could not find it on GitHub's Universe recap page.
- Carbon's security benchmarks and safety figures are company-reported; the only independent confirmation is the Intelligence Index. "First on 15 of 17" is Mashable's reading of the company's table, and we did not check the full table ourselves. Argon's v5 score of 50 is also Mashable's report.
- The Artificial Analysis model page says Carbon can be called through one API provider, Google's, but Google's post has no general release date, so we could not confirm who can call it today. Carbon hallucination and accuracy figures found on a gateway vendor's blog could not be confirmed on the evaluator's page and are not used.
- Carbon's general release date, products, and plans are not in the company post. Ted Sanders's explanation is an individual employee's comment, not an official OpenAI document.

## Further reading

We opened and checked sources of different kinds directly. They are grouped as company documents, independent evaluator, personal blog and community, press, security vendor, and our earlier articles.

Company documents:

- [Octoverse: Commits, pushes, reach new highs in 2026 as developers build with agents (GitHub)](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/) — English, the annual report (agent PRs, model-selection statistics, methodology notes)
- [Gemini 4 Carbon: our next frontier model (Google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) — English, the company announcement (release order, price, company figures)
- [Fairwind Program (Google DeepMind)](https://deepmind.google/fairwind-program) — English, trusted-partner program page (listed only Argon when we read it)

Independent evaluator:

- [Intelligence Benchmarking Methodology (Artificial Analysis)](https://artificialanalysis.ai/methodology/intelligence-benchmarking) — English, index v5.0 composition, private evaluations, and the note that versions aren't comparable
- [Gemini 4 Carbon (Artificial Analysis model page)](https://artificialanalysis.ai/models/gemini-4-carbon) — English, index 59, cost per task, output tokens, time to first token
- [Models (Artificial Analysis leaderboard)](https://artificialanalysis.ai/models) — English, the v5 leaderboard (first Carbon 59, second Claude Opus 5.5 Max 58)

Personal blog and community:

- [Simon Willison's Weblog, 2026-10-28](https://simonwillison.net/2026/oct/28/) — English, notes from GitHub Universe and the OpenAI model-naming explanation
- [GPT-6.1 Terra — Hacker News discussion](https://news.ycombinator.com/item?id=50248124) — English, OpenAI employee Ted Sanders's comment on model names and how to choose (personal comment)

Press:

- [Google announces Gemini 4 Carbon with 'significant' coding gains (9to5Google)](https://9to5google.com/2026/10/28/gemini-4-carbon-announcement/) — English, tech outlet (cross-check)
- [Google announces Gemini 4 Carbon, its new frontier AI model (Mashable, republished on Yahoo)](https://tech.yahoo.com/ai/gemini/articles/google-announces-gemini-4-carbon-193050677.html) — English, reading of the company's benchmark table, Argon's score, release scope

Security vendor:

- [GitHub Octoverse 2026: AI Agents, Citizen Developers, and the New Security Reality (GitGuardian, Security Boulevard)](https://securityboulevard.com/2026/10/github-octoverse-2026-ai-agents-citizen-developers-and-the-new-security-reality/) — English, used to cross-check Octoverse figures (the vendor's own figures are not used in this article)

Our earlier articles:

- [Which AI for Which Job — Uses the Companies Stated and the Tests We Use (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — Korean, the model-by-task table this article rewrites
- [Which AI Do People Use Most — Why the Numbers Differ (AP News NO.16)](https://www.apholdings.kr/ko/news/who-uses-which-ai/) — Korean, why survey numbers differ
- [Meta's First Frontier Model Muse Wonder — Who Graded the Scores (AP News NO.22)](https://www.apholdings.kr/ko/news/meta-muse-wonder-whose-scorecard/) — Korean, how to read a scoreboard
- [This Week in AI — Two Companies Go "Cheaper," Google Goes "Stronger, for Some People First" (AP News NO.15)](https://www.apholdings.kr/ko/news/this-week-gpt61-sonnet55/) — Korean, the same pattern at Argon's launch
