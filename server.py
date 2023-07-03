import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from _thread import *
import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import *
import socket
import numpy as np

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

running = False
result = 0
start_flag = 0
stop_flag = 0

# haarcascades fontalface 경로 
face_cascade = cv2.CascadeClassifier('C:/jangbogo/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('C:/jangbogo/haarcascade_upperbody.xml')

# font 설정
font = cv2.FONT_ITALIC
# gopen video
cap = cv2.VideoCapture(0)

# 마우스 클릭 시 클릭 좌표 저장 변수
coordinate_x = 0
coordinate_y = 0

client_sockets = []

# 마우스 이벤트 콜백함수 정의
def mouse_callback(event, x, y, flags, param): 
    global coordinate_x, coordinate_y
    # 왼쪽 마우스 버튼이 클릭되었을 경우
    if event == cv2.EVENT_LBUTTONDOWN:
        # x,y(마우스) 좌표 저장
        coordinate_x = x
        coordinate_y = y

# socket에서 수신한 버퍼를 반환하는 함수
def recvall(sock, count):
    # 바이트 문자열
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def wait():
    global client_soc
    global start_flag
    global client_sockets

    host = "172.30.1.63"
    port = 3333
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print('server start')
    while True:
        client_soc, addr = server_socket.accept() # 접속대기

        if client_soc not in client_sockets:
            client_sockets.append(client_soc)
        
start_new_thread(wait, ())


def tracking_mode():
    global start_flag
    global coordinate_x, coordinate_y
    global stop_flag
    global client_soc
    global client_sockets
    global jetson_c
    global rpi_c

    if len(client_sockets) >= 2:
        jetson_c = client_sockets[0]
        rpi_c = client_sockets[1]

    while True:
        if start_flag == 1:
            length = recvall(jetson_c, 16)
            stringData = recvall(jetson_c, int(length))
            data = np.fromstring(stringData, dtype='uint8')
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            
            #convert color to gray
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # set parameter for cascade
            faces = face_cascade.detectMultiScale(gray, 1.3, 7)

            # find face
            # 얼굴이 검출되었다면 얼굴 위치에 대한 좌표 정보를 리턴받음.
            for(x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),1)
                cv2.putText(frame,"detected face",(x-5,y-5),font,0.5,(255,255,0),2)

                # 마우스 좌표가 얼굴 박스 안에 있을 때
                if x <= coordinate_x and coordinate_x <= x+w and y<=coordinate_y and coordinate_y<=y+h:
                    # user_face에 좌표정보 저장
                    user_face = x,y,w,h
                    user_face = str(user_face)
                    jetson_c.sendall(user_face.encode())
                    jetson_c.sendall("2".encode())

                    # while문 탈출을 위한 flag
                    stop_flag = 1
  
                # 마우스 좌표 변수 초기화
                coordinate_x = 0
                coordinate_y = 0

            # show frame(window)
            cv2.imshow("frame", frame)
            # mousecallback
            cv2.setMouseCallback('frame', mouse_callback)
            cv2.waitKey(1)

            if stop_flag == 1:
                # client에게 영상 정보 전달 멈추게 하는 신호
                cv2.destroyAllWindows()

                # 버퍼 한 번 비워 주기
                length = recvall(jetson_c, 16)
                stringData = recvall(jetson_c, int(length))

                # stop_flag = 0으로 init / start_flag 2로 init
                stop_flag = 0
                start_flag = 2

        elif start_flag == 2:
            data = jetson_c.recv(1024)
            print(data.decode())
            rpi_c.sendall(data)

        else:
            continue

start_new_thread(tracking_mode, ())


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
    ## 버튼
        btnT = QPushButton()    
        btnT.setText(' 트래킹 On/Off ')
        btnT.setFont(QFont('Times', 30))

    ## 라벨
        label = QLabel('신호 결과', self)
        label.setAlignment(Qt.AlignHCenter)

    ## 라벨
        self.label_result = QLabel(' ', self)

    ## 폰트 설정
        font = label.font()
        font.setPointSize(20)
        font.setFamily('Times New Roman')
        font.setBold(True)
        label.setFont(font)
        self.label_result.setFont(font)
        
    ## 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(btnT)
        vbox.addWidget(label)
        vbox.addWidget(self.label_result)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.setWindowTitle('Reimplementing event handler')
        self.setGeometry(200, 200, 800, 600)
        self.show()
        btnT.clicked.connect(self.Tracking)
      
        
    def Tracking(self):
        global running
        global start_flag
        global client_sockets
        global jetson_c
        global rpi_c

        flag = 0

        if len(client_sockets) >= 2:
            jetson_c = client_sockets[0]
            rpi_c = client_sockets[1]
            flag = 1

        if flag == 1:
            if running == True:
                running = False
                jetson_c.sendall("0".encode())
                rpi_c.sendall("0".encode())
                start_flag = 0
            else:
                running = True
                jetson_c.sendall("1".encode())
                rpi_c.sendall("1".encode())
                start_flag = 1
        
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            self.showFullScreen()
        elif e.key() == Qt.Key_N:
            self.showNormal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())