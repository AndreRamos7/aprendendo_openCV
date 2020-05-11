'''
identifica_objetos_ em escala de cinza
identifica oobetos brancos em fundo preto e desenha um círculo ao redor
'''
import cv2 as cv
import numpy as np

video_cap = cv.VideoCapture(0)
video_cap.set(3, 360)
video_cap.set(4, 640)
video_fps = int(video_cap.get(cv.CAP_PROP_FPS))

def nothing(x):
    pass

cv.namedWindow("Reguladores")
cv.resizeWindow("Reguladores", 360, 300)
cv.createTrackbar("minimo", "Reguladores", 0, 255, nothing)
cv.createTrackbar("maximo", "Reguladores", 0, 255, nothing)

cv.createTrackbar("area_minimo", "Reguladores", 0, 300, nothing)
cv.createTrackbar("area_maximo", "Reguladores", 0, 300, nothing)

while video_cap.isOpened():
    sucesso, frame = video_cap.read()
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    kernel = (5, 5)
    frame_blur = cv.GaussianBlur(frame_gray, kernel, 1)

    minino = cv.getTrackbarPos("minimo", "Reguladores")
    maximo = cv.getTrackbarPos("maximo", "Reguladores")

    area_minino = cv.getTrackbarPos("area_minino", "Reguladores")
    area_maximo = cv.getTrackbarPos("area_maximo", "Reguladores")

    lx, frame_thresh = cv.threshold(frame_gray, minino, maximo,  cv.THRESH_BINARY)

    bordas = cv.Canny(frame_thresh, minino, maximo)
    objetos, lx = cv.findContours(bordas, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    #cv.drawContours(frame, objetos, -1, (0, 255, 0), 3)

    for objeto in objetos:
        x, y, w, h = cv.boundingRect(objeto)
        if area_minino < cv.contourArea(objeto) < area_maximo:
            #continue
            print(len(objetos))
            cv.circle(frame, (x, y), int(h/2), (0, 255, 255), 1)
        #cv.rectangle(frame, (x, y), (x+w, h+y), (255, 0, 0, 0.2), 2)

    #uniao_frames = np.vstack([np.hstack([frame, frame_gray]),    np.hstack([frame_blur, frame_thresh])])

    cv.imshow("Janela com frame", frame)
    cv.imshow("Janela com bordas", bordas)
    cv.imshow("Janela com frame_thresh", frame_thresh)

    if cv.waitKey(video_fps) == 27:
        break

cv.destroyAllWindows()
video_cap.release()
