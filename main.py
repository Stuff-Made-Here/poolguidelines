import cv2
import numpy as np

cap = cv2.VideoCapture(1)
cap.set(3, 1920)
cap.set(4, 1080)
cap.set(cv2.CAP_PROP_FPS, 60)

val = cap.get(cv2.CAP_PROP_MODE)
print(val)

width, height = 1920, 980
pts1 = np.float32([[20, 60], [1900, 45], [65, 1010], [1890, 960] ])
pts2 = np.float32([[0,0], [width,0], [0, height], [width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)

#mask blue color selection
lowerBlue = [255, 0, 0]
upperBlue = [255, 216, 183]
lowerBlue = np.array(lowerBlue, dtype="uint8")
upperBlue = np.array(upperBlue, dtype="uint8")

sensitivity = 15
lower_white = np.array([0, 0, 255-sensitivity])
upper_white = np.array([255, sensitivity, 255])


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    output = cv2.warpPerspective(frame, matrix, (width, height))
    frame = output

    # Our operations on the frame come here

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red mask and Blue mask to detect the pool cue as a vector
    maskBlue = cv2.inRange(hsv, lower_white, upper_white)
    cv2.imshow("maskBlue", maskBlue)

    res = cv2.bitwise_and(frame, frame, mask=maskBlue)
    cv2.imshow('res', res)
    cv2.moveWindow('res', -1320, 350)

    ret, gray = cv2.threshold(maskBlue, 70, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('gray', gray)
    cv2.moveWindow('gray', -1320, 700)

    ret2, thresh = cv2.threshold(gray, 127, 255, 1)
    cv2.imshow('thresh', thresh)
    cv2.moveWindow('thresh', -720, 0)

    # im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cnts = []

    frame2 = frame.copy()

    for c in contours:
        if cv2.contourArea(c) > 200: #and cv2.contourArea(c) < 60:
            # x, y, w, h = cv2.boundingRect(c)
            # cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # rect = cv2.minAreaRect(c)
            # box = cv2.boxPoints(rect)
            # print(box)
            # box = np.int0(box)
            cv2.drawContours(frame2, c, -1, (0, 255, 0), 2)
            cnts.append(c)
            #print(cv2.contourArea(c))

    print(len(cnts))
    #frame2 = frame.copy()
    #cv2.drawContours(frame2, cnts, -1, (0, 255, 0), 3)


    # ret, thresh = cv2.threshold(final, 127, 255, 240)
    # contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # #print(contours)
    # final2 = cv2.drawContours(final, contours, -1, (0, 255, 0), 10)
    # cv2.imshow("final", final2)

    #Cleaning Up Image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)

    #Finding Balls
    diameterBall = 35
    radiusBall = int(round(diameterBall / 2))
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 2 * radiusBall * 0.9,
                               minRadius=int(round(radiusBall * 0.8)),
                               maxRadius=int(round(radiusBall * 1.2)),
                               param1=60,
                               param2=20
                               )

    #Viewing Circles on Original Image
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 1, (0, 0, 255), 3)

        #imS = cv2.resize(frame,(2200,1600))
        cv2.imshow('detected circles', frame)
        cv2.imshow('detected circles 2', frame2)
        #cv2.resizeWindow('detected circles', 2200, 1600)
        cv2.moveWindow('detected circles', -1450, 50)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
