import numpy as np
import cv2

# 마우스 이벤트 콜백함수 정의
def mouse_callback(event, x, y, flags, param): 
    global coordinate_x, coordinate_y
    # 왼쪽 마우스 버튼이 클릭되었을 경우
    if event == cv2.EVENT_LBUTTONDOWN:
        # x,y(마우스) 좌표 저장
        coordinate_x = x
        coordinate_y = y

# haarcascades fontalface 경로 
face_cascade = cv2.CascadeClassifier('C:/tuk_term_project/haarcascade_frontalface_default.xml')
# tracker 설정
trackerKCF = cv2.TrackerKCF_create() 
# font 설정
font = cv2.FONT_ITALIC
# open video
cap = cv2.VideoCapture(0)

# 마우스 클릭 시 클릭 좌표 저장 변수
coordinate_x = 0
coordinate_y = 0

stop_flag = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
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
            stop_flag = 1

        # 마우스 좌표 변수 초기화
        coordinate_x = 0
        coordinate_y = 0

    # show frame(window)
    cv2.imshow("frame", frame)
    # mousecallback
    cv2.setMouseCallback('frame', mouse_callback)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    if stop_flag == 1:
        result = trackerKCF.init(frame, user_face)
        cv2.destroyAllWindows()
        break

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    isUpdated, trackObjectTuple = trackerKCF.update(frame) 
    if isUpdated: 
        x1 = (int(trackObjectTuple[0]) , int(trackObjectTuple[1]) ) 
        x2 = (int(trackObjectTuple[0] + trackObjectTuple[2]), int(trackObjectTuple[1] + trackObjectTuple[3])) 
        cv2.rectangle(frame, x1, x2, (255, 0, 0), 2) 
    cv2.imshow("track object", frame) 
    # cv2.imshow('roi_image', roi_img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break 
cap.release() 
cv2.destroyAllWindows()