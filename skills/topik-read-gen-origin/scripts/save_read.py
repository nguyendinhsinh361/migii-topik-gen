#!/usr/bin/env python3
"""
save_read.py — Lưu câu hỏi đọc TOPIK I & II đã gen ra CSV theo từng kind.

Nằm trong: skills/topik-read-gen-origin/scripts/

Mỗi câu hỏi = 1 dòng CSV. Content items được đánh số _1, _2, ... theo count_question.

Cách dùng:
  python skills/topik-read-gen-origin/scripts/save_read.py input.json
  python skills/topik-read-gen-origin/scripts/save_read.py input.json -o output/read-origin
  python skills/topik-read-gen-origin/scripts/save_read.py input.json --append
  python skills/topik-read-gen-origin/scripts/save_read.py input.json --validate-only

Cấu trúc output:
  output/read-origin/
  ├── level_1/
  │   ├── 120001.csv
  │   └── ...
  └── level_2/
      ├── 220001_a.csv
      └── ...
"""

import csv
import json
import os
import re
import sys
from datetime import datetime
from collections import defaultdict

# ─── Cấu hình ──────────────────────────────────────────────────────────────────

# scripts/ → topik-read-gen-origin/ → skills/ → project root
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SKILL_DIR))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "read-origin")

# Cột cố định (question-level)
BASE_COLUMNS = [
    "id", "kind", "level", "tag", "title", "count_question",
    "view_g_image", "g_image", "view_g_audio", "g_audio",
    "g_text", "g_text_vi", "g_text_en",
    "g_text_audio", "g_text_audio_vi", "g_text_audio_en",
    "topic",
]

# Cột lặp theo content (sẽ thêm hậu tố _1, _2, ...)
CONTENT_COLUMNS = [
    "q_text", "q_point", "q_answer", "q_correct",
    "explain_vi", "explain_en",
    "view_q_image", "q_image", "q_image_desc",
    "question_feature", "difficulty", "distractor_trap",
]

# ─── Quy tắc biên tập theo kind (dấu chấm / độ dài) ────────────────────────────
# Nguồn: "MIGII TOPIK - Read Rule - Gen Question AI New.xlsx" (biên tập viên bổ sung).
#
# _ANSWER_PERIOD: dấu "." cuối mỗi đáp án — THEO TỪNG CÂU HỎI con.
#   value = tuple (period_q1, period_q2, ...) cho từng câu hỏi con (1-based).
#     True  = đáp án PHẢI kết thúc bằng "." (câu hoàn chỉnh)
#     False = KHÔNG có "." (cụm danh từ / từ / cụm ngữ pháp / cụm ngắn)
#   ⚠️ Phần ĐỌC: PHẦN LỚN kind KHÔNG có dấu chấm. Kind nhiều câu hỏi (120005_*, 120007_*,
#      220005_*, 220008_*) thường khác nhau giữa các câu hỏi con.
_ANSWER_PERIOD = {
    "120001": (False,),
    "120002_1": (False,),
    "120002_2": (False,),
    "120002_3": (False,),
    "120002_4": (False,),
    "120003_1": (True,),
    "120003_2": (True,),
    "120004_1": (True,),
    "120004_2": (True,),
    "120005_(1)": (False, True),
    "120005_(2)": (False, False),
    "120006": (False,),
    "120007_1": (False, True),
    "120007_2": (False, True),
    "120007_3": (False, True),
    "220001_a": (False,),
    "220001_b": (False,),
    "220001_c": (False,),
    "220002_a": (False,),
    "220002_b_1": (True,),
    "220002_b_2": (True,),
    "220002_b_3": (True,),
    "220002_c": (True,),
    "220003_a_1": (False,),
    "220003_a_2": (False,),
    "220003_b": (True,),
    "220004": (False,),
    "220005_1_(1)": (False, True),
    "220005_1_(2)": (False, True),
    "220005_2": (False, True),
    "220006": (True,),
    "220007": (False,),
    "220008_1_(1)": (False, True),
    "220008_1_(2)": (False, True),
    "220008_1_(3)": (True, True),
    "220008_2": (False, False, True),
}

# _GTEXT_LENGTH: độ dài đoạn đọc G_text (ký tự). Chỉ các kind có đoạn văn riêng ở g_text.
_GTEXT_LENGTH = {
    "120005_(1)": [(130, 180)],
    "120005_(2)": [(130, 180)],
    "120007_1": [(140, 190)],
    "120007_2": [(150, 200)],
    "220005_1_(1)": [(180, 240)],
    "220005_1_(2)": [(200, 240)],
    "220005_2": [(420, 500)],
    "220008_1_(1)": [(550, 600)],
    "220008_1_(2)": [(380, 400)],
    "220008_1_(3)": [(400, 440)],
    "220008_2": [(460, 510)],
}

# _IMGTEXT_LENGTH: độ dài "Text trong ảnh" (nội dung chữ nằm trong q_image). Chỉ để tham chiếu/doc,
#   KHÔNG validate tự động vì text nằm trong ảnh chứ không ở g_text.
_IMGTEXT_LENGTH = {
    "120007_3": [(250, 300)],
    "220002_b_1": [(180, 220)],
    "220003_a_1": [(20, 30)],
    "220003_a_2": [(30, 60)],
}

# _QTEXT_LENGTH: độ dài text_question_1 (đoạn đọc/câu đọc gắn theo từng câu hỏi). Ký tự.
_QTEXT_LENGTH = {
    "120001": [(20, 35)],
    "120002_1": [(20, 35)],
    "120002_2": [(20, 35)],
    "120002_3": [(20, 35)],
    "120002_4": [(20, 35)],
    "120004_1": [(50, 80)],
    "120004_2": [(50, 80)],
    "120006": [(120, 150)],
    "220001_a": [(25, 30)],
    "220001_b": [(150, 200)],
    "220001_c": [(170, 250)],
    "220002_a": [(30, 40)],
    "220002_b_3": [(180, 210)],
    "220002_c": [(190, 250)],
    "220003_b": [(200, 240)],
    "220004": [(140, 170)],
    "220006": [(20, 40)],
    "220007": [(250, 320)],
}


def _period_for(kind, qidx):
    """True/False: đáp án của câu hỏi con thứ qidx (1-based) có dấu '.' cuối không.
    Mặc định False nếu kind chưa khai báo (phần Đọc đa số KHÔNG dấu chấm)."""
    rule = _ANSWER_PERIOD.get(str(kind).strip())
    if not rule:
        return False
    return rule[qidx - 1] if 0 <= qidx - 1 < len(rule) else rule[-1]


def _count_chars(text):
    """Đếm độ dài theo cách của BIÊN TẬP VIÊN = đếm gần như Google Dịch:
    TÍNH CẢ dấu cách, dấu câu, ký hiệu ㉠/㉡, xuống dòng — NHƯNG **KHÔNG tính**
    ký tự gạch dưới `_` của dòng trống (___)."""
    if not text:
        return 0
    return len(text.replace('_', '').strip())


def check_text_lengths(question):
    """Trả về list cảnh báo nếu g_text / q_text lệch khoảng quy định (không chặn lưu)."""
    warnings = []
    kind = str(question.get("kind", "")).strip()
    general = question.get("general", {})

    spec_g = _GTEXT_LENGTH.get(kind)
    if spec_g:
        n = _count_chars(general.get("g_text", ""))
        if n and not any(lo <= n <= hi for lo, hi in spec_g):
            rng = " hoặc ".join(f"{lo}~{hi}" for lo, hi in spec_g)
            warnings.append(f"g_text dài {n} ký tự, ngoài khoảng quy định {rng}")

    spec_q = _QTEXT_LENGTH.get(kind)
    if spec_q:
        content = question.get("content", [])
        qt = content[0].get("q_text", "") if content else ""
        n = _count_chars(qt)
        if n and not any(lo <= n <= hi for lo, hi in spec_q):
            rng = " hoặc ".join(f"{lo}~{hi}" for lo, hi in spec_q)
            warnings.append(f"text_question_1 dài {n} ký tự, ngoài khoảng quy định {rng}")

    return warnings


# Backward-compat: tập kind có dấu chấm ở câu hỏi đầu (Q1).
_KINDS_WITH_PERIOD = {k for k, v in _ANSWER_PERIOD.items() if v and v[0]}


def _fix_explain_periods(text):
    """Thêm dấu . cuối mỗi dòng dịch đáp án trong explain (trước separator ----)."""
    if not text:
        return text
    lines = text.split("\n")
    separator_found = False
    result = []
    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith("----"):
            separator_found = True
            result.append(line)
            continue
        if not separator_found and stripped:
            if re.match(r'^[①②③④\d]+[\.\)]?\s', stripped):
                if not stripped.endswith((".", "?", "!", "…", "~")):
                    line = stripped + "."
        result.append(line)
    return "\n".join(result)


def _strip_explain_periods(text):
    """Bỏ dấu . cuối mỗi dòng dịch đáp án trong explain (trước separator ----)."""
    if not text:
        return text
    lines = text.split("\n")
    separator_found = False
    result = []
    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith("----"):
            separator_found = True
            result.append(line)
            continue
        if not separator_found and stripped:
            if re.match(r'^[①②③④\d]+[\.\)]?\s', stripped):
                if stripped.endswith(".") and not stripped.endswith(("?", "!", "…", "~")):
                    line = stripped.rstrip(".")
        result.append(line)
    return "\n".join(result)


def get_csv_columns(max_cq):
    """Sinh danh sách cột CSV dựa trên max count_question."""
    cols = list(BASE_COLUMNS)
    for n in range(1, max_cq + 1):
        for col in CONTENT_COLUMNS:
            cols.append(f"{col}_{n}")
    cols.append("created_at")
    return cols


# ─── Hàm chính ─────────────────────────────────────────────────────────────────

def load_json(filepath):
    """Đọc file JSON, hỗ trợ cả format {questions: [...]} và [...] thuần."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "questions" in data:
            return data["questions"]
        questions = []
        for kind_key, items in data.items():
            if isinstance(items, list):
                questions.extend(items)
        return questions

    raise ValueError(f"Không nhận diện được format JSON: {type(data)}")


def flatten_question(question, timestamp=None, seq=0):
    """
    Chuyển 1 question JSON thành 1 row dict duy nhất.
    Content items được đánh số _1, _2, ... nằm ngang trong cùng 1 dòng.
    """
    # Dùng module-level _fix_explain_periods

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    general = question.get("general", {})
    content_list = question.get("content", [])
    kind = str(question.get("kind", ""))
    g_text_translate = general.get("g_text_translate", {})

    row = {
        "id": f"{kind}_{timestamp}_q{seq}",
        "kind": kind,
        "level": question.get("level", ""),
        "tag": question.get("tag", "read"),
        "title": question.get("title", ""),
        "count_question": question.get("count_question", 1),
        "view_g_image": "",
        "g_image": general.get("g_image", ""),
        "view_g_audio": "",
        "g_audio": general.get("g_audio", ""),
        "g_text": general.get("g_text", ""),
        "g_text_vi": g_text_translate.get("vi", ""),
        "g_text_en": g_text_translate.get("en", ""),
        "g_text_audio": general.get("g_text_audio", ""),
        "g_text_audio_vi": "",
        "g_text_audio_en": "",
        "topic": question.get("topic", ""),
        "created_at": timestamp,
    }

    # q_image_desc nằm ở top-level hoặc content-level
    top_img_desc = question.get("q_image_desc", question.get("q_image_description", {}))

    for idx, content in enumerate(content_list):
        n = idx + 1
        answers = content.get("q_answer", [])
        while len(answers) < 4:
            answers.append("")
        explain = content.get("explain", {})
        # Ưu tiên top-level, fallback content-level
        img_desc = top_img_desc if top_img_desc else content.get("q_image_desc", content.get("q_image_description", {}))
        d_traps = content.get("distractor_traps", {})

        # Image desc — hỗ trợ string (format mới) và dict (format cũ)
        # Nếu string chứa JSON → parse thành dict trước
        if isinstance(img_desc, str) and img_desc.strip().startswith("{"):
            try:
                import json as _json
                img_desc = _json.loads(img_desc)
            except (ValueError, TypeError):
                pass  # Không phải JSON hợp lệ → giữ nguyên string
        if isinstance(img_desc, str):
            img_text = img_desc
        elif isinstance(img_desc, dict):
            img_parts = []
            for ctx_key in ("style", "audio_summary", "content_context"):
                ctx_val = img_desc.get(ctx_key, "")
                if ctx_val:
                    img_parts.append(f"{ctx_key}: {ctx_val}")
            v_img = img_desc.get("image", "")
            if v_img:
                img_parts.append(v_img)
            for k in ("1", "2", "3", "4"):
                v = img_desc.get(k, "")
                if v:
                    img_parts.append(f"({k}) {v}")
            img_text = "\n".join(img_parts)
        else:
            img_text = str(img_desc) if img_desc else ""

        # Gộp distractor traps (keys "1"-"4")
        trap_parts = [d_traps.get(k, "") for k in ("1", "2", "3", "4")]

        # Auto-fix: thêm/bỏ dấu "." cuối mỗi đáp án — THEO TỪNG CÂU HỎI con (qidx = n)
        has_period = _period_for(kind, n)
        if has_period:
            answers = [a.rstrip() + "." if a.strip() and not a.rstrip().endswith((".", "?", "!", "…", "~")) and a.strip() not in ("①", "②", "③", "④", "1. ", "2. ", "3. ", "4. ") else a for a in answers]
        else:
            answers = [a.rstrip().rstrip(".") if a.strip() and a.strip() not in ("①", "②", "③", "④") and a.rstrip().endswith(".") and not a.rstrip().endswith(("?", "!", "…", "~")) else a for a in answers]

        # Auto-fix: dấu "." cuối mỗi dòng dịch đáp án trong explain — theo cùng quy tắc câu hỏi con
        if has_period:
            explain_vi = _fix_explain_periods(explain.get("vi", ""))
            explain_en = _fix_explain_periods(explain.get("en", ""))
        else:
            explain_vi = _strip_explain_periods(explain.get("vi", ""))
            explain_en = _strip_explain_periods(explain.get("en", ""))

        row[f"q_text_{n}"] = content.get("q_text", "")
        row[f"q_point_{n}"] = content.get("q_point", "")
        row[f"view_q_image_{n}"] = ""
        row[f"q_image_{n}"] = content.get("q_image", "")
        row[f"q_answer_{n}"] = "\n".join(answers)
        row[f"q_correct_{n}"] = content.get("q_correct", "")
        row[f"explain_vi_{n}"] = explain_vi
        row[f"explain_en_{n}"] = explain_en
        row[f"q_image_desc_{n}"] = img_text
        row[f"question_feature_{n}"] = content.get("question_feature", "")
        row[f"difficulty_{n}"] = content.get("difficulty", "")
        row[f"distractor_trap_{n}"] = "\n".join(trap_parts)

    return row


def validate_question(question):
    """
    Validate 1 câu hỏi đọc, trả về list các lỗi (rỗng = OK).
    """
    errors = []
    kind = str(question.get("kind", ""))
    level = question.get("level")

    for field in ("title", "general", "content", "level", "kind", "tag"):
        if not question.get(field):
            errors.append(f"Thiếu trường '{field}'")

    general = question.get("general", {})
    content_list = question.get("content", [])

    # Kiểm tra nội dung đọc — ít nhất 1 trong: g_text, q_text, q_image phải có
    has_g_text = bool(general.get("g_text", "").strip())
    has_q_text = any(c.get("q_text", "").strip() for c in content_list)
    def _get_image_desc(c):
        qid = c.get("q_image_description")
        if isinstance(qid, dict):
            return (qid.get("image") or "").strip()
        if isinstance(qid, str):
            return qid.strip()
        return ""
    has_q_image = any((c.get("q_image") or "").strip() or _get_image_desc(c)
                      for c in content_list)
    if not has_g_text and not has_q_text and not has_q_image:
        errors.append("Không có nội dung đọc (g_text, q_text, hoặc q_image đều rỗng)")

    declared = question.get("count_question")
    actual = len(content_list)
    if declared is not None and declared != actual:
        errors.append(f"count_question={declared} nhưng content có {actual} phần tử")

    valid_levels = {1, 2}
    if level not in valid_levels:
        errors.append(f"level={level} không hợp lệ (phải là 1 hoặc 2)")

    for idx, content in enumerate(content_list):
        prefix = f"content[{idx}]"
        q_correct = content.get("q_correct")
        if q_correct not in (1, 2, 3, 4):
            errors.append(f"{prefix}: q_correct={q_correct} không nằm trong 1-4")

        answers = content.get("q_answer", [])
        if len(answers) != 4:
            errors.append(f"{prefix}: cần đúng 4 đáp án, hiện có {len(answers)}")
        else:
            stripped = [a.strip() for a in answers]
            if len(set(stripped)) < 4:
                dupes = [a for a in stripped if stripped.count(a) > 1]
                errors.append(f"{prefix}: đáp án trùng nhau: {set(dupes)}")

        explain = content.get("explain", {})
        if not explain.get("vi"):
            errors.append(f"{prefix}: thiếu explain tiếng Việt")
        if not explain.get("en"):
            errors.append(f"{prefix}: thiếu explain tiếng Anh")

        if not content.get("q_point"):
            errors.append(f"{prefix}: thiếu q_point")

    return errors


def save_questions(questions, output_dir=None, append=False):
    """Lưu danh sách câu hỏi thành CSV, nhóm theo level/kind."""
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Tính max count_question để xác định số cột
    max_cq = max((len(q.get("content", [])) for q in questions), default=1)
    columns = get_csv_columns(max_cq)

    by_kind = defaultdict(list)
    kind_seq = defaultdict(int)
    for q in questions:
        kind = str(q.get("kind", "")).strip()
        if not kind or kind == "unknown":
            print(f"⚠️ Skipping question with empty/unknown kind: {q.get('title', 'N/A')}")
            continue
        seq = kind_seq[kind]
        kind_seq[kind] += 1
        row = flatten_question(q, timestamp=timestamp, seq=seq)
        by_kind[kind].append(row)

    def get_level_folder(kind):
        level = by_kind[kind][0]["level"] if by_kind[kind] else ""
        return f"level_{level}"

    created_files = {}

    for kind, rows in sorted(by_kind.items()):
        level_folder = get_level_folder(kind)
        folder = os.path.join(output_dir, level_folder)
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, f"{kind}.csv")
        file_exists = os.path.exists(filepath)
        mode = "a" if (append and file_exists) else "w"

        with open(filepath, mode, newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
            if mode == "w" or not file_exists:
                writer.writeheader()
            writer.writerows(rows)

        created_files[kind] = filepath
        action = "appended" if (append and file_exists) else "created"
        print(f"  [{kind}] {len(rows)} rows -> {filepath} ({action})")

    return created_files


def validate_and_report(questions):
    """Validate tất cả câu hỏi, in báo cáo."""
    total = len(questions)
    passed = 0
    failed = 0
    warned = 0

    for i, q in enumerate(questions):
        kind = q.get("kind", "?")
        errs = validate_question(q)
        if errs:
            failed += 1
            print(f"\n  X Cau {i+1} (kind={kind}): {len(errs)} loi")
            for e in errs:
                print(f"    - {e}")
        else:
            passed += 1

        # Cảnh báo độ dài g_text / text_question (không tính là lỗi, không chặn lưu)
        for w in check_text_lengths(q):
            warned += 1
            print(f"  ! Cau {i+1} (kind={kind}): {w}")

    print(f"\n{'='*50}")
    print(f"  Tong: {total} | Passed: {passed} | Failed: {failed} | Canh bao do dai: {warned}")
    print(f"{'='*50}")
    return failed == 0


def save_as_json(questions, output_dir=None):
    """Lưu câu hỏi thành JSON theo kind (giữ nguyên format gốc)."""
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    by_kind = defaultdict(list)
    for q in questions:
        kind = str(q.get("kind", "unknown"))
        by_kind[kind].append(q)

    created_files = {}
    for kind, items in sorted(by_kind.items()):
        level = items[0].get("level", "")
        folder = os.path.join(output_dir, f"level_{level}")
        os.makedirs(folder, exist_ok=True)

        filepath = os.path.join(folder, f"{kind}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        created_files[kind] = filepath
        print(f"  [{kind}] {len(items)} questions -> {filepath}")

    return created_files


def csv_to_json(csv_path):
    """Đọc CSV và chuyển ngược thành list question JSON."""
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    questions = []
    for row in rows:
        count_q = _to_int(row.get("count_question", 1)) or 1

        general = {
            "g_text": row.get("g_text", ""),
            "g_text_translate": {
                "vi": row.get("g_text_vi", ""),
                "en": row.get("g_text_en", ""),
            },
            "g_text_audio": "",
            "g_text_audio_translate": {"vi": "", "en": ""},
            "g_audio": "",
            "g_image": "",
        }

        content = []
        for n in range(1, count_q + 1):
            q_answer_raw = row.get(f"q_answer_{n}", "")
            answers = q_answer_raw.split("\n") if q_answer_raw else ["", "", "", ""]

            trap_raw = row.get(f"distractor_trap_{n}", "")
            traps = trap_raw.split("\n") if trap_raw else ["", "", "", ""]
            while len(traps) < 4:
                traps.append("")

            item = {
                "q_text": row.get(f"q_text_{n}", ""),
                "q_image": "",
                "q_point": _to_int(row.get(f"q_point_{n}", 0)),
                "q_answer": answers,
                "q_correct": _to_int(row.get(f"q_correct_{n}", 1)),
                "explain": {
                    "vi": row.get(f"explain_vi_{n}", ""),
                    "en": row.get(f"explain_en_{n}", ""),
                },
                "question_feature": row.get(f"question_feature_{n}", ""),
                "difficulty": _to_int(row.get(f"difficulty_{n}", 0)) or "",
                "distractor_traps": {
                    "1": traps[0], "2": traps[1], "3": traps[2], "4": traps[3],
                },
            }

            img_desc = row.get(f"q_image_desc_{n}", "")
            if img_desc:
                item["q_image_description"] = {"image": img_desc}

            content.append(item)

        question = {
            "title": row.get("title", ""),
            "general": general,
            "content": content,
            "level": _to_int(row.get("level", 1)),
            "kind": row.get("kind", ""),
            "count_question": count_q,
            "tag": row.get("tag", "read"),
            "topic": row.get("topic", ""),
        }
        questions.append(question)

    return questions


def merge_csvs(output_dir=None):
    """Gom tất cả CSV trong output_dir thành 1 file all_questions.csv."""
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    all_rows = []
    all_fieldnames = set()
    for root, dirs, files in os.walk(output_dir):
        for fname in sorted(files):
            if fname.endswith(".csv") and fname != "all_questions.csv":
                fpath = os.path.join(root, fname)
                with open(fpath, "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    if rows:
                        all_fieldnames.update(reader.fieldnames or [])
                    all_rows.extend(rows)

    if not all_rows:
        print("Khong tim thay CSV nao.")
        return None

    # Xác định max count_question từ fieldnames
    max_cq = 1
    for fn in all_fieldnames:
        if fn.startswith("q_text_"):
            try:
                n = int(fn.split("_")[-1])
                max_cq = max(max_cq, n)
            except ValueError:
                pass
    columns = get_csv_columns(max_cq)

    out_path = os.path.join(output_dir, "all_questions.csv")
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Merged {len(all_rows)} rows -> {out_path}")
    return out_path


# ─── Post-process: fix dấu chấm trên CSV đã gen ────────────────────────────────

def fix_csv_periods(output_dir=None):
    """
    Quét TẤT CẢ CSV trong output_dir, thêm/bỏ dấu chấm cuối đáp án + explain
    THEO TỪNG CÂU HỎI con (map _ANSWER_PERIOD). Phần Đọc đa số KHÔNG dấu chấm.
    Dùng khi AI gen CSV trực tiếp mà không qua flatten_question.
    """
    import glob as _glob

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    total_fixed = 0

    for csvfile in sorted(_glob.glob(os.path.join(output_dir, "level_*", "*.csv"))):
        basename = os.path.splitext(os.path.basename(csvfile))[0]
        # Bỏ qua file tạm _p* (parallel) và all_questions
        if "_p" in basename and basename.split("_p")[-1].isdigit():
            continue
        if basename == "all_questions":
            continue

        try:
            with open(csvfile, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                fieldnames = reader.fieldnames
                rows = list(reader)
        except Exception as e:
            print(f"  ⚠️ Skip {basename}: {e}")
            continue

        if not rows or not fieldnames:
            continue

        changed = 0
        for row in rows:
            row_kind = row.get("kind", "").strip() or basename
            # Fix q_answer_N / explain_*_N: thêm hoặc bỏ dấu chấm theo từng câu hỏi con
            for key in list(row.keys()):
                _m = re.search(r"_(\d+)$", key)
                qidx = int(_m.group(1)) if _m else 1
                row_has_period = _period_for(row_kind, qidx)

                if key.startswith("q_answer_") and row[key]:
                    lines = row[key].split("\n")
                    new_lines = []
                    for l in lines:
                        s = l.rstrip()
                        if not s or s in ("①", "②", "③", "④"):
                            new_lines.append(l)
                            continue
                        if row_has_period:
                            if not s.endswith((".", "?", "!", "…", "~")):
                                s = s + "."
                                changed += 1
                        else:
                            if s.endswith(".") and not s.endswith(("?", "!", "…", "~")):
                                s = s.rstrip(".")
                                changed += 1
                        new_lines.append(s)
                    row[key] = "\n".join(new_lines)

                # Fix explain: thêm/bỏ dấu chấm dòng đáp án
                if key.startswith("explain_") and row[key]:
                    fixed = _fix_explain_periods(row[key]) if row_has_period else _strip_explain_periods(row[key])
                    if fixed != row[key]:
                        changed += 1
                        row[key] = fixed

        if changed > 0:
            with open(csvfile, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(rows)
            total_fixed += changed
            print(f"  ✅ {basename}: fixed {changed} items ({len(rows)} rows)")
        else:
            print(f"  ── {basename}: OK ({len(rows)} rows)")

    print(f"\n  Tổng: fixed {total_fixed} items")
    return total_fixed


def stats(questions):
    """In thống kê nhanh danh sách câu hỏi."""
    by_kind = defaultdict(int)
    by_level = defaultdict(int)
    for q in questions:
        by_kind[str(q.get("kind", "?"))] += 1
        by_level[q.get("level", "?")] += 1

    print(f"\n  Tong: {len(questions)} cau hoi")
    print(f"  Theo level: {dict(sorted(by_level.items()))}")
    print(f"  Theo kind:")
    for k, v in sorted(by_kind.items()):
        print(f"    {k}: {v}")


# ─── Helpers ────────────────────────────────────────────────────────────────────

def _to_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


# ─── CLI ────────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Luu cau hoi doc TOPIK I & II tu JSON ra CSV theo kind"
    )
    parser.add_argument("input", nargs="?", default=None,
                        help="File JSON chua cau hoi da gen (bỏ qua khi dùng --fix-periods)")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--append", "-a", action="store_true")
    parser.add_argument("--validate-only", "-v", action="store_true")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--merge", action="store_true")
    parser.add_argument("--fix-periods", action="store_true",
                        help="Post-process: fix dau cham cuoi dap an + explain trong tat ca CSV")

    args = parser.parse_args()

    # Mode fix-periods: không cần input JSON
    if args.fix_periods:
        print(f"\n>>> Fix periods cho tat ca CSV trong {args.output_dir}")
        fix_csv_periods(output_dir=args.output_dir)
        print("\nHoan thanh!")
        return

    # Mode bình thường: cần input JSON
    if not args.input:
        parser.error("input is required (hoặc dùng --fix-periods)")

    print(f"\nDoc: {args.input}")
    questions = load_json(args.input)
    stats(questions)

    print(f"\nValidate...")
    all_ok = validate_and_report(questions)

    if args.validate_only:
        sys.exit(0 if all_ok else 1)

    if not all_ok:
        print("\n[!] Co loi validation. Van tiep tuc luu...")

    print(f"\nLuu CSV -> {args.output_dir}")
    save_questions(questions, output_dir=args.output_dir, append=args.append)

    if args.json:
        print(f"\nLuu JSON -> {args.output_dir}")
        save_as_json(questions, output_dir=args.output_dir)

    if args.merge:
        print(f"\nMerge CSV...")
        merge_csvs(output_dir=args.output_dir)

    print("\nHoan thanh!")


if __name__ == "__main__":
    main()
