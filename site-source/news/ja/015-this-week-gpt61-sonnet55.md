---
no: 15
slug: this-week-gpt61-sonnet55
date: 2026-10-03
category: 週間ニュース
tags: 週間AIニュース · GPT-6.1 Sol · Claude Sonnet 5.5 · Gemini 4 Argon
title: 今週のAIニュース — 二社は「より安く」、Googleは「より強く、まず一部に」
summary: 9月最後の週、OpenAIとAnthropicは同じ仕事をより安くこなすモデルを、GoogleはGemini 4 Argonをまず一部に公開しました。何が変わったのか、働く人にとってどういう意味があるのかを、公式資料で確認してまとめました。
---
> この記事はAI(Claude)と一緒に初稿を作り、編集者が検収しました。Anthropicはこの記事の執筆に使ったClaudeを作った会社です。利害関係がありうるため、すべての数値を「会社が発表したもの」と明示し、他社のニュースも同じ基準で扱いました。

> **訂正 (2026-10-03)** 最初に公開した記事では「Googleの公式資料でGemini 4の公開を確認できなかった」と書いていました。Googleは9月30日に公式ブログでGemini 4 Argonを発表しています。タイトル、冒頭の段落、3番の項目を訂正し、出典を追加しました。

今週(9月28日〜10月3日)の大きな発表は三件でした。OpenAIとAnthropicは、**性能が上がったという話よりも先に、値段が下がったという話**を出し、Googleは最も強い新モデルをまず一部に開く道を選びました。

## 1. OpenAI — GPT-6.1 Sol

OpenAIはGPT-6.1 Solを紹介する中で、「以前の最上位モデル(GPT-6 Astra)に近い知能を、はるかに低いコストで」と説明しています。開発者向け価格は、入力100万トークンあたり2ドル、出力10ドル、繰り返し使う入力は0.10ドルです。OpenAIは、コーディングと業務自動化の評価でAstraと同程度のスコアを約5分の1のコストで出したと発表しました。また、低い推論強度では事実誤りの率が11.4%から7.7%に下がったとのことです。(すべてOpenAIの発表した数値です。)

**知っておきたい点:** OpenAIのページによると、ChatGPTの「Work」とCodexで先に公開され、一般のチャットにはまだ提供されていません。対象は有料プラン(Plus・Pro・Business・Enterprise・Edu)です。

## 2. Anthropic — Claude Sonnet 5.5

AnthropicはSonnet 5.5を「以前のSonnet 5より30%以上速く、ほとんどの作業でコストが最大30%少ない」と紹介しています。トークン単価は据え置き(入力2ドル、出力10ドル)で、同じ仕事を**より少ないトークンで**終えるため値段が下がる、という説明です。同じ月の22日には上位モデルのOpus 5.5が登場し、Anthropicはこのモデルが「Opus 5より、通常の作業基準で40%少ないコストで動く」としています。AnthropicはSonnet 5.5を、文書・スライド・スプレッドシートの作成やバグ修正のような範囲の明確な日常作業向けに、Opus 5.5を判断が必要な複雑な仕事向けに分けています。フランスのIT系メディアNext.inkは、単価が下がっていない点を指摘したうえで、効率によって値段が下がる仕組みだと整理しています。

## 3. Google — Gemini 4 Argon、最も強いモデルはまず一部に

Googleは9月30日、公式ブログでGemini 4 Argonを発表しました。まずGoogleのFairwindプログラムを通じて信頼できるサイバーセキュリティの防御者だけに公開し、安全対策を整えたうえで、有料APIの顧客とGoogle AI Ultraの契約者から広げるとしています。二社が「値段」を前面に出したのに対し、Googleは「最も強いモデルを慎重に開く」ことを前面に出した形です。性能の数値は、Googleの発表以外に独立した検証を確認できなかったため、載せていません。

**知っておきたい点:** 10月1日に更新された開発者向けモデルのドキュメントで、いますぐ使える安定版はGemini 3.8 Flash(長時間の開発作業・エージェント向け)、画像向けのNano Banana Pro(4K・文字表現)、音声向けのGemini 3.8 Liveです。人の投票による順位サイトArenaにもGemini 4 Argonが載っています。詳しくは今週あわせて公開した「誰がよく使われているか」の回をご覧ください。

## 私たちの解釈

**事実:** 二社が同じ週に「同じ仕事をより安く」を打ち出しました。

**解釈:** モデルが良くなったからではなく、**使うときの値段が下がった**ことで、個人や小さな会社の選択肢が変わります。毎日回す仕事なら、性能スコアよりも「一件を処理するのにかかるお金」のほうが重要になりました。

**私たちなら:** いま使っているツールを替える前に、毎週やっている仕事を三つ選び、二つのモデルに同じ内容を頼んで、時間と結果を記録しておきます。方法は「作業ごとにどのAIを使うか」の回にあります。

## あわせて読んだ記事

この記事は、下記の公式発表と報道を直接開いて確認して書いたものです。数値は各社の発表であり、独立した検証を経たものではありません。

- [Introducing GPT-6.1 Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-1-sol/) — 英語
- [Claude Sonnet 5.5 (Anthropic)](https://www.anthropic.com/claude-sonnet-5-5) — 英語
- [Claude Opus 5.5 (Anthropic)](https://www.anthropic.com/claude-opus-5-5) — 英語
- [Claude Sonnet 5.5 : plus rapide, plus efficace, mais pas moins cher (Next.ink)](https://next.ink/brief-article/claude-sonnet-5-5-plus-rapide-plus-efficace-mais-pas-moins-cher/) — フランス語
- [Gemini models (Google AI for Developers)](https://ai.google.dev/gemini-api/docs/models) — 英語
- [Gemini 4 Argon: our next era of frontier intelligence (Google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) — 英語
