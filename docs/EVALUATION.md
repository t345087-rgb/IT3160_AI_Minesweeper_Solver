# Evaluation Plan

## 1. Metrics
Các chỉ số đánh giá:
- Win rate: số game thắng / tổng số game.
- Average steps: số bước trung bình mỗi game.
- Guess count: số lần phải chọn theo xác suất thay vì chắc chắn.
- Runtime: thời gian xử lý trung bình.

## 2. Experiment settings
Chạy thử trên các mức:
- Beginner: 9x9, 10 mines.
- Intermediate: 16x16, 40 mines.
- Expert: 16x30, 99 mines.

## 3. Baseline comparison
So sánh với:
1. Random agent.
2. Logic-only agent.
3. Logic + probability agent.

## 4. Expected result
Agent dùng logic + probability nên có tỉ lệ thắng cao hơn random agent và logic-only agent trong các tình huống phải đoán.
