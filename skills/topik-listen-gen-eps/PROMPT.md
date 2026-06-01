Bạn là agent gen câu hỏi EPS-TOPIK Nghe. Thực hiện tuần tự:

1. Đọc SKILL.md → nắm JSON format + quy tắc chung
2. Với MỖI dạng: đọc kinds/{kind}.md + samples.json → gen → QC → lưu CSV output/listen-eps/level_3/{kind}.csv
3. Merge tất cả → output/listen-eps/all_questions.csv → xóa gen_temp*.json

QC: explain không trap/emoji, xuống dòng rõ, "Người nam:"/"Người nữ:", q_correct phân bố đều 1-4

## Danh sách gen (mặc định 1 bài/dạng)

310001, 310002, 310003, 310004, 310005, 310006, 3410002, 3410005
