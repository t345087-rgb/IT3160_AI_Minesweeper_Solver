# AI Minesweeper Solver

## 1. Giới thiệu

**AI Minesweeper Solver** là project xây dựng một tác tử AI có khả năng chơi và giải trò chơi Minesweeper. Project được thực hiện trong khuôn khổ môn **Nhập môn Trí tuệ nhân tạo**.

Minesweeper là một trò chơi có yếu tố suy luận logic và ra quyết định trong điều kiện không chắc chắn. Người chơi cần dựa vào các con số trên bàn để xác định ô nào an toàn và ô nào có mìn. Trong nhiều tình huống, solver có thể suy luận chắc chắn; tuy nhiên, cũng có những trạng thái cần đánh giá xác suất để đưa ra lựa chọn hợp lý.

Project này tập trung vào việc mô phỏng bàn chơi, xây dựng solver, chạy đánh giá tự động và đo lường hiệu quả của thuật toán.

## 2. Mục tiêu project

Project hướng tới các mục tiêu chính sau:

* Mô phỏng đầy đủ bàn chơi Minesweeper.
* Xây dựng AI solver có khả năng chọn hành động tự động.
* Áp dụng suy luận logic để tìm ô an toàn hoặc ô chắc chắn có mìn.
* Sử dụng đánh giá xác suất trong các tình huống không chắc chắn.
* Chạy evaluation trên nhiều ván chơi để đo hiệu quả của solver.
* Cung cấp CLI để demo và đánh giá solver ở nhiều độ khó khác nhau.
* Cung cấp GUI để quan sát solver chạy trên bàn Minesweeper.
* Viết test tự động để kiểm tra độ ổn định của các module chính.

## 3. Thành viên nhóm

| Thành viên           | Vai trò chính                        |
| -------------------- | ------------------------------------ |
| Nguyễn Hữu Chính     | Solver logic, suy luận AI            |
| Hoàng Thị Thu Phương | Board engine, simulation, evaluation |
| Nguyễn Đăng Cao Tuấn | CLI, tài liệu, kiểm thử và tích hợp  |

## 4. Cấu trúc thư mục

```text
AI_Minesweeper_Solver/
├── docs/
│   ├── DEMO_GUIDE.md
│   ├── EVALUATION.md
│   └── PHAN_CONG_CONG_VIEC.md
├── src/
│   ├── minesweeper/
│   │   ├── __init__.py
│   │   ├── board.py
│   │   ├── cli.py
│   │   ├── evaluation.py
│   │   └── solver.py
│   └── minesweeper_gui/
│       ├── __init__.py
│       ├── app.py
│       ├── board_view.py
│       ├── control_panel.py
│       ├── game_loop.py
│       └── main_window.py
├── tests/
│   ├── test_board.py
│   ├── test_evaluation.py
│   └── test_solver.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 5. Các module chính

### 5.1. Board engine

File chính:

```text
src/minesweeper/board.py
```

Module này chịu trách nhiệm mô phỏng bàn chơi Minesweeper, bao gồm:

* Tạo bàn chơi với số hàng, số cột và số mìn tùy chọn.
* Đặt mìn ngẫu nhiên theo seed.
* Bảo vệ lượt click đầu tiên và các ô lân cận khi còn đủ vị trí đặt mìn.
* Tính số mìn xung quanh mỗi ô.
* Reveal ô.
* Flag ô nghi ngờ có mìn.
* Trả về trạng thái hiển thị của bàn chơi.

### 5.2. Solver

File chính:

```text
src/minesweeper/solver.py
```

Module solver chịu trách nhiệm chọn hành động tiếp theo cho AI. Solver sử dụng các chiến lược như:

* Suy luận logic cơ bản.
* Xác định ô chắc chắn an toàn.
* Xác định ô chắc chắn có mìn.
* Biểu diễn frontier thành graph và tách thành các connected component.
* Enumerate chính xác từng component nhỏ bằng backtracking có pruning.
* Ưu tiên biến xuất hiện trong nhiều constraint để prune sớm hơn.
* Dùng xác suất fallback cho component quá lớn, vô nghiệm hoặc khi không thể
  tạo global valid model.
* Kết hợp số model theo tổng số mìn của từng component với số mìn còn lại
  trên toàn bàn để tính global mine-count weighting.
* Chuyển xác suất chắc chắn thành hành động: flag khi xác suất mìn gần `1`,
  reveal khi xác suất mìn gần `0`.
* Mở ô trung tâm có tính thông tin cao ở trạng thái bàn mới.
* Chọn hành động reveal hoặc flag phù hợp.

Hai biến frontier được nối trong graph khi cùng thuộc một constraint. Với mỗi
component có không quá `MAX_ENUMERATION_VARIABLES` biến, solver gán từng biến
là safe hoặc mine và loại sớm nhánh khi số mìn đã gán vượt yêu cầu, hoặc khi số
biến còn lại không đủ để đạt yêu cầu.

Các model hợp lệ của từng component được nhóm theo số mìn, sau đó kết hợp với
tổng số mìn còn lại và số ô ẩn không thuộc frontier. Cách weighting toàn cục này
loại các tổ hợp không thể xảy ra và tạo marginal probability nhất quán giữa các
component. Với component quá lớn hoặc vô nghiệm, fallback được tính bằng
`remaining_mines / hidden_unflagged_cells` và clamp vào `[0, 1]`. Chi tiết được
trình bày trong `docs/ALGORITHM.md`.

### 5.3. Evaluation

File chính:

```text
src/minesweeper/evaluation.py
```

Module evaluation dùng để đánh giá solver trên nhiều ván chơi. Các chỉ số hiện có:

| Chỉ số          | Ý nghĩa                           |
| --------------- | --------------------------------- |
| Games           | Tổng số ván được đánh giá         |
| Wins            | Số ván solver thắng               |
| Losses          | Số ván solver thua                |
| Win rate        | Tỉ lệ thắng                       |
| Average guesses | Số lần đoán trung bình mỗi ván    |
| Average steps   | Số bước trung bình mỗi ván        |
| Average flags   | Số ô được cắm cờ trung bình       |
| Average runtime | Thời gian chạy trung bình mỗi ván |

Với metric guess hiện tại, `probability=None` trên hành động reveal được tính
là một guess vì solver không có estimate. Center opening dùng `probability=0.0`
vì Board đảm bảo lượt mở đầu tiên là an toàn.

### 5.4. CLI

File chính:

```text
src/minesweeper/cli.py
```

CLI hỗ trợ hai chế độ:

* Chạy demo một ván chơi.
* Chạy evaluation trên nhiều ván.

CLI cũng hỗ trợ các preset độ khó:

| Difficulty   |         Kích thước bàn |                 Số mìn |
| ------------ | ---------------------: | ---------------------: |
| beginner     |                  9 x 9 |                     10 |
| intermediate |                16 x 16 |                     40 |
| expert       |                16 x 30 |                     99 |
| custom       | Tùy chỉnh bằng tham số | Tùy chỉnh bằng tham số |

### 5.5. GUI

File chính:

```text
src/minesweeper_gui/app.py
```

GUI hỗ trợ tạo ván mới, chọn độ khó, thao tác thủ công trên bàn và chạy solver
trong background thread để quan sát từng bước giải.

## 6. Cài đặt

Yêu cầu:

* Python 3.12 hoặc tương thích.
* pip.

Clone repository:

```bash
git clone https://github.com/t345087-rgb/IT3160_AI_Minesweeper_Solver.git
cd IT3160_AI_Minesweeper_Solver
```

Cài dependencies:

```bash
python -m pip install -r requirements.txt
```

Cài project ở chế độ editable:

```bash
python -m pip install -e .
```

## 7. Cách chạy demo

Chạy demo với cấu hình mặc định:

```bash
python -m minesweeper.cli
```

Chạy demo với cấu hình tùy chỉnh:

```bash
python -m minesweeper.cli --rows 9 --cols 9 --mines 10 --steps 30 --seed 7
```

Chạy demo với preset độ khó:

```bash
python -m minesweeper.cli --difficulty beginner
```

```bash
python -m minesweeper.cli --difficulty intermediate
```

```bash
python -m minesweeper.cli --difficulty expert
```

Chạy GUI:

```bash
python -m minesweeper_gui.app
```

Nếu đã cài editable, có thể chạy bằng entry point:

```bash
minesweeper-gui
```

## 8. Cách chạy evaluation

Chạy evaluation mặc định:

```bash
python -m minesweeper.cli --evaluate --games 5
```

Ví dụ output:

```text
Evaluation result
- Games: 5
- Wins: 5
- Losses: 0
- Win rate: 100.00%
- Average steps: 24.20
- Average flags: 9.80
- Average guesses: 0.20
- Average runtime: 0.006049 seconds
```

Chạy evaluation với preset beginner:

```bash
python -m minesweeper.cli --evaluate --difficulty beginner --games 100
```

Chạy evaluation với preset intermediate:

```bash
python -m minesweeper.cli --evaluate --difficulty intermediate --games 100 --max-steps 500
```

Chạy evaluation với preset expert:

```bash
python -m minesweeper.cli --evaluate --difficulty expert --games 100 --max-steps 1000
```

Chạy evaluation với cấu hình custom:

```bash
python -m minesweeper.cli --evaluate --difficulty custom --rows 9 --cols 9 --mines 10 --games 10
```

### Kết quả evaluation hiện có

| Difficulty   | Games | Wins | Losses | Win rate | Avg. steps | Avg. flags | Avg. guesses | Avg. runtime |
| ------------ | ----: | ---: | -----: | -------: | ---------: | ---------: | -----------: | -----------: |
| Beginner     |   100 |   98 |      2 |   98.00% |      24.40 |       9.82 |         0.14 |   0.006662 s |
| Intermediate |   100 |   86 |     14 |   86.00% |     112.17 |      38.00 |         0.55 |   0.079003 s |
| Expert       |   100 |   32 |     68 |   32.00% |     231.32 |      76.27 |         2.65 |   0.250324 s |

Đây là kết quả của một lần chạy với 100 seed mặc định cho mỗi độ khó. Win rate
và runtime có thể thay đổi theo tập seed và môi trường chạy; xem
`docs/EVALUATION.md` để biết lệnh benchmark và cách diễn giải.

## 9. Kiểm thử

Project sử dụng `pytest` để kiểm thử tự động.

Chạy toàn bộ test:

```bash
python -m pytest
```

Kết quả hiện tại:

```text
70 passed
```

Các test hiện có:

| File test                  | Số test | Nội dung chính                                                        |
| -------------------------- | ------: | --------------------------------------------------------------------- |
| `tests/test_board.py`      |      16 | Kiểm tra board engine, first-click safety, flag, reveal, visible view |
| `tests/test_evaluation.py` |      11 | Kiểm tra evaluation, guess/runtime metric và format output            |
| `tests/test_solver.py`     |      43 | Kiểm tra inference, component-wise CSP, global weighting và actions   |

Tổng cộng:

```text
16 + 11 + 43 = 70 tests
```

## 10. Tài liệu liên quan

Các tài liệu phụ nằm trong thư mục `docs/`:

```text
docs/ALGORITHM.md
docs/DEMO_GUIDE.md
docs/EVALUATION.md
docs/PHAN_CONG_CONG_VIEC.md
```

Trong đó:

* `ALGORITHM.md`: mô tả deterministic inference, component-wise CSP,
  backtracking, pruning, global mine-count weighting và fallback.
* `EVALUATION.md`: mô tả kế hoạch, kết quả đánh giá solver, các chỉ số và cách
  chạy evaluation.
* `PHAN_CONG_CONG_VIEC.md`: mô tả phân công công việc trong nhóm.

## 11. Quy trình làm việc với Git

Các bước làm việc khuyến nghị:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/ten-chuc-nang
```

Sau khi sửa code:

```bash
python -m pytest
git status
git add <file-can-commit>
git commit -m "type: short description"
git push origin feature/ten-chuc-nang
```

Sau đó tạo Pull Request vào branch `develop`.

Không nên commit trực tiếp lên `develop`.

## 12. Trạng thái hiện tại

Project hiện đã có:

* Board engine hoạt động ổn định.
* Solver có thể tự động chọn hành động.
* CLI demo, GUI và evaluation.
* Evaluation có các chỉ số win rate, average guesses, average steps, average flags và average runtime.
* Preset độ khó beginner, intermediate, expert và custom.
* Component-wise CSP với backtracking, early pruning, global mine-count
  weighting và fallback xác suất.
* Hành động chắc chắn từ CSP probability và informative center opening.
* Test tự động với tổng cộng 70 test.
* Tài liệu demo, thuật toán và evaluation bằng tiếng Việt.

## 13. Kết luận

AI Minesweeper Solver là một project phù hợp với môn Nhập môn Trí tuệ nhân tạo vì kết hợp nhiều nội dung quan trọng như tìm kiếm, suy luận logic, ra quyết định trong điều kiện không chắc chắn và đánh giá hiệu quả thuật toán.

Project không chỉ mô phỏng trò chơi Minesweeper mà còn xây dựng một tác tử AI có khả năng chơi tự động, đưa ra quyết định và được đánh giá bằng các chỉ số định lượng rõ ràng.
