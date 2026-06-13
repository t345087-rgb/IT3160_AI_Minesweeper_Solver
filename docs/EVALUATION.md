# Kế hoạch đánh giá hệ thống

Tài liệu này mô tả cách đánh giá hiệu quả của hệ thống AI Minesweeper Solver.

## 1. Mục tiêu đánh giá

Mục tiêu là đo lường khả năng giải bàn Minesweeper của solver trên nhiều ván
chơi và nhiều độ khó. Do Minesweeper có yếu tố không chắc chắn, một ván đơn lẻ
không đủ để kết luận solver hoạt động tốt hay không.

Phần đánh giá tập trung vào:

- Độ chính xác: số ván thắng và win rate.
- Mức độ phải phỏng đoán: average guesses.
- Hiệu quả thực thi: average runtime trên mỗi ván.

## 2. Các chỉ số đánh giá

| Chỉ số          | Ý nghĩa                                    |
| --------------- | ------------------------------------------ |
| Games           | Tổng số ván được dùng để đánh giá          |
| Wins            | Số ván solver thắng                        |
| Losses          | Số ván solver thua                         |
| Win rate        | Tỉ lệ thắng của solver                     |
| Average guesses | Số lần đoán trung bình trong mỗi ván       |
| Average steps   | Số bước trung bình trong mỗi ván           |
| Average flags   | Số ô được cắm cờ trung bình trong mỗi ván  |
| Average runtime | Thời gian chạy trung bình để xử lý một ván |

## 3. Kết quả evaluation hiện có

| Difficulty   | Games | Win rate | Average guesses | Average runtime |
| ------------ | ----: | -------: | --------------: | --------------: |
| Beginner     |   100 |      96% |            1.17 |               - |
| Intermediate |   100 |      75% |            1.73 | khoảng 0.14 giây/game |
| Expert       |    10 |      30% |            3.60 | khoảng 0.275 giây/game |

Kết quả cho thấy độ khó cao hơn đi kèm win rate thấp hơn và số lần đoán trung
bình cao hơn trong các lần chạy đã đo. Tuy nhiên, tập Expert chỉ gồm 10 ván,
nhỏ hơn nhiều so với 100 ván của Beginner và Intermediate. Vì vậy, win rate
30% của Expert có độ bất định cao và chưa đủ để kết luận chắc chắn về hiệu năng
thực tế của solver ở độ khó này.

Các số liệu runtime cũng phụ thuộc vào phần cứng, phiên bản Python, tải hệ thống
và cấu hình chạy. Chúng nên được xem là số liệu tham khảo của lần evaluation
hiện có, không phải cam kết hiệu năng trên mọi môi trường.

## 4. Cách chạy đánh giá

Chạy lệnh sau từ thư mục gốc của project:

```bash
python -m minesweeper.cli --evaluate --games 100
```

Có thể chọn preset độ khó:

```bash
python -m minesweeper.cli --evaluate --difficulty beginner --games 100
python -m minesweeper.cli --evaluate --difficulty intermediate --games 100 --max-steps 500
python -m minesweeper.cli --evaluate --difficulty expert --games 10 --max-steps 1000
```

Số lượng ván càng lớn thì ước lượng win rate và average guesses càng ổn định.
Khi so sánh các phiên bản solver, cần giữ nguyên preset, số ván, seed và giới
hạn bước.

## 5. Kiểm thử tự động

Chạy toàn bộ test:

```bash
python -m pytest
```

Kết quả kiểm thử hiện tại:

```text
35 passed
```

Các test bao phủ board engine, evaluation, deterministic inference, subset
inference, frontier component discovery, component-wise probability
enumeration, fallback, backtracking và pruning.

## 6. Diễn giải kết quả

Win rate cao hơn cho thấy solver thắng nhiều ván hơn trong cùng điều kiện đánh
giá. Average guesses thấp hơn cho thấy solver thường cần ít quyết định không
chắc chắn hơn. Average runtime thấp hơn cho thấy thời gian xử lý mỗi ván ngắn
hơn, nhưng chỉ nên so sánh trực tiếp khi môi trường chạy tương đương.

Các kết quả quan sát được không tự chứng minh quan hệ nhân quả giữa một thay đổi
thuật toán và mức cải thiện. Muốn so sánh đáng tin cậy, các phiên bản cần được
chạy trên cùng tập seed và với kích thước mẫu đủ lớn.
