Đọc skill `skills/topik-write-gen-origin/SKILL.md` + tất cả file trong `kinds/` + `samples.json`.

Gen **1 câu mỗi kind** (4 câu). Tuân theo đúng JSON format, chiến lược bẫy, q_image_description (kind 230001), g_image_description (kind 230002), count_question theo từng file kind. Chủ đề đa dạng, q_correct phân bố đều 1-4, explain ghi chú trap type cho từng đáp án sai.

Sau khi gen xong, validate rồi lưu bằng script `skills/topik-write-gen-origin/scripts/save_write.py` vào `output/write-origin`.
