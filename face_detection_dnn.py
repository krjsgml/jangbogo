import cv2
import numpy as np

# Haar Cascade 분류기 로드
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 웹캠 영상 캡처 객체 생성
cap = cv2.VideoCapture(0)

# DNN 모듈을 사용하여 GPU 가속 활성화
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'res10_300x300_ssd_iter_140000_fp16.caffemodel')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

while True:
    # 웹캠 영상 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # 얼굴 검출을 위해 BGR 이미지를 blob으로 변환
    blob = cv2.dnn.blobFromImage(frame, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))

    # DNN 모델을 사용하여 얼굴 검출 수행
    net.setInput(blob)
    detections = net.forward()

    # 검출된 얼굴에 사각형 그리기
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # 신뢰도 임계값 설정
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (x, y, w, h) = box.astype(int)
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

    # 영상 출력
    cv2.imshow('Webcam', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) == ord('q'):
        break

# 사용한 리소스 해제
cap.release()
cv2.destroyAllWindows()