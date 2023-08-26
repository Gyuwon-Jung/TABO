import cv2
import os
import modules

def process_image(input_path, output_path):
    # 이미지 불러오기
    image_0 = cv2.imread(input_path)

    # 1. 보표 영역 추출 및 그 외 노이즈 제거
    image_1, subimages_array = modules.remove_noise(image_0)

    # 2. 오선 제거
    image_2, staves = modules.remove_staves(image_1)

    # 3. 악보 이미지 정규화
    image_3, staves = modules.normalization(image_2, staves, 10)

    result_img = cv2.bitwise_not(image_3)

    # 이미지 저장
    cv2.imwrite(output_path, result_img)

resource_path = os.getcwd() + "/resources/"
output_directory = os.path.join(os.getcwd(), "results")  # 결과 이미지를 저장할 디렉토리

# 결과 디렉토리가 없다면 생성
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 입력 이미지 파일들을 처리하고 결과를 저장
for i in range(126, 2066):  # 1부터 2065까지
    input_filename = f"1 ({i}).jpg"  # 형식에 맞는 이미지 파일 이름
    input_path = os.path.join(resource_path, input_filename)
    output_filename = f"result_{i}.jpg"  # 결과 파일 이름
    output_path = os.path.join(output_directory, output_filename)
    process_image(input_path, output_path)
    print(f"Processed image {i}")

print("Processing complete.")
