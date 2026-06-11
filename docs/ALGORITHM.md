# Algorithm Design

## 1. Board representation
Bàn chơi gồm các ô ở trạng thái:
- `hidden`: chưa mở.
- `revealed`: đã mở.
- `flagged`: được đánh dấu là mìn.

Mỗi vị trí được biểu diễn bởi `Position(row, col)`.

## 2. Deterministic inference
Với mỗi ô đã mở có số `n`:
- Đếm số ô đã flag xung quanh: `flagged`.
- Đếm tập ô ẩn xung quanh: `hidden`.
- Số mìn còn lại: `remaining = n - flagged`.

Luật:
- Nếu `remaining == 0`, mọi ô trong `hidden` là an toàn.
- Nếu `remaining == len(hidden)`, mọi ô trong `hidden` là mìn.

## 3. Constraint inference
Tạo constraint:

`sum(hidden_neighbors) = remaining_mines`

Ví dụ:

`A + B + C = 1`

Nếu có:

`A + B + C = 1`

và

`A + B + C + D + E = 2`

thì suy ra:

`D + E = 1`

## 4. Probability estimation
Khi không còn suy luận chắc chắn:
1. Lấy tất cả biến frontier.
2. Liệt kê các tổ hợp mìn hợp lệ.
3. Đếm số lần mỗi ô là mìn trong các tổ hợp hợp lệ.
4. Xác suất của ô = số lần là mìn / tổng số tổ hợp hợp lệ.
5. Chọn ô có xác suất thấp nhất để mở.

## 5. Hạn chế hiện tại
- Enumeration chỉ phù hợp với frontier nhỏ.
- Chưa tối ưu bằng chia component độc lập.
- Chưa có GUI.

## 6. Hướng phát triển
- Tách frontier thành các component độc lập.
- Dùng Gaussian elimination cho hệ phương trình tuyến tính.
- Thêm heuristic chọn ô ngoài frontier.
- Thêm giao diện trực quan.
