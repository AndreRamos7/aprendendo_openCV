'''
identifica_objetos_hsv
identifica locais parecidos com a cor dos olhos e desenha um círculo/retangulo ao redor
identifica pincel azul de quadro branco e desenha um círculo/retangulo ao redor
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
cv.resizeWindow("Reguladores", 360, 360)
cv.createTrackbar("min_h", "Reguladores", 0, 180, nothing)
cv.createTrackbar("min_s", "Reguladores", 0, 255, nothing)
cv.createTrackbar("min_v", "Reguladores", 0, 255, nothing)

cv.createTrackbar("max_h", "Reguladores", 0, 180, nothing)
cv.createTrackbar("max_s", "Reguladores", 0, 255, nothing)
cv.createTrackbar("max_v", "Reguladores", 0, 255, nothing)

cv.createTrackbar("area_minimo", "Reguladores", 0, 2000, nothing)
cv.createTrackbar("area_maximo", "Reguladores", 0, 2000, nothing)

while video_cap.isOpened():
    sucesso, frame = video_cap.read()
    kernel = (5, 5)
    frame_blur = cv.GaussianBlur(frame, kernel, 1)
    frame_hsv = cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)

    min_h = cv.getTrackbarPos("min_h", "Reguladores")
    min_s = cv.getTrackbarPos("min_s", "Reguladores")
    min_v = cv.getTrackbarPos("min_v", "Reguladores")

    max_h = cv.getTrackbarPos("max_h", "Reguladores")
    max_s = cv.getTrackbarPos("max_s", "Reguladores")
    max_v = cv.getTrackbarPos("max_v", "Reguladores")

    area_minino = cv.getTrackbarPos("area_minino", "Reguladores")
    area_maximo = cv.getTrackbarPos("area_maximo", "Reguladores")
    '''
    minimo = np.array([min_h, min_s, min_v], dtype='uint8')
    maximo = np.array([max_h, max_s, max_v], dtype='uint8')
     
    #celular?
    minimo = np.array([102, 172, 78], dtype='uint8')
    maximo = np.array([180, 255, 128], dtype='uint8')
    
    #mao
    minimo = np.array([0, 34, 130], dtype='uint8')
    maximo = np.array([20, 130, 230], dtype='uint8') #62, 78
    '''
    # olhos
    minimo = np.array([0, 0, 0], dtype='uint8')
    maximo = np.array([183, 100, 52], dtype='uint8')  # 62, 78

    #lx, frame_thresh = cv.threshold(frame_hsv, minimo, maximo, cv.THRESH_BINARY)

    frame_thresh = cv.inRange(frame_hsv, minimo, maximo)


    #bordas = cv.Canny(frame_thresh, minimo, maximo)
    objetos, lx = cv.findContours(frame_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #cv.drawContours(frame, objetos, -1, (0, 255, 0), 3)

    for objeto in objetos:
        x, y, w, h = cv.boundingRect(objeto)
        if area_minino < cv.contourArea(objeto) < area_maximo:
            #continue
            print(len(objetos))
            #cv.circle(frame, (x, y), int(h), (2, 255, 0), 2)
            cv.rectangle(frame, (x, y), (x+w, h+y), (255, 0, 0, 0.2), 2)

    #uniao_frames = np.vstack([np.hstack([frame, frame_gray]),    np.hstack([frame_blur, frame_thresh])])

    cv.imshow("Janela com frame", frame)
    cv.imshow("Janela com frame_thresh", frame_thresh)

    if cv.waitKey(video_fps) == 27:
        break

cv.destroyAllWindows()
video_cap.release()
