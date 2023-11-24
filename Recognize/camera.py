#기울어진 오선에 대한 보정 camera.py
import os
import numpy as np
import cv2
import functions as fs
import modules

# 이미지를 읽어옵니다.
resource_path = os.getcwd() + "/resources/"
src = cv2.imread(resource_path+"music.jpg")
dst = src.copy()
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
length = src.shape[1]
canny = cv2.Canny(gray, 5000, 1500, apertureSize = 5, L2gradient = True)
lines = cv2.HoughLinesP(canny, 0.9, np.pi / 180, 90, minLineLength = length*0.70, maxLineGap = 100) # 우리가 탐색할 선은 오선이므로 이미지의 70%이상인 선을 가지고 있으면 오선으로 간주

# 모든 선의 기울기를 계산하고 평균을 구합니다.
angles = []
for line in lines:
    line = line[0]
    angle = np.arctan2(line[3] - line[1], line[2] - line[0]) * 180. / np.pi
    if(angle>=0): # 직선 무시 일반적인 악보는 기울기가 0.0이기때문
        angles.append(angle)
avg_angle = np.mean(angles)

# 이미지의 중심을 기준으로 회전 변환 행렬을 계산합니다.
h, w = src.shape[:2]
center = (w / 2, h / 2)
M = cv2.getRotationMatrix2D(center, avg_angle, 1)
rotated = cv2.warpAffine(src, M, (w, h))

image_0 = fs.camera_threshold(rotated)


# 결과를 출력합니다.
cv2.imshow('result', image_0)
cv2.waitKey(0)
cv2.destroyAllWindows()