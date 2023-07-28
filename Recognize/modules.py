# modules.py
import cv2
import numpy as np
import functions as fs

def remove_noise(image):
    # 1. 보표 영역 추출 및 그 외 노이즈 제거
    image = fs.threshold(image)  # 이미지 이진화
    mask = np.zeros(image.shape, np.uint8)  # 보표 영역만 추출하기 위해 마스크 생성

    # 외곽선 검출
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 보표를 사각형으로 표시
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # 사각형 크기 조정
        new_y = y - 10  # 위로 10px 이동
        new_h = h + 20  # 위아래로 10px씩 늘림

        if w > image.shape[1] * 0.5:  # 보표 영역에만
            # 새로운 사각형 좌표 계산
            new_x, new_y, new_w, new_h = x, new_y, w, new_h

            # 이미지 범위를 벗어나지 않도록 조정
            new_y = max(0, new_y)
            new_h = min(image.shape[0] - new_y, new_h)

            # 사각형 그리기
            cv2.rectangle(mask, (new_x, new_y, new_w, new_h), (255, 0, 0), -1)

    masked_image = cv2.bitwise_and(image, mask)  # 보표 영역 추출

    return masked_image

def remove_staves(image):
    height, width = image.shape
    staves = []  # 오선의 좌표들이 저장될 리스트

    for row in range(height):
        pixels = 0
        for col in range(width):
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 흰색 픽셀의 개수를 셈
        if pixels >= width * 0.5:  # 이미지 넓이의 50% 이상이라면
            if len(staves) == 0 or abs(staves[-1][0] + staves[-1][1] - row) > 1:  # 첫 오선이거나 이전에 검출된 오선과 다른 오선
                staves.append([row, 0])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:  # 이전에 검출된 오선과 같은 오선
                staves[-1][1] += 1  # 높이 업데이트

    for staff in range(len(staves)):
        top_pixel = staves[staff][0]  # 오선의 최상단 y 좌표
        bot_pixel = staves[staff][0] + staves[staff][1]  # 오선의 최하단 y 좌표 (오선의 최상단 y 좌표 + 오선 높이)
        for col in range(width):
            if image[top_pixel - 1][col] == 0 and image[bot_pixel + 1][col] == 0:  # 오선 위, 아래로 픽셀이 있는지 탐색
                for row in range(top_pixel, bot_pixel + 1):
                    image[row][col] = 0  # 오선을 지움

    return image, [x[0] for x in staves]

def normalization(image, staves, standard):
    avg_distance = 0
    lines = int(len(staves) / 5)  # 보표의 개수
    for line in range(lines):
        for staff in range(4):
            staff_above = staves[line * 5 + staff]
            staff_below = staves[line * 5 + staff + 1]
            avg_distance += abs(staff_above - staff_below)  # 오선의 간격을 누적해서 더해줌
    avg_distance /= len(staves) - lines  # 오선 간의 평균 간격

    height, width = image.shape  # 이미지의 높이와 넓이
    weight = standard / avg_distance  # 기준으로 정한 오선 간격을 이용해 가중치를 구함
    new_width = int(width * weight)  # 이미지의 넓이에 가중치를 곱해줌
    new_height = int(height * weight)  # 이미지의 높이에 가중치를 곱해줌

    image = cv2.resize(image, (new_width, new_height))  # 이미지 리사이징
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 이미지 이진화
    staves = [x * weight for x in staves]  # 오선 좌표에도 가중치를 곱해줌

    return image, staves