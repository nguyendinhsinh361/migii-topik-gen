# TOPIK Listen QC — Kiểm tra & sửa lỗi dữ liệu nghe

Skill QC hoàn toàn độc lập. Đọc CSV đã gen, kiểm tra **toàn bộ tiêu chí** theo các bảng tham chiếu bên dưới + từng file `kinds/{kind}.md` trong folder của skill này, tự động sửa lỗi, lặp đến khi đạt.

## Khi nào dùng skill này
- Khi user yêu cầu QC / kiểm tra / sửa lỗi dữ liệu nghe
- Sau khi gen xong câu hỏi nghe, cần QC trước khi gửi BTV

## Đầu vào
- File CSV: `output/listen-origin/all_questions.csv` (hoặc file CSV user chỉ định)

## Bước 0: Đọc file kind tương ứng trước khi QC (BẮT BUỘC)

Trước khi bắt đầu QC, agent **PHẢI**:
1. Đọc các **bảng tham chiếu** bên dưới (mục "Bảng tham chiếu") — lấy toàn bộ bảng topic, trap, question_feature, difficulty, answer_grammar, audio_format, speech_level, quy tắc chung
2. Đọc file kind tương ứng trong folder `kinds/` của skill này: `kinds/{kind}.md` — lấy quy tắc riêng của từng kind đang QC

Mọi tiêu chí ghi trong bảng tham chiếu + kind files đều là tiêu chí QC. Danh sách checks bên dưới là **tóm tắt** để dễ check tự động, nhưng KHÔNG thay thế việc đọc bảng tham chiếu và kind files.

## Workflow

1. Đọc các bảng tham chiếu bên dưới (ghi nhớ các bảng/quy tắc)
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

## Bảng tham chiếu

### Danh mục chủ đề (topic)
| Code | Nhãn | Từ khóa |
|------|------|---------|
| `time_appointment` | Time & Appointments | 시간, 약속, 오전, 오후, 언제, 몇 시 |
| `workplace` | Workplace & Work | 회사, 회의, 보고서, 출근, 퇴근, 팀장 |
| `food_restaurant` | Food & Dining | 식당, 밥, 먹다, 메뉴, 주문, 요리 |
| `shopping_price` | Shopping & Price | 사다, 얼마, 할인, 비싸다, 마트, 백화점 |
| `health_hospital` | Health & Hospital | 병원, 아프다, 약, 의사, 운동, 건강 |
| `weather_season` | Weather & Seasons | 비, 눈, 덥다, 춥다, 날씨, 봄, 여름 |
| `home_housing` | Home & Housing | 집, 방, 아파트, 이사, 거실, 부엌 |
| `transport` | Transportation | 버스, 지하철, 택시, 역, 공항, 기차 |
| `hobby_leisure` | Hobbies & Leisure | 영화, 노래, 사진, 음악, 책, 등산, 수영 |
| `travel` | Travel & Tourism | 여행, 호텔, 예약, 관광지, 해외 |
| `family_relations` | Family & Relations | 가족, 엄마, 아빠, 결혼, 아이, 부모님 |
| `school_education` | School & Education | 학교, 수업, 시험, 공부, 선생님, 대학 |
| `phone_communication` | Phone & Communication | 전화, 번호, 메시지, 연락, 문자 |
| `culture_event` | Culture & Events | 공연, 전시, 축제, 콘서트, 미술관 |
| `environment_society` | Environment & Society | 환경, 경제, 사회, 정책, 인구, 기술 |

### Chiến lược bẫy (distractor_trap)
| Code | Mô tả | Kind áp dụng |
|------|-------|-------------|
| `trap_shared_noun` | Đáp án sai chứa ≥2 danh từ giống audio | 110001-110004, 110006-110007, 210002-210007 |
| `trap_similar_word` | Từ phát âm/dạng tương tự | 110003, 110004 |
| `trap_partial_topic` | Chỉ đề cập một phần nội dung | 110004 |
| `trap_neg_없안` | Thêm 없다/안/아니다 đảo nghĩa | 110001-110002, 110006-110007, 210002-210007 |
| `trap_same_ending` | 4 đáp án cùng dạng ngữ pháp | 110001-110002, 110006-110007, 210002-210007 |
| `trap_subject_swap` | Gán hành động cho sai người | 110006, 110008, 210003-210007 |
| `trap_opinion_swap` | Ý kiến người nói kia | 110007, 210005 |
| `trap_detail_distort` | Bóp méo chi tiết | 110005, 110008 |
| `trap_partial_truth` | >30% từ đúng | 110006, 110008_1-2 |
| `trap_wrong_inference` | Suy luận không được nêu | 110008 |
| `trap_cause_effect_swap` | Đảo nhân quả | 110006, 110008_3 |
| `trap_scope_change` | Thay phạm vi 모든↔일부 | 110006-110007, 110008_3 |
| `trap_temporal_distort` | Đảo thời gian | 110006, 110008_2 |
| `trap_comparison_flip` | Đảo so sánh | 110006, 210001_2 |
| `trap_action_swap` | Thay đổi hành động | 110005, 210001_1 |
| `trap_context_swap` | Thay đổi bối cảnh | 110005, 210001_1 |
| `trap_number_shift` | Thay số liệu | 210001_2 |

### Đặc điểm câu hỏi (question_feature)
| Code | Kind áp dụng |
|------|-------------|
| `qf_direct_qa` | 110001 |
| `qf_next_utterance` | 110002, 210002 |
| `qf_guess_place` | 110003 |
| `qf_guess_topic` | 110004 |
| `qf_match_image` | 110005, 210001_1 |
| `qf_match_graph` | 210001_2 |
| `qf_match_content` | 110006, 210004 |
| `qf_predict_action` | 210003 |
| `qf_main_opinion` | 110007, 210005 |
| `qf_multi_comprehension` | 110008, 210006 |
| `qf_content_match` | 210006, 210007 (Q1) |
| `qf_central_thought` | 210007 (Q1) |
| `qf_attitude` | 210007 (Q2) |

### Ngữ pháp đáp án (answer_grammar)
| Code | Kind áp dụng |
|------|-------------|
| `ans_informal_polite` | 110001, 110002 |
| `ans_noun_phrase` | 110003, 110004, 110008_2 (Q1) |
| `ans_image` | 110005, 210001_1, 210001_2 |
| `ans_formal_polite` | 110006-110007, 210002, 110008 (Q2) |
| `ans_plain_form` | 210003-210007 |
| `ans_purpose_phrase` | 110008_1 (Q1) |
| `ans_reason_phrase` | 110008_3 (Q1) |

### Thang độ khó (Difficulty Scale)
| Mức | Kind |
|:---:|------|
| 2 | 110001 |
| 3 | 110002 |
| 4 | 110003, 110004 |
| 5 | 110005 |
| 6 | 110006, 210002, 210001_1 |
| 7 | 210003, 210004, 210001_2 |
| 8 | 110007, 210005, 110008, 210006 |
| 9 | 210007 |

### Cấu trúc audio (audio_format)

Xem chi tiết trong từng file `kinds/{kind}.md`.

### Cấp độ giao tiếp (speech_level)
| Level | Audio | Đáp án |
|:-----:|-------|--------|
| 1 | informal_polite (~어요/세요) | informal_polite |
| 2 | pha trộn modifier + connective + formal | plain_form (~ㄴ다/한다) |

---

## Danh sách QC checks

### Nhóm 1: Metadata & Consistency

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| MC-1 | `tag` = "listen" | Exact match | ✅ |
| MC-2 | `level` hợp lệ | 110xxx → 1, 210xxx → 2 | ✅ |
| MC-3 | `kind` hợp lệ | Tồn tại file `kinds/{kind}.md` | ❌ báo cáo |
| MC-4 | `count_question` khớp | Đếm số q_text_N có dữ liệu | ✅ |
| MC-5 | `q_correct` trong 1-4 | Với mỗi q_correct_N | ✅ clamp |
| MC-6 | **TOPIK I q_correct = 1** | Nếu kind 110xxx → q_correct phải = 1. Nếu sai → đổi q_correct = 1 và swap đáp án đúng lên vị trí 1 | ✅ |
| MC-7 | 4 đáp án không trùng | Parse q_answer_N, check unique | ❌ cần LLM |
| MC-8 | `topic` hợp lệ | Thuộc danh sách topic trong bảng tham chiếu | ✅ |
| MC-9 | `question_feature` hợp lệ | Thuộc danh sách qf_* trong bảng tham chiếu, phù hợp với kind | ✅ |
| MC-10 | `difficulty` hợp lệ | Theo bảng Thang độ khó trong bảng tham chiếu | ✅ |
| MC-11 | `distractor_trap` hợp lệ | Mã trap phải thuộc danh sách trap_* trong bảng tham chiếu. Trap phải phù hợp kind (xem bảng Kind áp dụng) | ❌ cần LLM |

### Nhóm 2: Audio (g_text_audio)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| AU-1 | Audio không rỗng | g_text_audio != "" | ❌ cần LLM |
| AU-2 | **Format speaker theo kind** | Đọc kind file, check format. Ví dụ: 210006_(7) chỉ "여자:", 210004_(4) "남자:...\n여자:..." 2 lượt | ❌ cần LLM |
| AU-3 | **Số lượt thoại** theo kind | Kind file quy định bao nhiêu lượt. Ví dụ: 110001 = 1 câu, 110006 = 3-4 lượt | ❌ cần LLM |
| AU-4 | **Độ dài audio** theo kind | 210001_2: ~180, 110008_2: ~250, 110008_3: ~350 ký tự (±20%) | ❌ cần LLM |
| AU-5 | **Cấp độ ngữ pháp** | Level 1: informal_polite (~어요/세요). Level 2: pha trộn. Xem bảng speech_level | ❌ cần LLM |
| AU-6 | **Blank line** trong audio | Nếu kind 110001/110002 → audio format "남자: ___\n여자: ___" phải có blank line `______` đúng vị trí. Xem kind file | ❌ cần LLM |
| AU-7 | **Audio không phải câu hỏi** (110002) | g_text_audio KHÔNG kết thúc bằng ? cho kind 110002 | ❌ cần LLM |
| AU-8 | **Nội dung audio match kind** | Chủ đề audio phải phù hợp kind (210004 = phỏng vấn công việc, 210006_(3) = phỏng vấn TV...). Đọc kind file | ❌ cần LLM |

### Nhóm 3: Bản dịch audio

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| TR-1 | **"Người nam:" / "Người nữ:"** | g_text_audio_vi phải dùng "Người nam:" (KHÔNG "Nam:"). Regex: `(?<!Người )(?<!\w)Nam:` | ✅ |
| TR-2 | **"Man:" / "Woman:"** | g_text_audio_en phải dùng "Man:" / "Woman:" (KHÔNG "Male:" / "Female:") | ✅ |
| TR-3 | **Blank lines dịch đúng** | Nếu g_text_audio có `______` → vi và en cũng phải có `______` | ✅ |
| TR-4 | **Số dòng khớp** | Số dòng g_text_audio_vi = số dòng g_text_audio | ✅ |
| TR-5 | Bản dịch không rỗng | g_text_audio_vi và g_text_audio_en không rỗng khi g_text_audio có nội dung | ❌ cần LLM |

### Nhóm 4: Đáp án (q_answer)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| AN-1 | **answer_grammar đúng kind** | Xem bảng answer_grammar trong bảng tham chiếu. Ví dụ: 110001 → ans_informal_polite (~어요/아요), 210003 → ans_plain_form (~ㄴ다/한다) | ❌ cần LLM |
| AN-2 | **Đáp án sai đủ sai** (110001, 110002) | Đáp án sai phải rõ ràng sai, không mập mờ gần đúng | ❌ cần LLM |
| AN-3 | **Trap distribution** theo kind | Đọc kind file → bảng chiến lược bẫy → check distractor_trap khớp | ❌ cần LLM |
| AN-4 | **q_correct phân bố đều** | Trong cùng batch (cùng kind), q_correct phải phân bố đều 1-4 | ❌ check & báo cáo |

### Nhóm 5: Câu hỏi phụ (q_text)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| QT-1 | **q_text đúng kind** | Xem kind file quy định q_text cố định hay không. Ví dụ: 210007_(6) Q2 = "남자의 태도로...", 210007_(7) Q2 = "남자가 말하는 방식으로..." | ❌ cần LLM |
| QT-2 | **q_text rỗng khi cần** | Nhiều kind không có q_text (110001-110005). Check kind file | ✅ |

### Nhóm 6: Giải thích (explain)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| EX-1 | **Không chứa mã trap** | Regex `trap_[a-z_]+` trong explain_vi_*, explain_en_* | ✅ xóa |
| EX-2 | **EN chi tiết bằng VI** | len(explain_en) >= 50% len(explain_vi) | ❌ cần LLM |
| EX-3 | **Không prefix "Câu hỏi:"** | Regex `^(Câu hỏi|Question)\s*:` hoặc `\[(Câu hỏi|Question)\]` | ✅ xóa |
| EX-4 | **Không pattern "từ trùng audio"** | Pattern: "dùng từ ... từ audio nhưng" / "uses ... from the audio but" | ❌ cần LLM |
| EX-5 | **Dịch câu hỏi phụ** (110008, 210006, 210007) | explain phải có bản dịch q_text. KHÔNG để nguyên tiếng Hàn | ❌ cần LLM |
| EX-6 | **210006: KHÔNG dòng "[Dịch câu hỏi phụ]"** | Regex `\[Dịch câu hỏi phụ|\[Translate Q` | ✅ xóa |
| EX-7 | **"người nam"/"người nữ" trong explain_vi** | Không dùng "nam", "nữ", "anh ấy", "cô ấy" đơn lẻ | ✅ replace |
| EX-8 | **VI và EN cùng cấu trúc** | Cả 2 phải có: dịch đáp án → separator ---- → giải thích. Nếu VI giải thích từng đáp án → EN cũng phải | ❌ cần LLM |
| EX-9 | **210001_1/210001_2: explain không dịch audio, không mô tả ảnh** | Chỉ cần phần giải thích đáp án | ❌ cần LLM |
| EX-10 | **110005: explain ngắn gọn** | Chỉ 1 câu giải thích đáp án đúng, không diễn giải từng đáp án | ❌ cần LLM |
| EX-11 | **110003: explain chính xác ngôn ngữ học** | Không claim phát âm tương tự khi thực tế không giống, không claim từ vựng giống khi chỉ giống ở bản dịch tiếng Việt | ❌ cần LLM |
| EX-12 | **Không icon/emoji** | Regex `[✅❌✓✗☑☐⬜⬛🔴🟢]` trong explain | ✅ xóa |
| EX-13 | **Trích dẫn Hàn giữ nguyên** | Explain phải giữ nguyên từ/cụm tiếng Hàn trong ngoặc, KHÔNG dịch | ❌ cần LLM |

### Nhóm 7: Hình ảnh (kind có ảnh)

| ID | Kiểm tra | Cách check | Auto-fix? |
|----|----------|-----------|:---------:|
| IM-1 | **Kind có ảnh phải có q_image_desc** | 110005, 210001_1, 210001_2 | ❌ cần LLM |
| IM-2 | **q_image_desc đủ chi tiết** | Đọc kind file để biết format mô tả ảnh | ❌ cần LLM |

---

## Quy tắc sửa lỗi

### Lỗi sửa tự động (regex/string):
MC-1, MC-2, MC-4, MC-5, MC-6, MC-8, MC-9, MC-10, TR-1, TR-2, TR-3, TR-4, QT-2, EX-1, EX-3, EX-6, EX-7, EX-12

### Lỗi cần LLM viết lại:
Tất cả lỗi còn lại. Khi viết lại:
- Đọc `kinds/{kind}.md` để lấy quy tắc cụ thể
- Đọc các bảng tham chiếu ở trên để tra cứu
- Giữ nguyên các trường khác, chỉ sửa trường lỗi

## Output
- CSV đã sửa (ghi đè file gốc)
- Báo cáo tổng hợp: số lỗi theo nhóm, số đã sửa, số cần xem lại

## Lưu ý
- Skill này TÁCH BIỆT hoàn toàn với skill gen
- Folder `kinds/` chứa bản sao các kind files — dùng để tra cứu quy tắc khi QC
- Chỉ chỉnh CSV trong `output/`, KHÔNG chỉnh bất kỳ file nào khác
- Khi sửa LLM, phải tuân theo **tất cả quy tắc** trong kind file, không chỉ quy tắc QC
