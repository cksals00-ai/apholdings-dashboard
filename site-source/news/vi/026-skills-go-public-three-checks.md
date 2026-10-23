---
no: 26
slug: skills-go-public-three-checks
date: 2026-10-23
category: Góc nhìn
tags: Agent Skills · Anthropic · Linux Foundation · AAIF · phiên bản API · Railway · khóa API
title: Skill đã trở thành "chuẩn chung" — Agent Skills được hiến tặng cho quỹ, phiên bản API mới đầu tiên sau ba năm, và những chiếc chìa khóa bị đánh cắp: ba điều chúng tôi đã kiểm tra
summary: Ngày 22 tháng 10, Anthropic chuyển giao chuẩn Agent Skills cho AAIF thuộc Linux Foundation; một ngày trước đó, Claude API có phiên bản mới đầu tiên kể từ năm 2023; và cùng ngày, nhà cung cấp dịch vụ lưu trữ Railway thông báo các biến môi trường chứa khóa API của khách hàng có thể đã bị rò rỉ. Chúng tôi đọc ba tin khác nhau từ góc nhìn của "một thư mục skill" và ghi lại thứ tự mình đã kiểm tra.
---
> Bài viết này được soạn cùng AI (Claude) và đã được biên tập viên kiểm duyệt. Anthropic, trung tâm của bài viết này, là công ty tạo ra Claude mà chúng tôi dùng để viết bài, và công ty chúng tôi cũng tự xây dựng và sử dụng nhiều skill nội bộ, nên chúng tôi có lợi ích liên quan cần công khai. Vì vậy, các con số do công ty công bố được đánh dấu là "công ty công bố", và thay vì đánh giá tốt hay xấu, chúng tôi chỉ ghi lại thứ tự mình đã thực sự kiểm tra. Đây không phải là ý kiến đầu tư về bất kỳ công ty nào.

Tuần này, trong ba ngày có ba tin về "linh kiện" của các tác nhân AI. Một tin về định dạng (định dạng skill rời khỏi tay một công ty và về với một quỹ), một tin về phiên bản (Claude API có phiên bản mới sau ba năm), và một tin về chìa khóa (khóa API gửi ở nhà cung cấp dịch vụ lưu trữ có thể đã bị rò rỉ). Đọc riêng, đó là những tin khác nhau. Nhưng nhìn từ vị trí người vận hành một thư mục skill, cả ba hội tụ về cùng một câu hỏi: trong thư mục của tôi có gì, và nó phụ thuộc vào đâu? Hãy đọc bài này như phần tiếp theo của NO.8 (khi skill lên tới mười nghìn) và NO.20 (thứ tự kiểm tra trước khi cài đặt).

## 1. Định dạng — định dạng skill đã về với một quỹ (sự thật)

Ngày 22 tháng 10, Anthropic thông báo hiến tặng chuẩn Agent Skills cho Agentic AI Foundation (AAIF) thuộc Linux Foundation. Theo thông báo, phần hiến tặng gồm bản thân chuẩn, tên và logo "Agent Skills", tổ chức GitHub và tên miền agentskills.io. AAIF là quỹ do Anthropic lập cùng Block và OpenAI, và trước đó Anthropic cũng đã chuyển MCP (Model Context Protocol) cho quỹ này.

Thông cáo báo chí của Linux Foundation cho biết cùng ngày quỹ đã nhận bốn dự án: Agent Skills của Anthropic, Open Responses của OpenAI (chuẩn gọi mô hình dùng chung cho nhiều nhà cung cấp), OpenEnv của Hugging Face (chia sẻ môi trường học tăng cường) và OpenSandbox của Alibaba (sandbox cho tác nhân). Số dự án do quỹ quản lý tăng từ 3 khi ra mắt tháng 12 năm 2025 lên 10.

Trang đặc tả (agentskills.io) định nghĩa skill rất ngắn gọn. **Skill là một thư mục chứa tệp SKILL.md.** Tệp này gồm tên và mô tả (các trường tối thiểu) cùng phần hướng dẫn; nếu cần, các script, tài liệu tham khảo và mẫu được đặt trong cùng thư mục. Khi khởi động, tác nhân chỉ đọc tên và mô tả; khi có việc phù hợp, nó mới đọc toàn bộ hướng dẫn; trong lúc thực thi, nó mở script hoặc tệp tham khảo. Đặc tả gọi ba bước này là "công bố dần" (progressive disclosure).

Các con số về quy mô là do Anthropic công bố. Hơn 70 sản phẩm tác nhân đã chấp nhận định dạng này (ví dụ được nêu: ChatGPT, Cursor, GitHub Copilot, VS Code), khoảng 1 triệu skill đã được công bố, và khoảng 280 triệu lượt cài đặt. Tờ MIXED của Đức bổ sung rằng đây là số liệu công ty tự thống kê, không phải số người dùng được xác minh độc lập. Chúng tôi cũng giữ lập trường đó.

Cách vận hành cũng nằm trong thông báo. Các kỹ sư từ Anthropic, Google, OpenAI và những công ty khác sẽ bảo trì chuẩn với tư cách cá nhân chứ không phải đại diện công ty; hai người bảo trì chính là David Soria Parra và Mahesh Murag. Không cần là thành viên quỹ vẫn có thể dùng và đóng góp. Thông báo cũng nêu ba việc "sắp tới": phát hành có đánh số phiên bản, quy trình chính thức để đề xuất thay đổi đặc tả, và **hướng dẫn bảo mật cho người viết và cài đặt skill**. Như MIXED đã chỉ ra, ba điều này vẫn là đề xuất, chưa phải thứ đã ra mắt.

## 2. Phiên bản — Claude API có phiên bản mới sau ba năm (sự thật)

Một ngày trước đó, ngày 21 tháng 10, Claude API ra phiên bản mới "2026-10-21". Danh sách phiên bản trong tài liệu của Anthropic chỉ có ba mục — 2023-01-01, 2023-06-01 và nay là 2026-10-21 — tức là phiên bản mới đầu tiên sau ba năm bốn tháng. Tài khoản dành cho nhà phát triển (@ClaudeDevs) cho biết SDK và CLI mới dùng phiên bản này theo mặc định (chúng tôi không mở được trực tiếp bài đăng trên X; chúng tôi xác nhận qua bản tóm tắt của trang tổng hợp Hàn Quốc promppy và tài liệu chính thức của Anthropic).

Trong các thay đổi được liệt kê ở hướng dẫn di chuyển, đây là những điểm một nhóm nhỏ dễ gặp ngay:

- **Ba tham số temperature, top_p, top_k bị bỏ.** Gửi chúng dù ở giá trị mặc định cũng trả về lỗi 400. Tài liệu ghi rằng mã từng dựa vào temperature thấp để có câu trả lời ổn định sẽ mất hiệu ứng đó, và không có thiết lập nào thay thế.
- **Header xác thực thay đổi.** SDK mới gửi khóa theo dạng Authorization: Bearer thay vì X-Api-Key. Proxy hoặc gateway ở giữa đang đọc header cũ cần được sửa.
- Đặt khối document trực tiếp trong thông điệp assistant, hoặc citations trong khối text của thông điệp user, sẽ trả về lỗi 400.
- Nhiều tên trường phản hồi của Admin API thay đổi (roles → role_ids, name → display_name, v.v.).
- Python SDK dùng phiên bản mới từ 2.0.0. Giấy phép của SDK và CLI chuyển sang Apache 2.0.

Điều quan trọng là **phiên bản cũ không bị cắt ngay**. Tài liệu ghi rằng SDK hiện có vẫn gửi header 2023-06-01 nên bạn có thể ở lại phiên bản hiện tại, và ngày kết thúc của 2023-06-01 không được ghi ở đâu cả. "Không có ngày kết thúc" và "được duy trì mãi mãi" là hai điều khác nhau, nên chúng tôi chỉ ghi nhận điều thứ nhất là đã xác nhận.

## 3. Chìa khóa — khóa API gửi ở nhà cung cấp lưu trữ có thể đã bị rò rỉ (sự thật)

Cùng ngày 21 tháng 10, nhà cung cấp dịch vụ lưu trữ ứng dụng Railway đăng thông báo bảo mật trên blog chính thức. Nội dung chính: sáng hôm đó họ phát hiện hoạt động bất thường trong hệ thống lưu biến môi trường của khách hàng, và kết quả điều tra cho thấy **một bên thứ ba không được phép có thể đã truy cập các biến môi trường đã mã hóa và, với một phần trong số đó, lấy được cả nội dung đã giải mã**. Biến môi trường thường chứa khóa API và thông tin đăng nhập cơ sở dữ liệu, registry. Railway viết rằng họ xem sự việc này là "một phần của chuỗi tấn công gần đây nhắm vào các công ty nền tảng" với mục tiêu xâm nhập các nhà cung cấp suy luận AI.

Công ty đã làm ba việc: thông báo cho các nhà cung cấp phía trên để chủ động thu hồi khóa, tạm dừng mọi triển khai, và cho biết sẽ gửi email tới các tài khoản bị ảnh hưởng khi xác nhận được. Với người dùng, dù phân tích ban đầu cho thấy ảnh hưởng có thể chỉ giới hạn ở một nhóm người dùng, Railway vẫn khuyến nghị mạnh mẽ **thay ngay toàn bộ biến môi trường (gồm khóa API và thông tin đăng nhập registry riêng) và rà soát nhật ký của các dịch vụ đó để tìm hoạt động bất thường**. Thông báo không có con số nào như số tài khoản bị ảnh hưởng hay số biến bị lộ.

Trên mạng xã hội và một số trang tin có các ý kiến xoay quanh sự việc này như "khóa bị đánh cắp lập tức thành tiền mặt ở chợ đen", "có nhu cầu tạo dữ liệu huấn luyện để chưng cất mô hình", "hàng trăm nghìn đô la bị rút khỏi ví tiền mã hóa". Chúng tôi không xác nhận được bất kỳ điều nào trong số đó từ tài liệu của Railway hay cơ quan điều tra, nên trong bài này chúng tôi chỉ dừng ở mức "có những tuyên bố như vậy".

## Điểm ba tin gặp nhau trong một thư mục (diễn giải)

Thư mục skill rất nhẹ: một tệp SKILL.md và vài script. Nhưng thư mục nhẹ ấy dựa vào ba thứ.

Thứ nhất, **định dạng**. Cấu trúc thư mục và các trường tên, mô tả phải theo đặc tả thì sản phẩm tác nhân khác mới đọc được. Khi đặc tả còn nằm trong một công ty, quy tắc là "họ đổi thì mình đổi theo". Khi đã về quỹ, quy tắc thành "theo dõi phiên bản và quy trình đề xuất rồi đi theo". Cho đến khi các bản phát hành có phiên bản và hướng dẫn bảo mật mà quỹ hứa thực sự xuất hiện, trên thực tế điều này không khác hôm nay nhiều.

Thứ hai, **phiên bản API mà script gọi**. Nếu script trong skill đang truyền temperature, hoặc đi qua proxy đọc header X-Api-Key, skill đó sẽ hỏng âm thầm ngay khi bạn nâng cấp SDK. Skill không phải thứ kết thúc ở "cài xong chạy tốt"; nó là thứ phải chạy lại mỗi khi phiên bản API bên dưới thay đổi.

Thứ ba, **chìa khóa mà script dùng nằm ở đâu**. Dù bạn chưa từng ghi khóa vào skill, nếu khóa nằm trong biến môi trường của máy chủ chạy skill, và máy chủ đó ở nhà cung cấp lưu trữ, thì khóa có thể rò rỉ từ một nơi không liên quan gì đến thư mục của bạn — như sự việc Railway lần này. Chúng tôi cho rằng đây cũng là lý do quỹ đặt "hướng dẫn bảo mật cho người viết và cài đặt skill" làm nhiệm vụ đầu tiên (mối liên hệ này là diễn giải của chúng tôi, không phải lý do quỹ nêu ra).

## Nếu là chúng tôi — ba điều đã kiểm tra trong thư mục skill (thực hành)

Công ty chúng tôi xây dựng các skill nội bộ (chính sách màn hình ứng dụng, quy trình phân tích dữ liệu, kiểm tra bài viết, v.v.) theo định dạng SKILL.md. Đây là thứ tự chúng tôi đã thực sự kiểm tra sau tin tuần này.

1. **Kiểm tra định dạng.** Chúng tôi xác nhận mọi SKILL.md đều có name và description, và mô tả nói được trong một dòng "khi nào thì lấy skill này ra". Hai trường đó là mức tối thiểu đặc tả yêu cầu, và cũng là hai thứ duy nhất tác nhân đọc lúc khởi động. Khi quỹ phát hành bản có số phiên bản, chúng tôi quyết định ghi số phiên bản đó vào tài liệu tham khảo trong mỗi thư mục skill.
2. **Kiểm tra phiên bản.** Chúng tôi tìm các chuỗi temperature, top_p, top_k và X-Api-Key trong script của các thư mục skill. Hễ xuất hiện, skill đó được đưa vào danh sách "sửa trước khi nâng SDK". Chúng tôi không nâng SDK ngay; chỉ nâng khi danh sách cần sửa trống. Nếu ngày kết thúc phiên bản cũ được công bố, chúng tôi đẩy lịch lên sớm hơn.
3. **Kiểm tra chìa khóa.** Chúng tôi tìm lại để chắc không có khóa nào được ghi trong thư mục skill hay kho mã, và lập danh sách nơi khóa được đặt (biến môi trường của nhà cung cấp lưu trữ, công cụ quản lý bí mật). Khóa giao cho bên ngoài được xếp vào loại "khóa sẽ rò rỉ cùng nếu nhà cung cấp đó bị xâm nhập", và chúng tôi xác nhận đã đặt cảnh báo mức dùng và hạn mức chi tiêu. Chúng tôi cho rằng việc "rà soát nhật ký tìm hoạt động bất thường" mà Railway khuyến nghị chỉ hữu ích khi nó đến dưới dạng cảnh báo trong ngày thường, chứ không phải sau khi sự cố xảy ra.

Ba việc này đáng chạy mỗi quý một lần ngay cả khi không có tin mới. Ở NO.5 chúng tôi đã viết "chỉ dẫn là nợ, không phải tài sản", và thư mục skill cũng vậy. Thư mục càng nhiều, việc cần kiểm tra theo ba trục định dạng, phiên bản, chìa khóa càng tăng.

## Những điều chưa xác nhận được trong tin này

- Hơn 70 nền tảng, khoảng 1 triệu skill và khoảng 280 triệu lượt cài đặt do Anthropic công bố là số liệu công ty tự thống kê; chúng tôi không tìm thấy tài liệu xác minh độc lập.
- Chúng tôi không mở được bài đăng gốc trên X của @ClaudeDevs; phiên bản API mới được xác nhận qua tài liệu chính thức của Anthropic (danh sách phiên bản, hướng dẫn di chuyển). Số phiên bản major mới chính xác của SDK các ngôn ngữ khác ngoài Python chưa xác nhận được từ tài liệu.
- Tài liệu không có ngày kết thúc cho phiên bản 2023-06-01. Chúng tôi chỉ xác nhận được là "không có".
- Quy mô sự việc Railway (số tài khoản, số biến), chủ thể tấn công và mối liên hệ với các vụ xâm nhập nền tảng khác không có trong thông báo của Railway; các con số từ truyền thông và mạng xã hội (thiệt hại ví, v.v.) chưa xác nhận được.
- Với bài ngày 20 tháng 10 trên trang tham khảo Learn:US (cách cài đặt an toàn skill do người khác làm), chúng tôi chỉ đọc được tóm tắt công khai ở danh sách, không mở được phần thân bài.

## Những bài đã đọc cùng

Chúng tôi đã trực tiếp mở các nguồn có tính chất khác nhau. Thông báo của công ty và quỹ, tài liệu chính thức, báo chí và blog cá nhân được liệt kê riêng.

Thông báo của công ty và quỹ:

- [Donating Agent Skills to the Agentic AI Foundation (Anthropic)](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) — tiếng Anh, thông báo công ty (số liệu do công ty thống kê)
- [Agentic AI Foundation Announces Four New Projects: Agent Skills, Open Responses, OpenEnv, and OpenSandbox (Linux Foundation)](https://www.linuxfoundation.org/press/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox) — tiếng Anh, thông cáo báo chí của quỹ
- [Security Disclosure: Wednesday October 21st (Railway)](https://blog.railway.com/p/security-disclosure-wednesday-october-21st) — tiếng Anh, thông báo công ty

Tài liệu chính thức và đặc tả:

- [Agent Skills Overview (agentskills.io)](https://agentskills.io/) — tiếng Anh, trang đặc tả
- [Versions (Claude Platform Docs)](https://platform.claude.com/docs/en/api/versioning) — tiếng Anh, tài liệu chính thức
- [Migrating to API version 2026-10-21 (Claude Platform Docs)](https://platform.claude.com/docs/en/api/migration-2026-10-21) — tiếng Anh, tài liệu chính thức

Báo chí và tóm tắt:

- [Anthropic hands its widely used AI skills standard to an independent foundation (MIXED)](https://mixed-news.com/en/anthropic-agent-skills-agentic-ai-foundation/) — tiếng Anh, báo chí (chỉ ra giới hạn của số liệu công ty)
- [Anthropic công bố phiên bản Claude API mới 2026-10-21 (promppy)](https://www.promppy.com/item/2535081) — tiếng Hàn, trang tổng hợp tóm tắt bằng AI (nguồn gốc: bài đăng trên X)
- [Sự cố xâm nhập Railway, khóa API AI bị đánh cắp (promppy)](https://www.promppy.com/item/2535863) — tiếng Hàn, trang tổng hợp tóm tắt bằng AI (nguồn gốc: bài đăng trên X, có tuyên bố chưa xác nhận)

Blog cá nhân và trang thực hành:

- [Donating Agent Skills to the Agentic AI Foundation (Simon Willison)](https://simonwillison.net/2026/Oct/22/donating-agent-skills/) — tiếng Anh, blog cá nhân (nhìn lại dự đoán tháng 12 năm 2025)
- [Ba skill nên đưa vào Claude trước khi bắt đầu công việc (Learn:US)](https://learn.bizni.us/) — tiếng Hàn, trang thực hành (chỉ xem tóm tắt công khai)
