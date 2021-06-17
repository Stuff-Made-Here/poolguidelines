import time

import cv2
import numpy as np
import pickle

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

count = 0

file = open("text.txt", "w")
file.write("Hello")
file.close()

time.sleep(2)




while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cv2.imshow("org", frame)

    if count < 1:
        #print(frame)
        # for a in frame:
        #     for b in a:
        #         print(b)
        file = open("text.txt", "w")
        myarr = frame.ravel()
        print(len(myarr))
        np.savetxt("text2.txt", myarr, newline=" ")

        #pickle.dump(tuple(frame), file)
        file.close()


    count+=1

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()