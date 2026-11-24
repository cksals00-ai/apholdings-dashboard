---
no: 26
slug: skills-go-public-three-checks
date: 2026-10-23
category: Insight
tags: Agent Skills · Anthropic · Linux Foundation · AAIF · API version · Railway · API keys
title: Skills became a "shared standard" — the Agent Skills donation, the first new API version in three years, and stolen keys: three things we checked
summary: On October 22 Anthropic handed the Agent Skills standard to the AAIF under the Linux Foundation; a day earlier the Claude API got its first new version since 2023; and the same day hosting provider Railway announced that environment variables holding customers' API keys may have leaked. We read three different stories from the viewpoint of a single skill folder and wrote down the order in which we checked ours.
---
> This article was written with AI (Claude) and reviewed by an editor. Anthropic, at the center of this article, is the company that makes the Claude we used to write it, and our own company builds and uses several internal skills, so we have an interest to disclose. For that reason, figures announced by companies are marked as "company-announced," and instead of judging anything good or bad we only record the order in which we actually checked our own work. This is not an investment opinion on any company.

This week brought three stories about the "parts" of AI agents within three days. One is about a format (the skill format left one company's hands and went to a foundation), one about a version (the Claude API got a new version after three years), and one about keys (API keys stored with a hosting provider may have leaked). Read separately, they are different news. Read from the position of someone running a single skill folder, they converge on the same question: what is inside my folder, and what does it depend on? Please read this as a follow-up to NO.8 (when skills reach ten thousand) and NO.20 (the order to check before you install).

## 1. Format — the skill format went to a foundation (facts)

On October 22 Anthropic announced that it is donating the Agent Skills standard to the Agentic AI Foundation (AAIF) under the Linux Foundation. According to the announcement, the donation covers the standard itself, the "Agent Skills" name and logo, the GitHub organization, and the agentskills.io domain. The AAIF was founded by Anthropic together with Block and OpenAI, and Anthropic previously donated MCP (Model Context Protocol) to it.

The Linux Foundation's press release said it accepted four projects on the same day: Anthropic's Agent Skills, OpenAI's Open Responses (a model-calling spec that spans multiple providers), Hugging Face's OpenEnv (sharing reinforcement-learning environments), and Alibaba's OpenSandbox (sandboxes for agents). It said the foundation's project count went from 3 at its December 2025 launch to 10.

The spec site (agentskills.io) defines a skill in a few lines. **A skill is a folder containing a SKILL.md file.** That file holds a name and a description (the minimum fields) plus instructions, and scripts, reference documents, and templates can sit in the same folder when needed. At startup the agent reads only the name and description; when a matching task arrives it reads the full instructions; during execution it opens scripts or reference files. The spec calls these three stages "progressive disclosure."

The scale figures are company-announced. Anthropic said more than 70 agent products have adopted the format (it named ChatGPT, Cursor, GitHub Copilot, and VS Code as examples), that about 1 million skills have been published, and that there have been about 280 million installs. The German outlet MIXED added that these are the company's own counts, not independently verified user numbers. We take the same position.

The governance is in the announcement too. Engineers from Anthropic, Google, OpenAI, and others will maintain the standard as individuals rather than as company representatives, and the lead maintainers are David Soria Parra and Mahesh Murag. You can use and contribute without being a foundation member. It also listed three items of "what comes next": versioned releases, a formal process for proposing spec changes, and **security guidance for people who write and install skills**. As MIXED pointed out, these three are still proposals, not things that have shipped.

## 2. Version — the Claude API got its first new version in three years (facts)

One day earlier, on October 21, a new Claude API version, "2026-10-21," was released. Anthropic's version list in its documentation shows only three entries — 2023-01-01, 2023-06-01, and now 2026-10-21 — so this is the first new version in three years and four months. The developer account (@ClaudeDevs) said the new SDKs and CLI use this version by default (we could not open the X post directly; we confirmed it through the summary on the Korean aggregator promppy and Anthropic's official documentation).

Among the changes listed in the migration guide, these are the ones a small team is most likely to run into:

- **The temperature, top_p, and top_k parameters are gone.** Sending them even at default values returns a 400 error. The guide says code that relied on a low temperature for consistency loses that effect, and no other setting replaces it.
- **The authentication header changes.** The new SDK sends the key as Authorization: Bearer instead of X-Api-Key. A proxy or gateway in the middle that reads the old header needs updating.
- Placing a document block directly in an assistant message, or citations in a text block of a user message, returns a 400 error.
- Several response field names in the Admin API change (roles → role_ids, name → display_name, and so on).
- The Python SDK uses the new version from 2.0.0. The SDK and CLI licenses change to Apache 2.0.

The important point is that **the old version is not cut off right away**. The guide says existing SDKs keep sending the 2023-06-01 header so you can stay on your current version, and no end date for 2023-06-01 is written anywhere. "No end date" and "kept forever" are different statements, so we record only the former as confirmed.

## 3. Keys — API keys stored with a hosting provider may have leaked (facts)

On the same October 21, the app hosting provider Railway posted a security disclosure on its official blog. The gist: that morning it detected anomalous activity in the systems that store customer environment variables, and its investigation indicates that **an unauthorized third party may have accessed encrypted environment variables and, for some of them, obtained the decrypted contents**. Environment variables typically hold API keys and database and registry credentials. Railway wrote that it sees the incident as "part of a series of attacks recently targeting platform companies" with the aim of compromising AI inference providers.

The company took three actions. It notified upstream providers so they could revoke keys proactively, paused all deployments, and said it would email affected accounts as it confirms them. To users it strongly recommended, even though its initial analysis suggests the impact may be limited to a subset of users, that they **immediately roll all environment variables (including API keys and private registry credentials) and review the logs of those services for unusual activity**. The notice contains no numbers such as the count of affected accounts or leaked variables.

On social media and in some outlets there are claims around this incident that "stolen keys become cash on the black market right away," that "there is demand to generate training data for distillation," and that "hundreds of thousands of dollars drained from crypto wallets." We could not confirm any of these from Railway or law-enforcement material, so in this article we go no further than "such claims exist."

## Where the three stories meet in one folder (interpretation)

A skill folder is light: one SKILL.md and a few scripts. But that light folder leans on three things.

First, **the format**. The folder structure and the name and description fields have to follow the spec for other agent products to read them. While the spec lived inside one company, the rule was "when they change it, you follow." Now that it is at a foundation, it becomes "watch the versions and the proposal process and follow." Until the versioned releases and security guidance the foundation promised actually appear, this is in practice not very different from today.

Second, **the API version the scripts call**. If a script inside a skill passes temperature, or goes through a proxy that reads the X-Api-Key header, that skill breaks quietly the moment you upgrade the SDK. A skill is not something that ends with "it ran fine when installed"; it is something you have to run again every time the API version underneath changes.

Third, **where the keys the scripts use are kept**. Even if you never wrote a key into the skill itself, if the key sits in the environment variables of the server that runs the skill, and that server is at a hosting provider, then keys can leak from a place unrelated to your folder — as in this Railway incident. We think this is also why the foundation listed "security guidance for people who write and install skills" as a first task (this connection is our interpretation, not a reason the foundation stated).

## If it were us — three things we checked in our skill folders (practice)

Our company builds internal skills (app screen policy, data analysis procedures, article checks, and so on) in the SKILL.md format. This is the order in which we actually checked them after this week's news.

1. **Format check.** We confirmed that every skill's SKILL.md has a name and a description, and that the description says in one line "when to pull out this skill." Those two are the minimum fields the spec requires, and they are the only two the agent reads at startup. When the foundation's versioned release comes out, we decided to write that version number in the reference document inside each skill folder.
2. **Version check.** We searched the scripts in the skill folders for the strings temperature, top_p, top_k, and X-Api-Key. If any appears, that skill goes on the "fix before upgrading the SDK" list. We are not upgrading the SDK right now; we upgrade when the fix list is empty. If an end date for the old version is announced, we move the schedule up.
3. **Key check.** We searched again to make sure no key is written anywhere in the skill folders or the repository, and listed where keys live (a hosting provider's environment variables, a secrets manager). Keys entrusted to an outside provider are classified as "keys that leak together if that provider is breached," and we confirmed that usage alerts and spending limits are set for them. We judged that the "review logs for unusual activity" Railway recommended is only useful if it arrives as an alert in normal times, not after an incident.

These three are checks worth running once a quarter even when there is no news. In NO.5 we wrote that "instructions are debt, not assets," and skill folders are the same. The more folders you have, the more there is to check along the three axes of format, version, and keys.

## What we could not confirm in this news

- The more than 70 platforms, about 1 million skills, and about 280 million installs announced by Anthropic are the company's own counts, and we found no independent verification.
- We could not open the original @ClaudeDevs X post; we confirmed the new API version through Anthropic's official documentation (the version list and the migration guide). We could not confirm the exact new major version numbers of SDKs in languages other than Python from the documentation.
- There is no end date for the 2023-06-01 version in the documentation. We confirmed only that there is none.
- The scale of the Railway incident (account and variable counts), the attacker, and any link to other platform breaches are not in Railway's notice, and we could not confirm the figures from media and social media (wallet losses and so on).
- For the October 20 article on the reference site Learn:US (how to safely install skills made by others), we read only the public listing summary and could not open the body.

## What we read alongside

We directly opened sources of different kinds. Company and foundation announcements, official documentation, media, and personal blogs are listed separately.

Company and foundation announcements:

- [Donating Agent Skills to the Agentic AI Foundation (Anthropic)](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) — English, company announcement (figures are the company's counts)
- [Agentic AI Foundation Announces Four New Projects: Agent Skills, Open Responses, OpenEnv, and OpenSandbox (Linux Foundation)](https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox) — English, foundation press release
- [Security Disclosure: Wednesday October 21st (Railway)](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) — English, company notice

Official documentation and specification:

- [Agent Skills Overview (agentskills.io)](https://agentskills.io/) — English, specification site
- [Versions (Claude Platform Docs)](https://platform.claude.com/docs/en/api/versioning) — English, official documentation
- [Migrating to API version 2026-10-21 (Claude Platform Docs)](https://platform.claude.com/docs/en/api/migration-2026-10-21) — English, official documentation

News and summaries:

- [Anthropic hands its widely used AI skills standard to an independent foundation (MIXED)](https://mixed-news.com/en/anthropic-agent-skills-agentic-ai-foundation/) — English, media (notes the limits of company figures)
- [Anthropic releases new Claude API version 2026-10-21 (promppy)](https://www.promppy.com/item/2535081) — Korean, AI-summary aggregator (original source: X post)
- [Railway breach, AI API keys stolen (promppy)](https://www.promppy.com/item/2535863) — Korean, AI-summary aggregator (original source: X post, includes unconfirmed claims)

Personal blogs and practitioner sites:

- [Donating Agent Skills to the Agentic AI Foundation (Simon Willison)](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) — English, personal blog (looks back at a December 2025 prediction)
- [Three skills to put into Claude before starting work (Learn:US)](https://learn.bizni.us/) — Korean, practitioner site (public summary only)
