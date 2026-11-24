---
no: 17
slug: which-ai-for-which-job
date: 2026-10-03
category: Practice
tags: Choosing a model · Recommendations by task · Cost · Testing it yourself
title: Which AI for Which Job — The Uses Companies State Themselves and the Test We Use
summary: Documents, coding, voice, images, bulk processing. We gathered the uses each company recommends in its official materials, and laid out a way to find out in 30 minutes whether one fits your work.
---
> This article was drafted together with AI (Claude) and reviewed by an editor. Because it also covers Anthropic, the maker of Claude, we used as our basis only **what each company wrote about its own products**; these are not independent test results comparing them against each other. We do not say that either side is better.

"Which AI is good for this job?" is hard to answer in a single line. What is written in the official documents, though, is **which uses each company recommends.** We gathered those by task.

## What Companies Recommend by Task

- **Everyday documents, slides, spreadsheets, and well-defined bug fixes:** Anthropic points to Claude Sonnet 5.5 for these uses. It is the faster and cheaper option.
- **Long, complex development work (large code migrations, reviews):** Anthropic recommends Opus 5.5, and OpenAI recommends GPT-6.1 Sol (coding, computer use, professional work). Both have published their own scores for this use.
- **Long-running development work, agents that work automatically:** Google's documentation introduces Gemini 3.8 Flash for this use.
- **Voice assistants, speech synthesis:** Google points to Gemini 3.8 Live for low-latency voice conversation and Gemini 3.8 Flash TTS for expressive speech synthesis.
- **Images:** Google points to Nano Banana Pro for 4K resolution and complex compositions that include text, and Nano Banana 2 for fast bulk production.
- **High-volume work where price matters most:** Anthropic's documentation suggests starting with a small Haiku-class model and moving up if it falls short, and Google points to Gemini 3.1 Flash-Lite.

## Switching Models Is Not the Only Way to Cut Costs

Anthropic's documentation says that before switching models, you should try **adjusting intelligence against speed and cost with the "effort setting."** Both companies also offer "caching," which cuts the price substantially when the same input is used repeatedly (OpenAI $0.10, Anthropic $0.20, each per million tokens). It is very effective if you attach the same instructions every time.

## The 30-Minute Test

We have shortened the sequence suggested in Anthropic's documentation in our own way.

1. Pick three tasks you do every week (for example: organizing meeting minutes, drafting customer replies, tidying up a table).
2. Prepare one piece of real material for each, with personal information removed.
3. Enter the same instruction into two tools in exactly the same way.
4. Write down three things: accuracy, the number of places you had to fix, and the time it took.
5. If the scores are similar, choose the cheaper one; if it is work that must never be wrong even once, choose the one with the higher score.

## Our Interpretation

**Fact:** Companies guide by use, and they take their scores from their own evaluations.

**Interpretation:** There is no "best AI," only "the cheapest AI that fits my work." The scores companies announce are only a starting point, and the standard is the result confirmed with your own materials.

**What we would do:** We do not pile all our work onto one tool; we use a small model for light work and a large model only for hard work. And we rerun the same test every three months, because models change so fast.

## Further reading

Everything here was confirmed by directly opening the official documents below. The scores and uses are each company's claims.

- [Choosing a model (Anthropic Docs)](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) — English
- [Claude Sonnet 5.5 (Anthropic)](https://www.anthropic.com/claude-sonnet-5-5) — English
- [Introducing GPT-6.1 Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-1-sol/) — English
- [Gemini models (Google AI for Developers)](https://ai.google.dev/gemini-api/docs/models) — English
