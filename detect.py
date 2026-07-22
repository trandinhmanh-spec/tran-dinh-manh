from ultralytics import YOLO

model = YOLO("runs/detect/train-5/weights/best.pt")

results = model("test.jpg", save=True)
