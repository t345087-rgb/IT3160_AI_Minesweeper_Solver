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

## 4. Component-wise CSP
Khi không còn suy luận chắc chắn, solver biểu diễn frontier thành một bài toán
thỏa mãn ràng buộc (CSP):

- Mỗi ô ẩn thuộc frontier là một biến nhị phân: `safe` hoặc `mine`.
- Mỗi constraint quy định tổng số biến `mine` trong một nhóm ô.
- Frontier được biểu diễn thành graph, trong đó mỗi biến là một đỉnh.
- Hai biến được nối với nhau nếu chúng cùng xuất hiện trong một constraint.
- Graph được tách thành các connected component.
- Mỗi component nhỏ được enumeration độc lập thay vì liệt kê tổ hợp trên toàn
  bộ frontier.

Với mỗi component có không quá `MAX_ENUMERATION_VARIABLES` biến, solver đếm tất
cả assignment thỏa mãn các constraint của component. Xác suất một ô có mìn là:

`số assignment hợp lệ trong đó ô là mine / tổng số assignment hợp lệ`

Sau đó solver chọn ô có xác suất mìn thấp nhất để mở.

## 5. Backtracking và pruning
Enumeration được thực hiện bằng recursive backtracking:

1. Gán lần lượt từng biến là `safe` hoặc `mine`.
2. Sau mỗi phép gán, cập nhật `assigned_mines` và `unassigned_variables` của
   từng constraint liên quan.
3. Prune nhánh nếu `assigned_mines > mine_count`.
4. Prune nhánh nếu
   `assigned_mines + unassigned_variables < mine_count`.
5. Chỉ ghi nhận assignment khi tất cả constraint có đúng số mìn yêu cầu.

Để phát hiện nhánh vô ích sớm hơn, solver ưu tiên các biến xuất hiện trong
nhiều constraint hơn. Nếu hai biến có cùng độ ưu tiên, thứ tự hàng và cột được
dùng để giữ kết quả ổn định.

## 6. Fallback xác suất
Solver dùng xác suất toàn cục:

`remaining_mines / hidden_unflagged_cells`

cho các trường hợp:

- Component có nhiều hơn `MAX_ENUMERATION_VARIABLES` biến.
- Component không có assignment nào thỏa mãn toàn bộ constraint.

Giá trị fallback được giới hạn trong khoảng từ `0.0` đến `1.0`.

Các component hiện được giải độc lập, nhưng phân bố xác suất giữa các component
chưa được ràng buộc bởi tổng số mìn còn lại trên toàn bàn. Vì vậy, các xác suất
component-wise hiện là một xấp xỉ và vẫn có thể được cải tiến bằng cách kết hợp
số assignment theo tổng số mìn của từng component.

## 7. Hạn chế và hướng phát triển
- Kết hợp xác suất giữa các component với ràng buộc tổng số mìn toàn bàn.
- Cải thiện cách xử lý component lớn thay vì dùng cùng một fallback cho mọi ô.
- Dùng Gaussian elimination cho hệ phương trình tuyến tính.
- Thêm heuristic chọn ô ngoài frontier.
- Thêm giao diện trực quan.
