Đọc `skills/topik-read-gen-origin/SKILL.md` để hiểu format và cách gen câu hỏi. Sau đó gen từng dạng theo danh sách bên dưới — mỗi dạng đọc kind file tương ứng + samples.json trước khi gen.

## Số lượng gen theo dạng

### TOPIK I
- 120001: 1 bài
- 120002_1: 1 bài
- 120002_2: 1 bài
- 120002_3: 1 bài
- 120002_4: 1 bài
- 120003_1: 1 bài
- 120003_2: 1 bài
- 120004_1: 1 bài
- 120004_2: 1 bài
- 120005_(1): 1 bài
- 120005_(2): 1 bài
- 120006: 1 bài
- 120007_1: 1 bài
- 120007_2: 1 bài
- 120007_3: 1 bài

### TOPIK II
- 220001_a: 1 bài
- 220001_b: 1 bài
- 220001_c: 1 bài
- 220002_a: 1 bài
- 220002_b_1: 1 bài
- 220002_b_2: 1 bài
- 220002_b_3: 1 bài
- 220002_c: 1 bài
- 220003_a_1: 1 bài
- 220003_a_2: 1 bài
- 220003_b: 1 bài
- 220004: 1 bài
- 220005_1_(1): 1 bài
- 220005_1_(2): 1 bài
- 220005_2: 1 bài
- 220006: 1 bài
- 220007: 1 bài
- 220008_1_(1): 1 bài
- 220008_1_(2): 1 bài
- 220008_1_(3): 1 bài
- 220008_2: 1 bài

## Luồng lưu file (BẮT BUỘC)

Sau khi gen + QC xong từng dạng:
1. Lưu CSV riêng: `output/read-origin/level_{1|2}/{kind}.csv`
2. **Sau khi gen XONG TẤT CẢ các dạng** → merge thành `output/read-origin/all_questions.csv`:
   ```python
   import pandas as pd, glob
   dfs = [pd.read_csv(f) for f in sorted(glob.glob('output/read-origin/level_*/*.csv'))]
   pd.concat(dfs, ignore_index=True).to_csv('output/read-origin/all_questions.csv', index=False)
   ```
3. Xóa gen_temp*.json

## Lưu ý quan trọng
1. Explain KHÔNG chứa mã trap — giải thích bằng ngôn ngữ dễ hiểu cho người học
2. Câu ghép (count_question >= 2): explain phải dịch câu hỏi phụ, KHÔNG để tiếng Hàn
3. Câu có ảnh: explain chỉ dịch text hiển thị trên ảnh, KHÔNG dịch nguyên văn q_image_desc
4. Sau khi gen xong PHẢI chạy QC trước khi lưu
5. Lưu JSON tạm vào output/read-origin/, KHÔNG lưu trong skills/
