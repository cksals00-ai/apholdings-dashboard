---
no: 5
slug: instructions-are-debt
date: 2026-10-03
category: Insight
tags: Instructions · Prompts · Cleanup
title: Instructions You Give AI Are Debt, Not an Asset — Why We Try Deleting Them Every Quarter
summary: The belief that piling up rules makes AI smarter may be wrong. Here is how to cut instructions down and measure whether cutting them causes any problem.
---
> This article was drafted together with AI and reviewed by an editor. It draws on an external article, which is credited at the bottom.

When we put AI to work, we add one more rule each time it gets something wrong. "No tables," "Use polite speech," "Cite sources." After a few months, the instruction document grows to twenty or thirty lines, and we call it an asset. But we have rarely checked whether those rules are really doing any work.

## Rules are easy to add, and their effect is hard to verify

The article we referred to makes this argument: as models improve, rules that were once needed become unnecessary, and unnecessary rules are not harmless; they **increase the total amount that must be followed and blur even the important rules**. It cites benchmark research showing that compliance falls as the number of instructions grows. We could not check that figure against the original, though, so we take it only as "there is such research." What matters more in practice is the direction. **The more rules there are, the more AI can silently skip some of them, and we do not know what was skipped.**

## The cleanup standards we set

1. **Once a quarter, clear the instructions entirely.** Run the same task without instructions and look at the result.
2. **Add lines back one at a time and look at the difference.** If adding a line does not change the result, delete it.
3. **Be suspicious of rules with no "why" written down.** A rule whose reason no one can explain is often the trace of a single incident.
4. **Set standards rather than prohibitions.** One line, "Who is the reader of this piece," changes more than ten lines of "don't do this."
5. **Do not delete rules about irreversible actions.** Rules on deleting, paying, sending and publishing stay regardless of performance.

## Summary

Instructions are not an asset to stockpile but equipment that costs money to maintain. Try cutting them, and if there is no difference, it is lighter and safer to keep them cut.

## Further reading

This article was rewritten from our own team's perspective and standards, drawing on the concerns raised in the articles below. We did not follow their wording or structure, and where we could not verify a figure an original article cited against the primary data, we marked it as such. For some of the original articles, the full text opens only after logging in, so we read them based on the publicly available portion.

- [AI Hasn't Gotten Dumber — It's the Instructions You Wrote Six Months Ago Holding It Back (Korean) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-claude-md-rules)

Also checked against other sources:

- [How Many Instructions Can LLMs Follow at Once? (IFScale, arXiv)](https://arxiv.org/abs/2507.11538) — English
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — English
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — English
- [Lost in the Middle: How Language Models Use Long Contexts (arXiv)](https://arxiv.org/abs/2307.03172) — English
