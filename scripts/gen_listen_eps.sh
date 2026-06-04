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
  local kind="$1" count="$2" level="$3" suffix="${4:-}"
  mkdir -p "$OUTPUT/$level"
  local target="$OUTPUT/$level/${kind}${suffix}.csv"
  for i in $(seq 1 $count); do
    echo "[$(date +%H:%M:%S)] >>> Gen $kind ($i/$count)${suffix:+ [session$suffix]}..."
    opencode run --dangerously-skip-permissions "Đọc $SKILL/SKILL.md và $SKILL/kinds/${kind}.md. Gen 1 câu hỏi dạng $kind. Lưu CSV vào $target (append nếu đã tồn tại). QUAN TRỌNG: CHỈ đọc/ghi file $target, KHÔNG đọc/ghi/xóa bất kỳ file CSV nào khác."
    echo "[$(date +%H:%M:%S)] <<< Done $kind ($i/$count)${suffix:+ [session$suffix]}"
  done
}

# Merge các file tạm _p*.csv vào file chính {kind}.csv
merge_parallel_files() {
  local kind="$1" level="$2"
  local main="$OUTPUT/$level/${kind}.csv"
  local temps=($OUTPUT/$level/${kind}_p*.csv)
  if [ ${#temps[@]} -eq 0 ] || [ ! -f "${temps[0]}" ]; then return; fi

  python3 -c "
import pandas as pd, glob
files = sorted(glob.glob('$OUTPUT/$level/${kind}_p*.csv'))
if not files: exit()
dfs = []
# Giữ lại file chính nếu có
main = '$main'
import os
if os.path.exists(main):
    dfs.append(pd.read_csv(main, dtype=str))
for f in files:
    try: dfs.append(pd.read_csv(f, dtype=str))
    except: pass
if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(main, index=False)
    print(f'Merged {len(files)} temp files into ${kind}.csv ({len(merged)} rows)')
# Xóa file tạm
for f in files: os.remove(f)
"
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
  if [ "$PARALLEL" -gt 1 ] && [ "$COUNT" -gt 1 ]; then
    # Chạy theo batch, mỗi session ghi file riêng tránh race condition
    local_idx=0
    for ((i=0; i<COUNT; i+=PARALLEL)); do
      batch_end=$((i+PARALLEL < COUNT ? i+PARALLEL : COUNT))
      batch_size=$((batch_end - i))
      echo "[$(date +%H:%M:%S)] >>> Batch $((i/PARALLEL+1)) ($batch_size sessions)..."
      for ((j=0; j<batch_size; j++)); do
        local_idx=$((local_idx + 1))
        gen_kind "$KIND" 1 "level_3" "_p${local_idx}" &
      done
      wait
      echo "[$(date +%H:%M:%S)] <<< Batch done"
    done
    # Merge file tạm vào file chính
    merge_parallel_files "$KIND" "level_3"
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
  echo ">>> Running in batches of $PARALLEL sessions (đợi hết batch mới chạy tiếp)..."
  kinds_arr=($KINDS)
  total=${#kinds_arr[@]}
  for ((i=0; i<total; i+=PARALLEL)); do
    batch=("${kinds_arr[@]:i:PARALLEL}")
    echo "[$(date +%H:%M:%S)] >>> Batch: ${batch[*]}"
    for kind in "${batch[@]}"; do
      gen_kind "$kind" 1 "level_3" &
    done
    wait
    echo "[$(date +%H:%M:%S)] <<< Batch done"
  done
else
  for kind in $KINDS; do gen_kind "$kind" 1 "level_3"; done
fi

merge_all
echo ">>> DONE!"
