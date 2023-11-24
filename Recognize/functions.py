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