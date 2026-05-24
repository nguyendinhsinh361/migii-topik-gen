## Workflow gen câu hỏi TOPIK Read Origin

> Skill nằm tại: `skills/topik-read-gen-origin/`

### Bước 1: Đọc tài liệu
- Đọc `skills/topik-read-gen-origin/SKILL.md` để nắm JSON format, hệ thống nhãn, quy tắc chung
- Đọc **file kind mà user yêu cầu** trong `skills/topik-read-gen-origin/kinds/` — ví dụ `kinds/120001.md`, `kinds/220006.md`. Mỗi kind có cấu trúc riêng, chiến lược bẫy riêng. Nếu user không chỉ định kind cụ thể, hỏi lại hoặc gen đại diện 1 câu/kind
- Đọc `skills/topik-read-gen-origin/samples.json` — tìm đúng kind cần gen, xem **ít nhất 2 mẫu** để nắm phong cách output
- **Danh sách kind khả dụng (TOPIK I)**: 120001, 120002_1, 120002_2, 120002_3, 120002_4, 120003_1, 120003_2, 120004_1, 120004_2, 120005, 120005_1, 120006, 120007_1, 120007_2, 120007_3
- **Danh sách kind khả dụng (TOPIK II)**: 220001_a, 220001_b, 220001_c, 220002_a, 220002_b_1, 220002_b_2, 220002_b_3, 220002_c, 220003_a_1, 220003_a_2, 220003_b, 220004, 220005_1, 220005_2, 220006, 220007, 220008_1, 220008_2

### Bước 2: Gen câu hỏi
- Số lượng: theo user yêu cầu. Nếu không nói, **mặc định 5 câu/kind**
- Tuân theo **đúng JSON format** trong SKILL.md (các trường: kind, title, g_text, g_image, g_audio, content, explain, q_image_description)
- Với kind có **count_question = 2**: tạo 2 câu hỏi con trong mảng `content[]`
- Với kind có **ảnh** (q_image_description hoặc g_image_description): viết mô tả hình ảnh chi tiết theo phong cách trong kind file
- Các trường metadata (`topic`, `difficulty`, `question_feature`, `distractor_traps`) chỉ cần điền nếu kind file yêu cầu — KHÔNG bắt buộc

### Bước 3: Áp dụng chiến lược bẫy
- Mỗi kind file liệt kê các `trap_*` với **tỷ lệ %** — đây là xác suất **mỗi đáp án sai** dùng trap đó (tổng có thể >100% vì 1 câu có 3 đáp án sai, mỗi đáp án chọn 1 trap)
- Ghi chú trap type cho **từng đáp án sai** trong trường `explain`
- Ví dụ explain: `"① trap_subject_swap (혼자→친구와), ② đúng, ③ trap_detail_distort (수영→등산), ④ trap_neg_없안"`
- Đáp án sai PHẢI dùng lại từ vựng bài đọc khi kind yêu cầu `trap_shared_noun`

### Bước 4: Kiểm tra chất lượng
- `q_correct` phân bố đều 1-4 trên toàn bộ batch (không thiên lệch)
- `answer_grammar` khớp đúng code trong kind file (ans_noun_phrase, ans_sentence_plain, ...)
- Chủ đề **đa dạng** — không lặp chủ đề giữa các câu cùng kind
- Với kind 120007_1/2/3: content[0] và content[1] PHẢI hỏi khía cạnh KHÁC nhau
- Kiểm tra ngữ pháp Hàn: đúng trình độ (TOPIK I hoặc TOPIK II tùy kind)

### Bước 5: Lưu kết quả
- Validate JSON format trước khi lưu
- Chạy script: `python skills/topik-read-gen-origin/scripts/save_read.py` với input là JSON array
- Output lưu vào `output/read-origin/`
