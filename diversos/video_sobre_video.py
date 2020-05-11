#video_sobre_video
import cv2 as cv
import numpy as np

cam = cv.VideoCapture(0)
'''cam.set(3, 1080)
cam.set(4, 2024)'''


while cam.isOpened():
    sucesso, imagem = cam.read()
    w = imagem.shape[1]
    h = imagem.shape[0]
    imagem_cortada = imagem[300:h-100, 300:w-100]
    imagem_cortada = cv.resize(imagem_cortada, (200, 180))

    w_c = imagem_cortada.shape[1]
    h_c = imagem_cortada.shape[0]

    imagem[150:150+h_c, 150: 150+w_c] = imagem_cortada

    fonte = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(imagem, "Andre", (15, 65), fonte, 2, (0, 0, 255), 3, cv.LINE_AA)

    cv.imshow("Imagem", imagem)

    if cv.waitKey(40) == 27:
        break

cv.destroyAllWindows()
cam.release()