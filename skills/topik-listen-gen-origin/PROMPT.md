Đọc `skills/topik-listen-gen-origin/SKILL.md` để hiểu format và cách gen câu hỏi. Sau đó gen từng dạng theo danh sách bên dưới — mỗi dạng đọc kind file tương ứng + samples.json trước khi gen.

## Số lượng gen theo dạng

### TOPIK I
- 110001: 1 bài
- 110002: 1 bài
- 110003: 1 bài
- 110004: 1 bài
- 110005: 1 bài
- 110006: 1 bài
- 110007: 1 bài
- 110008_1: 1 bài
- 110008_2: 1 bài
- 110008_3: 1 bài

### TOPIK II
- 210001_1: 1 bài
- 210001_2: 1 bài
- 210002: 1 bài
- 210003: 1 bài
- 210004_(1): 1 bài
- 210004_(2): 1 bài
- 210004_(3): 1 bài
- 210004_(4): 1 bài
- 210005_(1): 1 bài
- 210005_(2): 1 bài
- 210006_(1): 1 bài
- 210006_(2): 1 bài
- 210006_(3): 1 bài
- 210006_(4): 1 bài
- 210006_(5): 1 bài
- 210006_(6): 1 bài
- 210006_(7): 1 bài
- 210006_(8): 1 bài
- 210007_(1): 1 bài
- 210007_(2): 1 bài
- 210007_(3): 1 bài
- 210007_(4): 1 bài
- 210007_(5): 1 bài
- 210007_(6): 1 bài
- 210007_(7): 1 bài

## Luồng lưu file (BẮT BUỘC)

Sau khi gen + QC xong từng dạng:
1. Lưu CSV riêng: `output/listen-origin/level_{1|2}/{kind}.csv`
2. **Sau khi gen XONG TẤT CẢ các dạng** → merge tất cả CSV thành `output/listen-origin/all_questions.csv`:
   ```python
   import pandas as pd, glob
   dfs = [pd.read_csv(f) for f in sorted(glob.glob('output/listen-origin/level_*/*.csv'))]
   pd.concat(dfs, ignore_index=True).to_csv('output/listen-origin/all_questions.csv', index=False)
   ```
3. Xóa gen_temp*.json

## Lưu ý quan trọng
1. Explain KHÔNG chứa mã trap — giải thích bằng ngôn ngữ dễ hiểu cho người học
2. g_text_audio_vi dùng "Người nam:"/"Người nữ:", g_text_audio_en dùng "Man:"/"Woman:"
3. q_correct PHẢI phân bố đều 1-4 cho TẤT CẢ levels (TOPIK I, II). KHÔNG fix cứng q_correct = 1 cho bất kỳ level nào.
4. Sau khi gen xong PHẢI chạy QC (Bước 4 trong SKILL.md) trước khi lưu
5. Lưu JSON tạm vào output/listen-origin/, KHÔNG lưu trong skills/
