#hsv_controles
'''identificacao de linhas em documentos pequenos e desenha uma linha  ao redor do doc
(fundo amarelo de papel EVA)'''
import math
import cv2 as cv
import numpy as np

video_chroma = cv.VideoCapture('../diversos/videos/chroma1.mp4')

def nothing(x):
    pass

cv.namedWindow("Regulagens")
cv.createTrackbar("min_canny", "Regulagens", 0, 255, nothing)
cv.createTrackbar("max_canny", "Regulagens", 0, 255, nothing)

ret, frame1 = video_chroma.read()
img_cortada = np.ndarray(shape=frame1.shape, dtype=int, order='F')

while video_chroma.isOpened():
    min_canny = cv.getTrackbarPos("min_canny", "Regulagens")
    max_canny = cv.getTrackbarPos("max_canny", "Regulagens")

    sucesso, frame_cam = video_chroma.read()
    frame_cam = cv.resize(frame_cam, (700, 800))
    gray = cv.cvtColor(frame_cam, cv.COLOR_BGR2GRAY)

    # Apply edge detection method on the image
    edges = cv.Canny(gray, min_canny, max_canny, apertureSize=3)
    lines = cv.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv.line(frame_cam, pt1, pt2, (0, 0, 255), 2, cv.LINE_AA)

    cv.imshow("frame_cam", frame_cam)

    if cv.waitKey(5) == 27:
        break

cv.destroyAllWindows()
video_chroma.release()