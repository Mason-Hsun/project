import numpy as np
import cv2
import os
import time
import utils
import threading
import sys
from datetime import datetime
class RC4:
    def __init__(self, save_directory):
        self.initial_key = "04070e5d02b9155a16034f9b02a0776c"
        self.iteration_count = 0
        self.key_written = False
        self.save_directory = save_directory
        # 追蹤已處理的檔案名稱
        self.processed_files = set()
    
    def logistic_map_counter_mode(self, key_hex, num_iterations, iteration_count):
        key_binary = bin(int(key_hex, 16))[2:]
        x0 = int(key_binary[:48], 2) / 2**48
        mu = (int(key_binary[47:111], 2) * 4) / (2**64)
        i0 = int(key_binary[112:128], 2)
        Q = 65535
        counter = i0
        result = []

        for _ in range(num_iterations):
            x_n = ((mu * x0 * (1 - x0)) * counter) % 1
            result.append(int(2**24 * x_n))
            counter = (counter % Q) + 1
            x0 = x_n
        return result

    def generate_key(self):
        num_iterations = 65536
        key_stream = self.logistic_map_counter_mode(self.initial_key, num_iterations, self.iteration_count)
        self.iteration_count += 1
        self.initial_key = hex(int(self.initial_key, 16) + 1)[2:]

        # 新增以下兩行以輸出當前金鑰值，僅在第一次呼叫時輸出
        if self.iteration_count == 1:
            current_key = self.initial_key
            print(f"Current Key: {current_key}")

        return key_stream

    def modify_filename(self, filepath):
        extension = filepath.split('.')[-1]
        new_filename = filepath.split('.')[0] + '_encryption.' + extension
        return new_filename
    
    def RC4_img(self, filepath):
        now = datetime.now()
        if not self.key_written:
            key_stream = self.generate_key()
            self.key_written = True
        else:
            key_stream = self.generate_key()

        output_image_path = self.modify_filename(filepath)
    
        frame = cv2.imread(filepath)
        height = frame.shape[0]
        weight = frame.shape[1]
        channels = frame.shape[2]
        i = 0
        for row in range(height):
            for col in range(weight):
                for c in range(channels):
                    frame[row, col, c] = frame[row, col, c] ^ int(key_stream[i % len(key_stream)])
                    i += 1
        print("Encryption photos\n")
        # 保存加密後的圖片
        cv2.imwrite(output_image_path, frame)


    def run(self):
        while True:
            if not os.path.exists(self.save_directory) or len(os.listdir(self.save_directory)) == 0:
                time.sleep(1)
                continue
            # 獲取目錄中的所有文件
            files = os.listdir(self.save_directory)
            # 過濾出照片文件
            image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg')) and file not in self.processed_files and "encryption" not in file]
            if image_files:
                # 取第一張照片進行加密
                uploaded_image_path = os.path.join(self.save_directory, image_files[0])

                # 加密並保存加密後的圖片
                self.RC4_img(uploaded_image_path)

                # 將已處理檔案名稱加入集合
                self.processed_files.add(image_files[0])
            else:
                pass
    def start_thread(self):
        thread1 = threading.Thread(target=self.run)
        thread1.start()
