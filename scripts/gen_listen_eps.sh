#!/bin/bash
# Gen câu hỏi Listen EPS
# Usage:
#   bash scripts/gen_listen_eps.sh                        # Tuần tự, 1 bài/dạng
#   bash scripts/gen_listen_eps.sh 310001 3               # Gen 3 bài dạng 310001
#   bash scripts/gen_listen_eps.sh --parallel 3           # Song song 3 sessions
#   bash scripts/gen_listen_eps.sh --parallel 3 310001 5  # Song song 3, dạng 310001, 5 bài

SKILL="skills/topik-listen-gen-eps"
OUTPUT="output/listen-eps"
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
  if [ "$PARALLEL" -gt 1 ] && [ "$COUNT" -gt 1 ]; then
    # Song song: chia count ra cho N workers
    for i in $(seq 1 $COUNT); do
      gen_kind "$KIND" 1 "level_3" &
      # Giới hạn số job song song
      if (( $(jobs -r | wc -l) >= PARALLEL )); then wait -n; fi
    done
    wait
  else
    gen_kind "$KIND" "$COUNT" "level_3"
  fi
  merge_all
  exit 0
fi

# Gen tất cả
KINDS="310001 310002 310003 310004 310005 310006 3410002 3410005"

mkdir -p "$OUTPUT/level_3"

if [ "$PARALLEL" -gt 1 ]; then
  echo ">>> Running $PARALLEL sessions in parallel..."
  for kind in $KINDS; do
    gen_kind "$kind" 1 "level_3" &
    if (( $(jobs -r | wc -l) >= PARALLEL )); then wait -n; fi
  done
  wait
else
  for kind in $KINDS; do gen_kind "$kind" 1 "level_3"; done
fi

merge_all
echo ">>> DONE!"
