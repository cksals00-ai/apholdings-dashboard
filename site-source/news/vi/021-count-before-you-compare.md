---
no: 21
slug: count-before-you-compare
date: 2026-10-09
category: Góc nhìn
tags: Đọc con số · Hạch toán doanh thu · Giá token · Chi phí mỗi việc
title: Xem cách đếm trước khi so sánh — vì sao 70 tỷ USD thành 50 tỷ USD, và cái bẫy trong giá token
summary: Cùng một "doanh thu quy năm" hay "giá mỗi token" có thể mang nghĩa khác nhau tùy cái gì được đếm. Hai bài báo tuần này cho thấy cách đọc con số.
---
> Bài này được soạn cùng AI (Claude) và có biên tập viên kiểm duyệt. Cả Anthropic và OpenAI đều xuất hiện, và Anthropic là công ty tạo ra Claude nên chúng tôi có lợi ích liên quan. Đây không phải ý kiến đầu tư về bất kỳ công ty hay cổ phiếu nào; mọi con số được lấy từ bài báo và thông báo của công ty.

Câu chuyện con số gây chú ý nhất của ngành AI tuần này không phải về hiệu năng mà về cách đếm.

## Trường hợp 1. Vì sao doanh thu của cùng một công ty từ 70 tỷ thành 50 tỷ USD

Ngày 8/10, Axios đưa tin doanh thu quy năm của OpenAI là 50 tỷ USD, không phải 70 tỷ USD như được đưa rộng rãi tháng trước. Con số 70 tỷ USD đến từ tài liệu chia sẻ với nhà đầu tư, được "nâng lên" (gross up) để so sánh trực tiếp hơn với Anthropic. Khác biệt nằm ở cách ghi nhận doanh số bán qua đối tác đám mây. Theo một giáo sư kế toán được Axios trích dẫn, khi khách hàng trả 100 qua nhà cung cấp đám mây, Anthropic có thể ghi toàn bộ 100 là doanh thu và ghi phần của nhà cung cấp là chi phí, còn OpenAI chỉ ghi phần của mình ở một số giao dịch đối tác. Cả hai được cho là đều phù hợp chuẩn kế toán GAAP.

Reuters cũng đưa tin ngày 9/10 rằng OpenAI cho nhà đầu tư biết doanh thu quy năm tháng 9 chỉ dưới 50 tỷ USD một chút. Khoảng chênh so với tín hiệu trước đó là gần 70 tỷ USD xuất phát từ việc muốn so sánh trực tiếp với Anthropic; khác với Anthropic, OpenAI không tính doanh thu bán qua các đối tác đám mây như AWS và Google Cloud (Financial Times đưa tin đầu tiên).

Doanh thu quy năm là cách kéo doanh số của một kỳ ra thành một năm, một chỉ số kiểu Thung lũng Silicon, và Axios nói thêm rằng nhà đầu tư thị trường công khai thường thích doanh thu thực tế hơn (theo Axios và Reuters; chúng tôi chưa xem tài liệu kế toán của cả hai công ty).

## Trường hợp 2. Giá mỗi token giảm nhưng giá mỗi việc có thể không giảm

Anthropic công bố Haiku 5.5 rẻ hơn Haiku 4.5 trung bình khoảng 75% (số liệu của công ty). Nhưng Next.ink, dẫn một đơn vị phân tích bên ngoài, cho biết mô hình này trả lời dài hơn nên mức tiết kiệm phụ thuộc vào cài đặt effort, và lưu ý yêu cầu trên 100.000 token có giá mỗi token cao gấp năm lần. Bản tin AI Weekly cũng đưa tin về các công ty chuyển sang mô hình rẻ hơn vì áp lực chi phí và khuyên đo "chi phí cho mỗi tác vụ hoàn thành" (số báo này tóm tắt bài của các báo khác, chúng tôi chưa kiểm tra bài gốc).

## Ba câu hỏi khi đọc một con số

1. **Đã đếm cái gì?** Tổng hay ròng; token, hay một việc đã hoàn thành.
2. **Ai đưa ra con số?** Chính công ty hay bên độc lập; nếu khác nhau thì điều kiện đo là gì.
3. **Đổi điều kiện thì sao?** Điểm ở mức effort cao nhất có thể khác ở mức mặc định, và yêu cầu dài có thể có đơn giá khác.

## Góc nhìn của chúng tôi

**Sự thật:** Doanh thu quy năm của cùng một công ty được đưa tin là 70 tỷ rồi 50 tỷ USD tùy cách đếm, và tuần này có ý kiến chỉ ra rằng giá token giảm và chi phí mỗi việc giảm không nhất thiết đi cùng nhau.

**Diễn giải:** Chỉ khi đơn vị và cách đếm giống nhau thì con số mới so sánh được. Điều này đúng khi so sánh các công ty và cũng đúng khi đọc con số của chính mình.

**Nếu là chúng tôi:** Trong báo cáo doanh thu của mình, tách tổng và ròng, và ghi công việc AI theo chi phí mỗi "bài viết, video hay đơn hàng" thay vì theo token. Khi trích số liệu của công ty khác, luôn ghi kèm nguồn và cách đếm.

## Tài liệu đọc kèm

Chúng tôi đã trực tiếp mở năm nguồn có tính chất khác nhau.

- [OpenAI annualized revenue $20 billion less than previously reported (Axios)](https://www.axios.com/2026/10/08/openai-50-billion-arr-anthropic-revenue-accounting) — tiếng Anh, bài báo
- [OpenAI's September annualized revenue nears $50 bln, less than previously indicated (Reuters, đăng trên Zawya)](https://www.zawya.com/en/special-coverage/openais-september-annualized-revenue-nears-50bln-less-than-previously-indicated-source-says-1586243) — tiếng Anh, tin hãng thông tấn
- [Introducing Claude Haiku 5.5 (Anthropic)](https://www.anthropic.com/claude-haiku-5-5) — tiếng Anh, thông báo chính thức của công ty
- [Chez Anthropic, Haiku 5.5 prend la relève des petits modèles rapides (Next.ink)](https://next.ink/260659/chez-anthropic-haiku-5-5-prend-la-releve-des-petits-modeles-rapides/) — tiếng Pháp, phân tích của báo
- [AI got too expensive, so companies are moving to cheaper models (AI Weekly #535)](https://aiweekly.co/issues/ai-got-too-expensive-so-companies-are-moving-to-cheaper) — tiếng Anh, bản tin
