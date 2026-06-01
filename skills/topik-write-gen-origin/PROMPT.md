Bạn là agent gen câu hỏi TOPIK Viết. Thực hiện tuần tự:

1. Đọc SKILL.md (file này cùng folder) → nắm JSON format + quy tắc chung
2. Với MỖI dạng trong danh sách bên dưới:
   a. Đọc kinds/{kind}.md
   b. Đọc samples.json để tham khảo mẫu
   c. Gen số bài theo yêu cầu, q_correct phân bố đều 1-4
   d. QC ngay: explain không trap/emoji, xuống dòng rõ, vi/en cùng cấu trúc, trích dẫn Hàn giữ nguyên
   e. 230002/230003: kèm 5 bài viết mẫu (examples), 230001_2 không ảnh
   f. Lưu CSV: output/write-origin/level_2/{kind}.csv
3. Merge tất cả → output/write-origin/all_questions.csv
4. Xóa gen_temp*.json

## Danh sách gen (mặc định 1 bài/dạng)

230001_1, 230001_2, 230002, 230003
