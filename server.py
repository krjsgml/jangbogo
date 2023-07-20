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
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

video_capture = cv2.VideoCapture(0)

running = False
result = 0
start_flag = 0
stop_flag = 0

# haarcascades fontalface 경로 
face_cascade = cv2.CascadeClassifier('C:/tuk_term_project/haarcascade_frontalface_default.xml')

# font 설정
font = cv2.FONT_ITALIC

client_sockets = []

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

    host = '172.30.1.63'
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
        self.video_window = VideoWindow()
        self.video_window.show()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            self.showFullScreen()
        elif e.key() == Qt.Key_N:
            self.showNormal()


class VideoWindow(QMainWindow):
    def __init__(self):
        global start_flag
        global stop_flag
        global client_soc
        global client_sockets
        global jetson_c
        global rpi_c
        global running

        super(VideoWindow, self).__init__()

        # PyQt 창 설정
        self.setWindowTitle("Tracking")
        self.setGeometry(100, 100, 480, 360)

        # PyQt에서 동영상을 표시할 라벨 생성
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, 480, 360)

        # 마우스 클릭 위치 저장할 클래스 멤버 변수
        self.coordinate_x = 0
        self.coordinate_y = 0

        # 타이머 생성 및 연결
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)  # 타이머 주기 (1ms)

        self.image_label.mousePressEvent = self.mousePressEvent

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

    def update_frame(self):
        global start_flag
        global stop_flag
        global client_soc
        global client_sockets
        global jetson_c
        global rpi_c
        global off
        global running
        off = 1

        if start_flag == 1:
            off = 1
            # OpenCV에서 프레임 읽어오기
            try:
                length = recvall(jetson_c, 16)
                stringData = recvall(jetson_c, int(length))
            except:
                pass
            
            data = np.fromstring(stringData, dtype='uint8')
            frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #convert color to gray
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            roi_x = int(71.5)
            roi_y = int(55)
            roi_width = int(150)
            roi_height = int(110)

            roi = gray[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

            cv2.rectangle(frame,(roi_x,roi_y),(roi_x+roi_width,roi_y+roi_height),(255,0,0),2)
            cv2.putText(frame,"put your face in red box",(10,10),font,0.5 ,(255,255,0),1)

            # set parameter for cascade
            faces = face_cascade.detectMultiScale(roi, 1.3, 7)

            # find face
            # 얼굴이 검출되었다면 얼굴 위치에 대한 좌표 정보를 리턴받음.
            for(x,y,w,h) in faces:
                x = x+roi_x
                y = y+roi_y
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),1)
                cv2.putText(frame,"detected face",(x-5,y-5),font,0.5,(255,255,0),2)

                # 마우스 좌표가 얼굴 박스 안에 있을 때
                if x <= self.coordinate_x and self.coordinate_x <= x+w and \
                    y<=self.coordinate_y and self.coordinate_y<=y+h:
                    print("Mouse clicked at (x={}, y={})"\
                          .format(self.coordinate_x, self.coordinate_y))
                    # user_face에 좌표정보 저장
                    user_face = x,y,w,h
                    user_face = str(user_face)
                    jetson_c.sendall(user_face.encode())

                    # while문 탈출을 위한 flag
                    stop_flag = 1

                # 마우스 좌표 변수 초기화
                self.coordinate_x = 0
                self.coordinate_y = 0

            # show frame(window)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # 이미지를 라벨에 표시
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

            if stop_flag == 1:
                self.close()
                # client에게 영상 정보 전달 멈추게 하는 신호
                jetson_c.sendall("2".encode())

                # stop_flag = 0으로 init / start_flag 2로 init
                stop_flag = 0
                start_flag = 2

        elif start_flag == 0:
            if off == 1:
                self.close()
                off = 0

        elif start_flag == 2:
            try:
                data = jetson_c.recv(1024) 
                #print(data.decode())
                if data.decode() == '0':
                    start_flag = 0
                    running = False
                rpi_c.sendall(data)
            except:
                pass


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.coordinate_x = event.x()
            self.coordinate_y = event.y()
            self.coordinate_x = self.coordinate_x/480*293
            self.coordinate_y = self.coordinate_y/360*220
            print(self.coordinate_x, self.coordinate_y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())