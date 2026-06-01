Bạn là agent gen câu hỏi TOPIK Đọc. Thực hiện tuần tự:

1. Đọc SKILL.md (file này cùng folder) → nắm JSON format + quy tắc chung
2. Với MỖI dạng trong danh sách bên dưới:
   a. Đọc kinds/{kind}.md
   b. Đọc samples.json để tham khảo mẫu
   c. Gen số bài theo yêu cầu, q_correct phân bố đều 1-4
   d. QC ngay: explain không trap/emoji, xuống dòng rõ, câu ghép phải dịch q_text, trích dẫn Hàn giữ nguyên
   e. Lưu CSV: output/read-origin/level_{1|2}/{kind}.csv
3. Merge tất cả → output/read-origin/all_questions.csv
4. Xóa gen_temp*.json

## Danh sách gen (mặc định 1 bài/dạng)

120001, 120002_1, 120002_2, 120002_3, 120002_4, 120003_1, 120003_2, 120004_1, 120004_2, 120005_(1), 120005_(2), 120006, 120007_1, 120007_2, 120007_3, 220001_a, 220001_b, 220001_c, 220002_a, 220002_b_1, 220002_b_2, 220002_b_3, 220002_c, 220003_a_1, 220003_a_2, 220003_b, 220004, 220005_1_(1), 220005_1_(2), 220005_2, 220006, 220007, 220008_1_(1), 220008_1_(2), 220008_1_(3), 220008_2
