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

## Lưu ý quan trọng
1. Explain KHÔNG chứa mã trap — giải thích bằng ngôn ngữ dễ hiểu cho người học
2. g_text_audio_vi dùng "Người nam:"/"Người nữ:", g_text_audio_en dùng "Man:"/"Woman:"
3. TOPIK I (110xxx) q_correct luôn = 1
4. Sau khi gen xong PHẢI chạy QC (Bước 4 trong SKILL.md) trước khi lưu
5. Lưu JSON tạm vào output/listen-origin/, KHÔNG lưu trong skills/
6. Sau khi lưu CSV xong, xóa gen_temp*.json
