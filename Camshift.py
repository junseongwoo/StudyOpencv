import numpy as np
import cv2 as cv

cap = cv.VideoCapture('./images/slow_traffic_small.mp4')

# 비디오의 프레임을 가져온다.
ret,frame = cap.read()

# 창의 초기 위치 설정
x, y, w, h = 300, 200, 100, 50 # 단순히 위치 값을 설정
track_window = (x, y, w, h)

# 추적을 위해 ROI 설정
roi = frame[y:y+h, x:x+w]
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# 종료 기준 설정, 10회 반복하거나 최소 1pt 이동해야함 
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )
while(1):
    ret, frame = cap.read()
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # camshift를 이용하여 새 위치를 얻음 
        ret, track_window = cv.CamShift(dst, track_window, term_crit)

        # 이미지에 그린다.
        pts = cv.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv.polylines(frame,[pts],True, 255,2)

        cv.imshow('img2',img2)
        k = cv.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break