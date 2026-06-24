#!/usr/bin/env python3
"""
save_listen.py — Luu cau hoi nghe EPS-TOPIK da gen ra CSV theo tung kind.

Nam trong: skills/topik-listen-gen-eps/scripts/

Moi cau hoi = 1 dong CSV. Content items duoc danh so _1, _2, ... theo count_question.

Cach dung:
  python skills/topik-listen-gen-eps/scripts/save_listen.py input.json
  python skills/topik-listen-gen-eps/scripts/save_listen.py input.json -o output/listen-eps
  python skills/topik-listen-gen-eps/scripts/save_listen.py input.json --append
  python skills/topik-listen-gen-eps/scripts/save_listen.py input.json --validate-only

Cau truc output:
  output/listen-eps/
  └── level_3/
      ├── 310001.csv
      ├── 310002.csv
      └── ...
"""

import csv
import json
import os
import re
import uuid
import sys
from datetime import datetime
from collections import defaultdict

# --- Cau hinh ---

# scripts/ -> topik-listen-gen-eps/ -> skills/ -> project root
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SKILL_DIR))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "listen-eps")

# Cot co dinh (question-level)
BASE_COLUMNS = [
    "id", "kind", "level", "tag", "title", "count_question",
    "view_g_image", "g_image", "view_g_audio", "g_audio",
    "g_text", "g_text_vi", "g_text_en",
    "g_text_audio", "g_text_audio_vi", "g_text_audio_en",
    "topic",
]

# Cot lap theo content (se them hau to _1, _2, ...)
CONTENT_COLUMNS = [
    "q_text", "q_point", "q_answer", "q_correct",
    "explain_vi", "explain_en",
    "view_q_image", "q_image", "q_image_desc",
    "question_feature", "difficulty", "distractor_trap",
]


def get_csv_columns(max_cq):
    """Sinh danh sach cot CSV dua tren max count_question."""
    cols = list(BASE_COLUMNS)
    for n in range(1, max_cq + 1):
        for col in CONTENT_COLUMNS:
            cols.append(f"{col}_{n}")
    cols.append("created_at")
    return cols


# --- Ham chinh ---

def load_json(filepath):
    """Doc file JSON, ho tro ca format {questions: [...]} va [...] thuan."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "questions" in data:
            return data["questions"]
        # Format grouped by kind
        questions = []
        for kind_key, items in data.items():
            if isinstance(items, list):
                questions.extend(items)
        return questions

    raise ValueError(f"Khong nhan dien duoc format JSON: {type(data)}")


def flatten_question(question, timestamp=None, seq=0):
    """
    Chuyen 1 question JSON thanh 1 row dict duy nhat.
    Content items duoc danh so _1, _2, ... nam ngang trong cung 1 dong.
    """
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
        "count_question": question.get("count_question", ""),
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

    # q_image_description nằm ở top-level, không phải trong content[]
    top_img_desc = question.get("q_image_description", {})

    for idx, content in enumerate(content_list):
        n = idx + 1
        answers = content.get("q_answer", [])
        while len(answers) < 4:
            answers.append("")
        explain = content.get("explain", {})
        # Ưu tiên top-level, fallback content-level
        img_desc = top_img_desc if top_img_desc else content.get("q_image_description", {})
        d_traps = content.get("distractor_traps", {})

        # Gop image desc (keys "1"-"4" + "image") thanh 1 chuoi
        img_parts = []
        for k in ("1", "2", "3", "4"):
            v = img_desc.get(k, "")
            if v:
                img_parts.append(f"({k}) {v}")
        v_img = img_desc.get("image", "")
        if v_img:
            img_parts.append(v_img)
        img_text = "\n".join(img_parts)

        # Gop distractor traps (keys "1"-"4")
        trap_parts = [d_traps.get(k, "") for k in ("1", "2", "3", "4")]

        row[f"q_text_{n}"] = content.get("q_text", "")
        row[f"q_point_{n}"] = content.get("q_point", "")
        row[f"view_q_image_{n}"] = ""
        row[f"q_image_{n}"] = content.get("q_image", "")
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
    Validate 1 cau hoi EPS-TOPIK, tra ve list cac loi (rong = OK).

    Kiem tra:
      1. Cac truong bat buoc ton tai
      2. q_correct nam trong 1-4
      3. 4 dap an khong trung nhau
      4. count_question khop len(content) — None duoc chap nhan
      5. level hop le (EPS chi co level 3)
      6. explain co ca vi va en
      7. Audio khong rong
      8. q_point — EPS cho phep null, khong bao loi
    """
    errors = []
    kind = str(question.get("kind", ""))
    level = question.get("level")

    for field in ("title", "general", "content", "level", "kind", "tag"):
        if not question.get(field):
            errors.append(f"Thieu truong '{field}'")

    general = question.get("general", {})
    content_list = question.get("content", [])

    if not general.get("g_text_audio", "").strip():
        errors.append("g_text_audio rong")

    audio_translate = general.get("g_text_audio_translate", {})
    if not audio_translate.get("vi"):
        errors.append("Thieu ban dich audio tieng Viet")
    if not audio_translate.get("en"):
        errors.append("Thieu ban dich audio tieng Anh")

    # count_question — None duoc chap nhan, chi canh bao khi khai sai
    declared = question.get("count_question")
    actual = len(content_list)
    if declared is not None and declared != actual:
        errors.append(f"count_question={declared} nhung content co {actual} phan tu")

    # EPS chi co level 3
    valid_levels = {3}
    if level not in valid_levels:
        errors.append(f"level={level} khong hop le (EPS phai la 3)")

    for idx, content in enumerate(content_list):
        prefix = f"content[{idx}]"
        q_correct = content.get("q_correct")
        if q_correct not in (1, 2, 3, 4):
            errors.append(f"{prefix}: q_correct={q_correct} khong nam trong 1-4")

        answers = content.get("q_answer", [])
        if len(answers) != 4:
            errors.append(f"{prefix}: can dung 4 dap an, hien co {len(answers)}")
        else:
            stripped = [a.strip() for a in answers]
            if len(set(stripped)) < 4:
                dupes = [a for a in stripped if stripped.count(a) > 1]
                errors.append(f"{prefix}: dap an trung nhau: {set(dupes)}")

        explain = content.get("explain", {})
        if not explain.get("vi"):
            errors.append(f"{prefix}: thieu explain tieng Viet")
        if not explain.get("en"):
            errors.append(f"{prefix}: thieu explain tieng Anh")

        # q_point — EPS thuong co null q_point, khong bao loi

    return errors


def save_questions(questions, output_dir=None, append=False):
    """Luu danh sach cau hoi thanh CSV, nhom theo level/kind."""
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Tinh max count_question de xac dinh so cot
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
    """Validate tat ca cau hoi, in bao cao."""
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

        for w in check_answer_balance(q):
            print(f"  ! Cau {i+1} (kind={kind}): [balance] {w}")

    print(f"\n{'='*50}")
    print(f"  Tong: {total} | Passed: {passed} | Failed: {failed}")
    print(f"{'='*50}")
    return failed == 0


def save_as_json(questions, output_dir=None):
    """Luu cau hoi thanh JSON theo kind (giu nguyen format goc)."""
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
    """Doc CSV va chuyen nguoc thanh list question JSON."""
    rows = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    questions = []
    for row in rows:
        count_q = _to_int(row.get("count_question")) or 1

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
                "q_point": _to_int_or_none(row.get(f"q_point_{n}")),
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
            "level": _to_int(row.get("level", 3)),
            "kind": row.get("kind", ""),
            "count_question": _to_int_or_none(row.get("count_question")),
            "tag": row.get("tag", "listen"),
            "topic": row.get("topic", ""),
        }
        questions.append(question)

    return questions


def merge_csvs(output_dir=None):
    """Gom tat ca CSV trong output_dir thanh 1 file all_questions.csv."""
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

    # Xac dinh max count_question tu fieldnames
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
    """In thong ke nhanh danh sach cau hoi."""
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


# --- Helpers ---

def _to_int(val):
    """Chuyen ve int, tra ve 0 neu khong duoc."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def _to_int_or_none(val):
    """Chuyen ve int, tra ve None neu khong duoc (cho q_point EPS)."""
    if val is None or val == "" or val == "None":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


# --- CLI ---

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Luu cau hoi nghe EPS-TOPIK tu JSON ra CSV theo kind"
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

    if args.merge:
        print(f"\nMerge CSV...")
        merge_csvs(output_dir=args.output_dir)

    print("\nHoan thanh!")


if __name__ == "__main__":
    main()
