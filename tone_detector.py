#############################
#       Get Skin Tone       #
#############################

from pickle import NONE
from colormath.color_objects import LabColor, HSVColor, sRGBColor
from colormath.color_conversions import convert_color

#from my module
from standards import warm_std_b, cool_std_b, lab_weight

class ToneDetector:
    
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

    def RGB_to_HSV(self, RGB): #H(0~360) S(0~1) V(0~1)
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
    
    def warm_or_cool(self, lab_b):
        warm_dist = 0 #웜과의 거리
        cool_dist = 0 #쿨과의 거리

        #피부, 입술, 눈동자 측정
        for i in range(5):
            warm_dist += abs(lab_b[i] - warm_std_b) * lab_weight[i]
            cool_dist += abs(lab_b[i] - cool_std_b) * lab_weight[i]
        
        #warm_dist > cool_dist면 cool
        #cool_dist > warm_dist면 warm
        if  warm_dist > cool_dist:
            self.skin_tone = 'cool'
        else:
            self.skin_tone = 'warm'

        return self.skin_tone

    # #그래프 출력용
    # def get_b(self, RGB):
    #     R = RGB[0]
    #     G = RGB[1]
    #     B = RGB[2]
        
    #     # RGB를 LAB로 변환
    #     rgb = sRGBColor(R, G, B, is_upscaled=True)
    #     lab = convert_color(rgb, LabColor)
    #     (l, a, b) = lab.get_value_tuple()
    #     Lab_color = [l, a, b]

    #     return b