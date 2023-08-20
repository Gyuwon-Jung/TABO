# main.py

import cv2
import os
import modules
import numpy as np
import functions as fs

subimages_array = []  # 서브 이미지 배열들을 저장할 리스트
stave_list=[] # 해당 악보의 모든 오선 정보를 담고 있는 리스트
# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"
image_0 = cv2.imread(resource_path + "music8.jpg")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1,subimages_array = modules.remove_noise(image_0)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 10)

# 오선 제거된 분할 이미지와 오선 정보에 대해 정규화 수행
normalized_images = []
for subimage_coords in subimages_array:
    x, y, w, h = subimage_coords
    subimage = image_0[y:y+h+10, x:x+w+10] #분할 좌표를 찾아 이미지화 margin을 10px 줬음 안그러면 템플릿 매칭때 오류 발생.
    subimage = fs.threshold(subimage) #그레이스케일 후 이진화
    normalized_image, stave_info = modules.remove_staves(subimage) #오선 제거
    normalized_image, stave_info = modules.normalization(normalized_image, stave_info, 10) # 정규화
    normalized_images.append((normalized_image))
    stave_list.append([stave_info])

result_img = cv2.bitwise_not(image_3)

# 템플릿 이미지 파일명과 해당 이미지에 표시될 텍스트들
template_data = [
{"file": "template\clef.png", "text": "Clef"},
{"file": "template\clef_2.png", "text": "Clef"},
{"file": "template\sharp.png", "text": "Sharp"},
{"file": "template\half_left.png", "text": "Half Note"},
{"file": "template\half_right.png", "text": "Half Note"},
{"file": "template\eight_flag.png", "text": "Eight_flag"},
{"file": "template\eight_flag_2.png", "text": "Eight_flag"},
{"file": "template\quarter_left.png", "text": "Quarter Note"},
{"file": "template\quarter_right.png", "text": "Quarter Note"},
{"file": "template\quarter_left_2.png", "text": "Quarter Note"},
{"file": "template\quarter_right_2.png", "text": "Quarter Note"},
{"file": "template\dot.png", "text": "Dot"},
{"file": "template\quarter_rest.png", "text": "Quater Rest Note"},
{"file": "template\whole_note.png", "text": "Whole Note"},

]

recognition_list = []

# 템플릿 매칭 및 결과 이미지에 음표와 텍스트 추가
for normalized_image in normalized_images:
    result_subimg = cv2.bitwise_not(normalized_image)

    # 각 subimage에 대한 processed_locations 리스트 초기화
    processed_locations = []

    for template_info in template_data:
        template_file = template_info["file"]
        template_text = template_info["text"]

        template_path = os.path.join(resource_path, template_file)
        template = cv2.imread(template_path)
        template = fs.threshold(template)
        result = cv2.matchTemplate(normalized_image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7

        locations = np.where(result >= threshold)
        for loc in zip(*locations[::-1]): #하나라도 검출 되었을때 중복 검출 방지 검사 반복문
            skip_location = False
            for processed_loc in processed_locations:
                distance = np.sqrt((loc[0] - processed_loc[0]) ** 2 + (loc[1] - processed_loc[1]) ** 2)
                if distance < 5:
                    skip_location = True
                    break

            if not skip_location:
                processed_locations.append([loc[0], loc[1], template_text, (loc[1] + loc[1] + template.shape[0]) / 2])
                cv2.rectangle(result_subimg, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]), (0, 0, 255),
                              2)
                # cv2.putText(result_img, f'{template_text} ({loc[0]}, {loc[1]})', (loc[0], loc[1] - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    processed_locations.sort(key=lambda entry: entry[0]) # x좌표 기준으로 정렬

    # # x, y 좌표 제거
    # processed_locations = [[entry[2], entry[3]] for entry in processed_locations]

    recognition_list.append(processed_locations)

    # 이미지 띄우기
    cv2.imshow('result_subimage', result_subimg)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()

# recognition_list의 모든 결과에 대해서 8분 음표로 바꾸기 및 Eight_Flag 정보 삭제
for result in recognition_list:
    i = 0
    while i < len(result) - 1:
        if result[i][2] == "Quarter Note" and result[i + 1][2] == "Eight_flag":
            result[i][2] = "Octa Note"
            del result[i + 1]  # Eight_Flag 정보 삭제

        elif result[i][2] == "Quarter Note" and result[i + 1][2] == "Dot": # 현재 음표 다음에 점이 존재할 경우
            result[i][2] = "Dotted Quarter Note"
            del result[i + 1]  # Dot 정보 삭제

        elif result[i][2] == "Half Note" and result[i + 1][2] == "Dot": # 현재 음표 다음에 점이 존재할 경우
            result[i][2] = "Dotted Half Note"
            del result[i + 1]  # Dot 정보 삭제

        else:
            i += 1

print(stave_list)

# 결과 확인
for result in recognition_list:
    print(result)


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