# Main.py
import cv2
import os
import modules

# 이미지 불러오기
resource_path = os.getcwd() + "/resource/"
image_0 = cv2.imread(resource_path + "music1.jpg")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1,subimages = modules.remove_noise(image_0)
print('보표')
print(subimages)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)
print('before')
print(staves)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 10)

result_img = cv2.bitwise_not(image_3)
print('after')
print(staves)

# 보표 영역 추출하여 띄우기
for idx, subimage_coords in enumerate(subimages):
    x, y, w, h = subimage_coords
    subimage = image_0[y:y+h, x:x+w]  # 정규화된 이미지에서 보표 영역 추출
    cv2.imshow(f'Subimage {idx+1}', subimage)  # 서브 이미지 번호 출력
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()

# 이미지 띄우기
cv2.imshow('result_image', result_img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()