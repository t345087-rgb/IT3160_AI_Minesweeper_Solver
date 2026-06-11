\# Kế hoạch đánh giá hệ thống



Tài liệu này mô tả cách đánh giá hiệu quả của hệ thống AI Minesweeper Solver.



\## 1. Mục tiêu đánh giá



Mục tiêu của phần đánh giá là đo lường khả năng giải bàn Minesweeper của solver trên nhiều ván chơi khác nhau.



Do Minesweeper là trò chơi có yếu tố không chắc chắn, một ván chơi đơn lẻ không đủ để kết luận solver hoạt động tốt hay không. Vì vậy, hệ thống được đánh giá trên nhiều ván chơi với các seed ngẫu nhiên khác nhau.



Phần đánh giá tập trung vào hai khía cạnh chính:



\* Độ chính xác: solver thắng được bao nhiêu ván.

\* Hiệu quả: solver mất bao nhiêu bước và bao nhiêu thời gian để giải một ván.



\## 2. Các chỉ số đánh giá



| Chỉ số          | Ý nghĩa                                    |

| --------------- | ------------------------------------------ |

| Games           | Tổng số ván chơi được dùng để đánh giá     |

| Wins            | Số ván solver thắng                        |

| Losses          | Số ván solver thua                         |

| Win rate        | Tỉ lệ thắng của solver                     |

| Average steps   | Số bước trung bình trong mỗi ván           |

| Average flags   | Số ô được cắm cờ trung bình trong mỗi ván  |

| Average runtime | Thời gian chạy trung bình để xử lý một ván |



\## 3. Cách chạy đánh giá



Chạy lệnh sau từ thư mục gốc của project:



```bash

python -m minesweeper.cli --evaluate --games 5

```



Ví dụ kết quả:



```text

Evaluation result

\- Games: 5

\- Wins: 5

\- Losses: 0

\- Win rate: 100.00%

\- Average steps: 81.00

\- Average flags: 10.00

\- Average runtime: 0.066572 seconds

```



Có thể thay đổi số lượng ván chơi. Ví dụ:



```bash

python -m minesweeper.cli --evaluate --games 100

```



Số lượng ván càng lớn thì kết quả đánh giá càng đáng tin cậy.



\## 4. Kiểm thử tự động



Module đánh giá cũng được kiểm thử bằng pytest.



Chạy lệnh:



```bash

python -m pytest

```



Kết quả kiểm thử hiện tại:



```text

14 passed

```



Các test kiểm tra những nội dung chính sau:



\* Một ván chơi có thể được chạy và trả về kết quả hợp lệ.

\* Hàm đánh giá trả về đúng các thống kê tổng hợp.

\* Hệ thống từ chối số lượng ván không hợp lệ.

\* Kết quả hiển thị có chứa thông tin về thời gian chạy trung bình.



\## 5. Diễn giải kết quả



Tỉ lệ thắng càng cao cho thấy solver càng hiệu quả trong việc giải bàn Minesweeper.



Thời gian chạy trung bình càng thấp cho thấy solver xử lý càng nhanh. Số bước trung bình và số cờ trung bình giúp mô tả hành vi của solver trong quá trình chơi.



Trong project này, phần đánh giá giúp chứng minh rằng solver có thể chơi nhiều bàn Minesweeper khác nhau và tạo ra các chỉ số đo lường rõ ràng về hiệu năng.



