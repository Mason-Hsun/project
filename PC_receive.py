import socket
import os
import utils
def receive_files(save_path, server_ip, server_port):
    # 建立Socket連線
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 綁定IP和Port
        server_socket.bind((server_ip, server_port))

        # 監聽連線
        server_socket.listen()

        print(f"Wait raspberry pi connecting...")

       
        client_socket, client_address = server_socket.accept()
        print(f"Connected by {client_address} ")

        while True:
            try:
                # 接收檔案名稱和大小
                file_info = client_socket.recv(1024).decode(errors='ignore')
                if not file_info:
                    break
                file_name, file_size = file_info.split(',')
                file_size = int(file_size)

                with open(os.path.join(save_path, file_name), 'wb') as file:
                    received_data = 0
                    while received_data < file_size:
                        data = client_socket.recv(1024)
                        if not data:
                            raise Exception("Connection reset by peer")
                        file.write(data)
                        received_data += len(data)

                print(f"File {file_name} receive success")

            except Exception as e:
                break  

    except Exception as e:
        pass

    finally:
        server_socket.close()

# 儲存資料夾路徑
save_path = os.getcwd()
utils.make_dir(save_path)

# 伺服器的IP和Port
server_ip = "192.168.0.103" # pc ip
server_port = 8888

# 執行接收檔案的函式
while True:
    receive_files(save_path, server_ip, server_port)
