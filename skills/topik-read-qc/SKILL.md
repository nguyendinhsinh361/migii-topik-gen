---
name: topik-read-qc
description: QC dữ liệu TOPIK Đọc. Đọc CSV, kiểm tra toàn bộ tiêu chí, tự động sửa lỗi, lặp đến 0 lỗi.
---

# TOPIK Read QC — Kiểm tra & sửa lỗi dữ liệu đọc

Skill QC hoàn toàn tách biệt với skill gen. Đọc CSV đã gen, kiểm tra **toàn bộ tiêu chí** dựa trên file kind trong folder `kinds/` của skill này + bảng tham chiếu bên dưới, tự động sửa lỗi, lặp đến khi đạt.

## Khi nào dùng skill này
- Khi user yêu cầu QC / kiểm tra / sửa lỗi dữ liệu đọc
- Sau khi gen xong câu hỏi đọc, cần QC trước khi gửi BTV

## Đầu vào
- File CSV: `output/read-origin/all_questions.csv` (hoặc file CSV user chỉ định)

## Bước 0: Đọc quy tắc trước khi QC (BẮT BUỘC)

Trước khi bắt đầu QC, agent **PHẢI**:
1. Đọc file kind tương ứng trong folder `kinds/` của skill này: `kinds/{kind}.md` — lấy quy tắc riêng của từng kind đang QC (cấu trúc bài đọc, cấu trúc câu hỏi phụ, cấu trúc đáp án, quy tắc bắt buộc, chiến lược bẫy, nhãn hệ thống)
2. Đọc **bảng tham chiếu bên dưới** — lấy toàn bộ bảng topic, trap, question_feature, difficulty, answer_grammar

Mọi tiêu chí ghi trong file kind + bảng tham chiếu đều là tiêu chí QC. Danh sách checks bên dưới là **tóm tắt** để dễ check tự động, nhưng KHÔNG thay thế việc đọc file kind.

## Workflow

1. Đọc **bảng tham chiếu** (phần cuối file SKILL.md này — ghi nhớ các bảng/quy tắc)
2. Đọc CSV bằng pandas
3. Với **mỗi dòng**:
   a. Xác định `kind`
   b. Đọc `kinds/{kind}.md` (quy tắc riêng)
   c. Chạy tất cả QC checks (xem bên dưới)
   d. Nếu lỗi → sửa trực tiếp trong DataFrame
4. Lưu CSV đã sửa
5. Đọc lại → chạy QC lần 2 → lặp đến khi **0 lỗi**
6. Xuất báo cáo tổng hợp

---

## Danh sách QC checks

### Nhóm 1: Metadata & Consistency

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| MC-1 | `tag` = "read" | Exact match | ✅ |
| MC-2 | `level` hợp lệ | 120xxx → 1, 220xxx → 2 | ✅ |
| MC-3 | `kind` hợp lệ | Tồn tại file `kinds/{kind}.md` | ❌ báo cáo |
| MC-4 | `count_question` khớp | Đếm số q_text_N có dữ liệu. Phải khớp giá trị trong kind file | ✅ |
| MC-5 | `q_correct` trong 1-4 | Với mỗi q_correct_N | ✅ clamp |
| MC-6 | 4 đáp án không trùng | Parse q_answer_N, check unique | ❌ cần LLM |
| MC-7 | `topic` hợp lệ | Thuộc danh sách topic trong bảng tham chiếu bên dưới | ✅ |
| MC-8 | `question_feature` hợp lệ | Thuộc danh sách qf_* trong bảng tham chiếu, phù hợp kind. Xem bảng nhãn hệ thống trong kind file | ✅ |
| MC-9 | `difficulty` hợp lệ | Theo bảng Thang độ khó trong bảng tham chiếu | ✅ |
| MC-10 | `distractor_trap` hợp lệ | Mã trap phải thuộc danh sách trong bảng tham chiếu, phù hợp kind (xem bảng chiến lược bẫy trong kind file) | ❌ cần LLM |
| MC-11 | **q_correct phân bố đều 1-4 (TẤT CẢ levels)** | Trong cùng batch (cùng kind), q_correct PHẢI phân bố đều qua 1-4 cho TẤT CẢ levels (TOPIK I, TOPIK II). KHÔNG fix cứng q_correct = 1 cho bất kỳ level nào. Nếu gen 4 câu cùng kind → phải có q_correct = 1, 2, 3, 4 (mỗi giá trị 1 lần). Nếu lệch → shuffle lại q_correct và swap đáp án tương ứng | ✅ shuffle & swap |

### Nhóm 2: Bài đọc (g_text / q_text)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| TX-1 | **Độ dài bài đọc** theo kind | Đọc kind file → lấy mục tiêu ký tự. Tolerance ±15%. Ví dụ: 220001_b q_text ~200, 220001_c q_text ~250, 220005_2 g_text ~450, 220008_1_(1) g_text ~600, 220008_2 g_text ~500, 120005_(1) g_text ~140-150, 120007_1 g_text ~180-220 | ❌ cần LLM |
| TX-2 | **Vị trí bài đọc** theo kind | Xem kind file. Ví dụ: 220007 passage phải ở q_text_1 (KHÔNG phải g_text) | ❌ cần LLM |
| TX-3 | **Bài đọc tiếng Hàn tự nhiên** | Không lẫn tiếng khác, ngữ pháp đúng level | ❌ cần LLM |

### Nhóm 3: Cấu trúc đặc biệt theo kind

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| SK-1 | **220005_2: ngôi thứ nhất + `<u>`** | g_text viết ở ngôi 나, có `<u></u>`, KHÔNG có `(  )`. content[0] q_text = "밑줄 친 부분에 나타난 '나'의 심정으로...". content[1] q_text = "윗글의 내용과 같은 것을..." | ❌ cần LLM |
| SK-2 | **220008_1_(3): KHÔNG `<u>`, thái độ toàn đoạn** | g_text KHÔNG có `<u></u>`. content[0] q_text = "윗글에 나타난 필자의 태도로..." | ✅ check tag |
| SK-3 | **220008_2: KHÔNG `<b>`** | g_text KHÔNG có `<b></b>` | ✅ xóa tag |
| SK-4 | **220007: passage ở q_text, bỏ `<보기>`** | q_text_1 chứa passage, KHÔNG có `<보기>`. Câu cần chèn nằm dưới đoạn văn | ❌ cần LLM |
| SK-5 | **120007_1: q_answer format** | q_answer dùng ㉠ ㉡ ㉢ ㉣ (KHÔNG ngoặc đơn "( ㉠ )") | ✅ replace |
| SK-6 | **220008_1_(1): g_text_vi giữ `<u>`** | g_text_vi phải preserve thẻ `<u></u>` từ g_text | ✅ check |
| SK-7 | **Nhãn hệ thống** theo kind | question_feature, text_format, answer_grammar phải khớp bảng trong kind file | ✅ |
| SK-8 | **Mọi quy tắc bắt buộc** trong kind file | Đọc phần "Quy tắc bắt buộc" trong kind file → check tất cả | ❌ cần LLM |

### Nhóm 4: Đáp án (q_answer)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| AN-1 | **answer_grammar đúng kind** | Xem bảng answer_grammar trong bảng tham chiếu + kind file. Ví dụ: 220005_2 content[0] → tính từ cảm xúc, content[1] → câu hoàn chỉnh ~30 ký tự | ❌ cần LLM |
| AN-2 | **Trap distribution** | Đọc kind file → bảng chiến lược bẫy → distractor_trap khớp | ❌ cần LLM |
| AN-3 | **Quy luật tạo đáp án** | Đọc kind file → phần "Quy luật tạo đáp án" nếu có (e.g. tổ hợp 2×2, phân bố 2-2 vị trí đầu) | ❌ cần LLM |

### Nhóm 5: Giải thích (explain)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| EX-1 | **Không chứa mã trap** | Regex `trap_[a-z_]+` trong explain_vi_*, explain_en_* | ✅ xóa |
| EX-2 | **EN chi tiết bằng VI** | len(explain_en) >= 50% len(explain_vi). explain_en KHÔNG chỉ là trap labels | ❌ cần LLM |
| EX-3 | **Câu ghép: dịch câu hỏi phụ** | Nếu count_question >= 2: explain phải chứa bản dịch q_text. KHÔNG để nguyên tiếng Hàn | ❌ cần LLM |
| EX-4 | **Câu có ảnh: dịch text ảnh đúng** | Chỉ dịch text hiển thị trên ảnh (tiêu đề, số liệu), KHÔNG dịch nguyên văn q_image_desc. Mỗi ý xuống dòng | ❌ cần LLM |
| EX-5 | **220004: KHÔNG viết lại q_answer** | explain KHÔNG liệt kê lại 4 đáp án | ✅ check |
| EX-6 | **220006: KHÔNG ngoặc kép** | q_text và bản dịch trong explain KHÔNG có "" bao quanh | ✅ xóa |
| EX-7 | **120006: KHÔNG "Thứ tự đúng"** | Regex `Thứ tự đúng:` hoặc `Correct order:` | ✅ xóa |
| EX-8 | **120007_1: KHÔNG liệt kê ㉠ trong explain** | Bỏ dòng "1. ( ㉠ ) 2. ( ㉡ )..." | ✅ xóa |
| EX-9 | **VI và EN cùng cấu trúc** | Cả 2: dịch đáp án → separator → giải thích. Cùng mức chi tiết | ❌ cần LLM |
| EX-10 | **120007_1/2/3: explain chi tiết** | explain phải giải thích đầy đủ logic, không đơn giản | ❌ cần LLM |
| EX-11 | **Không icon/emoji** | Regex `[✅❌✓✗☑☐⬜⬛🔴🟢]` trong explain | ✅ xóa |
| EX-12 | **Trích dẫn Hàn giữ nguyên** | Explain phải giữ nguyên từ/cụm tiếng Hàn trong ngoặc, KHÔNG dịch | ❌ cần LLM |
| EX-13 | **Explain xuống dòng rõ ràng** | Explain PHẢI có line breaks (`\n`) rõ ràng giữa các phần: dịch bài đọc, dịch đáp án (1. 2. 3. 4.), separator (----), giải thích từng đáp án. KHÔNG được viết thành 1 đoạn dài liền mạch. Mỗi đáp án giải thích trên 1 dòng riêng. Check: đếm số `\n` trong explain — nếu < 6 thì khả năng cao bị viết liền | ❌ cần LLM |

### Nhóm 6: Hình ảnh

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| IM-1 | **Kind có ảnh phải có q_image_desc** | Đọc kind file → nếu yêu cầu ảnh → q_image_desc không rỗng | ❌ cần LLM |
| IM-2 | **q_image_desc đúng format** | Đọc kind file → format mô tả ảnh | ❌ cần LLM |
| IM-3 | **220002_b_2: biểu đồ sắp lớn→nhỏ, đủ nhãn** | Segments sort descending, mỗi segment có nhãn | ❌ cần LLM |
| IM-4 | **120007_3: ảnh thông báo công cộng** | Đọc kind file → check nội dung ảnh | ❌ cần LLM |

---

## Quy tắc sửa lỗi

### Lỗi sửa tự động:
MC-1, MC-2, MC-4, MC-5, MC-7, MC-8, MC-9, MC-11, SK-2, SK-3, SK-5, SK-6, SK-7, EX-1, EX-5, EX-6, EX-7, EX-8, EX-11
> **Lưu ý**: MC-11 áp dụng cho TẤT CẢ levels (TOPIK I + TOPIK II), KHÔNG chỉ TOPIK II.

### Lỗi cần LLM:
Tất cả lỗi còn lại. Khi viết lại:
- Đọc `kinds/{kind}.md` để lấy **tất cả** quy tắc riêng của kind
- Đọc **bảng tham chiếu** bên dưới để lấy bảng topic, trap, question_feature, difficulty, answer_grammar
- Giữ nguyên các trường khác, chỉ sửa trường lỗi

## Output
- CSV đã sửa (ghi đè file gốc)
- Báo cáo: số lỗi theo nhóm, số đã sửa, số cần xem lại

---

## Bảng tham chiếu

Tất cả bảng dưới đây được trích từ quy tắc gen gốc. Dùng để tra cứu khi QC — kiểm tra các trường metadata có hợp lệ không.

### Danh mục chủ đề (topic)

| Code | Nhãn tiếng Anh | Tiếng Hàn | Kind thường gặp |
|------|---------------|-----------|----------------|
| `daily_life` | Daily Life & Routine | 일상생활 | 120001, 120002_1~4, 120004_1 |
| `food_restaurant` | Food & Dining | 음식/식당 | 120001, 120002_1~4 |
| `shopping_price` | Shopping & Price | 쇼핑/가격 | 120001, 120003_1~2 |
| `school_education` | School & Education | 학교/교육 | 120001, 120004_2, 220003_b |
| `hobby_leisure` | Hobbies & Leisure | 취미/여가 | 120001, 220002_c |
| `travel` | Travel & Tourism | 여행/관광 | 120003_1~2, 220002_b_1~3 |
| `health_hospital` | Health & Hospital | 건강/병원 | 120002_1~4, 220001_b |
| `weather_season` | Weather & Seasons | 날씨/계절 | 120001, 120002_1~4 |
| `culture_event` | Culture & Events | 문화/행사 | 220002_b_1~3, 220003_a_1~2 |
| `environment_society` | Environment & Society | 환경/사회 | 220003_b, 220006, 220008_1~2 |
| `science_tech` | Science & Technology | 과학/기술 | 220003_b, 220007, 220008_1~2 |
| `economy_business` | Economy & Business | 경제/산업 | 220006, 220008_1~2 |
| `language_expression` | Language & Expression | 언어/표현 | 220003_b, 220007 |
| `psychology_behavior` | Psychology & Behavior | 심리/행동 | 220003_b, 220008_1~2 |

---

### Chiến lược bẫy đáp án sai (distractor_trap)

#### Nhóm 1: Bẫy từ vựng (Vocabulary Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_shared_noun` | Shared-Noun Trap | Đáp án sai chứa từ vựng giống đoạn đọc |
| `trap_synonym_swap` | Synonym Swap | Thay từ đúng bằng từ đồng nghĩa nhưng sai ngữ cảnh |
| `trap_similar_word` | Similar Word | Đáp án chứa từ phát âm/dạng tương tự (e.g. 관광/관계) |

#### Nhóm 2: Bẫy phủ định (Negation Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_neg_없안` | Negation 없/안/아니 | Đáp án sai đảo nghĩa bằng 없다/안/아니다 |
| `trap_neg_않못` | Negation 않/못 | Đáp án sai thêm 않다/못하다 |
| `trap_neg_reverse` | Reverse NOT | Kind 120003_1~2 — đáp án ĐÚNG là cái SAI; bẫy là các phát biểu đúng |

#### Nhóm 3: Bẫy cấu trúc (Structural Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_same_ending` | Same-Ending Pattern | Cả 4 đáp án kết thúc cùng dạng ngữ pháp |
| `trap_order_swap` | Order Swap | Kind sắp xếp — đảo thứ tự 1-2 câu |
| `trap_grammar_form` | Grammar Form Trap | Đáp án sai dùng dạng ngữ pháp khác |

#### Nhóm 4: Bẫy nội dung (Content Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_partial_truth` | Partial Truth | Đáp án sai chứa >50% nội dung đúng nhưng sửa 1 chi tiết |
| `trap_subject_swap` | Subject Swap | Gán hành động/đặc điểm cho sai đối tượng |
| `trap_number_shift` | Number/Time Shift | Thay đổi con số/thời gian/số lượng từ bài đọc |
| `trap_detail_distort` | Detail Distortion | Đáp án sai bóp méo chi tiết nhỏ trong đoạn văn |
| `trap_overgeneralize` | Overgeneralization | Đáp án sai khái quát hóa quá mức từ nội dung cụ thể |
| `trap_wrong_inference` | Wrong Inference | Suy luận hợp lý nhưng KHÔNG có trong bài đọc |
| `trap_cause_effect_swap` | Cause-Effect Swap | Đảo quan hệ nhân quả: "A gây ra B" → "B gây ra A" |
| `trap_scope_change` | Scope Change | Thay đổi từ chỉ phạm vi: 모든↔일부, 항상↔가끔, 반드시↔때때로 |
| `trap_temporal_distort` | Temporal Distortion | Đảo biểu thức thời gian: 이미↔아직, 전에↔후에, 먼저↔나중에 |
| `trap_condition_omit` | Condition Omission | Bỏ/thêm điều kiện giới hạn khiến câu sai trở nên "đúng bề mặt" |
| `trap_comparison_flip` | Comparison Flip | Đảo chiều so sánh: "A hơn B" → "B hơn A" |
| `trap_wrong_relation` | Wrong Relation | Liên từ sai quan hệ nhân quả/tương phản/bổ sung |
| `trap_partial_topic` | Partial Topic | Cụm danh từ chỉ đề cập một phần nội dung, không phải nội dung chính |
| `trap_detail_as_main` | Detail As Main | Lấy chi tiết phụ làm nội dung chính |

---

### Đặc điểm câu hỏi (question_feature)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `qf_topic_identify` | Topic Identification | Đoạn văn nói về chủ đề gì? | 120001, 220003_a_1~2, 220003_b |
| `qf_fill_blank` | Fill in Blank | Điền từ/cụm vào chỗ trống ( ) | 120002_1~4, 220001_a, 220001_b, 220001_c |
| `qf_not_match` | NOT Matching | Chọn phát biểu KHÔNG khớp nội dung | 120003_1~2 |
| `qf_content_match` | Content Matching | Chọn phát biểu khớp nội dung | 120004_1, 220002_c |
| `qf_central_thought` | Central Thought | Ý chính / trung tâm của đoạn văn | 120004_2, 220003_b |
| `qf_multi_passage` | Multi-Question Passage | Đoạn văn + 2-3 câu hỏi | 120005, 120007_1~3, 220005_1~2, 220008_1~2 |
| `qf_sentence_order` | Sentence Ordering | Sắp xếp câu đúng thứ tự | 120006, 220004 |
| `qf_similar_meaning` | Similar Meaning | Tìm cụm có nghĩa tương tự phần gạch chân | 220002_a |
| `qf_graph_match` | Graph/Chart Matching | Nội dung khớp biểu đồ/đồ thị | 220002_b_1~3 |
| `qf_headline_explain` | Headline Explanation | Giải thích tiêu đề báo chí | 220006 |
| `qf_sentence_insert` | Sentence Insertion | Chèn câu vào vị trí phù hợp | 220007 |

---

### Ngữ pháp trong đáp án (answer_grammar)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `ans_noun_phrase` | Đáp án là danh từ/cụm danh từ | 120001, 120002_1~4 (một phần), 220003_a_1~2 |
| `ans_sentence_plain` | Đáp án là câu thể trần thuật (~ㄴ다/한다) | 120004_1, 120004_2, 220002_c, 220003_b, 220005_2, 220008_1, 220008_2 |
| `ans_sentence_polite` | Đáp án dùng ~ㅂ니다/습니다 | 120003_1~2 |
| `ans_grammar_form` | Đáp án là cấu trúc ngữ pháp | 220001_a, 220002_a |
| `ans_grammar_phrase` | Đáp án là cụm từ cùng gốc từ vựng, khác ngữ pháp | 120005 (Dạng 1 — content[0]) |
| `ans_conjunction` | Đáp án là liên từ (그리고, 그래서, 그렇지만...) | 120005_(2) (content[0]) |
| `ans_word_phrase` | Đáp án là từ hoặc cụm từ ngắn (cụm động từ, cụm tính từ, cụm bổ nghĩa) | 120007_2 (content[0]) |
| `ans_sentence_long` | Đáp án là câu dài (20+ ký tự) | 220001_b, 220001_c, 220006, 220008_1~2 |
| `ans_order_combo` | Đáp án là tổ hợp thứ tự (가)-(나)-(다)-(라) | 120006, 220004 |
| `ans_verb_polite` | Đáp án dùng ~어요/아요 (động từ) | 120002_1~4 |
| `ans_grammar_conjugation` | Đáp án là dạng chia ngữ pháp | 120005_(1) |
| `ans_sentence_purpose` | Đáp án mô tả mục đích ~(으)려고 | 120007_3 |
| `ans_single_noun` | Đáp án là danh từ đơn (~2 âm tiết) | 220003_a_1 |
| `ans_position_mark` | Đáp án là vị trí ㉠/㉡/㉢/㉣ | 220007 |

---

### Thang độ khó (Difficulty Scale)

| Mức | Kind | Kiểu suy luận |
|:---:|------|--------------|
| 2 | 120001 | `vocab_match` — Từ vựng đơn giản |
| 3 | 120002_1~4 | `context_fill` — Điền chỗ trống dựa ngữ cảnh |
| 4 | 120003_1~2 | `detail_extraction` — Trích xuất chi tiết từ hình/văn |
| 5 | 120004_1, 120004_2, 220002_a | `content_matching` — So khớp nội dung |
| 6 | 120006, 220001_a, 220003_a_1~2, 220004 | `logical_ordering` / `grammar_inference` |
| 7 | 120005, 120007_1~3, 220001_b, 220001_c, 220002_b_1~3, 220002_c, 220005_1~2 | `paragraph_comprehension` — Hiểu đoạn văn |
| 8 | 220003_b, 220006, 220007 | `abstract_reasoning` — Suy luận trừu tượng |
| 9 | 220008_1~2 | `deep_comprehension` — Hiểu sâu + nhiều câu hỏi |

---

## Lưu ý
- Skill này **TÁCH BIỆT hoàn toàn** với skill gen — chỉ đọc và sửa CSV
- Folder `kinds/` chứa bản sao các kind files — dùng để tra cứu quy tắc khi QC
- Chỉ chỉnh CSV trong `output/`, KHÔNG chỉnh bất kỳ file nào khác
- Khi sửa LLM, tuân theo **tất cả quy tắc** trong kind file + bảng tham chiếu
