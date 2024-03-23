import os
import cv2
import time
import utils
import numpy as np
from camera_control import CameraObject
from transfer import FileSender
from encryption import RC4 
import multiprocessing
from ultralytics import YOLO
from datetime import datetime
from filterpy.kalman import KalmanFilter
class TrashTracker:
    def __init__(self, save_directory):
        self.photo_index = 1
        self.confidence_threshold = 0.7
        self.save_directory = save_directory
        # Get model
        self.model = YOLO(os.path.join(os.getcwd(), "s7.pt"))
        self.model_h = YOLO(os.path.join(os.getcwd(), "h.pt"))
        self.count = 0
        # Kalman filter
        self.dt = 1.0
        self.kf = self.initialize_kalman_filter()
        self.prev_center = None
        utils.make_dir(self.save_directory)
        
    def initialize_kalman_filter(self):
        kf = KalmanFilter(dim_x=4, dim_z=2)
        kf.F = np.array([[1, self.dt, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, self.dt],
                         [0, 0, 0, 1]])
        kf.H = np.array([[1, 0, 0, 0],
                         [0, 0, 1, 0]])
        kf.R = np.diag([1.0, 1.0])
        kf.P *= 1e2
        return kf
    

    def run(self):
        try:
            camera = CameraObject()
            encypt = RC4(self.save_directory)
            transfer = FileSender(self.save_directory)
            transfer.start_thread()
            camera.start_control()
            encypt.start_thread()
            while camera.is_opened:
                success, frame = camera.capture_frame()
                if success:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    update_frame = self.process_frame(frame)
                    if update_frame is not None:
                        #cv2.imshow("Trash detected !!", update_frame)
                        #cv2.destroyAllWindows()
                        camera.save_photo(update_frame, self.save_directory)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    print("Failed to capture photo")
            camera_control_thread.join()
            camera.close_camera()
        except Exception as e:
            pass
                
    def process_frame(self, frame):
        results = self.model(frame, self.confidence_threshold)
        for r in results:
            for i, (x1, y1, x2, y2) in enumerate(r.boxes.xyxy):
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                update_frame = self.detect_trash(frame, center_x, center_y, x1, y1, x2, y2)
                if update_frame is not None:
                    return update_frame
        
    def detect_trash(self, frame, center_x, center_y, x1, y1, x2, y2):
        self.kf.predict()
        z = np.array([center_x, center_y])
        self.kf.update(z)
        pred_state = self.kf.x
        cv2.rectangle(frame,
            (int(pred_state[0] - (x2 - x1) // 2), int(pred_state[2] - (y2 - y1) // 2)),
            (int(pred_state[0] + (x2 - x1) // 2), int(pred_state[2] + (y2 - y1) // 2)),
            (0, 255, 0), 2
        )

        label = f"X: {int(pred_state[0])}, Y: {int(pred_state[2])}, Class: huang-zi-yu"
        cv2.putText(frame, label, 
            (int(pred_state[0]), int(pred_state[2]) - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA
        )
        update_frame = None
        if self.prev_center is not None:
            displacement = np.sqrt((center_x - self.prev_center[0]) ** 2 + (center_y - self.prev_center[1]) ** 2)
            speed_threshold = 5
            if displacement > speed_threshold:
                time.sleep(1)
                return self.detect_persion(frame)
            else:
                return None
        else:
            self.prev_center = (center_x, center_y)
            return None       
        
    def detect_persion(self, frame):
        results_h = self.model_h(frame)
        for r_h in results_h:
            for j, (x1_h, y1_h, x2_h, y2_h) in enumerate(r_h.boxes.xyxy):
                cv2.rectangle(frame,
                              (int(x1_h), int(y1_h)),
                              (int(x2_h), int(y2_h)),
                              (255, 0, 0), 2)
                cv2.putText(frame, "Class: huang-zi-yu", (int(x1_h), int(y1_h) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        return frame
