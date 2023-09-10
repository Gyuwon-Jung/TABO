import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

import functions as fs
import modules

# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"
image_0 = cv2.imread(resource_path + "music1.jpg")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1, subimage = modules.remove_noise(image_0)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 10)


# 4. 윤곽선 검출
closing_image = fs.closing(image_3)
# 윤곽선 검출
contours, _ = cv2.findContours(closing_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# 각 객체에 대한 처리
for i, contour in enumerate(contours):
    # 각 객체의 외곽 사각형 구하기
    x, y, w, h = cv2.boundingRect(contour)
    if w >= fs.weighted(5) and h >= fs.weighted(5):
        # cv2.rectangle(image_3, (x, y), (x + w, y + h), (255, 0, 0), 1)

        # 객체의 ROI 추출
        object_roi = image_3[y - 2:y + h + 2, x - 2: x + w + 2]

        # 이미지의 높이와 너비를 가져옵니다.
        height, width = object_roi.shape

        # 수직 히스토그램을 저장할 배열을 생성합니다.
        histogram = np.zeros((height, width), np.uint8)

        # 각 열마다 픽셀 값이 255인 개수를 세어 수직 히스토그램을 생성합니다.
        for col in range(width):
            pixels = 0
            for row in range(height):
                pixels += (object_roi[row][col] > 0)
            for pixel in range(pixels):
                histogram[height - pixel - 1, col] = 255  # 히스토그램을 아래부터 채웁니다.
        # if i==45:
        #     # 이미지 띄우기
        #     cv2.imshow('object', object_roi)
        #     k = cv2.waitKey(0)
        #     if k == 27:
        #         cv2.destroyAllWindows()
        #     # 히스토그램을 Matplotlib을 사용하여 시각화합니다.
        #     plt.figure(figsize=(10, 5))
        #     plt.imshow(histogram, cmap='gray', aspect='auto')
        #     plt.title('Vertical Histogram')
        #     plt.xlabel('Column')
        #     plt.ylabel('Pixel Height')
        #     plt.colorbar()
        #     plt.show()

        # 각 열의 픽셀 값을 출력합니다.
        for col in range(width):
            column_pixels = np.where(object_roi[:, col] > 0)[0]
            print(f"Column {col}: {column_pixels}")

        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()

        # # 이미지 띄우기
        # cv2.imshow('histogram', histogram)
        # k = cv2.waitKey(0)
        # if k == 27:
        #     cv2.destroyAllWindows()
        # # 이미지 띄우기
        # cv2.imshow('object', object_roi)
        # k = cv2.waitKey(0)
        # if k == 27:
        #     cv2.destroyAllWindows()

        # 수직 히스토그램을 기반으로 음표의 기둥 개수 탐지
        note_pillar_count = 0
        threshold = 30  # 기둥으로 간주할 픽셀 개수의 임계값 (30개 이상인 열을 기둥으로 판단)
        max_duplicate_distance = 3  # 중복 검출을 허용할 최대 거리 (3px 이상 차이는 새로운 기둥으로 판단)

        previous_pillar_position = None

        for col in range(width):
            if np.count_nonzero(histogram[:, col]) >= threshold:
                # 이전 기둥의 위치가 없거나, 현재 기둥과의 거리가 최대 거리 이상이면 중복 검출로 처리
                if previous_pillar_position is None or abs(
                        col - previous_pillar_position) >= max_duplicate_distance:
                    note_pillar_count += 1
                previous_pillar_position = col

        # 결과 출력
        print(f"Object {i + 1} - 음표 기둥 개수: {note_pillar_count}")

        # 음표 기둥 개수를 이미지 상에 표시
        cv2.putText(image_3, f"{i+1}: {note_pillar_count} ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 이미지 띄우기
cv2.imshow('result_image', image_3)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
