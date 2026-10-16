---
no: 22
slug: meta-muse-wonder-whose-scorecard
date: 2026-10-15
category: インサイト
tags: Meta · Muse Wonder · モデル評価 · 独立評価 · 学習設定
title: Meta初のトップ級モデル「Muse Wonder」— 点数は誰がつけたのか、使う前に見る3つのこと
summary: Metaが10月12日、初のフロンティア級モデルを公開した。会社発表の点数と独立した評価機関の点数を並べ、価格・使える場所・学習設定という、私たちの仕事で使う前に確認する3点を整理した。
---
> この記事はAI(Claude)と一緒に作成し、編集者が確認しました。比較対象として登場するClaudeモデルを作るAnthropicは、この記事を書くのに使ったツールの提供元でもあるため、私たちには利害関係があります。会社が発表した数値は「会社発表」と、独立した評価は別に表示します。特定の企業・銘柄に対する投資意見ではありません。

10月12日(月)、MetaのSuperintelligence LabsがMuse WonderとMuse Wonder Fullの2モデルを公開した。Metaが「初のフロンティア級モデル」と呼ぶものだ。このニュースで注目したいのは点数そのものより、誰がどんな条件で測ったのかである。

## 何が出たか(事実)

- Muse WonderはMetaのモデルAPIと、コーディングツールのMuse Codeで使える。API価格は入力100万トークンあたり4ドル、出力100万トークンあたり20ドル(キャッシュ入力は0.20ドル。独立評価機関Artificial Analysisによる)。
- Muse Wonder FullはMuse Code契約者専用。APIでは提供されない(TechCrunch)。MetaのMuse Code契約案内によると、Fullは4つのプランのうち上位2つ(Power・Maximum)に含まれ、この2プランは月50ドルと200ドルだとLetsDataScienceとDataNorthが伝えた。
- 両モデルともコンテキストは100万トークン、入力はテキスト・画像・動画・音声、出力はテキスト(Artificial Analysis)。
- 両モデルの重み(ウェイト)をダウンロードできるかどうかは確認できなかった(できないと書いたのはLetsDataScienceの1か所のみ)。Decryptは、重みを公開していたLlamaシリーズをMetaが事実上終えたと指摘した。

## 点数表の読み方

**会社発表。** Metaは自社指標「Personal Superintelligence Index」でWonder Fullが59.1点となりOpus 5.5(55.2)やGPT-6 Astra(54.5)を上回り、記憶テストMemoryBenchでも約85.5点で先行すると述べた(Decryptが伝えたMetaの主張。iThome・Latent Spaceの報道も同じ数値)。Decryptは、この2つの指標はMetaが作ったもので、指数の計算式は非公開だと書いている。

**独立評価。** Artificial Analysisの総合指数(v4.3、最大努力設定)では、Wonder Fullが56点、Wonderが52点、Metaの前モデルMuse Spark 1.3が48点だ。同じ指数でOpus 5.5は58点、Sonnet 5.5は56点、GPT-6 Astraは53点である(Artificial Analysisのランキング表で直接確認、各モデルの最高設定)。つまり独立評価では「3位前後」であり、会社指標の「上回る」とは様子が違う。

**もう少し詳しく。** Artificial Analysisは同じ記事で、コーディングエージェント指数でWonder Fullは68点、Sonnet 5.5を使うClaude Codeと同じで、Opus 5.5(66)より高いと書いた。一方、知識問題AA-OmniscienceではFullが30点、Wonderが25点で、Opus 5.5(46)やGPT-6 Astra(43)をかなり下回る。もっともらしい誤りを作る率(ハルシネーション率)はFullが23%、Wonderが27%と低めだが、指数45点以上のモデルで最も低いのはGemini 4 Argonの15%である。

## 使う前に見る3つのこと(解釈)

**1. 1件終わらせる費用。** トークン単価が同じでも、仕事1件の費用は違う。Artificial Analysisが同じ課題群を回した費用は、Wonderが4.52ドル、Opus 5.5が5.98ドル、Sonnet 5.5が5.46ドル、GPT-6 Astraが3.26ドル、Gemini 4 Argonが1.99ドル、GPT-6.1 Solが0.72ドルだった。同程度の知能の他モデルより高めという評価だ。価格がOpus 5.5と同じという報道もある(Decrypt)が、私たちが見る数字は単価ではなく1件あたりの費用である。

**2. どこで使えるか。** 最も点数が高いWonder Fullは契約の中でしか使えず、APIで私たちの自動化に組み込めない。APIで使えるのは、点数が一段低いWonderだ。

**3. 自分のコードや文章がどこへ行くか。** MetaのMuse Code契約案内によると、契約は初期設定が「Contributorモード」で、プロンプト・コード・ファイル・コンテキストと受け取った回答をMetaが今後のモデルの学習に使う代わりに利用量が増える。オフにするとそれ以降の内容は学習に使われないと案内にあるが、すでに送った内容がどうなるかは書かれておらず、確認できなかった。API経由のWonderにはこのモードがなく、標準モードの内容は学習に使われないという。Metaの利用規約の原文は私たち自身では開けなかったので、使う前に規約と設定画面で確認が必要だ。

## 確認できなかったこと

Metaの公式発表とモデルカードは直接開けなかった。上の「会社発表」はTechCrunch、Decrypt、iThomeなどの報道を通じて確認した内容だ。契約と学習設定は、MetaのMuse Code契約案内ページを直接開いて確認した。Metaが約束した完全な安全性レポートはまだ出ていないとDecryptは伝えた。実利用者のSimon Willisonは、Wonderに推論レベルが6段階(minimalからmax)あり、前のモデルより絵が良くなったようだと書いたが、1種類の絵による非公式の試験だと本人が断っている。点数のように読んではいけない。

## 私たちの考え

**事実:** MetaがAPIと契約でのみ使えるトップ級モデルを出した。会社指標と独立指標は見える絵が違う。最上位モデルは契約専用で、契約の初期設定は自分のコンテンツを学習に使う。

**解釈:** 新モデルが出るたびに「1位だ」と「3位だ」が同時に出てくる。どちらも嘘ではないかもしれない。誰が作った試験か、どの設定で測ったかが違うからだ。

**私たちなら:** 数字で乗り換えない。自分たちの仕事20件(台本の下書き、商品説明、コメント分類)を同じ条件で回し、「1件あたりの費用」と「直した回数」を記録して、人が確認してから出す。顧客情報と未公開資料は、学習に使われうる設定には入れない。

## 併せて読んだ記事

性格の異なる出典を直接開いて確認した。数値は各出典によるものである。

- [Meta releases its first frontier model, Muse Wonder (TechCrunch)](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder) — 英語、報道
- [Muse Wonder / Wonder Full evaluation (Artificial Analysis)](https://artificialanalysis.ai/articles/muse-wonder) — 英語、独立評価機関
- [Meta Muse Wonder and the frontier AI race (Decrypt)](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race) — 英語、報道(会社指標と独立指標)
- [Meta's best model skips API, coding plan trains on your code (LetsDataScience)](https://letsdatascience.com/blog/metas-best-model-skips-api-coding-plan-trains-on-your-code) — 英語、契約と学習設定
- [llm-meta-ai 0.2 (Simon Willison)](https://simonwillison.net/2026/Oct/12/llm-meta-ai/) — 英語、実利用者のブログ
- [Meta releases Muse Wonder, its first frontier-class AI model (AI Weekly)](https://aiweekly.co/alerts/meta-releases-muse-wonder-its-first-frontier-class-ai-model) — 英語、ニュースレター(他媒体の要約)
- [Muse Code Subscriptions (Meta)](https://dev.meta.ai/docs/muse-code/subscriptions) — 英語、Meta公式案内
- [Models Leaderboard (Artificial Analysis)](https://artificialanalysis.ai/leaderboards/models) — 英語、独立評価機関のランキング表
- [Meta's Muse Wonder (DataNorth)](https://datanorth.ai/news/metas-muse-wonder) — 英語、分析(プランと学習設定)
- [Muse Wonder報道 (iThome)](https://www.ithome.com.tw/news/179608) — 中国語(繁体字)、報道
