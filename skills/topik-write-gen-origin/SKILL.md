---
name: topik-write-gen-origin
description: "Gen câu hỏi TOPIK Viết (쓰기) Level 2. 4 dạng: 230001_1, 230001_2, 230002, 230003."
---

# TOPIK Writing Question Generator (TOPIK II)

Skill tạo câu hỏi phần Viết (쓰기) cho kỳ thi TOPIK II theo đúng format JSON của hệ thống Migii.

## Khi nào dùng skill này

- Khi user yêu cầu tạo/gen câu hỏi viết TOPIK (Level 2)
- Khi user chỉ định kind cụ thể (ví dụ: "gen 230002", "tạo câu hỏi dạng 230003")
- Khi user yêu cầu tạo đề thi viết TOPIK II

## Cấu trúc thư mục

```
skills/topik-write-gen-origin/
├── SKILL.md              ← File này (overview + quy tắc chung)
├── scripts/
│   └── save_write.py     ← Script lưu CSV/JSON theo kind
├── kinds/                ← Quy tắc chi tiết từng dạng
│   ├── 230001_1.md       Điền câu vào đoạn văn [51] (TOPIK II)
│   ├── 230001_2.md       Điền câu vào đoạn văn [52] (TOPIK II)
│   ├── 230002.md         Viết biểu đồ [53] (TOPIK II) [ảnh]
│   └── 230003.md         Trình bày quan điểm cá nhân [54] (TOPIK II)
└── samples.json          ← Mẫu câu hỏi tham khảo
```

Khi gen kind cụ thể, đọc file `kinds/{kind}.md` tương ứng + file SKILL.md này.

---

## Output Format (JSON)

Mỗi câu hỏi PHẢI tuân theo cấu trúc JSON sau:

```json
{
  "title": "<tiêu đề dạng câu hỏi bằng tiếng Hàn>",
  "general": {
    "g_text": "<đề bài viết chung — mô tả yêu cầu>",
    "g_text_translate": { "vi": "<dịch tiếng Việt>", "en": "<dịch tiếng Anh>" },
    "g_text_audio": "",
    "g_text_audio_translate": { "vi": "", "en": "" },
    "g_audio": "",
    "g_image": "<URL ảnh biểu đồ/đồ thị — chỉ kind 230002>"
  },
  "content": [
    {
      "q_text": "<đoạn văn hoặc câu hỏi phụ>",
      "q_image": "<URL ảnh đề bài — chỉ kind 230001>",
      "q_point": 2,
      "q_answer": ["<đáp án 1>", "<đáp án 2>", "<đáp án 3>", "<đáp án 4>"],
      "q_correct": 1,
      "explain": {
        "vi": "<giải thích tiếng Việt — dễ hiểu cho người học, KHÔNG ghi mã trap>",
        "en": "<giải thích tiếng Anh>"
      }
    }
  ],
  "level": 2,
  "kind": "230001_1",
  "count_question": 1,   // ⚠️ PHẢI >= 1, KHÔNG BAO GIỜ = 0
  "tag": "write",
  "topic": "<mã chủ đề từ bảng topic>",
  "example_1": "<bài viết mẫu — chỉ kind 230002 và 230003>",
  "example_2": "<bài viết mẫu>",
  "example_3": "<bài viết mẫu>",
  "example_4": "<bài viết mẫu>",
  "example_5": "<bài viết mẫu>"
}
```

### Trường metadata BẮT BUỘC

Các trường sau **PHẢI có** trong mỗi câu hỏi gen ra. Samples.json không chứa các trường này (vì lấy từ dữ liệu cũ), nhưng khi gen mới **BẮT BUỘC** phải thêm:

```json
// Trong content[] — thêm vào MỖI câu hỏi con:
"question_feature": "<mã từ bảng question_feature>",
"difficulty": 3,
"distractor_traps": {
  "1": "", "2": "trap_partial_truth", "3": "trap_grammar_connector", "4": "trap_wrong_inference"
}

// Ở cấp top-level — thêm vào MỖI câu hỏi:
"topic": "daily_routine"
```

- `topic`: chọn từ bảng **Danh mục chủ đề** bên dưới
- `question_feature`: chọn từ bảng **Đặc điểm câu hỏi** bên dưới, theo kind
- `difficulty`: lấy từ bảng **Thang độ khó** bên dưới, theo kind
- `distractor_traps`: ghi trap code cho **từng đáp án** (đáp án đúng để rỗng `""`)

### Khác biệt so với Listen/Read

| Trường | Listen | Read | Write |
|--------|--------|------|-------|
| `g_text_audio` | Nội dung audio | Luôn rỗng | Luôn rỗng |
| `g_text` | Thường rỗng | Đoạn văn chung | Đề bài viết (230002, 230003) |
| `q_text` | Câu hỏi phụ | Đoạn văn/câu hỏi | Đoạn văn cần điền hoặc câu hỏi phụ |
| `tag` | `"listen"` | `"read"` | `"write"` |
| `q_image` | Rỗng | URL ảnh | URL ảnh đề bài (230001) |
| `g_image` | Rỗng | Rỗng | URL ảnh biểu đồ (230002) |
| `level` | 1 hoặc 2 | 1 hoặc 2 | **Chỉ level 2** |

### Đặc điểm riêng của Write

- **230001_1, 230001_2**: Trắc nghiệm — chọn cặp (ㄱ)-(ㄴ) đúng điền vào đoạn văn. Đáp án là **tổ hợp 2×2** (xem chi tiết trong kind file)
- **230002**: Có `g_image` (**2 biểu đồ** + triển vọng/nguyên nhân) + `g_text` (đề bài). `count_question=3` (Q1-Q2: chọn mô tả ĐÚNG, Q3: chọn mô tả SAI). **Kèm 5 bài viết mẫu** (`example_1` đến `example_5`, 200~300 chữ)
- **230003**: Có `g_text` (đề bài 3 phần: dẫn nhập → chủ đề → 3 câu hỏi gợi ý). `count_question=10` (câu 1-4: điền từ, 5-8: chọn câu phù hợp, 9-10: sắp xếp ý). **Kèm 5 bài viết mẫu** (`example_1` đến `example_5`, 600~700 chữ)

### Format BẮT BUỘC cho kind có ảnh

- **230001_1**: Ảnh đề bài lưu trong `q_image`. Mô tả ảnh lưu trong `q_image_desc`.
- **230002**: Ảnh biểu đồ lưu trong `g_image` (1 ảnh duy nhất dùng chung cho 3 câu hỏi phụ). **BẮT BUỘC** điền `g_image_desc` — mô tả chi tiết biểu đồ theo template trong kind file (loại biểu đồ, tiêu đề, nguồn, trục, dữ liệu, xu hướng). `g_image_desc` KHÔNG ĐƯỢC rỗng. **KHÔNG** dùng `q_image_1/2/3` — phải rỗng.
- **230001_2**: KHÔNG cần ảnh.

Cách viết mô tả: xem chi tiết trong file `kinds/{kind}.md` tương ứng.

---

## Danh mục chủ đề (topic)

### Chủ đề Write (Level 2)

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

---

## Chiến lược bẫy đáp án sai (distractor_trap)

### Nhóm 1: Bẫy ngữ pháp (Grammar Traps) — chủ yếu 230001

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_grammar_ending` | Wrong Ending | Sai dạng kết thúc câu (~습니다 vs ~세요) | 230001_1 |
| `trap_grammar_connector` | Wrong Connector | Dùng sai liên từ (~기 때문에 vs ~어서) | 230001_1, 230001_2, 230003 |
| `trap_grammar_tense` | Wrong Tense | Sai thì (quá khứ/hiện tại/tương lai) | 230001_2 |

### Nhóm 2: Bẫy nội dung (Content Traps) — 230002, 230003

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_partial_truth` | Partial Truth | Đáp án sai chứa >50% nội dung đúng | 230001_1, 230001_2, 230002 |
| `trap_wrong_inference` | Wrong Inference | Suy luận hợp lý nhưng không có trong dữ liệu | 230001_2, 230002, 230003 |
| `trap_number_shift` | Number/Time Shift | Thay đổi số liệu biểu đồ | 230002 |
| `trap_comparison_flip` | Comparison Flip | Đảo chiều so sánh trong biểu đồ | 230002 |
| `trap_cause_effect_swap` | Cause-Effect Swap | Đảo quan hệ nhân quả | 230002 |
| `trap_overgeneralize` | Overgeneralization | Khái quát hóa quá mức | 230002, 230003 |
| `trap_synonym_swap` | Synonym Swap | Thay từ đồng nghĩa/gần nghĩa nhưng sai sắc thái | 230003 |

### ⚠️ CHỈ ĐÚNG 1 ĐÁP ÁN (CRITICAL)

- **TUYỆT ĐỐI chỉ có 1 đáp án đúng duy nhất.** 3 đáp án sai PHẢI rõ ràng sai, không được hợp lệ từ bất kỳ góc nhìn nào.
- Đáp án sai phải **tự mâu thuẫn nội tại** hoặc **trả lời sai loại thông tin**.
- Trước khi hoàn thành, **kiểm tra lại 3 đáp án sai**: nếu bất kỳ đáp án sai nào có thể trả lời câu hỏi một cách hợp lệ → PHẢI sửa lại.

---

## Đặc điểm câu hỏi (question_feature)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `qf_fill_blank_pair` | Fill Blank Pair | Chọn cặp (ㄱ)-(ㄴ) điền vào đoạn văn | 230001_1, 230001_2 |
| `qf_chart_comprehension` | Chart Comprehension | Hiểu biểu đồ, chọn mô tả đúng | 230002 |
| `qf_fill_word` | Fill Word | Chọn từ/ngữ pháp điền vào câu | 230003 |
| `qf_content_match` | Content Match | Chọn nội dung khớp với đề bài | 230002, 230003 |

---

## Định dạng bài viết (writing_format)

| Code | Mô tả | Đặc điểm | Kind chính |
|------|-------|----------|-----------|
| `write_fill_pair` | Đoạn văn có 2 chỗ trống (ㄱ)-(ㄴ) cần điền | Đoạn văn 3-5 câu, chủ đề sinh hoạt/giáo dục, 2 chỗ trống liên quan ngữ cảnh | 230001_1, 230001_2 |
| `write_chart_desc` | Đề bài mô tả biểu đồ/đồ thị + 3 câu hỏi phụ | g_image chứa biểu đồ, g_text mô tả yêu cầu, 3 content items hỏi về số liệu/xu hướng | 230002 |
| `write_opinion` | Đề bài trình bày quan điểm cá nhân + 10 câu hỏi phụ | g_text dài (đề bài + hướng dẫn), 10 content items: điền từ, chọn ngữ pháp, nội dung khớp | 230003 |

---

## Ngữ pháp đáp án (answer_grammar)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `ans_sentence_pair` | Đáp án là cặp câu (ㄱ)-(ㄴ), mỗi câu 5-15 ký tự | 230001_1, 230001_2 |
| `ans_sentence_long` | Đáp án là câu dài (20+ ký tự) mô tả biểu đồ | 230002 |
| `ans_word_phrase` | Đáp án là từ/cụm từ ngắn | 230003 |
| `ans_sentence_medium` | Đáp án là câu trung bình (10-20 ký tự) | 230003 |

---

## Ngữ pháp theo level (writing_grammar)

Write chỉ có trong TOPIK II (Level 2) — sử dụng ngữ pháp trung-cao cấp:

| Nhóm | Ngữ pháp | Ví dụ | Kind chính |
|------|---------|-------|-----------|
| Liên từ (연결어미) | ~(으)며, ~(으)ㄹ 뿐만 아니라, ~는 반면에, ~(으)므로 | 경제가 성장하는 반면에 환경은... | 230001_2, 230003 |
| Kết thúc câu (종결어미) | ~(으)ㄴ/는 것이다, ~아/어야 한다, ~(으)ㄹ 것이다 | 노력해야 한다 | 230001_1, 230003 |
| Danh từ hóa (명사형) | ~(으)ㅁ, ~기, ~는 것 | 증가하는 것으로 나타났다 | 230002 |
| So sánh/đối chiếu | ~에 비해, ~보다, ~(으)ㄴ/는 데 비해 | 작년에 비해 증가했다 | 230002 |
| Nguyên nhân-kết quả | ~기 때문에, ~(으)므로, ~(으)ㄴ 결과 | 변화한 결과로 | 230001_2, 230003 |
| Trích dẫn (인용) | ~(이)라고 하다, ~다고 생각하다 | ~라고 주장하는 사람들이 있다 | 230003 |

---

## Thang độ khó

| Mức | Kind | Mô tả |
|-----|------|-------|
| 1 | 230001_1 | `fill_blank_easy` — Điền câu vào đoạn văn đơn giản |
| 2 | 230001_2 | `fill_blank_medium` — Điền câu vào đoạn văn phức tạp hơn |
| 3 | 230002 | `chart_writing` — Phân tích biểu đồ và viết |
| 4 | 230003 | `opinion_writing` — Trình bày quan điểm cá nhân |

---

## Quy tắc chung khi gen

1. **tag = "write"** — luôn luôn
2. **level = 2** — Write chỉ có trong TOPIK II
3. **q_correct PHẢI là integer (1, 2, 3, hoặc 4)** — KHÔNG BAO GIỜ là số thập phân (1.0, 2.0...). PHẢI phân bố đều 1-4, KHÔNG fix cứng q_correct = 1. Khi lưu CSV, dùng `int(q_correct)` để tránh pandas ép float.
4. **explain giải thích dễ hiểu** cho từng đáp án sai (KHÔNG ghi mã trap nội bộ như `trap_grammar_ending`, `trap_grammar_connector`… vì explain dành cho người học)
5. **Chủ đề đa dạng** — không lặp lại chủ đề trong cùng batch
6. **Ngữ pháp chính xác** — đáp án đúng phải đúng ngữ pháp tiếng Hàn chuẩn
7. **Biểu đồ mô tả rõ** — kind 230002 cần `g_image_desc` chi tiết

### Giải thích (explain)

**Format explain.vi và explain.en PHẢI GIỐNG NHAU về cấu trúc** — chỉ khác ngôn ngữ. Cụ thể:

```
[Dịch câu hỏi / mô tả yêu cầu]

1. [Dịch đáp án 1]
2. [Dịch đáp án 2]
3. [Dịch đáp án 3]
4. [Dịch đáp án 4]
----------------------------
[Dịch/tóm tắt nội dung bài viết / đoạn văn liên quan]

Đáp án [N] là đáp án đúng vì [lý do].
Đáp án [X] sai vì [lý do].
Đáp án [Y] sai vì [lý do].
Đáp án [Z] sai vì [lý do].
```

- **Format explain PHẢI xuống dòng rõ ràng** — mỗi phần (dịch câu hỏi, dịch đáp án, separator, dịch nội dung, giải thích từng đáp án) PHẢI xuống dòng (`\n`). KHÔNG viết thành 1 đoạn dài liền mạch. Mỗi đáp án giải thích trên 1 dòng riêng. Explain phải dễ đọc, có cấu trúc rõ ràng.
- **`q_correct` PHẢI phân bố đều 1-4** trong cùng batch (cùng kind). KHÔNG được thiên lệch — ví dụ: nếu gen 4 câu cùng kind thì phải có q_correct = 1, 2, 3, 4 (mỗi giá trị 1 lần). KHÔNG fix cứng q_correct = 1.
- **vi** và **en** phải có **cùng số phần** và **cùng mức chi tiết**
- Nếu vi có dịch bài viết + giải thích đáp án sai → en cũng PHẢI có dịch bài viết + giải thích đáp án sai
- **KHÔNG** để en ngắn gọn kiểu "=> Answer 1" mà vi thì giải thích dài dòng
- Cả vi lẫn en đều phải giải thích **từng đáp án sai** vì sao sai
- **KHÔNG dùng icon/emoji** (✅, ❌, ✓, ✗...) trong explain. Explain là text thuần, không có icon
- **Trích dẫn tiếng Hàn giữ nguyên** — khi explain dẫn từ/cụm từ/câu tiếng Hàn từ bài viết/đoạn văn, PHẢI giữ nguyên tiếng Hàn trong ngoặc đơn, KHÔNG dịch sang tiếng Việt hay tiếng Anh. Ví dụ: "Người nam phân tích hiện tượng '양적인 관계 증가에도 질적 발전 부족'" — giữ nguyên phần Hàn
- **Danh sách đáp án trong explain phải THUẦN ngôn ngữ đích** — explain_vi chỉ có tiếng Việt, explain_en chỉ có tiếng Anh. KHÔNG trộn tiếng Hàn vào danh sách đáp án:
  - ❌ `1. 약속 (cuộc hẹn)` hoặc `1. Cuộc hẹn (약속)` hoặc `1. 음식` (chỉ Hàn)
  - ✅ explain_vi: `1. Cuộc hẹn` / explain_en: `1. Appointment`
- **Trích dẫn PHẢI dùng nháy kép ""** — tất cả trích dẫn trong explain (cả vi lẫn en) đều dùng `"..."`. KHÔNG dùng nháy đơn '...', ngoặc đơn (...), hay để trần không nháy.
- **Trích dẫn tiếng Hàn PHẢI đồng nhất giữa vi và en** — nếu explain_vi trích dẫn tiếng Hàn thì explain_en cũng PHẢI trích dẫn cùng cụm tiếng Hàn đó, KHÔNG được dịch sang tiếng Anh. Trích dẫn gốc tiếng Hàn giữ nguyên ở CẢ HAI ngôn ngữ.
- **Từ tiếng Anh trong explain_vi phải được dịch sang tiếng Việt** (ví dụ: "digital literacy" → "năng lực số")
- **Separator trong explain**: dùng `--------------------` (20 dashes), KHÔNG dùng `----` (4 dashes)
- **explain KHÔNG chứa nhãn bẫy đáp án** (trap labels) — thông tin trap đã nằm trong trường `distractor_traps`
- **Xưng hô tiếng Việt PHẢI thống nhất** — không trộn "em"+"tôi" hay "anh"+"bạn". Ưu tiên dùng **"bạn"** (ngôi 2) + **"tôi"** (ngôi 1), hoặc lược bỏ đại từ khi có thể.

### Kiểm tra sau khi gen (Validation Checklist)

- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Đáp án đúng phải đúng ngữ pháp tiếng Hàn chuẩn
- [ ] Bẫy đúng phân bố của kind (grammar traps cho 230001, content traps cho 230002/230003)
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch + lý do đáp án đúng + giải thích từng đáp án sai bằng ngôn ngữ dễ hiểu (KHÔNG chứa mã trap nội bộ)
- [ ] `count_question` khớp số phần tử trong `content` (230001: 1, 230002: 3, 230003: 10) — **PHẢI >= 1, KHÔNG BAO GIỜ = 0**
- [ ] `tag` = `"write"` (KHÔNG phải `"listen"` hay `"read"`)
- [ ] `level` = 2 (Write chỉ có trong TOPIK II)
- [ ] `q_correct` phân bố đều 1-4 trong cùng batch
- [ ] Kind 230001_1 → có `q_image` + `q_image_desc` (ảnh đoạn văn có chỗ trống)
- [ ] Kind 230002 → có `g_image` + `g_image_desc` KHÔNG RỖNG (1 ảnh biểu đồ dùng chung), `q_image_1/2/3` rỗng
- [ ] Kind 230002 → `g_image_desc` theo template: loại biểu đồ, tiêu đề, nguồn, trục, dữ liệu, xu hướng
- [ ] Kind 230002 → số liệu biểu đồ nhất quán giữa `g_image_desc` và đáp án
- [ ] Kind 230003 → `g_text` đề bài 3 phần (dẫn nhập → chủ đề → 3 câu hỏi gợi ý), đủ dài, rõ ràng
- [ ] Kind 230003 → 10 câu phụ đúng phân loại (1-4: điền từ, 5-8: chọn câu, 9-10: sắp xếp ý)
- [ ] Kind 230002, 230003 → có đủ 5 bài viết mẫu (`example_1` đến `example_5`)
- [ ] Kind 230002 → bài viết mẫu 200~300 chữ, nhất quán với biểu đồ
- [ ] Kind 230003 → bài viết mẫu 600~700 chữ, trả lời 3 câu hỏi gợi ý
- [ ] Kind 230001 → đáp án theo tổ hợp 2×2 (A/B cho ㄱ, C/D cho ㄴ)
- [ ] Chủ đề không trùng lặp trong cùng batch

## Workflow

1. User chỉ định kind → đọc file `kinds/{kind}.md` + SKILL.md
2. Hỏi số lượng (mặc định 5)
3. Gen câu hỏi theo JSON format + quy tắc kind
4. Lưu trực tiếp CSV theo kind vào `output/write-origin/level_2/{kind}.csv` bằng `scripts/save_write.py`
5. Validate theo checklist

### Quy tắc đường dẫn file

> **⚠️ QUAN TRỌNG: Folder `skills/` là READ-ONLY khi gen. KHÔNG ĐƯỢC tạo, sửa, hay xóa bất kỳ file nào trong `skills/` trong quá trình gen câu hỏi.**

| Loại file | Đường dẫn | Ghi chú |
|-----------|-----------|---------|
| CSV theo kind | `output/write-origin/level_2/{kind}.csv` | Output chính |
| CSV tổng hợp | `output/write-origin/all_questions.csv` | Merge từ tất cả kind |

### Lưu kết quả bằng script

```bash
# Lưu trực tiếp CSV theo kind + merge tổng
python skills/topik-write-gen-origin/scripts/save_write.py --data '<JSON_STRING>' -o output/write-origin --merge

# Chỉ validate
python skills/topik-write-gen-origin/scripts/save_write.py --data '<JSON_STRING>' --validate-only
```
