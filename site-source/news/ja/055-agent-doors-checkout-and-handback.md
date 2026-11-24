---
no: 55
slug: agent-doors-checkout-and-handback
date: 2026-11-23
category: 実践
tags: AIエージェント · エージェンティックコマース · Google Connected Apps · Universal Commerce Protocol · Booking Holdings Vayo · 決済の引き渡し · Sabre MCP · Grok · ユナイテッド · アップセル · エージェント経由価格 · 商品情報
title: エージェントが決済ボタンの手前まで来た — Googleは検索の中で食料品の買い物の決済を開き、Booking Holdingsのエージェントは「許可しない供給会社では決済画面を客に引き渡す」と書き、Sabre(セーバー)は「客は結果をめくって見ず、一つか二つしか見ない」と言って取引エンジンをまずGrokに差し込み、ホテルのCEOは「エージェントは衝動買いをしない」と言って門を閉じると述べた — 店が今週決めるのは四種類の門のうちの一つだ
summary: Googleは11月20日、米国で検索とGeminiアプリのConnected Appsを通じてAlbertsons・Safeway・Shaw's・Targetの食料品の注文を作り、決済まで終える機能を開いたと発表しました(Universal Commerce Protocol基盤・価格・数値なし)。Booking HoldingsのAI旅行エージェントVayoは11月17日、「直接連携があれば連携で、なければ予約サイトを探索して予約し、供給会社がエージェント予約を許可しなければ価格を確認したうえで決済画面を旅行者に引き渡す」とプレスリリースに書きました(非公開ベータ)。旅行流通網の会社Sabre(セーバー)は11月16日、Grok Botマーケットプレイスに初の旅行プラグインを載せ、「MCPサービスを試験・運用中のパートナー80社以上」と発表し、CEOはメディアに「客は結果をめくって見ず、一つか二つ、多くても三つしか見ない」と語りました。反対側ではホテルチェーンのCEOが「人は販促に揺れるがエージェントは揺れない」と言って自社ホテルのエージェント予約を止めると述べ、Booking HoldingsはLLM経由の予約が「1%にはるかに届かない」と語ったとSkiftが伝えました。四つを「門の種類・取っ手・一つか二つしか見えない陳列台・まだ小さな数字」でまとめ、コマース・アプリ・AIインフルエンサーを運営する小さなチームが今週決める一枚(門の表)を書きます。NO.45・47・50・53の「エージェントの門」実践編です。
---
> この記事はAI(Claude)とともに作成し、編集者が検収しました。当社はAnthropicとOpenAIの2社の有料顧客であり、Google・Metaのモデルも試験に使っています。利害関係を先に書きます — **この記事の主題である「店側の決定」は私たち自身の仕事です。**私たちはコマース(Hangeul Cubs)・アプリ(CourtMateなど)・AIインフルエンサー(Lia)を直接運営しているため、「私たちなら」の節は私たちが実際にやることを書いたものであり、どのプラットフォームかを勧める記事ではありません。1番のGoogleのニュースは私たちが試験に使う会社の発表であり、3番のSabreが2027年の拡張対象としてメディアに語ったプラットフォームの一覧には、この記事を書いたAIを作ったAnthropicのClaudeが入っています(プレスリリースには名前がありません)。そのため、どの会社にも評価を加えず、発表された数字と文章だけを移し、会社が発表した数値は「会社が発表したもの」として、1か所からしか出ていない内容はその出典を併記しました。この記事は特定企業に対する投資意見ではありません。

NO.45でユナイテッド航空が「客のエージェント」を門の外に立たせた日にOpenAIが店々をChatGPTの中に入れたことを、NO.47でOpenAIがエージェントに財布を握らせたことを、NO.50でShopifyの店が「エージェントがしてよいこと」を一枚で自動掲載し始めたことを、NO.53でMetaのエージェントがカナダの食料品の買い物で決済まで入ったことを書きました。今週の四つのニュースは、その門が**どんな形に固まっていくのか**を見せています — Googleは検索の中に決済の門を開き、Booking Holdingsのエージェントは「許可しない店では決済画面を客に引き渡す」という中間の門を書き、Sabreは店とエージェントの間の「取引エンジン」の座を取ろうとし、ホテルチェーンは門を閉じる理由を数字で語ります。会社発表三つ(Google・Vayo・Sabre)とメディア報道・コラム(Skift・PhocusWire)を、事実・解釈・私たちならに分けて書きます。

## 1. Google「年末の用事をConnected Appsで」 — 検索の中で食料品の買い物の決済まで (事実・会社発表)

Googleの公式ブログ記事**「Get your year-end tasks done with new Connected Apps」**(11月20日、筆者表記なし)を直接読みました。米国で**検索とGeminiアプリのConnected Appsを通じてAlbertsons・Safeway・Shaw's・Targetの食料品の注文を作り、決済まで終えられる**という発表です。記事はこれらの食料品アプリが**「Universal Commerce Protocol(UCP)基盤」**だと書き、別のコマース記事にリンクしています。金融は**Experian**がGeminiアプリにすでにあり、今回検索へ拡大されて信用スコアの確認と個人ローンの比較ができ、税金は**H&R Block**を検索から呼び出して税額計算・還付の推定ができ、**Angi・Thumbtack**(地域の修理・装飾の人材)は「数週間以内」に検索へつながると書きました。**価格・手数料・利用数値・正確な提供開始日・米国外の日程は記事にありません。**数値が一つもない発表です。

背景二つを併せて読みました。第一に、10月28日のGoogle開発者向け記事**「Build and manage Connected Apps in one place」**(検索・Geminiアプリの製品責任者2名の名前)。Connected Apps Platformをプレビューとして開き、開発者は**クラウドMCPサーバーまたはAndroid MCP(AppFunctions API)で連携**し、**Google Connected Console**で登録・試験・提出して検索・Geminiアプリのどこに載せるかを選び、公開後はトラフィック・遅延・エラー率と認証済みのロゴ・アカウントを管理します。「50以上のConnected Apps」がすでに出ており(生産性・チケット・健康・フィットネス)、Adobe・Experian・Localiza・PelotonがGeminiにあり、検索へは「数週間以内」に来ると書きました。この記事にはUCP・手数料・審査期間・国の一覧がありません。第二に、Target(ターゲット)の公式資料**「How Target is Shaping Shopping Experiences in Conversational AI」**(6月18日更新)。Targetは、Google検索(AI Modeを含む)・Geminiアプリ、Microsoft Copilot、OpenAI ChatGPTの**三つのプラットフォームで決済ができる初の大型小売店**だと書き、Googleでの流れを「質問 → 選択肢 → 「Buy」 → Targetアカウントにログイン → 確認」、決済はGoogle Payのクレジットカードか Target Circleカード、そして**「複数商品の一括決済は準備中」**(6月時点)と書きました。数値は一つ — **「AIが連れてきたトラフィックが第1四半期に前年比2,000%増えた」**(Targetが発表したもの、小売全体は約400% — Adobeの資料を引用)。7月の第1次Connected Apps(Instacart・Canva・YouTube Music、米国・オプトイン・購入はユーザー承認 — eWeek 7月17日)から今回の11月の食料品決済まで4か月です。

## 2. Booking Holdings Vayo「旅行の全部を予約する」 — 連携・探索・そして「決済画面を客に引き渡す」 (事実・会社発表・メディア)

Booking Holdings傘下のAI旅行スタートアップ**Vayoのプレスリリース**(11月17日、シアトル、PR Newswire — 私たちはfinvizの転載版で読み、原文のアドレスが併記されています)と、PhocusWire・Skift(テック担当アドリアナ・リー記者、11月17日)の記事を読みました。提供開始から1か月でVayoが**航空・ホテル・バケーションレンタル・レストラン・アクティビティ・公演チケット・レンタカー・鉄道・バス・フェリー・空港送迎・駐車場まで**予約するという発表です(非公開ベータの会員に当日提供、待機リストあり)。

方法がこの記事の核心です。プレスリリースは**「直接連携のある所は連携で、ない所は予約サイトを探索して旅行者の代わりに予約を完了する」**と書き、**「供給会社がエージェント予約を支援しない場合、Vayoは最善の選択肢を見つけて価格を確認したうえで、すぐに終えられるよう準備された決済画面を旅行者に渡す」**と書きました。すべての予約は旅行者の承認が必要で、**供給会社の確定を受けた後にのみ「確定」と表示**します。ログインは**1Password for Agents**でパスワードを見たり保存したりせず、決済は**StripeのLinkエージェントウォレット**で決済情報を見ずに終えると書きました。価格 — **Booking.comが最善の選択肢であるとき、すべてのVayo旅行者はBooking.comの最高ランクGenius Level 3の価格(一部の宿泊施設で最大20%割引)**を受けます。Vayo自体の料金・供給会社の一覧・予約件数はプレスリリースにありません。PhocusWireはVayoのCEO(マイク・フリジェン)の言葉として**「ユナイテッドのように許可しない所では決済画面を引き渡し、許可された経路で協力する機会を歓迎する」**を伝え、Booking Holdingsが提供開始時に**「製品の進展と市場状況を条件に1億ドルを投資する計画」**を明らかにし、ニューヨークのLola(KAYAK創業者たち)にも同じ金額を発表したと書きました(1億ドルはPhocusWire・Skiftの2媒体、プレスリリースにはなし)。Skiftは直接連携がBooking.com(ホテル・レンタカー・アクティビティ)・OpenTable・SeatGeekで、航空・鉄道などは許可された供給会社サイトの探索だと書き、Genius価格が比較においてBooking自体の在庫を有利にしうる点(Skiftの分析)、そして**Skift Researchの10月調査で米国の旅行者の27%だけがAI予約に抵抗がないと答え、AIの比重が「インスピレーション」段階21%対「予約」段階6%**という数字を付けました。予約件数・決済画面を引き渡した比率は会社が公開していません。

## 3. Sabre「取引エンジン」 — Grok Botに初の旅行プラグイン、「MCPパートナー80社以上」、「客は一つか二つしか見ない」 (事実・会社発表・メディア)

旅行流通網(GDS)の会社Sabre(セーバー)の**プレスリリース**(11月16日、テキサス州サウスレイク、PR Newswire — finviz転載版)と、PhocusWire、Skift(11月19日、同じ記者)を読みました。Sabreは11月17日のニューヨークの投資家デーで**Grok Botマーケットプレイスに載る「初のグローバル旅行プラグイン」**を先行公開し、対話型の予約・管理窓口**Mosaic Travel Connectorを「近くベータ」**で出すと発表しました。2025年に出したMCPサーバーとエージェント向けAPIの上に載り、**「MCPサービスを試験または運用中のパートナーが80社以上」**(会社発表・試験/運用の区分と名前なし)と書きました。新たに発表した**「イベント駆動API」**は欠航・遅延のシグナルを監視して影響を受ける旅行者を特定し、旅行会社のシステムとつながったAIツールに通知を押し込み、対応は**人間の相談員・コネクタが会話の中に規定に合う選択肢を出して一度のタップで承認・自律エージェントが直接処理**の三経路だと説明します。価格モニタリングはベータ、「2027年中に主要な対話型モデルと旅行会社のワークフローへ拡張」が計画で、**料金・収益条件・手数料はプレスリリースにありません。**Grok以外のプラットフォーム名もプレスリリースにはありません。

メディアが加えたもの。PhocusWireはSabreのCEOカート・エカートが第3四半期の決算発表で**「LLMプラットフォームはまだ消費者より企業側の機会に集中している」**と語ったと伝え、Skiftはエカートの言葉として**「消費者は結果をページをめくって見ることはなく、一つ・二つ・多くても三つの選択肢を受け取ることになる」**を移し、2027年の拡張対象として**ChatGPT・Claude・Gemini**を書きました(この三つの名前はSkiftの報道、プレスリリースにはなし)。Skiftの要約には「いま旅行会社に与えているインセンティブがLLMとの収益共有の形に変わりうる」というエカートの考えと、「経済性は実証されておらず、複数年の見通しからはおおむね外れている」というSkiftの評価がありますが、この箇所は本文ではなく記事の要約ブロックにあるため、**Skift要約1か所**として置きます。

## 4. 反対側 — 「エージェントは衝動買いをしない」と「LLM経由の予約は1%にはるかに届かない」 (事実・メディアコラム・会社発言)

Skift創業者ラファト・アリのコラム**「The AI Agent Is Travel's Ad Blocker」**(11月18日)を読みました — **最初の5段落までが開き、その先は有料の壁**のため、後半は記事の要約ブロックだけで読みました。開いている本文の要旨はこうです。旅行会社の収益は決済段階の衝動買い(良い座席・客室のアップグレード)から出るのに、**旅行者の代わりに予約するエージェントは衝動買いをしない** — だからアップセルの利益が危ない、ということです。ホテルチェーンMCRのCEOタイラー・モースが今月初めのSkift Commerce Summitでこの心配を語り、要約ブロックによれば**「人は販促に揺れるがエージェントは揺れない」と言って自社ホテルのエージェント予約を止めたい**と述べました。アナリストCitizensの11月15日の報告はエージェント二つ(Instinct・MetaのMuse)で予約を試して「印象的ではなかった」としながらも、オンライン旅行会社に長期的なリスクが大きいと見て、露出の順位をExpedia・Booking Holdings・Airbnb(最も少ない)の順に書きました(Skiftの伝聞・方法未確認)。

要約ブロックにだけある数字は**Skift要約1か所**として書きます — 航空の付帯収益2025年1,570億ドル・全体の約16%(2016年は674億・9.1%、IdeaWorksCompany推定)、Expediaの第3四半期の広告売上2億600万ドル、AirbnbのCEOの「広告10億ドルの機会」発言、SkiftがInstinctに「広告の配置は推薦に影響するか」と尋ねたときの答え「配置は私が使うシグナルではない」、**Booking HoldingsがLLM経由の予約を全ルームナイトの「1%にはるかに届かない」と語ったこと**、そして**ウィンダムが自社のAI電話相談員は公示料金より平均15%高い料金で予約すると語ったこと**(「エージェントも売れる」の例としてコラムが挙げたもの)。ユナイテッドのエージェント制限(NO.45)が同じ日に発表され、その理由は売上ではなく「セキュリティ・規制リスク」だった点も要約にあります。

## 短く二つ (事実・会社発表)

- **Google「他のAIアプリの履歴をGeminiへ移す」**(11月19日) — 五つの手順です: Geminiのインポート設定でプロンプトをコピー → 以前のAIツールに貼って好みの要約を受け取る → その答えをGeminiに貼る → 以前の提供元のアカウントから会話履歴をZIPでエクスポート → Geminiの設定にアップロード。どの提供元が対応するのか・容量の上限・料金プラン・保管条件は記事にありません。**「乗り換える門」**です — NO.48「モデルを替えるのに数週間かかる」の消費者側の版です。
- **Google Gemini API「Tool Retrieval」**(11月19日、プレビュー) — エージェントがツールを数十・数百個付けるとき、すべてのツールのパラメータ仕様を毎回送らず、名前・説明だけを置いて必要なときに仕様を呼び出せるようにする機能です(`tool_search`ツール + 保留するツールに`defer_loading`)。リモートMCPサーバー全体を遅延ロードすることもでき、別途の課金はなく(呼び出した仕様はその後入力トークンとして課金)、**節約の数値は記事になく「自分のトラフィックで測定せよ」**と書きました。1番のConnected AppsがMCPで連携されるのと同じ場所です — 店が出す「ツール」が増えたときの技術です。

## 四つを合わせて読むと (解釈)

第一に、**門は四つに分かれました — 直接連携、探索許可、決済の引き渡し、禁止。**NO.45で「客のエージェントは止め、店は入れる」と書いた二つの間に、Vayoが中間の門二つを書きました。「探索許可」はエージェントが店のサイトを人のように回って予約を終えることで、「決済の引き渡し」はエージェントが**価格の確認まですべて済ませておき、最後の決済ボタンだけを客が押す**ことです。重要なのは、**エージェントが「決済の引き渡し」の門からでも私たちの決済ページの手前まで来る**という点です — 店が何も決めなくても、エージェントはサイトを読み、カートを満たし、客を決済画面の前に立たせることができます。ですから「私たちの店はエージェントと無関係だ」という選択肢はなく、**四つのうちどの門かを決めることだけが残ります。**ユナイテッド(セキュリティ・規制)とMCR(アップセル)が「禁止」を選んだ理由が互いに異なる点も書き留めておきます — 禁止にも理由が二種類あります。

第二に、**取っ手は規格であり、小さな店は規格を選ぶ側ではなく追いかける側です。**Googleの食料品決済はUCPの上に、Connected AppsプラットフォームはMCPの上に、Sabreの取引エンジンもMCPの上に、Shopifyの店はpoppy.json(NO.50)の上にあります。三つの規格が競争しているように見えますが、店側から見れば共通点のほうが大きいです — **商品・価格・在庫・条件を機械が読める形式で出し、「してよいこと」を書き、決済はウォレット(Stripe Link・Google Pay)が代わりに持つ。**Sabreの「80社以上」は試験と運用を分けていない数字で(会社発表)、Googleの「50以上」はアプリ数であって取引量ではありません。規格がいくつ生き残るかは私たちには決められませんが、**商品情報1枚を正確に作ること**はどの規格が勝っても必要です — NO.53の「エージェントが読む商品情報1枚」が今週最も安い準備です。

第三に、**「一つか二つしか見えない」が陳列台を変えます。**エカートの「消費者はページをめくらず、一つ・二つ・三つだけを受け取る」という言葉は、検索広告時代の「10件の結果のうち上位」の競争が**「エージェントの選択基準に入るか」の競争**に変わるという意味です。そしてVayoのGenius Level 3は**「エージェント経由価格」という新しい欄**を見せています — 同じ部屋を人がサイトで買う値段とエージェントが買ってくれる値段が違いうること、その差がどの在庫を選ぶかに影響しうることはSkiftも指摘しました。ラファト・アリの「広告ブロッカー」の論点はその反対側です — エージェントはアップセルを買わないので、決済画面の「もう一つ勧める」収益が減りうる、ということ。ウィンダムの「AI電話相談員は15%高く売る」(Skift要約1か所)は、**店側のエージェントは売れる**という反例としてコラムが挙げたものです。まとめると、店は二つを決めなければなりません: **客側のエージェントに見せる価格・条件、そして私たち側のエージェントが勧めるもの。**

第四に、**数字はまだ小さいです — だから今決めるのが安い。**Booking Holdingsの「1%にはるかに届かない」(Skift要約1か所)、Skift Researchの「予約段階6%」、エカートの「LLMプラットフォームはまだ企業側」、Citizensの「印象的ではなかった」、そしてNO.43のAirbnb「ごくわずか」・NO.40のUber「最も忙しい週に4件」 — 客側のエージェントが実際に決済まで行く比率は、どの会社の数字でもまだ一桁の下にあります。Googleは数値を一つも発表していません。ですから今週やることは**連携の開発ではなく、門の種類を書くこと**です — お金がかからず、エージェントが増えた後に直すよりはるかに安いです。そして引き渡された決済画面が壊れていれば(ログインの壁・期限切れのカート・CAPTCHA)、Vayoのルールどおり**「確定」は供給会社の確定後にのみ**表示されるので、壊れた決済画面は売上ではなく「予約されず」で終わります。

## 私たちなら — コマース・アプリ・AIインフルエンサーを運営するチームが今週書く一枚 (実践)

1. **門の表一枚 — 私たちの商品・サービスごとに四つのうち一つを書く。**Hangeul Cubsの商品、CourtMateの有料機能、Liaチャンネルのコラボ問い合わせ、アプリのサブスクリプション — 行ごとに**直接連携 / 探索許可 / 決済の引き渡し / 禁止**のうち一つと理由(決済・返金リスク、在庫、規制)を書きます。デフォルトは**「決済の引き渡し」**に置きます — エージェントがカートまで作り、決済ボタンは人が押す流れです。その次に**私たちの決済ページがその流れを壊さないか**を人が一度歩いてみます: ログインの壁、短いセッション期限、CAPTCHA、カートのリンクが共有できるか。Vayoのルール二つをそのまま借ります — **注文は私たちのシステムの確定があってこそ「確定」**、**承認は件ごと**([NO.54](https://www.apholdings.kr/ko/news/agent-roster-and-incident-log/)「エージェント名簿・事故日誌」の「お金を語る文には出典必須」と同じ行)。「禁止」を選んだ行には、ユナイテッド式(セキュリティ)なのかMCR式(アップセル)なのか理由を書きます。
2. **取っ手は商品情報1枚から — 規格は後で選ぶ。**Shopifyの店はpoppy.json(NO.50)がすでにあり、Google Connected AppsコンソールとUCPは米国限定なので、いま私たちができるのは**エージェントが「価格を確認」するときに引っかからない情報**です — 価格・在庫・配送日・返金条件・サイズ規格を一か所に、機械が読める形で(構造化データ・商品フィード)、そして**サイト二か所に異なる価格がないように。**Vayoが「価格を確認したうえで」決済画面を引き渡すと書いた理由がここにあります — 不一致はエージェントでは「選ばれない」で終わります。Sabreの「80社」・Googleの「50」は私たちの決定の根拠ではなく、「規格が三つ以上回っている」というシグナルとしてだけ読みます。
3. **「一つか二つしか見えない陳列台」に入るための条件二行と、エージェント経由価格一行。**エージェントが選択肢を一つか二つに絞るとき、私たちの商品が入るには**比較可能な条件**(配送日・返金・総額)が書かれていなければなりません — Hangeul Cubsのセット、バスケットシューズのおすすめ記事ごとにその二行を入れます。そしてGenius Level 3のように**エージェント経由の注文に別の価格・条件を置くのか**を一行で決めます(私たちの答えは「同じ価格、アップセルなし」から始めます — ラファト・アリの論点どおり、決済画面の「もう一つ」はエージェントには通じないので、アップセルの代わりにセット構成そのものを商品に置きます)。Liaの台本には「エージェントが客の代わりに選ぶ時代」を学ぶトーンで、数値は「reported」としてだけ入れます。私たち自身のAI利用の側では「乗り換える門」を一度歩いてみます — 会話履歴をエクスポートしてみて、エクスポートできない知識があればNO.48の原則どおりモデルの外の文書へ移します。

## 今回選ばなかったもの

OpenAIのチーフサイエンティストの**「Perplexity and Intelligence」**(11月22日 — 内部パープレキシティ数値の公開と研究所共通の「上限」提案)は今週最大の評価・安全のニュースですが、この記事の主題(店の門)と筋が異なるため**次の記事で別に扱います**(NO.52・54の続報、OpenAIのアラインメント・展開安全ページの点検とともに)。NAVER AI Labの**Unfinished-Bench**(「エージェントがルールを書いた後に破った89%」、AI Weeklyの伝聞・arXiv原文未閲覧)と**SimAudit**(ロボットベンチマーク採点器の欠陥61件、伝聞)も同じ次の記事の資料です。Lean・Mathlibコミュニティの**「リーマン予想の証明の認証」**共同声明(11月21日)は直接開きましたが、**文中にAIツールの言及がなく**AI Weeklyの見出しの「Claudeの助け」は確認されず、この記事を書いたAIの製造元に関わるため書きません。Anthropicの上場完了・「主幹事の条件」(ロイターの見出し)・Next.inkの上場記事は投資のため見出しだけ。全米州知事協会の「連邦AI規則・州法維持」声明(11月22日)はNO.39の続報候補。OVHcloudのオープンウェイトモデルOlala(Next.ink)はNO.51の続報候補。ル・フィガロ–OpenAIのコンテンツ契約(Next.inkの見出し)はNO.42の続報候補。GoogleのRSSのWatch Duty山火事警報・量子・クリーンエネルギーの記事、カナダのサイバーセンターのOracle Java警報はAIのニュースではないか距離があるため外しました。Learn:US 42号(クロード・トレーダー・スキル)は投資領域のため見出しだけ。KayakのAI機能28個(Skiftの見出しだけ)・LolaのCEOのMuse批判(見出しだけ)・OpenAIのChatGPT旅行人材の採用(抜粋だけ)は本文を開かなかったため書いていません。11月20日の草稿(オリーブヤング「ディファイン:オムニ」・GPT-6.2の値下げ)はまだホームページになく、リンクしていません。

## このニュースで確認できなかったこと

- Google Connected Appsの食料品決済は会社発表であり、価格・手数料・利用数値・正確な提供開始日がありません。「UCP基盤」の説明記事(コマース側の別記事)とConnected Apps対応アプリ一覧のページは開いていません。10月28日の記事の「50以上」はアプリ数で、取引数値はありません。Target資料の「2,000%」はTargetが発表した第1四半期の数値で、測定方法は資料になく、6月の資料のため11月の食料品決済の流れ(複数商品決済の有無)はその資料では確認できません。メディア2か所(MediaPost・Search Engine Land)の関連記事は開けませんでした。
- VayoのプレスリリースはPR Newswireの原文ではなくfinvizの転載版で読みました(原文アドレスの表記あり)。供給会社の一覧・直接連携の範囲(Booking.com・OpenTable・SeatGeek)はSkiftの報道であり、プレスリリースにはありません。予約件数・決済画面を引き渡した比率・Vayoの料金は公開されていません。「1億ドル」はPhocusWire・Skiftの2媒体で、プレスリリースにはなく、条件(製品の進展・市場状況)はPhocusWireの表現です。Skift Researchの27%・21%・6%はSkift自体の調査で、標本は記事にありません。
- Sabreのプレスリリースもfinvizの転載版です。「80社以上」は試験・運用の区分のない会社の数値です。「ChatGPT・Claude・Geminiへ2027年に拡張」・「収益共有」・「経済性未実証」はSkiftの記事(一部は要約ブロック)で、プレスリリースにはGrok以外のプラットフォーム名がありません。「SpaceXSI」がプレスリリースの引用文に出てきますが、その役割の説明がないため書いていません。SabreのIRサイトで開いたプレスリリースは2025年9月のものだったため、今回の発表の確認には使っていません。
- Skiftのコラムは最初の5段落だけが開き、Booking Holdings「1%のはるか下」・ウィンダム「15%」・IdeaWorks 1,570億・Expedia 2億600万・Instinctの回答・ユナイテッドの理由は**記事の要約ブロック**でのみ読みました(本文との照合はできず)。Citizensの報告の方法・標本は確認できませんでした。MCRのCEOの発言はSkiftの伝聞です。
- Googleの履歴移行の記事は対応提供元・上限・料金プランがなく、Tool Retrievalの記事は節約の数値がありません(会社は「測定せよ」と書いています)。
- どの会社の発表も、私たちが直接試験したものはありません。私たちの「門の表」は今週始めるものであり、決済ページを歩いてみた結果は次の記事に書きます。

## 併せて読んだ記事

性格の異なる出典を直接開いて確認しました。会社発表・公式文書、メディア報道・コラム、私たちの以前の記事に分けて書きます。

会社発表・公式文書:

- [Get your year-end tasks done with new Connected Apps (Google、11月20日)](https://blog.google/products-and-platforms/products/search/connected-apps-holiday-errands/) — 英文、Albertsons・Safeway・Shaw's・Targetの食料品決済・UCP・Experian・H&R Block・Angi・Thumbtack・数値なし
- [Build and manage Connected Apps in one place (Google、10月28日)](https://blog.google/innovation-and-ai/technology/developers-tools/connected-apps-one-place/) — 英文、Connected Apps Platformプレビュー・MCPサーバー/Android MCP・Connected Console・50以上
- [How to transfer your chat history into Gemini (Google、11月19日)](https://blog.google/innovation-and-ai/products/gemini-app/switch-ai-assistants-transfer-history/) — 英文、5段階・ZIPインポート
- [Introducing Tool Retrieval in the Gemini API (Google、11月19日)](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/) — 英文、tool_search・defer_loading・リモートMCP遅延ロード・別途課金なし・節約数値なし
- [How Target is Shaping Shopping Experiences in Conversational AI (Target、6月18日更新)](https://corporate.target.com/press/fact-sheet/2026/06/conversational-ai) — 英文、三つのプラットフォームでの決済・UCP・Buy→ログイン→確認・Google Pay・「複数商品決済は準備中」・AIトラフィック2,000%(会社)
- [Booking Holdings' Vayo Now Books the Entire Trip (Vayoプレスリリース、11月17日 — PR Newswire、finviz転載)](https://finviz.com/news/424035/booking-holdings-vayo-now-books-the-entire-trip) — 英文、連携/探索/決済の引き渡し・承認・供給会社の確定・1Password for Agents・Stripe Link・Genius Level 3最大20%・非公開ベータ
- [Sabre Accelerates Agentic Travel Leadership with First-Mover Travel Experience within Grok Bot and Next-Gen Proactive Travel APIs (Sabreプレスリリース、11月16日 — PR Newswire、finviz転載)](https://finviz.com/news/423683/sabre-accelerates-agentic-travel-leadership-with-first-mover-travel-experience-within-grok-bot-and-next-gen-proactive-travel-apis) — 英文、Mosaic Travel Connectorベータ・Grok Bot初のプラグイン・MCPパートナー80社以上・イベント駆動API・2027拡張・料金なし

メディア報道・コラム:

- [Booking Holdings' AI Agent Vayo Can Now Reserve Flights and Hotels (Skift、11月17日)](https://skift.com/2026/11/17/booking-holdings-ai-agent-vayo-can-now-reserve-flights-and-hotels/) — 英文、直接連携Booking.com・OpenTable・SeatGeek・Skift Research 27%/21%/6%・Genius価格の比較への影響
- [AI agent Vayo adds travel booking (PhocusWire、11月)](https://www.phocuswire.com/news/startups/ai-agent-vayo-adds-travel-booking) — 英文、1億ドル投資の条件・Lola・CEO「ユナイテッドのように許可しない所では決済画面を引き渡す」
- [Sabre Wants to Be the Transaction Engine Behind AI Travel Bookings (Skift、11月19日)](https://skift.com/2026/11/19/sabre-wants-to-be-the-transaction-engine-behind-ai-travel-bookings/) — 英文、CEO「一つ・二つ・三つ」・ChatGPT・Claude・Gemini 2027・収益共有(要約ブロック)・経済性未実証
- [Sabre brings conversational travel booking to Grok (PhocusWire、11月)](https://www.phocuswire.com/sabre-brings-conversational-travel-booking-grok) — 英文、投資家デー11/17・CEO「LLMプラットフォームはまだ企業側」
- [The AI Agent Is Travel's Ad Blocker (Skift、ラファト・アリのコラム、11月18日 — 前半のみ無料)](https://skift.com/2026/11/18/the-ai-agent-is-travels-ad-blocker/) — 英文、衝動買い・MCRのCEO・Citizens 11/15・Booking「1%のはるか下」・ウィンダム15%(要約ブロック)
- [Google Brings Third-Party Apps Into Search AI Mode for Everyday Tasks (eWeek、7月17日)](https://eweek.com/news/google-ai-mode-connected-apps) — 英文、7月の第1次Connected Apps(Instacart・Canva・YouTube Music)・米国・オプトイン

私たちの以前の記事:

- [週間AIニュース — 価格は下がり限界は書かれ、エージェントはデスクトップとカートへ (AP News NO.53)](https://www.apholdings.kr/ko/news/weekly-2026-11-21/)
- [「してよいこと」をエージェントが来る前に書いておく三つの文書 (AP News NO.50)](https://www.apholdings.kr/ko/news/allowed-list-before-the-agent-arrives/)
- [モデルを替えるのに数週間かかる (AP News NO.48)](https://www.apholdings.kr/ko/news/model-swap-takes-weeks-keep-knowledge-outside/)
- [週間AIニュース — Googleは5日間でモデル三つと検索を変え、OpenAIはエージェントに財布を握らせ、ユナイテッドは「客のエージェント」を門の外に立たせた (AP News NO.47)](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [客のエージェントは止め、店は入れ、モデルは全員に (AP News NO.45)](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [客は自分のエージェントを連れてこられない (AP News NO.43)](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [スコア表に確率が付いた — Uberは最も忙しい週にエージェントが取った配車を4件と数えた (AP News NO.40)](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [AIが客を連れてくる玄関が三つになった (AP News NO.38)](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
- [確認コードがエージェントの手に届いたら (AP News NO.36)](https://www.apholdings.kr/ko/news/agents-raised-their-own-spending-caps/)
