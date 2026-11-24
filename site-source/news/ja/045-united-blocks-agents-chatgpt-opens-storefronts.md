---
no: 45
slug: united-blocks-agents-chatgpt-opens-storefronts
date: 2026-11-12
category: インサイト
tags: AIエージェント · ユナイテッド航空 · エージェントコマース · ChatGPT · OpenAI · Gemini 4 Carbon · グーグル · Epoch AI · モデル選択
title: 客のエージェントは止め、店は招き入れ、モデルは全員に — ユナイテッドは「個人AIエージェントによる予約の禁止」を発表し、OpenAIは同じ日に店がChatGPTの中へ自分のエージェントを置けるようにし、グーグルは「一部に先に」渡していたGemini 4 Carbonを料金を払う全員に開いた
summary: 11月11日、ユナイテッド航空は「承認されていない第三者の個人AIエージェント」による予約を、自社ウェブ・アプリと旅行代理店・比較サイトの経路で止めると発表しました。理由として挙げたのは、認証情報の漏えい、意図しない購入やマイルの使用、そして「チェックイン時に禁止物が入っていないことの確認は人がしなければならない」という航空規則です。その前日、OpenAIは「Businesses in ChatGPT」のベータを出し、米国のEC・オンラインサービス事業者がChatGPTの中に自分のエージェントを置き、自分の店がChatGPTの回答に何回言及され何回クリックされたかを見られるようにしました（決済はまだありません）。同じ日、グーグルは2週間前にサイバー防御者だけに渡していたGemini 4 Carbonを有料の開発者・企業とUltra加入者に開き、11月30日まではArgonと同じ料金です。最後の「短く」では、独立評価機関Epoch AIがClaude Fable 5.2に付けた点数を記しました — この記事を書いたAIの製造元のモデルなので利害関係を明示し、数字と但し書きだけを移します。
---
> この記事はAI（Claude）とともに作成し、編集者が検証しました。当社はAnthropicとOpenAIの2社の有料顧客で、2番はOpenAIの発表、3番はグーグルの発表です。末尾の「短く」は**この記事を書いたAIの製造元（Anthropic）のモデルに独立評価機関が付けた点数**なので、評価は加えず数字・区間・但し書きだけを移しました。会社が発表した数値は「会社が発表したもの」と表記しています。ユナイテッドやデルタなど上場企業の業績・株価と、Anthropicの上場ロードショーの報道は投資判断の材料なので書かず、この記事は特定企業への投資意見ではありません。

NO.43で「客は自分のエージェントを連れて来られない」と書きました。アマゾンはメタのエージェントを止めてテキストのAlexaを出し、Airbnbは「外部エージェントの予約はごくわずか」と言って自前のエージェントを2027年に出すとしました。今週は同じ扉が**三つの方向に**動きました。航空会社は客のエージェントを止め、ChatGPTは店のエージェントを自分の中へ招き入れ、グーグルは最も強いモデルを料金を払う全員に開きました。事実・解釈・私たちならに分けて記します。

## 1. ユナイテッド — 「承認されていない個人AIエージェント」の予約禁止（事実）

ユナイテッド航空は11月11日（水）に声明を出し、**「承認されていない第三者の個人AIエージェントまたはアシスタントによる利用を禁止する」**措置を明らかにしました。Skift・PYOK・AirlineGeeksの3媒体が同じ声明を伝え、ユナイテッドが声明の原文を載せたページは私たちには見つかりませんでした。範囲は二つです。**自社ウェブサイト・アプリ**で直接止め、**オンライン旅行代理店（OTA）・価格比較サイト**と協力してその経路でも自社データへのアクセスを止めます。声明はそのために「予約・発券・流通ポリシーを更新する」とし、自社の「Digital Trust Center」ページに制限の内容を記すとしました。施行日と止めるエージェントの名前は3媒体のどこにもありません。

理由は三つです。第一に、アカウントの認証情報を第三者のアシスタントと共有すると**機微な情報が漏れうる。**第二に、エージェントの行動が**意図しない購入・アカウント変更・マイル（MileagePlus）の使用**を引き起こしうる。第三に、「自動化されたAIの行動はFAA・DOTの規則に違反する可能性がある」— 例として挙げたのが**「フライトのチェックインでは、手荷物に爆発物のような禁止物が入っていないことを人が確認する必要がある」**という項目です。声明はこの立場が銀行・小売企業と同じだと記し、他の企業にも同様の措置を勧めました。Skiftは米国の航空会社で明示したのは初めてとし、PYOKはデルタが先に同様の対応をしているという伝聞を添えました。両媒体の「初」「2番目」は食い違っています。

背景は10月から積み上がっていました。TechCrunchが10月6日に整理したところでは、ユナイテッドは当時すでに利用規約の**「ロボット・スパイダー・その他の自動装置または手作業の工程でこのウェブサイトを監視・複製しない」**という条項を示し、特定のエージェントを止めているかは答えませんでした。デルタは「第三者エージェントが予約できる提携はなく、開くなら安全と顧客体験を考えて開く」と述べ、利用者は拒否された例を投稿しました。同じ記事で、ウォルマートはメタのMuse利用者が人間確認の段階で止められたのは**意図したものではなかった**とし（ウォルマートはMuseの提携先）、eBayは「すべてのショッピングエージェントではなく、承認されていないエージェントとスクレイピングだけを止める」、Yelpは「データライセンスを買った運営者だけ」としました。メタの言葉は**「個人エージェントを追い返すのは、その後ろにいる客を追い返すこと」**でした。OfficeChaiが10月18日に整理した金融側 — JPモルガンは外部エージェントの取引を止めて残高などの読み取り専用データだけを開き、シュワブのCEOは資金を動かそうとするエージェントを「週に数十回」止めているとブルームバーグTVで語ったという話 — は二次的な整理で、元の発言は確認できませんでした。Skiftによれば、ユナイテッドのCEOスコット・カービーはシカゴのイベントで**「新たな仲介者を作りたくない」**と述べ（WSJの伝聞）、デルタのCEOエド・バスティアンは予約エージェントに「慎重だ」と述べました。

同じ二日の間に、反対方向の動きもありました。OpenAIは11月10日、**AI旅行エージェントのスタートアップOdessiaを買収**しました（TechCrunch・Skift）。条件は非公開で、サービスはすでに終了し、創業者がOpenAIに加わって「旅行分野の将来」を手伝います。OpenAIの広報担当は「毎週12億人が旅行計画を含む日常の用事にChatGPTを使う」と述べました。Skiftはサウスウエストがフライト検索用のChatGPTプラグインを出したと記しましたが、これは一か所でしか見ていません。

## 2. OpenAI — 店がChatGPTの中に自分のエージェントを置く、決済はまだない（事実）

OpenAIは11月10日、**「Businesses in ChatGPT」**をベータで出しました（会社の発表記事は私たちの側から開けなかったため、TNW・PPC Landの2媒体で確認しました）。構成は二つです。**Business Hub**で事業者は自分のプロフィールを認証（青いチェック）し、説明・価格・在庫を直し、商品フィードを上げられます。そして**ChatGPTが自分の店を何回言及したか、プロフィールが何回見られたか、ウェブサイトへ何回クリックされたか、どんな話題の会話で出てきたか**を7日・28日単位で見ます。PPC Landが写した画面には、クリック欄に**「クリックはウェブサイト訪問やコンバージョンを確認するものではない」**という但し書きが付いています。利用者の会話は事業者に共有されず、データは非公開のしきい値を超えた場合にだけ見えます。「言及」の定義はありません。

**Business Agents**は米国のEC・オンラインサービス事業者だけが作れます。ChatGPTの回答に店が出ると、利用者はプロフィールを開いてその店のエージェントと会話し、エージェントは店が上げた商品情報で答えます。会話には**ラベルが付き、ChatGPT自身の回答とは分けられます。**買いたい人は**店のウェブサイトへ送られます — 決済はまだなく、Visaとエージェント決済を開発中**だとTNWは記しました。ルールは「AIであることを明かす、価格を正確に記す、圧力販売の禁止、購入と個人情報の共有は利用者の明示的な承認」です。事業者は料金を払って自分のエージェントを**ChatGPT広告の着地点**に置くことができ（9月16日に始まったSponsored Agentsの試験の延長）、スポンサー表示が付きます。TNWがDigidayを引いたところでは、料金を払ってもChatGPTがその店を薦める頻度は変わらないとOpenAIは述べています。認証は電話・SMS・DNSのいずれか、エージェントを直したり公開したりするには身分証が必要というのは、PPC LandがSearch Engine Roundtableを引いた内容です。米国外の事業者は公開当日に待機リストに入り、手数料は記されていません。PPC Landが見た最初の実際のダッシュボードの一つは28日間で言及690件・クリック24件（約3.5%）でしたが、これは一か所が見た二事業者の画面なので一般化しません。OpenAIが記した背景の数字 — 週12億人、広告主10万、8月の広告の年換算10億ドル — は会社が発表したものです。

## 3. グーグル — 「一部に先に」の2週間後、Carbonを料金を払う全員に（事実）

グーグルは11月10日、**Gemini 4 Carbon**を開きました（会社が発表したもの）。NO.33で「新しい採点表の1位はまだ誰でも呼べるわけではない」と書いたそのモデルです。10月28日にFairwindプログラムでサイバー防御者に先に渡し、2週間後に**有料の開発者・企業（Google AI Studio、Gemini for business）とGoogle AI Ultra加入者（Antigravity・Geminiアプリ・検索のAIモード）**に開きました。科学者には選考を経て6か月無料、サイバー防御者には引き続きFairwindで渡します。料金は**11月30日まで100万トークンあたり入力2ドル・出力10ドルでArgonと同じ、その後4・20ドルと2倍**になります。発表記事は「Argonは大半のソフトウェア・知識業務向け、Carbonは複雑な多段階デバッグや自由度の高い研究のようなより難しい課題向けで、検証と推論により多くのトークンを使う」と記します。Antigravityには一つのプロンプトを複数のエージェントチームに分けて回す**/swarm**がプレビューで入りました。

ベンチマークはすべて会社が発表したもので、一部は公開前・内部の結果です。CursorBench 4.0・Perplexity WANDR・Zapier AutomationBenchで1位、Artificial Analysisと作ったMKAで2位、適応型攻撃エージェントの経路を99%遮断、試行あたりの突破率0.8%（Argon 3.1%）、誠実さベンチマーク92%（Argon 70%）といった数字です。NO.44でAnthropicの表を移した際、AutomationBenchでCarbon 53.9%がFable 5.2 51.4%を上回ると書きましたが、そのCarbonがいまや誰でも呼べるモデルになりました。発表記事自身が「プロンプトインジェクションへの頑健性は改善すべき領域」と記し、タンパク質・実験科学側の結果は「より広いベンチマーク待ち」です。

## 短く — Epoch AIがClaude Fable 5.2に付けた点数（事実、利害関係の明示）

NO.44で「独立評価機関の点数はまだない」と記しました。その二行目を埋めます。Epoch AIのモデルページを11月12日に開くと、**Claude Fable 5.2のEpoch能力指数（ECI）は173で、追跡中の240モデルのうち1位**、次がGemini 4 Carbon 170、GPT-6 Astra 169、Claude Opus 5.5 169です。同じサイトのベンチマークページは174と記します（二つのページの差は丸めか更新時点の違いに見えますが確認できませんでした）。FourWeekMBAが11月9日のデータファイルを読んだところでは174.24、90%区間は170.1〜178.8で、Astraの区間（166.2〜172.5）と**重なります。**同じ整理は、Fable 5.2の結果がベンチマーク10個（Astraは24個）で、すべて最高の努力段階、公開前にEpoch自身のベンチマークだけで出した値なので変わりうると記します。モデルページには区間・評価日・努力段階がありません。EpochのECIページには「方法論論文はGoogle DeepMindの支援を受け、ECIはEpochの所有」という文があります。ベンチマーク別では、GPQA DiamondでCarbon 97%・Astra 96%がFable 5.2の94%を上回り、SpireClimbでAstra 34%がFable 5.2の20%を上回ります。ここまでが数字で、評価は加えません。Artificial Analysisの順位表は今日は開いていません。

## 三つをあわせて読むと（解釈）

第一に、**「扉は開くのではなく主が変わる」（NO.43）の次の文は「主が二人いる」です。**ユナイテッドは客が連れてきたエージェントを止め、同じ日にOpenAIは旅行エージェントの会社を買いました。航空会社は自分のカウンターで客をつかもうとし、プラットフォームは自分の中で客をつかもうとします。カービーの「新たな仲介者」はその間にある言葉です（解釈）。ただOpenAIが店を招き入れるやり方を見ると、**決済は店へ送り**、エージェントは「商品情報で答える」までです。ユナイテッドが挙げた三つの理由 — 認証情報、取り消せない行動（購入・マイル）、人の確認が要る規則 — はどれも**「エージェントが最後の段階を代わると起きること」**で、OpenAIの設計もまだ最後の段階を渡していません。二つは反対方向に見えて、同じ線の前に立っています。

第二に、**「露出」の数字をプラットフォーム自身が出し始めました。**NO.42でZiff Davisが「AI回答の引用はクリックの10倍なのに訪問は減った」とSearch Consoleで見たのを読みましたが、いまやChatGPTが店に「言及・閲覧・クリック」を直接見せます。但し書きは画面に付いています — **クリックは訪問でもコンバージョンでもありません。**最初の画面の3.5%は二事業者の数字なので使えませんが、欄が四つ（言及→クリック→訪問→コンバージョン）に分かれることだけは明らかです（解釈）。そして「払っても推薦頻度は変わらない」は会社の言葉で、まだ誰も外から測っていません。

第三に、**モデルの扉は「一部に先に」から「全員に、料金は2か月後に2倍」へ進みます。**NO.15・33・NO.44が同じ形です。グーグルもAnthropicも「大半はより安いモデル（Argon・Opus 5.5）」と自ら記します。Epochの数字は二行目を埋めてくれますが、区間が重なり結果数が少ない。NO.40の「1点差は区間の内側」が今回は**4〜5点差でも区間が重なる**と読めます（解釈）。点数一つでモデル選択表を変える理由は今日もありません。

## 私たちなら — アプリ・コマース・AIチャンネルを運営するチームが今週すること三つ（実践）

1. **「入ってくるエージェントの規則3行」（NO.43）に「なぜ」の欄を付ける。**ユナイテッドの三つの理由を私たちの言葉に直すと「認証情報を受け取る段階」「取り消せない段階（決済・返金・個人情報の変更）」「人が確認しなければならない段階（SafeListの成分判定は「避ける項目は見当たらなかった」までで、最終判断は保護者）」です。私たちのコマース4層とアプリ画面のうちこの三つに当たる段階に**「エージェントは代行不可」**の印を付け、規約の段落（代表の決定）にその理由を記します。止めるのではなく「どこまで」を書くのです。
2. **トラフィック表に「プラットフォームがくれた露出」の欄を入れ、四つに分ける。**NO.42のトラフィック3行（検索／AI引用／直接）の隣に「言及／クリック／訪問／コンバージョン」を置きます。Business Hubは米国限定なので今は私たちは登録できず、代わりに月1回、私たちのアプリ名をChatGPT・Geminiに尋ねて「言及されるか」を手で記します。プラットフォームが数字をくれる日が来たら、その欄に入る場所です。
3. **11月30日まで同じ料金のCarbonをモデル試験3件に入れる。**NO.17の私たちの試験（成分表判定・アプリ文言・リアの台本草稿）をArgon・Opus 5.5 HighとCarbonで同じ努力段階どうし回し、「会社が発表／私たちが確認」の二行で記します。12月1日に料金が2倍になることを表の頭に書いておきます。Epochの点数は二行目に「173〜174、区間重なり、結果10個」と入れ、1位の欄は空けておきます。

## 今回選ばなかったもの

Anthropicの上場ロードショー（11月10日）、The Informationが伝えたOpenAIの四半期売上、ニューヨーク市年金のAI投資の報道は投資の領域なので書きませんでした。The Hacker Newsの「Fable 5.2が多段階サイバー攻撃ベンチマークでGPT-6 Cyberを上回った」はサイバー能力の比較であり利害関係当事者のモデルなので、見出しだけ記録します。Fireworks AIの侵害拡大とRailwayの「不正なAI課金74万ドル」（BleepingComputer）はセキュリティ事故なので見出しだけ置き、続報でも手口は書きません（RailwayはNO.26の続報候補）。TNWの「豪州、OpenAIエージェントのメディケアポータル接触事件の後にAI安全規制機関を計画」はNO.39の続報候補に置きます（法案は未成立）。Epochの「推論性能指数」（11月9日）は「値段とコスト」の続報候補です。Learn:USの11月9日の記事（投資家の開示を読むトレーダースキル）は投資の領域なので扱いません。Wikipediaの「Agentic commerce」項目は定義とプロトコル年表だけで遮断事例・航空会社はなく、背景としてだけ読みました。

## このニュースで確認できなかったこと

- ユナイテッドの声明の原文ページ（Digital Trust Centerの更新分を含む）は見つからず、3媒体の引用が互いに一致することまで確認しました。施行日、止めるエージェントの名前、OTA側の具体的な方法はどこにもありません。
- カービー「新たな仲介者」（WSJの伝聞）・バスティアン「慎重」・ザッカーバーグ「旅行は最上位の用途」・サウスウエストのChatGPTプラグインはSkift一か所で見ました。JPモルガン・シュワブの項目はOfficeChaiの二次的な整理で、元の発言（ブルームバーグTV）は開けませんでした。
- OpenAIの発表記事は開けませんでした。「決済なし・Visaと開発中」「払っても推薦頻度は不変（Digiday）」はTNW、「身分証が必要（SERoundtable）」「最初のダッシュボード690/24」はPPC Landのそれぞれ一か所です。手数料と「言及」の定義、しきい値は公開されていません。
- Carbonのベンチマーク・安全性の数値はすべて会社の発表で、独立評価はまだ確認できていません。12月1日以降の料金4・20ドルは発表記事の「11月30日以降」を移したものです。
- Epochのモデルページ173とベンチマークページ174の差、90%区間（170.1〜178.8）と「ベンチマーク10個・最高努力段階」はFourWeekMBA一か所のデータファイル整理です。Epochの順位表自体は「Loading…」と表示され、直接照合できませんでした。

## あわせて読んだ記事

性格の異なる出典を直接開いて確認しました。会社の発表、研究・評価機関、媒体の報道、ウィキ、私たちの過去記事に分けて記します。

会社の発表：

- [Gemini 4 Carbon now available（Google、11月10日）](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) — 英文、公開範囲・料金（11月30日まで2/10、以後4/20）・/swarm・ベンチマークと安全性の数値（会社が発表したもの）
- [Introducing Businesses in ChatGPT（OpenAI、11月10日）](https://openai.com/index/introducing-businesses-chatgpt/) — 英文、発表記事（私たちの側から開けず、下の媒体2か所で確認）

研究・評価機関：

- [Claude Fable 5.2 — Epoch AIモデルページ](https://epoch.ai/models/claude-fable-5-2) — 英文、ECI 173・1位・Carbon 170・Astra 169・ベンチマーク別の点数（区間・評価日なし）
- [Epoch Capabilities Index（Epoch AI）](https://epoch.ai/eci) — 英文、指数の説明・データ11月11日更新・「方法論論文はGoogle DeepMindの支援」の文

媒体の報道：

- [United Airlines Moves to Block Personal AI Agents From Booking Flights（Skift、11月11日）](https://skift.com/2026/11/11/united-airlines-moves-to-block-personal-ai-agents-from-booking-flights/) — 英文、声明の引用・OTA経路・カービー発言（WSJの伝聞）・Odessia・サウスウエスト
- [United Airlines is Blocking AI Booking Agents: They Might Breach FAA And DOT Regulations（PYOK、11月11日）](https://www.paddleyourownkanoo.com/2026/11/11/united-airlines-is-blocking-ai-booking-agents-they-might-breach-faa-and-dot-regulations/) — 英文、規則の文・チェックインの例・ポリシー更新・デルタの伝聞
- [United Bans AI Agents From Booking Flights For Customers（AirlineGeeks、11月11日）](https://airlinegeeks.com/2026/11/11/united-bans-ai-agents-from-booking-flights-for-customers/) — 英文、認証情報・Digital Trust Center・他企業への同調の呼びかけ
- [The next hurdle for AI agents: getting websites to let them in（TechCrunch、10月6日）](https://techcrunch.com/2026/10/06/the-next-hurdle-for-ai-agents-getting-websites-to-let-them-in/) — 英文、ユナイテッドの規約条項・デルタ・ウォルマート・eBay・Yelp・メタの発言
- [Amazon, JPMorgan, Schwab And Delta Are All Blocking AI Agents（OfficeChai、10月18日）](https://officechai.com/ai/amazon-jpmorgan-schwab-and-delta-are-all-blocking-ai-agents-heres-why/) — 英文、金融側の遮断の整理（二次的な整理）
- [OpenAI acquires Odessia, travel startup created by Sonder founder（TechCrunch、11月10日）](https://techcrunch.com/2026/11/10/openai-acquires-odessia-travel-startup-created-by-sonder-founder/) — 英文、買収条件非公開・サービス終了・OpenAI広報の発言
- [OpenAI lets businesses claim ChatGPT profiles and launch their own agents（TNW、11月10日）](https://thenextweb.com/news/openai-businesses-in-chatgpt-business-agents) — 英文、Business Hub・Business Agents・決済なし・ルール・Digidayの引用
- [Businesses gain ChatGPT click and mention counts in OpenAI's Business Hub（PPC Land、11月10日）](https://ppc.land/businesses-gain-chatgpt-click-and-mention-counts-in-openais-business-hub/) — 英文、指標四つ・「クリック≠訪問」の但し書き・認証方法・最初のダッシュボード（一か所）
- [OpenAI tests Sponsored Agents in ChatGPT（TNW、9月16日）](https://thenextweb.com/news/openai-chatgpt-sponsored-agents-ads-manager-hubspot-shopify) — 英文、Sponsored Agentsの試験・Shopify・HubSpot・広告の背景
- [Epoch: Claude Fable 5.2 Sets ECI Record at 174, Astra at 169（FourWeekMBA）](https://fourweekmba.com/ai-epoch-claude-fable-5-2-sets-eci-record-at-174-astra-at-169/) — 英文、11月9日データファイルの90%区間・ベンチマーク数・努力段階（一か所の整理）

ウィキ：

- [Agentic commerce（Wikipedia）](https://en.wikipedia.org/wiki/Agentic_commerce) — 英文、定義・論点（責任・認証）・プロトコル年表（遮断事例なし）

私たちの過去記事：

- [同じモデルに扉が二つ（AP News NO.44）](https://www.apholdings.kr/ko/news/fable-5-2-two-doors-and-sandbagging-logs/)
- [客は自分のエージェントを連れて来られない（AP News NO.43）](https://www.apholdings.kr/ko/news/every-platform-builds-its-own-agent/)
- [検索から来ていた客が減っている（AP News NO.42）](https://www.apholdings.kr/ko/news/when-search-visitors-stop-coming/)
- [採点表に確率が付いた（AP News NO.40）](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [AIが客を連れてくる玄関が三つになった（AP News NO.38）](https://www.apholdings.kr/ko/news/three-front-doors-where-ai-brings-customers/)
- [GitHubのプルリクエスト10件のうち4件はエージェントが開く — 新しい採点表の1位はまだ誰でも呼べるわけではない（AP News NO.33）](https://www.apholdings.kr/ko/news/agent-prs-40-percent-and-a-new-number-one/)
- [作業別にどのAIを使うか（AP News NO.17）](https://www.apholdings.kr/ko/news/which-ai-for-which-job/)
- [今週のAIニュース — グーグルは「より強く、一部に先に」（AP News NO.15）](https://www.apholdings.kr/ko/news/this-week-gpt61-sonnet55/)
