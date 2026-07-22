from ultralytics import YOLO

def main():
    # 1. Khởi tạo mô hình
    # 'yolov8n.pt' là phiên bản Nano (nhỏ nhất và nhanh nhất) của YOLOv8. 
    # Khi chạy lần đầu, nó sẽ tự động tải file trọng số cơ bản này từ trên mạng về.
    model = YOLO('yolov8n.pt') 

    # 2. Tiến hành huấn luyện (Train)
    print("Bắt đầu quá trình huấn luyện...")
    results = model.train(
        data='dataset/data.yaml',  # Đường dẫn tới file cấu hình chứa thông tin hình ảnh và nhãn
        epochs=30,                 # Số vòng lặp huấn luyện toàn bộ dữ liệu (càng lớn model học càng kỹ)
        imgsz=640,                 # Kích thước ảnh đầu vào (640x640 pixel là chuẩn của YOLO)
        device='cpu',              # Chạy bằng CPU. Nếu sau này bạn có Card đồ họa rời (GPU NVIDIA), hãy đổi thành '0' để chạy nhanh gấp chục lần.
        batch=16,                  # (Tuỳ chọn) Số lượng ảnh đưa vào máy học cùng 1 lúc, thường là 8 hoặc 16.
        name='my_fire_model'       # (Tuỳ chọn) Đặt tên thư mục lưu kết quả thay vì để mặc định là train, train-2...
    )

    # 3. Kết thúc
    print("Huấn luyện thành công!")
    print(f"File trọng số tốt nhất được lưu tại: {results.save_dir}/weights/best.pt")

# Đảm bảo code chạy an toàn trên Windows (bắt buộc phải có __main__)
if __name__ == '__main__':
    main()
