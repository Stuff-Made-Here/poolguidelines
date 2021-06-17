import cv2
import numpy as np

def sort_contours(cnts, method="top-to-bottom"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
cap.set(cv2.CAP_PROP_FPS, 60)

width, height = 1920, 980
pts1 = np.float32([[20, 60], [1900, 45], [65, 1010], [1890, 960] ])
pts2 = np.float32([[0,0], [width,0], [0, height], [width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)

# mask red color selection
# lowerRed = [0, 0, 255]
# upperRed = [174, 166, 255]
# lowerRed = np.array(lowerRed, dtype="uint8")
# upperRed = np.array(upperRed, dtype="uint8")

#mask blue color selection
lowerBlue = [255, 0, 0]
upperBlue = [255, 216, 183]
lowerBlue = np.array(lowerBlue, dtype="uint8")
upperBlue = np.array(upperBlue, dtype="uint8")


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    output = cv2.warpPerspective(frame, matrix, (width, height))
    frame = output
    # Our operations on the frame come here



    # Red mask and Blue mask to detect the pool cue as a vector
    maskBlue = cv2.inRange(frame, lowerBlue, upperBlue)
    # maskRed = cv2.inRange(frame, lowerRed, upperRed)
    # final = cv2.add(maskRed, maskBlue)
    cv2.imshow("combined", maskBlue)

    res = cv2.bitwise_and(frame, frame, mask=maskBlue)
    cv2.imshow('res', res)
    #cv2.moveWindow('res', -1320, 350)

    ret, gray = cv2.threshold(maskBlue, 70, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('gray', gray)
    #cv2.moveWindow('gray', -1320, 700)

    ret2, thresh = cv2.threshold(gray, 127, 255, 1)
    cv2.imshow('thresh', thresh)
    #cv2.moveWindow('thresh', -720, 0)

    # im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cnts = []

    frame2 = frame.copy()
    print(len(contours))
    (cntsSorted,bnds) = sort_contours(contours)
    count = 0
    for c in cntsSorted:
        if count>1:
            break
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # point(c)=
        print(rect)
        box = np.int0(box)
        cv2.drawContours(frame2, [box], 0, (0, 0, 255), 1)
        cnts.append(c)
        # print(cv2.contourArea(c))
        count+=1

    # cv2.line(frame2, )
    cv2.imshow("stick frame",frame2)
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

        cv2.imshow('detected circles', frame)


    c = cv2.waitKey(1)
    if c == 27:
        break



cap.release()
cv2.destroyAllWindows()