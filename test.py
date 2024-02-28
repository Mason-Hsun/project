import cv2

# 创建 VideoCapture 对象
cap = cv2.VideoCapture(1)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# 读取并显示图像的循环
while cap.isOpened():
    # 读取一帧
    ret, frame = cap.read()

    # 检查帧是否成功读取
    if not ret:
        print("Error: Could not read frame.")
        break

    # 显示图像
    cv2.imshow('Camera', frame)

    # 检查是否按下 'q' 键，如果是则退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头对象并关闭所有窗口
cap.release()
cv2.destroyAllWindows()

