# AI Minesweeper Solver

Hệ thống giải đố Dò mìn thông minh cho môn **Nhập môn AI**.

## Trạng thái hiện tại

- Đã có board engine mô phỏng trò chơi Minesweeper.
- Đã có AI solver cơ bản dùng logic, constraint, subset inference và xác suất.
- Đã có CLI demo để chạy thử trên terminal.
- Đã có chế độ evaluation để chạy solver trên nhiều ván.
- Đã có test tự động bằng pytest.
- Đã có tài liệu proposal, thuật toán, phân công công việc và kế hoạch sprint.

## 1. Giới thiệu

Project xây dựng một AI agent có khả năng chơi Minesweeper bằng cách kết hợp:

- Suy luận logic cơ bản.
- Constraint Satisfaction Problem.
- Subset inference.
- Ước lượng xác suất trong trường hợp bắt buộc phải đoán.

Mục tiêu của project không chỉ là chơi Minesweeper tự động, mà còn minh họa các khái niệm quan trọng trong môn Nhập môn AI như agent, biểu diễn tri thức, suy luận logic, tìm kiếm ràng buộc và ra quyết định trong điều kiện không chắc chắn.

## 2. Thành viên

| Thành viên | MSSV | Vai trò |
|---|---:|---|
| Nguyễn Hữu Chính | 202416143 | Trưởng nhóm, Solver logic/CSP |
| Hoàng Thị Thu Phương | 202400068 | Board engine, simulation, evaluation |
| Nguyễn Đăng Cao Tuấn | 202400119 | CLI/demo, docs, report, presentation |

## 3. Cấu trúc repo

```text
IT3160_AI_Minesweeper_Solver/
├── src/minesweeper/
│   ├── board.py          # Mô phỏng bàn chơi
│   ├── solver.py         # AI solver
│   ├── evaluation.py     # Đánh giá solver trên nhiều game
│   └── cli.py            # Demo terminal và evaluation mode
├── tests/
│   ├── test_board.py
│   └── test_solver.py
├── docs/
│   ├── PROJECT_PROPOSAL.md
│   ├── PHAN_CONG_CONG_VIEC.md
│   ├── ALGORITHM.md
│   ├── EVALUATION.md
│   ├── FINAL_REPORT_OUTLINE.md
│   └── SPRINT_PLAN.md
├── examples/
│   └── demo_commands.md
├── .github/workflows/python-ci.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 4. Cài đặt

Clone repo:

```bash
git clone https://github.com/t345087-rgb/IT3160_AI_Minesweeper_Solver.git
cd IT3160_AI_Minesweeper_Solver
```

Tạo môi trường ảo:

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

Cài thư viện:

```bash
python -m pip install -r requirements.txt
```

Cài package ở chế độ editable để chạy module dễ hơn trong lúc phát triển:

```bash
python -m pip install -e .
```

## 5. Chạy demo một ván

```bash
python -m minesweeper.cli --rows 9 --cols 9 --mines 10 --steps 30 --seed 7
```

Lệnh trên chạy một ván Minesweeper 9x9 với 10 mìn, tối đa 30 bước, và in từng hành động của AI solver ra terminal.

Ví dụ hành động:

```text
Step 1: reveal Position(row=0, col=0) | no information; first hidden cell fallback | p=None
```

## 6. Chạy evaluation

Chạy solver trên nhiều ván để lấy thống kê:

```bash
python -m minesweeper.cli --evaluate --games 100
```

Có thể thay đổi kích thước bàn và số mìn:

```bash
python -m minesweeper.cli --evaluate --games 100 --rows 9 --cols 9 --mines 10
```

Kết quả evaluation gồm:

- Số ván đã chạy.
- Số ván thắng.
- Số ván thua.
- Tỉ lệ thắng.
- Số bước trung bình.
- Số flag trung bình.

Ví dụ output:

```text
Evaluation result
- Games: 5
- Wins: 5
- Losses: 0
- Win rate: 100.00%
- Average steps: 81.00
- Average flags: 10.00
```

## 7. Chạy test

```bash
python -m pytest
```

Kết quả mong muốn:

```text
5 passed
```

## 8. Nội dung AI trong project

Project thể hiện các kiến thức AI sau:

- **Agent**: AI quan sát trạng thái bàn chơi và chọn hành động reveal hoặc flag.
- **Knowledge representation**: Trạng thái bàn chơi được biểu diễn bằng các ô đã mở, ô ẩn, ô đã flag và số gợi ý.
- **Logical inference**: Nếu số mìn còn lại quanh một ô bằng 0, các ô lân cận còn lại là an toàn. Nếu số mìn còn lại bằng số ô ẩn lân cận, tất cả các ô đó là mìn.
- **Constraint Satisfaction Problem**: Mỗi ô ẩn ở frontier có thể được xem là biến nhị phân: có mìn hoặc không có mìn.
- **Subset inference**: So sánh các tập ràng buộc để suy ra ô an toàn hoặc ô có mìn.
- **Decision making under uncertainty**: Khi không suy luận chắc chắn được, solver chọn ô có xác suất chứa mìn thấp nhất.

## 9. Thuật toán tổng quát

Solver hoạt động theo thứ tự ưu tiên:

1. Thu thập constraint từ các ô đã reveal.
2. Áp dụng luật logic cơ bản.
3. Áp dụng subset inference.
4. Ước lượng xác suất mìn cho các ô frontier.
5. Nếu vẫn không có thông tin, chọn ô ẩn đầu tiên làm fallback.

Luồng quyết định:

```text
Board state
    ↓
Extract constraints
    ↓
Logical inference
    ↓
Subset inference
    ↓
Probability estimation
    ↓
Choose action: reveal / flag
```

## 10. Quy trình làm việc với Git

Nhóm làm việc theo mô hình branch:

```text
main      : bản ổn định cuối cùng
develop   : nhánh tích hợp chính
feature/* : nhánh làm việc của từng phần
```

Các nhánh chính:

```text
feature/solver-logic
feature/board-evaluation
feature/demo-docs
```

Quy trình làm việc:

```bash
git checkout develop
git pull origin develop
git checkout feature/demo-docs
git pull origin develop
```

Sau khi sửa code hoặc tài liệu:

```bash
python -m pytest
git status
git add .
git commit -m "message"
git push
```

Sau đó tạo Pull Request từ nhánh feature vào `develop`.

## 11. Phân công công việc

| Thành viên | Phần việc chính | File liên quan |
|---|---|---|
| Nguyễn Hữu Chính | Solver logic, CSP, xác suất | `src/minesweeper/solver.py`, `docs/ALGORITHM.md` |
| Hoàng Thị Thu Phương | Board engine, simulation, evaluation | `src/minesweeper/board.py`, `src/minesweeper/evaluation.py`, `docs/EVALUATION.md` |
| Nguyễn Đăng Cao Tuấn | CLI demo, README, report, slide | `src/minesweeper/cli.py`, `README.md`, `docs/FINAL_REPORT_OUTLINE.md` |

## 12. Hướng phát triển

- Thêm GUI để trực quan hóa quá trình giải.
- Tách frontier thành các component độc lập để tăng tốc evaluation.
- Dùng Gaussian elimination cho constraint solving.
- Chạy đánh giá hàng nghìn game để có số liệu ổn định hơn.
- So sánh solver logic với solver random baseline.
- Xuất kết quả evaluation ra file CSV để đưa vào báo cáo.