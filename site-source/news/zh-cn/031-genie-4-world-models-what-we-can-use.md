---
no: 31
slug: genie-4-world-models-what-we-can-use
date: 2026-10-28
category: 洞察
tags: 世界模型 · Genie 4 · Google DeepMind · 视频制作 · AI网红
title: 谷歌造出了「有声音的世界」—— Genie 4 展示的世界模型现状、没有数字的官方发布该怎么读、做视频的小团队现在该做什么
summary: 10月27日，Google DeepMind 发布了世界模型 Genie 4。你可以实时走进一行文字生成的世界，用说话改变天气、镜头和人物，而且它首次把音乐、环境音和对话一起生成出来。但官方文章里没有任何数字——没有分辨率、时长或延迟——目前能用的人也只有「受信任的测试者」。我们把前代 Genie 3 的公开数据、竞争对手 Runway 的模型以及 AMD 收购 World Labs 放在一起，梳理世界模型走到了哪一步。然后写下像我们这样制作 AI 网红视频的团队，面对这条消息马上该做什么、不该做什么。
---
> 本文由 AI（Claude）协助撰写，并经编辑审核。开发 Claude 的 Anthropic 是本文主角谷歌的竞争对手，而我们公司是 Claude 和谷歌 AI 工具的付费用户。公司发布的性能和功能均标注为「公司发布的内容」，官方文章中没有的数字会注明出自哪家媒体的报道。本文不构成买卖任何公司股票的建议。

「世界模型」这个词因 2018 年 David Ha 与 Jürgen Schmidhuber 的论文标题而广为流传。那篇论文的想法是：智能体压缩地学习周围环境如何随时间和空间变化，先在那个「梦境」里练习，再把学到的东西带回真实环境。八年后的 10 月 27 日，Google DeepMind 宣布已把这个想法推进到「实时走进一行文字造出的世界、用说话修改世界、还能听见声音」的程度。发布文很耀眼，却没有数字。本文用前代和竞争对手的公开数据来填补这个空白。

## 1. Genie 4 —— 公司发布的内容（事实）

Google DeepMind 于 10 月 27 日在博客发布 Genie 4（作者 Raia Hadsell、Diego Rivas、Hang Qi）。公司说明的特点如下。

- **连声音一起生成。** 公司写道，Genie 4 是「我们第一个原生生成音频的实时世界模型」。每个世界都有自己的环境音和音乐，角色会根据输入和事件进行对话。
- **一边运行一边用说话修改。** 模拟运行期间，可以用自然语言改变场景——「下雨」「镜头后拉」「加一个人」——Gemini 会把指令调整到适合周围场景，同时让世界继续推进。
- **物理和人的动作。** 它模仿空气阻力、碰撞等物理现象，公司称角色会对环境作出反应、动作自然。
- **Gemini 担任「导演」。** Gemini 3.8 Flash 观察场景，把目标拆成步骤，通过传入的画面确认每一步是否完成，并在世界变化或用户介入时修改计划。在机器人实验中，Gemini 4 Argon 把任务拆成步骤、像字幕一样发给 Genie，示例是 Apptronik 的人形机器人 Apollo 下跳棋。
- **谁能用。** 目前是面向「受信任的测试者」的研究预览。公司称将依次向 Google AI Ultra 订阅者的 Project Genie 以及 Gemini API、AI Studio 的早期访问合作伙伴提供，没有公开发布日期。Project Genie 的等候名单已开放。
- **自己写下了限制。** 公司称「视觉细节和物体的持续性仍可能随时间漂移」，尤其在较长的会话、多次修改或在场景中移动之后；复杂的物理交互、实时音频的准确性、可读的文字、空间准确性和长期一致性都列为「研究中」。公司自己的措辞是「早期实验模型」。所有生成的视频和音频都带有 SynthID 水印。

文章还列出了测试者尝试的领域。电影制作者把它当「草稿模式」，一边改镜头、灯光、台词、动作一边跑多个版本；摄影记者把一张二维资料照片变成可以走动的环境；游戏开发者用语言快速试验视觉风格和规则；企业合作伙伴则用来快速生成场景。

**官方文章里没有的东西。** 分辨率、每秒帧数、一次能保持的时长、延迟、任何一致性的测量数值——DeepMind 的文章和谷歌官方博客里一个都没有。TechCrunch 依据简报报道称它「能把场景一致地保持最多两分钟，是 Genie 3 的两倍」，韩国媒体 DigitalToday 引用 TechCrunch 写了同样的数字。换句话说，「两分钟」是来自单一媒体报道线索的数字，官方文件中没有。TechCrunch 转述的 DeepMind 工程师 Rivas 的话比数字更坦率：实时交互最有价值的阶段是「构思和分镜」，而「从头到尾的产品体验还不清楚」。

## 2. 数字在前代和竞争对手那里（事实）

官方文章没有数字时，我们把同一家公司上一次的发布和竞争对手的公开数据放在旁边。

- **Genie 3（Google DeepMind，2025 年 8 月 5 日）。** 官方文章有数字：720p 分辨率、每秒 24 帧、实时操控、「环境在几分钟内基本保持一致」，以及「视觉记忆可追溯至一分钟前」。它是只对少数学者和创作者开放的有限研究预览。当时列出的限制有：智能体可执行的动作范围、多个独立智能体之间的交互、真实地形的精确再现、文字显示，以及「几分钟而不是几小时」。引人注意的是，Genie 4 的限制清单与此几乎相同。声音和「导演」是新加的，限制则原样保留。
- **Runway GWM Worlds 2（2026 年 9 月 3 日）。** 视频生成公司 Runway 的世界模型同样是研究预览。官方文章的数字是 720p、每秒 24 帧、不限定时长地持续生成、音频 48kHz。台词作为文字输入的「动作」来处理。它写下的限制有：「实时生成以画质换速度」「快速转动镜头会破坏质感和形状」「长期记忆不完整」「参考图像只对第一帧有效」。也就是说 Runway 比谷歌早约两个月加入了声音，但谷歌的「第一个」限定在「实时世界模型之中」这一自家标准下，两种说法不一定冲突。我们没有办法核对两家公司的标准。
- **AMD 收购 World Labs（2026 年 9 月 28 日，AMD 公告）。** 芯片公司 AMD 宣布将以约 82 亿美元的全股票交易收购李飞飞创立的 World Labs。公告把 World Labs 描述为从文本、图像和视频生成、重建和模拟可交互三维环境的「空间智能模型」公司，并提到用于机器人学习的模拟技术。交易完成后李飞飞将出任 AMD 执行副总裁兼首席科学家，预计 2026 年底完成。公告没有使用「世界模型」一词。

TechCrunch 还提到《华尔街日报》关于亚马逊正在洽谈以约 70 亿美元收购 Decart 的报道，以及 Rivian 收购 Third Dimension，但我们没有找到官方资料，正文不作讨论。

## 怎么读一份没有数字的发布（解读）

第一，**「第一」和「最」只在公司自己划定的标准内成立。** 谷歌的「第一个原生生成音频」附带「实时世界模型」这个条件，而 Runway 约两个月前就以预览形式推出了带声音的实时世界模型。与其说谁错了，不如说两家公司画了不同的线。发布文里的最高级，要先找到那条线再读。

第二，**缺少数字的地方，前代的数字就是上限。** 如果 Genie 3 是 720p、24fps、「几分钟」，而 Genie 4 的文章没有数字，就没有理由假设分辨率或时长明显提升。媒体传出的「两分钟」也和 Genie 3 的「几分钟」相差不大。把这次发布的真正进展理解为**声音、操控、导演**这些功能，而不是数字，才是稳妥的读法。

第三，**「限制」段落比「功能」段落活得更久**——这和昨天的文章（NO.30）是同一个结论。Genie 3 和 Genie 4 的限制清单几乎一样，意味着一年两个月里这些问题没有被解决，下一代发布文里也可以先找同样的条目。文字读不清、跑得久了物体会变、声音不准——对真正要交付视频的人来说，这三条比功能更重要。

第四，是我们补充的解读。世界模型现在前进的方向**不是「成品视频」，而是「机器人和智能体的练习场」和「人的分镜板」。** 谷歌把机器人示例放在最前面，AMD 把机器人学习模拟写进收购理由，Rivas 把最有价值的阶段说成「构思和分镜」。2018 年论文「在梦境里练习」的想法原封不动。做视频的小团队如果把这条消息读成「视频生成更好了」，那就找错了门牌。

## 如果是我们 —— 制作 AI 网红视频的团队本周要做的三件事（实践）

1. **把世界模型和视频生成模型放在不同的格子里。** 我们的 Ria 视频现在是用视频生成模型（脚本→场景→剪辑）做的。Genie 4 不是替代这个位置的工具，而是**在确定场景之前用语言跑多个版本的「草稿模式」**。谷歌作为测试者案例举出的「电影制作者的草稿模式」和 Rivas 的「分镜阶段」就是这个位置。所以在我们的制作流程里，只把它作为候选写进「场景构思」一格，不写进「最终渲染」一格。Rivas 自己也说，把原型变成成品素材「还很远」。
2. **报名等候名单，但不改工作流。** Project Genie 的等候名单和 Gemini API 早期访问可以免费申请。但现在能用的只有「受信任的测试者」，又没有官方数字，所以在拿到之前，不把任何制作环节绑在这个工具上。拿到之后，按 NO.17 的测试方法跑我们的十个场景（Ria 的门店介绍、成分表讲解场景、篮球鞋对比场景等），先记录三项：**文字能否读清、两分钟内人物会不会变、声音和场景是否相符。** 公司自己写下的三条限制，就是我们的检查表。
3. **把水印和我们的标注对齐。** Genie 4 的全部输出都带 SynthID 水印。我们的 Ria 视频政策已经要求「明示 AI 人设」，方向一致。但水印是平台读的标记，我们的标注是人读的标记，二者不能互相替代。现在就先写下规则：如果加入了世界模型生成的场景，字幕标注里增加「部分场景为 AI 模拟」。在工具到来之前写好规则，总是更省钱。

## 这次没有选的内容

Anthropic 10 月 27 日的两项发布（新药研发初步成果、与美国总务署 GSA 扩大合作）和 Axios 关于「FTC 要求 Anthropic 高管作证」的独家报道，因为利益关系大且尚未交叉核实，没有收录。OpenAI 10 月 26 日的三篇文章（学术合作、CodeRabbit 案例、「ChatGPT 不断扩大的工作世界」）正文还没读。LiteLLM 1.107.0 供应链攻击（10 月 21 日，已在该公司事件报告中确认）和 OpenAI 披露的 Brotli 压缩库缺陷性质不同，将在下一篇以「AI 工具供应链」为题另行讨论。亚马逊–Decart、Rivian–Third Dimension 没有找到官方资料。

## 这条消息里没能确认的事

- Genie 4 的分辨率、每秒帧数、保持时长和延迟在官方文章里没有。「最多两分钟，是 Genie 3 的两倍」是 TechCrunch 的报道（DigitalToday 引用），我们没能在任何官方文件中确认。
- 「第一个原生生成音频的实时世界模型」是公司自家的标准，它与 Runway GWM Worlds 2（9 月 3 日）的标准差异我们没能确认。
- 我们自己没有用过 Genie 4。功能描述全部来自公司文章和简报报道，没有找到独立机构的测量。
- Project Genie 和 Gemini API 的提供时间只写了「依次」和「几周内」（TechCrunch），无法确定日期。

## 一起读过的文章

我们直接打开并核对了不同性质的来源，分为公司官方文件、公告、论文、媒体报道和我们之前的文章。

公司官方文件：

- [Genie 4: A new generation of world simulation (Google DeepMind)](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) — 英文，官方发布（功能、限制、提供范围；无数字）
- [We're announcing Genie 4, our new world model for real-time interactive simulation (Google)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-genie-4/) — 英文，谷歌官方博客（提供顺序）
- [Genie 3: A new frontier for world models (Google DeepMind)](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — 英文，前代官方发布（720p、24fps、「几分钟」、一分钟记忆）
- [Introducing GWM Worlds 2 (Runway)](https://runway.com/research/introducing-gwm-worlds-2) — 英文，竞争对手官方研究文章（720p、24fps、48kHz 音频、限制）

公告：

- [AMD to Acquire World Labs to Advance the Future of AI Compute (AMD Investor Relations)](https://ir.amd.com/news-events/press-releases/detail/1299/amd-to-acquire-world-labs-to-advance-the-future-of-ai-compute) — 英文，公司公告（约 82 亿美元全股票、预计完成时间）

论文：

- [World Models — David Ha, Jürgen Schmidhuber (arXiv, 2018)](https://arxiv.org/abs/1803.10122v1) — 英文，「世界模型」概念的起点

媒体报道：

- [Google's Genie 4 world model adds audio, more realistic worlds, and real-time steering (TechCrunch)](https://techcrunch.com/2026/10/27/googles-genie-4-world-model-adds-audio-more-realistic-worlds-and-real-time-steering/) — 英文，科技媒体（简报、「两分钟」、Rivas 的发言、市场背景）
- [Google DeepMind Rolls Out Genie 4 World Model in Research Preview (Unite.AI)](https://www.unite.ai/google-deepmind-rolls-out-genie-4-world-model-in-research-preview/) — 英文，AI 媒体（官方文章交叉核对、Genie 3 对比）
- [Google DeepMind unveils Genie 4 world model, targeting robots and film production (DigitalToday 英文版)](https://www.digitaltoday.co.kr/en/view/120253/google-deepmind-unveils-genie-4-world-model-targeting-robots-and-film-production) — 英文，韩国媒体（引用 TechCrunch）

我们之前的文章：

- [使用的价格减半，制造的成本每月数十亿美元 (AP News NO.30)](https://www.apholdings.kr/ko/news/half-price-terra-and-the-s1-compute-bill/) — 韩文，如何读「公司自己写下的边界」
- [什么工作用什么 AI —— 公司自己说明的用途和我们的测试方法 (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — 韩文，按任务测试模型的方法
