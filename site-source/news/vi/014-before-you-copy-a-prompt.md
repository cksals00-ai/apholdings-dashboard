---
no: 14
slug: before-you-copy-a-prompt
date: 2026-10-03
category: Thực hành
tags: Prompt · Điền chỗ trống · Kiểm tra nguồn
title: Trước khi dùng prompt người khác đưa — kiểm tra nguồn và sáu dòng cần điền
summary: Vì sao dán nguyên prompt người khác đăng lại không hiệu quả. Cách chọn tài liệu chính thức và sáu dòng chuẩn bị dùng được cho mọi prompt.
---
> Bài viết này được soạn thảo cùng AI và biên tập viên đã kiểm duyệt. Chúng tôi có tham khảo các bài viết bên ngoài, và những bài đã tham khảo được nêu ở cuối bài.

Nhận prompt từ bình luận trên mạng xã hội rồi dùng là chuyện phổ biến. Bản thân việc dùng lại là thói quen tốt, nhưng có nhiều trường hợp **dán nguyên xi thì không được**. Đây là tiêu chí của chúng tôi.

## Xem nguồn trước

Nếu có thể, hãy xem tài liệu chính thức của công ty làm ra công cụ trước. Bài viết chúng tôi tham khảo cho biết tác giả đã mở thư viện prompt chính thức do Anthropic công bố và chia thành loại dùng được ngay trong khung chat, loại phải dán thêm tài liệu, và loại cần công cụ phát triển. Ý tưởng phân loại này hữu ích. Phải lọc xem **đây có phải prompt chạy được trong môi trường của mình không** trước thì mới tiết kiệm thời gian.

## Tiền đề biến mất trong lúc dịch và truyền đi

Khi dịch prompt nước ngoài sang tiếng Hàn, đôi khi tiền đề "công cụ này đã biết tôi rồi" bị mất. AI trong khung chat mới không biết tôi. Khi đó AI sẽ hỏi lại hoặc kể lể những điều chung chung tầm thường. Bài viết chúng tôi tham khảo kể rằng họ phát hiện vấn đề này khi tự chạy thử. Chúng tôi cũng có thể gặp vấn đề tương tự, nên **trước khi viết prompt, hãy điền trước những gì AI không biết.**

## Sáu dòng chuẩn bị dùng được cho mọi prompt

Nếu là prompt về ý tưởng kinh doanh, hãy điền trước sáu dòng dưới đây.

1. Việc đã từng làm thật và được trả tiền (công việc cụ thể chứ không phải chức danh)
2. Điều mọi người hay hỏi tôi
3. Số giờ có thể dành mỗi tuần
4. Số tiền có thể dùng hiện nay
5. Những người đã liên lạc được
6. Số tiền mục tiêu và thời hạn

## Nói rõ "chỉ giữ lại một"

Hỏi AI một cách rộng thì nó liệt kê rộng. Vì liệt kê thì an toàn còn lựa chọn thì kéo theo trách nhiệm. Vì vậy ở cuối mỗi bước, hãy yêu cầu **"chỉ giữ lại một, kèm lý do trong một câu"**. Ứng viên phải giảm từ năm xuống một thì mới sang được bước tiếp theo.

## Kiểm tra cuối cùng

Không đưa thông tin cá nhân của mình vào prompt nhận được, và số liệu cùng sự thật trong kết quả thì kiểm tra nguồn riêng.

## Các bài đã đọc cùng

Bài viết này tham khảo vấn đề được nêu trong các bài dưới đây, rồi viết lại theo góc nhìn và tiêu chí của đội chúng tôi. Chúng tôi không theo câu chữ hay bố cục của chúng, và những số liệu mà bài gốc dẫn nhưng chúng tôi chưa tự kiểm tra được đến dữ liệu gốc thì đều đã đánh dấu như vậy. Một số bài gốc chỉ mở toàn văn sau khi đăng nhập, nên chúng tôi đọc theo phần được công khai.

- [52 prompt chính thức của công ty làm ra Claude, đã mở hết và phân loại (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-prompt-library)
- [Nếu bạn nói "giúp tôi kiếm tiền", Claude sẽ hỏi lại (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-money-chain)

Các nguồn khác chúng tôi đối chiếu:

- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — tiếng Anh
- [Prompt injection (Wikipedia)](https://en.wikipedia.org/wiki/Prompt_injection) — tiếng Anh
- [Prompt engineering overview (Anthropic Docs)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — tiếng Anh
