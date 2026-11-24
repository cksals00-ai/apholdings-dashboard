---
no: 50
slug: allowed-list-before-the-agent-arrives
date: 2026-11-17
category: インサイト
tags: エージェント · Poppy · Shopify · Meta Muse · Uber · エージェントセキュリティ · Apple · 健康AI · OpenEvidence · コマース
title: 「してよいこと」をエージェントが来る前に書いておく三つの文書 — Shopifyの全店舗は11月13日から /.well-known/poppy.json 一枚で「うちの店でエージェントがしてよいこと」を自動公開し、Uberは自社エージェント一つひとつに「許可された意図・制約・リスク等級」を登録してからでなければ動かさず、Appleは健康AIの回答に「臨床引用・懸念質問の検知・学習不使用」を付けて20万人に評価を任せた
summary: SierraとMetaが作った個人エージェント規格「Poppy」の1.0が11月13日に出ました。企業が自社ドメインの /.well-known/poppy.json という一つのファイルに「私たちは誰で、エージェントはどの入口から入って何をしてよいか」を書いておくと、客のエージェントがまずそれを読む方式で、Shopifyは全店舗にこのファイルを自動で公開し始め、MetaのMuseは訪れるすべてのサイトでこのファイルを最初に探します（会社発表）。Uberは11月6日のエンジニアリングブログで「本人確認は『誰か』にしか答えられず『この行動が文脈に合うか』には答えられない」として、エージェントごとに身元・所有者・許可された意図・制約・リスク等級を登録し、実行の瞬間に検問する構造を書きました（数値なし）。Appleは11月15日、OpenEvidenceとともに「健康AI利用研究」アプリを開き、米国の21歳以上最大20万人が臨床出典付きの回答を受け取って評価するようにし、「研究データはAIの学習に使わない」「懸念される質問は検知して医療従事者へ案内する」と書きました。三つを「行動が起きる前に許可範囲を文書に書く方式」としてまとめました。
---
> この記事はAI（Claude）とともに作成し、編集者が検収しました。当社はAnthropicとOpenAIの二社の有料顧客で、Googleのモデルも試験に使っています。1番のPoppyはAnthropicが最初に作った規格MCPの上に載っているため、その点を明記します。**当社はコマース・アプリ・AIインフルエンサーを自ら運営しているので、三つのニュースすべてで「文書を書かなければならない側」に立っています** — そのためどの会社の方式にも評価を加えず、文書に書かれていることと書かれていないことだけを伝えました。会社が発表した数値は「会社が発表したもの」と表記し、出典が一つしかない内容はその出典を併記しました。3番の健康に関する記述は医療上の助言ではありません。この記事は特定企業への投資意見ではありません。

NO.43で「客は自分のエージェントを連れてこられない」と書き、NO.45ではUnitedが「個人エージェントによる予約禁止」を発表したことを、NO.49ではAT&Tが「精度が90%台後半に届く前は自律権なし」という閾値を置いたことを書きました。今週の三つのニュースはその次の段階 — **「してよいこと」を行動が起きる前に文書に書いておく方式**です。店はエージェントが来る前にファイル一枚を、会社はエージェントを動かす前に登録簿一行を、Appleは回答が出る前に条件三つを書きました。事実・解釈・私たちならに分けて書きます。

## 1. Poppy 1.0 — 店が「うちでエージェントがしてよいこと」をファイル一枚に書く（事実、会社発表）

Sierra（元Salesforce共同CEOブレット・テイラーが率いるAI顧客対応の会社）は11月13日、公式ブログ（ブレット・テイラー、クレイ・ベイバー共著）で**「Personal Agent Protocol」— 愛称Poppy — 1.0**を出しました。10月6日にMetaとともに初めて発表し、10月9日に草案を出したあと「5週間、実際のウェブサイト・API・エージェントで草案を試験した」と書いています。規格の原文（personalagentprotocol.org）を直接読みました。方式はこうです — **企業が自社ドメインの `/.well-known/poppy.json` にJSON文書一つを置きます。** その中に `organization`（名前・ドメイン・ロゴ）、エージェントが入れる入口（`agent.protocols` 対話窓口、`apis` — OpenAPIまたはMCP、`web` — ブラウザセッション窓口、`tasks`、`extensions`）、そしてポリシー（`auth.disabled` ログインを切る、`web.disabled`「うちのサイトをブラウジングしないで」、`web.unscoped` ブラウザログインがアカウント全体へのアクセスか）を書きます。スコープごとに**`irreversible`（取り消せない行動）・`personal_data`（個人情報を含む）**の印を付ける `scope_hints` という欄があります。ログインはOAuth 2.0（PKCE・デバイスログイン RFC 8628）、セッションは署名付きの `Poppy-Session` トークンです。規格は「1.0は0.4に修正を加えたもの」と自ら書き、まだ扱っていない領域はロードマップページに回しています。Sierraの記事は、PoppyがMCP・OpenAPI・UCPといった既存規格の上に載っていること、コマース拡張はShopifyが共同で書いたこと、検証器の入った実装キットがあることを書いています。

参加企業は会社発表です。10月の初期デザインパートナー8社（Meta・Genesys・Instinct・NiCE・Rocket・Shopify・Stripe・Walmart）に60社が加わり**100社以上**（Affirm・デルタ航空・Salesforce・Twilio・Wayfair・Zoomなど）で、実際にオンにしたのはMercury（銀行 — 支払い要求は口座の承認ポリシーを通る）・Synchrony・ターキッシュ エアラインズ（マイレージ会員がビジネスクラスへのアップグレードを決済前に承認）です。二つの文がこの記事の中心です。**「すべてのShopify店舗が今やPoppyファイルを自動で公開するので、販売者が別途することはない」**（Sierra）— Shopifyは175か国以上の店を動かしており、カート・決済はUCPが、その前の「誰か・何をしてよいか」はPoppyが担います。そして**「MetaのMuseは訪れるすべてのサイトでPoppyを最初に探す」**。TNW（11月13日）はMuseの利用者を「1,000万人以上」と書き（媒体一つ）、1.0という番号でも規格が「草案」と表記され互換性が壊れる変更が来うること、VisaとMastercardが別のエージェント本人確認を作っていること、Amazonは客がMuseではなく自社エージェントを使うことを望んでいることを併せて書きました。

背景を二行置きます。Practical Ecommerce（9月24日）によると、Shopifyは9月8日 — Museが出た日 — Metaを「Agentic Storefronts」に加えて販売者の商品を既定でMetaに共有し（販売者は切れる）、Amazonは同じMuseに「許可されていないAIエージェントによるアクセスの継続は利用規約違反」という文言を出して遮断しました（NO.43）。CMSWire（10月7日）が伝えたSierra共同創業者の言葉は**「消費者がどのアクセスを与えるかを決め、企業がエージェントのできることの限度を決める」**で、Metaは「メールのように誰も所有しない規格」と言いましたが、ガバナンスモデルは公開されず、二社のパートナー一覧も互いに異なりました。規格サイトのフッターには**Apache License 2.0**と書かれています（personalagentprotocol.org、11月18日に直接確認）。標準化団体やガバナンス主体は明記されていません。決済はまだ中核ではなく「拡張の候補」です。

## 2. Uber — 「身元は『誰か』にしか答えない」、エージェントごとに許可された意図とリスク等級を登録してから実行の瞬間に検問（事実、会社発表）

Uberエンジニアリングブログ（11月6日、ショーン・タウト、マックス・ジュロヴィッチ、アディ・ラガヴェンドラ）の記事「Securing AI Agents: Lessons From Real-World Deployment」を直接読み、InfoQ（11月15日）が整理しています。出発点の文はこれです — **「従来の権限付与は『誰が』行動できるかは決められるが、エージェントがしようとする行動が文脈上適切かは判断できない。」**防ごうとするのはプロンプトインジェクション・ツールとメモリの汚染・目標の乗っ取り・行動のドリフト・ハルシネーションから出た行動です（手法は記事にもなく、私たちも書きません）。構造は三層です。**①配備前**：すべてのエージェントを「AI Registry」に登録し、身元・所有者・ペルソナ・**許可された意図（intents）・制約・依存関係・リスク等級**を書き、「Argus」という自動分析器がコード・プロンプト・設定・依存関係・エンドポイント・ツール呼び出し経路を調べて弱点を探し、ペルソナ・意図の下書きを先に作って開発者が確認します（MCPサーバーとツールも同じ手順）。**②実行中**：「AI Guard」がポリシー判断の地点として**ローカルに置いた小さな専用モデル**で動き、「Agent Guard」フックがエージェントとツール実行の境界で行動を捕まえて判断を適用します。見るのは、行動がペルソナ・許可された意図・意味上の制約に合うか、利用者の要求と役割に合うか、セッション全体の文脈で筋が通るかです。**③配備後**：エージェントの行動・ツール呼び出し・判断を一本に束ねた実行トレース（機微情報は伏せ、必要なときだけ内容を含む）と、記録した相互作用を新しいポリシーに**「再生」**して適用前に試す仕組みです。

直面した難しさも書かれています — **誤遮断と誤許可のバランス**（遮断せず記録だけするシャドーモード・再生・エージェント別の調整で扱う）、遅延（並列実行・大きな汎用モデルの代わりに小さな専用モデル）、開発者の摩擦（Argusの自動化）、そして「すべてのエージェントに同じ規則」が目的とリスクの異なるエージェントに合わなかったこと。記事は**「セキュリティ・精度・遅延・コスト・自律性・開発者体験は別々には最適化できない」**で締め、続編（ペルソナ・文脈ガードレール・可観測性・意図フィルタリング）を予告しました。**数値は一つもありません** — 誤遮断率・遅延・コスト・エージェント数のすべて。オープンソースかどうかも書かれていません。参考までに、Uberが8月に別のツール「ADR」を公開したという報道（Techstrong、8月10日 — エージェント5万個以上・10か月運用・「認証情報の露出がプロンプトインジェクションより多かった」という会社発表）がありますが、その記事も11月の記事も互いに言及しておらず、**二つの関係は私たちには確認できませんでした。**InfoQ記事の読者の質問一つをそのまま載せます — 「自分が作っていないエージェントにはこれがどう適用されるのか。」

## 3. Apple — 健康AIの回答に「臨床引用・懸念質問の検知・学習不使用」を付けて20万人に評価を任せる（事実、会社発表）

Appleは11月15日、ニュースルームで**「Apple Health AI Usage Study」**を発表し、同日に米国App Storeへ「Apple Health AI Study App」（開発者Apple Inc.、無料、iPhone専用、iOS 26.0以上）を出しました。二つのページを直接読みました。協力先は**OpenEvidence** — 2022年設立のマイアミの会社で、医師向けのLLM医学検索を運営し、Wikipediaによれば2025年12月時点で米国の医師約76万人が登録し月1,800万件の臨床相談に使われ（会社発表）、NEJM・JAMAとコンテンツのライセンス契約を結んでいます（資金調達の内容はこの記事では扱いません）。参加条件は**米国在住の21歳以上、Apple Intelligenceが有効なiPhone 15 Pro以上、iOS 26以上、最大20万人**です。参加者は日常の健康の質問をし、複雑な医学情報を平易な言葉で読み、アンケートで回答の質を評価します。回答は**NEJM・JAMA・Natureのような医学的出典から引き、各回答に査読済みの臨床引用リンクが付きます。**希望すればヘルスケアアプリの安静時心拍・活動・睡眠・検査結果を共有し、個人データが回答の適切さをどれだけ変えるかを見ます。条件三つが記事に書かれています — **「研究データはAIモデルの学習に使わない」**、アプリには**「特定の懸念される質問を検知し、参加者に医療従事者や他のリソースへのフォローアップを勧める」**ガードレールがある、そして**「このアプリは診断・治療をせず、専門家の助言の代わりにはならない」**。Appleのヘルス・フィットネス担当VPのサンブル・デサイ医師は「健康は深く個人的なもの」とし、この研究を「人々が健康AIをどう使い、理解し、評価するかを知る最も慎重な方法」と呼びました。研究期間はニュースルームにありません。

媒体が加えたものは一か所ずつです。TechCrunch（11月15日）は研究が**12か月以上**で、ヘルスデータは匿名化されて「安全な第三者クラウド」へ行き、**OpenEvidenceが質問・回答データを24時間後に削除する**と書きました（この三つはAppleのニュースルームになく、TechCrunch一か所）。同じ記事は、OpenAIが今年初めに「週3億件以上の健康関連の質問」を受けていると明らかにしたと付け加えました（OpenAIの原文は私たちの側で開けず、未確認）。TechCrunchは機種条件を「iPhone 15以上」と書きましたが、AppleのニュースルームとBusiness Standard（11月16日）は「iPhone 15 Pro以上」なので、私たちはAppleの表記に従いました。iGeeksBlog（11月16日）は、Appleが「LLMベースの消費者向け健康ツールは時に不完全または不明瞭な回答を出すことがある」と書いたと引用しましたが、私たちが読んだニュースルーム本文にその文を見つけられず、媒体一か所とします。App Storeのプライバシーラベルは「User ID — ユーザーに関連付け（分析・アプリ機能）」、年齢区分は18+でした。

## 三つを合わせて読むと（解釈）

第一に、**三つとも「行動の前」に書かれた文書です。**NO.39の「停止ボタン」は行動のあとに押すもので、NO.49のAT&Tの「精度90%台後半」は行動しながら測る閾値です。今回の三つはその前 — エージェントが来る前（poppy.json）、エージェントを動かす前（登録簿）、回答が出る前（引用・検知・告知）に書きます。順序が後ろから前へ移ってくるのが今年後半の方向に見えます（解釈）。三つの文書の共通の欄は**「取り消せない行動」**です — Poppyはスコープに `irreversible` の印を付け、Uberは「特権的な行動を利用者が実際に要求したことに結びつける」証拠の連鎖を語り、Appleは懸念される質問を人（医療従事者）へ渡します。NO.39で「取り消せない行動は最初からエージェントの手の外」と書きましたが、その文がプロトコルのフィールド名になりました。

第二に、**「塞ぐこと」と「開くこと」が同じファイルに書かれます。**poppy.jsonには「うちのサイトをブラウジングしないで」（`web.disabled`）と「APIから入って」（`apis`）が並んでいます。Unitedの禁止（NO.45）とShopifyの開放が同じ形式の文になりうるということで、だから客のエージェントは「塞がれた」ではなく「この入口は閉じ、あの入口は開いている」を読みます（解釈）。ただし読むときに注意することが三つ — 規格が「1.0だが草案」で壊れる変更が予告されていること、ライセンスはApache License 2.0と書かれているがガバナンス主体は明記されていないこと、CMSWireが書いた問い「店の門をどの会社のエージェントが守るのか」（Sierra自身も顧客対応エージェントを売る会社です）が開いていること。「100社以上」はデザインパートナーの数で「オンにした」のは三社なので、数字を伝えるときは二つの欄に分けます（NO.21）。

第三に、**UberとAppleは「人を外す文書」ではなく「人へ渡す条件を書いた文書」です。**Uberの登録簿は自律権を与えるための書類のように見えますが、核心は「文脈に合わない行動を実行直前に止める」と「新しい規則はまず記録だけするシャドーモードで回す」です。Appleは20万人に回答を評価させながら「診断・治療ではない」「懸念される質問は医療従事者へ」を先に書きました。NO.03で私たちの成分表アプリが「安全です」と言わないようにした方法を書きましたが、Appleの文書はその大判です — 違うのは**回答ごとに引用リンクが付き、その回答を評価する人が利用者本人**だということ（解釈）。数値がない点も同じです — Uberは誤遮断率を、Appleは期間を、Sierraは実際のセッション数を書いていません。この記事の数字のうち会社の外で数えたものは一つもありません。

## 私たちなら — コマース・アプリ・AIインフルエンサーを運営するチームが今週すること三つ（実践）

1. **自社コマースドメインの `/.well-known/poppy.json` を「公開せずに」まず埋めてみる。**NO.43の「入ってくるエージェントの規則3行」とNO.45の「なぜ」欄をこのファイルのフィールドに移すと空欄がすぐ見えます — `organization`、どの入口を開けるか（`web` だけか `apis` もか）、`web.disabled` を入れるか、`scope_hints` で注文・決済を `irreversible` に、配送先を `personal_data` に印を付けるか。規格が草案なので**公開は代表の決定のあと**で、表の頭に「1.0＝草案、壊れる変更あり得る」と書いておきます。私たちの商品が載っている外部チャネルにShopify基盤のものがあれば、その店はすでにファイルが自動公開されているので何が書かれているか一度読みます。
2. **私たちのエージェント登録簿一枚をUber式の七つの欄で書く。**リアの台本生成、成分表判定（NO.03）、コマース問い合わせ回答、そしてAP Newsを収集して書くこのセッションまで — それぞれに身元・所有者・ペルソナ・許可された意図・制約・依存関係（どのMCPサーバー・ツールを使うか）・リスク等級を書きます。NO.49の「人を外す閾値N%」の隣の欄に置きます。新しい制約を入れるときはUberのように**2週間シャドーモード**（遮断せず記録だけ）で回したあと、誤遮断・誤許可の件数を見てオンにします。
3. **セーフリスト（成分表アプリ）の回答にApple式の三行を付ける。**①回答ごとに根拠リンク（私たちはMFDSの告示・原材料DBが引用）、②「懸念質問」の一覧（アレルギー反応・薬との相互作用・乳幼児の摂取などは回答の代わりに「専門家へ」）、③利用規約に「利用者の質問はモデルの学習に使わない」という文が実際にあるかと保存期間（TechCrunchが書いた「24時間」のように数字で）。そして回答の下に評価ボタン一つ（「合っている／わからない／違う」）— 20万人ではなくても20件から数え始めます。

## 今回選ばなかったもの

NVIDIAのジェンスン・フアンCEOの辞任と復帰説、それに伴う株価・サプライチェーン・輸出規制の報道は個人の事案と投資領域なので書きません。Anthropicの上場関連報道（Bloomberg）は投資領域で利害関係があるため書きません。FRB金融安定調査の「AIリスクを挙げた回答87%」（Reuters）も同じ理由で見出しだけ置きます。DisneyのAI拡大（Bloomberg）は原文を開けませんでした。美団のLongCat-2.5（1.6兆パラメータのオープンウェイト、The Decoder）とEdge0-145Bは公式モデルカードを確認できず、土曜の週間ニュース候補に置きます。FAAの航空管制支援ツールSMARTの全国展開（Gizmodo、「人間の管制官が最終権限」）は「人の監督」の続編候補ですが原資料を開いていません。promppyで見た「ホワイトハウス、AIセキュリティ事故を自主申告すれば1年間規制上の責任を緩和」（AI Times）は原文のアドレスを確保できませんでした。OpenAIの科学ブログ開設とGPT-6 Astraと書いた標準模型の論文はopenai.comが私たちの側で開かないため見出しだけ置きます。Anthropicのモデル文書ページは今回Claude 4.xのモデルだけが見える旧版で開いたため引用を保留しました（11月14日に確認したFable 5.1の表と異なる）。Anthropicのニュースルームには11月16日も新しい記事がなく、OpenAIのニュース一覧は今回も開きませんでした。

## このニュースで確認できなかったこと

- Poppy規格サイトのフッターにはApache License 2.0と書かれていますが（11月18日に直接確認）、標準化団体やガバナンス主体は明記されていません。「100社以上」はデザインパートナー数（会社発表）で、実際にオンにしたのはMercury・Synchrony・ターキッシュ エアラインズの三社です。Museの利用者「1,000万人以上」はTNW一か所です。Shopify自身の発表ページは探しておらず、Sierraの記事の「全店舗自動公開」の文で書きました。
- Poppyを通じて実際に行われたセッション数・注文数はどこにもありません。決済は「拡張の候補」としてのみ書かれています。
- Uberの記事には数値がなく（誤遮断率・遅延・コスト・エージェント数）、オープンソースかどうかもありません。8月のADR公開の報道（Techstrong一か所）と11月の記事の関係は確認できませんでした。Uberがどのモデル会社のモデルを使うかも記事にありません。
- Appleの研究期間はニュースルームになく、「12か月以上」・「匿名化のうえ第三者クラウド」・「OpenEvidenceが24時間後に削除」はTechCrunch一か所です。機種条件はTechCrunch（「iPhone 15以上」）とApple（「iPhone 15 Pro以上」）で異なり、Appleに従いました。「不完全または不明瞭な回答」の文はiGeeksBlogがAppleの記事を引用したもので、私たちはニュースルーム本文に見つけられませんでした。
- OpenEvidenceの医師76万人・月1,800万件はWikipediaが伝えた会社発表です。OpenAIの「週3億件の健康の質問」はTechCrunchが書いたもので、OpenAIの原文は開けませんでした。
- どの会社の発表も、私たちが直接試験したり数えたものはありません。

## 一緒に読んだ記事

性質の異なる出典を直接開いて確認しました。会社発表・公式文書、規格原文、媒体報道、Wiki、私たちの以前の記事に分けて書きます。

会社発表・公式文書：

- [Releasing Poppy 1.0（Sierraブログ、ブレット・テイラー、クレイ・ベイバー、11月13日）](https://sierra.ai/blog/releasing-poppy) — 英語、MCP・OpenAPI・UCP上のOAuth・5週間の試験・コマース拡張はShopify共著・パートナー100社以上・Mercury・Synchrony・ターキッシュ エアラインズ・「すべてのShopify店舗がPoppyファイルを自動公開」・Muse全員に適用
- [Securing AI Agents: Lessons From Real-World Deployment（Uber Engineering、11月6日）](https://www.uber.com/blog/securing-ai-agents/) — 英語、AI Registry・Argus・AI Guard・Agent Guard・実行トレース・再生、三層構造、難しさの一覧、数値なし
- [Apple launches research study to explore the use of AI for health（Apple Newsroom、11月15日）](https://www.apple.com/newsroom/2026/11/apple-launches-research-study-to-explore-the-use-of-ai-for-health/) — 英語、OpenEvidence・21歳以上・iPhone 15 Pro以上・iOS 26・最大20万人・NEJM/JAMA/Nature引用・懸念質問の検知・学習不使用・診断ではない・デサイ発言
- [Apple Health AI Study App（App Store）](https://apps.apple.com/us/app/apple-health-ai-study-app/id6800060365) — 英語、開発者Apple Inc.・無料・iPhone専用・iOS 26.0以上・「医療上の助言・診断・治療を提供しない」・プライバシーラベル

規格原文：

- [Personal Agent Protocol 1.0 Specification](https://personalagentprotocol.org/docs/1.0/spec) — 英語、`/.well-known/poppy.json`・organization・agent.protocols・apis・web・tasks・extensions・auth.disabled・web.disabled・scope_hints（irreversible・personal_data）・OAuth 2.0 PKCE・RFC 8628・Poppy-Session・「1.0＝0.4＋修正」（冒頭10万字を読了）

媒体報道：

- [Sierra's Poppy 1.0: Shopify turns it on for every store, Meta's Muse looks for it first（TNW、11月13日）](https://thenextweb.com/news/sierra-poppy-1-0-shopify-meta-muse-personal-agents) — 英語、Muse 1,000万人以上（一か所）・「1.0だが草案」・ターキッシュ エアラインズ・Mercuryの事例・Visa・Mastercard・Amazon
- [Sierra and Meta unveil Personal Agent Protocol（TNW、10月6日）](https://thenextweb.com/news/personal-agent-protocol-sierra-meta) — 英語、初発表・パートナー6社・OAuth・客が読み取り/書き込みを決定・会社が経路を決定・決済は将来の作業
- [Sierra's Poppy draft spells out how AI agents can access businesses（NeoTeo、10月9日）](https://www.neoteo.com/en/sierras-poppy-draft-spells-out-how-ai-agents-can-access-businesses) — 英語、草案・/.well-known/poppy.json・デザインパートナー35社追加・Rocketデモ（Sierra自身の説明）
- [Genesys joins Sierra, Meta on open standard for personal AI agents（CMSWire、10月7日）](https://www.cmswire.com/contact-center/genesys-joins-sierra-meta-on-open-standard-for-personal-ai-agents-01/) — 英語、「消費者がアクセスを決め、企業が限度を決める」・ガバナンス未公開・パートナー一覧の差・開いた問い
- [Meta Muse, Shopify, Amazon and the race to own AI shopping（Practical Ecommerce、9月24日）](https://www.practicalecommerce.com/?p=1567232) — 英語、背景：9/8にShopifyのAgentic StorefrontsにMeta追加・AmazonのMuse遮断文言
- [Uber's Secure AI framework for autonomous agents（InfoQ、11月15日）](https://www.infoq.com/news/2026/11/uber-secure-ai-framework/) — 英語、Uber記事の整理・読者の問い「自分が作っていないエージェントには」
- [Uber open-sources ADR to catch agentic blunders（Techstrong.ai、8月10日）](https://techstrong.ai/articles/uber-open-sources-tool-to-catch-agentic-blunders-legacy-security-misses/) — 英語、8月の別ツール（会社発表の数値、一か所）— 11月の記事との関係は未確認
- [Apple launches new app to study how people use AI for health（TechCrunch、11月15日）](https://techcrunch.com/2026/11/15/apple-launches-new-app-to-study-how-people-use-ai-for-health/) — 英語、12か月以上・匿名化・第三者クラウド・24時間削除（一か所）・OpenAI週3億件（伝聞）
- [Apple launches app to study how people use AI for health queries（Business Standard、11月16日）](https://www.business-standard.com/technology/tech-news/apple-launches-app-to-study-how-people-use-ai-for-health-queries-details-126111600875_1.html) — 英語、iPhone 15 Pro以上・米国限定・期間・報酬なし
- [Apple's AI health study is open to up to 200,000 U.S. iPhone users（iGeeksBlog、11月16日）](https://www.igeeksblog.com/apple-health-ai-usage-study-app/) — 英語、「不完全または不明瞭な回答」の引用（一か所）・期間未公開・プライバシーラベル

Wiki：

- [OpenEvidence（Wikipedia）](https://en.wikipedia.org/wiki/OpenEvidence) — 英語、2022年設立・マイアミ・医師76万人・月1,800万件（会社発表）・NEJM・JAMAのライセンス

私たちの以前の記事：

- [ショーホストもカメラもない放送がレギュラー編成された（AP News NO.49）](https://www.apholdings.kr/ko/news/no-host-ai-broadcast-and-who-must-disclose/)
- [週間AIニュース — OpenAIはエージェントに財布を握らせ、Unitedは「客のエージェント」を門の外に立たせた（AP News NO.47）](https://www.apholdings.kr/ko/news/weekly-2026-11-14/)
- [客のエージェントは塞ぎ、店は入れ、モデルは皆に（AP News NO.45）](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [客は自分のエージェントを連れてこられない（AP News NO.43）](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [「エージェントが権限を超えうる」が開示書類に書かれ始めた（AP News NO.39）](https://www.apholdings.kr/ko/news/agent-risk-goes-into-the-filings/)
- [確認コードがエージェントの手に届くと（AP News NO.36）](https://www.apholdings.kr/ko/news/agents-raised-their-own-spending-caps/)
- [エージェントは「信用できない内部者」だ（AP News NO.29）](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
- [数字を比べる前に数え方から（AP News NO.21）](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [AIが成分表を代わりに読むとき（AP News NO.03）](https://www.apholdings.kr/ko/news/ai-reads-the-label/)
