import os
import cv2 
import time
import pygame
import picamera
import numpy as np
from gpiozero import Servo
from datetime import datetime
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
            self.camera = picamera.PiCamera()
            self.camera.resolution = (1024, 768)
            self.is_opened = True
            self.camera.vflip = True
            self.raw_capture = picamera.array.PiRGBArray(self.camera)
            print("PiCamera opened successfully")
        except picamera.exc.PiCameraError:
            print("Failed to open PiCamera")
            exit(1)
        
        
    
    def close_camera(self):
        self.camera.close()
        self.is_opened = False
        
        
    def capture_frame(self):
        self.raw_capture.truncate(0)
        self.camera.capture(self.raw_capture, format="rgb", use_video_port=True)
        return True, self.raw_capture.array
    
    def save_photo(self, frame, save_directory):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_index = len(os.listdir(self.save_directory) + 1)
        filename = f"image{file_index}_{timestamp}.jpg"
        cv2.imwrite(os.path.join(save_directory, filename), frame)
    
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
            
       
        