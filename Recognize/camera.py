#기울어진 오선에 대한 보정 camera.py
import os
import numpy as np
import cv2
import functions as fs
import modules

# 이미지를 읽어옵니다.
resource_path = os.getcwd() + "/resources/"
src = cv2.imread(resource_path+"rotate.jpg")
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
    if(angle>=0): # 세로 직선 무시 일반적인 악보는 기울기가 0.0이기때문
        angles.append(angle)
avg_angle = np.mean(angles)

# 이미지의 중심을 기준으로 회전 변환 행렬을 계산합니다.
h, w = src.shape[:2]
center = (w / 2, h / 2)
M = cv2.getRotationMatrix2D(center, avg_angle, 1)
rotated = cv2.warpAffine(src, M, (w, h))
#rotated = cv2.warpAffine(src, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(255,255,255)) #회전 이후 검은색 부분을 흰색으로 칠해주는 함수 지금은 threshold만 하면 해결

image = fs.camera_threshold(rotated)

cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
for i in range(1, cnt):
    x, y, w, h, area = stats[i]
    if w > image.shape[1] * 0.75:  # 보표 영역에만
        cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)  # 사각형 그리기

# 결과를 출력합니다.
cv2.imshow('result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()