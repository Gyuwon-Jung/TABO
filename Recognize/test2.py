import cv2
import os
import functions as fs
from Recognize import modules

# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"
image_0 = cv2.imread(resource_path + "music.jpg")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1, subimage = modules.remove_noise(image_0)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 10)

image_3 = cv2.bitwise_not(image_3)


cv2.imwrite(os.getcwd() + '/image.jpg', image_3)  # 현재 디렉토리에 'image.jpg'로 저장

# 이미지 띄우기
cv2.imshow('image', image_3)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()

