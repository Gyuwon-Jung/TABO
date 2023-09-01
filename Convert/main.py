import cv2
import os
import modules
import numpy as np
import functions as fs

def weighted(value):
    standard = 10
    return int(value * (standard / 10))

def closing(image):
    kernel = np.ones((weighted(5), weighted(5)), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

# 이미지 불러오기
resource_path = os.getcwd() + "/resources/"

# 모든 이미지 파일에 대해 반복
for i in range(1, 1715):  # 1 (1)에서 1 (1714)까지
    # 이미지 파일 경로 설정
    image_filename = os.path.join(resource_path, f"1 ({i}).png")
    image_0 = cv2.imread(image_filename)

    # 1. 보표 영역 추출 및 그 외 노이즈 제거
    image_1, subimages_array = modules.remove_noise(image_0)

    # 2. 오선 제거
    image_2, staves = modules.remove_staves(image_1)

    # 3. 악보 이미지 정규화
    image_3, staves = modules.normalization(image_2, staves, 10)

    # 오선 제거된 분할 이미지와 오선 정보에 대해 정규화 수행
    normalized_images = []

    for subimage_coords in subimages_array:
        x, y, w, h = subimage_coords
        subimage = image_0[y:y+h+10, x:x+w+10] # 분할 좌표를 찾아 이미지화 margin을 10px 줬음 안그러면 템플릿 매칭때 오류 발생.
        subimage = fs.threshold(subimage) # 그레이스케일 후 이진화
        normalized_image, stave_info = modules.remove_staves(subimage) # 오선 제거
        normalized_image, stave_info = modules.normalization(normalized_image, stave_info, 10) # 정규화

        # 4. 객체 검출 과정
        closing_image = closing(normalized_image)
        cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기

        # 디렉토리를 생성하여 객체를 저장할 경로 설정
        output_directory = os.path.join(os.getcwd(), "object_images")
        os.makedirs(output_directory, exist_ok=True)

        for j in range(1, cnt):
            (x, y, w, h, area) = stats[j]

            # 객체 추출
            object_image = normalized_image[y:y + h, x:x + w]
            result_subimg = cv2.bitwise_not(object_image)

            # 객체를 이미지로 저장 (파일 이름은 일련번호로 설정)
            object_filename = os.path.join(output_directory, f"object_{i}_{j}.png")
            cv2.imwrite(object_filename, result_subimg)

            # 완료 메시지 출력
            print(f"이미지 {i}, 객체 {j} 저장 완료")

        #     # 원본 이미지에 객체 경계 상자 그리기
        #     cv2.rectangle(normalized_image, (x, y), (x + w, y + h), (255, 0, 0), 1)
        #
        # # 이미지 띄우기
        # cv2.imshow('result_subimage', normalized_image)
        # k = cv2.waitKey(0)
        # if k == 27:
        #     cv2.destroyAllWindows()
