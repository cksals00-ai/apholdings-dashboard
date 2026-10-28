---
no: 31
slug: genie-4-world-models-what-we-can-use
date: 2026-10-28
category: Insight
tags: World models · Genie 4 · Google DeepMind · Video production · AI influencers
title: Google built a "world with sound" — what Genie 4 shows about where world models stand, how to read an announcement with no numbers, and what a small video team should do now
summary: On October 27, Google DeepMind unveiled its world model Genie 4. You walk through a world made from a line of text in real time, change the weather, camera and people by talking, and for the first time the model generates music, ambient sound and dialogue along with the visuals. But the official post contains not a single number — no resolution, length or latency — and the only people who can use it so far are "trusted testers." We put the published figures for its predecessor Genie 3, rival Runway's model and AMD's acquisition of World Labs side by side to work out how far world models have come. Then we wrote down what a team like ours, which makes AI-influencer videos, should do right away with this news — and what it should not do.
---
> This article was written with AI (Claude) and reviewed by an editor. Anthropic, which makes Claude, competes with Google, the subject of this article, and our company is a paying customer of both Claude and Google's AI tools. Performance and features announced by a company are labeled as "what the company announced," and for any figure not in the official post we say which outlet reported it. This article is not a recommendation to buy or sell any company's shares.

The term "world model" spread widely from the title of a 2018 paper by David Ha and Jürgen Schmidhuber. The idea was that an agent learns a compressed model of how its surroundings change over space and time, practices inside that "dream" first, and then carries what it learned into the real environment. Eight years later, on October 27, Google DeepMind announced it had pushed that idea to the point where you "walk through a world built from one line of text in real time, fix the world by talking to it, and hear it as well." The announcement is dazzling, but it has no numbers. This article fills that gap with the published figures from the predecessor and from competitors.

## 1. Genie 4 — what the company announced (facts)

Google DeepMind published Genie 4 on its blog on October 27 (authors Raia Hadsell, Diego Rivas and Hang Qi). The features the company described are as follows.

- **It makes sound along with the world.** The company wrote that Genie 4 is "our first real-time world model to generate audio natively." Each world gets its own ambient sound and music, and characters hold dialogue that adapts to inputs and events.
- **You fix it by talking while it runs.** While the simulation is running, you can change the scene in natural language — "make it rain," "pull the camera back," "add a person" — and Gemini adapts each instruction to the surrounding scene while keeping the world moving.
- **Physics and human motion.** It imitates physical phenomena such as aerodynamics and collisions, and the company says characters respond to their environment and move naturally.
- **Gemini plays "director."** Gemini 3.8 Flash observes the scene, breaks goals into steps, checks the incoming frames to confirm each step happened, and revises the plan when the world shifts or a user intervenes. In a robotics experiment, Gemini 4 Argon splits a task into steps and sends them to Genie like captions, and the example shows Apptronik's humanoid Apollo playing checkers.
- **Who can use it.** For now it is a research preview for "trusted testers." The company said it will roll out in turn to Google AI Ultra subscribers through Project Genie and to early-access partners of the Gemini API and AI Studio; there is no general release date. The Project Genie waitlist is open.
- **It wrote down its own limits.** The company said that "visual details and object permanence can still shift or drift over time," especially in longer sessions, after multiple edits or while navigating the scene, and listed complex physical interactions, real-time audio accuracy, legible text, spatial accuracy and long-term consistency as "ongoing research." Its own phrase is "an early, experimental model." All generated video and audio carries a SynthID watermark.

The post also lists the fields testers are trying. Filmmakers use it as a "draft mode" to run multiple takes while changing camera, lighting, dialogue and action; photojournalists turn a single 2D archival photo into an environment you can walk around; game developers quickly test visual styles and rules in words; and enterprise partners use it to generate scenarios fast.

**What is not in the official post.** Not one of resolution, frames per second, how long a session holds, latency, or any measured consistency figure appears in the DeepMind post or on Google's official blog. TechCrunch, citing a briefing, reported that it "maintains a consistent scene for up to two minutes, double the limit of Genie 3," and the Korean outlet DigitalToday quoted TechCrunch for the same figure. In other words, "two minutes" is a number from one line of media reporting and is not in any official document. What TechCrunch relayed from DeepMind engineer Rivas is more candid than any figure: the stage where real-time interaction is most valuable is "ideation and storyboarding," and "the end-to-end product experience is not yet clear."

## 2. The numbers are in the predecessor and the competitors (facts)

When an official post has no numbers, we put the same company's previous announcement and competitors' published figures next to it.

- **Genie 3 (Google DeepMind, August 5, 2025).** The official post had numbers: 720p resolution, 24 frames per second, real-time navigation, "environments that stay largely consistent for several minutes," and "visual memory reaching back up to one minute." It was a limited research preview open only to a small group of academics and creators. The limitations listed then were the range of actions agents can take, interactions between multiple independent agents, accurate reproduction of real geography, text rendering, and "minutes, not hours." It is striking that Genie 4's list of limitations is almost identical. Sound and the "director" were added; the limits stayed.
- **Runway GWM Worlds 2 (September 3, 2026).** The world model from the video-generation company Runway is also a research preview. The figures in its official post: 720p, 24 frames per second, generation with no fixed length, audio at 48 kHz. Dialogue is handled as a text "action." Its stated limits: "real-time generation trades fidelity for speed," "quick camera rotations degrade textures and geometry," "long-term memory is imperfect," and "image references work only for the first frame." That means Runway attached sound about two months before Google, but Google's "first" is qualified by its own criterion — "among real-time world models" — so the two claims do not necessarily collide. We have no way to compare the two companies' criteria.
- **AMD's acquisition of World Labs (September 28, 2026, AMD filing).** The chipmaker AMD said it will acquire World Labs, founded by Fei-Fei Li, in an all-stock deal valued at about $8.2 billion. The filing describes World Labs as a "spatial-intelligence model" company that generates, reconstructs and simulates interactive 3D environments from text, image and video, and also mentions technology for robotic learning and simulation. Li will become AMD's executive vice president and chief scientist when the deal closes, expected by the end of 2026. The filing does not use the words "world model."

TechCrunch also mentioned a Wall Street Journal report that Amazon is in talks to buy Decart for around $7 billion, and Rivian's acquisition of Third Dimension, but we could not find official material and do not cover them here.

## How to read an announcement with no numbers (interpretation)

First, **"first" and "most" are only true inside the criterion the company chose.** Google's "first to generate audio natively" carries the condition "real-time world model," and Runway put out a real-time world model with sound as a preview about two months earlier. Neither is wrong; the two companies drew different lines. The superlatives in an announcement should be read only after you find that line.

Second, **where a number is missing, the predecessor's number is the ceiling.** If Genie 3 was 720p, 24 fps and "several minutes," and the Genie 4 post gives no figures, there is no basis for assuming resolution or length grew noticeably. The "two minutes" the press reported is not far from Genie 3's "several minutes," either. The safe reading is that this release's real progress is in features — **sound, steering, direction** — rather than in numbers.

Third, **the "limitations" paragraph outlives the "features" paragraph** — the same conclusion as yesterday's article (NO.30). That Genie 3's and Genie 4's limitation lists are nearly the same means those problems went unsolved for a year and two months, and you can look for the same items first in the next generation's announcement. Text that cannot be read, objects that change the longer it runs, and sound that is not accurate — for anyone actually delivering video, those three matter more than the features.

Fourth, our own interpretation. Where world models are heading right now is **not "finished video" but "a practice ground for robots and agents" and "a storyboard for people."** Google led with a robot example, AMD put robot-learning simulation in its reasons for the acquisition, and Rivas named the most valuable stage as "ideation and storyboarding." The 2018 paper's idea of "practicing inside the dream" is intact. If a small team that makes video reads this news as "video generation got better," it has the wrong address.

## If it were us — three things a team making AI-influencer videos does this week (practice)

1. **Keep world models and video-generation models in separate boxes.** Our Ria videos are made today with video-generation models (script → scene → edit). Genie 4 is not a tool that replaces that slot; it is a **"draft mode" for running several takes in words before you settle on a scene.** That is the slot Google described with its "filmmaker's draft mode" tester example and Rivas's "storyboarding stage." So we write it down as a candidate only in the "scene ideation" box of our production order, never in the "final render" box. Rivas himself said turning prototypes into finished assets is "still a ways off."
2. **Join the waitlist, but do not change the workflow.** The Project Genie waitlist and Gemini API early access cost nothing to apply for. But since only "trusted testers" can use it today and there are no official figures, we tie no production step to this tool until it arrives. When it does, we run our ten scenes (Ria's store introduction, the ingredient-label explanation scene, the basketball-shoe comparison scene and so on) through the test method from NO.17 and record three items first: **whether text is legible, whether the character stays the same within two minutes, and whether the sound matches the scene.** The three limits the company wrote down itself are our checklist.
3. **Line the watermark up with our disclosure.** Every Genie 4 output carries a SynthID watermark. Our Ria video policy already requires "the AI persona to be stated," so the direction is the same. But a watermark is a mark platforms read and our disclosure is a mark people read, so neither substitutes for the other. We write the rule now: if a scene made with a world model goes in, the caption disclosure gains "parts of this scene are AI simulation." Writing the rule before the tool arrives is always cheaper.

## What we did not pick this time

Anthropic's two announcements of October 27 (early results in drug development, expanded cooperation with the U.S. General Services Administration) and Axios's exclusive that "the FTC is demanding testimony from Anthropic executives" were left out because the conflict of interest is large and they are not yet cross-checked. We have not yet read OpenAI's three posts of October 26 (academic cooperation, the CodeRabbit case, "ChatGPT's expanding world of work"). The LiteLLM 1.107.0 supply-chain attack (October 21, confirmed in the company's incident report) and the Brotli compression-library flaw disclosed by OpenAI are a different kind of story and will be covered separately in the next article as "the AI tool supply chain." For Amazon–Decart and Rivian–Third Dimension we could not find official material.

## What we could not confirm in this story

- Genie 4's resolution, frames per second, session length and latency are not in the official post. "Up to two minutes, double Genie 3" is TechCrunch's report (quoted by DigitalToday) and we could not confirm it in any official document.
- "First real-time world model to generate audio natively" is the company's own criterion, and we could not verify how it differs from Runway GWM Worlds 2 (September 3).
- We have not used Genie 4 ourselves. Every feature description comes from the company's post and briefing coverage, and we found no independent measurement.
- The timing for Project Genie and the Gemini API is given only as "in turn" and "in the coming weeks" (TechCrunch), so we could not fix a date.

## What we read alongside

We opened sources of different kinds directly. They are grouped as company documents, filings, papers, media reports and our earlier articles.

Company documents:

- [Genie 4: A new generation of world simulation (Google DeepMind)](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) — English, official announcement (features, limits, availability; no figures)
- [We're announcing Genie 4, our new world model for real-time interactive simulation (Google)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-genie-4/) — English, Google's official blog (rollout order)
- [Genie 3: A new frontier for world models (Google DeepMind)](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — English, the predecessor's official announcement (720p, 24 fps, "several minutes," one minute of memory)
- [Introducing GWM Worlds 2 (Runway)](https://runway.com/research/introducing-gwm-worlds-2) — English, a competitor's official research post (720p, 24 fps, 48 kHz audio, limits)

Filings:

- [AMD to Acquire World Labs to Advance the Future of AI Compute (AMD Investor Relations)](https://ir.amd.com/news-events/press-releases/detail/1299/amd-to-acquire-world-labs-to-advance-the-future-of-ai-compute) — English, company filing (about $8.2 billion all-stock, expected close)

Papers:

- [World Models — David Ha, Jürgen Schmidhuber (arXiv, 2018)](https://arxiv.org/abs/1803.10122v1) — English, the starting point of the "world model" idea

Media reports:

- [Google's Genie 4 world model adds audio, more realistic worlds, and real-time steering (TechCrunch)](https://techcrunch.com/2026/10/27/googles-genie-4-world-model-adds-audio-more-realistic-worlds-and-real-time-steering/) — English, tech outlet (briefing, "two minutes," Rivas's remarks, market context)
- [Google DeepMind Rolls Out Genie 4 World Model in Research Preview (Unite.AI)](https://www.unite.ai/google-deepmind-rolls-out-genie-4-world-model-in-research-preview/) — English, AI outlet (cross-check of the official post, Genie 3 comparison)
- [Google DeepMind unveils Genie 4 world model, targeting robots and film production (DigitalToday English)](https://www.digitaltoday.co.kr/en/view/120253/google-deepmind-unveils-genie-4-world-model-targeting-robots-and-film-production) — English, Korean outlet (quoting TechCrunch)

Our earlier articles:

- [The price you pay is halved, the cost of making it runs to billions a month (AP News NO.30)](https://www.apholdings.kr/ko/news/half-price-terra-and-the-s1-compute-bill/) — Korean, how to read "the limits a company writes down itself"
- [Which AI for which job — the uses companies state themselves and the test method we use (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — Korean, our per-task model test method
