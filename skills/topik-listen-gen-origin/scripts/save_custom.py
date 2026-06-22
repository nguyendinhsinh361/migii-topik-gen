#!/usr/bin/env python3
"""Save a single question JSON to a custom CSV path with append support."""
import json, sys, os, csv
from datetime import datetime

data = json.loads(sys.stdin.read())
output_path = sys.argv[1]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

columns = [
    "id", "kind", "level", "tag", "title", "count_question",
    "view_g_image", "g_image", "view_g_audio", "g_audio",
    "g_text", "g_text_vi", "g_text_en",
    "g_text_audio", "g_text_audio_vi", "g_text_audio_en",
    "topic",
    "q_text_1", "q_point_1", "q_answer_1", "q_correct_1",
    "explain_vi_1", "explain_en_1",
    "view_q_image_1", "q_image_1", "q_image_desc_1",
    "question_feature_1", "difficulty_1", "distractor_trap_1",
    "created_at",
]

questions = data if isinstance(data, list) else data.get("questions", [data])

rows = []
for seq, q in enumerate(questions):
    general = q.get("general", {})
    content_list = q.get("content", [])
    audio_trans = general.get("g_text_audio_translate", {})
    kind = str(q.get("kind", ""))

    row = {
        "id": f"{kind}+{uuid.uuid4().hex}",
        "kind": kind,
        "level": q.get("level", ""),
        "tag": q.get("tag", "listen"),
        "title": q.get("title", ""),
        "count_question": q.get("count_question", 1),
        "view_g_image": "", "g_image": general.get("g_image", ""),
        "view_g_audio": "", "g_audio": general.get("g_audio", ""),
        "g_text": general.get("g_text", ""), "g_text_vi": "", "g_text_en": "",
        "g_text_audio": general.get("g_text_audio", ""),
        "g_text_audio_vi": audio_trans.get("vi", ""),
        "g_text_audio_en": audio_trans.get("en", ""),
        "topic": q.get("topic", ""),
        "created_at": timestamp,
    }

    top_img_desc = q.get("q_image_description", {})

    for idx, content in enumerate(content_list):
        n = idx + 1
        answers = content.get("q_answer", [])
        while len(answers) < 4:
            answers.append("")
        explain = content.get("explain", {})
        img_desc = top_img_desc if top_img_desc else content.get("q_image_description", {})
        d_traps = content.get("distractor_traps", {})

        img_parts = []
        for k in ("1", "2", "3", "4"):
            v = img_desc.get(k, "")
            if v:
                img_parts.append(f"({k}) {v}")
        img_text = "\n".join(img_parts)

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

    rows.append(row)

file_exists = os.path.exists(output_path)
mode = "a" if file_exists else "w"

with open(output_path, mode, newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
    if mode == "w":
        writer.writeheader()
    writer.writerows(rows)

action = "appended" if mode == "a" else "created"
print(f"1 row -> {output_path} ({action})")
