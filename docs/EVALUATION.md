# Kế hoạch đánh giá hệ thống

Tài liệu này mô tả cách đánh giá AI Minesweeper Solver trên nhiều ván và nhiều
độ khó. Một lần chạy chỉ là mẫu thực nghiệm; kết quả có thể thay đổi theo seed,
phiên bản Python, phần cứng và tải hệ thống.

## 1. Các chỉ số đánh giá

| Chỉ số          | Ý nghĩa                                    |
| --------------- | ------------------------------------------ |
| Games           | Tổng số ván được dùng để đánh giá          |
| Wins            | Số ván solver thắng                        |
| Losses          | Số ván solver thua                         |
| Win rate        | Tỉ lệ thắng của solver                     |
| Average steps   | Số bước trung bình trong mỗi ván           |
| Average flags   | Số ô được cắm cờ trung bình trong mỗi ván  |
| Average guesses | Số lần đoán trung bình trong mỗi ván       |
| Average runtime | Thời gian inference trung bình mỗi ván     |

Một hành động reveal được tính là guess khi xác suất của nó không bằng `0.0`.
Runtime chỉ đo thời gian `choose_next_action`, không phải toàn bộ thời gian tạo
board, cập nhật board hoặc in output.

## 2. Kết quả benchmark 100 games

Các lệnh được chạy trên Python 3.12.10 với seed mặc định `0..99`:

```bash
python -m minesweeper.cli --evaluate --difficulty beginner --games 100
python -m minesweeper.cli --evaluate --difficulty intermediate --games 100 --max-steps 500
python -m minesweeper.cli --evaluate --difficulty expert --games 100 --max-steps 1000
```

| Difficulty   | Games | Wins | Losses | Win rate | Avg. steps | Avg. flags | Avg. guesses | Avg. runtime |
| ------------ | ----: | ---: | -----: | -------: | ---------: | ---------: | -----------: | -----------: |
| Beginner     |   100 |   98 |      2 |   98.00% |      24.40 |       9.82 |         1.14 |   0.005918 s |
| Intermediate |   100 |   86 |     14 |   86.00% |     112.17 |      38.00 |         1.55 |   0.072679 s |
| Expert       |   100 |   32 |     68 |   32.00% |     231.32 |      76.27 |         3.65 |   0.243818 s |

Trong lần chạy này, độ khó cao hơn có win rate thấp hơn, đồng thời average
steps, average guesses và runtime cao hơn. Đây là kết quả của đúng 100 seed đã
chạy, không phải cam kết rằng mọi lần chạy hoặc mọi tập seed sẽ cho cùng số
liệu.

## 3. Cách chạy đánh giá

Chạy từ thư mục gốc sau khi cài project:

```bash
python -m pip install -e .
python -m minesweeper.cli --evaluate --difficulty beginner --games 100
```

Có thể chọn các preset hoặc cấu hình custom:

```bash
python -m minesweeper.cli --evaluate --difficulty intermediate --games 100 --max-steps 500
python -m minesweeper.cli --evaluate --difficulty expert --games 100 --max-steps 1000
python -m minesweeper.cli --evaluate --difficulty custom --rows 9 --cols 9 --mines 10 --games 100
```

Khi so sánh các phiên bản solver, cần giữ nguyên preset, số ván, tập seed và
`max-steps`.

## 4. Kiểm thử tự động

Chạy toàn bộ test:

```bash
python -m pytest
```

Kết quả hiện tại:

```text
57 passed
```

Test suite gồm 11 board tests, 3 evaluation tests và 43 solver tests. Các test
solver bao phủ deterministic/subset inference, frontier components,
component-wise CSP, backtracking/pruning, component model counts, global
mine-count weighting, fallback, certain-probability actions và center opening.

## 5. Diễn giải kết quả

Win rate đo tỉ lệ ván thắng trong mẫu. Average guesses thấp hơn cho thấy solver
ít phải reveal khi chưa chắc chắn hơn. Average steps và flags mô tả lượng hành
động của solver, còn average runtime phản ánh chi phí inference trong môi
trường đo.

Các số liệu quan sát không tự chứng minh một thay đổi thuật toán là nguyên nhân
duy nhất tạo ra khác biệt. So sánh đáng tin cậy cần cùng tập seed, cùng cấu hình
và môi trường chạy tương đương.
