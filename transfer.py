import os
import socket
import time
import threading
class FileSender:
    def __init__(self, local_dir):
        self.server_ip = "192.168.0.103" # pc ip
        self.server_port = 8888
        self.local_dir = local_dir

    def send_file(self, file_path):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.server_ip, self.server_port))

            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            client_socket.sendall(f"{file_name},{file_size}".encode())

            with open(file_path, 'rb') as file:
                for chunk in iter(lambda: file.read(1024), b''):
                    client_socket.sendall(chunk)

            print(f"File {file_name} sent success")
            os.remove(file_path)

        except Exception as e:
            print(f"錯誤：{e}")

        finally:
            client_socket.close()
    
    def get_encryption_images(self):
        files = os.listdir(self.local_dir)
        return files

    def run(self):
        while True:
            encryption_images = self.get_encryption_images()
            if len(encryption_images) == 0:
                time.sleep(10)
            else:
                for image in encryption_images:
                    self.send_file(os.path.join(self.local_dir, image))
                time.sleep(10)
            
            
    def start_thread(self):
        thread1 = threading.Thread(target=self.run)
        thread1.start()


