# AI Minesweeper Solver

AI Minesweeper Solver là project xây dựng một tác tử AI có khả năng chơi và giải trò chơi **Minesweeper**. Project được thực hiện trong khuôn khổ môn **Nhập môn Trí tuệ nhân tạo**.

Minesweeper là một bài toán phù hợp để mô phỏng suy luận logic và ra quyết định trong điều kiện không chắc chắn. Solver trong project này kết hợp các luật suy luận chắc chắn, suy luận theo constraint, CSP theo từng component và đánh giá xác suất để chọn hành động tiếp theo.

---

## 1. Tính năng chính

* Mô phỏng bàn chơi Minesweeper với cơ chế mở ô, cắm cờ, kiểm tra thắng/thua.
* Đảm bảo lượt mở đầu tiên an toàn, đồng thời ưu tiên mở ô trung tâm để tạo nhiều thông tin ban đầu hơn.
* Solver tự động chọn hành động `reveal` hoặc `flag`.
* Hỗ trợ deterministic inference, subset inference, component-wise CSP và probability fallback.
* Có CLI để chạy demo hoặc đánh giá solver trên nhiều ván.
* Có GUI bằng PySide6 để quan sát AI chơi trực quan.
* Có test tự động bằng `pytest`.
* Có tài liệu riêng cho thuật toán, evaluation, demo và phân công công việc.

---

## 2. Thành viên nhóm

| Thành viên           | Vai trò chính                                 |
| -------------------- | --------------------------------------------- |
| Nguyễn Hữu Chính     | Solver logic, suy luận AI, CSP                |
| Hoàng Thị Thu Phương | Board engine, simulation, evaluation          |
| Nguyễn Đăng Cao Tuấn | CLI, GUI/demo, tài liệu, kiểm thử và tích hợp |

---

## 3. Công nghệ sử dụng

| Thành phần       | Công nghệ                  |
| ---------------- | -------------------------- |
| Ngôn ngữ chính   | Python                     |
| CLI              | argparse, rich             |
| GUI              | PySide6                    |
| Testing          | pytest                     |
| Đóng gói project | pyproject.toml, setuptools |

Yêu cầu Python: **Python 3.10 trở lên**.

---

## 4. Cấu trúc thư mục

```text
IT3160_AI_Minesweeper_Solver/
├── .github/
│   └── workflows/
├── docs/
│   ├── ALGORITHM.md
│   ├── EVALUATION.md
│   ├── FINAL_REPORT_OUTLINE.md
│   ├── PHAN_CONG_CONG_VIEC.md
│   ├── PROJECT_PROPOSAL.md
│   └── SPRINT_PLAN.md
├── examples/
│   └── demo_commands.md
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
│       ├── main_window.py
│       └── resources/
├── tests/
│   ├── test_board.py
│   ├── test_evaluation.py
│   └── test_solver.py
├── DEMO_GUIDE.md
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## 5. Các module chính

### 5.1. Board engine

File chính:

```text
src/minesweeper/board.py
```

Module này chịu trách nhiệm mô phỏng bàn chơi Minesweeper:

* Tạo bàn chơi theo số hàng, số cột và số mìn.
* Đặt mìn theo seed để có thể tái lập kết quả.
* Đảm bảo ô mở đầu tiên an toàn.
* Tính số mìn xung quanh mỗi ô.
* Quản lý trạng thái ô: `hidden`, `revealed`, `flagged`.
* Hỗ trợ reveal, flag, kiểm tra thắng/thua và tạo view hiển thị.

### 5.2. Solver

File chính:

```text
src/minesweeper/solver.py
```

Solver chọn hành động tiếp theo dựa trên các chiến lược:

* **Deterministic inference**: dùng luật chắc chắn của Minesweeper.
* **Subset inference**: suy ra constraint mới khi một tập biến là tập con của tập khác.
* **Frontier component discovery**: tách frontier thành các component độc lập.
* **Component-wise CSP**: enumerate các assignment hợp lệ cho component nhỏ bằng backtracking có pruning.
* **Global mine-count weighting**: kết hợp số model của các component với tổng số mìn còn lại trên toàn bàn.
* **Probability fallback**: dùng xác suất xấp xỉ khi component quá lớn, vô nghiệm hoặc không thể tính global model.
* **Action selection**: flag ô chắc chắn có mìn, reveal ô chắc chắn an toàn, hoặc chọn ô có xác suất mìn thấp nhất.

Giới hạn hiện tại của enumeration:

```text
MAX_ENUMERATION_VARIABLES = 20
```

### 5.3. Evaluation

File chính:

```text
src/minesweeper/evaluation.py
```

Module evaluation chạy solver trên nhiều ván và tính các chỉ số:

| Chỉ số          | Ý nghĩa                                |
| --------------- | -------------------------------------- |
| Games           | Tổng số ván được đánh giá              |
| Wins            | Số ván solver thắng                    |
| Losses          | Số ván solver thua                     |
| Win rate        | Tỉ lệ thắng                            |
| Average steps   | Số bước trung bình mỗi ván             |
| Average flags   | Số ô được cắm cờ trung bình            |
| Average guesses | Số lần đoán trung bình mỗi ván         |
| Average runtime | Thời gian inference trung bình mỗi ván |

### 5.4. CLI

File chính:

```text
src/minesweeper/cli.py
```

CLI hỗ trợ:

* Chạy demo một ván.
* Chạy evaluation nhiều ván.
* Chọn preset độ khó: `beginner`, `intermediate`, `expert`.
* Chạy cấu hình custom bằng `--rows`, `--cols`, `--mines`.

### 5.5. GUI

Thư mục chính:

```text
src/minesweeper_gui/
```

GUI được xây dựng bằng PySide6, hỗ trợ:

* Hiển thị bàn chơi trực quan.
* Chọn độ khó.
* Bắt đầu/dừng solver.
* Điều chỉnh tốc độ solver.
* Chơi thủ công bằng click chuột.
* Theo dõi số mìn, số flag và số ô đã mở trên status bar.

---

## 6. Cài đặt

Clone repository:

```bash
git clone https://github.com/t345087-rgb/IT3160_AI_Minesweeper_Solver.git
cd IT3160_AI_Minesweeper_Solver
```

Tạo môi trường ảo nếu cần:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows:

```bash
.venv\Scripts\activate
```

Kích hoạt môi trường ảo trên macOS/Linux:

```bash
source .venv/bin/activate
```

Cài dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Sau khi cài editable, có thể chạy project bằng cả hai kiểu:

```bash
python -m minesweeper.cli
```

hoặc:

```bash
minesweeper
```

---

## 7. Chạy CLI demo

Chạy demo mặc định:

```bash
python -m minesweeper.cli
```

Chạy demo với preset beginner:

```bash
python -m minesweeper.cli --difficulty beginner
```

Chạy demo với preset intermediate:

```bash
python -m minesweeper.cli --difficulty intermediate --steps 100
```

Chạy demo với preset expert:

```bash
python -m minesweeper.cli --difficulty expert --steps 200
```

Chạy demo với cấu hình custom:

```bash
python -m minesweeper.cli --difficulty custom --rows 9 --cols 9 --mines 10 --steps 30 --seed 7
```

Nếu đã cài editable, có thể dùng lệnh ngắn hơn:

```bash
minesweeper --difficulty beginner
```

---

## 8. Chạy GUI

Sau khi cài project ở chế độ editable, chạy:

```bash
minesweeper-gui
```

Hoặc chạy trực tiếp bằng module:

```bash
python -m minesweeper_gui.app
```

Trong GUI, người dùng có thể chọn độ khó, tạo ván mới, chơi thủ công hoặc nhấn **Start Solver** để AI tự động chơi.

---

## 9. Chạy evaluation

Chạy evaluation mặc định:

```bash
python -m minesweeper.cli --evaluate --games 100
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
python -m minesweeper.cli --evaluate --difficulty custom --rows 9 --cols 9 --mines 10 --games 100
```

Ví dụ output:

```text
Evaluation result
- Games: 100
- Wins: 98
- Losses: 2
- Win rate: 98.00%
- Average steps: 24.40
- Average flags: 9.82
- Average guesses: 0.14
- Average runtime: 0.006662 seconds
```

---

## 10. Kết quả benchmark hiện tại

Kết quả dưới đây được ghi nhận khi chạy 100 games với seed mặc định `0..99`:

| Difficulty   | Games | Wins | Losses | Win rate | Avg. steps | Avg. flags | Avg. guesses | Avg. runtime |
| ------------ | ----: | ---: | -----: | -------: | ---------: | ---------: | -----------: | -----------: |
| Beginner     |   100 |   98 |      2 |   98.00% |      24.40 |       9.82 |         0.14 |   0.006662 s |
| Intermediate |   100 |   86 |     14 |   86.00% |     112.17 |      38.00 |         0.55 |   0.079003 s |
| Expert       |   100 |   32 |     68 |   32.00% |     231.32 |      76.27 |         2.65 |   0.250324 s |

Kết quả có thể thay đổi theo seed, phiên bản Python, phần cứng và tải hệ thống. Khi so sánh các phiên bản solver, cần giữ nguyên preset, số ván, tập seed và `max-steps`.

---

## 11. Kiểm thử

Project sử dụng `pytest` để kiểm thử tự động.

Chạy toàn bộ test:

```bash
python -m pytest
```

Kết quả hiện tại:

```text
70 passed
```

Phân bố test:

| File test                  | Số test | Nội dung chính                                                                               |
| -------------------------- | ------: | -------------------------------------------------------------------------------------------- |
| `tests/test_board.py`      |      16 | Board engine, first-click safety, reveal, flag, visible view, win/loss                       |
| `tests/test_evaluation.py` |      11 | Evaluation result, guess counting, runtime metric, format output                             |
| `tests/test_solver.py`     |      43 | Deterministic inference, subset inference, CSP, global weighting, fallback, action selection |

Tổng cộng:

```text
16 + 11 + 43 = 70 tests
```

---

## 12. Tài liệu liên quan

Các tài liệu phụ nằm trong thư mục `docs/`:

| File                           | Nội dung                                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------------------- |
| `docs/ALGORITHM.md`            | Mô tả deterministic inference, subset inference, CSP, pruning, global weighting và fallback |
| `docs/EVALUATION.md`           | Mô tả chỉ số đánh giá, benchmark và cách chạy evaluation                                    |
| `docs/FINAL_REPORT_OUTLINE.md` | Dàn ý báo cáo cuối kỳ                                                                       |
| `docs/PHAN_CONG_CONG_VIEC.md`  | Phân công công việc trong nhóm                                                              |
| `docs/PROJECT_PROPOSAL.md`     | Đề xuất project ban đầu                                                                     |
| `docs/SPRINT_PLAN.md`          | Kế hoạch sprint                                                                             |

Ngoài ra:

| File                        | Nội dung                  |
| --------------------------- | ------------------------- |
| `DEMO_GUIDE.md`             | Hướng dẫn demo CLI và GUI |
| `examples/demo_commands.md` | Một số lệnh demo nhanh    |

---

## 13. Quy trình làm việc với Git

Quy trình khuyến nghị:

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

---

## 14. Trạng thái hiện tại

Project hiện đã hoàn thành các phần chính:

* Board engine hoạt động ổn định.
* Solver có khả năng tự động chọn hành động.
* CLI hỗ trợ demo và evaluation.
* GUI PySide6 hỗ trợ quan sát và tương tác trực quan.
* Evaluation có các chỉ số định lượng rõ ràng.
* Thuật toán đã có component-wise CSP, backtracking, early pruning, global mine-count weighting và fallback xác suất.
* Test tự động hiện có 70 test.
* Tài liệu thuật toán, evaluation, demo và phân công đã được bổ sung.

---

## 15. Kết luận

AI Minesweeper Solver là một project phù hợp với môn Nhập môn Trí tuệ nhân tạo vì kết hợp nhiều nội dung quan trọng: biểu diễn trạng thái, suy luận logic, constraint satisfaction problem, tìm kiếm có pruning, xác suất và đánh giá hiệu quả thuật toán.

Project không chỉ mô phỏng trò chơi Minesweeper mà còn xây dựng một tác tử AI có thể chơi tự động, đưa ra quyết định dựa trên thông tin hiện có và được đánh giá bằng các chỉ số định lượng.
