# Main.py

import cv2
import os
import modules
import numpy as np
import functions as fs

subimages_array = []  # 서브 이미지 배열들을 저장할 리스트

# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"
image_0 = cv2.imread(resource_path + "music.jpg")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1 = modules.remove_noise(image_0)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)
print('before')
print(staves)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 10)

# result_img = image_3.copy()
result_img = cv2.bitwise_not(image_3)
print('after')
print(staves)

# 템플릿 이미지 파일명과 해당 이미지에 표시될 텍스트들
template_data = [
{"file": "template\clef.png", "text": "Clef"},
{"file": "template\sharp.png", "text": "Sharp"},
{"file": "template\half_left.png", "text": "Half Note"},
{"file": "template\half_right.png", "text": "Half Note"},
{"file": "template\eight_flag.png", "text": "Eight_flag"},
{"file": "template\quarter_left.png", "text": "Quarter Note"},
{"file": "template\quarter_right.png", "text": "Quarter Note"},
{"file": "template\on_rest.png", "text": "Rest Note"},
{"file": "template\whole_note.png", "text": "Whole Note"},

]

# 이미 처리한 위치를 저장하는 변수
processed_locations = []

# 각 템플릿 이미지에 대해 템플릿 매칭 수행
for template_info in template_data:
    template_file = template_info["file"]
    template_text = template_info["text"]

    template_path = os.path.join(resource_path, template_file)
    template = cv2.imread(template_path)
    template = fs.threshold(template)  # 그레이스케일 및 이진화

    result = cv2.matchTemplate(image_3, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7  # 매칭 결과의 유사도 임계값

    # 유사도가 임계값보다 높은 위치 찾기
    locations = np.where(result >= threshold)
    for loc in zip(*locations[::-1]):
        # 이미 처리한 위치 주변을 제외
        skip_location = False
        for processed_loc in processed_locations:
            distance = np.sqrt((loc[0] - processed_loc[0]) ** 2 + (loc[1] - processed_loc[1]) ** 2)
            if distance < 30:  # 이미 처리한 위치와의 거리가 일정 값 이하라면 skip
                skip_location = True
                break

        if not skip_location:
            # 이미 처리한 위치 목록에 추가
            processed_locations.append((loc[0], loc[1], template_text))  # 템플릿 텍스트도 저장

            # 음표를 사각형으로 표시
            cv2.rectangle(result_img, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]), (0, 0, 255), 2)

            # 텍스트 추가
            cv2.putText(result_img, f'{template_text} ({loc[0]}, {loc[1]})', (loc[0], loc[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

print(processed_locations)

# 이미지 띄우기
cv2.imshow('result_image', result_img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()

# # 이미지 띄우기
# cv2.imshow('result_image', result_img)
# k = cv2.waitKey(0)
# if k == 27:
#     cv2.destroyAllWindows()


# # 템플릿 생성용 이미지 저장 경로
# output_path = os.path.join(os.getcwd(), "result_image.jpg")
#
# # 이미지 저장
# cv2.imwrite(output_path, result_img)
# print(f"Result image saved at: {output_path}")