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

# 4. 레이블링을 사용한 검출
closing_image = fs.closing(image_3)
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기


# 모든 객체를 반복하며 (배경 제외)
for i in range(1, cnt):
    (x, y, w, h, area) = stats[i]

    # 작은 객체는 무시합니다 (필요에 따라 최소 크기 임계값을 조정하세요)
    if w < fs.weighted(5) or h < fs.weighted(5):
        continue

    # 객체의 ROI를 추출합니다
    object_roi = image_3[y - 2:y + h + 2, x - 2: x + w + 2]

    # 객체의 높이와 너비를 계산합니다
    height, width = object_roi.shape

    # 수직 히스토그램을 저장할 배열을 생성합니다
    histogram = np.zeros((height, width), np.uint8)

    # 각 열에 대한 수직 히스토그램을 계산합니다
    for col in range(width):
        pixels = np.count_nonzero(object_roi[:, col])
        histogram[height - pixels:, col] = 255  # 히스토그램을 아래부터 채웁니다

    # # 객체와 해당 수직 히스토그램을 표시합니다 (디버깅을 위해 이 조건을 조정할 수 있습니다)
    # if i == 45:
    #     # 객체를 표시합니다
    #     cv2.imshow('object', object_roi)
    #     k = cv2.waitKey(0)
    #     if k == 27:
    #         cv2.destroyAllWindows()
    #
    #     # Matplotlib을 사용하여 수직 히스토그램을 시각화합니다
    #     plt.figure(figsize=(10, 5))
    #     plt.imshow(histogram, cmap='gray', aspect='auto')
    #     plt.title('수직 히스토그램')
    #     plt.xlabel('열')
    #     plt.ylabel('픽셀 높이')
    #     plt.colorbar()
    #     plt.show()

    # 각 열의 픽셀 값을 출력합니다
    for col in range(width):
        column_pixels = np.where(object_roi[:, col] > 0)[0]
        print(f"열 {col}: {column_pixels}")

    # 수직 히스토그램을 기반으로 객체 내의 음표 기둥 개수를 계산합니다
    note_pillar_count = 0
    threshold = 30  # 열을 음표 기둥으로 간주할 임계값 (필요에 따라 조정하세요)
    max_duplicate_distance = 3  # 중복 기둥으로 간주할 최대 거리 (필요에 따라 조정하세요)

    previous_pillar_position = None

    for col in range(width):
        if np.count_nonzero(histogram[:, col]) >= threshold:
            # 이전 기둥이 없거나 현재 기둥과의 거리가 최대 거리 이상인 경우 중복으로 처리
            if previous_pillar_position is None or abs(col - previous_pillar_position) >= max_duplicate_distance:
                note_pillar_count += 1
            previous_pillar_position = col

    # 현재 객체의 결과를 출력합니다
    print(f"객체 {i + 1} - 음표 기둥 개수: {note_pillar_count}")

    # 이미지에 음표 기둥 개수를 표시합니다
    cv2.putText(image_3, f"{i+1}: {note_pillar_count} ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 음표 기둥 개수가 표시된 최종 결과 이미지를 표시합니다
cv2.imshow('result_image', image_3)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
