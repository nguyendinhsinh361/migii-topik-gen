---
name: topik-write-qc
description: QC dữ liệu TOPIK Viết. Đọc CSV, kiểm tra toàn bộ tiêu chí, tự động sửa lỗi, lặp đến 0 lỗi.
---

# TOPIK Write QC — Kiểm tra & sửa lỗi dữ liệu viết

Skill QC tách biệt hoàn toàn với skill gen. Đọc CSV đã gen, kiểm tra **toàn bộ tiêu chí** (từ file kind tương ứng trong folder `kinds/` + bảng tham chiếu bên dưới), tự động sửa lỗi, lặp đến khi đạt.

## Khi nào dùng skill này
- Khi user yêu cầu QC / kiểm tra / sửa lỗi dữ liệu viết
- Sau khi gen xong câu hỏi viết, cần QC trước khi gửi BTV

## Đầu vào
- File CSV: `output/write-origin/all_questions.csv` (hoặc file CSV user chỉ định)

## Bước 0: Đọc quy tắc trước khi QC (BẮT BUỘC)

Trước khi bắt đầu QC, agent **PHẢI**:
1. Đọc file kind tương ứng trong folder `kinds/` của skill này — `kinds/{kind}.md` — lấy quy tắc riêng của từng kind đang QC (cấu trúc câu hỏi, quy luật tạo đáp án, chiến lược bẫy, nhãn hệ thống, yêu cầu biểu đồ/ảnh, bài viết mẫu)
2. Đọc bảng tham chiếu bên dưới — lấy toàn bộ quy tắc chung, bảng nhãn, giải thích format

Mọi tiêu chí ghi trong kind file và bảng tham chiếu đều là tiêu chí QC. Danh sách checks bên dưới là **tóm tắt** để dễ check tự động, nhưng KHÔNG thay thế việc đọc kind file.

## Workflow

1. Đọc CSV bằng pandas
2. Với **mỗi dòng**:
   a. Xác định `kind`
   b. Đọc `kinds/{kind}.md` (quy tắc riêng)
   c. Đối chiếu bảng tham chiếu (quy tắc chung)
   d. Chạy tất cả QC checks (xem bên dưới)
   e. Nếu lỗi → sửa trực tiếp trong DataFrame
3. Lưu CSV đã sửa
4. Đọc lại → chạy QC lần 2 → lặp đến khi **0 lỗi**
5. Xuất báo cáo tổng hợp

---

## Danh sách QC checks

### Nhóm 1: Metadata & Consistency

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| MC-1 | `tag` = "write" | Exact match | ✅ |
| MC-2 | `level` = 2 | Write chỉ có TOPIK II | ✅ |
| MC-3 | `kind` hợp lệ | Phải là 230001_1, 230001_2, 230002, hoặc 230003 | ❌ báo cáo |
| MC-4 | `count_question` khớp | 230001: 1, 230002: 3, 230003: 10 | ✅ |
| MC-5 | `q_correct` là integer trong 1-4 (KHÔNG float 1.0, 2.0) | Với mỗi q_correct_N: phải là integer, nếu float → convert int() | ✅ clamp + int() |
| MC-6 | 4 đáp án không trùng | Parse q_answer_N, check unique | ❌ cần LLM |
| MC-7 | **`q_correct` phân bố đều 1-4** | Trong cùng batch (cùng kind), q_correct PHẢI phân bố đều qua 1-4. KHÔNG được thiên lệch (vd: tất cả = 1). Nếu gen 4 câu cùng kind → phải có q_correct = 1, 2, 3, 4 (mỗi giá trị 1 lần). Nếu lệch → shuffle lại q_correct và swap đáp án tương ứng | ✅ shuffle & swap |
| MC-8 | `topic` hợp lệ | Phù hợp loại kind | ✅ |
| MC-9 | `question_feature` hợp lệ | Theo bảng tham chiếu. 230003: câu 1-4 `qf_fill_word`, câu 5-10 `qf_content_match` | ✅ |
| MC-10 | `difficulty` hợp lệ | Theo bảng tham chiếu | ✅ |

### Nhóm 2: Đề bài (g_text)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| GT-1 | **230003: g_text không lẫn tiếng Trung** | Regex `[一-鿿]` (CJK Unified Ideographs) | ❌ cần LLM |
| GT-2 | **230003: g_text 3 phần BẮT BUỘC** | Phải có: dẫn nhập xã hội → chủ đề nghị luận → 3 câu hỏi gợi ý. Đọc kind file | ❌ cần LLM |
| GT-3 | **230002: g_text KHÔNG chứa tên biểu đồ** | g_text KHÔNG ghi "국내 캠핑 인구 현황과 전망" hay tương tự | ✅ check |
| GT-4 | **g_text tiếng Hàn tự nhiên** | Ngữ pháp đúng, văn phong phù hợp level | ❌ cần LLM |

### Nhóm 3: Hình ảnh & Biểu đồ

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| IM-1 | **230001_2: KHÔNG cần ảnh** | q_image_1 phải rỗng | ✅ xóa |
| IM-2 | **230001_1: ảnh khớp đáp án** | q_image_desc_1 phải mô tả nội dung khớp q_answer_1. Xung quanh chỗ trống phải có từ gợi ý | ❌ cần LLM |
| IM-3 | **230002: chỉ 1 ảnh chung** | Ảnh ở g_image. q_image_1, q_image_2, q_image_3 phải rỗng | ✅ xóa |
| IM-4 | **230002: biểu đồ đơn giản** | Ít số liệu, chỉ số quan trọng. Triển vọng/nguyên nhân 1-2 ý. KHÔNG có 주요 트렌드. Dùng ký hiệu ⮕⬆⬇ | ❌ cần LLM |
| IM-5 | **230001_1: phong cách ảnh** | Đọc kind file → phong cách hình ảnh (khung email, grayscale...) | ❌ cần LLM |
| IM-6 | **230002: g_image_desc template** | Mô tả ảnh lưu trong `g_image_desc` (KHÔNG phải q_image_desc). Phải theo format template BẮT BUỘC trong kind file (loại biểu đồ, tiêu đề, nguồn, trục, dữ liệu...) | ❌ cần LLM |

### Nhóm 4: Đáp án (q_answer)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| AN-1 | **Quy luật tạo đáp án 230001** | Tổ hợp 2×2: (ㄱ) A/B × (ㄴ) C/D. Phải theo 1 trong 2 kiểu sắp xếp. Đọc kind file | ❌ cần LLM |
| AN-2 | **230003 câu 9-10: phân bố 2-2** | 4 vị trí đầu phân bố 2-2 (e.g. 2× (다), 2× (라)) | ❌ cần LLM |
| AN-3 | **answer_grammar đúng kind** | Xem bảng tham chiếu → answer_grammar | ❌ cần LLM |
| AN-4 | **Trap distribution** | Đọc kind file → chiến lược bẫy → distractor_trap khớp | ❌ cần LLM |
| AN-5 | **230002 Q3: chọn SAI** | content[2] (Q3) phải là "chọn câu SAI" — 3 đáp án đúng, 1 đáp án sai | ❌ cần LLM |

### Nhóm 5: Giải thích (explain)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| EX-1 | **Không chứa mã trap** | Regex `trap_[a-z_]+` trong explain_vi_*, explain_en_*. Explain dành cho người học | ✅ xóa |
| EX-2 | **EN chi tiết bằng VI** | len(explain_en) >= 50% len(explain_vi) | ❌ cần LLM |
| EX-3 | **VI và EN cùng cấu trúc** | Cả 2: dịch câu hỏi → dịch đáp án → separator ---- → giải thích. KHÔNG để EN ngắn gọn kiểu "=> Answer 1" | ❌ cần LLM |
| EX-4 | **Giải thích dễ hiểu** | Ngôn ngữ cho người học, giải thích tại sao đúng/sai bằng ngôn ngữ tự nhiên | ❌ cần LLM |
| EX-5 | **Không icon/emoji** | Regex `[✅❌✓✗☑☐⬜⬛🔴🟢]` trong explain | ✅ xóa |
| EX-6 | **Trích dẫn Hàn giữ nguyên** | Explain phải giữ nguyên từ/cụm tiếng Hàn trong ngoặc, KHÔNG dịch | ❌ cần LLM |
| EX-7 | **Explain xuống dòng rõ ràng** | Explain PHẢI có line breaks (`\n`) rõ ràng giữa các phần: dịch câu hỏi, dịch đáp án (1. 2. 3. 4.), separator (----), dịch nội dung, giải thích từng đáp án. KHÔNG được viết thành 1 đoạn dài liền mạch. Mỗi đáp án giải thích trên 1 dòng riêng. Check: đếm số `\n` trong explain — nếu < 6 thì khả năng cao bị viết liền | ❌ cần LLM |

### Nhóm 6: Bài viết mẫu (examples)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| XP-1 | **230002/230003 có đủ 5 examples** | example_1 đến example_5 không rỗng | ❌ cần LLM |
| XP-2 | **Độ dài example** | 230002: 200-300 ký tự. 230003: 600-700 ký tự | ❌ cần LLM |
| XP-3 | **Example đúng nội dung** | 230002: mô tả chính xác dữ liệu biểu đồ (nhất quán q_image_desc). 230003: trả lời 3 câu hỏi gợi ý | ❌ cần LLM |
| XP-4 | **5 bài khác nhau** | 5 bài có cách diễn đạt/góc nhìn/lập luận khác nhau | ❌ cần LLM |
| XP-5 | **Cấu trúc bài viết** | 230002: giới thiệu → so sánh → xu hướng → kết luận. 230003: mở bài → thân bài → kết bài | ❌ cần LLM |

### Nhóm 7: Quy tắc riêng từ kind file (catch-all)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| KF-1 | **Mọi "Quy tắc bắt buộc"** | Đọc phần "Quy tắc bắt buộc" trong kind file → check tất cả | ❌ cần LLM |
| KF-2 | **230002: số liệu nhất quán** | Số liệu trong q_image_desc PHẢI khớp đáp án đúng trong content[] | ❌ cần LLM |

---

## Quy tắc sửa lỗi

### Lỗi sửa tự động:
MC-1, MC-2, MC-4, MC-5, MC-8, MC-9, MC-10, GT-3, IM-1, IM-3, EX-1, EX-5

### Lỗi cần LLM:
Tất cả lỗi còn lại. Khi viết lại:
- Đọc `kinds/{kind}.md` để lấy **tất cả** quy tắc riêng
- Đối chiếu bảng tham chiếu bên dưới để lấy quy tắc chung
- Giữ nguyên các trường khác, chỉ sửa trường lỗi

## Output
- CSV đã sửa (ghi đè file gốc)
- Báo cáo: số lỗi theo nhóm, số đã sửa, số cần xem lại

## Lưu ý
- Skill này **TÁCH BIỆT hoàn toàn** với skill gen — chỉ đọc và sửa CSV
- Folder `kinds/` chứa bản sao các kind files — dùng để tra cứu quy tắc khi QC
- Chỉ chỉnh CSV trong `output/`, KHÔNG chỉnh bất kỳ file nào khác

---

## Bảng tham chiếu

Tất cả thông tin dưới đây được trích từ quy tắc gen gốc. Dùng để tra cứu nhanh khi QC mà KHÔNG cần tham chiếu file bên ngoài.

### Kind hợp lệ

| Kind | Mô tả | Đề thi tương ứng |
|------|-------|-------------------|
| `230001_1` | Điền câu vào đoạn văn [51] (TOPIK II) | Câu 51 |
| `230001_2` | Điền câu vào đoạn văn [52] (TOPIK II) | Câu 52 |
| `230002` | Viết biểu đồ [53] (TOPIK II) [ảnh] | Câu 53 |
| `230003` | Trình bày quan điểm cá nhân [54] (TOPIK II) | Câu 54 |

### Thang độ khó (difficulty)

| Kind | difficulty | Mô tả |
|------|-----------|-------|
| `230001_1` | 1 | `fill_blank_easy` — Điền câu vào đoạn văn đơn giản |
| `230001_2` | 2 | `fill_blank_medium` — Điền câu vào đoạn văn phức tạp hơn |
| `230002` | 3 | `chart_writing` — Phân tích biểu đồ và viết |
| `230003` | 4 | `opinion_writing` — Trình bày quan điểm cá nhân |

### Số câu hỏi (count_question)

| Kind | count_question |
|------|---------------|
| `230001_1` | 1 |
| `230001_2` | 1 |
| `230002` | 3 |
| `230003` | 10 |

### Đặc điểm câu hỏi (question_feature)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `qf_fill_blank_pair` | Fill Blank Pair | Chọn cặp (ㄱ)-(ㄴ) điền vào đoạn văn | 230001_1, 230001_2 |
| `qf_chart_comprehension` | Chart Comprehension | Hiểu biểu đồ, chọn mô tả đúng | 230002 |
| `qf_fill_word` | Fill Word | Chọn từ/ngữ pháp điền vào câu | 230003 (câu 1-4) |
| `qf_content_match` | Content Match | Chọn nội dung khớp với đề bài | 230003 (câu 5-10) |

### Ngữ pháp đáp án (answer_grammar)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `ans_sentence_pair` | Đáp án là cặp câu (ㄱ)-(ㄴ), mỗi câu 5-15 ký tự | 230001_1, 230001_2 |
| `ans_sentence_long` | Đáp án là câu dài (20+ ký tự) mô tả biểu đồ | 230002 |
| `ans_word_phrase` | Đáp án là từ/cụm từ ngắn | 230003 (câu 1-4) |
| `ans_sentence_medium` | Đáp án là câu trung bình (10-20 ký tự) | 230003 (câu 5-10) |

### Chiến lược bẫy đáp án sai (distractor_trap)

#### Nhóm 1: Bẫy ngữ pháp (Grammar Traps) — chủ yếu 230001

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_grammar_ending` | Wrong Ending | Sai dạng kết thúc câu (~습니다 vs ~세요) | 230001_1 |
| `trap_grammar_connector` | Wrong Connector | Dùng sai liên từ (~기 때문에 vs ~어서) | 230001_1, 230001_2, 230003 |
| `trap_grammar_tense` | Wrong Tense | Sai thì (quá khứ/hiện tại/tương lai) | 230001_2 |

#### Nhóm 2: Bẫy nội dung (Content Traps) — 230002, 230003

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_partial_truth` | Partial Truth | Đáp án sai chứa >50% nội dung đúng | 230001_1, 230001_2, 230002 |
| `trap_wrong_inference` | Wrong Inference | Suy luận hợp lý nhưng không có trong dữ liệu | 230001_2, 230002, 230003 |
| `trap_number_shift` | Number/Time Shift | Thay đổi số liệu biểu đồ | 230002 |
| `trap_comparison_flip` | Comparison Flip | Đảo chiều so sánh trong biểu đồ | 230002 |
| `trap_cause_effect_swap` | Cause-Effect Swap | Đảo quan hệ nhân quả | 230002 |
| `trap_overgeneralize` | Overgeneralization | Khái quát hóa quá mức | 230002, 230003 |
| `trap_synonym_swap` | Synonym Swap | Thay từ đồng nghĩa/gần nghĩa nhưng sai sắc thái | 230003 |

### Danh mục chủ đề (topic)

| Code | Nhãn tiếng Anh | Tiếng Hàn | Kind thường gặp |
|------|---------------|-----------|----------------|
| `daily_life` | Daily Life & Routine | 일상생활 | 230001_1 |
| `school_education` | School & Education | 학교/교육 | 230001_1, 230001_2 |
| `economy_business` | Economy & Business | 경제/산업 | 230002 |
| `environment_society` | Environment & Society | 환경/사회 | 230002, 230003 |
| `science_tech` | Science & Technology | 과학/기술 | 230002, 230003 |
| `culture_event` | Culture & Events | 문화/행사 | 230002, 230003 |
| `psychology_behavior` | Psychology & Behavior | 심리/행동 | 230003 |
| `language_expression` | Language & Expression | 언어/표현 | 230001_2, 230003 |

### Format giải thích (explain)

Format explain.vi va explain.en PHAI GIONG NHAU ve cau truc — chi khac ngon ngu:

```
[Dich cau hoi / mo ta yeu cau]

1. [Dich dap an 1]
2. [Dich dap an 2]
3. [Dich dap an 3]
4. [Dich dap an 4]
----------------------------
[Dich/tom tat noi dung bai viet / doan van lien quan]

Dap an [N] la dap an dung vi [ly do].
Dap an [X] sai vi [ly do].
Dap an [Y] sai vi [ly do].
Dap an [Z] sai vi [ly do].
```

- **Format explain PHAI xuong dong ro rang** — moi phan (dich cau hoi, dich dap an, separator, dich noi dung, giai thich tung dap an) PHAI xuong dong (`\n`). KHONG viet thanh 1 doan dai lien mach. Moi dap an giai thich tren 1 dong rieng.
- **vi** va **en** phai co **cung so phan** va **cung muc chi tiet**
- KHONG de en ngan gon kieu "=> Answer 1" ma vi thi giai thich dai dong
- Ca vi lan en deu phai giai thich **tung dap an sai** vi sao sai
