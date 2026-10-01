# Báo cáo bàn giao: đồng nhất giao diện D1 · D2 · KY

File đã chỉnh: `Tong_hop_3_giao_trinh_D1_D2_KY.html`. Bản gốc trước khi sửa: `backup/Tong_hop_3_giao_trinh_D1_D2_KY.truoc-khi-dong-nhat.html`.
Mã dựng lại file: `tools/dong-nhat-ui/` (chạy `python3 build.py`, đọc bản sao lưu và ghi ra file chính).

Quy ước: D1 = 乐读 5, D2 = 发展汉语 II, KY = 汉语口语.

## 1. Đã thay đổi
- **Khuôn bài chung cho cả ba:** đầu bài (tên giáo trình · Bài N · tên Hán · nghĩa Việt), thanh tab *Tổng quan · Từ vựng · Bài khóa / Hội thoại · Ngữ pháp / Mẫu câu · Luyện tập*, có tab *Bổ sung* khi bài có nội dung không thuộc 5 mục. Nội dung rộng 920 px trên desktop.
- **Xem toàn bài:** nút trên thanh công cụ chung, đọc liên tục mọi phần.
- **Thanh công cụ vỏ:** Hiện pinyin · Hiện dịch · Cỡ chữ · Xem toàn bài · Tùy chọn. Lựa chọn được giữ khi đổi bài, đổi giáo trình và tải lại. Nút Hiện dịch tự làm mờ ở nơi không có bản dịch (KY).
- **Pinyin:** chỉ hiện một lần, bằng ruby trên từng chữ Hán (119.559 ruby, đều một chữ một âm tiết). Hán 23 px, pinyin 13 px, Việt 16 px, giống nhau ở cả ba. Dòng pinyin riêng (D1 `.spy/.gpy`, D2 `.lp` và ghi chú pinyin) được ẩn, dữ liệu vẫn còn trong trang. Từ nhiều chữ không bị ngắt dòng giữa chừng. Tắt pinyin thì dòng thu gọn.
- **Từ vựng:** cùng khuôn *Từ vựng · Nghĩa tiếng Việt · Ví dụ · Chi tiết* (Loại từ, Hán Việt, Ghi chú, English). Cột Ví dụ ẩn khi cả bảng không có ví dụ. Điện thoại chuyển thành thẻ dọc.
- **Hội thoại KY:** tách từng lượt, tên người nói in đậm (chỉ khi dữ liệu có).
- **Ngữ pháp:** nhãn *Cấu trúc · Giải thích · Ví dụ · Lưu ý* cho các thẻ nhận dạng được (D2 bài 1–2; D1 thẻ mẫu câu).
- **Luyện tập:** có đáp án → *Kiểm tra · Xem đáp án · Làm lại*; không có đáp án → *Đánh dấu đã luyện · Làm lại*. Tiến độ tách *Đã làm* và *Làm đúng*. Khóa lưu bài làm giữ nguyên.
- **Điện thoại:** nút ≥ 44 px, bảng cuộn trong khung riêng, không tràn ngang cả trang (đã sửa KY bài 7, 10, 12 và D1 mục mẫu câu). Sơ đồ vẽ bằng ký tự khung của KY cuộn trong khung riêng.
- **Sửa thêm:** thời gian chờ khôi phục bài làm của KY tăng từ 0,6 s lên 3 s, vì trang mới nặng hơn nên bản trước bị mất bài làm sau khi tải lại.

## 2. Phần nội dung còn thiếu (để trống, không điền)
| Giáo trình | Phần thiếu |
|---|---|
| D2 | Bài 4 và bài 8: không có bài khóa. Bài 4, bài 8: không có ví dụ nào trong bảng từ vựng. Một số dòng thiếu ví dụ: bài 3 (1), bài 5 (2), bài 6 (1). |
| KY | Ngữ pháp / Mẫu câu trống ở cả 12 bài. Bài 4: không có bài khóa. Bài 5: chỉ có bản ghi âm (mọi tab khác trống). Bài 6: không có Tổng quan, Từ vựng, Bài khóa. Không có bản dịch Việt cho hội thoại, không có đáp án bài tập. |
| D1 | Bảng từ vựng không có ví dụ. Không có bài tập tương tác hay đáp án (Luyện tập gồm Kỹ năng và 实况阅读). Tab Bổ sung chỉ ở bài 2 (Bài giảng). |
| Pinyin | Không có trong từ điển nên để trống: 葬 · 陶 · 陵 (KY bài 2), 狭隘 (KY bài 3). |

## 3. Lỗi nội dung phát hiện (không sửa, cần rà sau)
- D2 bài 6: `“Suàn wǒ jiā”`, `Zhùyì “hái yǒu”`, `Bǎ “nà yì nián”` nằm ở dòng chữ Hán, nên có vẻ thiếu chữ Hán.
- D2 bài 3: các tiêu đề ghi “gợi ý” chưa có đáp án chính thức. Bài 4: có mục nguyên bản “Ghi chú về phần còn thiếu” (giữ ở Bổ sung).
- KY bài 6: ghi chú nguyên bản “File gốc chỉ có 3 trang cuối…” (giữ ở Bổ sung). 19 dấu “cần duyệt” ở cột nghĩa tiếng Việt của KY được giữ trong tiêu đề cột.
- D2 bài 6 có mục tiêu đề “Trang 100” (nguyên bản).

## 4. Kết quả kiểm tra (Chromium thật)
- Kích thước: desktop 1440×900, tablet 820×1180, điện thoại 390×844 (có cảm ứng). Đã duyệt toàn bộ 32 bài × mọi tab. Không có lỗi JavaScript, không tràn ngang cả trang, không nút nhỏ hơn 44 px ở điện thoại (đo cả ba cỡ).
- **Bảo toàn nội dung:** đối chiếu trước/sau cả 43 mục. Chỉ thiếu 86 ký tự, toàn bộ là nhãn giao diện cũ đã thay (tiêu đề cột bảng cũ, “Tiến độ / Ô đúng”).
- Đã thử: chuyển tab, Xem toàn bài, bật/tắt pinyin và dịch, phím mũi tên trên thanh tab, tìm kiếm tự mở đúng tab, Kiểm tra / Xem đáp án / Làm lại, Đánh dấu đã luyện, lưu bài làm sau khi tải lại (D2 và KY), khóa lưu giữ nguyên, chế độ tối (một trang).

## 5. Chưa kiểm chứng được
- Thiết bị thật, Safari, Firefox.
- Phông web (Google Fonts) không tải được trong môi trường kiểm tra, nên điểm xuống dòng có thể lệch nhẹ.
- Nút nghe của D1 (đọc bằng giọng trình duyệt) chưa nghe thử; chỉ ẩn khi trình duyệt không hỗ trợ. D2 và KY không có dữ liệu âm thanh.
- Chế độ tối mới xem một trang. Thứ tự Tab bàn phím và trình đọc màn hình chưa kiểm hết.
- Pinyin lấy từ từ điển nhúng sẵn và ruby có sẵn trong file; không tự sinh thêm.

---

# Bổ sung D2 (发展汉语 II) bài 9–14 từ file bản dịch song ngữ

Nguồn: `tools/dong-nhat-ui/nguon/ban-dich-bai-9-14.md`. Bộ chuyển đổi: `tools/dong-nhat-ui/md2fz.py`, được gọi từ `build.py`.

## Đã làm
- Thêm 6 bài vào D2: 9 中国的四季, 10 匆匆, 11 把生活调成“飞行模式”, 12 中国第一合唱——《黄河大合唱》, 13 胡适致吴健雄的一封信, 14 《乾隆帝》序. Mục lục D2 là Bài 1–14, tổng số bài là 38.
- Mỗi bài có đủ 5 tab theo khuôn chung (Tổng quan · Từ vựng · Bài khóa · Ngữ pháp · Luyện tập), bài 14 có thêm Bổ sung (Phụ lục). Chữ Hán đặt cùng bản dịch tiếng Việt ngay bên dưới. Bản dịch tắt/bật bằng nút **Hiện dịch**.
- Mục chú giải ngữ pháp dùng nhãn *Câu trong bài · Giải thích · Ví dụ · Thử làm* ngay như trong file nguồn.
- Đã bỏ phần lời nhắc và lời dẫn của cuộc trò chuyện (các dòng “tiếp tục…”, ghi chú của trợ lý, chú thích nguồn).
- Chỗ trống trong bài tập giữ nguyên, **không điền đáp án**. Bài tập của 9–14 là dạng văn bản tĩnh, vì file nguồn không có đáp án nên không có nút Kiểm tra / Xem đáp án.

## Phần còn thiếu (theo ghi chú của file nguồn, để trống)
- Bài 11: thiếu 题解 và 词语学习 (trang 171–172) nên tab Tổng quan và Từ vựng trống. Thiếu trang 182–184 và 186 ở phần bài tập.
- Bài 13: thiếu trang 219. Bài 14: thiếu trang 236.
- Bảng từ vựng bài 9–14 chỉ có *Từ vựng · Loại từ · Nghĩa*, không có ví dụ hay Hán Việt, nên cột Ví dụ bị ẩn.
- **Pinyin:** file nguồn không có pinyin, từ điển nhúng trong file không có 211 chữ Hán khác nhau (634 lần xuất hiện, chẳng hạn 摸 嫩 芽 煤 魂…). Những chữ này để trống pinyin, không tự sinh âm đọc. 32.132 chữ còn lại có pinyin. Nếu bạn muốn bổ sung pinyin cho 211 chữ này thì cần bạn duyệt nguồn pinyin.

## Kiểm tra
Mọi đoạn, câu, ô bảng và mục danh sách trong file nguồn đều có mặt trên trang (chỉ khác các nhãn tiêu đề cột và nhãn mục đã chuẩn hóa). Điện thoại 390 px không tràn ngang, không nút nhỏ hơn 44 px; desktop không tràn ngang. Không có lỗi JavaScript.
