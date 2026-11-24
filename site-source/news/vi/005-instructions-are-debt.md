---
no: 5
slug: instructions-are-debt
date: 2026-10-03
category: Góc nhìn
tags: Chỉ dẫn · Prompt · Dọn dẹp
title: Chỉ dẫn cho AI không phải tài sản mà là khoản nợ — vì sao chúng tôi thử xóa mỗi quý
summary: Niềm tin rằng càng chất nhiều quy tắc thì AI càng thông minh có thể là sai. Chúng tôi tổng hợp cách rút gọn chỉ dẫn và đo xem rút gọn có ổn không.
---
> Bài viết này được soạn thảo cùng AI và biên tập viên đã kiểm duyệt. Chúng tôi có tham khảo các bài viết bên ngoài, và những bài đã tham khảo được nêu ở cuối bài.

Khi giao việc cho AI, mỗi lần nó sai chúng ta lại thêm một dòng quy tắc. "Đừng dùng bảng", "Dùng kính ngữ", "Gắn nguồn". Vài tháng sau, tài liệu chỉ dẫn thành hai mươi, ba mươi dòng, và chúng ta gọi đó là tài sản. Nhưng hầu như chưa ai kiểm tra xem những quy tắc này có thật sự làm việc hay không.

## Quy tắc dễ thêm, hiệu quả khó kiểm chứng

Bài viết chúng tôi tham khảo nêu luận điểm này. Khi mô hình tốt lên, những quy tắc từng cần thiết trước đây đã không còn cần nữa, và quy tắc không còn cần thiết không phải là vô hại mà **làm tăng tổng lượng điều phải tuân thủ, khiến cả những quy tắc quan trọng cũng bị mờ đi**. Bài này dẫn một nghiên cứu benchmark cho rằng số chỉ thị càng nhiều thì tỷ lệ tuân thủ càng giảm. Tuy nhiên chúng tôi chưa kiểm tra được con số đó đến tận nguyên bản, nên chỉ tiếp nhận ở mức "có nghiên cứu như vậy". Điều quan trọng hơn trong thực tế là hướng đi. **Quy tắc càng nhiều thì AI càng có thể lặng lẽ bỏ sót một phần, và chúng ta không biết đã thiếu cái gì.**

## Tiêu chí dọn dẹp chúng tôi đặt ra

1. **Mỗi quý một lần, xóa trống toàn bộ chỉ dẫn.** Chạy cùng một tác vụ mà không có chỉ dẫn rồi xem kết quả.
2. **Thêm lại từng dòng và xem khác biệt.** Nếu thêm vào mà kết quả không đổi thì xóa dòng đó.
3. **Nghi ngờ những quy tắc không ghi "vì sao".** Quy tắc không giải thích được lý do thường chỉ là dấu vết của một sự cố nào đó.
4. **Đặt tiêu chuẩn thay vì cấm đoán.** Một dòng "độc giả của bài này là ai" thay đổi được nhiều hơn mười dòng "đừng làm...".
5. **Không xóa quy tắc về hành động không thể đảo ngược.** Quy tắc về xóa, thanh toán, gửi đi, đăng công khai được giữ lại bất kể hiệu năng.

## Tổng kết

Chỉ dẫn không phải tài sản để tích trữ mà là thiết bị tốn chi phí duy trì. Thử rút gọn, và nếu không có khác biệt thì cứ giữ bản đã rút gọn, như vậy nhẹ và an toàn hơn.

## Các bài đã đọc cùng

Bài viết này tham khảo vấn đề được nêu trong các bài dưới đây, rồi viết lại theo góc nhìn và tiêu chí của đội chúng tôi. Chúng tôi không theo câu chữ hay bố cục của chúng, và những số liệu mà bài gốc dẫn nhưng chúng tôi chưa tự kiểm tra được đến dữ liệu gốc thì đều đã đánh dấu như vậy. Một số bài gốc chỉ mở toàn văn sau khi đăng nhập, nên chúng tôi đọc theo phần được công khai.

- [AI không hề ngốc đi — chính những chỉ dẫn viết từ nửa năm trước đang kéo nó lại (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-claude-md-rules)

Các nguồn khác chúng tôi đối chiếu:

- [How Many Instructions Can LLMs Follow at Once? (IFScale, arXiv)](https://arxiv.org/abs/2507.11538) — tiếng Anh
- [Context Rot: How Increasing Input Tokens Impacts LLM Performance (Chroma Research)](https://research.trychroma.com/context-rot) — tiếng Anh
- [Effective context engineering for AI agents (Anthropic Engineering)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — tiếng Anh
- [Lost in the Middle: How Language Models Use Long Contexts (arXiv)](https://arxiv.org/abs/2307.03172) — tiếng Anh
