#!/bin/bash
# Gen câu hỏi Read Origin
# Usage:
#   bash scripts/gen_read_origin.sh                        # Tuần tự, 1 bài/dạng
#   bash scripts/gen_read_origin.sh 120001 3               # Gen 3 bài dạng 120001
#   bash scripts/gen_read_origin.sh 220005_1_(1) 2         # Gen 2 bài dạng 220005_1_(1)
#   bash scripts/gen_read_origin.sh --parallel 3           # Song song 3 sessions
#   bash scripts/gen_read_origin.sh --parallel 3 120001 5  # Song song 3, dạng 120001, 5 bài

SKILL="skills/topik-read-gen-origin"
OUTPUT="output/read-origin"
PARALLEL=1

# Parse --parallel flag
if [[ "$1" == "--parallel" ]]; then
  PARALLEL="$2"
  shift 2
fi

gen_kind() {
  local kind="$1" count="$2" level="$3"
  mkdir -p "$OUTPUT/$level"
  for i in $(seq 1 $count); do
    echo "[$(date +%H:%M:%S)] >>> Gen $kind ($i/$count)..."
    opencode run --dangerously-skip-permissions "Đọc $SKILL/SKILL.md và $SKILL/kinds/${kind}.md. Gen 1 câu hỏi dạng $kind. Lưu trực tiếp CSV vào $OUTPUT/$level/${kind}.csv (append nếu đã tồn tại)"
    echo "[$(date +%H:%M:%S)] <<< Done $kind ($i/$count)"
  done
}

merge_all() {
  echo ">>> Merging..."
  python3 -c "
import pandas as pd, glob
dfs = [pd.read_csv(f, dtype=str) for f in sorted(glob.glob('$OUTPUT/level_*/*.csv')) if pd.read_csv(f, dtype=str).shape[0] > 0]
if dfs:
    pd.concat(dfs, ignore_index=True).to_csv('$OUTPUT/all_questions.csv', index=False)
    print(f'Merged {len(dfs)} files')
"
}

# Nếu có tham số kind → gen 1 dạng cụ thể
if [ -n "$1" ] && [[ "$1" != "--"* ]]; then
  KIND="$1"
  COUNT="${2:-1}"
  if [[ "$KIND" == 12* ]]; then LEVEL="level_1"; else LEVEL="level_2"; fi
  if [ "$PARALLEL" -gt 1 ] && [ "$COUNT" -gt 1 ]; then
    # Song song: chia count ra cho N workers
    for i in $(seq 1 $COUNT); do
      gen_kind "$KIND" 1 "$LEVEL" &
      # Giới hạn số job song song
      if (( $(jobs -r | wc -l) >= PARALLEL )); then wait -n; fi
    done
    wait
  else
    gen_kind "$KIND" "$COUNT" "$LEVEL"
  fi
  merge_all
  exit 0
fi

# Gen tất cả
KINDS_L1="120001 120002_1 120002_2 120002_3 120002_4 120003_1 120003_2 120004_1 120004_2 120005_(1) 120005_(2) 120006 120007_1 120007_2 120007_3"
KINDS_L2="220001_a 220001_b 220001_c 220002_a 220002_b_1 220002_b_2 220002_b_3 220002_c 220003_a_1 220003_a_2 220003_b 220004 220005_1_(1) 220005_1_(2) 220005_2 220006 220007 220008_1_(1) 220008_1_(2) 220008_1_(3) 220008_2"

mkdir -p "$OUTPUT/level_1" "$OUTPUT/level_2"

if [ "$PARALLEL" -gt 1 ]; then
  echo ">>> Running $PARALLEL sessions in parallel..."
  for kind in $KINDS_L1; do
    gen_kind "$kind" 1 "level_1" &
    if (( $(jobs -r | wc -l) >= PARALLEL )); then wait -n; fi
  done
  for kind in $KINDS_L2; do
    gen_kind "$kind" 1 "level_2" &
    if (( $(jobs -r | wc -l) >= PARALLEL )); then wait -n; fi
  done
  wait
else
  for kind in $KINDS_L1; do gen_kind "$kind" 1 "level_1"; done
  for kind in $KINDS_L2; do gen_kind "$kind" 1 "level_2"; done
fi

merge_all
echo ">>> DONE!"
