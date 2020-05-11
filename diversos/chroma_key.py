#chroma_key
import cv2 as cv
import numpy as np

video_cam = cv.VideoCapture(0)
video = cv.VideoCapture('docs.mp4')

def nothing(x):
    pass

cv.namedWindow("Regulagens")
cv.createTrackbar("min-h", "Regulagens", 0, 360, nothing)
cv.createTrackbar("min-s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("min-v", "Regulagens", 0, 255, nothing)

cv.createTrackbar("max-h", "Regulagens", 0, 390, nothing)
cv.createTrackbar("max-s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("max-v", "Regulagens", 0, 255, nothing)


while video_cam.isOpened():
    sucess, frame_cam = video_cam.read()
    frame_cam_gray = cv.cvtColor(frame_cam, cv.COLOR_BGR2GRAY)
    sucesso, frame_video = video.read()
    frame_cam_blur = cv.GaussianBlur(frame_cam, (15, 15), 25)
    frame_video = cv.resize(frame_video, (frame_cam.shape[1], frame_cam.shape[0]))
    frame_cam_hsv = cv.cvtColor(frame_cam_blur, cv.COLOR_BGR2HSV)

    min_h = cv.getTrackbarPos("min-h", "Regulagens")
    min_s = cv.getTrackbarPos("min-s", "Regulagens")
    min_v = cv.getTrackbarPos("min-v", "Regulagens")

    max_h = cv.getTrackbarPos("max-h", "Regulagens")
    max_s = cv.getTrackbarPos("max-s", "Regulagens")
    max_v = cv.getTrackbarPos("max-v", "Regulagens")

    lower = np.array([min_h, min_s, min_v])#67, 100, 100
    upper = np.array([max_h, max_s, max_v])
    mascara = cv.inRange(frame_cam_hsv, lower, upper)
    #print(mascara)

    imagem_com_mascara = cv.bitwise_and(frame_video, frame_video, mask=mascara)

    cv.imshow("mascara", mascara)
    cv.imshow("frame_camera", frame_cam)
    cv.imshow("frame_cam_hsv", frame_cam_hsv)
    cv.imshow("imagem_com_mascara", imagem_com_mascara)

    if cv.waitKey(40) == 27:
        break

cv.destroyAllWindows()
video_cam.release()