Đọc `skills/topik-read-gen-eps/SKILL.md` để hiểu format và cách gen câu hỏi. Sau đó gen từng dạng theo danh sách bên dưới — mỗi dạng đọc kind file tương ứng + samples.json trước khi gen.

## Số lượng gen theo dạng

- 320001: 1 bài
- 320002: 1 bài
- 320003: 1 bài
- 320004: 1 bài
- 320005: 1 bài
- 3420002: 1 bài
- 3420003: 1 bài
- 3420006: 1 bài
- 3420007: 1 bài
- 3420008: 1 bài

## Luồng lưu file (BẮT BUỘC)

Sau khi gen + QC xong từng dạng:
1. Lưu CSV riêng: `output/read-eps/level_{1|2}/{kind}.csv`
2. **Sau khi gen XONG TẤT CẢ các dạng** → merge thành `output/read-eps/all_questions.csv`:
   ```python
   import pandas as pd, glob
   dfs = [pd.read_csv(f) for f in sorted(glob.glob('output/read-eps/level_*/*.csv'))]
   pd.concat(dfs, ignore_index=True).to_csv('output/read-eps/all_questions.csv', index=False)
   ```
3. Xóa gen_temp*.json

## Lưu ý quan trọng
1. Explain KHÔNG chứa mã trap — giải thích bằng ngôn ngữ dễ hiểu cho người học
2. Câu ghép: explain phải dịch câu hỏi phụ
3. Sau khi gen xong PHẢI chạy QC trước khi lưu
4. Lưu JSON tạm vào output/read-eps/, KHÔNG lưu trong skills/
