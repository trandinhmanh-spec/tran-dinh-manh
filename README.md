# 🔥 Hệ Thống Cảnh Báo Cháy Nổ (Fire & Smoke Detection System)

Đây là một ứng dụng Web trực quan được xây dựng bằng **Python (Flask)** kết hợp với mô hình trí tuệ nhân tạo **YOLO** (thông qua Ultralytics) để nhận diện và cảnh báo cháy nổ (lửa và khói) theo thời gian thực từ luồng camera.

## 🌟 Tính năng nổi bật
- **Dashboard trực quan**: Theo dõi camera trực tiếp và nhận cảnh báo ngay lập tức.
- **Cảnh báo thời gian thực**: Tự động phát hiện khói và lửa, hiển thị tỷ lệ tin cậy (confidence) và phát âm thanh cảnh báo.
- **Quản lý lịch sử**: Xem lại các sự kiện cảnh báo đã được lưu lại kèm theo hình ảnh chụp tự động.
- **Thống kê**: Biểu đồ báo cáo chi tiết về tình hình sự cố.
- **Giao diện hiện đại**: Thiết kế Dark mode, Glassmorphism cực kỳ chuyên nghiệp và thân thiện với người dùng.

## 🚀 Hướng dẫn cài đặt và chạy dự án

### Yêu cầu hệ thống
- Máy tính có cài đặt sẵn **Python 3.8+**.
- Khuyến nghị nên có Card đồ họa (GPU) để mô hình AI xử lý mượt mà hơn, tuy nhiên vẫn có thể chạy trên CPU bình thường.

### Các bước thực hiện

**1. Clone kho lưu trữ về máy (hoặc tải mã nguồn)**
```bash
git clone https://github.com/trandinhmanh-spec/tran-dinh-manh.git
cd tran-dinh-manh
```

*(Nếu thư mục làm việc của bạn là `FireSmokeDetection`, hãy truy cập vào thư mục đó).*

**2. Tạo môi trường ảo (Tùy chọn nhưng khuyến nghị)**
Điều này giúp các thư viện của dự án không bị xung đột với các ứng dụng khác trên máy bạn.
```bash
python -m venv venv
```
Kích hoạt môi trường ảo:
- Trên **Windows**: `venv\Scripts\activate`
- Trên **macOS/Linux**: `source venv/bin/activate`

**3. Cài đặt các thư viện cần thiết**
Cài đặt toàn bộ các packages được yêu cầu thông qua `requirements.txt`:
```bash
pip install -r requirements.txt
```

**4. Khởi chạy hệ thống**
Khởi động máy chủ Flask:
```bash
python app.py
```

**5. Sử dụng Hệ thống**
- Mở trình duyệt web và truy cập: [http://localhost:5000](http://localhost:5000)
- Đăng nhập bằng tài khoản mặc định:
  - **Tên đăng nhập**: `admin`
  - **Mật khẩu**: `123456`

---

## 🛠️ Công nghệ sử dụng
- **Backend**: Python, Flask, SQLAlchemy, Flask-Login.
- **AI/Computer Vision**: YOLOv8 (Ultralytics), OpenCV, PyTorch.
- **Frontend**: HTML, CSS (Glassmorphism), Vanilla JavaScript.
- **Database**: SQLite (cho cơ sở dữ liệu `database.db`).

## 📄 Ghi chú
- Nếu bạn gặp lỗi khi khởi động Camera, hãy kiểm tra lại kết nối của Webcam hoặc chỉnh sửa luồng camera (`src=0` thành đường dẫn RTSP hoặc index của camera khác) trong mã nguồn.
- Mô hình nhận diện mặc định được thiết lập là `yolov8n.pt`. 
