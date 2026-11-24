---
no: 17
slug: which-ai-for-which-job
date: 2026-10-03
category: Thực hành
tags: Chọn mô hình · Đề xuất theo công việc · Chi phí · Tự kiểm tra
title: Dùng AI nào cho việc nào — mục đích do chính các công ty nêu và cách thử của chúng tôi
summary: Từ tài liệu, lập trình, giọng nói, hình ảnh đến xử lý khối lượng lớn. Chúng tôi tập hợp các mục đích được đề xuất trong tài liệu chính thức của từng công ty và tổng hợp cách xác định trong 30 phút xem có hợp với công việc của mình không.
---
> Bài viết này được soạn thảo cùng AI (Claude) và biên tập viên đã kiểm duyệt. Vì có đề cập cả Anthropic, công ty tạo ra Claude, nên chúng tôi chỉ dựa vào **tài liệu do từng công ty viết về sản phẩm của họ**, và đây không phải kết quả thử nghiệm độc lập so sánh với nhau. Chúng tôi không nói bên nào tốt hơn.

Khó trả lời bằng một dòng cho câu hỏi "Việc này nên dùng AI nào?". Thay vào đó, **mỗi công ty khuyên dùng cho mục đích gì** thì có ghi trong tài liệu chính thức. Chúng tôi tập hợp theo từng loại công việc.

## Công ty khuyên dùng gì cho từng việc

- **Tài liệu, slide, bảng tính hằng ngày và sửa lỗi có phạm vi rõ ràng:** Anthropic giới thiệu Claude Sonnet 5.5 cho các mục đích này. Đây là phía nhanh hơn và rẻ hơn.
- **Công việc phát triển dài và phức tạp (chuyển mã nguồn lớn, rà soát):** Anthropic khuyên dùng Opus 5.5, còn OpenAI khuyên dùng GPT-6.1 Sol (lập trình, sử dụng máy tính, công việc chuyên môn). Cả hai nơi đều đưa ra điểm số cho mục đích này theo công bố của chính họ.
- **Công việc phát triển kéo dài, tác tử làm việc tự động:** Tài liệu của Google giới thiệu Gemini 3.8 Flash cho mục đích này.
- **Trợ lý giọng nói, tổng hợp giọng nói:** Google giới thiệu Gemini 3.8 Live cho hội thoại giọng nói có độ trễ thấp, và Gemini 3.8 Flash TTS cho tổng hợp giọng nói giàu biểu cảm.
- **Hình ảnh:** Google giới thiệu Nano Banana Pro cho độ phân giải 4K và bố cục phức tạp có chữ, và Nano Banana 2 cho sản xuất hàng loạt nhanh.
- **Việc coi trọng giá nhất và khối lượng lớn:** Tài liệu của Anthropic giới thiệu cách bắt đầu từ mô hình nhỏ cấp Haiku rồi nâng lên nếu chưa đủ, còn Google giới thiệu Gemini 3.1 Flash-Lite.

## Giảm chi phí không chỉ là đổi mô hình

Tài liệu của Anthropic khuyên trước khi đổi mô hình, hãy thử **điều chỉnh trí thông minh, tốc độ và chi phí bằng "thiết lập nỗ lực (effort)"**. Ngoài ra cả hai công ty đều có "bộ nhớ đệm (cache)", giúp giá giảm mạnh khi dùng lặp lại cùng một đầu vào (OpenAI 0,10 USD, Anthropic 0,20 USD, mỗi mức tính cho 1 triệu token). Với việc lần nào cũng gắn cùng một chỉ dẫn thì hiệu quả lớn.

## Cách thử trong 30 phút

Chúng tôi rút gọn trình tự mà tài liệu của Anthropic đề xuất theo cách của mình.

1. Chọn ba việc làm hằng tuần (ví dụ: sắp xếp biên bản họp, soạn nháp thư trả lời khách hàng, chỉnh sửa bảng).
2. Chuẩn bị mỗi việc một tài liệu thật đã bỏ thông tin cá nhân.
3. Đưa cùng một câu lệnh y hệt vào hai công cụ.
4. Ghi lại ba thứ: độ chính xác, số chỗ phải sửa, thời gian mất.
5. Nếu điểm tương đương thì chọn bên rẻ hơn; nếu là việc không được sai một lần nào thì chọn bên điểm cao hơn.

## Cách chúng tôi diễn giải

**Sự thật:** Các công ty phân chia mục đích để hướng dẫn, và điểm số lấy từ đánh giá của chính họ.

**Diễn giải:** Không có "AI tốt nhất", chỉ có "AI rẻ nhất phù hợp với việc của mình". Điểm do công ty công bố chỉ là điểm xuất phát, còn tiêu chuẩn là kết quả kiểm tra bằng tài liệu của mình.

**Nếu là chúng tôi:** Không dồn mọi việc vào một công cụ; việc nhẹ giao mô hình nhỏ, chỉ việc khó mới dùng mô hình lớn. Và cứ ba tháng chạy lại bài thử này một lần, vì mô hình thay đổi rất nhanh.

## Các bài đã đọc cùng

Mọi nội dung đều do chúng tôi trực tiếp mở tài liệu chính thức dưới đây để kiểm tra. Điểm số và mục đích là khẳng định của từng công ty.

- [Choosing a model (Anthropic Docs)](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) — tiếng Anh
- [Claude Sonnet 5.5 (Anthropic)](https://www.anthropic.com/claude-sonnet-5-5) — tiếng Anh
- [Introducing GPT-6.1 Sol (OpenAI)](https://openai.com/index/introducing-gpt-6-1-sol/) — tiếng Anh
- [Gemini models (Google AI for Developers)](https://ai.google.dev/gemini-api/docs/models) — tiếng Anh
