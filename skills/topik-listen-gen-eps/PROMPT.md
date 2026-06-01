Đọc `skills/topik-listen-gen-eps/SKILL.md` để hiểu format và cách gen câu hỏi. Sau đó gen từng dạng theo danh sách bên dưới — mỗi dạng đọc kind file tương ứng + samples.json trước khi gen.

## Số lượng gen theo dạng

- 310001: 1 bài
- 310002: 1 bài
- 310003: 1 bài
- 310004: 1 bài
- 310005: 1 bài
- 310006: 1 bài
- 3410002: 1 bài
- 3410005: 1 bài

## Luồng lưu file (BẮT BUỘC)

Sau khi gen + QC xong từng dạng:
1. Lưu CSV riêng: `output/listen-eps/level_{1|2}/{kind}.csv`
2. **Sau khi gen XONG TẤT CẢ các dạng** → merge thành `output/listen-eps/all_questions.csv`:
   ```python
   import pandas as pd, glob
   dfs = [pd.read_csv(f) for f in sorted(glob.glob('output/listen-eps/level_*/*.csv'))]
   pd.concat(dfs, ignore_index=True).to_csv('output/listen-eps/all_questions.csv', index=False)
   ```
3. Xóa gen_temp*.json

## Lưu ý quan trọng
1. Explain KHÔNG chứa mã trap — giải thích bằng ngôn ngữ dễ hiểu cho người học
2. g_text_audio_vi dùng "Người nam:"/"Người nữ:", g_text_audio_en dùng "Man:"/"Woman:"
3. Sau khi gen xong PHẢI chạy QC trước khi lưu
4. Lưu JSON tạm vào output/listen-eps/, KHÔNG lưu trong skills/
