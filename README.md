# AI Minesweeper Solver

Hệ thống giải đố Dò mìn thông minh cho môn **Nhập môn AI**.

## Trạng thái hiện tại

- Đã có board engine mô phỏng trò chơi Minesweeper.
- Đã có AI solver cơ bản dùng logic, constraint và xác suất.
- Đã có CLI demo để chạy thử trên terminal.
- Đã có test tự động bằng pytest.

## 1. Giới thiệu
Project xây dựng một AI agent có khả năng chơi Minesweeper bằng cách kết hợp:
- Suy luận logic cơ bản.
- Constraint Satisfaction Problem.
- Subset inference.
- Ước lượng xác suất trong trường hợp bắt buộc phải đoán.

## 2. Thành viên
| Thành viên | MSSV | Vai trò |
|---|---:|---|
| Nguyễn Hữu Chính | 202416143 | Trưởng nhóm, Solver logic/CSP |
| Hoàng Thị Thu Phương | 202400068 | Board engine, simulation, evaluation |
| Nguyễn Đăng Cao Tuấn | 202400119 | CLI/demo, docs, report, presentation |

## 3. Cấu trúc repo
```text
ai-minesweeper-solver/
├── src/minesweeper/
│   ├── board.py          # Mô phỏng bàn chơi
│   ├── solver.py         # AI solver
│   └── cli.py            # Demo terminal
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
├── .github/workflows/python-ci.yml
├── requirements.txt
├── pyproject.toml
└── README.md
```

## 4. Cài đặt
```bash
git clone <repo-url>
cd ai-minesweeper-solver
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Cài thư viện:
```bash
pip install -r requirements.txt
```

## 5. Chạy demo
```bash
python -m minesweeper.cli --rows 9 --cols 9 --mines 10 --steps 30 --seed 7
```

## 6. Chạy test
```bash
pytest
```

## 7. Nội dung AI trong project
Project thể hiện các kiến thức AI sau:
- Agent quan sát trạng thái bàn chơi và chọn hành động.
- Knowledge representation bằng constraints.
- Logical inference để suy ra ô an toàn hoặc ô có mìn.
- Constraint satisfaction để tìm cấu hình mìn hợp lệ.
- Decision making under uncertainty khi phải chọn ô có xác suất rủi ro thấp nhất.

## 8. Hướng phát triển
- Thêm GUI.
- Tách frontier thành các component độc lập để tăng tốc.
- Dùng Gaussian elimination cho constraint solving.
- Chạy đánh giá hàng nghìn game để có số liệu ổn định.
