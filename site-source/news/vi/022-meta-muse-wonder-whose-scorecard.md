---
no: 22
slug: meta-muse-wonder-whose-scorecard
date: 2026-10-15
category: Góc nhìn
tags: Meta · Muse Wonder · Đánh giá mô hình · Đánh giá độc lập · Cài đặt huấn luyện
title: Mô hình hàng đầu đầu tiên của Meta, Muse Wonder — ai chấm điểm, và ba điều cần xem trước khi dùng
summary: Meta ra mắt mô hình tầm frontier đầu tiên vào ngày 12 tháng 10. Chúng tôi đặt điểm do chính công ty công bố cạnh điểm của một đơn vị đánh giá độc lập, rồi xem giá, cách truy cập và cài đặt huấn luyện — ba điều cần kiểm tra trước khi dùng cho công việc của mình.
---
> Bài này được soạn với AI (Claude) và có biên tập viên kiểm duyệt. Anthropic, nơi tạo ra các mô hình Claude xuất hiện ở đây như đối tượng so sánh, cũng là nơi tạo ra công cụ chúng tôi dùng để viết bài, nên chúng tôi có lợi ích liên quan. Số liệu do công ty công bố được ghi rõ là "công ty công bố", đánh giá độc lập được đánh dấu riêng. Đây không phải ý kiến đầu tư về bất kỳ công ty hay cổ phiếu nào.

Thứ Hai 12 tháng 10, Superintelligence Labs của Meta công bố hai mô hình Muse Wonder và Muse Wonder Full — những mô hình Meta gọi là mô hình tầm frontier đầu tiên của mình. Điều đáng chú ý ở tin này không phải bản thân điểm số, mà là ai đo và đo trong điều kiện nào.

## Đã ra mắt những gì (sự thật)

- Muse Wonder dùng được qua API mô hình của Meta và Muse Code, công cụ lập trình của Meta. Giá API là 4 đô la cho mỗi triệu token đầu vào và 20 đô la cho mỗi triệu token đầu ra (đầu vào có bộ nhớ đệm là 0,20 đô la, theo đơn vị đánh giá độc lập Artificial Analysis).
- Muse Wonder Full chỉ dành cho người đăng ký Muse Code. Mô hình này không được cung cấp qua API (TechCrunch). Theo trang gói đăng ký Muse Code của Meta, Full nằm trong hai gói cao nhất trong bốn gói (Power và Maximum), và LetsDataScience cùng DataNorth cho biết hai gói này có giá 50 và 200 đô la mỗi tháng.
- Cả hai mô hình có cửa sổ ngữ cảnh 1 triệu token, nhận đầu vào là văn bản, hình ảnh, video và âm thanh, đầu ra là văn bản (Artificial Analysis).
- Chúng tôi chưa xác nhận được trọng số của hai mô hình có tải về được hay không (chỉ LetsDataScience nói là không). Decrypt chỉ ra rằng Meta trên thực tế đã dừng dòng Llama, dòng mô hình từng công bố trọng số.

## Đọc bảng điểm

**Công ty công bố.** Trên chỉ số riêng "Personal Superintelligence Index", Meta cho biết Wonder Full đạt 59,1 điểm, cao hơn Opus 5.5 (55,2) và GPT-6 Astra (54,5), và cũng dẫn đầu ở bài kiểm tra trí nhớ MemoryBench với khoảng 85,5 điểm (lời Meta qua Decrypt; iThome và Latent Space đưa cùng số liệu). Decrypt lưu ý cả hai thước đo đều do Meta tự tạo và công thức của chỉ số chưa được công bố.

**Đánh giá độc lập.** Trên chỉ số tổng hợp của Artificial Analysis (v4.3, mức nỗ lực tối đa), Wonder Full đạt 56 điểm, Wonder đạt 52 điểm, còn mô hình trước của Meta là Muse Spark 1.3 đạt 48 điểm. Trên cùng chỉ số, Opus 5.5 đạt 58, Sonnet 5.5 đạt 56 và GPT-6 Astra đạt 53 (kiểm tra trực tiếp trên bảng xếp hạng của Artificial Analysis, mỗi mô hình ở mức cài đặt cao nhất). Tức là theo thước đo độc lập, mô hình nằm quanh vị trí thứ ba — khác với chữ "dẫn đầu" trong chỉ số của công ty.

**Xem kỹ hơn.** Trong cùng bài, Artificial Analysis viết rằng trên chỉ số tác tử lập trình, Wonder Full đạt 68 điểm, ngang Claude Code chạy Sonnet 5.5 và cao hơn Opus 5.5 (66). Ngược lại, ở bài kiểm tra kiến thức AA-Omniscience, Full đạt 30 và Wonder đạt 25, thấp hơn nhiều so với Opus 5.5 (46) và GPT-6 Astra (43). Tỷ lệ bịa thông tin (ảo giác) thuộc mức thấp — 23% với Full và 27% với Wonder — nhưng trong các mô hình đạt từ 45 điểm trở lên trên chỉ số, mức thấp nhất là Gemini 4 Argon với 15%.

## Ba điều cần xem trước khi dùng (diễn giải)

**1. Chi phí cho mỗi việc hoàn thành.** Cùng giá token vẫn có thể cho chi phí mỗi việc khác nhau. Chi phí Artificial Analysis chạy cùng một bộ tác vụ là 4,52 đô la với Wonder, 5,98 đô la với Opus 5.5, 5,46 đô la với Sonnet 5.5, 3,26 đô la với GPT-6 Astra, 1,99 đô la với Gemini 4 Argon và 0,72 đô la với GPT-6.1 Sol. Đơn vị này nhận định Wonder đắt hơn đa số mô hình có mức thông minh tương tự. Có tin nói giá ngang Opus 5.5 (Decrypt), nhưng con số chúng tôi nhìn là chi phí mỗi việc, không phải đơn giá.

**2. Dùng ở đâu được.** Mô hình điểm cao nhất, Wonder Full, chỉ chạy trong gói đăng ký, nên không gắn vào tự động hóa của chúng tôi qua API được. Thứ truy cập được bằng API là Wonder, thấp hơn một bậc về điểm.

**3. Mã và bài viết của mình đi đâu.** Theo trang gói đăng ký Muse Code của Meta, gói đăng ký mặc định ở "chế độ Contributor": Meta có thể dùng lời nhắc, mã, tệp, ngữ cảnh và câu trả lời bạn nhận được để huấn luyện các mô hình sau này, đổi lại bạn được dùng nhiều hơn. Trang này ghi rằng khi tắt, nội dung về sau sẽ không dùng để huấn luyện, nhưng không nói nội dung đã gửi sẽ ra sao, nên chúng tôi chưa xác nhận được điểm này. Chế độ Contributor không có với Wonder qua API, và nội dung ở chế độ tiêu chuẩn được cho là không dùng để huấn luyện. Chúng tôi chưa tự mở được điều khoản sử dụng của Meta, nên hãy kiểm tra điều khoản và màn hình cài đặt trước khi dùng.

## Những điều chúng tôi chưa xác nhận được

Chúng tôi không mở trực tiếp được thông báo chính thức và model card của Meta. Các mục "công ty công bố" ở trên được xác nhận qua bài của TechCrunch, Decrypt, iThome và các nguồn khác. Phần gói đăng ký và cài đặt huấn luyện được chúng tôi kiểm tra bằng cách mở trực tiếp trang gói đăng ký Muse Code của Meta. Decrypt cho biết báo cáo an toàn đầy đủ mà Meta hứa vẫn chưa được công bố. Simon Willison, một người dùng thực tế, viết rằng Wonder có sáu mức suy luận (từ minimal đến max) và hình vẽ dường như tốt hơn mô hình trước, nhưng chính anh nói đây là thử nghiệm không chính thức dựa trên một loại hình vẽ. Không nên đọc đó như một điểm số.

## Góc nhìn của chúng tôi

**Sự thật:** Meta ra mắt một mô hình hàng đầu chỉ dùng được qua API và gói đăng ký; chỉ số của công ty và chỉ số độc lập cho bức tranh khác nhau; mô hình cao nhất chỉ có trong gói đăng ký; và cài đặt mặc định của gói đăng ký dùng nội dung của bạn để huấn luyện.

**Diễn giải:** Mỗi khi có mô hình mới, "nó đứng nhất" và "nó đứng thứ ba" xuất hiện cùng lúc. Cả hai có thể đều đúng, vì bài kiểm tra khác nhau về người tạo ra và về cài đặt khi chạy.

**Nếu là chúng tôi:** Chúng tôi không đổi mô hình chỉ vì một con số. Chúng tôi chạy 20 việc thật của mình (nháp kịch bản, mô tả sản phẩm, phân loại bình luận) trong cùng điều kiện, ghi lại "chi phí mỗi việc" và "số lần sửa", và chỉ đăng sau khi có người kiểm tra. Thông tin khách hàng và tài liệu chưa công bố không đưa vào bất kỳ cài đặt nào có thể dùng để huấn luyện.

## Đọc cùng

Chúng tôi đã trực tiếp mở các nguồn thuộc nhiều loại khác nhau. Số liệu theo đúng từng nguồn.

- [Meta releases its first frontier model, Muse Wonder (TechCrunch)](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder) — tiếng Anh, bài báo
- [Muse Wonder / Wonder Full evaluation (Artificial Analysis)](https://artificialanalysis.ai/articles/muse-wonder) — tiếng Anh, đơn vị đánh giá độc lập
- [Meta Muse Wonder and the frontier AI race (Decrypt)](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race) — tiếng Anh, bài báo (chỉ số công ty so với chỉ số độc lập)
- [Meta's best model skips API, coding plan trains on your code (LetsDataScience)](https://letsdatascience.com/blog/metas-best-model-skips-api-coding-plan-trains-on-your-code) — tiếng Anh, gói đăng ký và cài đặt huấn luyện
- [llm-meta-ai 0.2 (Simon Willison)](https://simonwillison.net/2026/Oct/12/llm-meta-ai/) — tiếng Anh, blog của người dùng thực tế
- [Meta releases Muse Wonder, its first frontier-class AI model (AI Weekly)](https://aiweekly.co/alerts/meta-releases-muse-wonder-its-first-frontier-class-ai-model) — tiếng Anh, bản tin (tóm tắt từ các nguồn khác)
- [Muse Code Subscriptions (Meta)](https://dev.meta.ai/docs/muse-code/subscriptions) — tiếng Anh, trang chính thức của Meta
- [Models Leaderboard (Artificial Analysis)](https://artificialanalysis.ai/leaderboards/models) — tiếng Anh, bảng xếp hạng của đơn vị đánh giá độc lập
- [Meta's Muse Wonder (DataNorth)](https://datanorth.ai/news/metas-muse-wonder) — tiếng Anh, phân tích (gói đăng ký và cài đặt huấn luyện)
- [Bài về Muse Wonder (iThome)](https://www.ithome.com.tw/news/179608) — tiếng Trung phồn thể, bài báo
