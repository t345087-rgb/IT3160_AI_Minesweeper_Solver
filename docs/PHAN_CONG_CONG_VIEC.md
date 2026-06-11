# Phân công công việc nhóm

## Thành viên 1: Nguyễn Hữu Chính - 202416143
**Vai trò:** Trưởng nhóm + phụ trách thuật toán logic/CSP

### Nhiệm vụ chính
1. Thiết kế mô hình biểu diễn bàn chơi Minesweeper.
2. Xây dựng các luật suy luận cơ bản:
   - Nếu số mìn còn lại quanh ô bằng 0 → các ô ẩn xung quanh an toàn.
   - Nếu số mìn còn lại bằng số ô ẩn xung quanh → tất cả ô ẩn đó là mìn.
3. Xây dựng thuật toán suy luận constraint/subset inference.
4. Nghiên cứu hướng Gaussian elimination hoặc CSP enumeration cho các trường hợp phức tạp.
5. Viết unit test cho solver logic.

### File phụ trách
- `src/minesweeper/solver.py`
- `tests/test_solver.py`
- `docs/ALGORITHM.md`

### Deliverable
- Solver đưa ra được hành động `reveal` hoặc `flag`.
- Giải thích rõ thuật toán trong báo cáo.

---

## Thành viên 2: Hoàng Thị Thu Phương - 202400068
**Vai trò:** Phụ trách game engine, mô phỏng bàn chơi và đánh giá kết quả

### Nhiệm vụ chính
1. Cài đặt lớp `Board`, `Position`, `CellState`.
2. Sinh bàn chơi ngẫu nhiên với số dòng, số cột, số mìn tùy chọn.
3. Đảm bảo first click an toàn.
4. Cài đặt reveal, flag, neighbors, visible view.
5. Thiết kế bộ đánh giá:
   - Số game thắng/thua.
   - Tỉ lệ thắng.
   - Số bước trung bình.
   - Số lần phải đoán.
6. Viết test cho board.

### File phụ trách
- `src/minesweeper/board.py`
- `tests/test_board.py`
- `docs/EVALUATION.md`

### Deliverable
- Board chạy ổn định, test pass.
- Có bảng kết quả thực nghiệm để đưa vào báo cáo.

---

## Thành viên 3: Nguyễn Đăng Cao Tuấn - 202400119
**Vai trò:** Phụ trách CLI/demo, tài liệu, báo cáo và thuyết trình

### Nhiệm vụ chính
1. Xây dựng giao diện chạy demo bằng terminal.
2. Viết README hướng dẫn cài đặt và chạy project.
3. Chuẩn hóa repo GitHub:
   - `.gitignore`
   - `requirements.txt`
   - GitHub Actions CI
4. Viết proposal, báo cáo cuối kỳ, slide thuyết trình.
5. Tổng hợp kết quả từ các thành viên.

### File phụ trách
- `src/minesweeper/cli.py`
- `README.md`
- `docs/PROJECT_PROPOSAL.md`
- `docs/FINAL_REPORT_OUTLINE.md`
- `.github/workflows/python-ci.yml`

### Deliverable
- Demo chạy được bằng lệnh terminal.
- Repo sạch, dễ đọc, có hướng dẫn đầy đủ.

---

# Quy tắc làm việc nhóm

## Branch Git đề xuất
- `main`: bản ổn định cuối cùng.
- `develop`: nhánh tích hợp.
- `feature/board-engine`: phần Board.
- `feature/solver-logic`: phần Solver.
- `feature/demo-docs`: phần Demo + Docs.

## Cách commit
Ví dụ:
- `feat(board): implement neighbor calculation`
- `feat(solver): add deterministic inference rules`
- `test(board): add first-click safety test`
- `docs(report): add project motivation section`

## Definition of Done
Một task được xem là xong khi:
1. Code chạy không lỗi.
2. Có test nếu task liên quan đến logic.
3. README hoặc docs được cập nhật nếu cần.
4. Được ít nhất một thành viên khác review.
