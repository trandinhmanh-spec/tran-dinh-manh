import cv2
import math
import time
import threading
import ctypes
import winsound
from datetime import datetime
from ultralytics import YOLO

# Cài đặt thời gian chờ (cooldown) giữa 2 lần cảnh báo liên tiếp (đơn vị: giây)
# Để tránh việc popup/chuông kêu liên tục mỗi mili-giây gây đứng máy
ALERT_COOLDOWN = 5.0 

# Biến lưu vết thời gian cảnh báo gần nhất
last_fire_alert = 0
last_smoke_alert = 0

def play_alarm_sound():
    """Phát âm thanh bíp lớn trên Windows"""
    # 1000 Hz, kéo dài 1000 mili-giây (1 giây)
    winsound.Beep(1000, 1000)

def show_warning_popup(message):
    """Hiển thị bảng Popup cảnh báo của Windows"""
    # 0x30 là icon Warning (dấu chấm than vàng)
    ctypes.windll.user32.MessageBoxW(0, message, "HỆ THỐNG CẢNH BÁO", 0x30 | 0x0)

def log_and_capture(frame, alert_type, conf):
    """Chụp ảnh, lưu file log thời gian và giả lập gửi Email"""
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # 1. Lưu log ra màn hình và file text
    log_msg = f"[{timestamp_str}] PHÁT HIỆN {alert_type} (Độ tin cậy: {conf}%)"
    print(log_msg)
    
    with open("alert_log.txt", "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")
        
    # 2. Chụp và lưu ảnh lại làm bằng chứng
    img_name = f"alert_{alert_type}_{file_timestamp}.jpg"
    cv2.imwrite(img_name, frame)
    print(f"--> Đã tự động lưu ảnh hiện trường: {img_name}")
    
    # 3. Tính năng nâng cao: Gửi Email (Ở đây ta in ra để mô phỏng)
    print(f"--> [Email Service] Đã gửi thông báo khẩn cấp tới admin@congty.com")
    print("-" * 50)

def main():
    global last_fire_alert, last_smoke_alert
    
    print("Đang khởi động hệ thống cảnh báo...")
    model = YOLO("runs/detect/train-5/weights/best.pt")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Lỗi: Không kết nối được Camera!")
        return

    print("Hệ thống ĐÃ BẬT. Nhấn phím 'q' để tắt.")

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        
        # Lưu riêng một khung hình sạch (chưa vẽ Bounding Box) để nếu có cháy thì chụp ảnh cho rõ
        clean_frame = frame.copy() 

        results = model(frame, stream=True, verbose=False)
        current_time = time.time()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                conf_percent = int(math.ceil(box.conf[0] * 100))
                cls = int(box.cls[0])
                class_name = model.names[cls].lower()

                # Vẽ khung lên màn hình (như giai đoạn 5)
                if class_name == 'fire':
                    color = (0, 0, 255)
                    display_name = "Fire"
                else:
                    color = (255, 0, 0)
                    display_name = "Smoke"
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{display_name} {conf_percent}%", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # ==========================================
                # GIAI ĐOẠN 6: XỬ LÝ LOGIC CẢNH BÁO (Hạ xuống >= 65%)
                # ==========================================
                if conf_percent >= 65:
                    
                    # NẾU LÀ LỬA (FIRE) -> Phát âm thanh, chụp ảnh, lưu thời gian
                    if class_name == 'fire' and (current_time - last_fire_alert > ALERT_COOLDOWN):
                        last_fire_alert = current_time
                        
                        # Dùng threading để phát âm thanh ngầm, không làm đứng/giật hình camera
                        threading.Thread(target=play_alarm_sound, daemon=True).start()
                        threading.Thread(target=log_and_capture, args=(clean_frame, "FIRE", conf_percent), daemon=True).start()
                        
                    # NẾU LÀ KHÓI (SMOKE) -> Hiện Popup, chụp ảnh, lưu thời gian
                    elif class_name == 'smoke' and (current_time - last_smoke_alert > ALERT_COOLDOWN):
                        last_smoke_alert = current_time
                        
                        popup_msg = f"CẢNH BÁO KHẨN CẤP:\nPhát hiện KHÓI với độ tin cậy {conf_percent}%!"
                        # Dùng threading để hiện popup ngầm
                        threading.Thread(target=show_warning_popup, args=(popup_msg,), daemon=True).start()
                        threading.Thread(target=log_and_capture, args=(clean_frame, "SMOKE", conf_percent), daemon=True).start()

        cv2.imshow("He Thong Canh Bao Chay No", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
