import cv2
from ultralytics import YOLO
import math

def main():
    # 1. Khởi tạo mô hình tốt nhất vừa train xong
    print("Đang tải mô hình...")
    model = YOLO("runs/detect/train-5/weights/best.pt")

    # 2. Khởi động Camera Laptop (OpenCV)
    # Số 0 thường đại diện cho camera mặc định của laptop
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Lỗi: Không thể mở được webcam!")
        return

    print("Webcam đã bật. Nhấn phím 'q' trên bàn phím để thoát.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Không thể đọc được khung hình từ webcam.")
            break

        # Lật ngược ảnh theo chiều ngang (như soi gương) để dễ nhìn hơn
        frame = cv2.flip(frame, 1)

        # 3. Đưa khung hình vào YOLOv8 để xử lý
        results = model(frame, stream=True, verbose=False)

        # 4. Vẽ Bounding Box
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Lấy tọa độ x1, y1, x2, y2 của Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Lấy độ tự tin (Confidence) và ép kiểu sang phần trăm
                conf = math.ceil((box.conf[0] * 100)) / 100
                conf_percent = int(conf * 100)

                # Lấy tên Class (Lửa hoặc Khói)
                cls = int(box.cls[0])
                class_name = model.names[cls]

                # Tùy chỉnh màu sắc (B, G, R)
                if class_name.lower() == 'fire':
                    color = (0, 0, 255) # Đỏ
                    display_name = "Fire"
                else:
                    color = (255, 0, 0) # Xanh dương
                    display_name = "Smoke"

                # Vẽ khung hình chữ nhật
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Viết text hiển thị: "Fire 96%" hoặc "Smoke 91%"
                text = f"{display_name} {conf_percent}%"
                
                # Làm nền cho text để dễ đọc hơn
                t_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(frame, (x1, y1), c2, color, -1)
                cv2.putText(frame, text, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 5. Hiển thị lên màn hình
        cv2.imshow("Kiem thu Webcam - Nhan dien Chay No (YOLOv8)", frame)

        # Nhấn phím 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng camera và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
