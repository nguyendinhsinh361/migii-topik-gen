#!/usr/bin/env python3
"""
save_listen.py — Lưu câu hỏi nghe TOPIK I & II đã gen ra CSV theo từng kind.

Nằm trong: skills/topik-listen-gen-origin/scripts/

Mỗi câu hỏi = 1 dòng CSV. Content items được đánh số _1, _2, ... theo count_question.

Cách dùng:
  python skills/topik-listen-gen-origin/scripts/save_listen.py input.json
  python skills/topik-listen-gen-origin/scripts/save_listen.py input.json -o output/listen-origin
  python skills/topik-listen-gen-origin/scripts/save_listen.py input.json --append
  python skills/topik-listen-gen-origin/scripts/save_listen.py input.json --validate-only

Cấu trúc output:
  output/listen-origin/
  ├── level_1/
  │   ├── 110001.csv
  │   └── ...
  └── level_2/
      ├── 210001_1.csv
      └── ...
"""

import csv
import json
import os
import uuid
import re
import sys
from datetime import datetime
from collections import defaultdict

# ─── Cấu hình ──────────────────────────────────────────────────────────────────

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SKILL_DIR))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "listen-origin")

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

# ─── Quy tắc biên tập theo kind (dấu chấm / độ dài / format) ───────────────────
# Nguồn: "MIGII TOPIK - Listen Rule - Gen Question AI New.xlsx" (biên tập viên bổ sung).
#
# _ANSWER_PERIOD: dấu "." cuối mỗi đáp án — THEO TỪNG CÂU HỎI con.
#   value = tuple (period_q1, period_q2, ...) cho từng câu hỏi con (1-based).
#     True  = đáp án PHẢI kết thúc bằng "." (câu hoàn chỉnh)
#     False = KHÔNG có "." (cụm danh từ / cụm ngắn / đáp án ảnh ①②③④)
#   ⚠️ Kind 2 câu hỏi (110008_*, 210006_*, 210007_*) thường KHÁC nhau giữa Q1 và Q2
#      (vd: Q1 là cụm danh từ -> False, Q2 là câu nội dung -> True).
_ANSWER_PERIOD = {
    "110001": (True,),
    "110002": (True,),
    "110003": (False,),
    "110004": (False,),
    "110005": (False,),
    "110006": (True,),
    "110007": (True,),
    "110008_1": (False, True),
    "110008_2": (False, True),
    "110008_3": (False, True),
    "210001_1": (False,),
    "210001_2": (False,),
    "210002": (True,),
    "210003": (True,),
    "210004_(1)": (True,),
    "210004_(2)": (True,),
    "210004_(3)": (True,),
    "210004_(4)": (True,),
    "210005_(1)": (True,),
    "210005_(2)": (True,),
    "210006_(1)": (True, True),
    "210006_(2)": (True, True),
    "210006_(3)": (True, True),
    "210006_(4)": (False, True),
    "210006_(5)": (False, True),
    "210006_(6)": (True, True),
    "210006_(7)": (False, True),
    "210006_(8)": (True, True),
    "210007_(1)": (True, True),
    "210007_(2)": (True, True),
    "210007_(3)": (True, True),
    "210007_(4)": (False, True),
    "210007_(5)": (True, True),
    "210007_(6)": (True, True),
    "210007_(7)": (True, True),
}

# _AUDIO_LENGTH: độ dài g_text_audio (số ký tự Hàn, KHÔNG tính nhãn 남자:/여자: và dòng trống).
#   value = list các khoảng (min, max). Nhiều khoảng = kind có nhiều cấu trúc lượt thoại
#   (đạt nếu nằm trong BẤT KỲ khoảng nào).
_AUDIO_LENGTH = {
    "110001": [(35, 45)],
    "110002": [(35, 45)],
    "110003": [(35, 45)],
    "110004": [(35, 45)],
    "110005": [(45, 55)],
    "110006": [(85, 95), (140, 160)],   # 3 lượt thoại / 4 lượt thoại
    "110007": [(120, 140)],
    "110008_1": [(160, 180)],
    "110008_2": [(240, 260)],
    "110008_3": [(330, 350)],
    "210001_1": [(65, 85)],
    "210001_2": [(140, 160)],
    "210002": [(80, 100)],
    "210003": [(120, 170)],
    "210004_(1)": [(120, 150)],
    "210004_(2)": [(150, 180)],
    "210004_(3)": [(140, 170)],
    "210004_(4)": [(170, 200)],
    "210005_(1)": [(100, 130), (140, 170)],  # 3 lượt thoại / 4 lượt thoại
    "210005_(2)": [(170, 200)],
    "210006_(1)": [(240, 290)],
    "210006_(2)": [(210, 260)],
    "210006_(3)": [(240, 290)],
    "210006_(4)": [(260, 310)],
    "210006_(5)": [(260, 310)],
    "210006_(6)": [(260, 310)],
    "210006_(7)": [(260, 310)],
    "210006_(8)": [(260, 310)],
    "210007_(1)": [(320, 340)],
    "210007_(2)": [(280, 340)],
    "210007_(3)": [(280, 340)],
    "210007_(4)": [(320, 340)],
    "210007_(5)": [(300, 340)],
    "210007_(6)": [(300, 340)],
    "210007_(7)": [(350, 380)],
}

# _FIXED_ORDER: thứ tự giới tính người nói trong g_text_audio.
#   True  = FIX CỨNG đúng thứ tự nam-nữ như format (format KHÔNG có "hoặc ngược lại").
#   False = được phép đảo nam↔nữ (format CÓ "hoặc ngược lại").
_FIXED_ORDER = {
    "110001": False, "110002": False, "110003": False, "110004": False,
    "110005": False, "110006": False, "110007": False,
    "110008_1": True, "110008_2": False, "110008_3": False,
    "210001_1": False, "210001_2": True,
    "210002": False, "210003": False,
    "210004_(1)": False, "210004_(2)": True, "210004_(3)": True, "210004_(4)": True,
    "210005_(1)": True, "210005_(2)": True,
    "210006_(1)": True, "210006_(2)": True, "210006_(3)": True, "210006_(4)": True,
    "210006_(5)": True, "210006_(6)": False, "210006_(7)": True, "210006_(8)": True,
    "210007_(1)": True, "210007_(2)": True, "210007_(3)": True, "210007_(4)": True,
    "210007_(5)": True, "210007_(6)": True, "210007_(7)": True,
}


def _period_for(kind, qidx):
    """True/False: đáp án của câu hỏi con thứ qidx (1-based) có dấu '.' cuối không.
    Mặc định True nếu kind chưa khai báo (an toàn cho câu hoàn chỉnh)."""
    rule = _ANSWER_PERIOD.get(str(kind).strip())
    if not rule:
        return True
    return rule[qidx - 1] if 0 <= qidx - 1 < len(rule) else rule[-1]


def _count_korean_audio_chars(audio):
    """Đếm ĐỘ DÀI g_text_audio theo cách của BIÊN TẬP VIÊN = đếm gần như Google Dịch:
    TÍNH CẢ nhãn 남자:/여자:, dấu cách, dấu câu, xuống dòng — NHƯNG **KHÔNG tính** ký tự
    gạch dưới `_` của dòng trống (___)."""
    if not audio:
        return 0
    return len(audio.replace('_', '').strip())


def check_audio_length(question):
    """Trả về list cảnh báo nếu độ dài g_text_audio lệch khoảng quy định (không chặn lưu)."""
    kind = str(question.get("kind", "")).strip()
    spec = _AUDIO_LENGTH.get(kind)
    if not spec:
        return []
    n = _count_korean_audio_chars(question.get("general", {}).get("g_text_audio", ""))
    if any(lo <= n <= hi for lo, hi in spec):
        return []
    ranges = " hoặc ".join(f"{lo}~{hi}" for lo, hi in spec)
    return [f"g_text_audio dài {n} ký tự, ngoài khoảng quy định {ranges}"]


# Backward-compat: tập kind có dấu chấm ở câu hỏi đầu (Q1). Giữ cho tham chiếu cũ.
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
    """Bỏ dấu . cuối mỗi dòng dịch đáp án trong explain (trước separator ----) cho kind KHÔNG có dấu chấm."""
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
    # Dùng module-level _fix_explain_periods / _strip_explain_periods

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    general = question.get("general", {})
    content_list = question.get("content", [])
    kind = re.sub(r"_p\d+$", "", str(question.get("kind", "")))   # bỏ hậu tố _p<n> của file tạm parallel (id/kind sạch)
    audio_translate = general.get("g_text_audio_translate", {})

    row = {
        "id": f"{kind}_{uuid.uuid4().hex}",
        "kind": kind,
        "level": question.get("level", ""),
        "tag": question.get("tag", "listen"),
        "title": question.get("title", ""),
        "count_question": question.get("count_question", 1),
        "view_g_image": "",
        "g_image": general.get("g_image", ""),
        "view_g_audio": "",
        "g_audio": general.get("g_audio", ""),
        "g_text": general.get("g_text", ""),
        "g_text_vi": "",
        "g_text_en": "",
        "g_text_audio": general.get("g_text_audio", ""),
        "g_text_audio_vi": audio_translate.get("vi", ""),
        "g_text_audio_en": audio_translate.get("en", ""),
        "topic": question.get("topic", ""),
        "created_at": timestamp,
    }

    # q_image_desc nằm ở top-level hoặc content-level
    # Hỗ trợ cả tên cũ (q_image_description) và tên mới (q_image_desc)
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

        # Xử lý image desc — hỗ trợ cả string (format mới) và dict (format cũ)
        # Nếu string chứa JSON → parse thành dict trước
        if isinstance(img_desc, str) and img_desc.strip().startswith("{"):
            try:
                import json as _json
                img_desc = _json.loads(img_desc)
            except (ValueError, TypeError):
                pass  # Không phải JSON hợp lệ → giữ nguyên string
        if isinstance(img_desc, str):
            # Format mới: string hoàn chỉnh (style + audio + descriptions)
            img_text = img_desc
        elif isinstance(img_desc, dict):
            # Format cũ: dict với keys "1"-"4" + "image"
            img_parts = []
            # Giữ style/audio context nếu có
            for ctx_key in ("style", "audio_summary", "audio_context", "content_context"):
                ctx_val = img_desc.get(ctx_key, "")
                if ctx_val:
                    img_parts.append(f"{ctx_key}: {ctx_val}")
            for k in ("1", "2", "3", "4"):
                v = img_desc.get(k, "")
                if v:
                    img_parts.append(f"({k}) {v}")
            v_img = img_desc.get("image", "")
            if v_img:
                img_parts.append(v_img)
            img_text = "\n".join(img_parts)
        else:
            img_text = str(img_desc) if img_desc else ""

        # Gộp distractor traps (keys "1"-"4")
        trap_parts = [d_traps.get(k, "") for k in ("1", "2", "3", "4")]

        # Auto-fix: thêm/bỏ dấu "." cuối mỗi đáp án — THEO TỪNG CÂU HỎI con (qidx = n)
        has_period = _period_for(kind, n)
        if has_period:
            answers = [a.rstrip() + "." if a.strip() and not a.rstrip().endswith((".", "?", "!", "…", "~")) and a.strip() not in ("①", "②", "③", "④") else a for a in answers]
        else:
            # Bỏ dấu chấm cuối nếu model tự thêm (trừ image answers)
            answers = [a.rstrip().rstrip(".") if a.strip() and a.strip() not in ("①", "②", "③", "④") and a.rstrip().endswith(".") and not a.rstrip().endswith(("?", "!", "…", "~")) else a for a in answers]

        # Auto-fix: dấu "." cuối mỗi dòng dịch đáp án trong explain — theo cùng quy tắc câu hỏi con
        if has_period:
            explain_vi = _fix_explain_periods(explain.get("vi", ""))
            explain_en = _fix_explain_periods(explain.get("en", ""))
        else:
            # Câu hỏi con KHÔNG có dấu chấm → strip "." khỏi dòng dịch đáp án trong explain
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
    Validate 1 câu hỏi, trả về list các lỗi (rỗng = OK).
    """
    errors = []
    kind = str(question.get("kind", ""))
    level = question.get("level")

    for field in ("title", "general", "content", "level", "kind", "tag"):
        if not question.get(field):
            errors.append(f"Thiếu trường '{field}'")

    general = question.get("general", {})
    content_list = question.get("content", [])

    if not general.get("g_text_audio", "").strip():
        errors.append("g_text_audio rỗng")

    audio_translate = general.get("g_text_audio_translate", {})
    if not audio_translate.get("vi"):
        errors.append("Thiếu bản dịch audio tiếng Việt")
    if not audio_translate.get("en"):
        errors.append("Thiếu bản dịch audio tiếng Anh")

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
            print(f"⚠️ Skipping question with empty/unknown kind")
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


def check_answer_balance(question):
    """Cảnh báo nếu đáp án ĐÚNG dài hơn đáng kể so với các đáp án sai (dễ lộ đáp án)."""
    warnings = []
    for idx, c in enumerate(question.get("content", []) or []):
        ans = [str(a).strip() for a in (c.get("q_answer", []) or [])
               if str(a).strip() and str(a).strip() not in ("①", "②", "③", "④")]
        if len(ans) < 4:
            continue
        try:
            qc = int(c.get("q_correct"))
        except (TypeError, ValueError):
            continue
        if not (1 <= qc <= len(ans)):
            continue
        clen = len(ans[qc - 1])
        others = [len(a) for j, a in enumerate(ans) if j != qc - 1]
        if not others:
            continue
        avg = sum(others) / len(others)
        if clen > max(others) and clen > 1.3 * avg:
            warnings.append(
                f"cau hoi {idx+1}: dap an DUNG (#{qc}) dai {clen} ky tu, "
                f"dai hon dang ke so voi 3 dap an sai (TB {round(avg)}) -> de lo dap an, nen can bang do dai"
            )
    return warnings


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

        for w in check_answer_balance(q):
            print(f"  ! Cau {i+1} (kind={kind}): [balance] {w}")

        # Cảnh báo độ dài g_text_audio (không tính là lỗi, không chặn lưu)
        for w in check_audio_length(q):
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
        kind = str(q.get("kind", "")).strip()
        if not kind or kind == "unknown":
            print(f"⚠️ Skipping question with empty/unknown kind")
            continue
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
            "g_text": "",
            "g_text_translate": {"vi": "", "en": ""},
            "g_text_audio": row.get("g_text_audio", ""),
            "g_text_audio_translate": {
                "vi": row.get("g_text_audio_vi", ""),
                "en": row.get("g_text_audio_en", ""),
            },
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
            content.append(item)

        question = {
            "title": row.get("title", ""),
            "general": general,
            "content": content,
            "level": _to_int(row.get("level", 1)),
            "kind": row.get("kind", ""),
            "count_question": count_q,
            "tag": row.get("tag", "listen"),
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
    Quét TẤT CẢ CSV trong output_dir, sửa dấu chấm cuối đáp án + explain
    theo _KINDS_WITH_PERIOD. Dùng khi AI gen CSV trực tiếp mà không qua
    flatten_question (ví dụ: opencode run trong gen_listen_origin.sh).
    """
    import glob as _glob

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    total_fixed = 0

    for csvfile in sorted(_glob.glob(os.path.join(output_dir, "level_*", "*.csv"))):
        basename = os.path.splitext(os.path.basename(csvfile))[0]
        # Bỏ qua file tạm _p* (parallel)
        if "_p" in basename and basename.split("_p")[-1].isdigit():
            continue
        if basename == "all_questions":
            continue

        # Xác định kind từ tên file HOẶC từ cột kind trong CSV
        kind_from_name = basename

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

        # Dùng kind từ row đầu tiên nếu có, fallback tên file
        kind = rows[0].get("kind", "").strip() or kind_from_name

        changed = 0
        for row in rows:
            row_kind = row.get("kind", "").strip() or kind
            row_kind = re.sub(r"_p\d+$", "", row_kind)
            # Chuẩn hoá id: {kind}_{uuid 32 hex}. Nếu uuid bị cắt ngắn/thiếu/dính _p -> tạo lại id đầy đủ
            if fieldnames and "id" in fieldnames and row.get("id") is not None:
                _rid = str(row.get("id", ""))
                if not re.fullmatch(re.escape(row_kind) + r"_[0-9a-f]{32}", _rid):
                    row["id"] = f"{row_kind}_{uuid.uuid4().hex}"
                    changed += 1

            # Tìm tất cả cột q_answer_N / explain_*_N
            for key in list(row.keys()):
                # Chỉ số câu hỏi con lấy từ hậu tố _N của tên cột (mặc định 1)
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
                            # Thêm dấu chấm
                            if not s.endswith((".", "?", "!", "…", "~")):
                                s = s + "."
                                changed += 1
                        else:
                            # Bỏ dấu chấm
                            if s.endswith(".") and not s.endswith(("?", "!", "…", "~")):
                                s = s.rstrip(".")
                                changed += 1
                        new_lines.append(s)
                    row[key] = "\n".join(new_lines)

                # Fix explain
                if key.startswith("explain_") and row[key]:
                    # Chỉ fix cột explain_vi_N, explain_en_N
                    if row_has_period:
                        fixed = _fix_explain_periods(row[key])
                    else:
                        fixed = _strip_explain_periods(row[key])
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
        description="Luu cau hoi nghe TOPIK I & II tu JSON ra CSV theo kind"
    )
    # --fix-periods mode: chỉ cần output-dir, không cần input JSON
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
