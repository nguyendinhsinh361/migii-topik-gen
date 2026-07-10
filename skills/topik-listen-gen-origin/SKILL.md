---
name: topik-listen-gen-origin
description: Gen câu hỏi TOPIK Nghe (듣기) Level 1-2. Đọc kind file + samples.json, gen JSON theo format, QC, lưu CSV. 35 dạng từ 110001 đến 210007.
---

# TOPIK Listening Question Generator (TOPIK I & II)

Skill tạo câu hỏi phần Nghe (듣기) cho kỳ thi TOPIK I & II theo đúng format JSON của hệ thống Migii.

## Khi nào dùng skill này

- Khi user yêu cầu tạo/gen câu hỏi nghe TOPIK I hoặc TOPIK II
- Khi user chỉ định kind cụ thể (ví dụ: "gen 110001", "tạo câu hỏi dạng 210006")
- Khi user yêu cầu tạo đề thi nghe TOPIK (Level 1-2)

## Cấu trúc thư mục

`
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
│   ├── 210004_(1).md     Khớp nội dung — Hội thoại thường ngày [13~16]
│   ├── 210004_(2).md     Khớp nội dung — Thông báo (안내) [13~16]
│   ├── 210004_(3).md     Khớp nội dung — Tin tức (뉴스) [13~16]
│   ├── 210004_(4).md     Khớp nội dung — Phỏng vấn [13~16]
│   ├── 210005_(1).md     Ý chính nam — Tranh luận informal [17~20]
│   ├── 210005_(2).md     Ý chính nam — Phỏng vấn/talkshow [17~20]
│   ├── 210006_(1).md     2 câu hỏi — Dialog informal [21~22]
│   ├── 210006_(2).md     2 câu hỏi — Dialog công sở [23~24]
│   ├── 210006_(3).md     2 câu hỏi — Phỏng vấn formal [25~26]
│   ├── 210006_(4).md     2 câu hỏi — Tranh luận [27~28]
│   ├── 210006_(5).md     2 câu hỏi — Talkshow nghề nghiệp [29~30]
│   ├── 210006_(6).md     2 câu hỏi — Tranh luận chính sách [31~32]
│   ├── 210006_(7).md     2 câu hỏi — 여 monologue bài giảng [33~34]
│   ├── 210006_(8).md     2 câu hỏi — 남 monologue diễn văn [35~36]
│   ├── 210007_(1).md     Tọa đàm — 남 hỏi, 여 trả lời [37~38]
│   ├── 210007_(2).md     Tọa đàm — 여 hỏi, 남 trả lời [39~40]
│   ├── 210007_(3).md     Tọa đàm — 여 monologue bài giảng [41~42]
│   ├── 210007_(4).md     Tọa đàm — 남 monologue tường thuật [43~44]
│   ├── 210007_(5).md     Tọa đàm — 여 bài giảng chức năng [45~46]
│   ├── 210007_(6).md     Tọa đàm — Phỏng vấn chính sách [47~48]
│   └── 210007_(7).md     Tọa đàm — 남 bài giảng triết học [49~50]
└── samples.json          ← Mẫu câu hỏi tham khảo
`

Khi gen kind cụ thể, đọc file `kinds/{kind}.md` tương ứng + file SKILL.md này.

---

> **🔗 ĐỒNG BỘ q_image_desc ↔ explain** (dạng có ảnh): Nội dung mô tả từng ảnh trong q_image_desc PHẢI khớp chính xác với nội dung explain tương ứng. TUYỆT ĐỐI KHÔNG được ảnh mô tả một kiểu, explain giải thích kiểu khác. → Gen q_image_desc TRƯỚC, rồi viết explain DỰA TRÊN nội dung q_image_desc đã gen.
> **📌 EXPLAIN DỰA TRÊN BẰNG CHỨNG TỪ AUDIO**: Lý do loại đáp án sai PHẢI dựa trên thông tin có trong audio. Nếu audio KHÔNG nêu rõ yếu tố X (địa điểm, thời gian...) → KHÔNG dùng X làm lý do loại. Giải thích dựa trên hành động/hành vi suy luận được từ audio.
## Quy tắc routing sub-kind

Một số kind được tách thành nhiều **sub-kind**. Mỗi sub-kind có kiểu audio, cấu trúc hội thoại, hoặc dạng câu hỏi phụ riêng biệt.

> **⚠️ KHÔNG có file "tổng quan"** — KHÔNG tồn tại file `210004.md`, `210005.md`, `210006.md`, `210007.md`. Chỉ có các file sub-kind cụ thể (vd: `210004_(1).md`).

### Kind có sub-kind

| Parent kind | Sub-kind files (trong `kinds/`) | Tiêu chí tách |
|-------------|-------------------------------|---------------|
| 210004 | `210004_(1).md`, `_(2).md`, `_(3).md`, `_(4).md` | Kiểu audio: hội thoại / 안내 / 뉴스 / phỏng vấn |
| 210005 | `210005_(1).md`, `_(2).md` | Kiểu audio: tranh luận / talkshow |
| 210006 | `210006_(1).md` ~ `_(8).md` | Kiểu audio + pattern câu hỏi phụ |
| 210007 | `210007_(1).md` ~ `_(7).md` | Kiểu chương trình: tọa đàm / bài giảng / tường thuật |

### Quy tắc gen

1. **User chỉ định parent kind** (vd: "gen 210004"):
   - Tra bảng trên để biết danh sách sub-kind
   - **Phân bổ đều** câu hỏi qua các sub-kind để đảm bảo đa dạng
   - Ví dụ: gen 5 câu 210004 → 1 câu 210004_(1) + 1 câu 210004_(2) + 1 câu 210004_(3) + 1 câu 210004_(4) + 1 câu random
   - Mỗi câu đọc đúng file sub-kind tương ứng: `kinds/210004_(N).md`

2. **User chỉ định sub-kind** (vd: "gen 210004_(3)"):
   - Đọc file `kinds/210004_(3).md` trực tiếp, gen tất cả câu theo sub-kind đó

3. **Trường `kind` trong JSON output**: Ghi **sub-kind** cụ thể (vd: `"210004_(3)"`), không ghi parent kind.

> **Lưu ý**: Các bảng topic, difficulty, trap bên dưới tham chiếu parent kind (vd: `210004`). Sub-kind kế thừa tất cả thuộc tính của parent trừ khi file sub-kind ghi đè riêng.

---

## Quy tắc biên tập theo kind (độ dài / format / dấu câu)

> **Nguồn**: Biên tập viên bổ sung — *"MIGII TOPIK - Listen Rule - Gen Question AI New.xlsx"*. Đây là quy tắc BẮT BUỘC, ưu tiên cao nhất. Khi gen mỗi kind PHẢI áp dụng đúng 3 cột: **độ dài audio**, **format hội thoại**, **dấu chấm sau đáp án**.

**Cách đọc bảng:**

- **Độ dài (ký tự)**: tổng số ký tự của `g_text_audio` đếm như **Google Dịch** — **TÍNH CẢ** nhãn `남자:`/`여자:`, dấu cách, dấu câu và xuống dòng; **KHÔNG tính** dòng trống `____`. Có 2 khoảng (vd `85~95 / 140~160`) = kind có 2 cấu trúc lượt thoại; chọn 1 và đạt đúng khoảng tương ứng.
- **Thứ tự người nói**: `Đảo được` = format có ghi *"hoặc ngược lại"* → được hoán đổi nam↔nữ. `FIX` = thứ tự nam-nữ phải GIỮ ĐÚNG như cột Format, KHÔNG được đảo.
- **Format**: cấu trúc lượt thoại mẫu. `___` = dòng trống (đáp án nối tiếp). Monologue = 1 người nói liên tục.
- **Đ.án Q1 / Đ.án Q2**: dấu "." cuối đáp án cho câu hỏi con thứ 1 / thứ 2. `True` = có ".", `False` = không có ".". Dấu `—` = kind chỉ có 1 câu hỏi con.

| Kind | Độ dài (ký tự) | Thứ tự | Format hội thoại | Đ.án Q1 | Đ.án Q2 |
|------|----------------|--------|------------------|:-------:|:-------:|
| 110001 | 35~45 | Đảo được | 여: ... / 남: `___` | True | — |
| 110002 | 35~45 | Đảo được | 여: ... / 남: `___` | True | — |
| 110003 | 35~45 | Đảo được | 여: ... / 남: `___` | False | — |
| 110004 | 35~45 | Đảo được | 여: ... / 남: ... | False | — |
| 110005 | 45~55 | Đảo được | 여: ... / 남: ... (đáp án ảnh ①②③④) | False | — |
| 110006 | 85~95 (3 lượt) / 140~160 (4 lượt) | Đảo được | 여 / 남 / 여 (/ 남) | True | — |
| 110007 | 120~140 | Đảo được | 여 / 남 / 여 / 남 | True | — |
| 110008_1 | 160~180 | **FIX** | Monologue 1 người (안내/공지) | False | True |
| 110008_2 | 240~260 | Đảo được | 6 lượt 남↔여 | False | True |
| 110008_3 | 330~350 | Đảo được | 6 lượt 남↔여 (phỏng vấn) | False | True |
| 210001_1 | 65~85 | Đảo được | 여 / 남 / 여 (đáp án ảnh) | False | — |
| 210001_2 | 140~160 | **FIX** | Monologue 남 (tin tức/báo cáo, đáp án biểu đồ) | False | — |
| 210002 | 80~100 | Đảo được | 여 / 남 / 여: `___` | True | — |
| 210003 | 120~170 | Đảo được | 남 / 여 / 남 / 여 | True | — |
| 210004_(1) | 120~150 | Đảo được | 남 / 여 / 남 / 여 (hội thoại) | True | — |
| 210004_(2) | 150~180 | **FIX** | Monologue 여 (안내) | True | — |
| 210004_(3) | 140~170 | **FIX** | Monologue 남 (뉴스) | True | — |
| 210004_(4) | 170~200 | **FIX** | 남 / 여 (phỏng vấn) | True | — |
| 210005_(1) | 100~130 (3 lượt) / 140~170 (4 lượt) | **FIX** | 남/여/남 (hoặc 여/남/여/남) | True | — |
| 210005_(2) | 170~200 | **FIX** | 여 / 남 (phỏng vấn/talkshow) | True | — |
| 210006_(1) | 240~290 | **FIX** | 여 / 남 / 여 / 남 | True | True |
| 210006_(2) | 210~260 | **FIX** | 남 / 여 / 남 / 여 | True | True |
| 210006_(3) | 240~290 | **FIX** | 여 / 남 | True | True |
| 210006_(4) | 260~310 | **FIX** | 남 / 여 / 남 / 여 / 남 | False | True |
| 210006_(5) | 260~310 | **FIX** | 여 / 남 / 여 / 남 | False | True |
| 210006_(6) | 260~310 | Đảo được | 남 / 여 / 남 / 여 | True | True |
| 210006_(7) | 260~310 | **FIX** | Monologue 여 (bài giảng) | False | True |
| 210006_(8) | 260~310 | **FIX** | Monologue 남 (diễn văn) | True | True |
| 210007_(1) | 320~340 | **FIX** | 남 / 여 | True | True |
| 210007_(2) | 280~340 | **FIX** | 여 / 남 | True | True |
| 210007_(3) | 280~340 | **FIX** | Monologue 여 (bài giảng) | True | True |
| 210007_(4) | 320~340 | **FIX** | Monologue 남 (tường thuật) | False | True |
| 210007_(5) | 300~340 | **FIX** | Monologue 여 (bài giảng chức năng) | True | True |
| 210007_(6) | 300~340 | **FIX** | 여 / 남 (phỏng vấn chính sách) | True | True |
| 210007_(7) | 350~380 | **FIX** | Monologue 남 (bài giảng triết học) | True | True |

> **Lưu ý quan trọng:**
> - Với kind **FIX** thứ tự: KHÔNG được đảo nam↔nữ. Giữ đúng người nói mở đầu như cột Format (vd 210004_(3) PHẢI là 남 đọc tin tức, KHÔNG đổi sang 여).
> - Với kind **Đảo được**: có thể chọn nam hoặc nữ mở đầu, miễn nhất quán trong 1 câu. Khi gen nhiều câu nên xen kẽ để đa dạng.
> - `save_listen.py` tự động thêm/bỏ dấu "." theo bảng này (map `_ANSWER_PERIOD`, `_AUDIO_LENGTH`, `_FIXED_ORDER`) và **cảnh báo** khi độ dài audio lệch khoảng. Vẫn PHẢI gen đúng độ dài ngay từ đầu, KHÔNG ỷ lại script.

---

## Output Format (JSON)

Mỗi câu hỏi PHẢI tuân theo cấu trúc JSON sau:

`json
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
        "vi": "<giải thích tiếng Việt — dễ hiểu cho người học, KHÔNG ghi mã trap>",
        "en": "<giải thích tiếng Anh>"
      }
    }
  ],
  "level": <1|2>,
  "kind": "<mã kind>",
  "count_question": <số câu hỏi con trong content — PHẢI >= 1, KHÔNG BAO GIỜ = 0>,
  "tag": "listen"
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

### Format BẮT BUỘC cho kind có ảnh

Kind có ảnh (110005, 210001_1, 210001_2) **PHẢI** có trường `q_image_description` ở **cấp top-level** (cùng cấp `title`, `general`), mô tả nội dung ảnh bằng text để AI tạo ảnh sau:

`json
{
  "q_image_description": {
    "1": "<mô tả nội dung hình 1.>",
    "2": "<mô tả nội dung hình 2.>",
    "3": "<mô tả nội dung hình 3.>",
    "4": "<mô tả nội dung hình 4.>"
  }
}
`

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

### ⚠️ CHỈ ĐÚNG 1 ĐÁP ÁN (CRITICAL)
> **⏺ DẤU CHẤM CUỐI ĐÁP ÁN — THEO TỪNG KIND & TỪNG CÂU HỎI CON**: KHÔNG phải mọi kind đều thêm dấu ".". Tra bảng **[Quy tắc biên tập theo kind](#quy-tắc-biên-tập-theo-kind-độ-dài--format--dấu-câu)** (cột "Dấu . sau đáp án"):
> - Cột `Đ.án Q1` / `Đ.án Q2` = quy tắc cho câu hỏi con thứ 1 / thứ 2. **True** = mỗi đáp án (và mỗi dòng dịch đáp án trong explain, trước separator) PHẢI kết thúc bằng ".". **False** = KHÔNG có "." (đáp án là cụm danh từ, cụm ngắn, hoặc ảnh ①②③④).
> - Kind 2 câu hỏi (110008_*, 210006_*, 210007_*) thường KHÁC nhau: Q1 = cụm danh từ (False), Q2 = câu nội dung (True). Áp dụng đúng cho từng câu hỏi con.
> - Đáp án dạng ảnh ①②③④ KHÔNG BAO GIỜ có dấu ".".

- **TUYỆT ĐỐI chỉ có 1 đáp án đúng duy nhất.** 3 đáp án sai PHẢI rõ ràng sai, không được hợp lệ từ bất kỳ góc nhìn nào.
- Đáp án sai phải **tự mâu thuẫn nội tại** hoặc **trả lời sai loại thông tin**:
  - Yes/No: `네` + phủ định = mâu thuẫn ✅ | `아니요` + khẳng định = mâu thuẫn ✅
  - ❌ SAI: "더워요?" → "아니요, 추워요" (hợp lệ!) → Phải đổi thành "아니요, 더워요" (mâu thuẫn)
  - WH (어디/뭐/언제): đáp án sai phải trả lời sai loại (hỏi 어디 → trả lời thời gian)
- Trước khi hoàn thành, **kiểm tra lại 3 đáp án sai**: nếu bất kỳ đáp án sai nào có thể trả lời câu hỏi một cách hợp lệ → PHẢI sửa lại.

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
- **Câu mở đầu g_text_audio phải khách quan, đi thẳng vào vấn đề**. KHÔNG dùng các cụm từ mang tính chào hỏi/giới thiệu: 안녕하십니까, 말씀드리겠습니다, 발표하겠습니다, 이야기해 보겠습니다, 설명드리겠습니다, 여러분. Ví dụ: ❌ "최근 여행 선호도 조사 결과를 발표하겠습니다." → ✅ "최근 여행 선호도 조사 결과, 해외여행을 선호하는 비율이 65%로..."

### 2. Xây dựng đáp án sai (distractor)

> **⛔ 4 ĐÁP ÁN CÂN BẰNG ĐỘ DÀI (ÁP DỤNG MỌI DẠNG)**: 4 đáp án PHẢI có độ dài tương đương nhau. **ĐẶC BIỆT KHÔNG để đáp án ĐÚNG dài đột biến** so với 3 đáp án còn lại — đáp án đúng dài hơn hẳn là dấu hiệu LỘ ĐÁP ÁN (thí sinh đoán câu dài nhất là đúng). Chênh lệch độ dài tối đa ~30%. Nếu đáp án đúng đang dài hơn → RÚT GỌN đáp án đúng, hoặc bổ sung chi tiết cho các đáp án sai để 4 câu cân nhau.
- Tuân theo tỷ lệ bẫy của từng kind (xem file kind tương ứng)
- Phải hợp lý nhưng SAI về nội dung
- Tái sử dụng từ vựng audio khi kind yêu cầu `shared_word`

### 3. Bản dịch audio (`g_text_audio_translate`)
- **vi**: Nhãn người nói BẮT BUỘC dùng `Người nam:` / `Người nữ:` — KHÔNG BAO GIỜ dùng `Nam:`, `Nữ:`, `남자:`, `여자:`
- **en**: Nhãn người nói dùng `Man:` / `Woman:`
- **Dòng trống**: Nếu g_text_audio có `남자: ______________________` → vi: `Người nam: ______________________`, en: `Man: ______________________` (giữ nguyên gạch dưới)
- Số dòng bản dịch PHẢI bằng số dòng g_text_audio

### 4. Giải thích (explain)

**Format explain.vi và explain.en PHẢI GIỐNG NHAU về cấu trúc** — chỉ khác ngôn ngữ. Cụ thể:

`
[Dịch câu hỏi phụ nếu có]          ← chỉ với kind có q_text

1. [Dịch đáp án 1]
2. [Dịch đáp án 2]
3. [Dịch đáp án 3]
4. [Dịch đáp án 4]
--------------------
[Dịch/tóm tắt nội dung audio/bài đọc liên quan]

Đáp án [N] là đáp án đúng vì [lý do].
Đáp án [X] sai vì [lý do].
Đáp án [Y] sai vì [lý do].
Đáp án [Z] sai vì [lý do].
`

- **Format explain PHẢI xuống dòng rõ ràng** — mỗi phần (dịch câu hỏi phụ, dịch đáp án, separator, dịch nội dung, giải thích từng đáp án) PHẢI xuống dòng (`\n`). KHÔNG viết thành 1 đoạn dài liền mạch. Mỗi đáp án giải thích trên 1 dòng riêng. Explain phải dễ đọc, có cấu trúc rõ ràng.
- **vi** và **en** phải có **cùng số phần** (dịch đáp án, separator, dịch nội dung, giải thích) và **cùng mức chi tiết**
- Nếu vi có dịch nội dung bài → en cũng PHẢI có dịch nội dung bài
- Nếu vi giải thích từng đáp án sai → en cũng PHẢI giải thích từng đáp án sai
- **KHÔNG** để en ngắn gọn kiểu "=> Answer 1" mà vi thì giải thích dài
- Highlight từ vựng/ngữ pháp quan trọng
- **KHÔNG thêm annotation trap** trong ngoặc sau mỗi đáp án (vd: KHÔNG viết "2. Nữ đang chơi game (trap_context_swap)"). Thông tin trap đã nằm trong trường `distractor_traps` riêng
- **KHÔNG giải thích đáp án sai** theo kiểu "Đáp án X dùng từ '...' từ audio nhưng..." — việc đáp án chứa từ trùng audio là bình thường, không cần lặp lại pattern này
- **BẮT BUỘC dùng "người nam"** thay cho "nam", "anh ấy" và **"người nữ"** thay cho "nữ", "cô ấy" trong explain tiếng Việt
- Với kind có **câu hỏi phụ** (110008_1/2/3, 210006, 210007): explain PHẢI **dịch cả câu hỏi phụ** (q_text) — nhưng **KHÔNG** thêm prefix "Câu hỏi:" / "Question:" trước bản dịch, chỉ dịch trực tiếp nội dung
- **Kind 210006**: explain **KHÔNG** cần dòng "[Dịch câu hỏi phụ 1]" / "[Translate Q1]" — chỉ cần dịch đáp án + giải thích
- **Kind 210007**: explain PHẢI dịch câu hỏi phụ sang tiếng Việt/Anh — **KHÔNG** để nguyên tiếng Hàn
- **TẤT CẢ levels** (TOPIK I, TOPIK II): `q_correct` PHẢI **phân bố đều 1-4** cho TẤT CẢ levels. KHÔNG fix cứng q_correct = 1 cho bất kỳ level nào. Ví dụ: nếu gen 4 câu cùng kind thì phải có q_correct = 1, 2, 3, 4 (mỗi giá trị 1 lần). KHÔNG được thiên lệch.
- **`q_correct` PHẢI là integer** (1, 2, 3, hoặc 4) — **KHÔNG BAO GIỜ** là số thập phân (1.0, 2.0, 3.0, 4.0).
- **KHÔNG dùng icon/emoji** (✅, ❌, ✓, ✗...) trong explain. Explain là text thuần, không có icon
- **Trích dẫn tiếng Hàn giữ nguyên** — khi explain dẫn từ/cụm từ/câu tiếng Hàn từ audio, PHẢI giữ nguyên tiếng Hàn trong ngoặc đơn, KHÔNG dịch sang tiếng Việt hay tiếng Anh. Ví dụ: "Người nam nói '내일 회의가 취소됐어요'" — giữ nguyên phần Hàn
- **🔤 THẺ `<g></g>` TRONG EXPLAIN (cập nhật)**: Cột TIẾNG VIỆT (explain_vi, explain_vi_2/3…) KHÔNG dùng thẻ `<g></g>` — viết tiếng Hàn trực tiếp. Cột TIẾNG ANH (explain_en, explain_en_2/3…) PHẢI bọc `<g></g>` quanh MỌI cụm tiếng Hàn (từ/cụm/câu trích dẫn tiếng Hàn).
- **explain_vi PHẢI dịch đầy đủ 4 đáp án sang tiếng Việt** — KHÔNG được bỏ sót đáp án nào
- **Danh sách đáp án trong explain phải THUẦN ngôn ngữ đích** — explain_vi chỉ có tiếng Việt, explain_en chỉ có tiếng Anh. KHÔNG trộn tiếng Hàn vào danh sách đáp án:
  - ❌ `1. 약속 (cuộc hẹn)` hoặc `1. Cuộc hẹn (약속)` hoặc `1. 음식` (chỉ Hàn)
  - ✅ explain_vi: `1. Cuộc hẹn` / explain_en: `1. Appointment`
- **explain_vi cho câu ghép (count_question >= 2) PHẢI dịch câu hỏi phụ (q_text) sang tiếng Việt** — KHÔNG để nguyên tiếng Hàn
- **explain KHÔNG dịch lại nội dung g_text_audio** — nội dung audio đã có bản dịch ở g_text_audio_vi/en, explain chỉ cần dịch đáp án + giải thích
- **explain_vi phải là câu tiếng Việt hoàn chỉnh**. Có thể trích dẫn cụm tiếng Hàn, nhưng KHÔNG được nửa Việt nửa Hàn. Ví dụ: ❌ "Cô ấy cũng nói 갓생은 SNS에서 시작됐고, 부정적인 영향도 존재한다고 언급했다" → ✅ "Cô ấy cũng nói 갓생은 SNS에서 시작됐고, 부정적인 영향도 존재한다"
- **Trích dẫn PHẢI dùng nháy kép ""** — tất cả trích dẫn trong explain (cả vi lẫn en) đều dùng `"..."`. KHÔNG dùng nháy đơn '...', ngoặc đơn (...), hay để trần không nháy.
- **Trích dẫn tiếng Hàn PHẢI đồng nhất giữa vi và en** — nếu explain_vi trích dẫn tiếng Hàn (ví dụ: "안 늦었어요") thì explain_en cũng PHẢI trích dẫn cùng cụm tiếng Hàn đó (ví dụ: "안 늦었어요"), KHÔNG được dịch sang tiếng Anh (❌ "it's not late"). Trích dẫn gốc tiếng Hàn giữ nguyên ở CẢ HAI ngôn ngữ.
- **Từ tiếng Anh trong explain_vi phải được dịch sang tiếng Việt** (ví dụ: "digital literacy" → "năng lực số")
- **Từ tiếng Hàn đặc biệt phải được dịch, không để nguyên** (ví dụ: 천일염 → muối biển)
- **Separator trong explain**: dùng `--------------------` (20 dashes), KHÔNG dùng `----` (4 dashes)
- **explain KHÔNG chứa nhãn bẫy đáp án** (trap labels) — thông tin trap đã nằm trong trường `distractor_traps`
- **explain KHÔNG bịa phân tích ngữ âm/phát âm** — KHÔNG viết "A có phát âm gần B" trừ khi thực sự đúng. Đáp án sai chỉ cần: "không liên quan đến nội dung hội thoại"
- **explain KHÔNG bịa quan hệ giữa 2 người nói** — nếu 남자 chỉ khuyên 여자 → KHÔNG viết "hai người quyết định cùng nhau". Phân biệt rõ: ai làm gì, ai nói gì, ai quyết định gì
- **4 đáp án cân bằng độ dài** — chênh lệch tối đa ~30%. KHÔNG để 1 đáp án dài gấp 2-3 lần đáp án khác
- **⛔ CẤM KOREAN TRONG g_text_audio_vi**: g_text_audio_vi PHẢI dịch 100% sang tiếng Việt. KHÔNG được giữ nguyên bất kỳ từ Hàn nào (팀장님, 부장님, 선생님, 사장님...). Tất cả chức danh, tên riêng phải được dịch hoặc chuyển ngữ.
- **Dịch đáp án trong explain PHẢI CHÍNH XÁC nghĩa gốc tiếng Hàn** — KHÔNG dịch thoáng, KHÔNG thay đổi sắc thái. Chú ý: ~면 좋겠습니다 = "mong/ước" (KHÔNG phải "nên"), ~고 싶습니다 = "muốn", ~아야 합니다 = "phải"
- **Dịch đáp án trong explain PHẢI TỰ NHIÊN** — câu dịch phải đọc lên như câu người thật nói. KHÔNG dịch word-by-word từ tiếng Hàn. Nếu cấu trúc Hàn phức tạp → diễn đạt lại cho tự nhiên trong ngôn ngữ đích.
- **Xưng hô trong explain_vi PHẢI khớp với g_text_audio_vi** — nếu g_text_audio_vi dùng "Người nam"/"Người nữ" thì explain_vi cũng PHẢI dùng "Người nam"/"Người nữ"
- **Xưng hô tiếng Việt PHẢI thống nhất** trong g_text_audio_vi, explain_vi, và đáp án dịch. KHÔNG trộn "em" với "tôi", hoặc "anh" với "bạn". Ưu tiên dùng **"bạn"** (ngôi 2) + **"tôi"** (ngôi 1), hoặc lược bỏ đại từ khi có thể (tự nhiên nhất trong tiếng Việt).
- **⛔ XƯNG HÔ PHẢI KHỚP GIỚI TÍNH**: KHÔNG dùng đại từ sai giới tính người nghe. 남자 nói với 여자 → KHÔNG gọi "anh" (đại từ nam). 여자 nói với 남자 → KHÔNG gọi "chị" (đại từ nữ). Luôn dùng **"bạn"** cho ngôi 2 để tránh lỗi giới tính.
  - ❌ SAI: 남자→여자: "Vậy **anh** biết chỗ nào tốt không?" ("anh" = nam, nhưng đang nói với nữ)
  - ✅ ĐÚNG: 남자→여자: "Vậy **bạn** biết chỗ nào tốt không?"
  - ❌ SAI: 여자→남자: "**Chị** có thể giúp tôi được không?" ("chị" = nữ, nhưng đang nói với nam)
  - ✅ ĐÚNG: 여자→남자: "**Bạn** có thể giúp tôi được không?"
- **🏷️ CHỨC DANH DÙNG LÀM ĐẠI TỪ (BẮT BUỘC)**: Trong tiếng Hàn, chức danh (부장님, 과장님, 선생님, 사장님, 기사님, 의사 선생님...) thường được dùng làm đại từ ngôi 2 khi nói TRỰC TIẾP với người mang chức danh đó. Khi dịch, PHẢI xác định chức danh đó chỉ AI:
  - **Chỉ người ĐANG trong hội thoại** → dịch thành ngôi 2 ("bạn"/"you"), KHÔNG dịch thành chức danh ngôi 3
  - **Chỉ người THỨ BA không có mặt** → giữ nguyên chức danh ("giám đốc"/"the boss")
  - ❌ SAI: 남자 nói với 여자 (chính là 부장님): "부장님도 괜찮으실지..." → "Không biết giám đốc có ổn không nhỉ?" (dịch ngôi 3)
  - ✅ ĐÚNG: → "Không biết bạn có ổn không ạ?" (dịch ngôi 2, dùng "ạ" vì nói với cấp trên)
  - ❌ SAI (EN): "I wonder if the boss will be okay" → ✅ ĐÚNG: "I wonder if you'll be okay with it"
  - **Hậu tố kính ngữ tiếng Việt**: Khi người nói ở vị trí THẤP hơn (nhân viên nói với sếp, học sinh nói với thầy/cô) → dùng "ạ" (KHÔNG dùng "nhỉ", "nhé"). Khi ngang hàng hoặc cao hơn → dùng "nhỉ", "nhé" bình thường.

### 5. Số lượng
- Mặc định: 5 câu mỗi kind nếu user không chỉ định
- Tối đa: 20 câu mỗi lần

### 6. Kiểm tra sau khi gen (Validation Checklist)
- [ ] **4 đáp án cân bằng độ dài** — đáp án ĐÚNG KHÔNG dài đột biến so với 3 đáp án còn lại (chênh lệch ~30%); nếu lệch → rút gọn đáp án đúng / thêm chi tiết cho đáp án sai
- [ ] `q_correct` nằm trong 1-4
- [ ] 4 đáp án không trùng nhau
- [ ] Audio là tiếng Hàn tự nhiên
- [ ] Ngữ pháp đúng level
- [ ] Bẫy đúng phân bố của kind
- [ ] Bản dịch (vi/en) chính xác
- [ ] `explain` chứa dịch 4 đáp án + lý do đáp án đúng
- [ ] `count_question` khớp số phần tử trong `content` — **PHẢI >= 1, KHÔNG BAO GIỜ = 0**

## Workflow

1. User chỉ định kind → kiểm tra có sub-kind không (xem bảng **Quy tắc routing sub-kind**)
   - Có sub-kind → đọc file tổng quan, phân bổ đều qua sub-kinds, đọc từng file sub-kind
   - Không có sub-kind → đọc file `kinds/{kind}.md` trực tiếp
2. Hỏi số lượng (mặc định 5)
3. Gen câu hỏi theo JSON format + quy tắc kind + chiến lược bẫy
4. **⚠️ QC (Quality Control)** — Đọc lại TOÀN BỘ JSON vừa gen, kiểm tra từng câu theo checklist QC bên dưới. Nếu phát hiện lỗi → **sửa ngay trong JSON** trước khi lưu. KHÔNG ĐƯỢC bỏ qua bước này.
5. Lưu trực tiếp CSV theo kind vào `output/listen-origin/level_{1,2}/{kind}.csv` bằng `scripts/save_listen.py`
6. Validate theo checklist cấu trúc

### Bước 4: QC — Kiểm tra & sửa lỗi TRƯỚC KHI LƯU

> **QUAN TRỌNG**: Bước này chạy SAU khi gen xong JSON, TRƯỚC khi lưu file. Agent PHẢI đọc lại từng câu hỏi đã gen và đối chiếu với quy tắc kind. Nếu sai → sửa ngay trong JSON. Nếu không sửa được → gen lại câu đó.

#### QC-1: Cấu trúc audio (`g_text_audio`) khớp quy tắc kind

Mỗi kind có cấu trúc audio riêng được mô tả trong `kinds/{kind}.md`. Agent PHẢI kiểm tra:

- **Kind 110001, 110002**: g_text_audio PHẢI có format `여자: ...\n남자: ______________________` hoặc `남자: ...\n여자: ______________________` (có nhãn người nói + dòng trống cuối). Nếu audio chỉ có 1 câu đơn mà thiếu nhãn và dòng trống → **LỖI, phải sửa lại**.
- **Kind 210002**: g_text_audio PHẢI có **3 dòng**: 2 lượt nói + 1 dòng trống `______________________` ở cuối. Nếu thiếu dòng trống → **LỖI**.
- **Tất cả kind hội thoại** (110003-110008, 210001-210007): g_text_audio phải có nhãn `남자:`/`여자:` trước mỗi lượt nói.

#### QC-2: Bản dịch tiếng Việt (`g_text_audio_vi`)

- **PHẢI dùng** `Người nam:` và `Người nữ:` — **KHÔNG BAO GIỜ** dùng `Nam:`, `Nữ:`, `남자:`, `여자:`, `Anh:`, `Chị:`
- **Dòng trống**: Nếu g_text_audio có `남자: ______________________` thì g_text_audio_vi PHẢI có `Người nam: ______________________` (giữ nguyên gạch dưới, dịch nhãn)
- **Số dòng**: g_text_audio_vi phải có SỐ DÒNG BẰNG g_text_audio (mỗi lượt nói trong Hàn → 1 lượt nói trong Việt)
- **Nội dung**: Dịch đầy đủ, không bỏ sót câu nào

#### QC-3: Bản dịch tiếng Anh (`g_text_audio_en`)

- Dùng `Man:` và `Woman:` — KHÔNG dùng `Male:`, `Female:`, `M:`, `F:`
- Dòng trống: `Man: ______________________` hoặc `Woman: ______________________`
- Số dòng bằng g_text_audio

#### QC-4: Giải thích (`explain.vi` và `explain.en`) — format đồng bộ

- **vi và en PHẢI có cùng cấu trúc**: cùng số phần (dịch đáp án, separator `----`, dịch nội dung, giải thích), cùng mức chi tiết
- Nếu vi giải thích từng đáp án sai → en cũng PHẢI giải thích từng đáp án sai
- **KHÔNG** để en ngắn gọn kiểu "=> Answer 1" mà vi thì giải thích dài
- Dùng **"người nam"** — KHÔNG dùng "nam", "anh ấy", "người đàn ông" khi chỉ người nói nam
- Dùng **"người nữ"** — KHÔNG dùng "nữ", "cô ấy", "người phụ nữ" khi chỉ người nói nữ
- Ví dụ: ✅ "Người nam đang hỏi về..." — ❌ "Nam đang hỏi về..." / "Anh ấy hỏi về..."

#### QC-5: Không có dữ liệu placeholder/test

- g_text_audio KHÔNG chứa nội dung test mẫu
- Mỗi câu hỏi phải có nội dung audio **khác biệt**, không trùng lặp giữa các câu

#### QC-6: Độ dài audio (`g_text_audio`) theo kind

Đếm số ký tự tiếng Hàn trong `g_text_audio` (không tính nhãn `남자:`, `여자:` và dòng trống `______`). Đối chiếu **cột "Độ dài (ký tự)"** trong bảng [Quy tắc biên tập theo kind](#quy-tắc-biên-tập-theo-kind-độ-dài--format--dấu-câu) — đây là nguồn chuẩn cho TẤT CẢ 35 kind. Nếu chưa đạt khoảng → **bổ sung/cắt bớt nội dung** cho đúng, KHÔNG được bỏ qua.

**Cách đếm**: Đếm như Google Dịch — TÍNH CẢ nhãn `남자: `/`여자: `, dấu cách, dấu câu, xuống dòng; **KHÔNG tính** dòng trống `___`. Kind có 2 khoảng (110006, 210005_(1)) = 2 cấu trúc lượt thoại; đạt đúng khoảng tương ứng với số lượt đã chọn.

**Nếu thiếu**: thêm lượt thoại / chi tiết / phản hồi tự nhiên. **Nếu thừa**: rút gọn. `save_listen.py` sẽ **cảnh báo** (dòng `! Cau N ...`) nếu lệch khoảng — nhưng PHẢI gen đúng từ đầu.

#### QC-7: Thứ tự người nói (FIX vs Đảo được) + Dấu chấm sau đáp án

Đối chiếu bảng [Quy tắc biên tập theo kind](#quy-tắc-biên-tập-theo-kind-độ-dài--format--dấu-câu):

- **Thứ tự người nói**: Kind đánh dấu **FIX** → người nói mở đầu PHẢI đúng giới tính như cột Format (vd 210004_(3) = 남 đọc 뉴스, 210006_(7) = 여 monologue). KHÔNG được đảo. Kind **Đảo được** → tự do chọn nhưng nhất quán trong 1 câu.
- **Dấu "." sau đáp án** — THEO TỪNG CÂU HỎI CON:
  - Cột `Đ.án Q1` = True → mọi đáp án câu hỏi 1 kết thúc bằng ".". = False → KHÔNG có ".".
  - Cột `Đ.án Q2` (kind 2 câu hỏi) áp dụng riêng cho câu hỏi 2.
  - Mỗi dòng dịch đáp án trong `explain` (trước separator) theo CÙNG quy tắc với đáp án tương ứng.
  - Đáp án ảnh ①②③④ KHÔNG BAO GIỜ có ".".
  - `save_listen.py` tự động chuẩn hóa dấu "." theo `_ANSWER_PERIOD` — nhưng explain nên viết đúng từ đầu để đồng bộ vi/en.

#### QC-8: Tính nhất quán dữ liệu

- `q_correct` nằm trong 1-4 và đáp án tương ứng thực sự đúng
- `count_question` khớp số phần tử trong `content` — **PHẢI >= 1, KHÔNG BAO GIỜ = 0**
- `kind` trong JSON khớp với kind được yêu cầu gen
- 4 đáp án `q_answer` không được trùng nhau
- `distractor_traps` ghi đúng: đáp án đúng để rỗng `""`, đáp án sai có trap code hợp lệ

#### Cách thực hiện QC

`
SAU khi gen JSON, TRƯỚC khi lưu:
1. Duyệt từng câu hỏi trong JSON
2. Với mỗi câu, kiểm tra QC-1 → QC-8
3. Nếu phát hiện lỗi:
   a. Sửa TRỰC TIẾP trong JSON (không cần hỏi user)
   b. Ghi nhận lỗi đã sửa
4. Sau khi sửa hết → mới chuyển sang bước 5 (lưu file)
5. Báo cáo cho user: "QC passed ✓" hoặc "QC: đã sửa N lỗi (chi tiết: ...)"
`

> **Nếu agent bỏ qua bước QC hoặc lưu file mà chưa QC → dữ liệu sẽ bị lỗi. Bước này là BẮT BUỘC.**

### Quy tắc đường dẫn file

> **⚠️ QUAN TRỌNG: Folder `skills/` là READ-ONLY khi gen. KHÔNG ĐƯỢC tạo, sửa, hay xóa bất kỳ file nào trong `skills/` trong quá trình gen câu hỏi.**

| Loại file | Đường dẫn | Ghi chú |
|-----------|-----------|---------|
| CSV theo kind | `output/listen-origin/level_{1,2}/{kind}.csv` | Output chính |
| CSV tổng hợp | `output/listen-origin/all_questions.csv` | Merge từ tất cả kind |

### Lưu kết quả bằng script

`bash
# Lưu trực tiếp CSV theo kind + merge tổng
python skills/topik-listen-gen-origin/scripts/save_listen.py --data '<JSON_STRING>' -o output/listen-origin --merge

# Chỉ validate
python skills/topik-listen-gen-origin/scripts/save_listen.py --data '<JSON_STRING>' --validate-only

# Append thêm batch mới
python skills/topik-listen-gen-origin/scripts/save_listen.py --data '<JSON_STRING>' --append
`
