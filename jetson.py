import socket
from _thread import *
import cv2
import numpy as np

#HOST = '172.30.1.63'
#HOST = "172.30.1.58"  # EH408
#HOST = "172.30.1.88"  # EH408
HOST = "172.30.1.63"  # EH408
PORT = 3333

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

## webcam 이미지 capture
cam = cv2.VideoCapture(0)

user_face = 0

start_flag = 0
 
### 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 293)
cam.set(4, 220)
 
## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]

# Tracking Flag
flag = 1000

# user_info flag
user_flag = 1

# Tracker create
trackerKCF = cv2.TrackerCSRT_create()

# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    global flag
    global user_face
    global user_flag

    while True:
        data = client_socket.recv(1024)
        try:
            sig = data.decode()
            print("recive : ",repr(data.decode()))
        except:
            continue
        
        if sig == "1":
            flag = 1

        elif sig == "2":
            flag = 2

        elif sig == "0":
            flag = 3

        else:
            if user_flag == 1:
                user_face = tuple(map(int, sig.strip("()").split(",")))
                print(user_face)
                user_flag = 0
                flag = 2

        if (sig == 'w' and sig == 'e' and sig == 'r'
            and sig == 's' and sig == 'd' and sig == 'f'
            and sig == 'x' and sig == 'c' and sig == 'v'):
            pass


        
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

while True:
    if flag == 1:
        # 비디오의 한 프레임씩 읽는다.
        # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)

        # cv2.imencode(ext, img [, params])
        # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
        result, frame = cv2.imencode('.jpg', frame, encode_param)

        # frame을 String형태로 변환
        data = np.array(frame)
        stringData = data.tobytes()

        client_socket.sendall((str(len(stringData))).encode().ljust(16) + stringData)


    elif flag == 2:
        # 비디오의 한 프레임씩 읽는다.
        # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if start_flag == 0:
            trackerKCF.init(gray, user_face)
            start_flag = 1

        elif start_flag == 1:
            # 추적 객체 위치 업데이트
            isUpdated, trackObjectTuple = trackerKCF.update(gray) 
            if isUpdated: 
                x1 = (int(trackObjectTuple[0]) , int(trackObjectTuple[1]) ) 
                x2 = (int(trackObjectTuple[0] + trackObjectTuple[2]), int(trackObjectTuple[1] + trackObjectTuple[3])) 
                cv2.rectangle(frame, x1, x2, (255, 0, 0), 2) 

            # user가 frame에서 없어졌을 때, tracking이 더 이상 진행되지 않을 때
            else:
                flag = 0

            # 좌측 상단
            if int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) >= 0 and \
               int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 70 and \
               int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 30 and \
               int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 120:
                msg = "f"
                #print('right')
               
               
            elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) > 70 and \
                 int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 150 and \
                 int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 30 and \
                 int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 120:
                msg = "d"
                #print('forward')
           
            elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) > 150 and \
                 int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 220 and \
                 int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 30 and \
                 int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 120:
                msg = "s"
                #print('left')
               
            elif int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) >= 0 and \
                 int(trackObjectTuple[0] + (trackObjectTuple[2]/2)) <= 220 and \
                 int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) >= 0 and \
                 int(trackObjectTuple[1] + (trackObjectTuple[3]/2)) < 30:
                msg = "q"
                #print('stop')
            
            else:
                msg = "q"
                
            client_socket.sendall(msg.encode())
            cv2.imshow("track object", frame) 
            cv2.waitKey(1)

    elif flag == 3:
        cv2.destroyAllWindows()
        user_face = 0
        start_flag = 0
        user_flag = 1
        trackerKCF = cv2.TrackerCSRT_create()
        continue

    elif flag == 0:
        break

    else:
        continue
    
client_socket.close()

