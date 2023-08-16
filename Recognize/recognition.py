# recognition.py
import os
import cv2
import numpy as np
import functions as fs

def pitch_matching(stave_info, recognition_info):
    for stave in stave_info