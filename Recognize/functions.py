# functions.py
import cv2
import numpy as np

def weighted(value):
    standard = 10
    return int(value * (standard / 10))

def threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image

def camera_threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 10)
    return image

def closing(image):
    kernel = np.ones((weighted(5), weighted(5)), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

def get_number(note):
    mapping = {
        'C4': '3/5', 'D4': '5/5', 'E4': '7/5', 'F4': '8/5', 'G4': '10/5',
        'A4': '12/5', 'B4': '14/5', 'C5': '15/5', 'D5': '17/5', 'E5': '19/5',
        'F5': '20/5'
    }

    return mapping.get(note, "해당 문자열에 대한 숫자가 없습니다.")

def convert_to_sentence(mapped_result_list):
    memorize_index = []
    sen = ""

    note_mapping = {
        'Treble': ('\ntabstave notation=true clef=treble\nnotes', 0),
        'Quarter Note': (' :q ', 0.25),
        'Half Note': (' :h ', 0.5),
        'Dotted Quarter Note': (' :qd ', 0.375),
        'Eight Note': (' :8 ', 0.125),
        'Whole Note': (' :w ', 1),
        'Quarter Rest': (' :4 ##', 0.25)
    }

    for result in mapped_result_list:
        k = 0  # 각 result 리스트마다 k 값을 초기화
        for i in range(len(result)):
            action, value = note_mapping.get(result[i][0], ('', 0))
            if k == 1:
                memorize_index.append([i])
                sen += " |"
                k = 0

            sen += action
            if result[i][0] not in ['Treble', 'Quarter Rest']:
                sen += get_number(result[i][1])
            k += value

    sen += " =|="
    return sen