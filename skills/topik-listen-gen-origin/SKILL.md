# TOPIK Listening Question Generator (TOPIK I & II)

Skill tạo câu hỏi phần Nghe (듣기) cho kỳ thi TOPIK I & II theo đúng format JSON của hệ thống Migii.

## Khi nào dùng skill này

- Khi user yêu cầu tạo/gen câu hỏi nghe TOPIK I hoặc TOPIK II
- Khi user chỉ định kind cụ thể (ví dụ: "gen 110001", "tạo câu hỏi dạng 210006")
- Khi user yêu cầu tạo đề thi nghe TOPIK (Level 1-2)

## Cấu trúc thư mục

```
skills/topik-listen-gen-origin/
├── SKILL.md              ← File này (overview + quy tắc chung)
├── scripts/
│   └── save_listen.py    ← Script lưu CSV/JSON theo kind
├── kinds/                ← Quy tắc chi tiết từng dạng
│   ├── 110001.md         Hỏi-đáp đơn giản (TOPIK I)
│   ├── 110002.md         Chọn câu nối tiếp (TOPIK I)
│   ├── 110003.md         Đoán địa điểm (TOPIK I)
│   ├── 110004.md         Đoán chủ đề (TOPIK I)
│   ├── 110005.md         Chọn hình phù hợp (TOPIK I) [ảnh]
│   ├── 110006.md         Khớp nội dung (TOPIK I)
│   ├── 110007.md         Ý chính của nữ (TOPIK I)
│   ├── 110008_1.md       Hội thoại ngắn [25~26] (TOPIK I)
│   ├── 110008_2.md       Hội thoại ngắn [27~28] (TOPIK I)
│   ├── 110008_3.md       Hội thoại ngắn [29~30] (TOPIK I)
│   ├── 210001_1.md       Chọn hình phù hợp (TOPIK II) [ảnh]
│   ├── 210001_2.md       Chọn biểu đồ phù hợp (TOPIK II) [ảnh]
│   ├── 210002.md         Câu nối tiếp nâng cao (TOPIK II)
│   ├── 210003.md         Dự đoán hành động (TOPIK II)
│   ├── 210004.md         Khớp nội dung nâng cao (TOPIK II) — tổng quan
│   ├── 210004_(1).md       Khớp nội dung — Hội thoại thường ngày [13~16]
│   ├── 210004_(2).md       Khớp nội dung — Thông báo (안내) [13~16]
│   ├── 210004_(3).md       Khớp nội dung — Tin tức (뉴스) [13~16]
│   ├── 210004_(4).md       Khớp nội dung — Phỏng vấn [13~16]
│   ├── 210005.md         Ý chính của nam (TOPIK II) — tổng quan
│   ├── 210005_(1).md       Ý chính nam — Tranh luận informal [17~20]
│   ├── 210005_(2).md       Ý chính nam — Phỏng vấn/talkshow [17~20]
│   ├── 210006.md         2 câu hỏi / hội thoại (TOPIK II) — tổng quan
│   ├── 210006_(1).md       2 câu hỏi — Dialog informal [21~22]
│   ├── 210006_(2).md       2 câu hỏi — Dialog công sở [23~24]
│   ├── 210006_(3).md       2 câu hỏi — Phỏng vấn formal [25~26]
│   ├── 210006_(4).md       2 câu hỏi — Tranh luận [27~28]
│   ├── 210006_(5).md       2 câu hỏi — Talkshow nghề nghiệp [29~30]
│   ├── 210006_(6).md       2 câu hỏi — Tranh luận chính sách [31~32]
│   ├── 210006_(7).md       2 câu hỏi — 여 monologue bài giảng [33~34]
│   ├── 210006_(8).md       2 câu hỏi — 남 monologue diễn văn [35~36]
│   ├── 210007.md         Chương trình giáo dục (TOPIK II) — tổng quan
│   ├── 210007_(1).md       Tọa đàm — 남 hỏi, 여 trả lời [37~38]
│   ├── 210007_(2).md       Tọa đàm — 여 hỏi, 남 trả lời [39~40]
│   ├── 210007_(3).md       Tọa đàm — 여 monologue bài giảng [41~42]
│   ├── 210007_(4).md       Tọa đàm — 남 monologue tường thuật [43~44]
│   ├── 210007_(5).md       Tọa đàm — 여 bài giảng chức năng [45~46]
│   ├── 210007_(6).md       Tọa đàm — Phỏng vấn chính sách [47~48]
│   └── 210007_(7).md       Tọa đàm — 남 bài giảng triết học [49~50]
└── samples.json          ← Mẫu câu hỏi tham khảo
```

Khi gen kind cụ thể, đọc file `kinds/{kind}.md` tương ứng + file SKILL.md này.

---

## Quy tắc routing sub-kind

Một số kind được tách thành nhiều **sub-kind** (đánh dấu "tổng quan" trong cây thư mục). Mỗi sub-kind có kiểu audio, cấu trúc hội thoại, hoặc dạng câu hỏi phụ riêng biệt.

### Kind có sub-kind

| Parent kind | Sub-kinds | Tiêu chí tách |
|-------------|-----------|---------------|
| 210004 | 210004_(1), _(2), _(3), _(4) | Kiểu audio: hội thoại / 안내 / 뉴스 / phỏng vấn |
| 210005 | 210005_(1), _(2) | Kiểu audio: tranh luận / talkshow |
| 210006 | 210006_(1) ~ _(8) | Kiểu audio + pattern câu hỏi phụ |
| 210007 | 210007_(1) ~ _(7) | Kiểu chương trình: tọa đàm / bài giảng / tường thuật |

### Quy tắc gen

1. **File "tổng quan"** (vd: `210004.md`) chỉ là overview — **KHÔNG dùng trực tiếp để gen**. Luôn đọc file sub-kind cụ thể.

2. **User chỉ định parent kind** (vd: "gen 210004"):
   - Đọc file tổng quan để biết danh sách sub-kind
   - **Phân bổ đều** câu hỏi qua các sub-kind để đảm bảo đa dạng
   - Ví dụ: gen 5 câu 210004 → 1 câu 210004_(1) + 1 câu 210004_(2) + 1 câu 210004_(3) + 1 câu 210004_(4) + 1 câu random
   - Mỗi câu đọc đúng file sub-kind tương ứng để lấy quy tắc riêng

3. **User chỉ định sub-kind** (vd: "gen 210004_(3)"):
   - Đọc file sub-kind trực tiếp, gen tất cả câu theo sub-kind đó

4. **Trường `kind` trong JSON output**: Ghi **sub-kind** cụ thể (vd: `"210004_(3)"`), không ghi parent kind.

> **Lưu ý**: Các bảng topic, difficulty, trap bên dưới tham chiếu parent kind (vd: `210004`). Sub-kind kế thừa tất cả thuộc tính của parent trừ khi file sub-kind ghi đè riêng.

---

## Output Format (JSON)

Mỗi câu hỏi PHẢI tuân theo cấu trúc JSON sau:

```json
{
  "title": "<tiêu đề dạng câu hỏi bằng tiếng Hàn>",
  "general": {
    "g_text": "",
    "g_text_translate": { "vi": "", "en": "" },
    "g_text_audio": "<nội dung audio / đoạn hội thoại bằng tiếng Hàn>",
    "g_text_audio_translate": {
      "vi": "<bản dịch tiếng Việt>",
      "en": "<bản dịch tiếng Anh>"
    },
    "g_audio": "",
    "g_image": ""
  },
  "content": [
    {
      "q_text": "<câu hỏi phụ nếu có, nếu không thì để rỗng>",
      "q_image": "",
      "q_point": <điểm>,
      "q_answer": ["<đáp án 1>", "<đáp án 2>", "<đáp án 3>", "<đáp án 4>"],
      "q_correct": <số thứ tự đáp án đúng 1-4>,
      "explain": {
        "vi": "<giải thích tiếng Việt — GHI RÕ trap type cho từng đáp án sai>",
        "en": "<giải thích tiếng Anh>"
      }
    }
  ],
  "level": <1|2>,
  "kind": "<mã kind>",
  "count_question": <số câu hỏi con trong content>,
  "tag": "listen"
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

### Format BẮT BUỘC cho kind có ảnh

Kind có ảnh (110005, 210001_1, 210001_2) **PHẢI** có trường `q_image_description` ở **cấp top-level** (cùng cấp `title`, `general`), mô tả nội dung ảnh bằng text để AI tạo ảnh sau:

```json
{
  "q_image_description": {
    "1": "<mô tả nội dung hình ①>",
    "2": "<mô tả nội dung hình ②>",
    "3": "<mô tả nội dung hình ③>",
    "4": "<mô tả nội dung hình ④>"
  }
}
```

Cách viết mô tả: xem chi tiết trong file `kinds/{kind}.md` tương ứng.

---

## Danh mục chủ đề (topic)

Phân tích từ 5.701 câu hỏi nghe thực tế. Ngưỡng gán nhãn: ≥2 từ khóa khớp.

### Chủ đề chung (Level 1, 2)

| Code | Nhãn tiếng Anh | Tiếng Hàn | Từ khóa nhận diện |
|------|---------------|-----------|-------------------|
| `time_appointment` | Time & Appointments | 시간/약속 | 시간, 약속, 오전, 오후, 언제, 몇 시 |
| `workplace` | Workplace & Work | 직장/업무 | 회사, 회의, 보고서, 출근, 퇴근, 팀장, 사장, 직장, 업무 |
| `food_restaurant` | Food & Dining | 음식/식당 | 식당, 밥, 먹다, 메뉴, 주문, 요리, 커피, 음식 |
| `shopping_price` | Shopping & Price | 쇼핑/가격 | 사다, 얼마, 할인, 비싸다, 마트, 백화점, 쇼핑 |
| `health_hospital` | Health & Hospital | 건강/병원 | 병원, 아프다, 약, 의사, 운동, 진찰, 건강 |
| `weather_season` | Weather & Seasons | 날씨/계절 | 비, 눈, 덥다, 춥다, 날씨, 봄, 여름, 가을, 겨울 |
| `home_housing` | Home & Housing | 집/주거 | 집, 방, 아파트, 이사, 거실, 부엌 |
| `transport` | Transportation | 교통/이동 | 버스, 지하철, 택시, 역, 공항, 비행기, 기차, 교통 |
| `hobby_leisure` | Hobbies & Leisure | 취미/여가 | 영화, 노래, 사진, 음악, 책, 등산, 수영, 취미 |
| `travel` | Travel & Tourism | 여행/관광 | 여행, 호텔, 예약, 관광지, 해외 |
| `family_relations` | Family & Relations | 가족/관계 | 가족, 엄마, 아빠, 결혼, 아이, 부모님 |
| `school_education` | School & Education | 학교/교육 | 학교, 수업, 시험, 공부, 선생님, 대학, 도서관 |
| `phone_communication` | Phone & Communication | 전화/통신 | 전화, 번호, 메시지, 연락, 문자 |
| `culture_event` | Culture & Events | 문화/행사 | 공연, 전시, 축제, 콘서트, 미술관, 박물관 |
| `environment_society` | Environment & Society | 환경/사회 | 환경, 경제, 사회, 정책, 인구, 기술, 연구 |

**Quy tắc phân bố theo level:**
- Level 1: chủ đề đời sống đơn giản, phân bố đều
- Level 2: pha trộn 2-3 chủ đề/câu, thiên về xã hội (environment_society 3%), 210007 mang tính học thuật

---

## Chiến lược bẫy đáp án sai (distractor_trap)

### Nhóm 1: Bẫy từ vựng (Vocabulary Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_shared_noun` | Shared-Noun Trap | Đáp án sai chứa ≥2 danh từ giống audio | 110001, 110002, 110003, 110004, 110006, 110007, 210002-210007 |
| `trap_similar_word` | Similar Word | Đáp án chứa từ phát âm/dạng tương tự (e.g. 약국↔학교, 운동↔운전) | 110003, 110004 |
| `trap_partial_topic` | Partial Topic | Đáp án chỉ đề cập một phần nội dung, không phải chủ đề chính | 110004 |

### Nhóm 2: Bẫy phủ định (Negation Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_neg_없안` | Negation 없/안/아니 | Đáp án sai thêm 없다/안/아니다 để đảo nghĩa | 110001, 110002, 110006, 110007, 210002-210007 |

### Nhóm 3: Bẫy cấu trúc (Structural Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_same_ending` | Same-Ending Pattern | Cả 4 đáp án kết thúc cùng dạng ngữ pháp | 110001, 110002, 110006, 110007, 210002-210007 |

### Nhóm 4: Bẫy nội dung (Content Traps)

| Code | Nhãn tiếng Anh | Mô tả | Kind áp dụng |
|------|---------------|-------|-------------|
| `trap_subject_swap` | Subject Swap | Gán hành động/ý kiến cho sai người (남↔여) | 110006, 110008_1, 110008_2, 110008_3, 210003-210007 |
| `trap_opinion_swap` | Opinion Swap | Đáp án sai thể hiện ý kiến người nói kia | 110007, 210005 |
| `trap_detail_distort` | Detail Distortion | Bóp méo chi tiết nhỏ | 110005, 110008_1, 110008_2, 110008_3 |
| `trap_partial_truth` | Partial Truth | Đáp án sai chứa >30% từ đúng | 110006, 110008_1, 110008_2 |
| `trap_wrong_inference` | Wrong Inference | Suy luận hợp lý nhưng không được nêu | 110008_1, 110008_2, 110008_3 |
| `trap_cause_effect_swap` | Cause-Effect Swap | Đảo quan hệ nhân quả | 110006, 110008_3 |
| `trap_scope_change` | Scope Change | Thay đổi từ chỉ phạm vi: 모든↔일부 | 110006, 110007, 110008_3 |
| `trap_temporal_distort` | Temporal Distortion | Đảo biểu thức thời gian | 110006, 110008_2 |
| `trap_comparison_flip` | Comparison Flip | Đảo chiều so sánh | 110006, 210001_2 |
| `trap_action_swap` | Action Swap | Đáp án sai thay đổi hành động | 110005, 210001_1 |
| `trap_context_swap` | Context Swap | Đáp án sai thay đổi bối cảnh | 110005, 210001_1 |
| `trap_number_shift` | Number/Time Shift | Thay đổi số liệu biểu đồ | 210001_2 |

### Quy tắc gán nhãn bẫy

- Mỗi câu hỏi có thể có NHIỀU nhãn bẫy cùng lúc (ví dụ: trap_shared_noun + trap_neg_없안 + trap_same_ending)
- Gán nhãn dựa trên ĐÁP ÁN SAI, không phải đáp án đúng
- Chỉ gán khi có bằng chứng rõ ràng, không suy đoán

---

## Đặc điểm câu hỏi (question_feature)

Nhãn gán cho q_text — xác định kiểu thông tin cần trích xuất.

### Nhóm câu hỏi có q_text

| Code | Nhãn tiếng Anh | Mô tả | Số lượng |
|------|---------------|-------|:--------:|
| `qf_content_match` | Content Match | "들은 내용으로 맞는 것을 고르십시오" | 733 |
| `qf_what` | What (General) | "무엇입니까?", "무엇을 삽니까?" | 409 |
| `qf_what_doing` | What Doing | "무엇을 하고 있습니까?" | 228 |
| `qf_where` | Where/Which | "어디입니까?", "어느 나라?" | 223 |
| `qf_central_thought` | Central Thought | "중심 생각으로 맞는 것" | 120 |
| `qf_attitude` | Attitude/Manner | "태도로 맞는 것을 고르십시오" | 126 |
| `qf_why` | Why/Reason | "왜?", "이유" | 122 |
| `qf_when_time` | When/Time | "언제?", "몇 시?", "얼마 동안?" | 117 |
| `qf_who` | Who | "누구입니까?" | 72 |
| `qf_how_many` | How Many | "몇 명?", "몇 개?" | 53 |
| `qf_intention` | Intention | "말하는 의도를 고르십시오" | 42 |
| `qf_how_much` | How Much (Price) | "얼마입니까?" | 35 |
| `qf_how` | How/Method | "어떻게?", "방법" | 34 |

### Nhóm câu hỏi KHÔNG có q_text

Kiểu câu hỏi xác định từ kind + title, không cần q_text:

| Code | Kind áp dụng | Mô tả |
|------|-------------|-------|
| `qf_direct_qa` | 110001 | Nghe câu hỏi → chọn câu trả lời trực tiếp |
| `qf_next_utterance` | 110002, 210002 | Nghe hội thoại → chọn câu nối tiếp |
| `qf_guess_place` | 110003 | Nghe → đoán địa điểm |
| `qf_guess_topic` | 110004 | Nghe → đoán chủ đề đang nói |
| `qf_match_image` | 110005, 210001_1 | Nghe → chọn hình khớp |
| `qf_match_graph` | 210001_2 | Nghe số liệu → chọn biểu đồ |
| `qf_match_content` | 110006, 210004 | Nghe → chọn phát biểu khớp nội dung |
| `qf_predict_action` | 210003 | Nghe → dự đoán hành động tiếp theo |
| `qf_main_opinion` | 110007, 210005 | Nghe → xác định ý kiến chính (남/여) |
| `qf_multi_comprehension` | 110008_1, 110008_2, 110008_3, 210006 | Nghe dài và trả lời 2 câu hỏi |

---

## Cấu trúc ngữ pháp trong audio (grammar_semantic)

Phân tích ngữ pháp theo Ý NGHĨA — phát hiện thực tế từ audio 5.701 câu.

### Phân bố theo level (chỉ liệt kê ≥5%)

**Level 1 (1.692 câu):**
gram_honorific_시(35%), gram_request_세요(34%), gram_cond_면(16%), gram_contrast_는데(14%), gram_cause_니까(12%), gram_honorific_습니다(12%), gram_cause_어서(11%), gram_intent_겠(11%), gram_request_주세요(11%), gram_intent_려고(7%), gram_purpose_러(6%), gram_contrast_지만(6%)

**Level 2 (1.767 câu):**
gram_cond_면(50%), gram_honorific_습니다(47%), gram_contrast_는데(45%), gram_cause_니까(26%), gram_prog_고있(24%), gram_intent_겠(22%), gram_contrast_지만(22%), gram_honorific_시(21%), gram_request_세요(17%), gram_cause_어서(17%), gram_time_면서(14%), gram_cause_때문(14%), gram_compare_보다(10%), gram_result_게되(10%)

### Bảng nhãn ngữ pháp theo ý nghĩa

| Code | Cấu trúc | Ý nghĩa | L1 | L2 |
|------|----------|---------|:--:|:--:|
| `gram_cause_어서` | ~어서/아서 | Nguyên nhân (nhẹ) | 11% | 17% |
| `gram_cause_니까` | ~니까 | Nguyên nhân (nhấn mạnh) | 12% | 26% |
| `gram_cause_때문` | ~때문에 | Nguyên nhân (danh từ hóa) | — | 14% |
| `gram_cond_면` | ~(으)면 | Điều kiện | 16% | 50% |
| `gram_contrast_지만` | ~지만 | Đối lập trực tiếp | 6% | 22% |
| `gram_contrast_는데` | ~는데/은데 | Bối cảnh/đối lập mềm | 14% | 45% |
| `gram_intent_려고` | ~(으)려고 | Ý định | 7% | — |
| `gram_intent_겠` | ~겠어요/겠습니다 | Dự định/suy đoán | 11% | 22% |
| `gram_ability_수있` | ~(을) 수 있다 | Khả năng (có thể) | — | — |
| `gram_request_세요` | ~(으)세요 | Yêu cầu lịch sự | 34% | 17% |
| `gram_request_주세요` | ~주세요 | Nhờ vả cụ thể | 11% | — |
| `gram_compare_보다` | ~보다 | So sánh | — | 10% |
| `gram_compare_제일` | 제일/가장 | So sánh nhất | — | 8% |
| `gram_prog_고있` | ~고 있다 | Đang diễn ra | — | 24% |
| `gram_result_게되` | ~게 되다 | Kết quả thay đổi | — | 10% |
| `gram_time_면서` | ~면서 | Đồng thời | — | 14% |
| `gram_time_동안` | ~동안 | Khoảng thời gian | — | 7% |
| `gram_honorific_시` | ~시/셨/세요 | Kính ngữ (시) | 35% | 21% |
| `gram_honorific_습니다` | ~습니다/ㅂ니다 | Kính ngữ trang trọng | 12% | 47% |
| `gram_purpose_기위해` | ~기 위해(서) | Mục đích (formal) | — | 8% |
| `gram_purpose_러` | ~(으)러 | Mục đích (đi đâu) | 6% | 7% |

*Ghi chú: "—" = dưới 5%, vẫn tồn tại nhưng không đủ phổ biến để làm nhãn chính.*

### Ngữ pháp trong đáp án (answer_grammar)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `ans_informal_polite` | Đáp án dùng ~어요/아요 | 110001, 110002 |
| `ans_noun_phrase` | Đáp án là danh từ/cụm danh từ | 110003, 110004, 110008_2 (Q1) |
| `ans_image` | Đáp án là hình ảnh (không có text) | 110005, 210001_1, 210001_2 |
| `ans_formal_polite` | Đáp án dùng ~ㅂ니다/습니다 | 110006, 110007, 210002, 110008_1 (Q2), 110008_2 (Q2), 110008_3 (Q2) |
| `ans_plain_form` | Đáp án dùng thể trần thuật (~ㄴ다/한다/이다) | 210003, 210004, 210005, 210006, 210007 |
| `ans_purpose_phrase` | Đáp án dùng ~기 위해 (mục đích) | 110008_1 (Q1) |
| `ans_reason_phrase` | Đáp án dùng ~아/어서 (lý do) | 110008_3 (Q1) |

---

## Cấu trúc audio (audio_format)

| Code | Mô tả | Số lượng | Kind chính |
|------|-------|:--------:|-----------|
| `audio_dialog_short` | Hội thoại 남/여 ngắn (1-2 lượt) | ~720 | 110003-110005, 210001_1 |
| `audio_dialog_medium` | Hội thoại 남/여 trung bình (3-4 lượt) | 1.547 | 110006-110007, 210002-210005 |
| `audio_dialog_long` | Hội thoại 남/여 dài (5+ lượt) | 302 | 210006, 210007 |
| `audio_single_sentence` | Câu đơn (15-50 ký tự) | ~830 | 110001, 110002 |
| `audio_monologue` | Độc thoại/tin tức/bài giảng | 477 | 210001_2, 210007 |

---

## Thang độ khó (Difficulty Scale)

| Mức | Kind | Kiểu suy luận | Nhãn |
|:---:|------|--------------|------|
| 2 | 110001 | `direct_match` | Hỏi-đáp đơn giản |
| 3 | 110002 | `pragmatic_response` | Chọn câu nối tiếp |
| 4 | 110003, 110004 | `keyword_inference` | Đoán địa điểm/chủ đề |
| 5 | 110005 | `scene_matching` | Chọn hình |
| 6 | 110006, 210002, 210001_1 | `content_matching` / `scene_matching` | Khớp nội dung |
| 7 | 210003, 210004, 210001_2 | `action_prediction` / `graph_matching` | Hành động / biểu đồ |
| 8 | 110007, 210005, 110008_1, 110008_2, 110008_3, 210006 | `opinion_extraction` / `multi_comprehension` | Ý chính / 2 câu hỏi |
| 9 | 210007 | `academic_comprehension` | Chương trình giáo dục |

### Mô tả kiểu suy luận (reasoning_type)

| Code | Mô tả |
|------|-------|
| `direct_match` | Ghép câu hỏi với câu trả lời trực tiếp |
| `pragmatic_response` | Chọn phản hồi phù hợp ngữ cảnh giao tiếp |
| `keyword_inference` | Suy luận địa điểm/chủ đề từ từ khóa |
| `scene_matching` | Nghe audio, chọn bức tranh minh họa khớp |
| `detail_extraction` | Trích xuất chi tiết cụ thể từ hội thoại |
| `content_matching` | So khớp phát biểu với nội dung hội thoại |
| `graph_matching` | Nghe số liệu, chọn biểu đồ khớp |
| `action_prediction` | Dự đoán hành động tiếp theo |
| `opinion_extraction` | Xác định ý kiến/quan điểm chính |
| `multi_comprehension` | Trả lời 2 câu hỏi từ 1 đoạn |
| `academic_comprehension` | Hiểu nội dung phỏng vấn/tọa đàm chuyên sâu |

---

## Cấp độ giao tiếp trong audio (speech_level)

Xác định mức trang trọng khi tạo audio. Chi tiết ngữ pháp cụ thể → xem phần [grammar_semantic](#cấu-trúc-ngữ-pháp-trong-audio-grammar_semantic).

| Level | Audio chính | Đáp án |
|:-----:|------------|--------|
| 1 | `informal_polite` (~어요/세요) 46%, `connective` (~니까/는데) 19% | `informal_polite` |
| 2 | `modifier` (~ㄴ/는) 31%, `connective` 27%, `formal_polite` (~ㅂ니다) 16% | `plain_form` (~ㄴ다/한다) — xem answer_grammar |

**Quy tắc**: Audio Level 1 dùng `informal_polite`. Audio Level 2 pha trộn. **Đáp án** Level 2 thường dùng `plain_form`.

---

## Quy tắc chung khi gen câu hỏi

### 1. Chất lượng nội dung tiếng Hàn
- Dùng ngữ pháp đúng level (xem bảng speech_level + grammar_semantic)
- Hội thoại tự nhiên, đa dạng chủ đề đời sống
- KHÔNG lặp lại từ vựng/ngữ cảnh giữa các câu trong cùng batch
- Level 2: pha trộn 2-3 topic categories mỗi câu

### 2. Xây dựng đáp án sai (distractor)
- Tuân theo tỷ lệ bẫy của từng kind (xem file kind tương ứng)
- Phải hợp lý nhưng SAI về nội dung
- Tái sử dụng từ vựng audio khi kind yêu cầu `shared_word`

### 3. Giải thích (explain)
- **vi**: Dịch cả 4 đáp án → dấu `--------------------` → giải thích đáp án đúng
- **en**: Tương tự bằng tiếng Anh
- Highlight từ vựng/ngữ pháp quan trọng
- **KHÔNG thêm annotation trap** trong ngoặc sau mỗi đáp án (vd: KHÔNG viết "② Nữ đang chơi game (trap_context_swap)"). Thông tin trap đã nằm trong trường `distractor_traps` riêng
- **Dùng "người nam" thay cho "남"** và **"người nữ" thay cho "nữ"** trong explain tiếng Việt (vd: "Người nam đang giải thích..." thay vì "Nam đang giải thích...")
- Với kind có **câu hỏi phụ** (110008_1/2/3, 210006, 210007): explain PHẢI **dịch cả câu hỏi phụ** (q_text) trước khi dịch đáp án

### 4. Số lượng
- Mặc định: 5 câu mỗi kind nếu user không chỉ định
- Tối đa: 20 câu mỗi lần

### 5. Kiểm tra sau khi gen (Validation Checklist)
- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Audio là tiếng Hàn tự nhiên
- [ ] Ngữ pháp đúng level
- [ ] Bẫy đúng phân bố của kind
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch 4 đáp án + lý do đáp án đúng
- [ ] `count_question` khớp số phần tử trong `content`

## Workflow

1. User chỉ định kind → kiểm tra có sub-kind không (xem bảng **Quy tắc routing sub-kind**)
   - Có sub-kind → đọc file tổng quan, phân bổ đều qua sub-kinds, đọc từng file sub-kind
   - Không có sub-kind → đọc file `kinds/{kind}.md` trực tiếp
2. Hỏi số lượng (mặc định 5)
3. Gen câu hỏi theo JSON format + quy tắc kind + chiến lược bẫy
4. Lưu JSON tạm → chạy `scripts/save_listen.py` để tách CSV theo kind
5. Validate theo checklist

### Lưu kết quả bằng script

```bash
# Lưu CSV theo kind + JSON + merge tổng
python skills/topik-listen-gen-origin/scripts/save_listen.py gen_temp.json -o output/listen-origin --json --merge

# Chỉ validate
python skills/topik-listen-gen-origin/scripts/save_listen.py gen_temp.json --validate-only

# Append thêm batch mới
python skills/topik-listen-gen-origin/scripts/save_listen.py new_batch.json --append
```

Output: `output/listen-origin/level_{1,2}/{kind}.csv`
