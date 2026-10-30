---
no: 33
slug: agent-prs-40-percent-and-a-new-number-one
date: 2026-10-30
category: Góc nhìn
tags: GitHub Octoverse · PR do agent mở · chọn mô hình · Gemini 4 Carbon · Artificial Analysis
title: Cứ mười pull request trên GitHub thì bốn do agent mở — Số lập trình viên chỉ dùng một mô hình đã giảm, còn vị trí số 1 trên bảng điểm mới thì chưa ai gọi được
summary: Ngày 28/10, GitHub công bố trong báo cáo thường niên Octoverse 2026 rằng «hơn 40% pull request trong tháng 9 được bắt đầu bằng agent». Hồi tháng 3 con số là 17%. Cũng trong báo cáo đó, 61% người dùng Copilot tự chọn mô hình đã dùng từ hai mô hình trở lên trong một tháng, và không mô hình nào vượt quá 25% số yêu cầu. Cùng ngày, bốn tuần sau khi công bố Argon, Google ra mắt «mô hình mạnh nhất» Gemini 4 Carbon — và lần này cũng dành cho một nhóm chuyên gia phòng thủ mạng trước. Bảng điểm nơi Carbon đứng nhất vừa được làm lại toàn bộ một ngày trước đó, nên không thể so với điểm cũ. Chúng tôi đặt cạnh nhau con số từ phía người dùng (GitHub) và con số từ phía nhà sản xuất (Google và tổ chức đánh giá), rồi ghi lại một đội nhỏ nên sửa gì trong cách chọn mô hình.
---
> Bài này được viết cùng AI (Claude) và đã qua biên tập viên kiểm tra. Anthropic, công ty tạo ra Claude, là đối thủ cạnh tranh của Google và OpenAI xuất hiện trong bài, và một mô hình của Anthropic đứng thứ hai trên bảng xếp hạng được bàn ở đây. GitHub là công ty thuộc Microsoft, và công ty chúng tôi là khách hàng trả phí của công cụ AI từ các công ty này. Số liệu do công ty công bố được ghi là «công ty công bố», số liệu của tổ chức đánh giá độc lập được ghi kèm phiên bản bảng điểm. Bài này không phải lời khuyên mua hay bán cổ phiếu của bất kỳ công ty nào.

Ở NO.16 chúng tôi viết «AI nào được dùng nhiều nhất», ở NO.17 viết «việc nào dùng AI nào». Câu trả lời khi đó là «mỗi khảo sát một con số, và các công ty đã nêu mục đích sử dụng». Tuần này, hai bộ số liệu khác hẳn tính chất ra cùng một ngày. Một là số của **phía người dùng**: báo cáo thường niên của GitHub đếm hoạt động cả năm, cho thấy 225 triệu lập trình viên thực sự đẩy gì lên và chọn mô hình nào. Hai là số của **phía nhà sản xuất**: Google lại ra một «mô hình mạnh nhất» và đứng đầu bảng điểm của một tổ chức đánh giá độc lập. Đặt hai bộ số cạnh nhau, điều hiện ra không phải «cái nào tốt nhất» mà là «người ta thực sự chọn thế nào».

## 1. GitHub Octoverse 2026 — 40% pull request do agent mở (sự thật)

GitHub công bố báo cáo thường niên Octoverse 2026 ngày 28/10 (công ty công bố, kỳ thống kê từ 1/10/2025 đến 30/9/2026). Dưới đây là số liệu từ bài chính thức mà chúng tôi đọc trực tiếp.

- **Pull request do agent bắt đầu.** «Tính đến tháng 9, lập trình viên bắt đầu hơn 40% pull request bằng agent. Hồi tháng 3 là 17%.» Riêng tháng 9 là 110 triệu, gấp khoảng 6 lần tháng 3. Báo cáo ghi con số này là **«mức sàn»**, vì không phải mọi lần dùng agent đều được phát hiện.
- **Những PR đó ra sao.** Khoảng 87% PR do agent mở sửa nhiều tệp (PR không có dấu vết agent là 79%), và tỷ lệ được hợp nhất trong hai tuần tăng từ 83% hồi tháng 2 lên 90% vào tháng 9. Nhóm đối chứng giữ ở khoảng 86%.
- **Quy mô chung.** Trong 12 tháng: 17,9 tỷ lượt push, 34,3 tỷ commit, 1,3 tỷ PR được hợp nhất (khoảng 3,5 triệu mỗi ngày), 45,4 tỷ job Actions. Commit tăng từ 12,9 tỷ năm trước lên 34,3 tỷ. Báo cáo cho biết khung thời gian và cách tính đã thay đổi năm nay nên số liệu 2024 và 2025 được tính lại. Lập trình viên Simon Willison có mặt tại sự kiện ghi lại con số công bố trên sân khấu: «220 triệu PR được hợp nhất mỗi tháng, tăng gấp ba trong chưa đầy một năm».
- **Ngôn ngữ.** Theo số người đóng góp, TypeScript đứng nhất, Python nhì, JavaScript ba, và Rust tăng gấp đôi trong một năm, nhanh nhất. Tỷ lệ PR đã hợp nhất có dấu vết AI: TypeScript khoảng 44,1%, Python 41,1%, Rust 40,4%, Java 21,2%.
- **Lập trình viên.** Hơn 225 triệu. Mỹ 38,3 triệu, Ấn Độ 32,0 triệu, cả hai nước đều tăng hơn 10 triệu trong năm nay.

## 2. Cùng báo cáo — số người chỉ dùng một mô hình đã giảm (sự thật)

Octoverse 2026 lần đầu đưa vào thống kê về mô hình mà người dùng **tự chọn** trong GitHub Copilot (công ty công bố). Báo cáo loại bỏ lựa chọn tự động, mức dùng của nhân viên và các yêu cầu dùng khóa riêng, chỉ đếm mô hình có từ 1.000 người dùng hoạt động hằng tuần, và nói rõ các con số này «mô tả mức sử dụng quan sát được, không phải chất lượng mô hình».

- **Dùng từ hai trở lên.** Trong tháng 9, **61% người dùng tự chọn mô hình đã dùng nhiều hơn một mô hình**. Bốn tháng trước là 50%.
- **Nhiều loại hơn.** Số mô hình khác nhau mà người dùng trả phí sử dụng tăng từ 29 hồi tháng 5 lên 47 vào tháng 9, và **không mô hình nào vượt quá 25% số yêu cầu.** Báo cáo không công bố thị phần theo tên mô hình.
- **Mục đích tách ra.** Trong mỗi 100 yêu cầu do người dùng chọn: 38 cho mô hình đa dụng, 37 cho suy luận sâu và lập kế hoạch, 25 cho mô hình nhanh và nhẹ. 63% người dùng trả phí đã dùng chọn mô hình tự động ít nhất một lần trong tháng 9.
- **Bản thân Copilot.** 55% người dùng hoạt động hằng tháng dùng tính năng agent (một năm trước là 35%), và agent trên đám mây tăng 230% so với năm trước.

Cùng tuần, phía OpenAI cũng có một «cách chọn». Trong chủ đề Hacker News về GPT-6.1 Terra, nhân viên OpenAI Ted Sanders giải thích rằng tên mô hình của công ty xếp **theo kích cỡ (Luna < Terra < Sol < Astra)**, kích cỡ quyết định chủ yếu độ tin cậy, chi phí mỗi token và khả năng nhớ các sự kiện ít gặp, còn số phiên bản (6.1) thể hiện mức cải thiện — «chưa phải bước nhảy đủ lớn để gọi là 7». Ông cũng gợi ý: chỉ cần chất lượng thì Astra, hơi quan tâm giá thì Sol, rất quan tâm giá thì Terra hoặc Luna. Dòng chính của cuộc thảo luận là lời phàn nàn: mô hình ra lẻ từng cái nên khó biết cái nào hơn, lại không có hướng dẫn theo tác vụ nên ai cũng phải tự đánh giá. Simon Willison giới thiệu bình luận này, và chúng tôi đã mở chủ đề gốc để xác nhận. Đây là bình luận cá nhân của một nhân viên, không phải tài liệu công ty.

## 3. Google Gemini 4 Carbon — lại «mô hình mạnh nhất», lại dành cho một nhóm trước (sự thật)

Ngày 28/10, Google đăng «Gemini 4 Carbon: our next frontier model» (ký tên Koray Kavukcuoglu của Google DeepMind, công ty công bố). Hai tuần sau khi Argon lên ứng dụng Gemini.

- **Họ nói nó là gì.** «Đạt mức tốt nhất về an ninh mạng và các tác vụ dài (long horizon)», và công ty cho biết các nhóm nội bộ đã để nó làm việc **nhiều ngày liền** trên các tác vụ nhiều bước như tìm và vá lỗi trong các kho mã lớn. Họ nói mã hóa, agent, khoa học, web full-stack và đa phương thức đều tốt hơn.
- **Ai dùng trước.** Tuần này là **một nhóm chuyên gia phòng thủ mạng**; tiếp theo là các đối tác tin cậy trong chương trình Fairwind (chính phủ, hạ tầng trọng yếu, nền tảng cốt lõi, phòng thí nghiệm nghiên cứu phòng thủ, được tiếp cận sau thẩm định); đồng thời tham gia chương trình thử nghiệm tự nguyện trước phát hành của chính phủ Mỹ; còn với lập trình viên, doanh nghiệp và người tiêu dùng là «sớm nhất có thể». **Không có ngày, sản phẩm hay gói cước.** Lúc chúng tôi đọc, trang chương trình Fairwind chỉ ghi Argon. Cả 9to5Google lẫn Mashable đều đọc thời điểm phát hành rộng rãi là «chưa xác định».
- **Giá.** Blog công ty ghi giá giới thiệu giống Argon (2 USD mỗi triệu token đầu vào, 10 USD đầu ra, giảm 95% cho đầu vào được cache) và giá sau đó (4 USD và 20 USD). Nhưng đó là bảng giá của một mô hình chưa gọi được.
- **Số liệu công ty.** WebDev Arena +89 Elo lên hạng 4 (1.768); tìm lỗ hổng SEC-bench Pro 88,2%; khai thác ExploitGym 54,8%; vá lỗi CWE-bench 71,0%; tỷ lệ tấn công thành công 0,0% trên bộ đo tiêm lệnh gián tiếp của Gray Swan (Argon 0,7%); trên Terminal-Bench 4.0 gian lận thành công 0,0%, số lần thử 0,4%; cảnh báo lệch hướng mức cao trong môi trường mã hóa nội bộ giảm khoảng 80%; khẳng định không căn cứ giảm khoảng một nửa. Tất cả do công ty công bố, và công ty cho biết các bộ đo an ninh mạng được chạy khi đã tắt rào chắn. Mashable đọc bảng của công ty và viết «đứng nhất ở 15 trên 17 bộ đo, GPT-6 Astra dẫn ở FrontierSWE 2 và Claude Opus 5.5 dẫn ở OSWorld-2.1».
- **Bảng điểm độc lập.** Trên Chỉ số Trí tuệ **v5.0** của Artificial Analysis, Carbon (High) **đứng nhất với 59 điểm**. Trang mô hình của tổ chức này mà chúng tôi mở trực tiếp ghi: nhất trong 54 mô hình, chi phí 7,76 USD mỗi tác vụ (hạng 47/53), dùng 200 triệu token đầu ra cho toàn bộ chỉ số (trung vị 70 triệu; hạng 51/53 về độ dài dòng), 97,9 giây đến token đầu tiên (trung vị 3,37 giây). Trên bảng xếp hạng của chính tổ chức này (đã kiểm tra trực tiếp), hạng nhì là Claude Opus 5.5 (Max) 58 điểm; con số 50 của Argon là theo Mashable. Trang mô hình ghi có thể gọi qua một nhà cung cấp API là Google (nhãn «Không có API công khai» mà chúng tôi từng thấy đã không còn khi mở lại), nhưng bài của Google không nêu thời điểm phát hành rộng rãi.

Điều quan trọng là chính bảng điểm đã thay đổi. Artificial Analysis **làm lại chỉ số thành v5.0 ngày 27/10** (xác nhận trực tiếp qua nhật ký thay đổi và trang phương pháp của tổ chức). Chín bài đánh giá được gom vào bốn mảng — công việc tri thức, mã hóa, khoa học, tổng quát — mỗi mảng 25%, trong đó năm bài (AA-Briefcase, AutomationBench-AA, FrontierCode 2.0, CritPt v2, AA-Omniscience v1.1) là **đánh giá kín, không công bố đề**. GDPval bị loại khỏi chỉ số. Trang phương pháp ghi rõ điểm của các phiên bản khác nhau không thể so trực tiếp. Argon được 53 ở phiên bản cũ và 50 ở v5. Cùng một mô hình mất 3 điểm — không phải mô hình kém đi, mà là thước đo đã đổi.

## Cách đọc hai bộ số liệu cạnh nhau (diễn giải)

Thứ nhất, **«40%» nghĩa là «bắt đầu bằng agent», không phải «do agent viết».** GitHub đếm dấu vết phát hiện được và gọi đó là mức sàn. PR được người theo dõi từ đầu đến cuối và PR do agent tự mở nằm chung một con số. Dù vậy, điều chúng tôi để ý là tỷ lệ hợp nhất. Việc PR do agent mở được hợp nhất trong hai tuần với tỷ lệ cao hơn (90%) so với phần còn lại (86%) cho thấy người duyệt **đã bắt đầu chấp nhận** chúng. Hướng đi không phải là tỷ lệ từ chối tăng. Tuy nhiên, đây là quan sát bên trong GitHub nơi Copilot bám rất sâu; số liệu của các đội dùng công cụ khác không có ở đây.

Thứ hai, **với câu hỏi «mô hình nào tốt nhất», người dùng đang trả lời «nhiều cái».** 61% dùng từ hai trở lên, 47 loại, không cái nào quá 25%. Ở NO.16 chúng tôi viết «mỗi khảo sát một con số», và số của GitHub cho thêm một lý do: người ta không chọn một mô hình mà **chia công việc thành các làn** rồi chọn theo làn (đa dụng 38, suy luận 37, nhẹ 25). Và việc một người trong công ty nói thẳng «tên mô hình của chúng tôi xếp theo kích cỡ, hãy chọn theo mức nhạy cảm với giá» là điều công ty hiếm khi nói trong tài liệu chính thức. Chúng tôi đọc bình luận đó không như «hướng dẫn của công ty» mà như «gợi ý rằng trục lựa chọn là kích cỡ, giá và tốc độ».

Thứ ba, **một «số 1 mới» phải được xem trên ba điểm.** Có phải đứng nhất ngay sau khi thước đổi không (v5 ra một ngày trước)? Hơn bao nhiêu (1 điểm so với hạng nhì)? Gọi được không (chưa)? Rồi thêm chi phí và độ dài dòng: 7,76 USD mỗi tác vụ, hạng 47/53; token đầu ra gấp khoảng 3 lần trung vị; hơn một phút rưỡi mới có token đầu tiên. Mô hình hơn 1 điểm có hợp với việc của chúng tôi không, các con số này nói nhiều hơn điểm số. Ở NO.15 chúng tôi mô tả Argon là «mạnh hơn, dành cho một nhóm trước», ở NO.22 hỏi «ai chấm điểm». Carbon lặp lại cả hai bài. Khác biệt lần này là «trước» không phải người đăng ký trả phí mà là **chuyên gia phòng thủ mạng**. Công ty đã định mục đích đầu tiên của mô hình này là an ninh, và chúng tôi hiểu đó là lý do họ thận trọng hơn với thời điểm phát hành rộng rãi (diễn giải).

Thứ tư, diễn giải riêng của chúng tôi. Số của phía người dùng và số của phía nhà sản xuất giải thích cho nhau. Khi mô hình «mạnh nhất» thay đổi mỗi hai tuần, người dùng không trói mình vào một mô hình; khi người dùng chạy nhiều mô hình, lựa chọn tự động (63% dùng) và định tuyến trở thành mặc định. Khi viết «tiêu chí làm việc khi mô hình thay đổi hằng tuần» ở NO.4, đó còn là giả định; giờ số liệu của GitHub đã đỡ cho giả định đó.

## Nếu là chúng tôi — sửa ba dòng trong tài liệu chọn mô hình (thực hành)

Đội chúng tôi dùng xen kẽ ba bốn mô hình cho backend ứng dụng, tích hợp thương mại và kịch bản video của Ria. Sửa «bảng mô hình theo tác vụ» của NO.17 bằng số liệu tuần này thì gói gọn trong ba dòng.

1. **Đếm cả PR của chính mình.** Gắn nhãn cho PR do agent (Claude Code, Codex, v.v.) mở, và mỗi tháng ghi ba con số: «tỷ lệ PR do agent mở, tỷ lệ hợp nhất trong hai tuần, tỷ lệ hoàn tác (revert)». Toàn GitHub là 40% và 90%. Nếu số của chúng tôi thấp hơn, đó là vấn đề công cụ hoặc nghẽn ở khâu duyệt; nếu tỷ lệ hợp nhất cao mà hoàn tác tăng, khâu duyệt đã lỏng. Con số thứ ba (hoàn tác) không có trong báo cáo GitHub, và đó là lý do chúng tôi xem thêm.
2. **Chia thành ba làn.** Viết lại bảng tác vụ theo đúng ba làn mà người dùng GitHub thực tế đã chia (38/37/25): đa dụng, suy luận sâu, nhẹ. «Bản nháp đầu kịch bản Ria» là đa dụng, «rà soát quy tắc phán định thành phần của SafeList» là suy luận sâu, «phân loại 100 mô tả sản phẩm» là nhẹ. Mỗi làn ghi lựa chọn đầu và **mô hình dự phòng**, và khi có mô hình mới thì chỉ thử ở **đúng một làn đó**, không phải toàn bộ. Đặt mức nhạy cảm với giá của tác vụ làm tiêu chí thứ hai của làn. Cùng trục với điều Sanders nói.
3. **Số 1 mới chỉ được thử sau khi qua ba dòng kiểm tra.** ① Có so sánh trên cùng phiên bản bảng điểm không (không trộn điểm v4 với v5)? ② Có gọi được qua API không (nếu không thì ghi «chờ» vào bảng và không thử)? ③ Chi phí mỗi tác vụ, độ dài đầu ra, thời gian đến token đầu tiên khác bao nhiêu so với mô hình đang dùng? Điền xong ba dòng mới thử ở một làn của mục 2. Không đổi mô hình vì chênh 1 điểm.

## Những gì lần này chúng tôi không chọn

«Mistral Large 4 (đánh giá ngày 29/10)» trong nhật ký thay đổi của Artificial Analysis không được đề cập vì chúng tôi không tìm thấy thông báo chính thức của Mistral (bài AI Weekly ngày 10/10 dẫn trang mô hình trên Hugging Face để viết «dự kiến mở trọng số ngày 31/10», và chúng tôi chưa mở trực tiếp trang đó). Các số liệu riêng mà công ty bảo mật GitGuardian kèm theo khi đọc Octoverse (28,65 triệu bí mật bị lộ, tỷ lệ commit chứa bí mật do một công cụ lập trình cụ thể hỗ trợ, v.v.) chưa được đối chiếu nên không dùng. Đoạn nhắc đến thay đổi lãnh đạo tại Google DeepMind trong bài của Mashable chỉ có một nguồn nên không dùng. Ba bài mới trên Hugging Face (mô hình chuyển lời nói đa ngôn ngữ của NVIDIA, LFM3 của LiquidAI, và «Có thể tin LLM phán đoán một ý tưởng nghiên cứu có mới không?» của AI2) chúng tôi chưa đọc nội dung. Các thông báo ngày 27 và 28/10 của Anthropic (phát triển thuốc, AI for Science) có xung đột lợi ích lớn nên sẽ xử lý riêng sau khi đối chiếu.

## Những gì chúng tôi chưa xác nhận được

- Mọi số liệu Octoverse đều do GitHub công bố, không có kiểm chứng độc lập. Tỷ lệ agent được chính công ty gọi là «mức sàn», và thống kê mô hình chỉ đếm các yêu cầu tự chọn bên trong Copilot. Thị phần theo tên mô hình không được công bố.
- «220 triệu PR được hợp nhất mỗi tháng» mà Simon Willison ghi lại là con số công bố trên sân khấu; bài chính thức chúng tôi đọc chỉ có tổng 12 tháng (1,3 tỷ). Chúng tôi cũng không tìm thấy con số này trên trang tóm tắt GitHub Universe.
- Các bộ đo an ninh và số liệu an toàn của Carbon là công ty công bố; xác nhận độc lập duy nhất là Chỉ số Trí tuệ. «Nhất ở 15 trên 17» là cách Mashable đọc bảng của công ty, chúng tôi chưa kiểm tra trực tiếp toàn bộ bảng. Điểm v5 là 50 của Argon cũng là theo Mashable.
- Trang mô hình của Artificial Analysis ghi Carbon có thể gọi qua một nhà cung cấp API là Google, nhưng bài của Google không có thời điểm phát hành rộng rãi nên chúng tôi chưa xác nhận được hiện ai gọi được. Số liệu về tỷ lệ ảo giác và độ chính xác của Carbon trên blog của một công ty cổng trung gian không xác nhận được trên trang của tổ chức này nên không dùng.
- Thời điểm phát hành rộng rãi, sản phẩm và gói cước của Carbon không có trong bài của công ty. Giải thích của Ted Sanders là bình luận cá nhân của nhân viên, không phải tài liệu chính thức của OpenAI.

## Bài đọc cùng

Chúng tôi đã mở và kiểm tra trực tiếp các nguồn khác nhau về tính chất. Chia thành tài liệu chính thức của công ty, tổ chức đánh giá độc lập, blog cá nhân và cộng đồng, báo chí, công ty bảo mật, và bài trước của chúng tôi.

Tài liệu chính thức của công ty:

- [Octoverse: Commits, pushes, reach new highs in 2026 as developers build with agents (GitHub)](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/) — tiếng Anh, báo cáo thường niên gốc (PR do agent mở, thống kê chọn mô hình, ghi chú phương pháp)
- [Gemini 4 Carbon: our next frontier model (Google)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/) — tiếng Anh, thông báo gốc của công ty (thứ tự phát hành, giá, số liệu công ty)
- [Fairwind Program (Google DeepMind)](https://deepmind.google/fairwind-program) — tiếng Anh, trang chương trình đối tác tin cậy (chỉ ghi Argon lúc chúng tôi đọc)

Tổ chức đánh giá độc lập:

- [Intelligence Benchmarking Methodology (Artificial Analysis)](https://artificialanalysis.ai/methodology/intelligence-benchmarking) — tiếng Anh, cấu trúc chỉ số v5.0, đánh giá kín, lưu ý không so sánh được giữa các phiên bản
- [Gemini 4 Carbon (trang mô hình của Artificial Analysis)](https://artificialanalysis.ai/models/gemini-4-carbon) — tiếng Anh, chỉ số 59, chi phí mỗi tác vụ, token đầu ra, thời gian đến token đầu tiên
- [Models (bảng xếp hạng của Artificial Analysis)](https://artificialanalysis.ai/models) — tiếng Anh, bảng xếp hạng v5 (nhất Carbon 59, nhì Claude Opus 5.5 Max 58)

Blog cá nhân và cộng đồng:

- [Simon Willison's Weblog, 2026-10-28](https://simonwillison.net/2026/oct/28/) — tiếng Anh, ghi chép tại GitHub Universe và giới thiệu phần giải thích cách đặt tên mô hình của OpenAI
- [GPT-6.1 Terra — thảo luận trên Hacker News](https://news.ycombinator.com/item?id=50248124) — tiếng Anh, bình luận của nhân viên OpenAI Ted Sanders về tên mô hình và tiêu chí chọn (bình luận cá nhân)

Báo chí:

- [Google announces Gemini 4 Carbon with 'significant' coding gains (9to5Google)](https://9to5google.com/2026/10/28/gemini-4-carbon-announcement/) — tiếng Anh, báo công nghệ (để đối chiếu)
- [Google announces Gemini 4 Carbon, its new frontier AI model (Mashable, đăng lại trên Yahoo)](https://tech.yahoo.com/ai/gemini/articles/google-announces-gemini-4-carbon-193050677.html) — tiếng Anh, cách đọc bảng bộ đo của công ty, điểm của Argon, phạm vi phát hành

Công ty bảo mật:

- [GitHub Octoverse 2026: AI Agents, Citizen Developers, and the New Security Reality (GitGuardian, Security Boulevard)](https://securityboulevard.com/2026/10/github-octoverse-2026-ai-agents-citizen-developers-and-the-new-security-reality/) — tiếng Anh, dùng để đối chiếu số liệu Octoverse (số liệu riêng của công ty này không dùng trong bài)

Bài trước của chúng tôi:

- [Việc nào dùng AI nào — Mục đích các công ty nêu và cách thử của chúng tôi (AP News NO.17)](https://www.apholdings.kr/ko/news/which-ai-for-which-job/) — tiếng Hàn, bảng mô hình theo tác vụ mà bài này viết lại
- [AI nào được dùng nhiều nhất — Vì sao các con số khác nhau (AP News NO.16)](https://www.apholdings.kr/ko/news/who-uses-which-ai/) — tiếng Hàn, lý do mỗi khảo sát một con số
- [Mô hình tiên phong đầu tiên của Meta Muse Wonder — Ai chấm điểm (AP News NO.22)](https://www.apholdings.kr/ko/news/meta-muse-wonder-whose-scorecard/) — tiếng Hàn, cách đọc bảng điểm
- [Tin AI tuần này — Hai công ty «rẻ hơn», Google «mạnh hơn, dành cho một nhóm trước» (AP News NO.15)](https://www.apholdings.kr/ko/news/this-week-gpt61-sonnet55/) — tiếng Hàn, cùng mô-típ khi Argon ra mắt
