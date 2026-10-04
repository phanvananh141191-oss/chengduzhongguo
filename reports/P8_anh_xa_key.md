# P8 · Đổi key mục lục và chuyển dữ liệu localStorage

Thực hiện bởi `tools/rekey.py` (chạy cuối `build_v4.sh`).

- **63 key** mục lục đổi theo quy ước `{book}:{loại}{số}` (bảng dưới).
- **Alias**: mọi key cũ vẫn mở đúng (`#fz:l5`, `#ky:s4`, vị trí đọc `u3-last`, liên kết `nav` trong khung). Khung vẫn nhận id nội bộ cũ qua trường `fk`, nên anchor `::…` không đổi.
- **Chuyển dữ liệu**: khi mở trang, khung ngoài đổi tên khoá đã lưu `u3xb:u3x:<sách>:<bài>:…` và `u3xb:ans:<sách>:<bài>:…` (`l5`→`l05`, `s4`→`l04`); khoá thô cũ `u3x:`/`ans:` (chạy từ http) cũng được gom vào `u3xb:` với tên mới. Không ghi đè nếu khoá mới đã có.
- **Sửa kèm**: ô đáp án `textarea.uans` trước đây điền lại giá trị đã lưu *trước* khi cầu nối nạp xong (nên trống khi mở từ file) — nay đợi `UEX.ready`. Khung nằm trong khung ngoài luôn lưu qua cầu nối để tên khoá thống nhất.
- Kiểm bằng Playwright: khoá cũ → khoá mới, nội dung còn nguyên, gõ mới lưu đúng khoá mới, tải lại vẫn thấy; không lỗi JS.
- Chưa đổi: khoá riêng của `ld` (`ledu5-*`) và `gt_*` của `ky` — không dính key mục lục.

| Key cũ | Key mới |
|---|---|
| `fz:l1` | `fz:l01` |
| `fz:l2` | `fz:l02` |
| `fz:l3` | `fz:l03` |
| `fz:l4` | `fz:l04` |
| `fz:l5` | `fz:l05` |
| `fz:l6` | `fz:l06` |
| `fz:l7` | `fz:l07` |
| `fz:l8` | `fz:l08` |
| `fz:l9` | `fz:l09` |
| `fz:l10` | `fz:l10` |
| `fz:l11` | `fz:l11` |
| `fz:l12` | `fz:l12` |
| `fz:l13` | `fz:l13` |
| `fz:l14` | `fz:l14` |
| `fz:lg` | `fz:grammar-index` |
| `fz:lv` | `fz:word-index` |
| `ky:s0` | `ky:intro` |
| `ky:s1` | `ky:l01` |
| `ld:l:1` | `ld:l01` |
| `kb:lessons/01.md` | `kb:l01` |
| `ky:s2` | `ky:l02` |
| `ld:l:2` | `ld:l02` |
| `kb:lessons/02.md` | `kb:l02` |
| `ky:s3` | `ky:l03` |
| `ld:l:3` | `ld:l03` |
| `kb:lessons/03.md` | `kb:l03` |
| `ky:s4` | `ky:l04` |
| `ld:l:4` | `ld:l04` |
| `kb:lessons/04.md` | `kb:l04` |
| `ky:s5` | `ky:l05` |
| `ld:l:5` | `ld:l05` |
| `kb:lessons/05.md` | `kb:l05` |
| `ky:s6` | `ky:l06` |
| `ld:l:6` | `ld:l06` |
| `kb:lessons/06.md` | `kb:l06` |
| `ky:s7` | `ky:l07` |
| `ld:l:7` | `ld:l07` |
| `kb:lessons/07.md` | `kb:l07` |
| `ky:s8` | `ky:l08` |
| `ld:l:8` | `ld:l08` |
| `kb:lessons/08.md` | `kb:l08` |
| `ky:s9` | `ky:l09` |
| `ld:l:9` | `ld:l09` |
| `kb:lessons/09.md` | `kb:l09` |
| `ky:s10` | `ky:l10` |
| `ld:l:10` | `ld:l10` |
| `kb:lessons/10.md` | `kb:l10` |
| `ky:s11` | `ky:l11` |
| `ld:l:11` | `ld:l11` |
| `kb:lessons/11.md` | `kb:l11` |
| `ky:s12` | `ky:l12` |
| `ld:l:12` | `ld:l12` |
| `kb:lessons/12.md` | `kb:l12` |
| `ky:s13` | `ky:word-index` |
| `ld:v:les` | `ld:hub` |
| `ld:v:mor` | `ld:bank-morpheme` |
| `ld:v:for` | `ld:bank-formal` |
| `ld:v:pat` | `ld:bank-pattern` |
| `ld:v:chk` | `ld:bank-chunk` |
| `ld:v:par` | `ld:bank-parsing` |
| `ld:v:scn` | `ld:bank-scanning` |
| `ld:v:map` | `ld:bank-skillmap` |
| `ld:v:gap` | `ld:bank-gap` |
