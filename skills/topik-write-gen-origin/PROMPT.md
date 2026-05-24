## Workflow gen câu hỏi TOPIK Write Origin

> Skill nằm tại: `skills/topik-write-gen-origin/`

### Bước 1: Đọc tài liệu
- Đọc `skills/topik-write-gen-origin/SKILL.md` để nắm JSON format, hệ thống nhãn, quy tắc chung
- Đọc **file kind mà user yêu cầu** trong `skills/topik-write-gen-origin/kinds/` — mỗi kind có cấu trúc riêng (230001_1/2 = điền câu, 230002 = biểu đồ, 230003 = luận). Nếu user không chỉ định, hỏi lại hoặc gen 1 câu/kind
- Đọc `skills/topik-write-gen-origin/samples.json` — tìm đúng kind cần gen, xem **ít nhất 2 mẫu** để nắm phong cách output
- **Danh sách kind khả dụng**: 230001_1, 230001_2, 230002, 230003

### Bước 2: Gen câu hỏi
- Số lượng: theo user yêu cầu. Nếu không nói, **mặc định 5 câu/kind**
- Tuân theo **đúng JSON format** trong SKILL.md
- Kind 230001_1: `q_image_description` mô tả email/thư mời với ㉠㉡ chỗ trống
- Kind 230002: `q_image_description` mô tả biểu đồ/infographic chi tiết — **PHẢI theo template**:
  ```
  Loại biểu đồ: [막대/선/원 그래프]
  Tiêu đề: [제목]
  Trục X: [nhãn, đơn vị]
  Trục Y: [nhãn, đơn vị]
  Dữ liệu: [năm: giá trị, năm: giá trị, ...]
  Xu hướng: [tăng/giảm/ổn định]
  Phát hiện chính: [mô tả ngắn]
  ```
- Kind 230003: `g_text` là đoạn văn luận điểm 200-300 ký tự
- `count_question` theo từng kind file (1 hoặc 2)

### Bước 3: Áp dụng chiến lược bẫy
- Mỗi kind file liệt kê các `trap_*` — **BẮT BUỘC** áp dụng
- Tỷ lệ % = xác suất **mỗi đáp án sai** dùng trap đó (tổng có thể >100%)
- Ghi chú trap type cho **từng đáp án sai** trong trường `explain`
- Kind 230001: ưu tiên `trap_grammar_ending`, `trap_grammar_connector`
- Kind 230002: ưu tiên `trap_number_shift`, `trap_comparison_flip`
- Kind 230003: ưu tiên `trap_wrong_inference`, `trap_overgeneralize`

### Bước 4: Kiểm tra chất lượng
- `q_correct` phân bố đều 1-4
- `answer_grammar` khớp đúng code trong kind file
- Chủ đề **đa dạng**
- Ngữ pháp TOPIK II: ~(으)므로, ~는 반면, ~(으)ㄹ 뿐만 아니라
- Biểu đồ: số liệu nhất quán giữa q_image_description và đáp án

### Bước 5: Lưu kết quả
- Validate JSON format trước khi lưu
- Chạy script: `python skills/topik-write-gen-origin/scripts/save_write.py` với input là JSON array
- Output lưu vào `output/write-origin/`
