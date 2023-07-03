import cv2 
trackerKCF = cv2.TrackerKCF_create() 
videoCapture = cv2.VideoCapture(0) 
for i in range(1): 
    # 5회 반복한다. 
    _, frameNDArray = videoCapture.read() 
    frameNDArray = cv2.flip(frameNDArray, 1)
    trackObjectTuple = cv2.selectROI("select", frameNDArray) # 추적할 객체를 마우스로 드래그해 선택하고 스페이스 키나 엔터 키를 누른다. 
    result = trackerKCF.init(frameNDArray, trackObjectTuple)

while True: 
    _, frameNDArray = videoCapture.read()
    frameNDArray = cv2.flip(frameNDArray, 1)
    # roi_img = frameNDArray[trackObjectTuple[1]:trackObjectTuple[1] + trackObjectTuple[3], trackObjectTuple[0]:trackObjectTuple[0] + trackObjectTuple[2]] 
    # y:y+h, x:x+w -------------------- x->0 y->1 w->2 h->3
    isUpdated, trackObjectTuple = trackerKCF.update(frameNDArray) 
    if isUpdated: 
        x1 = (int(trackObjectTuple[0]) , int(trackObjectTuple[1]) ) 
        x2 = (int(trackObjectTuple[0] + trackObjectTuple[2]), int(trackObjectTuple[1] + trackObjectTuple[3])) 
        cv2.rectangle(frameNDArray, x1, x2, (255, 0, 0), 2) 
    cv2.imshow("track object", frameNDArray) 
    # cv2.imshow('roi_image', roi_img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break 
videoCapture.release() 
cv2.destroyAllWindows()