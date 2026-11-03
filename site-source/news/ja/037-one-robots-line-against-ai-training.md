---
no: 37
slug: one-robots-line-against-ai-training
date: 2026-11-03
category: 実践
tags: robots.txt · AI学習の拒否 · IETF AI選好 · Google · Microsoft Bing · OpenAI · Anthropic · サイト運営
title: robots.txtの一行で「AI学習に使わないで」— Google・Microsoft・OpenAI・Anthropicが同じトークンを受け入れ、Bingは「学習」と「回答での引用」を分けた。私たちのサイトが今週決める三つのこと
summary: 10月30日、四つの会社が同じ日に同じ約束をしました。サイト運営者がrobots.txtに「__usage_ai-training」という共通の名前を一行書けば、Google・Microsoft・OpenAI・Anthropicはそれを「このサイトの記事を生成AIの学習に使わないで」という意味に読む、というものです。これまでは会社ごとに違うクローラー名を一つずつ止める必要がありました。同じ日、Microsoft Bingはさらに一歩進み、「学習に使うこと」と「AI回答を作るときに引用すること」を分けて別々に選べるようにし、2027年2月1日から適用すると発表しました。ただしこの一行は鍵ではなく宣言であり、まだ標準でもありません。私たちのホームページのrobots.txtを直接開いてみると、この選好を何も表現していない状態でした。サイトを運営する小さなチームが今週決める三つのことを書きました。最後に、同じ日に出たAnthropicの上場書類の修正版を短く添えました。
---
> この記事はAI（Claude）と共に作成し、編集者が確認しました。最初の話題の標準草案を書いた人はClaudeを作るAnthropicの所属で、Anthropicは約束した四社のうちの一つです。最後の「短く」はAnthropicの上場書類を扱います。私たちの会社はAnthropicとOpenAIの有料顧客です。会社文書の表現は「会社文書が書いたこと」として伝え、出典が一か所だけの内容はその出典を併記しました。特定企業に対する投資意見ではなく、投資判断の資料でもありません。

サイトを運営するチームは、この3年間「私たちの記事がAI学習に使われるのを防ぐには、どこに何を書けばいいのか」を会社ごとに別々に調べる必要がありました。GoogleはGoogle-Extended、OpenAIはGPTBot、AnthropicはClaudeBot、AppleはApplebot-Extended。名前が違い、止められる範囲も違いました。NO.28では商業検索の88%にAI要約が出るという調査を、NO.25ではウェブのシェアが数えていないものを書きました。今週の話題はその反対側、**「私の記事をAIがどう使ってよいか」をサイト側から書く方法**が初めて一行にまとまったということです。ただし一行ができたことと、その一行が守られることは別の問題なので、事実と限界を分けて書きます。

## 1. 四社が同じトークンを受け入れた — IETF草案「__usage_ai-training」（事実）

10月30日、Anthropicの標準担当テクニカルリード、ケビン・ケリーがIETFに**「機械可読な学習選好シグナル（Machine-Readable Training Preference Signal）」**の草案を提出しました。文書番号はdraft-kelley-aipref-training-preference-signal-00で、2027年5月3日に期限が切れる**個人草案**です。文書の冒頭に「IETFが承認したものではなく、正式な地位はない」と書かれています。草案が定めるのは一つだけです。robots.txtのUser-Agentグループ名の位置に書く**ポリシートークン`__usage_ai-training`**です。このグループの下にDisallowを書けば「そのパスのコンテンツをAI学習に使わないでほしい」という選好、Allowを書けば「使ってよい」という選好になります。「学習」の意味はIETFのAI選好ワーキンググループの用語草案に従い、**「生成AIモデルの学習済みパラメータを変更するために資産を使うこと」**です。

同じ日、四社がこのトークンを守ると表明しました。私たちが直接確認したのは三か所です。**Microsoft**はBingブログに「業界の同業者とともにrobots.txtの共通AI学習選好を発表する」と書き、**2027年2月1日**から適用するとしました。**Google**はSearch Centralブログに「IETFで検討中の提案を自発的に採用する計画」で「複数のAI提供者に対する学習選好を一度に表現できるようになる」と書き（本文は私たちのfetchでは目次しか見えず、Search Engine RoundtableとPPC Landが引用した文で確認）、クローラー文書のGoogle-Extended項目に**「2027年初め」**にサポート予定という注記を付けました。**Anthropic**は草案の著者がIETFメーリングリストに「すでにサポートの実装を始めた」と知らせましたが、どのクローラーにいつ適用されるかは書かず、「時間がかかる」「既存のクローラー制御を置き換えるのではなく補完する」「解釈は変わりうる」という注意書きを付けました。**OpenAI**の公式記事は私たちのfetchが遮断されて開けず、Engadgetは「数か月以内に」実装すると伝え、PPC Landは「時期は示されなかった」と書きました。

草案には運営者が知っておくべき規則がいくつかあります。第一に、**このトークンはクロールの指示ではありません。**「コンテンツ利用の選好とクローラーの通行規則は互いに独立」と書かれています。第二に、**`User-Agent: *`のワイルドカードはこのトークンに適用されません。**トークン名を直接書いたグループだけが選好として読まれます。第三に、具体的な表現が一般的な表現より優先し、「私的な契約がこの選好を上書きしうる」と書かれています。第四に、選好は「資産を取得した時点のrobots.txt」が基準です。Engadgetはこの点を「すでに収集されたものは取り消せない」と解き、「クロール自体やGoogle検索での表示を防ぐものではない」とも書きました。

Googleの解釈はGoogle検索担当のジョン・ミューラーが説明しました（Search Engine Roundtable・PPC Land）。サイトがGoogle-Extendedを別に書かず**共通トークンだけを止めた場合、「Google-Extendedを止めたかのように」解釈**するということです。Googleのクローラー文書によれば、Google-Extendedは独自のクローラーではなく「制御の役割」だけを持つトークンで、**Geminiモデルの学習**と**GeminiアプリとVertex AIのグラウンディング**（回答時に検索インデックスの内容をモデルに渡すこと）を併せて制御し、**Google検索への掲載や順位には影響しない**と書かれています。Google側からの反論も同じ報道に出ています。Googleのゲイリー・イリーズはrobots.txtは「提案であって、セキュリティ上の制御ではない」とし「誰でも30秒あればGooglebotになりすませる」と述べ（PPC Landが引用したポッドキャストでの発言）、IETF参加者のネイト・ヘイクは「IETFのレベルではまだ終わっておらず、大きな争点が残っている」「草案は利用者の行為を事実上例外にしている」と述べました（Search Engine Roundtable）。

## 2. Bingは「学習」と「回答での引用」を分けた — 三つの設定と四つの日付（事実）

同じ10月30日、Microsoft Bingは共通トークンのサポートに加えて独自の設定を発表しました（クリシュナ・マダヴァン、Bingブログ）。核心は**二つの用途を分けたこと**です。会社文書の定義では、**「学習（training）」は生成AIモデルの学習済みパラメータを変更する利用**、**「グラウンディング（grounding）」はAIが回答を作るときに参考資料としてコンテンツを入れる利用**です。文書は従来のインデックス化と順位付けはグラウンディングではないと書いています。

設定は次の通りです。**学習**はAllow/Disallowの二値で、サイト全体はrobots.txtの`__usage_ai-training`グループ、ページ単位は`<meta name="Bingbot" content="ai-training:disallow">`または同じ内容のX-Robots-Tagヘッダーで書きます。ページ単位がrobots.txtより優先します。**グラウンディング**はAllow / DisallowExtended / Disallowの三値で、**ページ単位（meta・ヘッダー）でのみ**書きます。サイト全体用のrobots.txt設定はありません。DisallowExtendedはMicrosoftが直接運営する体験（AIモード・AIオーバービュー・Copilot・Microsoft 365）でのみ引用を許し、第三者に販売するグラウンディングサービスでは拒む値です。**何も書かなければ両方ともAllow**です。会社文書はこの選好が「従来のBing検索結果の資格を変えない」と書きつつ、同時にグラウンディングをDisallowやDisallowExtendedにすると「AIが生成する体験での露出が大きく減る」と書きました。どちらを選んでも露出・トラフィック・対価を保証しないという文もあります。

日付は四つです。**2026年12月15日**、Bingウェブマスターツールに一時的なグラウンディング設定が開きます（その日時点でNoArchive・NoCacheを使うサイトのみ）。**2027年2月1日**、新しい選好がクロールされ次第適用されます。**2027年3月1日**を過ぎると、2023年から使われてきたNoArchive・NoCacheは学習・グラウンディングの選好としては読まれなくなります。**2027年9月30日**、一時的なグラウンディング設定が終わります。文書はIndexNowで再クロールを要請できるが日付は保証しないと付け加えました。

## 短く — Anthropicの上場書類修正版（事実）

11月2日、AnthropicはS-1の修正版に第3四半期の数字を入れました。私たちは今回EDGARの原文がfetch遮断で開けなかったため、**メディア四社（Fortune・Business Insider・SiliconANGLE・Investing.com）が書類を引用した数値**を伝えます。第3四半期（7〜9月）の売上約**170億ドル**（第2四半期116億、前年同期14億 — Fortune）、営業費用175億、**営業損失5億6,700万ドル**（第2四半期は営業利益9億7,400万。SiliconANGLEだけが5億3,600万と書き、メディア間で差があります）、純損失233億ドルの大部分は転換社債の公正価値変動による会計上の費用です。営業損失の主な理由として書類が挙げたのは**「短期の約定で買ったコンピューティング50億ドル」**（Business Insider・SiliconANGLE）と、従業員の寄付マッチングプログラムの非現金費用20億ドルです。第2四半期から第3四半期の間に**値下げで売上が約6億ドル減った**という文はFortune一社が伝えました。コンピューティングとインフラの購入・リース約定の合計は**8,954億ドル**（四社一致）で、そのうち2030年までに4,475億・12か月以内に698億という内訳はInvesting.com一社の整理です。NO.30で「使う値段は半分に、作る費用は月に数十億」と書きましたが、この書類はその二つが同じ四半期に一つの会社の中で出会ったことを示しています（解釈）。投資判断の資料ではなく、公募の規模・価格・時期は書きません。原文を直接読んだ後、「値段と費用」の続編として改めて扱います。

## 二つの話題を併せて読むと（解釈）

第一に、**一行は鍵ではなく宣言です。**草案自身が「クロール行動の指示ではない」と書き、Googleの社員は「30秒でなりすませる」と言います。この一行がすることは、「私たちの記事を学習に使わないでほしい」という意思を四社が同じ方法で読むようにするところまでです。守るかどうかは各社の約束にかかっており、守られたかどうかをサイト側で確認する方法は今のところありません。それでも、この3年間のように会社ごとの名前を別々に探す作業は減ります。特に小さなチームには、**「新しいAI会社が現れるたびにrobots.txtを直す作業」が「トークン一つをその会社が受け入れるか確認する作業」に変わること**が実質的な変化です（解釈）。

第二に、**学習と引用は別の問いです。**Bingだけが二つを分け、共通トークンは学習だけを扱います。GoogleはトークンをGoogle-Extendedの拒否と解釈しますが、Googleの文書によればGoogle-Extendedは学習だけでなくGeminiアプリ・Vertexのグラウンディングも併せて制御します。すると共通トークン一つで「学習は拒否、Gemini回答での引用は許可」をGoogleにどう表現するかが空白になります。私たちはこの部分をGoogleの文書で確認できず、Googleが2027年にサポートを始めるときに埋まる問いとして残します。Bingが「引用を止めるとAI体験での露出が大きく減る」と書いたのは率直な文で、NO.28で見た「商業検索の88%にAI要約」と同じ方向です。**学習を拒むことと引用を拒むことは、サイトにとって別の費用がかかります**（解釈）。

第三に、**「人が頼んだ行為」は外側にあります。**ヘイクの指摘どおり草案は利用者が直接要請して取得するものを事実上例外にし、ケリーのメールも「解釈は変わりうる」と書いています。私たちの記事がAIチャットで誰かの質問に答える中で読まれることは、このトークンとは別に続きます。それを止めるかどうかは別の決定で、私たちは止めない側です。AP Newsは読まれるために書く記事だからです（解釈）。

## 私たちなら — 今週決める三つのこと（実践）

1. **コンテンツを三つの束に分け、「学習／引用」の二つの欄を埋める。**私たちのホームページのrobots.txtを直接開くと、`User-agent: *`の一グループにAllowとフォルダのDisallow（ソース・スクリプト・バックアップ・文書、校閲前の四言語）だけがあり、AIトークンは一つもありませんでした。草案の規則では`*`はトークンに適用されないので、**私たちは今、何の選好も表現していない状態**であり、Bing基準では両方ともAllowです。そこでまず決定表を作ります。①AP News・製品紹介・会社紹介は「学習許可・引用許可」— 読まれるために書く記事だからです。②ソース・スクリプト・バックアップ・内部文書のフォルダはすでにクロールを止めていますが、これは通行規則であって学習選好ではないので、トークングループにも同じパスをDisallowで書いておきます。③利用者の文章が混じるページ（レビュー・掲示板・問い合わせ）は「学習拒否」と書き、引用はBingでDisallowExtendedにします。決定表はNO.29の権限表の隣に置き、四半期ごとに見直します。
2. **書くときはトークングループを別に追加し、会社別の名前もそのまま残す。**草案・Google・Anthropicのいずれも「既存の制御は引き続き機能する」としているので、`__usage_ai-training`グループを**追加**し、Google-Extended・GPTBot・ClaudeBotなど既存のグループは消しません。`*`に書いたものがトークンに適用されるとは期待しません。Bingのグラウンディング選好はrobots.txtにはなくページ単位のmeta・ヘッダーだけなので、③の束のページテンプレートにだけ入れます。カレンダーには**2027年2月1日**（Bing適用）と**3月1日**（NoArchive・NoCacheが選好として読まれなくなる）を書き、2月の第1週にGoogleとOpenAIが実際にサポートを始めたかを各社の文書で改めて開いて確認します。公式文書が開けなければメディア二社の照合で確認します。
3. **「書いた」と「守られた」を別の欄に置く。**このトークンが守られたかどうかをサイト側で知る方法はありません。だからできることだけをします。サーバーログでAIクローラー名（GPTBot・ClaudeBot・Bingbotなど）の訪問を**月1回**集計し、Google-Extendedには独自のクローラー名がなくログには出ないという点を表に書いておきます。Google Search ConsoleのAIパフォーマンスレポートにクリックデータが入らない可能性があるという話（イリーズの発言、Search Engine Roundtableの11月2日まとめ、一か所）は注記を付けて参考にとどめます。3か月後、各社の文書で「学習」の定義が変わったかを再確認します。選好を書いたという事実を「AIは私たちの記事を使わない」とは報告しません。

## 今回選ばなかったもの

RedditのCEOがGoogle検索トラフィックの減少を認めたという報道（11月2日、Search Engine Roundtable）は、発言の原文と決算説明会の資料を開けず次回に回しました。SemiAnalysisが11月2日に出したエージェント・ベンチマークGDPx（11領域、最高モデルでも12%、金融・法務は二値採点で全て0）はAnthropicのモデルが1位で私たちには利害関係が大きく、他メディアの照合もまだ少ないため、NO.33・34の「スコアボードが測るもの」の続編として別に扱います。Alphabetの60億ユーロ債・Oracleの200億ドル調達（TNWがロイターを引用）は「短く」の約定の数字と同じ系列ですが、投資判断の資料と読まれうるため「値段と費用」の続編で併せて見ます。OpenAIがデータセンターを「コンピュート・キャンパス」と呼ぶという報道（Axios・Business Insider）は本文を開いていません。流出や噂として出回ったモデルの話とカーネル欠陥のエクスプロイトの話は、公式確認がないか攻撃側の記述になるため書きません。

## この話題で確認できなかったこと

- OpenAIの公式記事（「Helping websites express AI training preferences」）はfetch遮断で開けませんでした。「数か月以内」はEngadget一社の伝聞で、PPC Landは時期はなかったと書きました。GPTBotなどどのクローラーがトークンを読むかも確認できていません。
- Google Search Centralブログの本文は私たちのfetchでは目次しか見えず、メディア二社が引用した文で確認しました。共通トークンだけを止めた場合にGeminiアプリのグラウンディングまで止まるのかは、Googleの文書で見つけられませんでした。
- Anthropicの「すでに実装を始めた」は著者のメール一通で、適用クローラー・時期はありません。Anthropicの公式文書（クローラー案内）に反映されたかは確認していません。
- Bing文書の日付・設定は直接確認しましたが、「従来の検索の資格を変えない」は会社の言葉で、独立した検証はありません。
- 「短く」の数値はすべてメディアが書類を引用したものです。営業損失（5億6,700万対5億3,600万）はメディア間で差があり、値下げ6億・2030年までの4,475億・12か月の698億・コンピューティング費用99億はそれぞれ一か所です。EDGARの原文が開けたら照合します。

## 併せて読んだ記事

性格の異なる出典を直接開いて確認しました。標準文書、会社の公式文書・発言、メディア報道に分けて記します。

標準文書：

- [Machine-Readable Training Preference Signal, draft-kelley-aipref-training-preference-signal-00（IETF Datatracker）](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/) — 英語、トークンの定義・「クロール指示ではない」・ワイルドカード規則・私的契約条項

会社の公式文書・発言：

- [Your content, your choice: clearer preferences for training and grounding（Microsoft Bingブログ）](https://blogs.bing.com/search/2026/10/your-content-your-choice-clearer-preferences-for-training-and-grounding/) — 英語、学習・グラウンディングの定義、三つの設定、構文、四つの日付
- [Supporting a shared AI training control for websites（Google Search Centralブログ）](https://developers.google.com/search/blog/2026/10/ai-training-control) — 英語、Googleの採用宣言（本文はメディア引用で確認）
- [Googleの共通クローラー文書 — Google-Extended項目（Google開発者文書）](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended) — 英語、Google-Extendedの範囲（学習・グラウンディング）、検索順位とは無関係、「2027年初め」サポートの注記
- [ケビン・ケリーのIETF ai-controlメール — Anthropicのサポート実装開始（IETF Mail Archive）](https://mailarchive.ietf.org/arch/msg/ai-control/mddjatOxSR0h6GmLRBWlc839c7w/) — 英語、「すでに開始」「数か月」「補完」「解釈は変わりうる」

メディア報道：

- [Google joins OpenAI and Anthropic in promising new scraping controls（Engadget）](https://www.engadget.com/2303225/google-openai-anthropic-ai-crawling-controls/) — 英語、四社の約束と時期、「過去の収集は取り消せない」
- [Google and Bing back one robots.txt rule to opt out of AI training（PPC Land）](https://ppc.land/google-and-bing-back-one-robots-txt-rule-to-opt-out-of-ai-training/) — 英語、ミューラー・イリーズ・ヘイクの発言、会社別の既存クローラー名
- [Google Also Adopts New AI Training Control（Search Engine Roundtable）](https://www.seroundtable.com/google-ai-training-control-42430.html) — 英語、Googleの文の引用、ミューラーのGoogle-Extended解釈、ヘイクの「利用者の行為は例外」の指摘
- [Anthropic's growth slowed and costs jumped in the third quarter, updated IPO filing shows（Fortune）](https://fortune.com/2026/11/02/anthropics-growth-slowed-and-costs-jumped-in-the-third-quarter-updated-ipo-filing-shows/) — 英語、「短く」の売上・営業損失・流動性・値下げ（一か所）
- [Anthropic's amended IPO paperwork reveals soaring Q3 revenue and a stunning compute bill（Business Insider、Yahoo Finance再掲）](https://uk.finance.yahoo.com/news/anthropics-amended-ipo-paperwork-reveals-153730799.html) — 英語、「短期約定のコンピューティング50億」の書類引用、コンピューティング費用99億（一か所）
- [Anthropic's quarterly revenue jumps to $17B, losses grow ahead of IPO（SiliconANGLE）](https://siliconangle.com/2026/11/02/anthropics-quarterly-revenue-jumps-to-17b-losses-grow-ahead-of-ipo/) — 英語、営業損失の表記の差（5億3,600万）、短期コンピューティング50億
- [Anthropic posts $17B third-quarter revenue as landmark AI debut nears（Investing.com）](https://www.investing.com/news/stock-market-news/anthropic-posts-17b-thirdquarter-revenue-as-landmark-ai-debut-nears-4992371) — 英語、営業費用175億、約定の年別内訳（一か所）

私たちの以前の記事：

- [AIが広告文を代わりに書き直し始める — 商業検索の88%にはAI要約が出る（AP News NO.28）](https://www.apholdings.kr/ko/news/ai-rewrites-your-ads-what-to-check/)
- [ChatGPTのウェブシェアが再び上がった — この数字が数えていないもの（AP News NO.25）](https://www.apholdings.kr/ko/news/chatgpt-share-rebound-what-web-misses/)
- [エージェントは「信頼できない内部者」だ — 「権限0から始める」提案（AP News NO.29）](https://www.apholdings.kr/ko/news/agents-are-insiders-permission-checks/)
- [使う値段は半分に、作る費用は月に数十億ドル — AnthropicはS-1にコンピューティング費用を書いた（AP News NO.30）](https://www.apholdings.kr/ko/news/half-price-terra-and-the-s1-compute-bill/)
