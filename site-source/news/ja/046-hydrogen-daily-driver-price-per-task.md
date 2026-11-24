---
no: 46
slug: hydrogen-daily-driver-price-per-task
date: 2026-11-13
category: インサイト
tags: Gemini 4 Hydrogen · Google · モデル価格 · Artificial Analysis · Epoch AI · 推論コスト · モデル選択 · AlphaProof Code
title: 「毎日使うモデル」の欄ができた — GoogleはGemini 4 HydrogenをFlashの2倍の価格で出し、独立評価機関は「Argonより1点上、1タスク1.87ドル」と測り、Epochはチップ1個が同時に受けられるリクエスト数を数えた
summary: 11月12日、GoogleはGemini 4 Hydrogenを公開しました。位置づけは「CarbonとArgonは深く考え、Hydrogenは毎日の仕事を速く終える」で、価格は100万トークンあたり入力1.50ドル・出力7.50ドルとGemini 3.8 Flashの2倍です（Flash自体も2027年1月1日に同じ価格になるとVentureBeatは整理しています）。API・アプリ・検索に一度に入り、無料ユーザーにも自動モデル選択で届きます。独立評価機関Artificial Analysisは既定設定で知能指数51（Argon 50）、1タスクあたり1.87ドルと測りました。Epoch AIは11月9日に「推論性能指数」を出し、チップ1個が同時に受けられるリクエスト数を数え、最新チップはFLOP/sでは2.5倍なのにこの数え方では25倍だと書きました。三つを「トークン単価ではなくタスク単価で読む方法」としてまとめ、最後に「短く」として、Google DeepMindがSignalプロトコルのコードを4週間で形式検証したという発表を記します。
---
> この記事はAI（Claude）と共同で作成し、編集者が検証しました。当社はAnthropicとOpenAIの2社の有料顧客で、Googleのモデルも試験に使っています。1番と「短く」はGoogleの発表で、Googleはこの記事を書いたAIの製造元（Anthropic）と競合します。2番の独立評価の順位表ではAnthropicのモデルが最上位にあるため、**評価は加えず数字だけを写しました。** 企業が発表した数値は「企業が発表したもの」と表記し、この記事は特定企業への投資意見ではありません。

NO.45で「モデルの扉はまず一部に開き、2か月後に価格が2倍になる」と書きました。そのときのGoogleの発表記事は「ほとんどのソフトウェア・知識作業はArgonで」でした。2日後、Googleはその下にもう一つ欄を作りました。**「毎日使うモデル」**の欄です。この記事はその欄の価格を三つの数え方 — 企業が付けたトークン単価、独立機関が測ったタスク単価、そしてその価格の底にあるチップの容量 — で読みます。事実・解釈・私たちならに分けて記します。

## 1. Google — Gemini 4 Hydrogen、「CarbonとArgonは深く考え、Hydrogenは毎日の仕事を速く」（事実）

Googleは11月12日（木）に**Gemini 4 Hydrogen**を公開しました（企業発表、筆者はGoogle DeepMindのコライ・カブクチュオール）。位置づけは一文です — **「CarbonとArgonは深く考える。Hydrogenは毎日の仕事を速く終える。」** コーディングで言えば、設計判断はCarbon・Argonが、コードを書きテストを回し変更を確認する仕事はHydrogenが担う図で、Antigravityの中では**Orchestrator**が一つのセッション内でCarbonとHydrogenを行き来して使います。パラメータ数は書かれていません。思考の段階はlow・medium・high（既定）に**xhigh**が新たに加わって四つ、コンテキストは入力100万トークンに出力も100万トークンまでです。

価格は**100万トークンあたり入力1.50ドル・出力7.50ドル**で、100万トークンのコンテキスト全体で同じ価格です。投入先は一度に広い範囲です。Gemini APIとGoogle AI Studio（全階層）、Android Studio（有料）、Antigravity（Google AI Pro・Ultra加入者）、Gemini for business、Geminiアプリのモデル選択 — そして**無料ユーザーには自動モデル選択で**、**Google検索には世界中のすべてのユーザーに**入ります。Google SheetsのGeminiにはPro・Ultra加入者から入ります。

企業が発表した数字は次のとおりです。既定（high）設定でGemini 3.8 Flashより**2.5倍速く**タスクを終え、Terminal-Bench 4.1は**57%**（3.8 Flash 18.2%）、HLE-Diamond 58.8%、Artificial Analysis知能指数**51（Argon 50）、xhighで54**です。AntigravityのOrchestrator（Carbon+Hydrogen）はTerminal-Bench 4.0でCarbon単独に近い成功率を**クォータ24%減・19%速く**出したとしています。初期パートナー試験で複雑なグラフ・SQL・データ作業が2〜2.8倍速くなりトークンは12〜23%減ったこと、作り話の主張が3.8 Flashの5分の1以下であること、エージェントタスクで権限を越える行動が最大81%減り、塞がれたタスクで権限の境界を迂回する可能性が半分であること、間接プロンプトインジェクションに2.3倍強いことも、すべて企業が発表したものです。モデルカードは記事にリンクされており、私たちは開いていません。

企業の表には**負けている欄**もあります。The Decoderが写した表で、ArgonがHydrogenを上回る項目はChartography（71.6%対66.6%）、Carbonが上回る項目はAgents' Last Exam v1.1（77.4%対71.6%）とOSWorld-2.1（81.5%対77.6%）です。Digital Trendsは同じ表で科学・数学、コンピュータ操作、Terminal-Bench 4.1においてHydrogenが競合モデルに劣るが差は小さいと書き、VentureBeatはGoogleの表のTerminal-Bench 4.1の欄にClaude Sonnet 5.5が63.9%と記されていると写しました（VentureBeat 1か所）。Argonは思考段階がmedium・highの二つだけなので、企業が「Argonより1点上」とした比較はHydrogenの既定段階対Argonの既定段階です。

## 2. 価格表 — 1か月で変わったもの、そして独立機関が測った「タスクあたり」の価格（事実）

VentureBeatが整理した価格表を私たちの以前の記事と合わせて記します（すべて100万トークンあたり入力/出力、標準階層）。**Hydrogen 1.50/7.50。** Gemini 3.8 Flashは**12月31日まで0.75/3.75、2027年1月1日から1.50/7.50** — つまりHydrogenの価格は「Flash導入価格の2倍」であり「2か月後のFlash価格と同じ」です。Gemini 4 Argonは導入価格2/10から4/20へ、Gemini 4 CarbonはNO.45で記したとおり**11月30日まで2/10、その後4/20**です。Claude Fable 5.2はNO.44で記したとおり8/40です。Googleの価格ページは私たちの側で開くとGemini 3.5 Flashまでしか見えない旧版だったため、Flashの2027年値上げとArgonの移行は**VentureBeat 1か所の整理**でのみ確認しました（同じ日付を記した開発者ブログは複数ありますが、信頼できる媒体とは数えていません）。Hydrogenのキャッシュ入力0.075ドル、バッチ・フレックス半額も同じ記事にしかありません。

独立評価機関**Artificial Analysis**のHydrogen（high）モデルページを11月13日に直接開きました。知能指数v5.0.1で**51（78モデル中21位）**、**1タスクあたり1.87ドル**、混合単価1.10ドル（キャッシュ7：入力2：出力1基準）、キャッシュ割引95%、指数を1回回すのに出力トークン1億1,000万個（同クラス中央値7,280万個）です。速度・幻覚の数値はまだ空欄です。同機関の順位表ページを開くと**Claude Fable 5.2（max）65、Gemini 4 Carbon（high）60、Claude Opus 5.5（max）59、GPT-6 Astra（max）57、GPT-6.1 Sol（max）55、Claude Sonnet 5.5（max）55**で、Argon（high）は50です。私たちが開いた順位表ページにHydrogenはまだなく、xhigh 54・medium 41・low 27と段階別のタスク単価（3.16・0.80・0.29ドル）、Terminal-Bench 4.0 54%（Sonnet 5.5 max 64%）はVentureBeat・The Decoder・OfficeChaiの3媒体が同じ数字を写したものです。そのうち**3.8 Flash（high）が指数31で1タスク7.77ドル**という数字はVentureBeat 1か所にしかありません。

## 3. Epoch AI — 「推論性能指数」、チップ1個が同時に受けるリクエスト数（事実）

Epoch AIは11月9日に**推論性能指数（Inference Performance Index、IPI）**v1を出しました（筆者ジェイソン・リー、データは11月6日更新）。測るのはFLOP/sではなく**「チップ1個が要求出力速度50〜400トークン/秒の範囲で同時に受けられるリクエスト数」**で、NVIDIA GB300 1個を1とする相対値です。モデリング条件はエージェント作業に合わせています — キャッシュ済みコンテキスト26万2,144トークン、プリフィル1,024トークン、出力トークン1個あたり新規入力約1.51個、投機的デコーディング3トークン採択。Kimi K3・GLM-5.2・Qwen3-Coder-480B・MAI-Base-2の代理モデルの四つの平均です。

結果はこうです。**GB300はH100の約25倍**の推論容量を出すが8ビットFLOP/sでは2.5倍で、FLOP/sだけ見ると差を約10倍小さく見ること。同じチップでも72個を一つの高帯域の束にするGB300 NVL72が8個束のB300 HGX（0.54）より約1.9倍であること。H200 HGX 0.12、MI355X約0.55、VR200（Vera Rubin）2.18。そして背景の数字を一つ — **OpenRouterでエージェント用APIキーが使ったトークンが人のキーの約7倍**（9月末）だったこと。限界も記事に書かれています。NVIDIAのシミュレータ（AISimulate）で出した「理論上の最高速度」の投影であって実測ではなく、ソフトウェアの成熟度で変わり、精度（FP8・FP4）がモデル品質を保つかは確認しておらず、平均方式（算術平均）を変えると古いチップの点数が大きく下がるとしています。実測（SemiAnalysis InferenceX）と比べると、モデリング値の50%仮定で平均約12%の差でした。筆者はNVIDIAでLLMサービングをしていた人で、この記事には資金源が書かれていません（ECIページにはGoogle DeepMind支援の文があるとNO.45で記しました — これは別の記事です）。

## 短く — Google DeepMindのAlphaProof Code、Signalプロトコルのコードを4週間で形式検証（事実）

Google DeepMindは11月10日に**AlphaProof Code**を発表しました（企業発表）。人間の専門家がSignalメッセンジャープロトコルのセキュリティ目標を形式仕様に移して検討し、AIエージェントがLean言語でその証明を書き自ら監査する構造です。企業が記した結果は — 中核の暗号コードの形式検証を**4週間**で終え（同様の仕事に専門家チームが数年かけたとしている）、エージェントが人間の検討に回した部分はコードの**約1%**、すでに修正済みのバグ2個をわざと戻し入れると、どちらも「このバージョンは安全でない」という機械検証済みの証明が出たというものです。証明の行数は本文が「600万行以上」、ページのメタデータが「300万行以上」と食い違っています。成果物は公開され技術論文がリンクされていますが、製品ではなく、公開予定もなく、「拡張にはさらなる研究が必要」と書かれています。ここまでが企業の発表で、私たちは論文を開いていません。

## 三つを一緒に読むと（解釈）

第一に、**モデル選択表の「既定の欄」が変わる速さが2か月から2日に縮みました。** NO.45のGoogleの記事は「ほとんどはArgon」で、今回の記事は「毎日はHydrogen」です。二つの言葉は矛盾ではありません — 企業は役割を三つに分け（Carbon：難しいタスク、Argon：ほとんどの作業、Hydrogen：毎日の実行）、Orchestratorのように**一つのタスクの中でモデルを切り替えて使うこと**を基本に敷きました（解釈）。NO.17で「作業別にどのAIを」と記しましたが、いまは企業がその表を自分のモデルの中で先に分けてくれます。表を写し取るのではなく、私たちのタスクがどの欄に入るかを私たちが測らなければなりません。

第二に、**トークン単価とタスク単価は別の数字です。** HydrogenのトークンはFlashの2倍の価格なのに、Artificial Analysisが測ったタスクあたりのコストはHydrogen 1.87ドル対Flash 7.77ドルです（Flashの数値はVentureBeat 1か所）。安いモデルがトークンを多く使えばタスクは高くなります。逆に同じモデルのxhighは出力トークンをほぼ2倍使うのでタスク単価もほぼ2倍（3.16ドル）です。NO.21で「数字を比べる前に数え方から」と記しましたが、価格表の数え方は**「単価 × そのタスクに実際に使ったトークン数」**です（解釈）。そして2027年1月1日のFlash値上げ、12月1日のCarbon値上げのように、**価格が変わる日付**が表の一部です。

第三に、**価格の底にはチップがあり、その数え方もFLOP/sではありません。** Epochの指数は「同時にいくつ受けるか」で測り、その基準では世代差が10倍大きくなります。エージェントキーが人のキーの7倍のトークンを使うという数字と合わせて読めば、モデル価格が下がる理由の一部はモデルではなくサービング側にあるかもしれないという意味です（解釈 — Epochの値はモデリングで、実際の値下げとのつながりはEpochも私たちも測っていません）。小さなチームがチップを選ぶことはありませんが、**「価格はさらに下がりうる」を前提に表を組んでよいか**の根拠としては読む価値があります。

## 私たちなら — アプリ・コマース・AIチャンネルを運営するチームが今週やる三つ（実践）

1. **NO.45のCarbon試験3件にHydrogenを加え、4モデルで回す。** NO.17の私たちの試験（成分表判定・アプリ文言・Lia台本の下書き）をArgon（high）・Carbon（high）・Opus 5.5（high）・Hydrogen（high）で**同じ段階同士**で回し、結果の横に「企業発表 / 私たちが確認したもの」の2行を記します。今回は欄を一つ足します — **そのタスクに実際に使った入力・出力トークン数。** SafeListの成分判定のように短く繰り返すタスクが「毎日使うモデル」の欄に入るか、Lia台本のように長いタスクはどの欄かを、私たちの数字で決めます。
2. **単価表に「タスクあたりコスト」列を付ける。** モデル別のトークン単価の横に私たちのタスク三つの「単価 × 実トークン数」を記し、価格が変わる日付（Carbon 12月1日、Flash 2027年1月1日）を表の頭に置きます。NO.41でLiaの15秒動画の単価（Gemini Omni）を記したように、動画も同じ列に置きます。「安いモデル」ではなく「安いタスク」を選ぶ表です。
3. **夜に回してもよい仕事のリストを作る。** キャッシュ割引95%（Artificial Analysisページ）とバッチ半額（VentureBeatの伝聞 — Googleの価格ページで確認できたら）は「今すぐ」でない仕事にだけ適用されます。商品説明の一括点検、週報の下書き、翻訳の初稿のように、人が朝に確認すればよい仕事を書き出し、その仕事だけをバッチ・キャッシュで回します。ここでも「取り消せない段階」（NO.45）はリストの外です。

## 今回選ばなかったもの

Anthropicのニュースページの11月12日の項目は題名なしで日付だけが見え、Manufacturing Diveは同じ日に「Claude for Manufacturing」（スキル17個のプラグイン）の発表を伝えました — この記事を書いたAIの製造元の製品なので題名だけ記します。Google DeepMindのGemini Robotics 2.5（11月10日、200余りのタスク・Mercedesのキッティング96%）とAlphaGenome 2は私たちの仕事から遠いので題名だけ置きます。Mistralが11月5日に出したStudio（マネージドエージェント・ワークフロー・アプリ、クラウド・VPC・オンプレミス）は価格がなく数値がすべて企業発表なので、「小さなチームのエージェント運用層」の続編候補に置きます。Box CEOの「精度74%→79%」はXの投稿の伝聞なので使いませんでした。BigGoの「GoogleがFlashの名前を引退させた」はGoogleの記事にない表現なので使わず、Googleのモデル文書には11月13日時点でもArgonだけでCarbon・Hydrogenはありません。Gemini 4 Hydrogenのモデルカードは開いていません。

## このニュースで確認できなかったもの

- Googleの価格ページが私たちの側で旧版として開いたため、Gemini 3.8 Flashの2027年1月1日の値上げ（0.75/3.75→1.50/7.50）、Argonの導入価格終了、Hydrogenのキャッシュ入力0.075ドル・バッチ半額はVentureBeat 1か所の整理です。同じ日付を記した開発者ブログは信頼できる媒体とは数えていません。
- Artificial Analysisのページで直接見たのはHydrogen（high）51・1.87ドル・1.10ドルと順位表の6モデルの点数です。xhigh 54・medium 41・low 27、段階別タスク単価、Terminal-Bench 4.0 54%は媒体3か所が同じ数字を写したもので、3.8 Flashの指数31・1タスク7.77ドルはVentureBeat 1か所です。
- 企業の表のClaude Sonnet 5.5 63.9%（Terminal-Bench 4.1）はVentureBeat 1か所が写したもので、Googleの発表記事で私たちが直接確認したのはHydrogen 57%・Flash 18.2%です。パートナー試験（2〜2.8倍）と安全性の数値はすべて企業発表で、独立の確認はありません。
- EpochのIPIはシミュレータで出したモデリング値で実測ではありません。「エージェントキーのトークン7倍」はEpochがOpenRouterのデータを読んだもので、私たちは元データを開いていません。
- AlphaProof Codeの「600万行」と「300万行」の差は記事内の不一致で、技術論文は開いていません。

## 一緒に読んだ記事

性格の異なる出典を直接開いて確認しました。企業発表、研究・評価機関、媒体報道、ウィキ、私たちの以前の記事に分けて記します。

企業発表：

- [Introducing Gemini 4 Hydrogen for Agentic Workflows（Google、11月12日）](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) — 英文、位置づけ・価格・公開範囲・思考段階4つ・ベンチマークと安全性の数値（企業発表）
- [Gemini 4 Hydrogen: everyday coding and agentic workflows for developers（Google、11月12日）](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-hydrogen/) — 英文、開発者向け経路・Orchestrator（価格・Flashへの言及なし）
- [Introducing AlphaProof Code（Google DeepMind、11月10日）](https://deepmind.google/blog/introducing-alphaproof-code/) — 英文、Signalプロトコルの形式検証・4週間・約1%・戻し入れたバグ2個（企業発表）

研究・評価機関：

- [Gemini 4 Hydrogen（high）— Artificial Analysisモデルページ](https://artificialanalysis.ai/models/gemini-4-hydrogen-high) — 英文、知能指数51（v5.0.1）・1タスク1.87ドル・混合単価1.10ドル・キャッシュ割引95%
- [Artificial Analysisモデル順位表](https://artificialanalysis.ai/leaderboards/models) — 英文、Fable 5.2 65・Carbon 60・Opus 5.5 59・Astra 57・Sol 55・Sonnet 5.5 55・Argon 50（私たちが開いた時点ではHydrogenなし）
- [Inference Performance Index（Epoch AI、11月9日）](https://epoch.ai/publications/inference-performance-index) — 英文、指数の定義・GB300 25倍・VR200 2.18・エージェントキー7倍・限界と検証

媒体報道：

- [Google launches Gemini 4 Hydrogen — a faster, smarter, pricier Flash successor（VentureBeat、11月12日）](https://venturebeat.com/technology/google-launches-gemini-4-hydrogen-a-faster-smarter-pricier-flash-successor) — 英文、価格表（Flashの2027年値上げ・Argon・Carbon）・AA段階別タスク単価・Flash 7.77ドル・Sonnet 5.5 63.9%（1か所）
- [Google's Gemini 4 Hydrogen outscores the bigger Argon just four weeks after its launch（The Decoder、11月12日）](https://the-decoder.com/googles-gemini-4-hydrogen-outscores-the-bigger-argon-just-four-weeks-after-its-launch/) — 英文、企業の表のHydrogen/Argon/Carbon比較（負けている欄を含む）・AA Terminal-Bench 54%・xhighトークン2倍の但し書き
- [Gemini 4 Hydrogen Places Ahead Of Gemini 4 Argon, Muse Wonder And GPT 6.1 Terra On Artificial Analysis Intelligence Index（OfficeChai、11月12日）](https://officechai.com/ai/gemini-4-hydrogen-artificial-analysis-intelligence-index/) — 英文、AA順位の整理・段階別の点数とコスト
- [Google launches Gemini 4 Hydrogen for faster coding and agentic tasks（Interesting Engineering、11月12日）](https://interestingengineering.com/ai-robotics/google-gemini-4-hydrogen-coding-benchmark) — 英文、企業数値の整理・OrchestratorはUltra加入者から
- [Google's next-gen Gemini 4 Hydrogen AI model is here, touting faster intelligence for all（Digital Trends、11月12日）](https://www.digitaltrends.com/cool-tech/googles-next-gen-gemini-4-hydrogen-ai-model-is-here-touting-faster-intelligence-for-all/) — 英文、無料ユーザーの自動選択・検索全体・企業の表で劣る項目
- [Anthropic launches 'Claude for Manufacturing'（Manufacturing Dive、11月12日）](https://www.manufacturingdive.com/news/anthropic-launches-claude-for-manufacturing/874303/) — 英文、Anthropicの11月12日の発表（題名のみ記録）

ウィキ：

- [Gemini (language model)（Wikipedia）](https://en.wikipedia.org/wiki/Gemini_%28language_model%29) — 英文、Flash系列の年表（3.8 Flashは9月2日公開、Google文書を引用；Gemini 4世代の項目はまだない）

私たちの以前の記事：

- [客のエージェントは止め、店は入れ、モデルは皆に（AP News NO.45、同じ回で公開）](https://www.apholdings.kr/ko/news/united-blocks-agents-chatgpt-opens-storefronts/)
- [同じモデルに扉が二つ（AP News NO.44、同じ回で公開）](https://www.apholdings.kr/ko/news/fable-5-2-two-doors-and-sandbagging-logs/)
- [週間AIニュース — 安くなった扉（AP News NO.41、同じ回で公開）](https://www.apholdings.kr/ko/news/weekly-2026-11-07/)
- [スコアボードに確率が付いた（AP News NO.40）](https://www.apholdings.kr/ko/news/scoreboard-probabilities-and-four-rides/)
- [GitHubのプルリクエスト10件中4件はエージェントが開く — 新しいスコアボードの1位はまだ誰でも呼べるわけではない（AP News NO.33）](https://www.apholdings.kr/ko/news/agent-prs-40-percent-and-a-new-number-one/)
- [数字を比べる前に数え方から（AP News NO.21）](https://www.apholdings.kr/ko/news/count-before-you-compare/)
- [作業別にどのAIを使うか（AP News NO.17）](https://www.apholdings.kr/ko/news/which-ai-for-which-job/)
