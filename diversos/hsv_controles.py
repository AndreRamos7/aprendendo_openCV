#hsv_controles
'''controles para ajustar cores'''
import cv2 as cv
import numpy as np

video_cam = cv.VideoCapture(0)

def nothing(x):
    pass

cv.namedWindow("Regulagens")
cv.createTrackbar("min_h", "Regulagens", 0, 180, nothing)
cv.createTrackbar("min_s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("min_v", "Regulagens", 0, 255, nothing)

cv.createTrackbar("max_h", "Regulagens", 0, 180, nothing)
cv.createTrackbar("max_s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("max_v", "Regulagens", 0, 255, nothing)


while video_cam.isOpened():
    sucesso, frame_cam = video_cam.read()
    frame_cam_hsv = cv.cvtColor(frame_cam, cv.COLOR_BGR2HSV)

    min_h = cv.getTrackbarPos("min_h", "Regulagens")
    min_s = cv.getTrackbarPos("min_s", "Regulagens")
    min_v = cv.getTrackbarPos("min_v", "Regulagens")

    max_h = cv.getTrackbarPos("max_h", "Regulagens")
    max_s = cv.getTrackbarPos("max_s", "Regulagens")
    max_v = cv.getTrackbarPos("max_v", "Regulagens")

    lower = np.array([min_h, min_s, min_v])
    upper = np.array([max_h, max_s, max_v])
    mask = cv.inRange(frame_cam, lower, upper)

    cv.imshow("mascara", mask)
    cv.imshow("frame_camera", frame_cam)
    cv.imshow("frame_cam_hsv", frame_cam_hsv)

    if cv.waitKey(40) == 27:
        break

cv.destroyAllWindows()
video_cam.release()