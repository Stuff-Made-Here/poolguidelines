import psutil
import cv2
from time import time
import socket
from goprocam import GoProCamera, constants


# WRITE = False
# gpCam = GoProCamera.GoPro(constants.gpcontrol)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# t=time()
# gpCam.livestream("start")
# gpCam.video_settings(res='1080p', fps='30')
# gpCam.gpControlSet(constants.Stream.WINDOW_SIZE, constants.Stream.WindowSize.R720)
# cap = cv2.VideoCapture("udp://10.5.5.9:8554", cv2.CAP_FFMPEG)
# counter = 0
# while True:
#     nmat, frame = cap.read()
#     cv2.imshow("GoPro OpenCV", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     if time() - t >= 2.5:
#         sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
#         if WRITE == True:
#             cv2.imwrite(str(counter)+".jpg", frame)
#             counter += 1
#             if counter >= 10:
#                 break
#         t=time()
# # When everything is done, release the capture
# cap.release()
# cv2.destroyAllWindows()

import pyvirtualcam
import numpy as np

with pyvirtualcam.Camera(width=1280, height=720, fps=20) as cam:
    print(f'Using virtual camera: {cam.device}')
    frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
    while True:
        frame[:] = cam.frames_sent % 255  # grayscale animation
        cam.send(frame)
        cam.sleep_until_next_frame()