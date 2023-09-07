import cv2
import os
import numpy as np

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

# 4. 윤곽선 검출
closing_image = fs.closing(image_3)
# 윤곽선 검출
contours, _ = cv2.findContours(closing_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 이전 기둥의 위치를 저장할 변수
previous_pillar_position = None

# 각 객체에 대한 처리
for i, contour in enumerate(contours):
    # 각 객체의 외곽 사각형 구하기
    x, y, w, h = cv2.boundingRect(contour)
    if w >= fs.weighted(5) and h >= fs.weighted(5):
        cv2.rectangle(image_3, (x, y), (x + w, y + h), (255, 0, 0), 1)

        # 객체의 높이 계산
        object_height = h

        # 객체의 ROI 추출
        object_roi = image_3[y - 2:y + h + 2, x-2 : x + w + 2]

        # 수평 히스토그램 계산
        horizontal_histogram = np.sum(object_roi, axis=0) / 255

        # 수평 히스토그램을 기반으로 음표의 기둥 개수 탐지
        note_pillar_count = 0
        threshold = 28  # 기둥으로 간주할 픽셀 값의 임계값 (높이의 70% 이상인 픽셀)
        for value in horizontal_histogram:
            if value >= threshold:
                # 이전 기둥의 위치와 현재 기둥의 위치가 일정 거리 이상 차이나면 중복 검출로 간주
                if previous_pillar_position is None or abs(x - previous_pillar_position) > 3:
                    note_pillar_count += 1
                    previous_pillar_position = x

        # 결과 출력
        print(f"Object {i + 1} - 음표 기둥 개수: {note_pillar_count}")

        # 음표 기둥 개수를 이미지 상에 표시
        cv2.putText(image_3, f"object: {note_pillar_count}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 이미지 띄우기
cv2.imshow('result_image', image_3)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
