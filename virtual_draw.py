import cv2
import numpy as np
import time
import os
import handtrack as htm

################################
brushThick = 25
eraserThick = 100
drawColor = (255,0,255)
################################
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.65, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720,1280,3), np.uint8)
# print(type(imgCanvas))

while True:
     
    #import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList,_ = detector.findPosition(img, draw=False)
    # print(type(lmList))

    if len(lmList) != 0:
        #check ujung jari tengah & telunjuk
        # x1,y1 = lmList[8][1:]
        # x2,y2 = lmList[12][1:]
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #check jari
        fingers = detector.fingersUp()
        #2 jari naik == pilih warna
        if fingers[1] and fingers[2]:
            print('test1')
            if y1 < 125:
                if 250 < x1 < 450:
                    drawColor = (0,255,0)
                elif 550 < x1 < 750:
                    drawColor = (0,0,0)
                elif 1050 < x1 < 1200:
                    drawColor = (0,0,0)
                    imgCanvas = np.zeros((720,1280,3), np.uint8)
            cv2.rectangle(img, (x1,y1-25), (x2,y2+25), drawColor, cv2.FILLED)
        #1jari naik == drawing
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1,y1),15,drawColor,cv2.FILLED)
            print('draw')
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            cv2.line(img, (xp,yp),(x1,y1), drawColor, brushThick)
            cv2.line(imgCanvas, (xp,yp),(x1,y1), drawColor, brushThick)
            xp,yp = x1,y1

    imGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imGray, 50,255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    cv2.imshow("Image", img)
    cv2.imshow("canvas", imgCanvas)
    cv2.imshow("Inversion", imgInv)
    if cv2.waitKey(1) == 27: 
            break
cv2.destroyAllWindows()


