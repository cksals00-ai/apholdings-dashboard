---
no: 3
slug: ai-reads-the-label
date: 2026-10-03
category: Practice
tags: Connectors · MCP · Ingredient checking · Safelist
title: When AI Reads the Ingredient Label for You — How We Made It Stop Saying "It's Safe"
summary: Connecting an external tool to an AI assistant turns its answers from "a feeling" into "evidence." Here is the rule we set while building the Safelist connector: say only as far as "not seen."
---
> This article was drafted together with AI and reviewed by an editor. Safelist is not a diagnostic tool.

## The problem: the plausible answer is the most dangerous one

If you ask an AI, "Does this snack contain milk and wheat?", it will usually answer plausibly. But when AI answers from memory, it does not know the product has changed, and it will claim an ingredient is there when it is not, or miss one that is. When it comes to food, both are a problem.

## The solution: connect an external tool

Today's AI assistants can attach external tools through "connectors" (technically, a connection standard such as MCP). When asked a question, the AI queries public data directly instead of trying to recall, and passes along the result. The Safelist connector looks up a food's ingredients from public data of Korea's Ministry of Food and Drug Safety and shows whether it contains the ingredients the user avoids.

## Three rules we set

1. **Never say "it's safe."** The most the tool can say is "no item you avoid was seen." Cross-contact during production and labeling errors cannot be known from the data.
2. **Confirm the ingredients to avoid first.** Every child avoids different ingredients, so we set the criteria before looking anything up.
3. **Never remove the disclaimer.** The line at the end of each answer, "Not a diagnosis · Based on public DB · Final judgment rests with the guardian," stays even when summarizing.

## Generalizing: a framework for any task

The same framework works beyond ingredient labels.

- For questions where numbers or facts matter, **leave it to a lookup tool.**
- Make the tool **say it doesn't know** what it doesn't know.
- Write conclusions **only as far as the data allows.**

What makes AI trustworthy was not a bigger model, but a design that lets it say it doesn't know what it doesn't know.

## Try it yourself

You can find the Safelist app and AI connector in the Safelist introduction on our homepage. [See the AP Safe introduction](/en/products/safe/)
