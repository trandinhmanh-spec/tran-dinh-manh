import time
import os

csv_file = r"C:\Users\Admin\Music\hệ thống nhận diện\FireSmokeDetection\runs\detect\train-5\results.csv"

def wait_for_epoch(target_epoch):
    while True:
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as f:
                lines = f.readlines()
                # filter out empty lines
                lines = [l.strip() for l in lines if l.strip()]
                if len(lines) > 1:
                    last_line = lines[-1]
                    epoch_str = last_line.split(',')[0].strip()
                    if epoch_str.isdigit():
                        current_epoch = int(epoch_str)
                        if current_epoch >= target_epoch:
                            print(f"Reached epoch {current_epoch}!")
                            return
        time.sleep(60)

if __name__ == "__main__":
    wait_for_epoch(20)
