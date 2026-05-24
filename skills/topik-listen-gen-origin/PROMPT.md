## Workflow gen câu hỏi TOPIK Listen Origin

> Skill nằm tại: `skills/topik-listen-gen-origin/`

### Bước 1: Đọc tài liệu
- Đọc `skills/topik-listen-gen-origin/SKILL.md` để nắm JSON format, hệ thống nhãn, quy tắc chung
- Đọc **file kind mà user yêu cầu** trong `skills/topik-listen-gen-origin/kinds/` — ví dụ `kinds/110001.md`, `kinds/210003.md`. Mỗi kind có cấu trúc audio, speech_level, chiến lược bẫy riêng. Nếu user không chỉ định kind cụ thể, hỏi lại hoặc gen đại diện 1 câu/kind
- Đọc `skills/topik-listen-gen-origin/samples.json` — tìm đúng kind cần gen, xem **ít nhất 2 mẫu** để nắm phong cách output
- **Danh sách kind khả dụng**: 110001, 110002, 110003, 110004, 110005, 110006, 110007, 110008_1, 110008_2, 110008_3, 210001_1, 210001_2, 210002, 210003, 210004, 210005, 210006, 210007

### Bước 2: Gen câu hỏi
- Số lượng: theo user yêu cầu. Nếu không nói, **mặc định 5 câu/kind**
- Tuân theo **đúng JSON format** trong SKILL.md
- `g_text_audio`: viết nội dung transcript hội thoại (`남자: ...\n여자: ...`) hoặc monolog tùy kind. **KHÔNG nhầm với `g_audio`** — `g_audio` chứa URL file mp3, để trống khi gen
- `speech_level`: dùng đúng level trong kind file (informal_polite cho audio, formal_polite cho đáp án)
- Với kind có **ảnh** (110005, 210001_1, 210001_2): viết `q_image_description` chi tiết theo hướng dẫn trong kind file
- Các trường metadata (`topic`, `difficulty`, `question_feature`, `distractor_traps`) chỉ cần điền nếu kind file yêu cầu — KHÔNG bắt buộc

### Bước 3: Áp dụng chiến lược bẫy
- Mỗi kind file liệt kê các `trap_*` với **tỷ lệ %** — đây là xác suất **mỗi đáp án sai** dùng trap đó (tổng có thể >100% vì 1 câu có 3 đáp án sai, mỗi đáp án chọn 1 trap)
- Ghi chú trap type cho **từng đáp án sai** trong trường `explain`
- Ví dụ explain: `"① trap_subject_swap (여자→남자), ② đúng, ③ trap_detail_distort (도서관→학교), ④ trap_neg_없안"`
- Kind 110006: BẮT BUỘC `trap_subject_swap` (≥2/3 đáp án sai gán sai người) + `trap_same_ending`
- Kind 110007: BẮT BUỘC có sự khác biệt quan điểm nam/nữ + `trap_opinion_swap`

### Bước 4: Kiểm tra chất lượng
- `q_correct` phân bố đều 1-4 trên toàn bộ batch (không thiên lệch)
- `answer_grammar` khớp đúng code trong kind file (ans_noun_phrase, ans_sentence_plain, ...)
- Chủ đề **đa dạng** — không lặp chủ đề giữa các câu cùng kind
- Hội thoại phải tự nhiên, phù hợp ngữ cảnh Hàn Quốc
- Kiểm tra ngữ pháp: đúng trình độ TOPIK I

### Bước 5: Lưu kết quả
- Validate JSON format trước khi lưu
- Chạy script: `python skills/topik-listen-gen-origin/scripts/save_listen.py` với input là JSON array
- Output lưu vào `output/listen-origin/`
