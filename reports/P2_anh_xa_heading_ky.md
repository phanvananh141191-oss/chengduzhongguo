# P2 · Bảng ánh xạ heading cho 12 file md của `ky` (để duyệt)

Đây là điểm dừng duyệt sau P2. **Chưa sửa file md nào.** Số liệu đo trực tiếp từ 12 file trong `nguon_md_ky/` (bài 1 là `.docx`, đọc theo style Title/Heading1–3).

## 1. Mẫu chuẩn (đích của bước chuẩn hoá)

```
# 第n课 <Hán> · Bài n: <Việt>                      ← h1 duy nhất
## Bảng tên nhân vật
## PREPARE · 驱动 (Khởi động)
### Mở đầu                                        (đoạn giới thiệu + câu hỏi mở đầu)
### 牛刀小试 (Thử sức bước đầu)
#### A 双人活动 … / B 结果展示 …
### 学习目标 (Mục tiêu học tập)
## EXPLORE · 促成 (Khám phá)
### 促成 · 对话 (Hội thoại)
#### 词语表 n-1 🔊
#### A … G   (Hán trước, Việt sau, kèm 🔊 n-2 nếu có)
#### Hội thoại 1 … k  (các đoạn đọc to)
### 促成 · 拓展 (Mở rộng)
#### 词语表 n-3 🔊
#### A … (bài tập / bài đọc)
## PRODUCE · 产出 (Sản xuất)
### 任务支持
### 任务选择
#### 任务一 / 任务二 / 任务三
### 评价 (Tự đánh giá)                              ← M3: mục con của PRODUCE
## 附录 · 录音文本 (Bài nghe)
### 🎧 <tên> n-4-k
### 📝 参考答案 (chỉ bài 9, 11)
```

**Lớp ghi chú KB.** Mọi khối «Ghi chú sắc thái cấu trúc» và «Những từ dễ dịch lệch» (đang là h2 rời, lặp 3–6 lần mỗi bài) được hạ xuống `####` và gắn vào **đúng mục đứng ngay trước nó** (PREPARE, 对话, 拓展, PRODUCE+评价, 附录). Script sinh HTML `ky` tách chúng thành hộp gập «📝 Ghi chú KB»; script sinh KB dùng cùng khối đó (S8 so băm).

**Phần bỏ khỏi thân bài** (không mất nội dung, chuyển sang KB): `# Bài k · Phần n` / `# PHẦN n` (chỉ là dấu chia lượt gửi), `## Mục lục` (bài 9), «Tổng kết …» cuối bài (bài 2, 3, 4, 5, 6, 7, 8, 12), «Phụ lục tổng hợp» (bài 10) và «Tổng hợp các chỗ Lưu ý văn bản» (bài 1) → Phụ lục A/B của KB theo M4.

## 2. Ánh xạ theo bài (chỗ lệch so với mẫu)

| Bài | Nguồn | Lệch hiện có | Việc chuẩn hoá |
|---|---|---|---|
| 1 | docx | Mọi mục lớn là H1; câu hỏi mở đầu là H2; 评价 và PRODUCE là H1 không có mục con; cuối có «Tổng hợp các chỗ Lưu ý văn bản» | Hạ H1→h2 theo mẫu, 评价→h3; «Lưu ý văn bản» sang KB Phụ lục A. Chuyển docx→md trước. |
| 2 | md | `促成 · 对话` tách đôi (`### 促成 · 对话` rồi `### 促成 · 对话 (tiếp: bài tập C–G)`); notes theo 3 phần + phụ lục; `## 评价`; `## Tổng kết` | Gộp hai mục 对话 làm một; 评价→###; bỏ Tổng kết. |
| 3 | md | Bảng từ và bài tập A–G ở `##` thay vì `####`; 拓展 là `## EXPLORE · 促成 · 拓展`; có «Kho từ nhỏ (小词库)» trong 拓展 B; `# Tổng kết toàn bài` | Hạ cấp; giữ 小词库 làm mục con của B; 评价 ###. |
| 4 | md | 5 dấu `# Bài 4 · Phần k`; A–G ở `###`; có «Bài đọc» trong 拓展; bài tập ghi `A 听录音…🔊 4-2` (Hán trước) | Bỏ dấu Phần; hạ A–G xuống `####`; giữ mẫu nhãn Hán-trước. |
| 5 | md | Bài tập ghi «Bài tập A» (Việt thuần); 拓展 tách `### Bảng từ ngữ 🔊 5-3`; 评价 có mục con «Nói về thu hoạch» | Đổi nhãn thành `A …` Hán-trước-Việt-sau theo bảng 3.2; giữ mục con. |
| 6 | md | 5 dấu Phần; `## EXPLORE · 促成 · 拓展` rồi `### 促成 · 拓展` lặp tiêu đề; bài tập `A.` `B.` | Gộp tiêu đề lặp; chuẩn nhãn. |
| 7 | md | 5 dấu `# PHẦN n`; đoạn hội thoại `### 1.–5.` ngang hàng với 促成; **任务选择 không có tiêu đề cho từng nhiệm vụ**; 评价 `###` | Hạ `1.–5.` xuống `####`; tìm ranh giới 任务一/二/三 trong thân văn bản để chèn tiêu đề (cần duyệt vị trí). |
| 8 | md | 5 dấu PHẦN; **bài tập A–G không có tiêu đề** (chỉ có `### 1.–4.` của hội thoại); 任务选择 không có tiêu đề nhiệm vụ; bài nghe ghi «Bài nghe 1: … 🔊 8-4-1» | Không suy được ranh giới A–G từ heading: cần dò theo mẫu «A.», «B.» trong thân và duyệt; mục «词语表» và bài nghe 8-2 sang đúng chỗ (xem HTML hiện tại). |
| 9 | md | Có `## Mục lục` (bỏ); 对话 và 拓展 là `##`; có 参考答案 gộp trong phụ lục (`#### 促成 · 对话`, `#### 促成 · 拓展`); notes cả ở PREPARE và 评价 | Hạ cấp; giữ 📝 参考答案 làm mục con của 附录. |
| 10 | md | **Không có h1** (bắt đầu `## Bài 10`); bài tập A–H (có H); tên bài nghe `🎧 受访者 n 10-4-n`; «Phụ lục tổng hợp» 1–4 cuối file | Thêm h1 từ tên bài; Phụ lục tổng hợp sang KB. |
| 11 | md | `促成 · 对话` và `Bảng từ vựng`/`Bài tập và hội thoại` ở `##`/`###` không đều; «Hội thoại 1–5» ở `###`; bài đọc/段话; 参考答案 gộp trong phụ lục | Hạ cấp; HTML hiện ghi «促成 · 段话»: giữ tên này theo kế hoạch 14.6 mục 5. |
| 12 | md | Không có h1; bài tập **gộp** «Bài tập A–B», «C–G», «A–C»; hội thoại không đánh số | Tách thành A, B, C… theo thân văn bản (cần duyệt); gắn số cho các đoạn hội thoại. |

Số bài có nhãn bài tập Việt thuần hoặc sai cấp: **3, 5, 6, 7, 8, 11, 12** (và hạ cấp ở 4, 9, 10).

## 3. Quyết định cần bạn xác nhận trước khi chuẩn hoá hàng loạt

1. **Bảng tên nhân vật** (mọi bài có): giữ ở đầu bài `ky` làm hộp gập, hay chỉ để ở KB? Mặc định tôi đề xuất **hộp gập đầu bài**.
2. **Bài 7, 8, 12** (tiêu đề bài tập/nhiệm vụ không có hoặc gộp): tôi dò ranh giới theo mẫu «A.», «B.», «Nhiệm vụ …» trong thân. Với chỗ không dò chắc, tôi để **một dòng đánh dấu cần duyệt** thay vì tự đoán. Đồng ý?
3. **Chữ Hán trước hay Việt trước** cho nhãn bài tập: kế hoạch chọn Hán trước (`A 听录音…`). Bài 5, 6, 9, 10, 11, 12 đang Việt thuần: xác nhận đổi.
4. **«Tổng kết» cuối bài** (do dịch giả viết, không thuộc sách): bỏ khỏi trang bài, chuyển KB. Đồng ý?
5. **Bài 8** có nhận định C8 chưa kiểm: mục «闲话谈“瘾”» là tên cả bài, không phải mục. Vị trí h3 này trong HTML hiện tại tôi sẽ xác định khi nạp, không tự gán.

Sau khi bạn trả lời 5 câu trên, bước tiếp theo là viết `tools/normalize_ky_md.py` (đầu ra `nguon_md_ky/chuan/Bai01…12.md`), chạy S1/S2/S3 cho 12 file, rồi dừng duyệt bài mẫu trước khi sinh HTML (P5).
