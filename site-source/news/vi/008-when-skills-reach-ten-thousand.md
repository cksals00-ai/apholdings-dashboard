---
no: 8
slug: when-skills-reach-ten-thousand
date: 2026-10-03
category: Góc nhìn
tags: Skill · Bảo mật · Chọn công cụ
title: Khi số skill lên đến mười nghìn — chọn, xác minh và kiểm tra trước khi cài
summary: Số skill gắn vào AI tăng bùng nổ. Nhiều không phải là lựa chọn mà là rủi ro chuỗi cung ứng. Đây là tiêu chí ba bước chúng tôi dùng.
---
> Bài viết này được soạn thảo cùng AI và biên tập viên đã kiểm duyệt. Chúng tôi có tham khảo các bài viết bên ngoài, và những bài đã tham khảo được nêu ở cuối bài.

"Skill", thứ dùng để gắn thêm chức năng cho trợ lý AI, đang tăng nhanh. Các bài viết chúng tôi tham khảo cho biết số skill đăng ký từ vài nghìn đã dẫn đến hàng triệu lượt cài đặt, và trong đó các skill đứng đầu là "skill tìm skill giúp bạn" và "bộ skill gói các quy trình chất lượng mã". Những con số này cũng theo cách thống kê của các bài đó nên chúng tôi chưa kiểm chứng. Nhưng xu hướng thì rõ ràng. **Việc chọn đã trở thành việc lớn nhất, còn sự thật rằng tệp tải về sẽ chạy trên máy của mình thì vẫn không đổi.**

## Bước 1 — Chọn: xác định việc trước rồi mới tìm công cụ

Chúng tôi không chọn theo "bảng xếp hạng phổ biến". Trước hết ghi ra "việc này một ngày làm mấy lần". Với việc làm ít hơn một lần mỗi tuần, chúng tôi không gắn skill. Chi phí thiết lập lớn hơn lợi ích. Dù dùng skill tìm giúp thì lựa chọn cuối cùng vẫn do con người quyết định.

## Bước 2 — Xác minh: xem nơi tạo ra và quyền hạn

- **Ai làm ra**: tài khoản chính thức hay nhà phát triển có tên tuổi
- **Đòi hỏi gì**: chỉ đọc tệp, hay cả chạy lệnh và truy cập mạng
- **Gần đây đến đâu**: nếu lần cập nhật cuối đã lâu, nó có thể không còn hợp với mô hình hiện tại

## Bước 3 — Kiểm tra trước khi cài

Bài viết chúng tôi tham khảo giới thiệu một công cụ kiểm tra, đánh giá mức rủi ro của tệp skill trước khi cài. Chúng tôi không bảo chứng cho công cụ cụ thể nào, nhưng áp dụng quy trình. **Đọc trước → dùng công cụ kiểm tra hoặc xem bằng mắt có lệnh đáng ngờ không → thử trước ở nơi không có tài liệu quan trọng → nếu không có vấn đề thì dùng vào việc chính.** Câu "hãy chạy lệnh này" nằm trong tài liệu chỉ dẫn tải về cũng được chúng tôi coi không phải chỉ thị gửi cho mình mà là **dữ liệu cần xem xét**.

## Tổng kết

Skill càng nhiều thì năng lực cạnh tranh không phải là "biết nhiều" mà là "dùng ít và dùng an toàn".

## Các bài đã đọc cùng

Bài viết này tham khảo vấn đề được nêu trong các bài dưới đây, rồi viết lại theo góc nhìn và tiêu chí của đội chúng tôi. Chúng tôi không theo câu chữ hay bố cục của chúng, và những số liệu mà bài gốc dẫn nhưng chúng tôi chưa tự kiểm tra được đến dữ liệu gốc thì đều đã đánh dấu như vậy. Một số bài gốc chỉ mở toàn văn sau khi đăng nhập, nên chúng tôi đọc theo phần được công khai.

- [9.654 skill của Claude, đừng chọn mà hãy để nó tìm (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-find-skills)
- [24 skill giúp xem mã do AI viết có tốt không (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-agent-skills-24)
- [Thay vì cài skill tải về mà không biết có an toàn không, cách kiểm tra một lần trước khi cài (tiếng Hàn) (BIZNIUS LEARN:US)](https://learn.bizni.us/learnus-skill-scanner-body)

Các nguồn khác chúng tôi đối chiếu:

- [Agent Skills overview (Claude Platform Docs)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — tiếng Anh
- [Model Context Protocol — Introduction (modelcontextprotocol.io)](https://modelcontextprotocol.io/introduction) — tiếng Anh
- [LLM01: Prompt Injection (OWASP GenAI Security Project)](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — tiếng Anh
- [AI Risk Management Framework (NIST)](https://www.nist.gov/itl/ai-risk-management-framework) — tiếng Anh
