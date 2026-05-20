# EPS-TOPIK Listening Question Generator (Level 3)

Skill tao cau hoi phan Nghe (듣기) cho ky thi EPS-TOPIK (Level 3 — danh cho nguoi lao dong nuoc ngoai tai Han Quoc) theo dung format JSON cua he thong Migii.

## Khi nao dung skill nay

- Khi user yeu cau tao/gen cau hoi nghe EPS-TOPIK
- Khi user chi dinh kind cu the (vi du: "gen 310001", "tao cau hoi dang 3410005")
- Khi user yeu cau tao de thi nghe EPS

## Cau truc thu muc

```
skills/topik-listen-gen-eps/
├── SKILL.md              ← File nay (overview + quy tac chung)
├── scripts/
│   └── save_listen.py    ← Script luu CSV/JSON theo kind
├── kinds/                ← Quy tac chi tiet tung dang
│   ├── 310001.md         Nhan dien tu/cau (EPS, gom 3410001)
│   ├── 310002.md         Nhin hinh chon dap an (EPS, gom 3410003) [anh]
│   ├── 310003.md         Chon hinh lien quan (EPS, gom 3410006) [anh]
│   ├── 310004.md         Hoi-dap EPS (gom 3410004)
│   ├── 310005.md         Trich xuat chi tiet (EPS, gom 3410007)
│   ├── 310006.md         2 cau hoi EPS
│   ├── 3410002.md        Nhan dien gio (EPS) [anh]
│   └── 3410005.md        Chon cau noi tiep EPS (pragmatic_response)
└── samples.json          ← Mau cau hoi tham khao
```

Khi gen kind cu the, doc file `kinds/{kind}.md` tuong ung + file SKILL.md nay.

---

## Output Format (JSON)

Moi cau hoi PHAI tuan theo cau truc JSON sau:

```json
{
  "title": "<tieu de dang cau hoi bang tieng Han>",
  "general": {
    "g_text": "",
    "g_text_translate": { "vi": "", "en": "" },
    "g_text_audio": "<noi dung audio / doan hoi thoai bang tieng Han>",
    "g_text_audio_translate": {
      "vi": "<ban dich tieng Viet>",
      "en": "<ban dich tieng Anh>"
    },
    "g_audio": "",
    "g_image": ""
  },
  "content": [
    {
      "q_text": "<cau hoi phu neu co, neu khong thi de rong>",
      "q_image": "",
      "q_point": <diem hoac null>,
      "q_answer": ["<dap an 1>", "<dap an 2>", "<dap an 3>", "<dap an 4>"],
      "q_correct": <so thu tu dap an dung 1-4>,
      "explain": {
        "vi": "<giai thich tieng Viet>",
        "en": "<giai thich tieng Anh>"
      },
      "question_feature": "<ma dac diem tu bang question_feature>",
      "difficulty": <muc do kho 1-4>,
      "distractor_traps": {
        "1": "<trap code cho dap an 1 — rong neu la dap an dung>",
        "2": "<trap code cho dap an 2>",
        "3": "<trap code cho dap an 3>",
        "4": "<trap code cho dap an 4>"
      }
    }
  ],
  "level": 3,
  "kind": "<ma kind>",
  "count_question": <so cau hoi con trong content>,
  "tag": "listen",
  "topic": "<ma chu de tu bang topic>"
}
```

### Format bo sung cho kind co anh

Them truong `q_image_description` mo ta noi dung anh bang text:

```json
{
  "q_image_description": {
    "1": "<mo ta noi dung hinh 1>",
    "2": "<mo ta noi dung hinh 2>",
    "3": "<mo ta noi dung hinh 3>",
    "4": "<mo ta noi dung hinh 4>"
  }
}
```

Voi kind 310002/3410003 (chi 1 buc tranh, dap an trong audio):
```json
{
  "q_image_description": {
    "image": "<mo ta buc tranh duy nhat>"
  }
}
```

---

## Danh muc chu de (topic)

### Chu de chung (ap dung cho EPS)

| Code | Nhan tieng Anh | Tieng Han | Tu khoa nhan dien |
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

### Chu de rieng EPS-TOPIK (Level 3)

Phat hien tu du lieu 2.242 cau EPS — cac chu de dac thu cho nguoi lao dong nuoc ngoai:

| Code | Nhan tieng Anh | Tu khoa nhan dien | Ty le (L3) |
|------|---------------|-------------------|:-----------:|
| `factory_work` | Factory & Production | 공장, 기계, 작업, 생산, 제품, 부품, 조립, 포장 | 5% |
| `dormitory_life` | Dormitory Life | 기숙사, 룸메이트, 세탁기, 청소, 방, 규칙, 소음 | 6% |
| `safety_workplace` | Workplace Safety | 안전, 사고, 위험, 보호, 장갑, 안전모, 소화기 | 2% |
| `wages_contract` | Wages & Contract | 월급, 급여, 계약, 근무, 야근, 휴일, 수당 | 3% |

---

## Chien luoc bay dap an sai (distractor_trap)

### Nhom 1: Bay tu vung (Vocabulary Traps)

| Code | Nhan tieng Anh | Mo ta | Bang chung tu du lieu |
|------|---------------|-------|----------------------|
| `trap_shared_noun` | Shared-Noun Trap | Dap an sai chua >=2 danh tu giong audio | 10.058 luot phat hien |
| `trap_sound_similarity` | Sound Similarity | 4 dap an phat am gan giong nhau | 100% o 310001/3410001/3410002. Tu don 2 am tiet chiem 85% |
| `trap_opposite_meaning` | Opposite Meaning | Dap an sai dung tu trai nghia voi dap an dung | 15% o 210006/210007, 6% o 110006 |

### Nhom 2: Bay phu dinh (Negation Traps)

| Code | Nhan tieng Anh | Mo ta | Bang chung tu du lieu |
|------|---------------|-------|----------------------|
| `trap_neg_없안` | Negation 없/안/아니 | Dap an sai them 없다/안/아니다 de dao nghia | 456 luot 없, 333 luot 안, 209 luot 아니 |
| `trap_neg_않못` | Negation 않/못 | Dap an sai them 않다/못하다 de phu dinh hanh dong | 333 luot 않, 162 luot 못 |

### Nhom 3: Bay cau truc (Structural Traps)

| Code | Nhan tieng Anh | Mo ta | Bang chung tu du lieu |
|------|---------------|-------|----------------------|
| `trap_same_ending` | Same-Ending Pattern | Ca 4 dap an ket thuc cung dang ngu phap | Pho bien nhat: ~ㅂ니다(907), ~있다(235), ~어요(185) |
| `trap_same_start` | Same-Start Pattern | Ca 4 dap an bat dau bang cung mot tu | 66 cau o 310004, 58 cau o 210007 |

### Nhom 4: Bay noi dung (Content Traps)

| Code | Nhan tieng Anh | Mo ta | Bang chung tu du lieu |
|------|---------------|-------|----------------------|
| `trap_subject_swap` | Subject Swap | Gan hanh dong/y kien cho sai nguoi (가↔나) | 1.026 luot swap_general |
| `trap_number_shift` | Number/Time Shift | Thay doi con so/thoi gian tu audio | 398 cau phat hien. Rat cao o 3410004-3410007(100%), 310006(52%) |
| `trap_partial_truth` | Partial Truth | Dap an sai chua >30% tu dung tu audio nhung bi sua 1 chi tiet | 34% o 210004, 50% dap an sai 210006 |

### Quy tac gan nhan bay

- Moi cau hoi co the co NHIEU nhan bay cung luc
- Gan nhan dua tren DAP AN SAI, khong phai dap an dung
- Chi gan khi co bang chung ro rang, khong suy doan

---

## Dac diem cau hoi (question_feature)

### Nhom cau hoi co q_text

| Code | Nhan tieng Anh | Mo ta |
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

### Nhom cau hoi KHONG co q_text

| Code | Kind ap dung | Mo ta |
|------|-------------|-------|
| `qf_direct_qa` | 310004 | Nghe cau hoi -> chon cau tra loi truc tiep |
| `qf_next_utterance` | 3410005 | Nghe hoi thoai -> chon cau noi tiep |
| `qf_match_image` | 310003 | Nghe -> chon hinh khop |
| `qf_match_content` | 310005 | Nghe -> chon phat bieu khop noi dung |
| `qf_identify_sound` | 310001 | Nghe -> nhan dien tu/cau |
| `qf_identify_time` | 3410002 | Nghe gio -> chon dong ho |
| `qf_image_qa` | 310002 | Nhin hinh + nghe 4 cau mo ta -> chon dung |

---

## Cau truc ngu phap trong audio (grammar_semantic)

### Phan bo Level 3 (2.242 cau, chi liet ke >=5%)

gram_honorific_시(21%), gram_request_세요(19%), gram_honorific_습니다(18%), gram_cause_니까(8%), gram_cond_면(7%), gram_contrast_는데(7%), gram_prog_고있(6%), gram_intent_겠(6%), gram_cause_어서(5%)

### Bang nhan ngu phap theo y nghia (Level 3)

| Code | Cau truc | Y nghia | L3 |
|------|----------|---------|:--:|
| `gram_cause_어서` | ~어서/아서 | Nguyen nhan (nhe) | 5% |
| `gram_cause_니까` | ~니까 | Nguyen nhan (nhan manh) | 8% |
| `gram_cond_면` | ~(으)면 | Dieu kien | 7% |
| `gram_contrast_지만` | ~지만 | Doi lap truc tiep | 3% |
| `gram_contrast_는데` | ~는데/은데 | Boi canh/doi lap mem | 7% |
| `gram_intent_려고` | ~(으)려고 | Y dinh | 4% |
| `gram_intent_겠` | ~겠어요/겠습니다 | Du dinh/suy doan | 6% |
| `gram_request_세요` | ~(으)세요 | Yeu cau lich su | 19% |
| `gram_request_주세요` | ~주세요 | Nho va cu the | 4% |
| `gram_prog_고있` | ~고 있다 | Dang dien ra | 6% |
| `gram_honorific_시` | ~시/셨/세요 | Kinh ngu (시) | 21% |
| `gram_honorific_습니다` | ~습니다/ㅂ니다 | Kinh ngu trang trong | 18% |

### Ngu phap trong dap an (answer_grammar)

| Code | Mo ta | Kind ap dung |
|------|-------|-------------|
| `ans_formal` | Dap an dung ~ㅂ니다 | 310004, 310005, 310006, va cac EPS kinds |
| `ans_short_word` | Dap an la tu don / cum ngan | 310001, 3410002 |
| `ans_sentence` | Dap an la cau day du | 3410005, 310003 |

---

## Cau truc audio (audio_format)

| Code | Mo ta | Kind chinh |
|------|-------|-----------|
| `audio_dialog_가나` | Hoi thoai 가/나 (EPS) | 310003-310006 |
| `audio_single_word` | Tu don/cum ngan (<15 ky tu) | 310001, 3410002 |
| `audio_single_sentence` | Cau don (15-50 ky tu) | 310004, 3410005 |
| `audio_numbered` | 4 cau mo ta danh so (1. 2. 3. 4.) | 310002 |

---

## Thang do kho (Difficulty Scale) — EPS kinds only

| Muc | Kind | Kieu suy luan | Nhan |
|:---:|------|--------------|------|
| 1 | 310001, 3410002 | `sound_recognition` / `time_recognition` | Nhan dien tu/gio |
| 2 | 310004, 310002 | `direct_match` / `image_qa` | Hoi-dap don gian |
| 3 | 3410005 | `pragmatic_response` | Chon cau noi tiep |
| 4 | 310003 | `scene_matching` | Chon hinh lien quan |
| 5 | 310005 | `detail_extraction` | Trich xuat chi tiet |
| 8 | 310006 | `multi_comprehension` | 2 cau hoi / doan dai |

### Mo ta kieu suy luan (reasoning_type)

| Code | Mo ta |
|------|-------|
| `sound_recognition` | Nhan dien chinh xac tu/cau duoc nghe |
| `time_recognition` | Nghe gio, chon dong ho phu hop |
| `direct_match` | Ghep cau hoi voi cau tra loi truc tiep |
| `image_qa` | Nhin hinh, nghe cau hoi + dap an, chon dung |
| `pragmatic_response` | Chon phan hoi phu hop ngu canh giao tiep |
| `scene_matching` | Nghe audio, chon buc tranh minh hoa khop |
| `detail_extraction` | Trich xuat chi tiet cu the tu hoi thoai |
| `multi_comprehension` | Tra loi 2 cau hoi tu 1 doan |

---

## Cap do giao tiep trong audio (speech_level)

| Level | Audio chinh | Dap an |
|:-----:|------------|--------|
| 3 | `informal_polite` 37%, `modifier` 31%, `connective` 16% | `formal_polite` (~ㅂ니다) cho EPS |

**Quy tac**: Audio EPS dung `informal_polite` la chinh. **Dap an** EPS thuong dung `formal_polite` (~ㅂ니다) — xem answer_grammar `ans_formal`.

---

## Quy tac chung khi gen cau hoi

### 1. Chat luong noi dung tieng Han
- Dung ngu phap dung Level 3 (xem bang speech_level + grammar_semantic)
- Hoi thoai tu nhien, da dang chu de doi song + lao dong
- KHONG lap lai tu vung/ngu canh giua cac cau trong cung batch
- Pha tron chu de chung + chu de EPS dac thu

### 2. Xay dung dap an sai (distractor)
- Tuan theo ty le bay cua tung kind (xem file kind tuong ung)
- Phai hop ly nhung SAI ve noi dung
- Tai su dung tu vung audio khi kind yeu cau `shared_word`

### 3. Giai thich (explain)
- **vi**: Dich ca 4 dap an -> dau `--------------------` -> giai thich dap an dung, ghi chu trap type cho tung dap an sai
- **en**: Tuong tu bang tieng Anh
- Highlight tu vung/ngu phap quan trong

### 4. So luong
- Mac dinh: 5 cau moi kind neu user khong chi dinh
- Toi da: 20 cau moi lan

### 5. Kiem tra sau khi gen (Validation Checklist)
- [ ] `q_correct` nam trong 1-4
- [ ] 4 dap an khong trung nhau
- [ ] Audio la tieng Han tu nhien
- [ ] Ngu phap dung Level 3
- [ ] Bay dung phan bo cua kind
- [ ] Ban dich (vi/en) chinh xac
- [ ] `explain` chua dich 4 dap an + ly do dap an dung + trap type cho dap an sai
- [ ] `count_question` khop so phan tu trong `content`
- [ ] `level` luon = 3

## Workflow

1. User chi dinh kind -> doc file `kinds/{kind}.md`
2. Hoi so luong (mac dinh 5)
3. Gen cau hoi theo JSON format + quy tac kind + chien luoc bay
4. Luu JSON tam -> chay `scripts/save_listen.py` de tach CSV theo kind
5. Validate theo checklist

### Luu ket qua bang script

```bash
# Luu CSV theo kind + JSON + merge tong
python skills/topik-listen-gen-eps/scripts/save_listen.py gen_temp.json -o output/listen-eps --json --merge

# Chi validate
python skills/topik-listen-gen-eps/scripts/save_listen.py gen_temp.json --validate-only

# Append them batch moi
python skills/topik-listen-gen-eps/scripts/save_listen.py new_batch.json --append
```

Output: `output/listen-eps/level_3/{kind}.csv`
