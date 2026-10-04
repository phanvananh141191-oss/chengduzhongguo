# P2 · Rà soát các chỗ «cần duyệt» (cờ ⚠ trong `P2_ket_qua_chuan_hoa.md`)

Số cờ đo được: 66 dòng ⚠ (nhóm lại bên dưới; con số 68–72 tính cả các ghi chú không phải tiêu đề).

| Nhóm | Số | Bài | Kết quả rà |
|---|---|---|---|
| Tiêu đề bài tập A–G chèn từ nhãn Hán trong thân | 50 | 2×11, 7×10, 8×11, 9×6, 11×5, 12×7 | Đúng. Chuỗi A→G liên tục ở mọi bài (bài 9, 11 chỉ "lệch" vì phần 参考答案). 拓展 bài 3 là A B C D. Không còn nhãn Hán nào chưa chuyển. |
| Tiêu đề 任务 chèn từ thân | 11 | 7, 8, 9/10, 11 | Đúng ranh giới; nhãn chuẩn hoá `任务X　…`. |
| Tiêu đề 词语表 | 4 | 7, 8 | Đúng vị trí (trước bảng từ, kèm 🔊 n-1/n-3). |
| Nhãn Việt thuần (bài 1 E, bài 3 B) | 0 còn lại | 1, 3 | Đã sửa: lấy Hán từ ô bảng / thân. |
| Gộp tiêu đề trùng | 1 | 2 | Đúng (`促成 · 对话` đã gộp). |
| Ghi chú dịch giả → KB | 4 | 6 | Rà: toàn nhận xét của người dịch, không phải nội dung sách; nằm ở `nguon_md_ky/chuan/_kb/`. |
| Khung bỏ | 2 | 11 | Đúng. |

Sửa trong `tools/normalize_ky_md.py` khi rà: nhận nhãn Hán `A 中…` (kể cả ngoặc/“), cắt nhãn dài ở câu đầu, lấy nhãn từ ô bảng, nhãn Việt `A.`/`A:`, chuẩn hoá nhãn 任务.

Kiểm bất biến: 0 dòng thân bị mất, 0 dòng thêm ở cả 12 file.

Còn nên mắt người xem: nhãn dài của bài 8 F/G và bài 12 F (đã giữ nguyên văn đề, không rút gọn).
