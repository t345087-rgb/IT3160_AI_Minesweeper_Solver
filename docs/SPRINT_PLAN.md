# Sprint Plan

## Sprint 0: Khởi tạo repo và tài liệu
**Mục tiêu:** Có repo sạch, README, proposal, phân công công việc.

Tasks:
- Tạo cấu trúc thư mục.
- Tạo README.
- Tạo proposal.
- Tạo phân công công việc.
- Tạo GitHub Actions CI.

## Sprint 1: Board engine
**Mục tiêu:** Có mô phỏng bàn chơi Minesweeper.

Tasks:
- Implement `Position`.
- Implement `Board`.
- Implement `neighbors`.
- Implement `reveal` và `flag`.
- Đảm bảo first click an toàn.
- Viết test cho board.

## Sprint 2: Logic solver
**Mục tiêu:** AI suy luận được các bước chắc chắn.

Tasks:
- Tạo constraint từ các ô đã mở.
- Implement deterministic rules.
- Implement subset inference.
- Viết test solver.

## Sprint 3: Probability solver
**Mục tiêu:** AI xử lý được tình huống phải đoán.

Tasks:
- Liệt kê valid assignments.
- Tính xác suất mìn từng ô.
- Chọn ô có xác suất thấp nhất.
- Ghi nhận số lần phải đoán.

## Sprint 4: Evaluation + report
**Mục tiêu:** Có kết quả thực nghiệm và báo cáo hoàn chỉnh.

Tasks:
- Chạy nhiều game để tính win rate.
- So sánh random, logic-only, logic+probability.
- Viết final report.
- Chuẩn bị slide.
