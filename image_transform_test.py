import cv2
import numpy as np


img = cv2.imread("testimage2.jpg")

width, height = 1920, 980

pts1 = np.float32([[20, 60], [1900, 45], [65, 1010], [1890, 960] ])
pts2 = np.float32([[0,0], [width,0], [0, height], [width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
print(matrix)
output = cv2.warpPerspective(img, matrix, (width, height))

#for x in range(0,4):
 #   cv2.circle(img,(pts1[x][0],pts1[x][1]),5,(0,0,255), cv2.FILLED)

# mask red color selection
upperRed = [0, 0, 255]
lowerRed = [120, 110, 218]
lowerRed = np.array(lowerRed, dtype="uint8")
upperRed = np.array(upperRed, dtype="uint8")

#mask blue color selection
lowerBlue = [255, 0, 0]
#upperBlue = [255, 191, 138]
upperBlue = [255, 216, 183]
lowerBlue = np.array(lowerBlue, dtype="uint8")
upperBlue = np.array(upperBlue, dtype="uint8")

maskBlue = cv2.inRange(output, lowerBlue, upperBlue)
maskRed = cv2.inRange(output, lowerRed, upperRed)
cv2.imshow("Red Mask", maskRed)
cv2.imshow("Blue Mask", maskBlue)
final = cv2.add(maskRed, maskBlue)
cv2.imshow("combined", final)

cv2.imshow("1", img)
cv2.imshow("2", output)
cv2.waitKey(0)