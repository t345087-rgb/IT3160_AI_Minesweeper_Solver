# Project Proposal: Intelligent Minesweeper Solver
## Hệ thống giải đố Dò mìn thông minh

## 1. Thông tin project
**Tên dự án:** AI Minesweeper Solver - Giải pháp tối ưu cho bài toán quyết định dưới điều kiện không chắc chắn.

**Đội ngũ thực hiện:**
- Nguyễn Hữu Chính - 202416143
- Hoàng Thị Thu Phương - 202400068
- Nguyễn Đăng Cao Tuấn - 202400119

## 2. Đặt vấn đề
Minesweeper không chỉ là trò chơi giải trí mà còn là bài toán yêu cầu suy luận logic, biểu diễn tri thức và ra quyết định trong điều kiện không chắc chắn. Người chơi phải suy luận vị trí mìn dựa trên các con số đã mở. Khi không thể suy luận chắc chắn, người chơi phải chọn nước đi có rủi ro thấp nhất.

## 3. Mục tiêu
Xây dựng một tác tử AI có khả năng:
1. Biểu diễn trạng thái bàn chơi Minesweeper.
2. Suy luận các ô chắc chắn an toàn hoặc chắc chắn có mìn.
3. Sử dụng ràng buộc để xử lý tình huống phức tạp.
4. Ước lượng xác suất mìn để chọn bước đi tốt nhất khi bắt buộc phải đoán.
5. Đánh giá hiệu quả bằng các chỉ số thực nghiệm.

## 4. Phương pháp đề xuất
### 4.1 Logic-based inference
Sử dụng các luật suy luận cơ bản của Minesweeper:
- Nếu một ô số đã đủ số mìn được đánh dấu, các ô ẩn còn lại quanh nó là an toàn.
- Nếu số ô ẩn còn lại đúng bằng số mìn còn thiếu, tất cả các ô đó là mìn.

### 4.2 Constraint Satisfaction Problem
Mỗi ô ẩn ở biên được xem như biến nhị phân:
- `0`: không có mìn.
- `1`: có mìn.

Mỗi ô số tạo ra một phương trình ràng buộc dạng:

`x1 + x2 + ... + xk = số_mìn_còn_lại`

### 4.3 Subset inference
Nếu có hai ràng buộc A và B, trong đó tập biến của A là tập con của B, ta có thể suy ra ràng buộc mới từ `B - A`.

### 4.4 Probability fallback
Khi không còn nước đi chắc chắn, AI liệt kê các cấu hình hợp lệ trên frontier nhỏ để tính xác suất mìn cho từng ô, sau đó chọn ô có xác suất thấp nhất.

## 5. Công nghệ sử dụng
- Python 3.10+
- NumPy
- Pytest
- Rich CLI
- GitHub Actions CI

## 6. Sản phẩm cuối cùng
1. Source code solver.
2. Demo chạy bằng terminal.
3. Unit tests.
4. Báo cáo giải thích thuật toán.
5. Kết quả thực nghiệm.
6. Slide thuyết trình.

## 7. Độ phù hợp với môn Nhập môn AI
Project phù hợp vì có các nội dung cốt lõi của AI:
- Tác tử thông minh.
- Biểu diễn tri thức.
- Suy luận logic.
- Constraint satisfaction.
- Ra quyết định dưới bất định.
- Đánh giá hiệu năng của tác tử.
