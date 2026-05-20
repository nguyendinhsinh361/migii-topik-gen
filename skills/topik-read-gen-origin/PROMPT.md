Đọc skill `skills/topik-read-gen-origin/SKILL.md` + tất cả file trong `kinds/` + `samples.json`.

Gen **1 câu mỗi kind** (32 câu). Tuân theo đúng JSON format, chiến lược bẫy, answer_grammar, q_image_description (kind ảnh), count_question=2 (kind multi) trong từng file kind. Chủ đề đa dạng, q_correct phân bố đều 1-4, explain ghi chú trap type cho từng đáp án sai.

Sau khi gen xong, validate rồi lưu bằng script `skills/topik-read-gen-origin/scripts/save_read.py` vào `output/read-origin`.
