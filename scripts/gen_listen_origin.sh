#!/bin/bash
# Gen câu hỏi Listen Origin
# Usage:
#   bash scripts/gen_listen_origin.sh                        # Tuần tự, 1 bài/dạng
#   bash scripts/gen_listen_origin.sh 110001 3               # Gen 3 bài dạng 110001
#   bash scripts/gen_listen_origin.sh --parallel 3           # Song song 3 sessions
#   bash scripts/gen_listen_origin.sh --parallel 3 110001 5  # Song song 3, dạng 110001, 5 bài
#   --model <id>                                 # Đổi model (mặc định opencode-go/deepseek-v4-flash [gói Go] | Zen: opencode/deepseek-v4-flash | free: opencode/deepseek-v4-flash-free)

SKILL="skills/topik-listen-gen-origin"
OUTPUT="output/listen-origin"
PARALLEL=1
MODEL="opencode-go/deepseek-v4-flash"   # Mặc định: DeepSeek V4 Flash qua gói OpenCode Go. Đổi qua --model (Zen trả phí: opencode/deepseek-v4-flash | free: opencode/deepseek-v4-flash-free)

# Parse cờ --parallel / --model (đặt TRƯỚC tham số kind, theo thứ tự bất kỳ)
while [[ "$1" == "--"* ]]; do
  case "$1" in
    --parallel) PARALLEL="$2"; shift 2 ;;
    --model)    MODEL="$2";    shift 2 ;;
    *) echo "Cờ không hợp lệ: $1"; exit 1 ;;
  esac
done
echo ">>> Model: $MODEL"

gen_kind() {
  local kind="$1" count="$2" level="$3" suffix="${4:-}"
  mkdir -p "$OUTPUT/$level"
  local target="$OUTPUT/$level/${kind}${suffix}.csv"
  for i in $(seq 1 $count); do
    # Random q_correct 1-4 cho mỗi câu (tránh model mặc định = 1)
    local rc1=$(( (RANDOM % 4) + 1 ))
    local rc2=$(( (RANDOM % 4) + 1 ))
    echo "[$(date +%H:%M:%S)] >>> Gen $kind ($i/$count)${suffix:+ [session$suffix]} [q_correct=$rc1/$rc2]..."
    local _prompt="Đọc $SKILL/SKILL.md và $SKILL/kinds/${kind}.md. Gen 1 câu hỏi dạng $kind. Tuân thủ MỌI quy tắc trong kind file — ĐẶC BIỆT đọc kĩ phần ĐỌC TRƯỚC KHI GEN ở đầu file kind (format q_image_desc, format explain, CHỈ 1 đáp án đúng). BẮT BUỘC: q_correct = $rc1 (đặt đáp án đúng ở vị trí $rc1). Nếu dạng có 2 câu hỏi con: content[0].q_correct=$rc1, content[1].q_correct=$rc2. XÂY DỰNG đáp án sao cho đáp án đúng NẰM Ở VỊ TRÍ $rc1. Lưu CSV vào $target (append nếu đã tồn tại). CHỈ đọc/ghi file $target."
    local _attempt=1
    while true; do
      _out=$(opencode run --model "$MODEL" --dangerously-skip-permissions "$_prompt" 2>&1)
      printf '%s\n' "$_out"
      if printf '%s' "$_out" | grep -qi "database is locked" && [ "$_attempt" -lt 4 ]; then
        echo "   [retry $_attempt] DB locked → thử lại sau $((_attempt*2))s..."; sleep $((_attempt*2)); _attempt=$((_attempt+1)); continue
      fi
      break
    done
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
    if "id" in merged.columns: merged = merged.drop_duplicates(subset="id", keep="first")
    merged.to_csv(main, index=False)
    print(f'Merged {len(files)} temp files into ${kind}.csv ({len(merged)} rows)')
# Xóa file tạm
for f in files: os.remove(f)
"
}

fix_periods() {
  echo ">>> Fixing periods (dấu chấm cuối đáp án + explain)..."
  python3 "$SKILL/scripts/save_listen.py" --fix-periods -o "$OUTPUT"
}

merge_all() {
  echo ">>> Merging..."
  python3 -c "
import pandas as pd, glob
dfs = [pd.read_csv(f, dtype=str) for f in sorted(glob.glob('$OUTPUT/level_*/*.csv')) if pd.read_csv(f, dtype=str).shape[0] > 0]
if dfs:
    merged = pd.concat(dfs, ignore_index=True)
    if "id" in merged.columns: merged = merged.drop_duplicates(subset="id", keep="first")
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

fix_periods
merge_all
echo ">>> DONE!"
