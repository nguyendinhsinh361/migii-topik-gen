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
        "vi": "<giải thích tiếng Việt>",
        "en": "<giải thích tiếng Anh>"
      },
      "question_feature": "<mã đặc điểm từ bảng question_feature>",
      "difficulty": <mức độ khó 1-4>,
      "distractor_traps": {
        "1": "<trap code cho đáp án 1 — rỗng nếu là đáp án đúng>",
        "2": "<trap code cho đáp án 2>",
        "3": "<trap code cho đáp án 3>",
        "4": "<trap code cho đáp án 4>"
      }
    }
  ],
  "level": 2,
  "kind": "230001_1",
  "count_question": 1,
  "tag": "write",
  "topic": "<mã chủ đề từ bảng topic>"
}
```

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

- **230001_1, 230001_2**: Câu hỏi dạng trắc nghiệm — chọn cặp (ㄱ)-(ㄴ) đúng để điền vào đoạn văn
- **230002**: Có `g_image` (biểu đồ/đồ thị) + `g_text` (đề bài). `count_question=3` (3 câu hỏi phụ về biểu đồ)
- **230003**: Có `g_text` (đề bài dài). `count_question=10` (10 câu hỏi phụ: điền từ, chọn ngữ pháp, nội dung)

### Format bổ sung cho kind có ảnh

```json
{
  "q_image_description": {
    "image": "<mô tả chi tiết nội dung hình ảnh (đoạn văn, biểu đồ)>"
  }
}
```

Áp dụng cho: 230001_1, 230001_2 (ảnh đoạn văn có chỗ trống), 230002 (ảnh biểu đồ).

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

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_grammar_ending` | Wrong Ending | Đáp án sai dùng sai dạng kết thúc câu (e.g. -습니다 vs -세요) |
| `trap_grammar_connector` | Wrong Connector | Dùng sai liên từ (e.g. -기 때문에 vs -어서 vs -니까) |
| `trap_grammar_tense` | Wrong Tense | Sai thì (quá khứ/hiện tại/tương lai) |

### Nhóm 2: Bẫy nội dung (Content Traps) — 230002, 230003

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `trap_partial_truth` | Partial Truth | Đáp án sai chứa >50% nội dung đúng |
| `trap_number_shift` | Number/Time Shift | Thay đổi số liệu biểu đồ |
| `trap_wrong_inference` | Wrong Inference | Suy luận hợp lý nhưng không có trong dữ liệu |
| `trap_overgeneralize` | Overgeneralization | Khái quát hóa quá mức |

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
| `ans_sentence_plain` | Đáp án là câu trần thuật về biểu đồ (~ㄴ다/한다) | 230002 |
| `ans_grammar_form` | Đáp án là cấu trúc ngữ pháp (liên từ, kết thúc câu) | 230003 (câu điền ngữ pháp) |
| `ans_sentence_long` | Đáp án là câu dài (20+ ký tự) mô tả nội dung | 230003 (câu nội dung) |
| `ans_noun_phrase` | Đáp án là danh từ/cụm danh từ | 230003 (câu điền từ) |

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
3. **q_correct phân bố đều 1-4** — tránh thiên lệch
4. **explain ghi rõ trap type** cho từng đáp án sai
5. **Chủ đề đa dạng** — không lặp lại chủ đề trong cùng batch
6. **Ngữ pháp chính xác** — đáp án đúng phải đúng ngữ pháp tiếng Hàn chuẩn
7. **Biểu đồ mô tả rõ** — kind 230002 cần `q_image_description` chi tiết

### Kiểm tra sau khi gen (Validation Checklist)

- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Đáp án đúng phải đúng ngữ pháp tiếng Hàn chuẩn
- [ ] Bẫy đúng phân bố của kind (grammar traps cho 230001, content traps cho 230002/230003)
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch + lý do đáp án đúng + ghi chú trap type cho từng đáp án sai
- [ ] `count_question` khớp số phần tử trong `content` (230001: 1, 230002: 3, 230003: 10)
- [ ] `tag` = `"write"` (KHÔNG phải `"listen"` hay `"read"`)
- [ ] `level` = 2 (Write chỉ có trong TOPIK II)
- [ ] `q_correct` phân bố đều 1-4 trong cùng batch
- [ ] Kind 230001 → có `q_image_description` (ảnh đoạn văn có chỗ trống)
- [ ] Kind 230002 → có `g_image` + `q_image_description` (ảnh biểu đồ)
- [ ] Kind 230002 → số liệu biểu đồ nhất quán giữa `q_image_description` và đáp án
- [ ] Kind 230003 → `g_text` đề bài đủ dài, rõ ràng
- [ ] Chủ đề không trùng lặp trong cùng batch
