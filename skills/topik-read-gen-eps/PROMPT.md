Bạn là agent gen câu hỏi EPS-TOPIK Đọc. Thực hiện tuần tự:

1. Đọc SKILL.md → nắm JSON format + quy tắc chung
2. Với MỖI dạng: đọc kinds/{kind}.md + samples.json → gen → QC → lưu CSV output/read-eps/level_3/{kind}.csv
3. Merge tất cả → output/read-eps/all_questions.csv → xóa gen_temp*.json

QC: explain không trap/emoji, xuống dòng rõ, câu ghép dịch q_text, q_correct phân bố đều 1-4

## Danh sách gen (mặc định 1 bài/dạng)

320001, 320002, 320003, 320004, 320005, 3420002, 3420003, 3420006, 3420007, 3420008
