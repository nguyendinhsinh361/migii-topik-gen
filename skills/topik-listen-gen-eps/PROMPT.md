## Workflow gen câu hỏi EPS-TOPIK Listen

> Skill nằm tại: `skills/topik-listen-gen-eps/`

### Bước 1: Đọc tài liệu
- Đọc `skills/topik-listen-gen-eps/SKILL.md` để nắm JSON format, hệ thống nhãn, quy tắc chung
- Đọc **file kind mà user yêu cầu** trong `skills/topik-listen-gen-eps/kinds/` — ví dụ `kinds/310001.md`, `kinds/3410002.md`. Mỗi kind có cấu trúc audio, chiến lược bẫy riêng. Nếu user không chỉ định, hỏi lại hoặc gen 1 câu/kind
- Đọc `skills/topik-listen-gen-eps/samples.json` — tìm đúng kind cần gen, xem **ít nhất 2 mẫu** để nắm phong cách output
- **Danh sách kind khả dụng**: 310001, 310002, 310003, 310004, 310005, 310006, 3410002, 3410005

### Bước 2: Gen câu hỏi
- Số lượng: theo user yêu cầu. Nếu không nói, **mặc định 5 câu/kind**
- Tuân theo **đúng JSON format** trong SKILL.md
- `g_text_audio`: viết nội dung transcript hội thoại hoặc monolog tùy kind. **KHÔNG nhầm với `g_audio`** — `g_audio` chứa URL file mp3, để trống khi gen
- Với kind có **ảnh** (310002, 310003, 3410002): viết `q_image_description` chi tiết theo hướng dẫn trong kind file
- Chủ đề ưu tiên bối cảnh EPS: nhà máy, ký túc xá, an toàn lao động

### Bước 3: Áp dụng chiến lược bẫy
- Mỗi kind file liệt kê các `trap_*` với **tỷ lệ %** — đây là xác suất **mỗi đáp án sai** dùng trap đó (tổng có thể >100% vì 1 câu có 3 đáp án sai, mỗi đáp án chọn 1 trap)
- Ghi chú trap type cho **từng đáp án sai** trong trường `explain`
- Kind 310001: BẮT BUỘC `trap_sound_similarity` (100%)
- Kind 310006: BẮT BUỘC `trap_same_ending`

### Bước 4: Kiểm tra chất lượng
- `q_correct` phân bố đều 1-4
- `answer_grammar` khớp đúng code trong kind file
- Chủ đề **đa dạng**, ưu tiên bối cảnh EPS (công việc, đời sống lao động)
- Ngữ pháp đơn giản, phù hợp trình độ EPS-TOPIK

### Bước 5: Lưu kết quả
- Validate JSON format trước khi lưu
- Chạy script: `python skills/topik-listen-gen-eps/scripts/save_listen.py` với input là JSON array
- Output lưu vào `output/listen-eps/`
