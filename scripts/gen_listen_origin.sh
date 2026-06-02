#!/bin/bash
# Gen câu hỏi Listen Origin
# Usage:
#   bash scripts/gen_listen_origin.sh                        # Tuần tự, 1 bài/dạng
#   bash scripts/gen_listen_origin.sh 110001 3               # Gen 3 bài dạng 110001
#   bash scripts/gen_listen_origin.sh --parallel 3           # Song song 3 sessions
#   bash scripts/gen_listen_origin.sh --parallel 3 110001 5  # Song song 3, dạng 110001, 5 bài

SKILL="skills/topik-listen-gen-origin"
OUTPUT="output/listen-origin"
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
    opencode run --dangerously-skip-permissions "Đọc $SKILL/SKILL.md và $SKILL/kinds/${kind}.md. Gen 1 câu hỏi dạng $kind. Lưu CSV vào $OUTPUT/$level/${kind}.csv (append nếu đã tồn tại)"
    echo "[$(date +%H:%M:%S)] <<< Done $kind ($i/$count)"
  done
}

merge_all() {
  echo ">>> Merging..."
  python3 -c "
import pandas as pd, glob
dfs = [pd.read_csv(f, dtype=str) for f in sorted(glob.glob('$OUTPUT/level_*/*.csv')) if pd.read_csv(f, dtype=str).shape[0] > 0]
if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    # Reorder: example_ and created_at at end
    end_cols = [c for c in merged.columns if c.startswith('example_') or c == 'created_at']
    other_cols = [c for c in merged.columns if c not in end_cols]
    merged = merged[other_cols + end_cols]
    merged.to_csv('$OUTPUT/all_questions.csv', index=False)
    print(f'Merged {len(dfs)} files')
"
}

# Nếu có tham số kind → gen 1 dạng cụ thể
if [ -n "$1" ] && [[ "$1" != "--"* ]]; then
  KIND="$1"
  COUNT="${2:-1}"
  if [[ "$KIND" == 11* ]]; then LEVEL="level_1"; else LEVEL="level_2"; fi
  if [ "$PARALLEL" -gt 1 ] && [ "$COUNT" -gt 1 ]; then
    # Chạy theo batch, mỗi batch tối đa PARALLEL sessions, đợi hết mới chạy tiếp
    for ((i=0; i<COUNT; i+=PARALLEL)); do
      batch_end=$((i+PARALLEL < COUNT ? i+PARALLEL : COUNT))
      batch_size=$((batch_end - i))
      echo "[$(date +%H:%M:%S)] >>> Batch $((i/PARALLEL+1)) ($batch_size sessions)..."
      for ((j=0; j<batch_size; j++)); do
        gen_kind "$KIND" 1 "$LEVEL" &
      done
      wait
      echo "[$(date +%H:%M:%S)] <<< Batch done"
    done
  else
    gen_kind "$KIND" "$COUNT" "$LEVEL"
  fi
  merge_all
  exit 0
fi

# Gen tất cả
KINDS_L1="110001 110002 110003 110004 110005 110006 110007 110008_1 110008_2 110008_3"
KINDS_L2="210001_1 210001_2 210002 210003 210004_(1) 210004_(2) 210004_(3) 210004_(4) 210005_(1) 210005_(2) 210006_(1) 210006_(2) 210006_(3) 210006_(4) 210006_(5) 210006_(6) 210006_(7) 210006_(8) 210007_(1) 210007_(2) 210007_(3) 210007_(4) 210007_(5) 210007_(6) 210007_(7)"

mkdir -p "$OUTPUT/level_1" "$OUTPUT/level_2"

if [ "$PARALLEL" -gt 1 ]; then
  echo ">>> Running in batches of $PARALLEL sessions (đợi hết batch mới chạy tiếp)..."
  # Level 1
  kinds_arr=($KINDS_L1)
  total=${#kinds_arr[@]}
  for ((i=0; i<total; i+=PARALLEL)); do
    batch=("${kinds_arr[@]:i:PARALLEL}")
    echo "[$(date +%H:%M:%S)] >>> Batch L1: ${batch[*]}"
    for kind in "${batch[@]}"; do
      gen_kind "$kind" 1 "level_1" &
    done
    wait
    echo "[$(date +%H:%M:%S)] <<< Batch done"
  done
  # Level 2
  kinds_arr=($KINDS_L2)
  total=${#kinds_arr[@]}
  for ((i=0; i<total; i+=PARALLEL)); do
    batch=("${kinds_arr[@]:i:PARALLEL}")
    echo "[$(date +%H:%M:%S)] >>> Batch L2: ${batch[*]}"
    for kind in "${batch[@]}"; do
      gen_kind "$kind" 1 "level_2" &
    done
    wait
    echo "[$(date +%H:%M:%S)] <<< Batch done"
  done
else
  for kind in $KINDS_L1; do gen_kind "$kind" 1 "level_1"; done
  for kind in $KINDS_L2; do gen_kind "$kind" 1 "level_2"; done
fi

merge_all
echo ">>> DONE!"
