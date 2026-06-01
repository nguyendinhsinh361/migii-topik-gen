Đọc `skills/topik-write-gen-origin/SKILL.md` để hiểu format và cách gen câu hỏi. Sau đó gen từng dạng theo danh sách bên dưới — mỗi dạng đọc kind file tương ứng + samples.json trước khi gen.

## Số lượng gen theo dạng

- 230001_1: 1 bài
- 230001_2: 1 bài
- 230002: 1 bài
- 230003: 1 bài

## Luồng lưu file (BẮT BUỘC)

Sau khi gen + QC xong từng dạng:
1. Lưu CSV riêng: `output/write-origin/level_2/{kind}.csv`
2. **Sau khi gen XONG TẤT CẢ các dạng** → merge thành `output/write-origin/all_questions.csv`:
   ```python
   import pandas as pd, glob
   dfs = [pd.read_csv(f) for f in sorted(glob.glob('output/write-origin/level_*/*.csv'))]
   pd.concat(dfs, ignore_index=True).to_csv('output/write-origin/all_questions.csv', index=False)
   ```
3. Xóa gen_temp*.json

## Lưu ý quan trọng
1. Explain KHÔNG chứa mã trap — giải thích bằng ngôn ngữ dễ hiểu cho người học
2. explain_vi và explain_en PHẢI cùng cấu trúc, cùng mức chi tiết
3. 230002/230003 PHẢI kèm 5 bài viết mẫu (examples)
4. 230001_2 KHÔNG cần ảnh
5. 230003 g_text không lẫn tiếng Trung
6. Sau khi gen xong PHẢI chạy QC trước khi lưu
7. Lưu JSON tạm vào output/write-origin/, KHÔNG lưu trong skills/
