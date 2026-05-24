# EPS-TOPIK Listening Question Generator (Level 3)

Skill tạo câu hỏi phần Nghe (듣기) cho kỳ thi EPS-TOPIK (Level 3 — dành cho người lao động nước ngoài tại Hàn Quốc) theo đúng format JSON của hệ thống Migii.

## Khi nào dùng skill này

- Khi user yêu cầu tạo/gen câu hỏi nghe EPS-TOPIK
- Khi user chỉ định kind cụ thể (ví dụ: "gen 310001", "tạo câu hỏi dạng 3410005")
- Khi user yêu cầu tạo đề thi nghe EPS

## Cấu trúc thư mục

```
skills/topik-listen-gen-eps/
├── SKILL.md              ← File này (overview + quy tắc chung)
├── scripts/
│   └── save_listen.py    ← Script lưu CSV/JSON theo kind
├── kinds/                ← Quy tắc chi tiết từng dạng
│   ├── 310001.md         Nhận diện từ/câu (EPS, gồm 3410001)
│   ├── 310002.md         Nhìn hình chọn đáp án (EPS, gồm 3410003) [ảnh]
│   ├── 310003.md         Chọn hình liên quan (EPS, gồm 3410006) [ảnh]
│   ├── 310004.md         Hỏi-đáp EPS (gồm 3410004)
│   ├── 310005.md         Trích xuất chi tiết (EPS, gồm 3410007)
│   ├── 310006.md         2 câu hỏi EPS
│   ├── 3410002.md        Nhận diện giờ (EPS) [ảnh]
│   └── 3410005.md        Chọn câu nối tiếp EPS (pragmatic_response)
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
      "q_point": <điểm hoặc null>,
      "q_answer": ["<dap an 1>", "<dap an 2>", "<dap an 3>", "<dap an 4>"],
      "q_correct": <số thứ tự đáp án đúng 1-4>,
      "explain": {
        "vi": "<giải thích tiếng Việt — GHI RÕ trap type cho từng đáp án sai>",
        "en": "<giải thích tiếng Anh>"
      }
    }
  ],
  "level": 3,
  "kind": "<mã kind>",
  "count_question": <số câu hỏi con trong content>,
  "tag": "listen"
}
```

### Trường tùy chọn (OPTIONAL — chỉ thêm nếu cần phân tích chuyên sâu)

Các trường sau **KHÔNG bắt buộc** khi gen câu hỏi. Samples.json không chứa các trường này. Chỉ thêm khi user yêu cầu phân tích metadata:

```json
// Trong content[]:
"question_feature": "<mã từ bảng question_feature>",
"difficulty": 3,
"distractor_traps": {
  "1": "", "2": "trap_same_ending", "3": "trap_neg_없안", "4": "trap_shared_noun"
}

// Ở cấp top-level:
"topic": "daily_routine"
```

### Format bổ sung cho kind có ảnh

Thêm trường `q_image_description` mô tả nội dung ảnh bằng text:

```json
{
  "q_image_description": {
    "1": "<mô tả nội dung hình 1>",
    "2": "<mô tả nội dung hình 2>",
    "3": "<mô tả nội dung hình 3>",
    "4": "<mô tả nội dung hình 4>"
  }
}
```

Với kind 310002/3410003 (chỉ 1 bức tranh, đáp án trong audio):
```json
{
  "q_image_description": {
    "image": "<mô tả bức tranh duy nhất>"
  }
}
```

> ⚠️ **Lưu ý**: `q_image_description` là trường **chỉ dùng khi gen câu hỏi mới** — dùng để mô tả ảnh bằng text cho AI tạo ảnh sau. Trường này KHÔNG có trong `samples.json` (vì samples lấy từ dữ liệu thực đã có ảnh URL). Đặt ở **cấp top-level** của JSON (cùng cấp với `title`, `general`).

---

## Danh mục chủ đề (topic)

### Chủ đề chung (áp dụng cho EPS)

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
| `phone_communication` | Phone & Communication | 전화/통신 | 전화, 번호, 메시지, 연락, 문자 |

### Chủ đề riêng EPS-TOPIK (Level 3)

Phát hiện từ dữ liệu 2.242 câu EPS — các chủ đề đặc thù cho người lao động nước ngoài:

| Code | Nhãn tiếng Anh | Từ khóa nhận diện | Tỷ lệ (L3) |
|------|---------------|-------------------|:-----------:|
| `factory_work` | Factory & Production | 공장, 기계, 작업, 생산, 제품, 부품, 조립, 포장 | 5% |
| `dormitory_life` | Dormitory Life | 기숙사, 룸메이트, 세탁기, 청소, 방, 규칙, 소음 | 6% |
| `safety_workplace` | Workplace Safety | 안전, 사고, 위험, 보호, 장갑, 안전모, 소화기 | 2% |
| `wages_contract` | Wages & Contract | 월급, 급여, 계약, 근무, 야근, 휴일, 수당 | 3% |

---

## Chiến lược bẫy đáp án sai (distractor_trap)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `trap_sound_similarity` | 4 đáp án phát âm gần giống nhau | 310001, 3410002 |
| `trap_shared_noun` | Đáp án sai chứa >=2 danh từ giống audio | 310004, 310005, 310006, 3410005 |
| `trap_same_ending` | Cả 4 đáp án kết thúc cùng dạng ngữ pháp | 310001, 310004, 310005, 310006, 3410005 |
| `trap_neg_없안` | Đáp án sai thêm 없다/안/아니다 để đảo nghĩa | 310001, 310004, 310005, 3410005 |
| `trap_subject_swap` | Gán hành động cho sai người (가↔나) | 310005, 310006 |

### Quy tắc gán nhãn bẫy

- Mỗi câu hỏi có thể có NHIỀU nhãn bẫy cùng lúc
- Gán nhãn dựa trên ĐÁP ÁN SAI, không phải đáp án đúng
- Chỉ gán khi có bằng chứng rõ ràng, không suy đoán

---

## Đặc điểm câu hỏi (question_feature)

### Nhóm câu hỏi có q_text

| Code | Nhãn tiếng Anh | Mô tả |
|------|---------------|-------|
| `qf_content_match` | Content Match | "들은 내용으로 맞는 것을 고르십시오" |
| `qf_what` | What (General) | "무엇입니까?", "무엇을 삽니까?" |
| `qf_what_doing` | What Doing | "무엇을 하고 있습니까?" |
| `qf_where` | Where/Which | "어디입니까?", "어느 나라?" |
| `qf_central_thought` | Central Thought | "중심 생각으로 맞는 것" |
| `qf_why` | Why/Reason | "왜?", "이유" |
| `qf_when_time` | When/Time | "언제?", "몇 시?", "얼마 동안?" |
| `qf_who` | Who | "누구입니까?" |
| `qf_how_many` | How Many | "몇 명?", "몇 개?" |
| `qf_how_much` | How Much (Price) | "얼마입니까?" |

### Nhóm câu hỏi KHÔNG có q_text

| Code | Kind áp dụng | Mô tả |
|------|-------------|-------|
| `qf_direct_qa` | 310004 | Nghe câu hỏi -> chọn câu trả lời trực tiếp |
| `qf_next_utterance` | 3410005 | Nghe hội thoại -> chọn câu nối tiếp |
| `qf_match_image` | 310003 | Nghe -> chọn hình khớp |
| `qf_match_content` | 310005 | Nghe -> chọn phát biểu khớp nội dung |
| `qf_identify_sound` | 310001 | Nghe -> nhận diện từ/câu |
| `qf_identify_time` | 3410002 | Nghe giờ -> chọn đồng hồ |
| `qf_image_qa` | 310002 | Nhìn hình + nghe 4 câu mô tả -> chọn đúng |
| `qf_multi_comprehension` | 310006 | Nghe dài và trả lời 2 câu hỏi |

---

## Cấu trúc ngữ pháp trong audio (grammar_semantic)

### Phân bố Level 3 (2.242 câu, chỉ liệt kê >=5%)

gram_honorific_시(21%), gram_request_세요(19%), gram_honorific_습니다(18%), gram_cause_니까(8%), gram_cond_면(7%), gram_contrast_는데(7%), gram_prog_고있(6%), gram_intent_겠(6%), gram_cause_어서(5%)

### Bảng nhãn ngữ pháp theo ý nghĩa (Level 3)

| Code | Cấu trúc | Ý nghĩa | L3 |
|------|----------|---------|:--:|
| `gram_cause_어서` | ~어서/아서 | Nguyên nhân (nhẹ) | 5% |
| `gram_cause_니까` | ~니까 | Nguyên nhân (nhấn mạnh) | 8% |
| `gram_cond_면` | ~(으)면 | Điều kiện | 7% |
| `gram_contrast_지만` | ~지만 | Đối lập trực tiếp | 3% |
| `gram_contrast_는데` | ~는데/은데 | Bối cảnh/đối lập mềm | 7% |
| `gram_intent_려고` | ~(으)려고 | Ý định | 4% |
| `gram_intent_겠` | ~겠어요/겠습니다 | Dự định/suy đoán | 6% |
| `gram_request_세요` | ~(으)세요 | Yêu cầu lịch sự | 19% |
| `gram_request_주세요` | ~주세요 | Nhờ vả cụ thể | 4% |
| `gram_prog_고있` | ~고 있다 | Đang diễn ra | 6% |
| `gram_honorific_시` | ~시/셨/세요 | Kính ngữ (시) | 21% |
| `gram_honorific_습니다` | ~습니다/ㅂ니다 | Kính ngữ trang trọng | 18% |

### Ngữ pháp trong đáp án (answer_grammar)

| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `ans_word_phrase` | Đáp án là từ đơn / cụm ngắn | 310001 |
| `ans_formal_polite` | Đáp án dùng ~ㅂ니다/습니다 | 310002 |
| `ans_image` | Đáp án là hình ảnh | 310003, 3410002 |
| `ans_formal` | Đáp án dùng ~ㅂ니다 | 310004, 310005, 310006 |
| `ans_informal_polite` | Đáp án dùng ~아/어요 | 3410005 |

---

## Cấu trúc audio (audio_format)

| Code | Mô tả | Kind chính |
|------|-------|-----------|
| `audio_dialog_가나` | Hội thoại 가/나 (EPS) | 310003-310006 |
| `audio_single_word` | Từ đơn/cụm ngắn (<15 ký tự) | 310001, 3410002 |
| `audio_single_sentence` | Câu đơn (15-50 ký tự) | 310004, 3410005 |
| `audio_numbered` | 4 câu mô tả đánh số (1. 2. 3. 4.) | 310002 |

---

## Thang đo khó (Difficulty Scale) — EPS kinds only

| Mức | Kind | Kiểu suy luận | Nhãn |
|:---:|------|--------------|------|
| 1 | 310001, 3410002 | `sound_recognition` / `time_recognition` | Nhận diện từ/giờ |
| 2 | 310004, 310002 | `direct_match` / `image_qa` | Hỏi-đáp đơn giản |
| 3 | 3410005 | `pragmatic_response` | Chọn câu nối tiếp |
| 4 | 310003 | `scene_matching` | Chọn hình liên quan |
| 5 | 310005 | `detail_extraction` | Trích xuất chi tiết |
| 8 | 310006 | `multi_comprehension` | 2 câu hỏi / đoạn dài |

### Mô tả kiểu suy luận (reasoning_type)

| Code | Mô tả |
|------|-------|
| `sound_recognition` | Nhận diện chính xác từ/câu được nghe |
| `time_recognition` | Nghe giờ, chọn đồng hồ phù hợp |
| `direct_match` | Ghép câu hỏi với câu trả lời trực tiếp |
| `image_qa` | Nhìn hình, nghe câu hỏi + đáp án, chọn đúng |
| `pragmatic_response` | Chọn phản hồi phù hợp ngữ cảnh giao tiếp |
| `scene_matching` | Nghe audio, chọn bức tranh minh họa khớp |
| `detail_extraction` | Trích xuất chi tiết cụ thể từ hội thoại |
| `multi_comprehension` | Trả lời 2 câu hỏi từ 1 đoạn |

---

## Cấp độ giao tiếp trong audio (speech_level)

| Level | Audio chính | Đáp án |
|:-----:|------------|--------|
| 3 | `informal_polite` 37%, `modifier` 31%, `connective` 16% | `formal_polite` (~ㅂ니다) cho EPS |

**Quy tắc**: Audio EPS dùng `informal_polite` là chính. **Đáp án** EPS thường dùng `formal_polite` (~ㅂ니다) — xem answer_grammar `ans_formal`.

---

## Quy tắc chung khi gen câu hỏi

### 1. Chất lượng nội dung tiếng Hàn
- Dùng ngữ pháp đúng Level 3 (xem bảng speech_level + grammar_semantic)
- Hội thoại tự nhiên, đa dạng chủ đề đời sống + lao động
- KHÔNG lặp lại từ vựng/ngữ cảnh giữa các câu trong cùng batch
- Pha trộn chủ đề chung + chủ đề EPS đặc thù

### 2. Xây dựng đáp án sai (distractor)
- Tuân theo tỷ lệ bẫy của từng kind (xem file kind tương ứng)
- Phải hợp lý nhưng SAI về nội dung
- Tái sử dụng từ vựng audio khi kind yêu cầu `shared_word`

### 3. Giải thích (explain)
- **vi**: Dịch cả 4 đáp án -> dấu `--------------------` -> giải thích đáp án đúng, ghi chú trap type cho từng đáp án sai
- **en**: Tương tự bằng tiếng Anh
- Highlight từ vựng/ngữ pháp quan trọng

### 4. Số lượng
- Mặc định: 5 câu mỗi kind nếu user không chỉ định
- Tối đa: 20 câu mỗi lần

### 5. Kiểm tra sau khi gen (Validation Checklist)
- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Audio là tiếng Hàn tự nhiên
- [ ] Ngữ pháp đúng Level 3
- [ ] Bẫy đúng phân bố của kind
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch 4 đáp án + lý do đáp án đúng + trap type cho đáp án sai
- [ ] `count_question` khớp số phần tử trong `content`
- [ ] `level` luôn = 3

## Workflow

1. User chỉ định kind -> đọc file `kinds/{kind}.md`
2. Hỏi số lượng (mặc định 5)
3. Gen câu hỏi theo JSON format + quy tắc kind + chiến lược bẫy
4. Lưu JSON tạm -> chạy `scripts/save_listen.py` để tách CSV theo kind
5. Validate theo checklist

### Lưu kết quả bằng script

```bash
# Lưu CSV theo kind + JSON + merge tổng
python skills/topik-listen-gen-eps/scripts/save_listen.py gen_temp.json -o output/listen-eps --json --merge

# Chỉ validate
python skills/topik-listen-gen-eps/scripts/save_listen.py gen_temp.json --validate-only

# Append thêm batch mới
python skills/topik-listen-gen-eps/scripts/save_listen.py new_batch.json --append
```

Output: `output/listen-eps/level_3/{kind}.csv`
