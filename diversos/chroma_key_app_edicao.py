#chroma_key_app
'''
este script é usado para teste/utilizacao em videos de chromaKey existentes na web
'''
import cv2 as cv
import numpy as np

video_ch_key = cv.VideoCapture('videos/fumaca.mp4')
video_camera = cv.VideoCapture(0)
_, frame1 = video_ch_key.read()
'''
video_FourCC = int(video_ch_key.get(cv.CAP_PROP_FOURCC))
video_fps = video_ch_key.get(cv.CAP_PROP_FPS)
video_size = (int(video_ch_key.get(cv.CAP_PROP_FRAME_WIDTH)), int(video_ch_key.get(cv.CAP_PROP_FRAME_HEIGHT)))

fourcc = cv.VideoWriter_fourcc(*'mjpg')
print(video_fps)
out = cv.VideoWriter("videos/output.avi", fourcc, 30.00, video_size)
'''
def nothing(x):
    pass

cv.namedWindow("Regulagens")
cv.resizeWindow("Regulagens", 360, 300)
cv.createTrackbar("min-h", "Regulagens", 0, 360, nothing)
cv.createTrackbar("min-s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("min-v", "Regulagens", 0, 255, nothing)

cv.createTrackbar("max-h", "Regulagens", 0, 390, nothing)
cv.createTrackbar("max-s", "Regulagens", 0, 255, nothing)
cv.createTrackbar("max-v", "Regulagens", 0, 255, nothing)
alpha = 0.5
beta = (1.0 - alpha)

while video_ch_key.isOpened():
    sucess, frame_camera = video_ch_key.read()
    frame_camera = frame_camera[:, ::-1]
    #frame_cam_gray = cv.cvtColor(frame_camera, cv.COLOR_BGR2GRAY)
    sucesso, frame_video = video_camera.read()
    #frame_camera_blur = cv.GaussianBlur(frame_camera, (15, 15), 25)
    #frame_video = frame_video[:, ::-1]

    #dst = cv.addWeighted(frame_camera, alpha, frame_video, beta, 0.0)

    frame_video = cv.resize(frame_video, (frame_camera.shape[1], frame_camera.shape[0]))
    frame_cam_hsv = cv.cvtColor(frame_camera, cv.COLOR_BGR2HSV)

    min_h = cv.getTrackbarPos("min-h", "Regulagens")
    min_s = cv.getTrackbarPos("min-s", "Regulagens")
    min_v = cv.getTrackbarPos("min-v", "Regulagens")

    max_h = cv.getTrackbarPos("max-h", "Regulagens")
    max_s = cv.getTrackbarPos("max-s", "Regulagens")
    max_v = cv.getTrackbarPos("max-v", "Regulagens")

    lower = np.array([min_v, min_s, min_h])#0, 0, 149
    upper = np.array([max_v, max_s, max_h])#270, 23, 255
    '''
    #parede
    lower = np.array([0, 0, 124])
    upper = np.array([286, 65, 255])
    
    #lencol
    lower = np.array([0, 0, 0])
    upper = np.array([312, 161, 255])
    '''
    mascara = cv.inRange(frame_cam_hsv, lower, upper)
    mascara_inv = cv.bitwise_not(mascara)

    imagem_com_mascara = cv.bitwise_and(frame_video, frame_video, mask=mascara)

    bg = cv.bitwise_and(frame_video, frame_video, mask=mascara)
    fg = cv.bitwise_and(frame_camera, frame_camera, mask=mascara_inv)

    merge = cv.add(bg, fg)
    video_save = cv.resize(merge.copy(), (640, 480))

    if sucess:
        #out.write(video_save)
        #cv.imshow("bg", bg)
        #cv.imshow("fg", fg)
        cv.imshow("merge", merge)
        '''cv.imshow("mascara", mascara)
        cv.imshow("frame_camera", frame_camera)
        cv.imshow("frame_cam_hsv", frame_cam_hsv)'''
        #cv.imshow("imagem_com_mascara", imagem_com_mascara)

        if cv.waitKey(1) == 27:
            break

cv.destroyAllWindows()
video_ch_key.release()