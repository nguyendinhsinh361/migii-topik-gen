---
name: topik-read-gen-origin
description: Gen câu hỏi TOPIK Đọc (읽기) Level 1-2. 36 dạng từ 120001 đến 220008_2.
---

# TOPIK Reading Question Generator (TOPIK I & II)

Skill tạo câu hỏi phần Đọc (읽기) cho kỳ thi TOPIK I & II theo đúng format JSON của hệ thống Migii.

## Khi nào dùng skill này

- Khi user yêu cầu tạo/gen câu hỏi đọc TOPIK (Level 1 & 2)
- Khi user chỉ định kind cụ thể (ví dụ: "gen 120001", "tạo câu hỏi dạng 220007")
- Khi user yêu cầu tạo đề thi đọc TOPIK I hoặc TOPIK II

## Cấu trúc thư mục

`
skills/topik-read-gen-origin/
├── SKILL.md              ← File này (overview + quy tắc chung)
├── scripts/
│   └── save_read.py      ← Script lưu CSV/JSON theo kind
├── kinds/                ← Quy tắc chi tiết từng dạng
│   ├── 120001.md         Đoán chủ đề đoạn văn ngắn (TOPIK I)
│   ├── 120002_1.md       Điền chỗ trống [34] (TOPIK I)
│   ├── 120002_2.md       Điền chỗ trống [35~37] (TOPIK I)
│   ├── 120002_3.md       Điền chỗ trống [38] (TOPIK I)
│   ├── 120002_4.md       Điền chỗ trống [39] (TOPIK I)
│   ├── 120003_1.md       Chọn đáp án sai [40~41] (TOPIK I) [ảnh]
│   ├── 120003_2.md       Chọn đáp án sai [42] (TOPIK I) [ảnh]
│   ├── 120004_1.md       Nội dung khớp (TOPIK I)
│   ├── 120004_2.md       Ý chính / trung tâm (TOPIK I)
│   ├── 120005_(1).md     Đọc đoạn + 2 câu hỏi — Điền ngữ pháp + Nội dung khớp (TOPIK I)
│   ├── 120005_(2).md     Đọc đoạn + 2 câu hỏi — Điền liên từ + Xác định chủ đề (TOPIK I)
│   ├── 120006.md         Sắp xếp câu theo thứ tự (TOPIK I)
│   ├── 120007_1.md       Đoạn văn ngắn khó [59~60] (TOPIK I)
│   ├── 120007_2.md       Đoạn văn ngắn khó [61~68] (TOPIK I)
│   ├── 120007_3.md       Đoạn văn ngắn khó [69~70] (TOPIK I)
│   ├── 220001_a.md       Điền ngữ pháp liên kết [1~2] (TOPIK II)
│   ├── 220001_b.md       Điền nội dung đoạn [16~18] (TOPIK II)
│   ├── 220001_c.md       Điền nội dung đoạn [28~31] (TOPIK II)
│   ├── 220002_a.md       Ý nghĩa tương tự — 밑줄 [3~4] (TOPIK II)
│   ├── 220002_b_1.md     Nội dung tương tự [9] (TOPIK II) [ảnh]
│   ├── 220002_b_2.md     Nội dung tương tự [10] (TOPIK II) [ảnh]
│   ├── 220002_b_3.md     Nội dung tương tự [11~12] (TOPIK II) [ảnh]
│   ├── 220002_c.md       Nội dung khớp văn bản [32~34] (TOPIK II)
│   ├── 220003_a_1.md     Chủ đề đoạn văn [5~6] (TOPIK II) [ảnh]
│   ├── 220003_a_2.md     Chủ đề đoạn văn [7~8] (TOPIK II) [ảnh]
│   ├── 220003_b.md       Chủ đề đoạn văn dài [35~38] (TOPIK II)
│   ├── 220004.md         Sắp xếp câu nâng cao (TOPIK II)
│   ├── 220005_1_(1).md   Đoạn văn dễ — Liên từ/trạng từ + Chủ đề [19~20] (TOPIK II)
│   ├── 220005_1_(2).md   Đoạn văn dễ — Thành ngữ + Nội dung khớp [21~22] (TOPIK II)
│   ├── 220005_2.md       Đoạn văn dễ [23~24] (TOPIK II)
│   ├── 220006.md         Tiêu đề báo chí (TOPIK II)
│   ├── 220007.md         Chèn câu vào đúng vị trí (TOPIK II)
│   ├── 220008_1_(1).md   Đoạn văn khó — Tiểu thuyết văn học + Cảm xúc nhân vật [42~43] (TOPIK II)
│   ├── 220008_1_(2).md   Đoạn văn khó — Học thuật + Điền từ + Chủ đề [44~45] (TOPIK II)
│   ├── 220008_1_(3).md   Đoạn văn khó — Học thuật + Thái độ tác giả + Nội dung khớp [46~47] (TOPIK II)
│   └── 220008_2.md       Đoạn văn khó [48~50] (TOPIK II)
└── samples.json          ← Mẫu câu hỏi tham khảo
`

Khi gen kind cụ thể, đọc file `kinds/{kind}.md` tương ứng + file SKILL.md này.

---

> **🔗 ĐỒNG BỘ q_image_desc ↔ explain** (dạng có ảnh): Nội dung mô tả từng ảnh trong q_image_desc PHẢI khớp chính xác với nội dung explain tương ứng. TUYỆT ĐỐI KHÔNG được ảnh mô tả một kiểu, explain giải thích kiểu khác. → Gen q_image_desc TRƯỚC, rồi viết explain DỰA TRÊN nội dung q_image_desc đã gen.
## Quy tắc routing sub-kind

Một số kind được tách thành nhiều **sub-kind** (đánh dấu "tổng quan" trong cây thư mục). Mỗi sub-kind có kiểu đoạn văn, dạng câu hỏi phụ, hoặc format đáp án riêng biệt.

### Kind có sub-kind

| Parent kind | Sub-kinds | Có file tổng quan? | Tiêu chí tách |
|-------------|-----------|---------------------|---------------|
| 120002 | 120002_1, _2, _3, _4 | ❌ Không có file tổng quan | Dạng câu hỏi theo cấu trúc đoạn văn |
| 120003 | 120003_1, _2 | ❌ Không có file tổng quan | Dạng câu hỏi [ảnh] |
| 120005 | 120005_(1), _(2) | ❌ Không có file tổng quan | Dạng câu hỏi: điền ngữ pháp + nội dung khớp / điền liên từ + chủ đề |
| 120007 | 120007_1, _2, _3 | ❌ Không có file tổng quan | Dạng đoạn văn ngắn khó |
| 220002_b | 220002_b_1, _2, _3 | ❌ Không có file tổng quan | Nội dung tương tự [ảnh] |
| 220003_a | 220003_a_1, _2 | ❌ Không có file tổng quan | Chủ đề đoạn văn [ảnh] |
| 220005_1 | 220005_1_(1), _(2) | ⚠️ KHÔNG có file tổng quan | Dạng câu hỏi: liên từ + chủ đề [19~20] / thành ngữ + nội dung khớp [21~22] |
| 220008_1 | 220008_1_(1), _(2), _(3) | ⚠️ KHÔNG có file tổng quan | Thể loại văn bản: tiểu thuyết [42~43] / học thuật điền từ [44~45] / học thuật thái độ [46~47] |

### Quy tắc gen

1. **KHÔNG có file tổng quan** cho bất kỳ parent kind nào — luôn đọc file sub-kind cụ thể.

2. **User chỉ định parent kind** (vd: "gen 220008_1"):
   - Tra bảng trên để xác định danh sách sub-kind
   - **Phân bổ đều** câu hỏi qua các sub-kind để đảm bảo đa dạng
   - Ví dụ: gen 6 câu 220008_1 → 2 câu 220008_1_(1) + 2 câu 220008_1_(2) + 2 câu 220008_1_(3)
   - Mỗi câu đọc đúng file sub-kind tương ứng để lấy quy tắc riêng

3. **User chỉ định sub-kind** (vd: "gen 220008_1_(1)"):
   - Đọc file sub-kind trực tiếp, gen tất cả câu theo sub-kind đó

4. **Trường `kind` trong JSON output**: Ghi **sub-kind** cụ thể (vd: `"220008_1_(1)"`), không ghi parent kind.

> **Lưu ý**: Các bảng topic, difficulty, trap bên dưới tham chiếu parent kind (vd: `220008_1~2`). Sub-kind kế thừa tất cả thuộc tính của parent trừ khi file sub-kind ghi đè riêng.

---

## Quy tắc biên tập theo kind (độ dài / dấu câu)

> **Nguồn**: Biên tập viên bổ sung — *"MIGII TOPIK - Read Rule - Gen Question AI New.xlsx"*. Quy tắc BẮT BUỘC, ưu tiên cao nhất. Khi gen mỗi kind PHẢI áp dụng đúng: **độ dài đoạn đọc**, **độ dài text câu hỏi**, **dấu chấm sau đáp án**.

**Cách đọc bảng:**

- **G_text (ký tự)**: độ dài đoạn văn đọc dùng chung ở `g_text`. `—` = kind không có đoạn `g_text` riêng. *Text trong ảnh* = nội dung chữ nằm TRONG ảnh (`q_image`), không phải `g_text`.
- **Text câu hỏi (ký tự)**: độ dài đoạn/câu đọc gắn theo câu hỏi (`text_question_1` / `q_text`). `—` = không quy định.
- **Đ.án Q1 / Q2 / Q3**: dấu "." cuối đáp án cho từng câu hỏi con. `True` = có ".", `False` = không. `—` = không có câu hỏi con đó.
- **Đếm như Google Dịch**: TÍNH CẢ dấu cách, dấu câu, ký hiệu ㉠/㉡, xuống dòng; **KHÔNG tính** dòng trống `___`.

| Kind | G_text (ký tự) | Text câu hỏi (ký tự) | Đ.án Q1 | Đ.án Q2 | Đ.án Q3 |
|------|----------------|----------------------|:-------:|:-------:|:-------:|
| 120001 | — | 20~35 | False | — | — |
| 120002_1 | — | 20~35 | False | — | — |
| 120002_2 | — | 20~35 | False | — | — |
| 120002_3 | — | 20~35 | False | — | — |
| 120002_4 | — | 20~35 | False | — | — |
| 120003_1 | — | — | True | — | — |
| 120003_2 | — | — | True | — | — |
| 120004_1 | — | 50~80 | True | — | — |
| 120004_2 | — | 50~80 | True | — | — |
| 120005_(1) | 130~180 | — | False | True | — |
| 120005_(2) | 130~180 | — | False | False | — |
| 120006 | — | 120~150 | False | — | — |
| 120007_1 | 140~190 | — | False | True | — |
| 120007_2 | 150~200 | — | False | True | — |
| 120007_3 | Text trong ảnh: 250~300 | — | False | True | — |
| 220001_a | — | 25~30 | False | — | — |
| 220001_b | — | 150~200 | False | — | — |
| 220001_c | — | 170~250 | False | — | — |
| 220002_a | — | 30~40 | False | — | — |
| 220002_b_1 | Text trong ảnh: 180~220 | — | True | — | — |
| 220002_b_2 | — | — | True | — | — |
| 220002_b_3 | — | 180~210 | True | — | — |
| 220002_c | — | 190~250 | True | — | — |
| 220003_a_1 | Text trong ảnh: 20~30 | — | False | — | — |
| 220003_a_2 | Text trong ảnh: 30~60 | — | False | — | — |
| 220003_b | — | 200~240 | True | — | — |
| 220004 | — | 140~170 | False | — | — |
| 220005_1_(1) | 180~240 | — | False | True | — |
| 220005_1_(2) | 200~240 | — | False | True | — |
| 220005_2 | 420~500 | — | False | True | — |
| 220006 | — | 20~40 | True | — | — |
| 220007 | — | 250~320 | False | — | — |
| 220008_1_(1) | 550~600 | — | False | True | — |
| 220008_1_(2) | 380~400 | — | False | True | — |
| 220008_1_(3) | 400~440 | — | True | True | — |
| 220008_2 | 460~510 | — | False | False | True |

> **Lưu ý quan trọng:**
> - Phần ĐỌC khác phần NGHE: **mặc định đáp án KHÔNG có dấu chấm** (False), chỉ một số kind cụ thể mới có (True). Đừng tự thêm dấu chấm.
> - Với "Text trong ảnh": độ dài áp cho nội dung chữ vẽ trong `q_image`, mô tả trong `q_image_desc` — KHÔNG nằm ở `g_text`.
> - `save_read.py` tự động thêm/bỏ dấu "." theo bảng này (map `_ANSWER_PERIOD`) và **cảnh báo** khi `g_text`/`text_question` lệch khoảng (map `_GTEXT_LENGTH`, `_QTEXT_LENGTH`). Vẫn PHẢI gen đúng từ đầu.

---

## Output Format (JSON)

Mỗi câu hỏi PHẢI tuân theo cấu trúc JSON sau:

`json
{
  "title": "<tiêu đề dạng câu hỏi bằng tiếng Hàn>",
  "general": {
    "g_text": "<đoạn văn đọc chung — nếu count_question >= 2>",
    "g_text_translate": { "vi": "<dịch tiếng Việt>", "en": "<dịch tiếng Anh>" },
    "g_text_audio": "",
    "g_text_audio_translate": { "vi": "", "en": "" },
    "g_audio": "",
    "g_image": ""
  },
  "content": [
    {
      "q_text": "<đoạn văn hoặc câu hỏi phụ>",
      "q_image": "",
      "q_point": 2,
      "q_answer": ["<đáp án 1>", "<đáp án 2>", "<đáp án 3>", "<đáp án 4>"],
      "q_correct": 1,
      "explain": {
        "vi": "<giải thích tiếng Việt — dễ hiểu cho người học>",
        "en": "<giải thích tiếng Anh>"
      }
    }
  ],
  "level": 1,
  "kind": "120001",
  "count_question": 1,   // ⚠️ PHẢI >= 1, KHÔNG BAO GIỜ = 0
  "tag": "read"
}
`

### Trường metadata BẮT BUỘC

Các trường sau **PHẢI có** trong mỗi câu hỏi gen ra. Samples.json không chứa các trường này (vì lấy từ dữ liệu cũ), nhưng khi gen mới **BẮT BUỘC** phải thêm:

`json
// Trong content[] — thêm vào MỖI câu hỏi con:
"question_feature": "<mã từ bảng question_feature>",
"difficulty": 3,
"distractor_traps": {
  "1": "", "2": "trap_detail_distort", "3": "trap_neg_없안", "4": "trap_shared_noun"
}

// Ở cấp top-level — thêm vào MỖI câu hỏi:
"topic": "daily_routine"
`

- `topic`: chọn từ bảng **Danh mục chủ đề** bên dưới
- `question_feature`: chọn từ bảng **Đặc điểm câu hỏi** bên dưới, theo kind
- `difficulty`: lấy từ bảng **Thang độ khó** bên dưới, theo kind
- `distractor_traps`: ghi trap code cho **từng đáp án** (đáp án đúng để rỗng `""`)

### Khác biệt so với Listening

| Trường | Listen | Read |
|--------|--------|------|
| `g_text_audio` | Nội dung audio | **Luôn rỗng** |
| `g_text` | Thường rỗng | Đoạn văn đọc chung (khi count_question ≥ 2) |
| `q_text` | Câu hỏi phụ hoặc rỗng | Đoạn văn đọc HOẶC câu hỏi phụ |
| `tag` | `"listen"` | `"read"` |
| `q_image` | Rỗng (mô tả qua q_image_description) | URL ảnh thực (poster, biểu đồ, biển hiệu) |

### Format BẮT BUỘC cho kind có ảnh

Kind có ảnh (120003_1, 120003_2, 220002_b_1, 220002_b_2, 220002_b_3, 220003_a_1, 220003_a_2) **PHẢI** có trường `q_image_description` ở **cấp top-level** (cùng cấp `title`, `general`):

`json
{
  "q_image_description": {
    "image": "<mô tả chi tiết nội dung hình ảnh>"
  }
}
`

Cách viết mô tả: xem chi tiết trong file `kinds/{kind}.md` tương ứng.

---

## Danh mục chủ đề (topic)

Phân tích từ câu hỏi đọc thực tế TOPIK I & II.

### Chủ đề chung (Level 1, 2)

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

## Chiến lược bẫy đáp án sai (distractor_trap)

### Nhóm 1: Bẫy từ vựng (Vocabulary Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_shared_noun` | Shared-Noun Trap | Đáp án sai chứa từ vựng giống đoạn đọc |
| `trap_synonym_swap` | Synonym Swap | Thay từ đúng bằng từ đồng nghĩa nhưng sai ngữ cảnh |
| `trap_similar_word` | Similar Word | Đáp án chứa từ phát âm/dạng tương tự (e.g. 관광/관계) |

### Nhóm 2: Bẫy phủ định (Negation Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_neg_없안` | Negation 없/안/아니 | Đáp án sai đảo nghĩa bằng 없다/안/아니다 |
| `trap_neg_않못` | Negation 않/못 | Đáp án sai thêm 않다/못하다 |
| `trap_neg_reverse` | Reverse NOT | Kind 120003_1~2 — đáp án ĐÚNG là cái SAI; bẫy là các phát biểu đúng |

### Nhóm 3: Bẫy cấu trúc (Structural Traps)

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_same_ending` | Same-Ending Pattern | Cả 4 đáp án kết thúc cùng dạng ngữ pháp |
| `trap_order_swap` | Order Swap | Kind sắp xếp — đảo thứ tự 1-2 câu |
| `trap_grammar_form` | Grammar Form Trap | Đáp án sai dùng dạng ngữ pháp khác |

### Nhóm 4: Bẫy nội dung (Content Traps)

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

### ⚠️ CHỈ ĐÚNG 1 ĐÁP ÁN (CRITICAL)
> **⏺ DẤU CHẤM CUỐI ĐÁP ÁN — THEO TỪNG KIND & TỪNG CÂU HỎI CON**: Phần ĐỌC **đa số kind KHÔNG có dấu "."** (đáp án là từ/cụm danh từ/cụm ngữ pháp). Tra bảng **[Quy tắc biên tập theo kind](#quy-tắc-biên-tập-theo-kind-độ-dài--dấu-câu)** (cột `Đ.án Q1/Q2/Q3`):
> - **True** = mỗi đáp án (và mỗi dòng dịch đáp án trong explain, trước separator) PHẢI kết thúc bằng ".". **False** = KHÔNG có ".".
> - Kind nhiều câu hỏi (120005_*, 120007_*, 220005_*, 220008_*) thường khác nhau giữa các câu hỏi con → áp dụng đúng cho từng câu hỏi.
> - Đáp án dạng ảnh ①②③④ KHÔNG BAO GIỜ có ".".

- **TUYỆT ĐỐI chỉ có 1 đáp án đúng duy nhất.** 3 đáp án sai PHẢI rõ ràng sai, không được hợp lệ từ bất kỳ góc nhìn nào.
- Đáp án sai phải **tự mâu thuẫn nội tại** hoặc **trả lời sai loại thông tin**.
- Trước khi hoàn thành, **kiểm tra lại 3 đáp án sai**: nếu bất kỳ đáp án sai nào có thể trả lời câu hỏi một cách hợp lệ → PHẢI sửa lại.

---

## Đặc điểm câu hỏi (question_feature)

### Dạng câu hỏi chính

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

## Định dạng văn bản đọc (text_format)

Thay thế `audio_format` của Listen — xác định dạng bài đọc:

| Code | Mô tả | Độ dài trung bình | Kind chính |
|------|-------|:-----------------:|-----------|
| `text_short_sentence` | 1-2 câu ngắn, từ vựng đơn giản | 15-30 ký tự | 120001, 120002 |
| `text_paragraph_short` | Đoạn văn ngắn (3-5 câu) | 50-100 ký tự | 120004_1, 120004_2, 220002_c |
| `text_paragraph_long` | Đoạn văn dài (6+ câu) | 150-300 ký tự | 220003_b, 220007, 220008_1~2 |
| `text_passage_multi` | Đoạn dài + nhiều câu hỏi | 150-500 ký tự (g_text) | 120005, 120007_1~3, 220005_1~2, 220008_1~2 |
| `text_notice_poster` | Thông báo / poster / quảng cáo (ảnh) | Ảnh | 120003_1~2, 220002_b_1~3, 220003_a_1~2 |
| `text_headline` | Tiêu đề báo (ngắn, ẩn dụ) | 15-30 ký tự | 220006 |
| `text_ordered_sentences` | 4 câu (가)(나)(다)(라) cần sắp xếp | 120-200 ký tự | 120006, 220004 |

---

## Ngữ pháp đáp án (answer_grammar)

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

## Thang độ khó (Difficulty Scale)

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

## Cấp độ đọc theo level (reading_level)

| Level | Đặc điểm văn bản | Ngữ pháp phổ biến |
|:-----:|------------------|------------------|
| 1 | Câu ngắn, từ vựng cơ bản N5-N4, chủ đề sinh hoạt | ~ㅂ니다/어요, ~는/은, ~에서, ~과/와 |
| 2 | Đoạn văn dài, từ vựng trung-cao cấp, chủ đề xã hội/khoa học | ~(으)ㄴ/는, ~기 때문에, ~(으)므로, ~에 따르면 |

---

## Quy tắc chung khi gen câu hỏi

### 1. Chất lượng nội dung tiếng Hàn
- Dùng ngữ pháp đúng level (xem bảng reading_level)
- Văn bản tự nhiên, đa dạng chủ đề
- KHÔNG lặp lại từ vựng/ngữ cảnh giữa các câu trong cùng batch
- Level 2: đoạn văn mạch lạc, chủ đề xã hội/khoa học/tâm lý

### 2. Xây dựng đáp án sai (distractor)

> **⛔ 4 ĐÁP ÁN CÂN BẰNG ĐỘ DÀI (ÁP DỤNG MỌI DẠNG)**: 4 đáp án PHẢI có độ dài tương đương nhau. **ĐẶC BIỆT KHÔNG để đáp án ĐÚNG dài đột biến** so với 3 đáp án còn lại — đáp án đúng dài hơn hẳn là dấu hiệu LỘ ĐÁP ÁN (thí sinh đoán câu dài nhất là đúng). Chênh lệch độ dài tối đa ~30%. Nếu đáp án đúng đang dài hơn → RÚT GỌN đáp án đúng, hoặc bổ sung chi tiết cho các đáp án sai để 4 câu cân nhau.
- Tuân theo tỷ lệ bẫy của từng kind (xem file kind tương ứng)
- Phải hợp lý nhưng SAI về nội dung
- Tái sử dụng từ vựng bài đọc khi kind yêu cầu `trap_shared_noun`
- Đáp án sai phải cùng format/độ dài với đáp án đúng

### 3. Giải thích (explain)

**Format explain.vi và explain.en PHẢI GIỐNG NHAU về cấu trúc** — chỉ khác ngôn ngữ. Cụ thể:

**Câu đơn (count_question = 1):**
`
[Dịch bài đọc/đoạn văn]
[Nếu có ảnh: dịch text hiển thị trên ảnh, mỗi ý xuống dòng]

1. [Dịch đáp án 1]
2. [Dịch đáp án 2]
3. [Dịch đáp án 3]
4. [Dịch đáp án 4]
--------------------
[Giải thích — dùng ngôn ngữ dễ hiểu, KHÔNG ghi mã trap]

Đáp án [N] là đáp án đúng vì [lý do].
Đáp án [X] sai vì [lý do].
Đáp án [Y] sai vì [lý do].
Đáp án [Z] sai vì [lý do].
`

**Câu ghép (count_question ≥ 2):**
`
[Dịch bài đọc/đoạn văn]

[Dịch câu hỏi phụ 1]: ...
1. [Dịch đáp án 1]  2. [Dịch đáp án 2]  3. [Dịch đáp án 3]  4. [Dịch đáp án 4]
--------------------
Đáp án [N] là đáp án đúng vì [lý do].
Đáp án [X] sai vì [lý do].
Đáp án [Y] sai vì [lý do].
Đáp án [Z] sai vì [lý do].

[Dịch câu hỏi phụ 2]: ...
1. [Dịch đáp án 1]  2. [Dịch đáp án 2]  3. [Dịch đáp án 3]  4. [Dịch đáp án 4]
--------------------
Đáp án [N] là đáp án đúng vì [lý do].
Đáp án [X] sai vì [lý do].
Đáp án [Y] sai vì [lý do].
Đáp án [Z] sai vì [lý do].
`

- **Format explain PHẢI xuống dòng rõ ràng** — mỗi phần (dịch bài, dịch đáp án, separator, giải thích từng đáp án) PHẢI xuống dòng (`\n`). KHÔNG viết thành 1 đoạn dài liền mạch. Mỗi đáp án giải thích trên 1 dòng riêng. Explain phải dễ đọc, có cấu trúc rõ ràng.
- **TẤT CẢ levels** (TOPIK I, TOPIK II): `q_correct` PHẢI **phân bố đều 1-4** cho TẤT CẢ levels. KHÔNG fix cứng q_correct = 1 cho bất kỳ level nào. Ví dụ: nếu gen 4 câu cùng kind thì phải có q_correct = 1, 2, 3, 4 (mỗi giá trị 1 lần). KHÔNG được thiên lệch.
- **`q_correct` PHẢI là integer** (1, 2, 3, hoặc 4) — **KHÔNG BAO GIỜ** là số thập phân (1.0, 2.0, 3.0, 4.0).
- **vi** và **en** phải có **cùng số phần** và **cùng mức chi tiết**: dịch bài, dịch đáp án, separator, giải thích
- Nếu vi giải thích từng đáp án sai → en cũng PHẢI giải thích từng đáp án sai
- **KHÔNG** để en ngắn gọn kiểu "=> Answer 1" mà vi thì giải thích dài — explain_en PHẢI chi tiết bằng explain_vi
- **KHÔNG** ghi mã trap nội bộ (trap_detail_distort, trap_partial_truth…) vào explain — explain dành cho người học
- **Câu ghép (count_question ≥ 2)**: PHẢI dịch cả câu hỏi phụ (q_text) vào explain trước phần dịch đáp án
- **Câu có ảnh**: Phần dịch text ảnh trong explain chỉ dịch **text hiển thị trên ảnh** (tiêu đề, số liệu, nhãn…), KHÔNG dịch nguyên văn q_image_description (vì q_image_desc chứa cả mô tả bố cục/màu sắc)
- Highlight từ vựng/ngữ pháp quan trọng
- **KHÔNG dùng icon/emoji** (✅, ❌, ✓, ✗...) trong explain. Explain là text thuần, không có icon
- **Trích dẫn tiếng Hàn giữ nguyên** — khi explain dẫn từ/cụm từ/câu tiếng Hàn từ bài đọc, PHẢI giữ nguyên tiếng Hàn trong ngoặc đơn, KHÔNG dịch sang tiếng Việt hay tiếng Anh. Ví dụ: "Đoạn văn đề cập '환경 보호의 중요성'" — giữ nguyên phần Hàn
- **🔤 KHÔNG DÙNG THẺ `<g></g>` TRONG EXPLAIN (cập nhật)**: Các cột giải thích (explain_vi, explain_en và _2/_3…) KHÔNG cần và KHÔNG được bọc thẻ `<g></g>`. Nếu cần nêu/trích tiếng Hàn thì viết trực tiếp, KHÔNG kèm thẻ.
- **Danh sách đáp án trong explain phải THUẦN ngôn ngữ đích** — explain_vi chỉ có tiếng Việt, explain_en chỉ có tiếng Anh. KHÔNG trộn tiếng Hàn vào danh sách đáp án:
  - ❌ `1. 약속 (cuộc hẹn)` hoặc `1. Cuộc hẹn (약속)` hoặc `1. 음식` (chỉ Hàn)
  - ✅ explain_vi: `1. Cuộc hẹn` / explain_en: `1. Appointment`
- **Trích dẫn PHẢI dùng nháy kép ""** — tất cả trích dẫn trong explain (cả vi lẫn en) đều dùng `"..."`. KHÔNG dùng nháy đơn '...', ngoặc đơn (...), hay để trần không nháy.
- **Trích dẫn tiếng Hàn PHẢI đồng nhất giữa vi và en** — nếu explain_vi trích dẫn tiếng Hàn (ví dụ: "환경 보호") thì explain_en cũng PHẢI trích dẫn cùng cụm tiếng Hàn đó, KHÔNG được dịch sang tiếng Anh. Trích dẫn gốc tiếng Hàn giữ nguyên ở CẢ HAI ngôn ngữ.
- **Từ tiếng Anh trong explain_vi phải được dịch sang tiếng Việt** (ví dụ: "digital literacy" → "năng lực số")
- **Separator trong explain**: dùng `--------------------` (20 dashes), KHÔNG dùng `----` (4 dashes)
- **explain KHÔNG bịa phân tích ngữ âm/phát âm** — KHÔNG viết "A có phát âm gần B" trừ khi thực sự đúng. Đáp án sai chỉ cần: "không liên quan đến nội dung hội thoại"
- **explain KHÔNG chứa nhãn bẫy đáp án** (trap labels) — thông tin trap đã nằm trong trường `distractor_traps`
- **Xưng hô tiếng Việt PHẢI thống nhất** — không trộn "em"+"tôi" hay "anh"+"bạn". Ưu tiên dùng **"bạn"** (ngôi 2) + **"tôi"** (ngôi 1), hoặc lược bỏ đại từ khi có thể.

### 4. Số lượng
- Mặc định: 5 câu mỗi kind nếu user không chỉ định
- Tối đa: 20 câu mỗi lần

### 5. Kiểm tra sau khi gen (Validation Checklist)
- [ ] **4 đáp án cân bằng độ dài** — đáp án ĐÚNG KHÔNG dài đột biến so với 3 đáp án còn lại (chênh lệch ~30%); nếu lệch → rút gọn đáp án đúng / thêm chi tiết cho đáp án sai
- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Văn bản là tiếng Hàn tự nhiên, đúng level
- [ ] Bẫy đúng phân bố của kind
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch + lý do đáp án đúng
- [ ] `count_question` khớp số phần tử trong `content` — **PHẢI >= 1, KHÔNG BAO GIỜ = 0**
- [ ] `tag` = `"read"` (KHÔNG phải `"listen"`)
- [ ] Kind có ảnh → có `q_image_description`
- [ ] **Độ dài** `g_text` / `text_question` đúng khoảng trong bảng [Quy tắc biên tập theo kind](#quy-tắc-biên-tập-theo-kind-độ-dài--dấu-câu) (`save_read.py` sẽ cảnh báo nếu lệch)
- [ ] **Dấu "." sau đáp án** đúng theo từng câu hỏi con (cột `Đ.án Q1/Q2/Q3`) — phần Đọc đa số KHÔNG dấu chấm; explain theo cùng quy tắc

## Workflow

1. User chỉ định kind → kiểm tra có sub-kind không (xem bảng **Quy tắc routing sub-kind**)
   - Có sub-kind → đọc file tổng quan, phân bổ đều qua sub-kinds, đọc từng file sub-kind
   - Không có sub-kind → đọc file `kinds/{kind}.md` trực tiếp
2. Hỏi số lượng (mặc định 5)
3. Gen câu hỏi theo JSON format + quy tắc kind + chiến lược bẫy
4. Lưu trực tiếp CSV theo kind vào `output/read-origin/level_{1,2}/{kind}.csv` bằng `scripts/save_read.py`
5. Validate theo checklist

### Quy tắc đường dẫn file

> **⚠️ QUAN TRỌNG: Folder `skills/` là READ-ONLY khi gen. KHÔNG ĐƯỢC tạo, sửa, hay xóa bất kỳ file nào trong `skills/` trong quá trình gen câu hỏi.**

| Loại file | Đường dẫn | Ghi chú |
|-----------|-----------|---------|
| CSV theo kind | `output/read-origin/level_{1,2}/{kind}.csv` | Output chính |
| CSV tổng hợp | `output/read-origin/all_questions.csv` | Merge từ tất cả kind |

### Lưu kết quả bằng script

`bash
# Lưu trực tiếp CSV theo kind + merge tổng
python skills/topik-read-gen-origin/scripts/save_read.py --data '<JSON_STRING>' -o output/read-origin --merge

# Chỉ validate
python skills/topik-read-gen-origin/scripts/save_read.py --data '<JSON_STRING>' --validate-only

# Append thêm batch mới
python skills/topik-read-gen-origin/scripts/save_read.py --data '<JSON_STRING>' --append
`
