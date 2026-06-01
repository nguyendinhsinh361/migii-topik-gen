Bạn là agent gen câu hỏi TOPIK Nghe. Thực hiện tuần tự:

1. Đọc SKILL.md (file này cùng folder) → nắm JSON format + quy tắc chung
2. Với MỖI dạng trong danh sách bên dưới:
   a. Đọc kinds/{kind}.md
   b. Đọc samples.json để tham khảo mẫu
   c. Gen số bài theo yêu cầu, q_correct phân bố đều 1-4
   d. QC ngay: explain không trap/emoji, xuống dòng rõ, "Người nam:"/"Người nữ:", trích dẫn Hàn giữ nguyên
   e. Lưu CSV: output/listen-origin/level_{1|2}/{kind}.csv
3. Merge tất cả → output/listen-origin/all_questions.csv
4. Xóa gen_temp*.json

## Danh sách gen (mặc định 1 bài/dạng)

110001, 110002, 110003, 110004, 110005, 110006, 110007, 110008_1, 110008_2, 110008_3, 210001_1, 210001_2, 210002, 210003, 210004_(1), 210004_(2), 210004_(3), 210004_(4), 210005_(1), 210005_(2), 210006_(1), 210006_(2), 210006_(3), 210006_(4), 210006_(5), 210006_(6), 210006_(7), 210006_(8), 210007_(1), 210007_(2), 210007_(3), 210007_(4), 210007_(5), 210007_(6), 210007_(7)
