#hsv_controles
'''controles para ajustar cores com identificacao de documentos pequenos e desenha um retângulo ao redor do doc
(fundo amarelo de papel EVA)'''
import cv2 as cv
import numpy as np

video_chroma = cv.VideoCapture('videos/chroma1.mp4')


def nothing(x):
    pass

cv.namedWindow("Regulagens")
cv.createTrackbar("min_h", "Regulagens", 0, 180, nothing)
cv.createTrackbar("min_s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("min_v", "Regulagens", 0, 255, nothing)

cv.createTrackbar("max_h", "Regulagens", 0, 180, nothing)
cv.createTrackbar("max_s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("max_v", "Regulagens", 0, 255, nothing)
count = 0
ret, frame1 = video_chroma.read()
img_cortada = np.ndarray(shape=frame1.shape, dtype=int, order='F')

while video_chroma.isOpened():

    min_h = cv.getTrackbarPos("min_h", "Regulagens")
    min_s = cv.getTrackbarPos("min_s", "Regulagens")
    min_v = cv.getTrackbarPos("min_v", "Regulagens")

    max_h = cv.getTrackbarPos("max_h", "Regulagens")
    max_s = cv.getTrackbarPos("max_s", "Regulagens")
    max_v = cv.getTrackbarPos("max_v", "Regulagens")

    sucesso, frame_cam = video_chroma.read()
    frame_cam = cv.resize(frame_cam, (300, 400))
    frame_cam_hsv = cv.cvtColor(frame_cam, cv.COLOR_BGR2HSV)
    frame_cam_blur = cv.blur(frame_cam_hsv, (5, 5), 5)

    lower = np.array([min_h, min_s, min_v])
    upper = np.array([max_h, max_s, max_v])
    mask = cv.inRange(frame_cam_blur, lower, upper)
    mask_inv = cv.bitwise_not(mask)
    imagem_com_mascara = cv.bitwise_and(frame_cam, frame_cam, mask=mask_inv)

    objetos, lx = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for objeto in objetos:
        x, y, w, h = cv.boundingRect(objeto)
        if 5000 < cv.contourArea(objeto) < 15000:
            print(len(objetos))
            img_cortada = frame_cam[y:y + h, x:x + w]
            cv.rectangle(frame_cam, (x, y), (x+w, h+y), (255, 0, 0, 0.2), 2)

    image = cv.resize(img_cortada, (img_cortada.shape[1], img_cortada.shape[0]))
    cv.imwrite("frames/frame%d.jpg" % count, image)
    count += 1
    cv.imshow("mask_inv", mask_inv)
    cv.imshow("imagem_com_mascara", imagem_com_mascara)
    cv.imshow("frame_cam", frame_cam)

    if cv.waitKey(5) == 27:
        break

cv.destroyAllWindows()
video_chroma.release()