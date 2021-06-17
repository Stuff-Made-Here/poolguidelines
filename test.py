import cv2
import numpy as np


imgo = cv2.imread("testimage2.jpeg")

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
cap.set(cv2.CAP_PROP_FPS, 60)

width, height = 1920, 980

pts1 = np.float32([[20, 60], [1900, 45], [65, 1010], [1890, 960] ])
pts2 = np.float32([[0,0], [width,0], [0, height], [width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
print(matrix)




while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    output = cv2.warpPerspective(frame, matrix, (width, height))
    img = output
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    cv2.imshow("canny", edges)

    # lines = cv2.HoughLines(edges,1,np.pi/180,200)
    # for rho,theta in lines[0]:
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a*rho
    #     y0 = b*rho
    #     x1 = int(x0 + 1000*(-b))
    #     y1 = int(y0 + 1000*(a))
    #     x2 = int(x0 - 1000*(-b))
    #     y2 = int(y0 - 1000*(a))
    #
    #     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
    #
    # cv2.imwrite('houghlines3.jpg',img)
    minLineLength = 50
    maxLineGap = 15
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
    for x1, y1, x2, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imwrite('houghlines5.jpg', img)


    cv2.imshow("1", img)
    cv2.imshow("2", output)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()