import os
import cv2
import functions as fs
import numpy as np



# 이미지를 읽어옵니다.
resource_path = os.getcwd() + "/resources/"
src = cv2.imread(resource_path + "rotate.jpg")
dst = src.copy()

# 이미지를 흑백으로 변환합니다.
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 적응적인 이진화를 수행합니다.
adaptive_threshold = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,11,10)

# 적용된 적응적인 이진화를 컬러 이미지로 변환합니다.
adaptive_threshold_color = cv2.cvtColor(adaptive_threshold, cv2.COLOR_GRAY2BGR)

# 이미지를 화면에 표시하고 사용자가 아무 키나 누를 때까지 대기합니다.
cv2.imshow("Adaptive Thresholding", adaptive_threshold_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
