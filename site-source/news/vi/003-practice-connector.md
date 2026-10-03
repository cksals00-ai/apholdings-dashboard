---
no: 3
slug: ai-reads-the-label
date: 2026-10-03
category: Thực hành
tags: Connector · MCP · Kiểm tra thành phần · Safelist
title: Khi AI đọc bảng thành phần thay bạn — cách chúng tôi khiến nó không nói "an toàn"
summary: Khi kết nối công cụ bên ngoài với trợ lý AI, câu trả lời chuyển từ "cảm giác" sang "căn cứ". Chúng tôi tổng hợp quy tắc đặt ra khi xây dựng connector Safelist: chỉ nói đến mức "không thấy".
---
> Bài viết này được soạn thảo cùng AI và biên tập viên đã kiểm duyệt. Safelist không phải là công cụ chẩn đoán.

## Vấn đề: câu trả lời nghe có vẻ hợp lý là thứ nguy hiểm nhất

Khi hỏi AI "Gói bánh này có sữa với lúa mì không?", nó thường trả lời nghe rất hợp lý. Nhưng nếu AI trả lời dựa vào trí nhớ, nó sẽ không biết sản phẩm đã thay đổi, rồi nói có thành phần không có hoặc bỏ sót thành phần có thật. Với chuyện ăn uống, cả hai đều là rắc rối.

## Giải pháp: kết nối với công cụ bên ngoài

Trợ lý AI ngày nay có thể gắn công cụ bên ngoài thông qua "connector" (về mặt kỹ thuật là các chuẩn kết nối như MCP). Khi nhận câu hỏi, thay vì lục lại trí nhớ, AI trực tiếp tra cứu dữ liệu công khai rồi chuyển kết quả đến bạn. Connector Safelist tra cứu nguyên liệu của thực phẩm bằng dữ liệu công khai của Bộ An toàn Thực phẩm và Dược phẩm Hàn Quốc (MFDS), và cho thấy sản phẩm có chứa thành phần mà người dùng cần tránh hay không.

## Ba quy tắc chúng tôi đặt ra

1. **Không nói "an toàn".** Điều công cụ có thể nói chỉ dừng ở "không thấy mục cần tránh". Vì lẫn tạp trong quá trình sản xuất hay lỗi ghi nhãn thì dữ liệu không thể biết được.
2. **Xác nhận thành phần cần tránh trước.** Mỗi đứa trẻ cần tránh thành phần khác nhau, nên trước khi tra cứu phải xác định tiêu chí trước.
3. **Không xóa phần miễn trừ.** Dòng cuối câu trả lời "Không phải chẩn đoán · Theo CSDL công khai · Quyết định cuối cùng thuộc về người giám hộ" vẫn được giữ lại cả khi tóm tắt.

## Khái quát: khung dùng được cho mọi việc

Không phải bảng thành phần thì khung này vẫn áp dụng được.

- Với câu hỏi mà con số hay sự thật quan trọng, **giao cho công cụ tra cứu.**
- Điều công cụ không biết thì **để nó nói là không biết.**
- Kết luận **chỉ viết trong phạm vi dữ liệu cho phép.**

Điều khiến AI đáng tin không phải là mô hình lớn hơn, mà là thiết kế buộc nó nói rằng nó không biết khi nó không biết.

## Tự mình dùng thử

Bạn có thể xem ứng dụng Safelist và connector AI trong phần giới thiệu Safelist trên trang chủ. [Xem giới thiệu AP Safe](/en/products/safe/)
