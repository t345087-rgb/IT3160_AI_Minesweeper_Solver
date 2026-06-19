# Hướng dẫn Demo Project "AI Minesweeper Solver"

## 1. Giới thiệu
Project **AI Minesweeper Solver** xây dựng một tác tử AI có khả năng chơi và giải trò chơi Minesweeper. AI sử dụng suy luận logic và đánh giá xác suất để đưa ra các quyết định tối ưu. Project bao gồm giao diện dòng lệnh (CLI) và giao diện người dùng đồ họa (GUI) để tương tác và đánh giá solver.

## 2. Chuẩn bị môi trường và Cài đặt

### Yêu cầu
*   **Hệ điều hành:** Linux, macOS, hoặc Windows.
*   **Python:** Phiên bản 3.10 trở lên.
*   **pip:** Trình quản lý gói của Python.
*   **Git:** Để clone repository.

### Các bước cài đặt
1.  **Clone repository:**
    ```bash
    git clone https://github.com/t345087-rgb/IT3160_AI_Minesweeper_Solver.git
    cd IT3160_AI_Minesweeper_Solver
    ```

2.  **Cài đặt project:**
    ```bash
    python -m pip install -e .
    ```
    Lệnh này sẽ cài đặt tất cả các dependencies cần thiết (bao gồm `PySide6` cho GUI và `rich` cho CLI) và thiết lập các entry point `minesweeper` (CLI) và `minesweeper-gui` (GUI).

## 3. Các lệnh để chạy Project

### 3.1. Chạy CLI (Command Line Interface)

*   **Chạy Demo mặc định (9x9, 10 mìn, 30 bước):**
    ```bash
    python -m minesweeper
    ```
    hoặc
    ```bash
    minesweeper
    ```

*   **Chạy Demo với độ khó Beginner (9x9, 10 mìn):**
    ```bash
    minesweeper --difficulty beginner
    ```

*   **Chạy Demo với độ khó Expert (16x30, 99 mìn):**
    ```bash
    minesweeper --difficulty expert
    ```

*   **Chạy Evaluation (100 ván, mặc định Beginner):**
    ```bash
    minesweeper --evaluate --games 100
    ```

*   **Chạy Evaluation độ khó Intermediate (16x16, 40 mìn, 100 ván):**
    ```bash
    minesweeper --evaluate --difficulty intermediate --games 100
    ```

### 3.2. Khởi chạy GUI (Graphical User Interface)

```bash
minesweeper-gui
```
Thao tác này sẽ mở cửa sổ ứng dụng GUI của Minesweeper.

## 4. Hướng dẫn Demo AI giải bàn cờ (GUI)

1.  **Khởi chạy GUI:** Mở terminal và chạy lệnh `minesweeper-gui`.
2.  **Chọn độ khó:** Trên `Control Panel` ở phía trên, chọn một độ khó từ dropdown (ví dụ: "Medium").
3.  **Thay đổi tốc độ (tùy chọn):** Điều chỉnh "Delay" trong `Solver Speed` để kiểm soát tốc độ AI thực hiện mỗi bước (mặc định 100ms).
4.  **Bắt đầu Solver:** Nhấn nút "Start Solver". AI sẽ bắt đầu chơi tự động.
5.  **Quan sát:**
    *   Các ô sẽ tự động được mở hoặc cắm cờ.
    *   Màn hình sẽ hiển thị trạng thái hiện tại của bàn cờ.
    *   Status bar ở dưới cùng sẽ cập nhật số mìn, số cờ đã cắm và số ô đã mở trong thời gian thực.
    *   Khi game kết thúc (thắng hoặc thua), một cửa sổ thông báo sẽ hiện lên.
6.  **Dừng Solver:** Nhấn nút "Stop Solver" để tạm dừng AI bất cứ lúc nào.
7.  **Chơi ván mới:** Nhấn nút "New Game" trên `Control Panel` hoặc chọn `File -> New Game` để bắt đầu một ván chơi mới.

## 5. Luồng Demo Đề xuất (3-5 phút)

1.  **(0-0:30 giây) Giới thiệu:**
    *   Giới thiệu ngắn gọn về project "AI Minesweeper Solver" và mục tiêu của nó (giải Minesweeper bằng AI logic và xác suất).
    *   Nhấn mạnh 2 giao diện: CLI và GUI.

2.  **(0:30-1:30 phút) Demo CLI (nhanh):**
    *   Mở terminal, chạy demo một ván game mặc định: `minesweeper`
    *   Chạy một ví dụ evaluation nhỏ: `minesweeper --evaluate --difficulty beginner --games 5`
    *   Giải thích nhanh các số liệu hiển thị (Win Rate, Avg Steps, Avg Guesses).

3.  **(1:30-3:30 phút) Demo GUI (trọng tâm):**
    *   Khởi chạy GUI: `minesweeper-gui`
    *   Giải thích các thành phần chính: `Board View`, `Control Panel` (Difficulty, Speed, Buttons), `Status Bar`.
    *   Chọn độ khó "Medium".
    *   Nhấn "Start Solver" và để AI chơi.
    *   Trong khi AI chơi, giải thích các hành động của AI:
        *   Suy luận logic để tìm ô an toàn/mìn chắc chắn.
        *   Sử dụng xác suất khi cần đoán (nếu AI phải đoán, sẽ thấy ô đó được mở).
        *   Cập nhật số liệu trên Status Bar.
    *   Đảm bảo AI hoàn thành game (thắng hoặc thua) và thông báo hiện lên.

4.  **(3:30-5:00 phút) Các tính năng nổi bật & Hỏi đáp:**
    *   **Logic AI:** Khả năng suy luận deterministic và xác suất.
    *   **Tương tác người dùng:** Có thể click thủ công để chơi cùng AI (nếu muốn).
    *   **Mở rộng:** Dễ dàng thêm các chiến lược solver mới hoặc độ khó tùy chỉnh.
    *   Mở rộng phần GUI để highlight các ô đang được xử lí bởi AI.
    *   Mở rộng phần CLI để hỗ trợ các tuỳ chọn sâu hơn.
    *   **Kiểm thử:** Đề cập đến hệ thống kiểm thử tự động với `pytest`.
    *   Mời hỏi đáp.

## 6. Các tính năng chính cần làm nổi bật

*   **Bộ giải thông minh:** AI không chỉ đoán ngẫu nhiên mà sử dụng logic và xác suất.
*   **Hai giao diện:** Người dùng có thể chọn CLI để chạy nhanh hoặc GUI để quan sát trực quan.
*   **Khả năng mở rộng:** Cấu trúc module rõ ràng cho phép dễ dàng mở rộng.
*   **Đánh giá định lượng:** Có thể đo lường hiệu suất AI bằng các chỉ số rõ ràng.
*   **Đa dạng độ khó:** Hỗ trợ nhiều cấu hình bàn chơi.

## 7. Các vấn đề thường gặp và cách khắc phục nhanh

*   **"command not found: minesweeper" hoặc "command not found: minesweeper-gui"**:
    *   **Khắc phục:** Đảm bảo bạn đã chạy `python -m pip install -e .` thành công và môi trường Python của bạn được cấu hình đúng để nhận diện các script đã cài đặt (đảm bảo thư mục `~/.local/bin` hoặc tương đương có trong PATH).
*   **GUI không mở hoặc báo lỗi PySide6**:
    *   **Khắc phục:** Kiểm tra lại cài đặt PySide6: `python -m pip install PySide6`. Đảm bảo không có xung đột môi trường Python.
*   **AI mắc kẹt/không tìm thấy nước đi an toàn**:
    *   **Giải thích:** Trong một số trường hợp phức tạp, đặc biệt là ở độ khó cao, AI có thể hết nước đi an toàn và phải đoán, hoặc thậm chí không tìm được nước đi nào. Điều này mô phỏng hành vi của con người trong các tình huống 50/50.
*   **Kết quả evaluation khác với `README.md`**:
    *   **Giải thích:** Kết quả có thể thay đổi nhẹ tùy theo phiên bản Python, thư viện, seed ngẫu nhiên và hiệu suất phần cứng. `README.md` đã đề cập đến điều này.

## 8. Gợi ý Screenshot/Recording

*   **CLI Demo:** Chụp màn hình hoặc quay ngắn cảnh chạy `minesweeper` và `minesweeper --evaluate`.
*   **GUI Demo:** Quay lại toàn bộ quá trình AI giải một bàn cờ ở độ khó "Medium" hoặc "Hard", làm nổi bật các bước AI mở ô, cắm cờ và cập nhật status bar.