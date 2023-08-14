# recognition.py
import os
import cv2
import numpy as np
import functions as fs

# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"

def analyze(image):
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

    recognition_list = []

    # 템플릿 매칭 및 결과 이미지에 음표와 텍스트 추가

    result_subimg = cv2.bitwise_not(image)

    # 각 subimage에 대한 processed_locations 리스트 초기화
    processed_locations = []

    for template_info in template_data:
        template_file = template_info["file"]
        template_text = template_info["text"]

        template_path = os.path.join(resource_path, template_file)
        template = cv2.imread(template_path)
        template = fs.threshold(template)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7

        locations = np.where(result >= threshold)
        for loc in zip(*locations[::-1]):  # 하나라도 검출 되었을때 중복 검출 방지 검사 반복문
            skip_location = False
            for processed_loc in processed_locations:
                distance = np.sqrt((loc[0] - processed_loc[0]) ** 2 + (loc[1] - processed_loc[1]) ** 2)
                if distance < 30:
                    skip_location = True
                    break

            if not skip_location:
                processed_locations.append(
                    (loc[0], loc[1], template_text, (loc[1] + loc[1] + template.shape[0]) / 2))
                cv2.rectangle(result_subimg, loc, (loc[0] + template.shape[1], loc[1] + template.shape[0]),
                              (0, 0, 255),
                              2)
                # cv2.putText(result_img, f'{template_text} ({loc[0]}, {loc[1]})', (loc[0], loc[1] - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    processed_locations.sort(key=lambda entry: entry[0])  # x좌표 기준으로 정렬
    recognition_list.append(processed_locations)

    # 이미지 띄우기
    cv2.imshow('result_subimage', result_subimg)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()


    return recognition_list
