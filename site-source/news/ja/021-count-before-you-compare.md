---
no: 21
slug: count-before-you-compare
date: 2026-10-09
category: インサイト
tags: 数字の読み方 · 売上の会計処理 · トークン価格 · 1件あたりのコスト
title: 数字を比べる前に数え方を確認する — 700億ドルが500億ドルになった理由と、トークン価格の落とし穴
summary: 同じ「年換算売上」や「トークンあたりの価格」も、何を数えるかによって意味が変わります。今週の報道2件から、数字の読み方を整理しました。
---
> この記事はAI(Claude)と共同で下書きを作り、編集者が確認しました。AnthropicとOpenAIの両方が登場し、AnthropicはClaudeの開発元のため利害関係があります。いずれの企業や銘柄についても投資意見ではなく、数値はすべて報道と企業の発表から転記したものです。

今週のAI業界で最も目を引いた数字の話題は、性能ではなく「数え方」でした。

## 事例1. 同じ会社の売上が700億ドルから500億ドルになった理由

Axiosは10月8日、OpenAIの年換算売上は先月広く報じられた700億ドルではなく500億ドルだと伝えました。700億ドルは投資家に共有された資料に由来する数字で、Anthropicとより直接比較できるように「かさ上げ(gross up)」して計算したものだといいます。違いは、クラウドパートナー経由の販売をどう計上するかです。Axiosが引用した会計学の教授によれば、顧客がクラウド事業者を通じて100を支払った場合、Anthropicは100全体を売上に計上し事業者の取り分を費用として記載できる一方、OpenAIは一部のパートナー販売で自社の取り分だけを売上に計上します。どちらも会計基準(GAAP)には適合しているとされています。

ロイターも10月9日、OpenAIが投資家に示した9月の年換算売上は500億ドルをわずかに下回ると伝えました。先に700億ドル近いと示していた数字との差は、Anthropicと直接比較しようとしたことから生じたもので、OpenAIはAnthropicと違い、AWSやGoogle Cloudなどクラウドパートナー経由の販売を売上に含めていないという説明です(最初に報じたのはフィナンシャル・タイムズ)。

年換算売上はある期間の売上を1年に引き延ばして見る、シリコンバレーでよく使われる指標で、Axiosは公開市場の投資家は通常、実際の売上を好むとも付け加えています(いずれもAxiosとロイターの報道に基づく。両社の会計資料は私たちは確認していません)。

## 事例2. トークンあたりの価格が下がっても、1件あたりの価格は同じとは限らない

AnthropicはHaiku 5.5の価格がHaiku 4.5より平均約75%低いと発表しました(企業の発表)。しかしNext.inkは、外部の分析会社を引用して、このモデルは回答が長めで節約幅はeffort設定によると伝え、10万トークンを超えるリクエストはトークン単価が5倍になる点にも触れました。AI Weeklyのニュースレターも、コスト負担からより安いモデルに移る企業を取り上げ、「完了した作業1件あたりのコスト」を測るよう助言しています(この号は他メディアの報道の要約であり、元の報道は私たちは確認していません)。

## 数字を読むための3つの質問

1. **何を数えた数字か?** 総額か純額か。トークンか、完了した作業1件か。
2. **誰が出した数字か?** 企業自身か、独立した第三者か。両者が違うなら、測定条件は何か。
3. **条件を変えるとどうなるか?** 最高effortでのスコアは既定の段階で変わりうるし、長いリクエストでは単価が変わりうる。

## 私たちの解釈

**事実:** 同じ会社の年換算売上が、数え方によって700億ドルとも500億ドルとも報じられ、トークン価格の低下と1件あたりのコストの低下は必ずしも一致しないという指摘が今週出ました。

**解釈:** 数字は、単位と数え方が同じ場合にだけ比較できます。会社どうしの比較だけでなく、自分たちの数字を見るときも同じです。

**私たちなら:** 私たちの収益報告では総額と純額を分けて書き、AIの作業はトークンではなく「記事1本、動画1本、注文1件」あたりの費用で記録します。他社の数字を引用するときは、出典と数え方を必ず併記します。

## あわせて読んだ資料

性質の異なる5つの出典を直接開いて確認しました。

- [OpenAI annualized revenue $20 billion less than previously reported (Axios)](https://www.axios.com/2026/10/08/openai-50-billion-arr-anthropic-revenue-accounting) — 英語、報道
- [OpenAI's September annualized revenue nears $50 bln, less than previously indicated (Reuters、Zawya掲載)](https://www.zawya.com/en/special-coverage/openais-september-annualized-revenue-nears-50bln-less-than-previously-indicated-source-says-1586243) — 英語、通信社報道
- [Introducing Claude Haiku 5.5 (Anthropic)](https://www.anthropic.com/claude-haiku-5-5) — 英語、企業の公式発表
- [Chez Anthropic, Haiku 5.5 prend la relève des petits modèles rapides (Next.ink)](https://next.ink/260659/chez-anthropic-haiku-5-5-prend-la-releve-des-petits-modeles-rapides/) — フランス語、メディアの分析
- [AI got too expensive, so companies are moving to cheaper models (AI Weekly #535)](https://aiweekly.co/issues/ai-got-too-expensive-so-companies-are-moving-to-cheaper) — 英語、ニュースレター
