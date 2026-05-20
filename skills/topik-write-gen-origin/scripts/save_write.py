#!/usr/bin/env python3
"""
save_write.py — Lưu câu hỏi viết TOPIK II đã gen ra CSV theo từng kind.

Nằm trong: skills/topik-write-gen-origin/scripts/

Mỗi câu hỏi = 1 dòng CSV. Content items được đánh số _1, _2, ... theo count_question.

Cách dùng:
  python skills/topik-write-gen-origin/scripts/save_write.py input.json
  python skills/topik-write-gen-origin/scripts/save_write.py input.json -o output/write-origin
  python skills/topik-write-gen-origin/scripts/save_write.py input.json --append
  python skills/topik-write-gen-origin/scripts/save_write.py input.json --validate-only

Cấu trúc output:
  output/write-origin/
  └── level_2/
      ├── 230001.csv
      ├── 230002.csv
      └── 230003.csv
"""

import csv
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

# ─── Cấu hình ──────────────────────────────────────────────────────────────────

# scripts/ → topik-write-gen-origin/ → skills/ → project root
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SKILL_DIR))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "write-origin")

# Cột cố định (question-level)
BASE_COLUMNS = [
    "id", "kind", "level", "tag", "title", "count_question",
    "g_text", "g_text_vi", "g_text_en",
    "g_image", "g_image_desc",
    "topic",
]

# Cột lặp theo content (sẽ thêm hậu tố _1, _2, ...)
CONTENT_COLUMNS = [
    "q_text", "q_point", "q_answer", "q_correct",
    "explain_vi", "explain_en",
    "q_image_desc",
    "question_feature", "difficulty", "distractor_trap",
]


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
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    general = question.get("general", {})
    content_list = question.get("content", [])
    kind = str(question.get("kind", ""))
    g_text_translate = general.get("g_text_translate", {})

    # g_image (biểu đồ — kind 230002)
    g_image = general.get("g_image", "")

    # g_image_desc: ưu tiên g_image_description.image, fallback g_text_image
    g_img_desc_obj = general.get("g_image_description", {})
    g_img_desc = ""
    if isinstance(g_img_desc_obj, dict):
        g_img_desc = g_img_desc_obj.get("image", "")
    if not g_img_desc:
        g_img_desc = general.get("g_text_image", "")

    row = {
        "id": f"{kind}_{timestamp}_q{seq}",
        "kind": kind,
        "level": question.get("level", ""),
        "tag": question.get("tag", "write"),
        "title": question.get("title", ""),
        "count_question": question.get("count_question", 1),
        "g_text": general.get("g_text", ""),
        "g_text_vi": g_text_translate.get("vi", ""),
        "g_text_en": g_text_translate.get("en", ""),
        "g_image": g_image,
        "g_image_desc": g_img_desc,
        "topic": question.get("topic", ""),
        "created_at": timestamp,
    }

    for idx, content in enumerate(content_list):
        n = idx + 1
        answers = content.get("q_answer", [])
        while len(answers) < 4:
            answers.append("")
        explain = content.get("explain", {})
        img_desc = content.get("q_image_description", {})
        d_traps = content.get("distractor_traps", {})

        # Gộp image desc (keys "1"-"4" + "image") thành 1 chuỗi
        img_parts = []
        for k in ("1", "2", "3", "4"):
            v = img_desc.get(k, "")
            if v:
                img_parts.append(f"({k}) {v}")
        v_img = img_desc.get("image", "")
        if v_img:
            img_parts.append(v_img)
        img_text = "\n".join(img_parts)

        # Gộp distractor traps (keys "1"-"4")
        trap_parts = [d_traps.get(k, "") for k in ("1", "2", "3", "4")]

        row[f"q_text_{n}"] = content.get("q_text", "")
        row[f"q_point_{n}"] = content.get("q_point", "")
        row[f"q_answer_{n}"] = "\n".join(answers)
        row[f"q_correct_{n}"] = content.get("q_correct", "")
        row[f"explain_vi_{n}"] = explain.get("vi", "")
        row[f"explain_en_{n}"] = explain.get("en", "")
        row[f"q_image_desc_{n}"] = img_text
        row[f"question_feature_{n}"] = content.get("question_feature", "")
        row[f"difficulty_{n}"] = content.get("difficulty", "")
        row[f"distractor_trap_{n}"] = "\n".join(trap_parts)

    return row


def validate_question(question):
    """
    Validate 1 câu hỏi viết, trả về list các lỗi (rỗng = OK).
    """
    errors = []
    kind = str(question.get("kind", ""))
    level = question.get("level")

    for field in ("title", "general", "content", "level", "kind", "tag"):
        if not question.get(field):
            errors.append(f"Thiếu trường '{field}'")

    general = question.get("general", {})
    content_list = question.get("content", [])

    # tag phải là "write"
    if question.get("tag") != "write":
        errors.append(f"tag='{question.get('tag')}' phải là 'write'")

    # Đề bài — ít nhất 1 trong: g_text, q_text, q_image, g_image phải có nội dung
    has_g_text = bool(general.get("g_text", "").strip())
    def _get_g_image_desc():
        gid = general.get("g_image_description")
        if isinstance(gid, dict):
            return (gid.get("image") or "").strip()
        if isinstance(gid, str):
            return gid.strip()
        return ""
    has_g_image = bool((general.get("g_image") or "").strip()) or bool(_get_g_image_desc())
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
    if not has_g_text and not has_q_text and not has_q_image and not has_g_image:
        errors.append("Không có nội dung đề bài (g_text, q_text, q_image, g_image đều rỗng)")

    declared = question.get("count_question")
    actual = len(content_list)
    if declared is not None and declared != actual:
        errors.append(f"count_question={declared} nhưng content có {actual} phần tử")

    # Write chỉ có TOPIK II (level 2)
    valid_levels = {2}
    if level not in valid_levels:
        errors.append(f"level={level} không hợp lệ (Write chỉ có level 2)")

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
        kind = str(q.get("kind", "unknown"))
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

    print(f"\n{'='*50}")
    print(f"  Tong: {total} | Passed: {passed} | Failed: {failed}")
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
            "g_image": row.get("g_image", ""),
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
            "level": _to_int(row.get("level", 2)),
            "kind": row.get("kind", ""),
            "count_question": count_q,
            "tag": row.get("tag", "write"),
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
        description="Luu cau hoi viet TOPIK II tu JSON ra CSV theo kind"
    )
    parser.add_argument("input", help="File JSON chua cau hoi da gen")
    parser.add_argument("--output-dir", "-o", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--append", "-a", action="store_true")
    parser.add_argument("--validate-only", "-v", action="store_true")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--merge", action="store_true")

    args = parser.parse_args()

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

    print(f"\nMerge CSV...")
    merge_csvs(output_dir=args.output_dir)

    print("\nHoan thanh!")


if __name__ == "__main__":
    main()
