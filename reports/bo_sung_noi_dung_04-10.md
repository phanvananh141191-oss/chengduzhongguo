# Yêu cầu bổ sung nội dung (04/10/2026) và kết quả đo

**Quy tắc bạn đặt:** nguồn không có bản dịch → dịch sang tiếng Việt; nguồn chỉ có tiếng Việt, không có chữ Hán → biên soạn chữ Hán theo nghĩa tiếng Việt, kèm pinyin. Mọi chỗ bổ sung được **đánh dấu** để phân biệt với nguyên văn sách.

## Đo trên bản v4 (`tools/audit_gaps.py`)

| Nguồn | Hán không có Việt | Việt không có Hán | Xử lý |
|---|---|---|---|
| `fz` bài 1–14 | 0 | 0 chỗ thật (các dòng báo là tiêu đề phụ, Hán nằm ở heading) | Không cần |
| `ld` | 0 | 5 đoạn 《家庭学校》 (bài 1, 泛读) chỉ có tóm ý | **Đã biên soạn Hán + pinyin** (`tools/sync_ld.py`, mục 5), nhãn «Hán biên soạn lại từ tóm ý» |
| `ky` (12 file md) | chưa kiểm ở mức câu | chưa kiểm ở mức câu | Kiểm khi sinh HTML (P5); chỗ thiếu sẽ dịch/biên soạn và đánh dấu |
| `fz` bài 2 (题解), 4 (走进课文, mục 四), 8 (题解, 走进课文) | — | — | **Không có nguồn nào** (không Hán, không Việt): không thể dịch. Giữ banner «Chưa có trong nguồn» cho đến khi bạn gửi nội dung gốc |

Ghi chú: 5 đoạn `ld` được viết lại từ phần tóm ý tiếng Việt, nên chỉ phản ánh đúng ý tóm, không phải nguyên văn bài đọc. Muốn có nguyên văn thì cần bạn gửi bài 《家庭学校》 gốc.
