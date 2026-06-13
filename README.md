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
│   ├── EVALUATION.md
│   └── PHAN_CONG_CONG_VIEC.md
├── src/
│   └── minesweeper/
│       ├── __init__.py
│       ├── board.py
│       ├── cli.py
│       ├── evaluation.py
│       └── solver.py
├── tests/
│   ├── test_board.py
│   ├── test_evaluation.py
│   └── test_solver.py
├── requirements.txt
├── pyproject.toml
└── README.md