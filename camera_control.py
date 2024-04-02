import os
import cv2 
import time
import pygame
import utils
import numpy as np
import trash_detect
import threading
from datetime import datetime
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

class CameraObject():
    def __init__(self):
        self.camera = None
        self.is_opened = None
        self.raw_capture = None 
        self.pigpio_factory = PiGPIOFactory()
        self.servo_lr = Servo(18, pin_factory=self.pigpio_factory)
        self.servo_ud = Servo(17, pin_factory=self.pigpio_factory)
        os.environ['PIGPIO_ADDR'] = '192.168.50.69'  
        os.environ['PIGPIO_PORT'] = '8888' 
        try:
            self.camera = cv2.VideoCapture(0)
            self.is_opened = self.camera.isOpened()
            print("PiCamera opened successfully")
        except picamera.exc.PiCameraError:
            print("Failed to open PiCamera")
            exit(1)
        except Exception as e:
            print("{}".format(e))
            exit(1)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
        
    
    def close_camera(self):
        self.camera.close()
        self.is_opened = False
        
        
    def capture_frame(self):
        success, frame = self.camera.read()
        if success:
            frame = cv2.resize(frame, (256, 256))
        return success, frame
    
    def save_photo(self, frame, save_directory):
        print("Save Image")
        time.sleep(0.5)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_index = len(os.listdir(save_directory)) + 1
        filename = "image{}_{}.png".format(timestamp, file_index)
        cv2.imwrite(os.path.join(save_directory, filename), frame)
        origin_image_dir = os.path.join(os.getcwd(),"not_encryption")
        utils.make_dir(origin_image_dir)
        cv2.imwrite(os.path.join(origin_image_dir,filename),frame)
        time.sleep(0.5)

    def control_servo(self):
        pygame.init()
        pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Servo Control")
        lr_step = 0.1  
        ud_step = 0.1  
        running = True
        while running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.servo_ud.value = min(self.servo_ud.value + ud_step, 1.0)
            elif keys[pygame.K_DOWN]:
                self.servo_ud.value = max(self.servo_ud.value - ud_step, -1.0)
            elif keys[pygame.K_LEFT]:
                self.servo_lr.value = min(self.servo_lr.value + lr_step, 1.0)
            elif keys[pygame.K_RIGHT]:
                self.servo_lr.value = max(self.servo_lr.value - lr_step, -1.0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()    
    
    def start_control(self):
        servo_control_thread = threading.Thread(target=self.control_servo)
        servo_control_thread.start()

