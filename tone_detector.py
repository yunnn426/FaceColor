#############################
#       Get Skin Tone       #
#############################

from pickle import NONE
import cv2
import numpy as np
from colormath.color_objects import LabColor, HSVColor, sRGBColor
from colormath.color_conversions import convert_color
import colorsys
from PIL import Image
import colorsys

#from my module
#from standards import warm_std_a, warm_std_b, cool_std_a, cool_std_b

#웜,쿨 기준 lab (b 사용)
warm_std_a = 5.43
warm_std_b = 18.66
cool_std_a = 5.82
cool_std_b = 15.98


class ImageAnalyzer:
    def __init__(self):
        self.skin_tone = None

    def RGB_to_LAB(self, RGB):
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]

        # RGB를 LAB로 변환
        rgb = sRGBColor(R, G, B, is_upscaled=True)
        lab = convert_color(rgb, LabColor)
        (l, a, b) = lab.get_value_tuple()
        Lab_color = [l, a, b]

        return Lab_color

    def RGB_to_HSV(self, RGB):
        R = RGB[0]
        G = RGB[1]
        B = RGB[2]
        
        # RGB를 HSV로 변환
        #rgb = sRGBColor(R / 255, G / 255, B / 255)
        rgb = sRGBColor(R, G, B, is_upscaled=True)
        hsv = convert_color(rgb, HSVColor)
        (h, s, v) = hsv.get_value_tuple()
        HSV = [h, s, v]

        return HSV

    #기준 lab값과의 차이를 비교해 톤 판단
    def examine_tone(self, face_part):
        a = face_part[1]
        b = face_part[2]
        warm_dist = 0
        cool_dist = 0

        
        #b값 비교
        warm_dist += abs(b - warm_std_b)
        cool_dist += abs(b - cool_std_b)
    
        #warm_dist > cool_dist면 cool
        #cool_dist > warm_dist면 warm
        if  warm_dist > cool_dist:
            self.skin_tone = 'cool'
        else:
            self.skin_tone = 'warm'

        return self.skin_tone

    #lab값으로 톤 판단
    def examine_tone_lab(self, face_part):
        a = face_part[1]
        b = face_part[2]
        print("a: ", a, " b: ", b) 

        # a > b인 경우 쿨톤, 그렇지 않은 경우 웜톤으로 판단
        if a > b:
            self.skin_tone = 'cool'
        else:
            self.skin_tone = 'warm'

        return self.skin_tone

    #hsv값으로 톤 판단
    def examine_tone_hsv(self, face_part):
        h = face_part[0]
        
        # Hue: 0~118) warm, 119~255) cool
        if h > 118:
            self.skin_tone = 'cool'
        else:
            self.skin_tone = 'warm'
        
        return self.skin_tone
    
    def analyze_image(self, rgb_arr):
        # 이미지 열기
        #img = Image.open(image_path)
        # 이미지의 평균 색상 계산
        avg_color = rgb_arr
        # 평균 색상을 LAB 및 HSV로 변환
        lab_color = self.RGB_to_LAB(avg_color)
        hsv_color = self.RGB_to_HSV(avg_color)
        #print("lab: ", lab_color)
        #print("hsv: ", hsv_color)
        # 피부톤 조사
        tone = self.examine_tone(lab_color)
        #tone = self.examine_tone_hsv(hsv_color)
        # 피부톤 반환
        return tone

 