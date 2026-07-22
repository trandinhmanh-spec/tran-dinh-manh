import cv2
import math
import time
import os
import json
from datetime import datetime
from ultralytics import YOLO

# Cooldown 5s to avoid spam
ALERT_COOLDOWN = 5.0

class VideoCamera:
    def __init__(self, alert_callback=None):
        self.model = YOLO("runs/detect/train-5/weights/best.pt")
        
        settings_file = 'settings.json'
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                config = json.load(f)
            cam_source = config.get("camera_source", "0")
        else:
            cam_source = "0"
            
        if cam_source.isdigit():
            cam_source = int(cam_source)
            
        self.video = cv2.VideoCapture(cam_source)
        self.alert_callback = alert_callback
        
        self.last_fire_alert = 0
        self.last_smoke_alert = 0
        
        # Đảm bảo thư mục lưu ảnh tồn tại
        self.alerts_dir = os.path.join("static", "alerts")
        if not os.path.exists(self.alerts_dir):
            os.makedirs(self.alerts_dir)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return b''

        frame = cv2.flip(frame, 1)
        clean_frame = frame.copy() # Bản sao sạch để lưu

        # YOLO xử lý
        results = self.model(frame, stream=True, verbose=False)
        current_time = time.time()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                conf_percent = int(math.ceil(box.conf[0] * 100))
                cls = int(box.cls[0])
                class_name = self.model.names[cls].lower()

                if class_name == 'fire':
                    color = (0, 0, 255)
                    display_name = "Fire"
                else:
                    color = (255, 0, 0)
                    display_name = "Smoke"

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{display_name} {conf_percent}%", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Kiểm tra cảnh báo (Hạ ngưỡng siêu nhạy xuống 50% cho bật lửa nhỏ)
                if conf_percent >= 50:
                    alert_triggered = False
                    alert_type = ""
                    
                    if class_name == 'fire' and (current_time - self.last_fire_alert > ALERT_COOLDOWN):
                        self.last_fire_alert = current_time
                        alert_type = "FIRE"
                        alert_triggered = True
                    elif class_name == 'smoke' and (current_time - self.last_smoke_alert > ALERT_COOLDOWN):
                        self.last_smoke_alert = current_time
                        alert_type = "SMOKE"
                        alert_triggered = True
                        
                    if alert_triggered and self.alert_callback:
                        # Lưu ảnh
                        file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        img_filename = f"alert_{alert_type}_{file_timestamp}.jpg"
                        img_path = os.path.join(self.alerts_dir, img_filename)
                        cv2.imwrite(img_path, clean_frame)
                        
                        # Gọi callback truyền dữ liệu lưu DB và gửi cho client
                        self.alert_callback(alert_type, conf_percent, f"alerts/{img_filename}")

        # Mã hoá frame thành JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return b''
        return jpeg.tobytes()
