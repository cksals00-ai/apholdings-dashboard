---
no: 20
slug: check-before-you-install
date: 2026-10-09
category: Practice
tags: Skills · Plugins · Pre-install checks · Review analysis · Citing sources
title: Before you use a "paste it and you're done" AI setup — one checklist for review mining, skill finders, finance briefings and reel skills
summary: We bundled four "install and run" methods from a Korean newsletter this week and wrote down the four checks we make before installing, with the sources behind them.
---
> This article was drafted with AI (Claude) and reviewed by an editor. Some of the tools discussed come from Anthropic, the maker of Claude, so we have a stake. This is not investment or purchase advice. For the Korean articles we referenced, we read only the publicly visible opening and could not check the rest.

The Korean AI practice newsletter Learn:US again posted several "copy this and paste it into your AI" articles this week. Going by the publicly visible openings, there are four: a three-step method for finding complaints that no product has solved by reading product reviews; how to install a skill that finds other skills; how to get a morning market briefing from a finance plugin; and how to build a personal style file and draft scripts with an Instagram Reels skill. They are clearly useful. But the closer installing and running sit together, the easier it is to skip the checks in between. We go through four steps.

## Step 1. What are you installing? Check the source and read the contents

Anthropic's engineering article warns that a skill adds instructions and code to an agent, so a malicious one could leak data or cause unintended actions. Its advice: install only from trusted sources, and for less-trusted ones, read the bundled files and any instructions to contact outside endpoints first. Research points the same way. A paper that analyzed 31,132 skills from two skill marketplaces reported that 26.1% contained at least one "pattern warranting review" (the authors caution this does not mean malicious, and that skills bundling executable scripts were flagged more often; skills were collected in December 2025).

How we apply it: before installing, look at the maker, the license and the file list, and read any script once. The skill-installer repository vercel-labs/skills is MIT-licensed, and its documentation explains environment variables that turn off the usage telemetry. We prefer tools with that kind of documentation.

## Step 2. What can it reach? Start with minimum access

Connect mail, calendar, drive or payment information read-only first, and have a person press the button for anything that sends or deletes. This is the same principle as our earlier piece "Connect, then shorten the morning."

## Step 3. How do you trust the output? Cite a source for every figure

The finance plugin article sets a rule: attach a source to every figure in the briefing and mark any you could not verify. A good rule. The README of Anthropic's financial-services repository (Apache-2.0) also states that it is not investment, legal or tax advice, that outputs are drafts for professional review, and that it makes no investment recommendations and executes no transactions. We draw the same line. A briefing like this is a tool for gathering reading material, not for deciding what to buy.

## Step 4. Does it fit our work? Test review mining small

The idea of tabulating why people bought and what they disliked from reviews, then grouping complaints that recur across products but are solved by none, applies directly to commerce. We test it like this: use only the reviews of one or two products we sell ourselves, forbid guessing beyond what the reviews say, and compare the three "gap candidates" it produces against real customer inquiries. Reviews containing personal information are cleaned first.

## Our take

**Fact:** All four methods put installing and running close together, and the risks of the skills ecosystem are raised both in an official article and in a research paper.

**Interpretation:** "What to look at before installing" ages more slowly than "how to install." Tools change weekly, but the order of checks can be reused almost unchanged.

**What we would do:** When bringing in a new tool, make these four steps a one-page checklist and put only tools that pass on the approved list.

## Read together

Below are four Korean articles and four sources of different kinds.

Korean articles (only the publicly visible opening was checked):

- [3 steps to make revenue-generating digital products with Claude (Learn:US)](https://learn.bizni.us/learnus-review-to-product) — Korean
- [How to install a skill that finds skills and get your first recommendation (Learn:US)](https://learn.bizni.us/learnus-find-skills-guide) — Korean
- [How to install the Claude finance plugin and get your first briefing (Learn:US)](https://learn.bizni.us/learnus-claude-finance-plugin) — Korean
- [How to install the Instagram agent skill and get your first Reels script (Learn:US)](https://learn.bizni.us/learnus-instagram-agent-skill) — Korean

Materials checked from other sources:

- [Equipping agents for the real world with Agent Skills (Anthropic Engineering)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — English, official article
- [Agent Skills in the Wild: An Empirical Study of Security Vulnerabilities at Scale (arXiv)](https://arxiv.org/html/2601.10338v1) — English, research paper
- [vercel-labs/skills (GitHub)](https://github.com/vercel-labs/skills) — English, open-source repository
- [anthropics/financial-services (GitHub)](https://github.com/anthropics/financial-services) — English, open-source repository and disclaimer
