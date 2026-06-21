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
  local kind="$1" count="$2" level="$3" suffix="${4:-}"
  mkdir -p "$OUTPUT/$level"
  local target="$OUTPUT/$level/${kind}${suffix}.csv"
  for i in $(seq 1 $count); do
    # Random q_correct 1-4 cho mỗi câu (tránh model mặc định = 1)
    local rc1=$(( (RANDOM % 4) + 1 ))
    local rc2=$(( (RANDOM % 4) + 1 ))
    echo "[$(date +%H:%M:%S)] >>> Gen $kind ($i/$count)${suffix:+ [session$suffix]} [q_correct=$rc1/$rc2]..."
    opencode run --dangerously-skip-permissions "Đọc $SKILL/SKILL.md và $SKILL/kinds/${kind}.md. Gen 1 câu hỏi dạng $kind. Tuân thủ MỌI quy tắc trong kind file — ĐẶC BIỆT đọc kĩ phần ĐỌC TRƯỚC KHI GEN ở đầu file kind (format q_image_desc, format explain, CHỈ 1 đáp án đúng). BẮT BUỘC: q_correct = $rc1 (đặt đáp án đúng ở vị trí $rc1). Nếu dạng có 2 câu hỏi con: content[0].q_correct=$rc1, content[1].q_correct=$rc2. XÂY DỰNG đáp án sao cho đáp án đúng NẰM Ở VỊ TRÍ $rc1. Lưu CSV vào $target (append nếu đã tồn tại). CHỈ đọc/ghi file $target."
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

fix_periods() {
  echo ">>> Fixing periods (dấu chấm cuối đáp án + explain)..."
  python3 "$SKILL/scripts/save_read.py" --fix-periods -o "$OUTPUT"
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
  if [[ "$KIND" == 12* ]]; then LEVEL="level_1"; else LEVEL="level_2"; fi
  if [ "$PARALLEL" -gt 1 ] && [ "$COUNT" -gt 1 ]; then
    # Chạy theo batch, mỗi session ghi file riêng tránh race condition
    local_idx=0
    for ((i=0; i<COUNT; i+=PARALLEL)); do
      batch_end=$((i+PARALLEL < COUNT ? i+PARALLEL : COUNT))
      batch_size=$((batch_end - i))
      echo "[$(date +%H:%M:%S)] >>> Batch $((i/PARALLEL+1)) ($batch_size sessions)..."
      for ((j=0; j<batch_size; j++)); do
        local_idx=$((local_idx + 1))
        gen_kind "$KIND" 1 "$LEVEL" "_p${local_idx}" &
      done
      wait
      echo "[$(date +%H:%M:%S)] <<< Batch done"
    done
    # Merge file tạm vào file chính
    merge_parallel_files "$KIND" "$LEVEL"
  else
    gen_kind "$KIND" "$COUNT" "$LEVEL"
  fi
  fix_periods
  merge_all
  exit 0
fi

# Gen tất cả
KINDS_L1="120001 120002_1 120002_2 120002_3 120002_4 120003_1 120003_2 120004_1 120004_2 120005_(1) 120005_(2) 120006 120007_1 120007_2 120007_3"
KINDS_L2="220001_a 220001_b 220001_c 220002_a 220002_b_1 220002_b_2 220002_b_3 220002_c 220003_a_1 220003_a_2 220003_b 220004 220005_1_(1) 220005_1_(2) 220005_2 220006 220007 220008_1_(1) 220008_1_(2) 220008_1_(3) 220008_2"

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

fix_periods
merge_all
echo ">>> DONE!"
