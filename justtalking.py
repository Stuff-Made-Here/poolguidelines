import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)
cap.set(3, 1920)
cap.set(4, 1080)

fps = cap.get(cv2.CAP_PROP_FPS)
resx = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
resy = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(fps)
print(resx)
print(resy)

circledetect = 0

start_time = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Noise Reduction
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)
    #cv2.imshow("Noise Reduced", gray)

    diameterBall = 35
    radiusBall = int(round(diameterBall / 2))


    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 2 * radiusBall * 0.9,
                               minRadius=int(round(radiusBall * 0.8)),
                               maxRadius=int(round(radiusBall * 1.2)),
                               param1=60,
                               param2=20
                               )
    #print("--- Detecting Balls seconds ---" % (time.time() - start_time))

    circledetect += len(circles)

    average = circledetect/((time.time() - start_time))


    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            #circlect += 1
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 1, (0, 0, 255), 3)

        cv2.imshow('detected circles', frame)

    print(average)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()