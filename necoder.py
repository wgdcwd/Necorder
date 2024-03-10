import cv2 as cv
import numpy as np
import random

target_format = "avi"
target_fourcc = "XVID"
target_file = "record" + "." + target_format

video = cv.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")

isRecord = False
isNega = False
isNegaOn = False

if video.isOpened() :
    target = cv.VideoWriter()
    fps = video.get(cv.CAP_PROP_FPS)
    if fps > 60 :
        fps = 60
    wait_msec = int(1 / fps * 1000)

    while True :
        valid, img = video.read()
        isNega = random.choice([True, False])
        if isNega == True :
            if isNegaOn : 
                img = 255 - img
        h,w,*_ = img.shape
        is_color = (img.ndim > 2) and (img.shape[2] > 1)
        if isRecord == False : 
            cv.imshow("Video Player", img)
            key = cv.waitKey(wait_msec)
            if key == ord(" ") :
                isRecord = True
                target.open(target_file, cv.VideoWriter_fourcc(*target_fourcc), fps, (w, h), is_color)
            elif key == 27 :
                break
            elif key == ord("n") :
                isNegaOn = not isNegaOn

        elif isRecord == True:
            cv.circle(img, (20,20), radius=10, color=(0, 0, 255), thickness=2)
            
            target.write(img)
            cv.imshow("Video Player", img)
            key = cv.waitKey(wait_msec)
            if key == ord(" ") :
                target.release()
                isRecord = False
            elif key == 27 :
                break
            elif key == ord("n") :
                isNegaOn = not isNegaOn
            
    
    cv.destroyAllWindows()
