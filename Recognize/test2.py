import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

import functions as fs
import modules

# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"
image_0 = cv2.imread(resource_path + "music.jpg")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1, subimage = modules.remove_noise(image_0)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 10)

parent =image_3
src = parent.copy()
tmp = parent.copy()

roi = cv2.selectROI("Select ROI drag area!!!!!", src)
tar = tmp[roi[1] : roi[1] + roi[3], roi[0] : roi[0] + roi[2]]
h, w = tar.shape[:2]

while True:
    res = cv2.matchTemplate(src, tar, cv2.TM_CCOEFF_NORMED)
    _, maxv, _, maxloc = cv2.minMaxLoc(res)
    if maxv < 0.8:
        break
    print('maxv : ', maxv)
    print('maxloc : ', maxloc)
    x, y = maxloc
    cv2.rectangle(parent, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 0), -1)

cv2.imshow('p', parent)
cv2.waitKey()
cv2.destroyAllWindows()