---
no: 31
slug: genie-4-world-models-what-we-can-use
date: 2026-10-28
category: Góc nhìn
tags: Mô hình thế giới · Genie 4 · Google DeepMind · Sản xuất video · AI influencer
title: Google đã tạo ra "thế giới có âm thanh" — Genie 4 cho thấy mô hình thế giới đang ở đâu, cách đọc một thông báo chính thức không có con số, và đội làm video nhỏ nên làm gì ngay bây giờ
summary: Ngày 27 tháng 10, Google DeepMind công bố mô hình thế giới Genie 4. Bạn đi lại theo thời gian thực trong một thế giới tạo từ một dòng chữ, thay đổi thời tiết, máy quay và nhân vật bằng lời nói, và lần đầu tiên mô hình tạo ra cả nhạc, âm thanh môi trường và hội thoại cùng với hình ảnh. Nhưng bài viết chính thức không có một con số nào — không độ phân giải, thời lượng hay độ trễ — và hiện chỉ "người thử nghiệm tin cậy" mới được dùng. Chúng tôi đặt cạnh nhau số liệu công khai của bản tiền nhiệm Genie 3, mô hình của đối thủ Runway và thương vụ AMD mua World Labs để xem mô hình thế giới đã đi đến đâu. Rồi ghi lại những việc một đội như chúng tôi — làm video AI influencer — nên làm ngay với tin này, và những việc không nên làm.
---
> Bài viết này được soạn cùng AI (Claude) và do biên tập viên kiểm tra. Anthropic, công ty tạo ra Claude, là đối thủ của Google — nhân vật chính của bài — và công ty chúng tôi là khách hàng trả phí của cả Claude lẫn các công cụ AI của Google. Hiệu năng và tính năng do công ty công bố được ghi là "điều công ty công bố", và với con số không có trong bài chính thức, chúng tôi ghi rõ hãng tin nào đưa. Bài này không phải lời khuyên mua hay bán cổ phiếu của bất kỳ công ty nào.

Thuật ngữ "mô hình thế giới" lan rộng từ tên bài báo năm 2018 của David Ha và Jürgen Schmidhuber. Ý tưởng là một tác tử học một mô hình nén về cách môi trường xung quanh thay đổi theo không gian và thời gian, luyện tập trước trong "giấc mơ" đó, rồi mang điều đã học sang môi trường thật. Tám năm sau, ngày 27 tháng 10, Google DeepMind thông báo đã đẩy ý tưởng ấy đến mức "đi lại theo thời gian thực trong thế giới dựng từ một dòng chữ, sửa thế giới bằng lời nói, và còn nghe được âm thanh." Thông báo rất lộng lẫy, nhưng không có con số. Bài này lấp khoảng trống đó bằng số liệu công khai của bản tiền nhiệm và các đối thủ.

## 1. Genie 4 — điều công ty công bố (sự thật)

Google DeepMind công bố Genie 4 trên blog ngày 27 tháng 10 (tác giả Raia Hadsell, Diego Rivas và Hang Qi). Các đặc điểm công ty nêu ra như sau.

- **Tạo âm thanh cùng với thế giới.** Công ty viết Genie 4 là "mô hình thế giới thời gian thực đầu tiên của chúng tôi tạo âm thanh một cách bản địa." Mỗi thế giới có âm thanh môi trường và nhạc riêng, và nhân vật hội thoại theo đầu vào và sự kiện.
- **Vừa chạy vừa sửa bằng lời nói.** Trong lúc mô phỏng đang chạy, bạn có thể đổi cảnh bằng ngôn ngữ tự nhiên — "cho mưa", "lùi máy quay", "thêm một người" — và Gemini điều chỉnh chỉ dẫn cho hợp với cảnh xung quanh trong khi thế giới vẫn tiếp diễn.
- **Vật lý và chuyển động của người.** Nó mô phỏng các hiện tượng vật lý như lực cản không khí, va chạm, và công ty nói nhân vật phản ứng với môi trường và chuyển động tự nhiên.
- **Gemini đóng vai "đạo diễn".** Gemini 3.8 Flash quan sát cảnh, chia mục tiêu thành các bước, kiểm tra khung hình nhận được để xác nhận từng bước đã xong, và sửa kế hoạch khi thế giới thay đổi hoặc người dùng can thiệp. Trong thí nghiệm robot, Gemini 4 Argon chia nhiệm vụ thành các bước và gửi cho Genie như phụ đề; ví dụ là robot hình người Apollo của Apptronik chơi cờ đam.
- **Ai được dùng.** Hiện là bản xem trước nghiên cứu cho "người thử nghiệm tin cậy". Công ty nói sẽ lần lượt cung cấp cho người đăng ký Google AI Ultra qua Project Genie và cho đối tác truy cập sớm của Gemini API và AI Studio; không có ngày phát hành rộng rãi. Danh sách chờ Project Genie đang mở.
- **Tự ghi ra giới hạn.** Công ty nói "chi tiết hình ảnh và tính bền vững của vật thể vẫn có thể trôi dạt theo thời gian", nhất là trong phiên dài, sau nhiều lần sửa hoặc khi di chuyển trong cảnh; tương tác vật lý phức tạp, độ chính xác của âm thanh thời gian thực, chữ đọc được, độ chính xác không gian và tính nhất quán dài hạn đều được liệt kê là "đang nghiên cứu". Cách gọi của chính công ty là "mô hình thử nghiệm giai đoạn đầu". Toàn bộ video và âm thanh tạo ra đều có hình mờ SynthID.

Bài viết cũng kể các lĩnh vực người thử nghiệm đang thử. Nhà làm phim dùng nó như "chế độ nháp" để chạy nhiều lượt quay trong khi đổi máy quay, ánh sáng, lời thoại và hành động; phóng viên ảnh biến một bức ảnh tư liệu 2D thành môi trường có thể đi lại; nhà phát triển game thử nhanh phong cách hình ảnh và luật chơi bằng lời; đối tác doanh nghiệp dùng để tạo kịch bản nhanh.

**Điều không có trong bài chính thức.** Độ phân giải, số khung hình mỗi giây, thời lượng giữ được trong một phiên, độ trễ, hay bất kỳ số đo nhất quán nào — không cái nào xuất hiện trong bài của DeepMind lẫn blog chính thức của Google. TechCrunch, dựa trên buổi họp báo, đưa tin nó "giữ cảnh nhất quán tới hai phút, gấp đôi Genie 3", và báo Hàn Quốc DigitalToday dẫn lại TechCrunch với cùng con số. Nói cách khác, "hai phút" là con số từ một mạch tin báo chí duy nhất và không có trong tài liệu chính thức nào. Điều TechCrunch thuật lại từ kỹ sư Rivas của DeepMind còn thẳng thắn hơn mọi con số: giai đoạn mà tương tác thời gian thực có giá trị nhất là "lên ý tưởng và dựng storyboard", và "trải nghiệm sản phẩm từ đầu đến cuối vẫn chưa rõ ràng."

## 2. Con số nằm ở bản tiền nhiệm và đối thủ (sự thật)

Khi bài chính thức không có con số, chúng tôi đặt thông báo trước đó của cùng công ty và số liệu công khai của đối thủ bên cạnh.

- **Genie 3 (Google DeepMind, 5 tháng 8 năm 2025).** Bài chính thức có con số: độ phân giải 720p, 24 khung hình mỗi giây, điều khiển thời gian thực, "môi trường về cơ bản nhất quán trong vài phút", và "trí nhớ hình ảnh quay lại tới một phút". Đó là bản xem trước nghiên cứu giới hạn, chỉ mở cho một nhóm nhỏ học giả và nhà sáng tạo. Giới hạn khi đó gồm phạm vi hành động tác tử có thể làm, tương tác giữa nhiều tác tử độc lập, tái hiện chính xác địa hình thật, hiển thị chữ, và "vài phút chứ không phải vài giờ". Điều đáng chú ý là danh sách giới hạn của Genie 4 gần như giống hệt. Âm thanh và "đạo diễn" được thêm vào; giới hạn vẫn còn nguyên.
- **Runway GWM Worlds 2 (3 tháng 9 năm 2026).** Mô hình thế giới của công ty tạo video Runway cũng là bản xem trước nghiên cứu. Số liệu trong bài chính thức: 720p, 24 khung hình mỗi giây, tạo liên tục không giới hạn thời lượng, âm thanh 48 kHz. Lời thoại được xử lý như một "hành động" nhập bằng chữ. Giới hạn họ ghi: "thời gian thực đánh đổi chất lượng lấy tốc độ", "xoay máy quay nhanh làm vỡ chất liệu và hình khối", "trí nhớ dài hạn chưa hoàn chỉnh", "ảnh tham chiếu chỉ áp dụng cho khung hình đầu". Nghĩa là Runway gắn âm thanh trước Google khoảng hai tháng, nhưng chữ "đầu tiên" của Google đi kèm tiêu chí riêng "trong số các mô hình thế giới thời gian thực", nên hai tuyên bố không nhất thiết mâu thuẫn. Chúng tôi không có cách đối chiếu tiêu chí của hai công ty.
- **AMD mua World Labs (28 tháng 9 năm 2026, công bố của AMD).** Hãng chip AMD cho biết sẽ mua World Labs do Fei-Fei Li sáng lập bằng giao dịch toàn cổ phiếu trị giá khoảng 8,2 tỷ USD. Công bố mô tả World Labs là công ty "mô hình trí tuệ không gian" tạo, tái dựng và mô phỏng môi trường 3D tương tác từ văn bản, hình ảnh và video, và cũng nhắc đến công nghệ mô phỏng cho học robot. Bà Li sẽ trở thành phó chủ tịch điều hành kiêm nhà khoa học trưởng của AMD khi giao dịch hoàn tất, dự kiến cuối năm 2026. Công bố không dùng từ "mô hình thế giới".

TechCrunch còn nhắc đến tin của Wall Street Journal rằng Amazon đang đàm phán mua Decart với giá khoảng 7 tỷ USD, và việc Rivian mua Third Dimension, nhưng chúng tôi không tìm được tài liệu chính thức nên không bàn trong bài.

## Cách đọc một thông báo không có con số (diễn giải)

Thứ nhất, **"đầu tiên" và "nhất" chỉ đúng trong tiêu chí công ty tự chọn.** "Đầu tiên tạo âm thanh bản địa" của Google đi kèm điều kiện "mô hình thế giới thời gian thực", còn Runway đã ra bản xem trước mô hình thế giới thời gian thực có âm thanh khoảng hai tháng trước. Không bên nào sai; hai công ty kẻ hai đường khác nhau. Các so sánh nhất trong thông báo chỉ nên đọc sau khi tìm ra đường kẻ đó.

Thứ hai, **chỗ thiếu con số thì con số của bản tiền nhiệm là trần.** Nếu Genie 3 là 720p, 24 fps và "vài phút", mà bài Genie 4 không có số, thì không có cơ sở để giả định độ phân giải hay thời lượng tăng rõ rệt. "Hai phút" báo chí đưa cũng không khác mấy "vài phút" của Genie 3. Cách đọc an toàn là tiến bộ thật của lần ra mắt này nằm ở tính năng — **âm thanh, điều khiển, đạo diễn** — chứ không phải ở con số.

Thứ ba, **đoạn "giới hạn" sống lâu hơn đoạn "tính năng"** — cùng kết luận với bài hôm qua (NO.30). Danh sách giới hạn của Genie 3 và Genie 4 gần như giống nhau nghĩa là những vấn đề đó chưa được giải quyết suốt một năm hai tháng, và ở thông báo thế hệ sau bạn có thể tìm đúng những mục ấy trước. Chữ không đọc được, chạy lâu thì vật thể đổi, âm thanh không chính xác — với người thực sự phải giao video, ba điều này quan trọng hơn tính năng.

Thứ tư, diễn giải chúng tôi thêm vào. Nơi mô hình thế giới đang hướng tới lúc này **không phải "video hoàn chỉnh" mà là "sân tập cho robot và tác tử" và "storyboard cho con người".** Google đưa ví dụ robot lên đầu, AMD đưa mô phỏng học robot vào lý do mua lại, và Rivas gọi giai đoạn giá trị nhất là "lên ý tưởng và storyboard". Ý tưởng "luyện tập trong giấc mơ" của bài báo 2018 vẫn nguyên. Một đội làm video nhỏ mà đọc tin này thành "tạo video đã tốt hơn" thì đã tìm nhầm địa chỉ.

## Nếu là chúng tôi — ba việc đội làm video AI influencer làm trong tuần này (thực hành)

1. **Để mô hình thế giới và mô hình tạo video ở hai ô khác nhau.** Video Ria của chúng tôi hiện làm bằng mô hình tạo video (kịch bản → cảnh → dựng). Genie 4 không phải công cụ thay thế ô đó, mà là **"chế độ nháp" để chạy nhiều lượt bằng lời trước khi chốt cảnh.** Đó chính là vị trí mà Google mô tả qua ví dụ "chế độ nháp của nhà làm phim" và "giai đoạn storyboard" của Rivas. Nên trong quy trình sản xuất, chúng tôi chỉ ghi nó làm ứng viên ở ô "lên ý tưởng cảnh", không ghi vào ô "render cuối". Chính Rivas nói việc biến nguyên mẫu thành tài sản hoàn chỉnh "vẫn còn xa".
2. **Đăng ký danh sách chờ, nhưng không đổi quy trình.** Danh sách chờ Project Genie và truy cập sớm Gemini API đăng ký không mất phí. Nhưng vì hiện chỉ "người thử nghiệm tin cậy" được dùng và không có số liệu chính thức, chúng tôi không buộc bất kỳ bước sản xuất nào vào công cụ này trước khi nó đến. Khi có, chúng tôi chạy mười cảnh của mình (Ria giới thiệu cửa hàng, cảnh giải thích bảng thành phần, cảnh so sánh giày bóng rổ, v.v.) theo phương pháp thử của NO.17 và ghi ba mục trước: **chữ có đọc được không, nhân vật có giữ nguyên trong hai phút không, âm thanh có khớp cảnh không.** Ba giới hạn công ty tự viết ra chính là bảng kiểm của chúng tôi.
3. **Khớp hình mờ với phần công bố của chúng tôi.** Mọi đầu ra của Genie 4 đều có hình mờ SynthID. Chính sách video Ria của chúng tôi đã yêu cầu "nêu rõ nhân vật AI", nên cùng hướng. Nhưng hình mờ là dấu để nền tảng đọc, còn phần công bố của chúng tôi là dấu để người đọc, nên không cái nào thay thế cái kia. Chúng tôi viết quy tắc ngay bây giờ: nếu có cảnh làm bằng mô hình thế giới, phụ đề công bố thêm "một phần cảnh là mô phỏng AI". Viết quy tắc trước khi công cụ đến luôn rẻ hơn.

## Những gì chúng tôi không chọn lần này

Hai thông báo ngày 27 tháng 10 của Anthropic (kết quả ban đầu trong phát triển thuốc, mở rộng hợp tác với Cơ quan Dịch vụ Tổng hợp Hoa Kỳ GSA) và tin độc quyền của Axios "FTC yêu cầu lãnh đạo Anthropic ra điều trần" bị loại vì xung đột lợi ích lớn và chưa được kiểm chứng chéo. Ba bài ngày 26 tháng 10 của OpenAI (hợp tác học thuật, trường hợp CodeRabbit, "Thế giới công việc đang mở rộng của ChatGPT") chúng tôi chưa đọc nội dung. Cuộc tấn công chuỗi cung ứng LiteLLM 1.107.0 (21 tháng 10, đã xác nhận trong báo cáo sự cố của công ty) và lỗ hổng thư viện nén Brotli do OpenAI công bố có tính chất khác, sẽ được bàn riêng ở bài tiếp theo với chủ đề "chuỗi cung ứng công cụ AI". Với Amazon–Decart và Rivian–Third Dimension, chúng tôi không tìm được tài liệu chính thức.

## Những điều chưa xác nhận được trong tin này

- Độ phân giải, số khung hình mỗi giây, thời lượng giữ được và độ trễ của Genie 4 không có trong bài chính thức. "Tới hai phút, gấp đôi Genie 3" là tin của TechCrunch (DigitalToday dẫn lại), chúng tôi không xác nhận được trong tài liệu chính thức nào.
- "Mô hình thế giới thời gian thực đầu tiên tạo âm thanh bản địa" là tiêu chí riêng của công ty; khác biệt tiêu chí với Runway GWM Worlds 2 (3 tháng 9) chúng tôi chưa xác nhận được.
- Chúng tôi chưa tự dùng Genie 4. Mọi mô tả tính năng đều từ bài của công ty và tin họp báo; chúng tôi không tìm thấy đo lường của tổ chức độc lập.
- Thời điểm cung cấp Project Genie và Gemini API chỉ ghi "lần lượt" và "trong vài tuần tới" (TechCrunch), nên chưa chốt được ngày.

## Những bài đã đọc cùng

Chúng tôi trực tiếp mở và kiểm tra các nguồn khác tính chất, chia thành tài liệu chính thức của công ty, công bố, bài báo khoa học, tin báo chí và bài trước của chúng tôi.

Tài liệu chính thức của công ty:

- [Genie 4: A new generation of world simulation (Google DeepMind)](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) — tiếng Anh, thông báo chính thức (tính năng, giới hạn, phạm vi cung cấp; không có con số)
- [We're announcing Genie 4, our new world model for real-time interactive simulation (Google)](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-genie-4/) — tiếng Anh, blog chính thức của Google (thứ tự cung cấp)
- [Genie 3: A new frontier for world models (Google DeepMind)](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/) — tiếng Anh, thông báo chính thức của bản tiền nhiệm (720p, 24 fps, "vài phút", trí nhớ một phút)
- [Introducing GWM Worlds 2 (Runway)](https://runway.com/research/introducing-gwm-worlds-2) — tiếng Anh, bài nghiên cứu chính thức của đối thủ (720p, 24 fps, âm thanh 48 kHz, giới hạn)

Công bố:

- [AMD to Acquire World Labs to Advance the Future of AI Compute (AMD Investor Relations)](https://ir.amd.com/news-events/press-releases/detail/1299/amd-to-acquire-world-labs-to-advance-the-future-of-ai-compute) — tiếng Anh, công bố của công ty (khoảng 8,2 tỷ USD toàn cổ phiếu, dự kiến hoàn tất)

Bài báo khoa học:

- [World Models — David Ha, Jürgen Schmidhuber (arXiv, 2018)](https://arxiv.org/abs/1803.10122v1) — tiếng Anh, điểm xuất phát của khái niệm "mô hình thế giới"

Tin báo chí:

- [Google's Genie 4 world model adds audio, more realistic worlds, and real-time steering (TechCrunch)](https://techcrunch.com/2026/10/27/googles-genie-4-world-model-adds-audio-more-realistic-worlds-and-real-time-steering/) — tiếng Anh, báo công nghệ (họp báo, "hai phút", phát biểu của Rivas, bối cảnh thị trường)
- [Google DeepMind Rolls Out Genie 4 World Model in Research Preview (Unite.AI)](https://www.unite.ai/google-deepmind-rolls-out-genie-4-world-model-in-research-preview/) — tiếng Anh, báo AI (đối chiếu bài chính thức, so sánh Genie 3)
- [Google DeepMind unveils Genie 4 world model, targeting robots and film production (DigitalToday bản tiếng Anh)](https://www.digitaltoday.co.kr/en/view/120253/google-deepmind-unveils-genie-4-world-model-targeting-robots-and-film-production) — tiếng Anh, báo Hàn Quốc (dẫn TechCrunch)

Bài trước của chúng tôi:

- [Giá sử dụng giảm một nửa, chi phí tạo ra hàng tỷ đô la mỗi tháng (AP News NO.30)](https://www.apholdings.kr/ko/news/half-price-terra-and-the-s1-compute-bill/) — tiếng Hàn, cách đọc "ranh giới công ty tự viết ra"
- [Việc nào dùng AI nào — công dụng do chính các công ty nêu và phương pháp thử của chúng tôi (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — tiếng Hàn, phương pháp thử mô hình theo từng việc
