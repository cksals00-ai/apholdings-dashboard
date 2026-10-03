---
no: 7
slug: where-time-and-money-leak
date: 2026-10-03
category: Thực hành
tags: Bộ nhớ · Chi phí · Hiệu suất công việc
title: Ba chỗ thất thoát thời gian và tiền bạc khi làm việc với AI
summary: Lặp lại cùng một lời giải thích, ngồi chờ cho xong việc, và trả tiền cho dữ liệu chẳng ai đọc. Ba chỗ rò rỉ và cách chặn lại.
---
> Bài viết này được soạn thảo cùng AI và biên tập viên đã kiểm duyệt. Chúng tôi có tham khảo các bài viết bên ngoài, và những bài đã tham khảo được nêu ở cuối bài.

Công cụ AI thường thất thoát thời gian và tiền bạc không phải vì chậm mà vì **cách dùng**. Đây là ba chỗ chúng tôi kiểm tra.

## 1. Lặp lại cùng một lời giải thích

Nếu mỗi lần mở cuộc trò chuyện mới bạn lại viết lại phần giới thiệu dự án từ đầu, đó là chỗ rò rỉ thứ nhất. Cách xử lý đơn giản. Hãy ghi mục đích dự án, các điều cấm và thuật ngữ vào **một trang tài liệu hướng dẫn** luôn được đọc trước tiên. Tài liệu này phải ngắn. Như bài trước đã nói, nếu dài ra thì ngược lại sẽ bị mờ đi. Chúng tôi làm việc này bằng kho tài liệu dự án và tài liệu hướng dẫn, và cố không để vượt quá một trang.

## 2. Thời gian chờ đợi

Nếu bạn giao việc mất nhiều thời gian như build, triển khai, chuyển đổi hàng loạt rồi ngồi nhìn màn hình, đó là chỗ rò rỉ thứ hai. Với việc chạy lâu, nguyên tắc cơ bản là **chạy nền và trong lúc đó giao việc khác**. Làm tuần tự thì mất tổng thời gian cộng lại, làm đồng thời thì chỉ mất bằng việc dài nhất. Với những việc có kết quả đổ ra dài như điều tra, hãy giao cho một người làm riêng và **chỉ nhận về bản tóm tắt**, màn hình làm việc của mình sẽ không bị rối.

## 3. Chi phí cho dữ liệu chẳng ai đọc

Bài viết chúng tôi tham khảo chỉ ra rằng nếu đưa nguyên cả tệp log hay bản dump dung lượng lớn vào tác tử lập trình, phần lớn là nội dung lặp và khoảng trắng mà mô hình không cần, chỉ tốn tiền. Công cụ mà bài đó giới thiệu thực sự giảm được bao nhiêu thì chúng tôi chưa kiểm chứng, nên không hứa hẹn hiệu quả. Tuy nhiên nguyên tắc thì áp dụng được cả khi không có công cụ. **Với văn bản dài do máy sinh ra, con người nên cắt lấy phần cần thiết trước rồi mới đưa vào.** Với log lỗi, hai mươi dòng trước và sau chỗ xảy ra lỗi thường là đủ.

## Bảng kiểm tra

- Tuần này đã lặp lại cùng một lời giải thích bao nhiêu lần
- Đã có lúc nào phải dừng lại chờ một việc mất nhiều thời gian chưa
- Đã có lúc nào đưa nguyên cả log hay bảng dài vào chưa

Chỉ cần một câu trả lời là "có" thì hãy sửa từ dòng đó trước.

## Các bài đã đọc cùng

Bài viết này tham khảo vấn đề được nêu trong các bài dưới đây, rồi viết lại theo góc nhìn và tiêu chí của đội chúng tôi. Chúng tôi không theo câu chữ hay bố cục của chúng, và những số liệu mà bài gốc dẫn nhưng chúng tôi chưa tự kiểm tra được đến dữ liệu gốc thì đều đã đánh dấu như vậy. Một số bài gốc chỉ mở toàn văn sau khi đăng nhập, nên chúng tôi đọc theo phần được công khai.

- [Ba cách xóa thời gian chờ của Claude, chỉ cần copy-paste là xong (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-wait)
- [Chi phí tác tử lập trình, bạn đang mở mắt mà vẫn bị hớ (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-headroom)

Các nguồn khác chúng tôi đối chiếu:

- [Prompt caching (Claude Platform Docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — tiếng Anh
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — tiếng Anh
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — tiếng Anh
