## Workflow gen câu hỏi EPS-TOPIK Read

> Skill nằm tại: `skills/topik-read-gen-eps/`

### Bước 1: Đọc tài liệu
- Đọc `skills/topik-read-gen-eps/SKILL.md` để nắm JSON format, hệ thống nhãn, quy tắc chung
- Đọc **file kind mà user yêu cầu** trong `skills/topik-read-gen-eps/kinds/` — ví dụ `kinds/320001.md`, `kinds/3420007.md`. Mỗi kind có cấu trúc riêng. Nếu user không chỉ định, hỏi lại hoặc gen 1 câu/kind
- Đọc `skills/topik-read-gen-eps/samples.json` — tìm đúng kind cần gen, xem **ít nhất 2 mẫu** để nắm phong cách output
- **Danh sách kind khả dụng**: 320001, 320002, 320003, 320004, 320005, 3420002, 3420003, 3420006, 3420007, 3420008

### Bước 2: Gen câu hỏi
- Số lượng: theo user yêu cầu. Nếu không nói, **mặc định 5 câu/kind**
- Tuân theo **đúng JSON format** trong SKILL.md
- Với kind có **ảnh** (320001, 320003, 320004): viết `q_image_description` chi tiết theo hướng dẫn trong kind file
- Chủ đề ưu tiên bối cảnh EPS: nhà máy, ký túc xá, an toàn lao động, hợp đồng

### Bước 3: Áp dụng chiến lược bẫy
- Mỗi kind file liệt kê các `trap_*` với **tỷ lệ %** — đây là xác suất **mỗi đáp án sai** dùng trap đó (tổng có thể >100% vì 1 câu có 3 đáp án sai, mỗi đáp án chọn 1 trap)
- Ghi chú trap type cho **từng đáp án sai** trong trường `explain`
- Kind 320001/3420001: BẮT BUỘC 4 đáp án cùng nhóm ngữ nghĩa
- Kind 320002 (gồm 3420004): BẮT BUỘC dùng format hội thoại 가/나 — file `kinds/320002.md` cover cả 2 kind code

### Bước 4: Kiểm tra chất lượng
- `q_correct` phân bố đều 1-4
- `answer_grammar` khớp đúng code trong kind file
- Chủ đề **đa dạng**, ưu tiên bối cảnh EPS
- Ngữ pháp đơn giản, phù hợp trình độ EPS-TOPIK

### Bước 5: Lưu kết quả
- Validate JSON format trước khi lưu
- Chạy script: `python skills/topik-read-gen-eps/scripts/save_read.py` với input là JSON array
- Output lưu vào `output/read-eps/`
