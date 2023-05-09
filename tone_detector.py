#############################
#       Get Skin Tone       #
#############################

from pickle import NONE
from colormath.color_objects import LabColor, HSVColor, sRGBColor
from colormath.color_conversions import convert_color

#Lab의 b값
#웜쿨 판단용
warm_std_b = [13.600828619628416, 13.63082566685463, 20.024053123569743, 2.8507945613448897, 5.5708967963920335] 
cool_std_b = [7.190367258960277, 6.9384118526366, 9.126889116433446, -5.286951388817933, -2.655967261522798]

#피부(좌우), 입술, 눈동자(좌우) 가중치
lab_weight = [30, 30, 20, 5, 5]


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
            warm_dist += abs(lab_b[i] - warm_std_b[i]) * lab_weight[i]
            cool_dist += abs(lab_b[i] - cool_std_b[i]) * lab_weight[i]
        
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