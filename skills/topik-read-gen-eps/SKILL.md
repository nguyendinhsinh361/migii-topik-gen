---
name: topik-read-gen-eps
description: Gen câu hỏi EPS-TOPIK Đọc (읽기) Level 3. 10 dạng từ 320001 đến 3420008.
---

# EPS-TOPIK Reading Question Generator (Level 3)

Skill tạo câu hỏi phần Đọc (읽기) cho kỳ thi EPS-TOPIK (Level 3 — lao động nước ngoài) theo đúng format JSON của hệ thống Migii.

## Khi nào dùng skill này

- Khi user yêu cầu tạo/gen câu hỏi đọc EPS-TOPIK
- Khi user chỉ định kind EPS cụ thể (ví dụ: "gen 320001", "tạo câu hỏi dạng 3420007")
- Khi user yêu cầu tạo đề thi đọc EPS-TOPIK

## Cấu trúc thư mục

```
skills/topik-read-gen-eps/
├── SKILL.md              ← File này (overview + quy tắc chung)
├── scripts/
│   └── save_read.py      ← Script lưu CSV/JSON theo kind
├── kinds/                ← Quy tắc chi tiết từng dạng
│   ├── 320001.md         Xem hình chọn từ/câu (EPS, gồm 3420001) [ảnh]
│   ├── 320002.md         Điền chỗ trống (EPS, gồm 3420004)
│   ├── 320003.md         Trả lời câu hỏi — hình (EPS, gồm 3420005) [ảnh]
│   ├── 320004.md         Đọc + trả lời (EPS) [ảnh]
│   ├── 320005.md         Đọc dài + 2 câu hỏi (EPS)
│   ├── 3420002.md        Từ liên quan (EPS)
│   ├── 3420003.md        Đồng nghĩa / trái nghĩa (EPS)
│   ├── 3420006.md        Chủ đề đoạn văn (EPS)
│   ├── 3420007.md        Nội dung khớp (EPS)
│   └── 3420008.md        Từ vựng theo mô tả (EPS)
└── samples.json          ← Mẫu câu hỏi tham khảo (10 mẫu)
```

Khi gen kind cụ thể, đọc file `kinds/{kind}.md` tương ứng + file SKILL.md này.

---

## Output Format (JSON)

Mỗi câu hỏi PHẢI tuân theo cấu trúc JSON sau:

```json
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
      "q_point": null,
      "q_answer": ["<đáp án 1>", "<đáp án 2>", "<đáp án 3>", "<đáp án 4>"],
      "q_correct": 1,
      "explain": {
        "vi": "<giải thích tiếng Việt — dễ hiểu cho người học, KHÔNG ghi mã trap>",
        "en": "<giải thích tiếng Anh>"
      }
    }
  ],
  "level": 3,
  "kind": "320001",
  "count_question": 1,   // ⚠️ PHẢI >= 1, KHÔNG BAO GIỜ = 0
  "tag": "read"
}
```

### Trường metadata BẮT BUỘC

Các trường sau **PHẢI có** trong mỗi câu hỏi gen ra. Samples.json không chứa các trường này (vì lấy từ dữ liệu cũ), nhưng khi gen mới **BẮT BUỘC** phải thêm:

```json
// Trong content[] — thêm vào MỖI câu hỏi con:
"question_feature": "<mã từ bảng question_feature>",
"difficulty": 3,
"distractor_traps": {
  "1": "", "2": "trap_detail_distort", "3": "trap_neg_없안", "4": "trap_shared_noun"
}

// Ở cấp top-level — thêm vào MỖI câu hỏi:
"topic": "daily_routine"
```

- `topic`: chọn từ bảng **Danh mục chủ đề** bên dưới
- `question_feature`: chọn từ bảng **Đặc điểm câu hỏi** bên dưới, theo kind
- `difficulty`: lấy từ bảng **Thang độ khó** bên dưới, theo kind
- `distractor_traps`: ghi trap code cho **từng đáp án** (đáp án đúng để rỗng `""`)

### Lưu ý riêng EPS-TOPIK

| Trường | EPS-TOPIK |
|--------|-----------|
| `level` | **Luôn = 3** |
| `q_point` | **null** (EPS không tính điểm theo câu) |
| `count_question` | **Luôn là integer** = len(content). VD: 1 cho câu đơn |
| `tag` | `"read"` |
| `q_image` | URL ảnh thực (poster, biển hiệu, hình minh họa) |

### Format BẮT BUỘC cho kind có ảnh

Kind có ảnh (320001, 320003, 320004) **PHẢI** có trường `q_image_description` ở **cấp top-level** (cùng cấp `title`, `general`):

```json
{
  "q_image_description": {
    "image": "<mô tả chi tiết nội dung hình ảnh>"
  }
}
```

Cách viết mô tả: xem chi tiết trong file `kinds/{kind}.md` tương ứng.

---

## Danh mục chủ đề (topic)

### Chủ đề riêng EPS-TOPIK (Level 3)

| Code | Nhãn tiếng Anh | Kind chính |
|------|---------------|-----------|
| `factory_work` | Factory & Production | 320002, 3420004 |
| `dormitory_life` | Dormitory Life | 320003, 3420005 |
| `safety_workplace` | Workplace Safety | 320003, 3420007 |
| `wages_contract` | Wages & Contract | 320004, 3420004 |
| `korean_culture` | Korean Culture & Etiquette | 3420006, 3420007 |
| `daily_vocab` | Daily Vocabulary | 320001, 3420001, 3420002, 3420008 |

### Chủ đề chung (dùng được cho EPS)

| Code | Nhãn tiếng Anh | Tiếng Hàn |
|------|---------------|-----------|
| `daily_life` | Daily Life & Routine | 일상생활 |
| `food_restaurant` | Food & Dining | 음식/식당 |
| `shopping_price` | Shopping & Price | 쇼핑/가격 |
| `health_hospital` | Health & Hospital | 건강/병원 |
| `weather_season` | Weather & Seasons | 날씨/계절 |
| `travel` | Travel & Tourism | 여행/관광 |

---

## Chiến lược bẫy đáp án sai (distractor_trap)

### Nhóm 1: Bẫy từ vựng (Vocabulary Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_similar_word` | Similar Word | Đáp án chứa từ phát âm/dạng tương tự | 320001, 320002, 3420002, 3420003, 3420006, 3420008 |
| `trap_shared_noun` | Shared-Noun Trap | Đáp án sai chứa từ vựng giống đoạn đọc | 320002, 3420006, 3420008 |
| `trap_synonym_swap` | Synonym Swap | Thay từ đúng bằng từ đồng nghĩa nhưng sai ngữ cảnh | 320002, 3420003 |

### Nhóm 2: Bẫy phủ định (Negation Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_neg_reverse` | Negation Reverse | Đảo nghĩa phủ định | 320005 |
| `trap_neg_없안` | Negation 없/안/아니 | Đáp án sai đảo nghĩa bằng 없다/안 | 3420007 |

### Nhóm 3: Bẫy nội dung (Content Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_detail_distort` | Detail Distortion | Bóp méo chi tiết nhỏ | 320003, 320004, 320005, 3420007 |
| `trap_partial_truth` | Partial Truth | Đáp án sai chứa >50% nội dung đúng | 320004, 320005, 3420007 |
| `trap_number_shift` | Number/Time Shift | Thay đổi con số/thời gian | 320004 |
| `trap_subject_swap` | Subject Swap | Gán hành động cho sai đối tượng | 3420007 |

---

## Đặc điểm câu hỏi (question_feature)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `qf_image_word` | Image → Word/Sentence | Nhìn hình chọn từ/câu mô tả | 320001, 3420001 |
| `qf_image_qa` | Image Q&A | Nhìn hình + đọc câu hỏi → chọn đáp án | 320003, 320004, 3420005 |
| `qf_fill_blank` | Fill in Blank | Điền từ/cụm vào chỗ trống ( ) | 320002, 3420004 |
| `qf_word_relation` | Word Relationship | Tìm từ liên quan | 3420002 |
| `qf_synonym_antonym` | Synonym/Antonym | Tìm từ đồng nghĩa hoặc trái nghĩa | 3420003 |
| `qf_vocab_definition` | Vocabulary Definition | Đọc mô tả, chọn từ phù hợp | 3420008 |
| `qf_topic_identify` | Topic Identification | Đoạn văn nói về chủ đề gì? | 3420006 |
| `qf_content_match` | Content Matching | Chọn phát biểu khớp nội dung | 3420007 |
| `qf_multi_passage` | Multi-Question Passage | Đoạn văn + 2 câu hỏi | 320005 |

---

## Định dạng văn bản đọc (text_format)

| Code | Mô tả | Độ dài trung bình | Kind chính |
|------|-------|:-----------------:|-----------|
| `text_dialog_eps` | Hội thoại 가/나 ngắn (EPS) | 30-80 ký tự | 320002, 3420004 |
| `text_image_only` | Chỉ có hình, không text | Ảnh | 320001, 3420001, 320003 |
| `text_single_word` | Từ đơn hoặc cụm ngắn | 2-10 ký tự | 3420002, 3420003, 3420008 |
| `text_paragraph_short` | Đoạn văn ngắn (3-5 câu) | 50-100 ký tự | 320004, 3420006, 3420007 |
| `text_paragraph_long` | Đoạn văn dài (6+ câu) | 150-300 ký tự | 320005 |
| `text_passage_multi` | Đoạn dài + nhiều câu hỏi | 150-500 ký tự (g_text) | 320005 |

---

## Ngữ pháp đáp án (answer_grammar)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `ans_noun_phrase` | Đáp án là danh từ/cụm danh từ | 320001, 320002, 320003, 320004, 320005, 3420002, 3420003, 3420006, 3420008 |
| `ans_sentence_long` | Đáp án là câu dài (20+ ký tự) | 3420007 |

---

## Thang độ khó (Difficulty Scale)

| Mức | Kind | Kiểu suy luận |
|:---:|------|--------------|
| 1 | 320001, 3420001 | `image_recognition` — Nhận diện từ qua hình |
| 2 | 3420002, 3420003, 3420008 | `vocab_match` — Từ vựng đơn giản |
| 3 | 320002, 3420004 | `context_fill` — Điền chỗ trống dựa ngữ cảnh |
| 4 | 320003, 3420005, 3420006 | `detail_extraction` — Trích xuất chi tiết từ hình/văn |
| 5 | 3420007 | `content_matching` — So khớp nội dung |
| 7 | 320004, 320005 | `paragraph_comprehension` — Hiểu đoạn văn |

---

## Cấp độ đọc EPS (reading_level)

| Level | Đặc điểm văn bản | Ngữ pháp phổ biến |
|:-----:|------------------|------------------|
| 3 (EPS) | Đoạn ngắn-trung bình, từ vựng thực tế lao động | ~(으)면, ~어야 하다, ~지 마십시오, ~(으)세요 |

---

## Quy tắc chung khi gen câu hỏi

### 1. Chất lượng nội dung tiếng Hàn
- Dùng ngữ pháp đúng level EPS (xem bảng reading_level)
- Văn bản tự nhiên, đa dạng chủ đề (lao động, an toàn, ký túc xá, lương, văn hóa Hàn, từ vựng hàng ngày)
- KHÔNG lặp lại từ vựng/ngữ cảnh giữa các câu trong cùng batch

### 2. Xây dựng đáp án sai (distractor)
- Tuân theo tỷ lệ bẫy của từng kind (xem file kind tương ứng)
- Phải hợp lý nhưng SAI về nội dung
- Tái sử dụng từ vựng bài đọc khi kind yêu cầu `trap_shared_noun`
- Đáp án sai phải cùng format/độ dài với đáp án đúng

### 3. Giải thích (explain)

**Format explain.vi và explain.en PHẢI GIỐNG NHAU về cấu trúc** — chỉ khác ngôn ngữ. Cụ thể:

```
[Dịch bài đọc/đoạn văn]

1. [Dịch đáp án 1]
2. [Dịch đáp án 2]
3. [Dịch đáp án 3]
4. [Dịch đáp án 4]
--------------------
[Dịch/tóm tắt nội dung bài đọc liên quan]

Đáp án [N] là đáp án đúng vì [lý do].
Đáp án [X] sai vì [lý do].
Đáp án [Y] sai vì [lý do].
Đáp án [Z] sai vì [lý do].
```

- **Format explain PHẢI xuống dòng rõ ràng** — mỗi phần (dịch bài, dịch đáp án, separator, dịch nội dung, giải thích từng đáp án) PHẢI xuống dòng (`\n`). KHÔNG viết thành 1 đoạn dài liền mạch. Mỗi đáp án giải thích trên 1 dòng riêng. Explain phải dễ đọc, có cấu trúc rõ ràng.
- **`q_correct` PHẢI phân bố đều 1-4** trong cùng batch (cùng kind). KHÔNG được thiên lệch — ví dụ: nếu gen 4 câu cùng kind thì phải có q_correct = 1, 2, 3, 4 (mỗi giá trị 1 lần). KHÔNG fix cứng q_correct = 1.
- **`q_correct` PHẢI là integer** (1, 2, 3, hoặc 4) — **KHÔNG BAO GIỜ** là số thập phân (1.0, 2.0, 3.0, 4.0).
- **vi** và **en** phải có **cùng số phần** và **cùng mức chi tiết**
- Nếu vi giải thích từng đáp án sai → en cũng PHẢI giải thích từng đáp án sai
- **KHÔNG** để en ngắn gọn kiểu "=> Answer 1" mà vi thì giải thích dài
- Highlight từ vựng/ngữ pháp quan trọng
- **KHÔNG dùng icon/emoji** (✅, ❌, ✓, ✗...) trong explain. Explain là text thuần, không có icon
- **Trích dẫn tiếng Hàn giữ nguyên** — khi explain dẫn từ/cụm từ/câu tiếng Hàn từ bài đọc, PHẢI giữ nguyên tiếng Hàn trong ngoặc đơn, KHÔNG dịch sang tiếng Việt hay tiếng Anh. Ví dụ: "Đoạn văn đề cập '안전 규칙을 지켜야 합니다'" — giữ nguyên phần Hàn

### 4. Số lượng
- Mặc định: 5 câu mỗi kind nếu user không chỉ định
- Tối đa: 20 câu mỗi lần

### 5. Kiểm tra sau khi gen (Validation Checklist)
- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Văn bản là tiếng Hàn tự nhiên, đúng level EPS
- [ ] Bẫy đúng phân bố của kind
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch + lý do đáp án đúng + giải thích từng đáp án sai (KHÔNG chứa mã trap)
- [ ] `count_question` khớp số phần tử trong `content` (hoặc null) — **PHẢI >= 1, KHÔNG BAO GIỜ = 0**
- [ ] `tag` = `"read"` (KHÔNG phải `"listen"`)
- [ ] `level` = 3
- [ ] `q_point` = null (EPS không tính điểm)
- [ ] Kind có ảnh → có `q_image_description`

## Workflow

1. User chỉ định kind → đọc file `kinds/{kind}.md`
2. Hỏi số lượng (mặc định 5)
3. Gen câu hỏi theo JSON format + quy tắc kind + chiến lược bẫy
4. Lưu trực tiếp CSV theo kind vào `output/read-eps/level_3/{kind}.csv` bằng `scripts/save_read.py`
5. Validate theo checklist

### Quy tắc đường dẫn file

> **⚠️ QUAN TRỌNG: Folder `skills/` là READ-ONLY khi gen. KHÔNG ĐƯỢC tạo, sửa, hay xóa bất kỳ file nào trong `skills/` trong quá trình gen câu hỏi.**

| Loại file | Đường dẫn | Ghi chú |
|-----------|-----------|---------|
| CSV theo kind | `output/read-eps/level_3/{kind}.csv` | Output chính |
| CSV tổng hợp | `output/read-eps/all_questions.csv` | Merge từ tất cả kind |

### Lưu kết quả bằng script

```bash
# Lưu trực tiếp CSV theo kind + merge tổng
python skills/topik-read-gen-eps/scripts/save_read.py --data '<JSON_STRING>' -o output/read-eps --merge

# Chỉ validate
python skills/topik-read-gen-eps/scripts/save_read.py --data '<JSON_STRING>' --validate-only

# Append thêm batch mới
python skills/topik-read-gen-eps/scripts/save_read.py --data '<JSON_STRING>' --append
```
