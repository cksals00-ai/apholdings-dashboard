---
no: 24
slug: inspectors-inside-the-building
date: 2026-10-19
category: Góc nhìn
tags: Anthropic · METR · đánh giá bên ngoài · kiểm chứng độc lập · quyền công bố
title: Kiểm toán viên đã bước vào bên trong tòa nhà — việc Anthropic mở 「quyền truy cập ngang nhân viên」 cho METR, và cách đọc phạm vi của 「không có quyền phủ quyết」
summary: Ngày 15 tháng 10, Anthropic cho biết đã mở quyền truy cập vào thiết bị và công cụ nội bộ cho 6 nhân viên của tổ chức đánh giá bên ngoài METR. Chúng tôi tách riêng điều gì là mới, câu 「không có quyền phủ quyết」 đi kèm những điều kiện nào, và điều gì vẫn chưa được xác nhận.
---
> Bài viết này được soạn cùng AI (Claude) và có biên tập viên kiểm duyệt. Anthropic, nhân vật chính của bài, là công ty tạo ra Claude, công cụ chúng tôi dùng để viết bài, nên chúng tôi có lợi ích liên quan. Những gì Anthropic tự công bố được ghi là 「điều công ty đã công bố」, còn diễn giải của bên thứ ba được đánh dấu riêng. Đây không phải ý kiến đầu tư vào bất kỳ doanh nghiệp cụ thể nào.

Ngày 15 tháng 10, Anthropic đăng lên blog chính thức một bản cập nhật về 「các bên đánh giá độc lập (independent evaluators)」 (bài được ghi là đã sửa một phần chú thích vào ngày 16 tháng 10 sau khi đăng). Điểm cốt lõi là một cơ chế đã bắt đầu, trong đó 6 nhân viên của tổ chức đánh giá bên ngoài METR dùng thiết bị và công cụ nội bộ của Anthropic để kiểm tra rủi ro. Bài này tách riêng điều gì được xác nhận từ thông báo đó và điều gì còn tùy cách đọc.

## Điều Anthropic đã công bố (điều công ty đã công bố)

- **METR:** 6 nhân viên của METR, một tổ chức đánh giá phi lợi nhuận, được tiếp nhận như nhân viên mới nhập công ty, dùng thiết bị và không gian văn phòng của công ty, và được truy cập các công cụ, hệ thống nội bộ ở mức tương tự nhóm đánh giá rủi ro nội bộ của Anthropic. Các nhân viên này được khuyến khích chia sẻ mọi thứ với họ, trừ dữ liệu khách hàng, thông tin được bảo mật giữa luật sư và thân chủ, và thông tin về kiến trúc mô hình (architecture).
- **Điều kiện công bố:** METR công bố phân tích riêng của mình về mức độ rủi ro, sự cố và thực tiễn của Anthropic. Anthropic viết rằng 「không thể ngăn việc công bố」, nhưng có thể yêu cầu xóa thông tin thuộc ba nhóm nêu trên. Thông tin nào thuộc các nhóm đó do Anthropic quyết định, còn METR có quyền nêu ý kiến về mức độ truy cập mà mình nhận được.
- **Vận hành tách biệt:** Sự hợp tác này nằm trong một nhóm nhỏ, theo hợp đồng có tính ràng buộc, và những nhân viên khác của METR làm dự án khác với Anthropic được tách khỏi công việc của nhóm này. Được biết METR đã nhiều lần xem xét các báo cáo rủi ro của Anthropic trong một năm qua.
- **Khung ba bậc:** Bậc đầu tiên là kiểm tra phạm vi hẹp, trong đó phạm vi truy cập do Anthropic quyết định và việc công bố của bên đánh giá cần Anthropic phê duyệt. Bậc hai cho phép công bố mà không cần phê duyệt và được xem nhiều thông tin hơn, nhưng vẫn có thể bị yêu cầu xóa một số nhóm thông tin nhất định, và bên đánh giá có thể công khai ý kiến về việc yêu cầu xóa đó có chính đáng hay không. Bậc ba là cách làm của METR, kết hợp quyền truy cập ngang nhân viên với quyền công bố tương tự bậc hai. Anthropic cho biết về lâu dài muốn đặt nhiều bên đánh giá ở bậc ba.
- **Những nơi khác:** SecureBio đang xem xét chương về vũ khí hóa học và sinh học trong báo cáo rủi ro tháng 8, với thông tin và quyền công bố hạn chế hơn METR. Với Accenture và Faculty, Anthropic thúc đẩy hợp tác rộng hơn, bao gồm đánh giá mô hình, red team và đánh giá mức độ căn chỉnh (alignment), còn với một số tổ chức khác gồm Hugging Face thì chỉ ghi là đang trong 「thảo luận ban đầu」. Phạm vi trao đổi hay mức độ truy cập của Hugging Face không có trong bài đó.

## 「Không có quyền phủ quyết」 đến đâu (diễn giải)

**1. Quyền phủ quyết và quyền biên tập là hai việc khác nhau.** Không thể ngăn việc công bố là một chuyện, còn Anthropic có thể buộc xóa thông tin thuộc các nhóm do họ định ra là chuyện khác. Ba nhóm thì tương đối rõ ràng, nhưng cái gì nằm trong đó do Anthropic phán đoán. Tuy vậy, có một cơ chế là METR có thể nói công khai về mức độ truy cập.

**2. Không phải mọi bên đánh giá đều có cùng điều kiện.** Theo Benzinga và CellCog, SecureBio đang ở bậc đầu tiên, và bậc đầu tiên cần Anthropic phê duyệt khi công bố. Câu 「bên đánh giá muốn công bố thế nào cũng được」 chỉ đúng với bậc ba (và bậc hai).

**3. Chưa có kết quả.** Crypto Briefing chỉ ra rằng tại thời điểm công bố vẫn chưa có kết quả đánh giá nào của METR từ quyền truy cập này. Phải đợi báo cáo đầu tiên ra đời và xem phần bị xóa nhiều hay ít thì mới biết cơ chế này thực chất đến đâu.

**4. Chúng tôi không xác nhận được về tiền và thời hạn.** CellCog chỉ ra rằng bài của Anthropic nêu độc lập về tài chính với công ty được đánh giá là một yêu cầu, nhưng không viết ai trả chi phí cho nhóm METR được cử đến. Việc sự hợp tác này có vĩnh viễn không, có áp dụng cho các lần ra mắt mô hình sắp tới không, bên đánh giá có quyền trì hoãn việc ra mắt không, chúng tôi không tìm thấy trong bài chính thức (Tech-Insider cũng chỉ ra điểm tương tự).

## Bối cảnh: dòng chảy trong cùng tuần

Benzinga đưa tin rằng trong cùng tuần, FTC của Mỹ đã gửi yêu cầu điều tra dân sự đến OpenAI và Anthropic, và tổng hợp rằng tháng trước Anthropic đã cam kết tăng cường đánh giá bên ngoài và ký 「thỏa thuận của Nhà Trắng về siêu trí tuệ」. Tech-Insider diễn giải cơ chế này gắn với những áp lực đó, nhưng sự liên hệ ấy và dự báo 「các công ty khác sẽ làm theo」 là suy đoán của trang tin này chứ không phải sự thật đã được đưa tin. Vụ FTC được đề cập trong bài trước (NO.23) nằm cùng dòng chảy này, nhưng Anthropic không nói rằng thông báo lần này là vì chuyện đó.

## Những điều chúng tôi không xác nhận được trong tin này

- Chúng tôi không tìm thấy lời giải thích của chính METR. Danh sách blog của METR chỉ có đến bài ngày 6 tháng 10 (「AI systems could cover up misbehavior」), và không thấy bài nào giải thích sự hợp tác lần này. Vì vậy chúng tôi chỉ biết lập trường của METR qua bài của Anthropic.
- Các con số và điều kiện nêu trên đều đến từ thông báo của chính Anthropic và chưa được kiểm chứng độc lập. Phần lớn các bài đưa tin chỉ lặp lại thông báo này. Crypto Briefing ghi việc phân bậc đánh giá khác với bài chính thức (ghi Faculty ở bậc hai), nhưng không có chỗ nào trong bài chính thức có sự phân bậc như vậy, nên chúng tôi viết theo bài chính thức.
- Nghiên cứu của Stanford HAI mà lần kiểm tra trước chúng tôi từng cân nhắc, lần kiểm tra này cũng không tìm thấy nghiên cứu mới nào liên quan trực tiếp đến vụ này. Bài của HAI xuất hiện trong kết quả tìm kiếm là một đề xuất kiểm toán của bên thứ ba từ năm 2021 nên chúng tôi không đưa vào bài.

## Suy nghĩ của chúng tôi

**Sự thật:** Anthropic đã mở quyền truy cập ngang nhân viên cho 6 nhân viên METR, và cho biết không ngăn việc công bố nhưng có thể yêu cầu xóa các nhóm thông tin nhất định. Điều kiện khác nhau tùy từng bên đánh giá.

**Diễn giải:** Câu 「bên ngoài đang xem xét」 kéo theo những câu hỏi: ai định phạm vi truy cập, ai phê duyệt việc công bố, ai trả chi phí. Thông báo lần này đã trả lời một phần trong số đó, còn một phần vẫn để trống cho đến khi có báo cáo đầu tiên.

**Nếu là chúng tôi:** Chúng tôi cũng đọc những lời 「an toàn」 「đã được kiểm chứng」 của các công cụ AI mình dùng bằng chính những câu hỏi này. Ghi lại ai đã đo, có phải ca do công ty tự chọn không, điều kiện là gì, và với công việc của mình thì chạy thêm một lần theo tiêu chuẩn của mình. Bản tin này cũng vậy: phần có lợi ích liên quan thì nói rõ ngay đầu bài, còn điều chưa trực tiếp mở ra xác nhận được thì ghi là chưa xác nhận được.

## Các bài đã đọc cùng

Chúng tôi đã trực tiếp mở và xác nhận những nguồn có tính chất khác nhau. Các con số và điều kiện là theo từng nguồn.

Tài liệu chính thức của công ty:

- [An update on independent evaluators (Anthropic)](https://www.anthropic.com/news/an-update-on-independent-evaluators) — tiếng Anh, thông báo chính thức của công ty

Tin bài và phân tích:

- [Anthropic Gives AI Watchdog Unprecedented Internal Access (Benzinga)](https://www.benzinga.com/markets/private-markets/26/10/62397762/anthropic-lets-outside-ai-evaluators-inside-its-systems-and-publish-findings-it-cant-block) — tiếng Anh, báo/trang tin (có ghi chú đã dùng một phần công cụ AI)
- [Anthropic gives outside AI safety evaluators METR and SecureBio inside access (Crypto Briefing)](https://cryptobriefing.com/anthropic-metr-securebio-ai-safety-evaluation/) — tiếng Anh, báo/trang tin (phân bậc khác với bài chính thức)
- [Anthropic Gives METR Employee-Like Access: What It Means (CellCog)](https://cellcog.ai/blog/anthropic-metr-embedded-evaluators/) — tiếng Anh, blog doanh nghiệp (có quảng bá dịch vụ AI của chính họ)
- [Anthropic Gives METR 6 Staff AI System Access (Tech-Insider)](https://tech-insider.org/au/anthropic-metr-outside-evaluators-access-2026/) — tiếng Anh, báo/trang tin (dự báo là suy đoán của tác giả)
