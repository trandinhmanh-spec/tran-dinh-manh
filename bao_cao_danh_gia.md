# Giai đoạn 4: Đánh giá mô hình

Như trong sơ đồ bạn cung cấp, YOLO đã xuất đầy đủ các thông số đánh giá vào thư mục `runs/detect/train-5`. Dưới đây là phân tích chi tiết các chỉ số dựa trên dữ liệu học của bạn:

## 1. Các chỉ số quan trọng (Metrics)
*(Lấy từ kết quả hoàn thiện của Epoch 30)*

- **Accuracy (Độ chính xác tổng thể - mAP50-95):** `42.73%` 
  *(Trong nhận diện vật thể YOLO, người ta dùng mAP làm đại diện cho Accuracy. Chỉ số này ở mức ổn đối với một mô hình mới train 30 epochs).*
- **Precision (Độ chuẩn xác):** `74.34%` 
  *(Ý nghĩa: Mỗi khi mô hình báo "Đây là đám cháy/khói", thì có tới 74.34% trường hợp đó thực sự là cháy/khói. Tỉ lệ nhận diện sai/báo động giả khá thấp).*
- **Recall (Độ phủ):** `68.03%` 
  *(Ý nghĩa: Giả sử trong khung hình có 100 đám cháy/khói, mô hình có khả năng tìm ra được 68 đám. Một vài đám cháy nhỏ hoặc bị che khuất có thể bị bỏ sót).*
- **mAP50:** `74.48%` 
  *(Chỉ số cực kỳ quan trọng, cho thấy khi áp dụng độ đo giao nhau chuẩn (IoU 50), độ chính xác của hệ thống rất tốt).*

## 2. Chọn mô hình sử dụng
> **Đã hoàn thành!** 
> Mô hình được chọn để tích hợp vào hệ thống nhận diện thực tế chính là file: **`runs/detect/train-5/weights/best.pt`**. (File `detect.py` hiện tại cũng đã được cập nhật để dùng đúng trọng số tốt nhất này).

---

## 3. Biểu đồ trực quan

### Ma trận nhầm lẫn (Confusion Matrix)
Biểu đồ này giúp bạn xem mô hình có bị nhầm lẫn giữa Lửa (Fire) và Khói (Smoke), hay nhầm lẫn với vật thể nền (Background) hay không. Đường chéo đậm chứng tỏ mô hình phân loại rất chính xác:

![Confusion Matrix](./runs/detect/train-5/confusion_matrix.png)

### Biểu đồ kết quả huấn luyện (Results)
Theo dõi sự sụt giảm của các chỉ số sai số (Loss) và sự tăng trưởng của hiệu năng (Metrics) mượt mà xuyên suốt 30 Epochs:

![Training Results](./runs/detect/train-5/results.png)
