import json
import os

INPUT_FILE = "input/admin_topik.json"
OUTPUT_DIR = "input_clean"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read()

# Fix unescaped quotes before combining dot below (U+0323) inside JSON strings
raw = raw.replace('"\u0323', '\\"\u0323')
data = json.loads(raw)

# Group by tag/level/kind
groups = {}
for item in data:
    tag = str(item.get("tag") or "unknown")
    level = str(item.get("level") or "unknown")
    kind = str(item.get("kind") or "unknown")
    key = (tag, level, kind)
    groups.setdefault(key, []).append(item)

# Write each group
for (tag, level, kind), items in groups.items():
    folder = os.path.join(OUTPUT_DIR, tag, f"level_{level}", kind)
    os.makedirs(folder, exist_ok=True)

    # Parse JSON string fields to actual objects
    clean_items = []
    for item in items:
        clean = dict(item)
        for field in ("general", "content"):
            if isinstance(clean.get(field), str):
                try:
                    clean[field] = json.loads(clean[field])
                except (json.JSONDecodeError, TypeError):
                    pass
        clean_items.append(clean)

    out_path = os.path.join(folder, "questions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(clean_items, f, ensure_ascii=False, indent=2)

    print(f"[{tag}] level={level} kind={kind} -> {len(clean_items)} items -> {out_path}")

print(f"\nDone! Total: {len(data)} items split into {len(groups)} files.")
