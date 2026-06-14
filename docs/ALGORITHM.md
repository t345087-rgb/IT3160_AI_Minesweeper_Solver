# Algorithm Design

## 1. Biểu diễn bàn chơi và constraint

Bàn chơi gồm các ô ở trạng thái `hidden`, `revealed` hoặc `flagged`. Mỗi vị trí
được biểu diễn bởi `Position(row, col)`.

Mỗi ô `hidden` thuộc frontier là một biến nhị phân:

- `0`: ô an toàn.
- `1`: ô có mìn.

Với mỗi ô số đã `revealed`, solver đếm các ô lân cận đã flag và tạo constraint:

```text
sum(hidden_neighbors) = displayed_number - flagged_neighbors
```

Vế phải là số mìn còn lại quanh ô số đó.

## 2. Deterministic inference

Với một constraint có tập biến `hidden` và số mìn còn lại `remaining`:

- Nếu `remaining == 0`, mọi ô trong `hidden` đều an toàn và được `REVEAL`.
- Nếu `remaining == len(hidden)`, mọi ô trong `hidden` đều là mìn và được
  `FLAG`.

Solver chạy các luật chắc chắn này trước khi tính xác suất.

## 3. Subset inference

Nếu tập biến của constraint `A` là tập con của constraint `B`, solver tạo
constraint trên phần hiệu:

```text
variables(B - A) = mine_count(B) - mine_count(A)
```

Ví dụ:

```text
A + B + C = 1
A + B + C + D + E = 2
```

suy ra:

```text
D + E = 1
```

Nếu số mìn của constraint suy ra bằng `0` hoặc bằng số biến, solver tạo hành
động chắc chắn tương ứng.

## 4. Frontier component discovery

Solver biểu diễn frontier thành graph:

- Mỗi `Position` thuộc frontier là một vertex.
- Hai vertex được nối nếu cùng xuất hiện trong một constraint.
- Connected components chia frontier thành các nhóm CSP độc lập về constraint.

Việc chia component tránh phải enumerate mọi biến frontier trong cùng một
không gian tìm kiếm. Thứ tự component và vị trí được ổn định theo hàng, cột.

## 5. Component-wise CSP

Với component có không quá `MAX_ENUMERATION_VARIABLES` biến, solver enumerate
chính xác tất cả assignment thỏa mãn các constraint của component.

Component lớn hơn giới hạn không được enumerate và chuyển sang fallback. Nếu
một component vô nghiệm, component đó cũng dùng fallback; kết quả exact của
các component nhỏ, hợp lệ khác vẫn được giữ trong bước component-wise
fallback.

## 6. Backtracking và pruning

Enumeration dùng recursive backtracking:

1. Sắp xếp biến theo số constraint chứa biến, ưu tiên biến xuất hiện nhiều hơn.
2. Gán từng biến lần lượt là `safe` (`0`) hoặc `mine` (`1`).
3. Cập nhật `assigned_mines` và `unassigned_variables` cho các constraint liên
   quan.
4. Prune nếu `assigned_mines > required_mines`.
5. Prune nếu
   `assigned_mines + unassigned_variables < required_mines`.
6. Chỉ ghi nhận model khi mọi constraint có đúng số mìn yêu cầu.

Nếu hai biến có cùng độ ưu tiên, solver dùng thứ tự hàng và cột để giữ kết quả
ổn định.

## 7. Component model counts

Solver không chỉ lưu marginal probability cục bộ mà nhóm model hợp lệ theo
tổng số mìn trong component:

- `ways_by_mine_count[m]`: số model hợp lệ có đúng `m` mìn.
- `mine_hits_by_position_and_mine_count[position][m]`: số model có đúng `m`
  mìn trong đó `position` là mìn.

Các phân phối này là đầu vào cho bước weighting theo tổng số mìn toàn bàn.

## 8. Global mine-count weighting

Số mìn còn lại được tính bằng:

```text
remaining_mines = total_mines - flagged_cells
```

Solver ghép `ways_by_mine_count` của các component bằng convolution/dynamic
programming. Prefix và suffix distributions cho phép tính trọng số của từng
ô mà không phải ghép lại toàn bộ component từ đầu.

Gọi `U` là số ô `hidden` không thuộc frontier. Nếu các component dùng tổng
`m` mìn, số cách đặt phần mìn còn lại ngoài frontier là:

```text
C(U, remaining_mines - m)
```

Tổng số global valid models là tổng số model component nhân với số tổ hợp ngoài
frontier tương ứng. Xác suất của từng ô frontier được tính từ số global valid
models trong đó ô là mìn. Các ô unconstrained có cùng xác suất, được tính từ
số mìn kỳ vọng ngoài frontier trên cùng tập global valid models.

Nhờ bước này, xác suất giữa các component và các ô ngoài frontier đều bị ràng
buộc bởi tổng số mìn còn lại trên toàn bàn.

## 9. Probability fallback

Fallback probability là:

```text
remaining_mines / hidden_unflagged_cells
```

Giá trị được clamp vào `[0, 1]`. Fallback được dùng khi:

- Component vượt `MAX_ENUMERATION_VARIABLES`.
- Component vô nghiệm.
- `remaining_mines` không nằm trong khoảng hợp lệ.
- Không tồn tại global valid model.

Khi global weighting không dùng được, solver chuyển sang xử lý component-wise:
component nhỏ và hợp lệ vẫn được enumerate cục bộ; chỉ component quá lớn hoặc
vô nghiệm nhận fallback probability.

## 10. Chọn hành động từ xác suất

Sau deterministic và subset inference, solver xử lý probability estimates theo
thứ tự:

1. Nếu `probability >= 1 - PROBABILITY_EPSILON`, chọn `FLAG`.
2. Nếu `probability <= PROBABILITY_EPSILON`, chọn `REVEAL`.
3. Chỉ khi không có hành động chắc chắn, reveal ô có xác suất mìn thấp nhất.

Nếu không có constraint hoặc probability estimate, solver dùng ô `hidden` đầu
tiên làm fallback cuối cùng.

## 11. Informative center opening

Khi board chưa có ô `revealed` hoặc `flagged`, solver mở:

```text
Position(rows // 2, cols // 2)
```

Board đảm bảo first click và các ô lân cận của nó an toàn khi còn đủ vị trí để
đặt mìn. Vì ô giữa có nhiều ô lân cận hơn ô góc, mở giữa thường tạo vùng thông
tin ban đầu lớn hơn.

## 12. Hạn chế

- Component lớn dùng cùng fallback probability thay vì một phép xấp xỉ CSP chi
  tiết hơn.
- Backtracking vẫn có độ phức tạp theo cấp số nhân trong trường hợp xấu.
- Kết quả benchmark phụ thuộc vào tập seed, cấu hình chạy và môi trường.
