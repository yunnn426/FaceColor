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

#HSV의 v값
#계절 구분용
spring_std_v = [0.8712156862745101, 0.882823529411765, 0.7739607843137257, 0.44454901960784327, 0.4208627450980393]
fall_std_v = [0.8302745098039217, 0.8724705882352943, 0.6870588235294117, 0.443607843137255, 0.4167843137254903]

summer_std_v = [0.8801568627450983, 0.8880000000000002, 0.7502745098039217, 0.4200784313725491, 0.4252549019607845]
winter_std_v = [0.8525490196078434, 0.8619607843137257, 0.6508235294117647, 0.44329411764705895, 0.41223529411764714]

#피부(좌우), 입술, 눈동자(좌우) 가중치
weight = [30, 30, 20, 5, 5]


class ToneDetector:
    
    def __init__(self):
        self.skin_tone = None
        self.color_result = None

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
    
    
    ###########
    # 웜쿨 구분 #
    ###########

    def warm_or_cool(self, lab_b):
        warm_dist = 0 #웜과의 거리
        cool_dist = 0 #쿨과의 거리

        #피부, 입술, 눈동자 측정
        for i in range(5):
            warm_dist += abs(lab_b[i] - warm_std_b[i]) * weight[i]
            cool_dist += abs(lab_b[i] - cool_std_b[i]) * weight[i]
        
        #warm_dist > cool_dist면 cool
        #cool_dist > warm_dist면 warm
        if  warm_dist > cool_dist:
            self.skin_tone = 'cool'
        else:
            self.skin_tone = 'warm'

        return self.skin_tone


    ###########
    # 계절 구분 #
    ###########

    #웜-> 봄/가을 구분
    def spring_or_fall(self, hsv_v):
        spring_dist = 0
        fall_dist = 0

        #피부, 입술, 눈동자 측정
        for i in range(5):
            spring_dist += abs(hsv_v[i] - spring_std_v[i]) * weight[i]
            fall_dist += abs(hsv_v[i] - fall_std_v[i]) * weight[i]

        #spring_dist > fall_dist면 fall
        #fall_dist > spring_dist면 spring
        if spring_dist > fall_dist:
            self.skin_tone = 'warm_fall'
        else:
            self.skin_tone = 'warm_spring'
        
        return self.skin_tone

    #쿨-> 여름/겨울 구분
    def summer_or_winter(self, hsv_v):
        summer_dist = 0
        winter_dist = 0

        #피부, 입술, 눈동자 측정
        for i in range(5):
            summer_dist += abs(hsv_v[i] - summer_std_v[i]) * weight[i]
            winter_dist += abs(hsv_v[i] - winter_std_v[i]) * weight[i]

        #summer_dist > winter_dist면 winter
        #winter_dist > summer_dist면 summer
        if summer_dist > winter_dist:
            self.skin_tone = 'cool_winter'
        else:
            self.skin_tone = 'cool_summer'
        
        return self.skin_tone


    ###########
    # 세부 구분 #
    ###########
    """
    결과 반환용
    warm_spring_bright == 0
    warm_spring_light == 1

    cool_summer_light == 2
    cool_summer_bright == 3
    cool_summer_mute = 4

    warm_fall_strong == 5
    warm_fall_mute == 6
    warm_fall_deep == 7

    cool_winter_bright == 8
    cool_winter_deep == 9
    """

    #봄-> 라이트/브라이트 구분
    def season_spring(self, s, v) :
        light_dist = 0
        bright_dist = 0

        #S값 차이 구하기
        sprint_light_s = (161.2 / 255) - s
        spring_bright_s = (203.3 / 255) - s

        #V값 차이 구하기
        sprint_light_v = (236.0 / 255) - v
        spring_bright_v = (241.0 / 255) - v

        light_dist = abs(sprint_light_s) + abs(sprint_light_v)
        bright_dist = abs(spring_bright_s) + abs(spring_bright_v)
    
        #print(light_dist)
        #print(bright_dist)

        if bright_dist < light_dist:
            self.skin_tone = "warm_spring_bright"
            self.color_result = 0
        else:
            self.skin_tone = "warm_spring_light"
            self.color_result = 1

        return self.skin_tone, self.color_result

    #여름-> 라이트/브라이트/뮤트 구분
    def season_summer(self, s, v) :
        light_dist = 0
        bright_dist = 0
        mute_dist = 0

        #S값 차이 구하기
        summer_light_s = (110.3000 / 255) - s
        summer_bright_s = (203.4000 / 255) - s
        summer_mute_s = (149.6000 / 255) - s

        #V값 차이 구하기
        summer_light_v = (246.0000 / 255) - v
        summer_bright_v = (218.1000 / 255) - v
        summer_mute_v = (176.6000 / 255) - v


        light_dist = abs(summer_light_s) + abs(summer_light_v)
        bright_dist = abs(summer_bright_s) + abs(summer_bright_v)
        mute_dist = abs(summer_mute_s) + abs(summer_mute_v)

        #print(light_dist)
        #print(bright_dist)
        #print(mute_dist)

        if light_dist < bright_dist:
            if light_dist < mute_dist:
                self.skin_tone = "cool_summer_light"
                self.color_result = 2
            else:
                self.skin_tone = "cool_summer_mute"
                self.color_result = 4
        else :
            if bright_dist < mute_dist:
                self.skin_tone = "cool_summer_bright"
                self.color_result = 3
            else:
                self.skin_tone = "cool_summer_mute"
                self.color_result = 4
            
        return self.skin_tone, self.color_result
        
    #가을-> 딥/뮤트/스트롱 구분
    def season_fall(self, s, v) :
        deep_dist = 0
        mute_dist = 0
        strong_dist = 0

        #S값 차이 구하기
        fall_deep_s = (191.9000 / 255) - s
        fall_mute_s = (143.0000 / 255) - s
        fall_strong_s = (227.2000 / 255) - s

        #V값 차이 구하기
        fall_deep_v = (163.5000 / 255) - v
        fall_mute_v = (199.4000 / 255) - v
        fall_strong_v = (222.8000 / 255) - v


        deep_dist = abs(fall_deep_s) + abs(fall_deep_v)
        mute_dist = abs(fall_mute_s) + abs(fall_mute_v)
        strong_dist = abs(fall_strong_s) + abs(fall_strong_v)
        #print (deep_dist)
        #print(mute_dist)
        #print(strong_dist)

        if deep_dist < mute_dist:
            if deep_dist < strong_dist:
                self.skin_tone = "warm_fall_deep"
                self.color_result = 7
            else:
                self.skin_tone = "warm_fall_strong"
                self.color_result = 5
        else :
            if mute_dist < strong_dist:
                self.skin_tone = "warm_fall_mute"
                self.color_result = 6
            else:
                self.skin_tone = "warm_fall_strong"
                self.color_result = 5
        
        return self.skin_tone, self.color_result

    #겨울-> 브라이트/딥 구분
    def season_winter(self, s, v) :
        deep_dist = 0
        bright_dist = 0

        #S값 차이 구하기
        winter_deep_s = (168.7 / 255) - s
        winter_bright_s = (226.1 / 255) - s

        #V값 차이 구하기
        winter_deep_v = (139.3 / 255) - v
        winter_bright_v = (216.3 / 255) - v

        deep_dist = abs(winter_deep_s) + abs(winter_deep_v)
        bright_dist = abs(winter_bright_s) + abs(winter_bright_v)
    
        #print(deep_dist)
        #print(bright_dist)

        if bright_dist < deep_dist:
            self.skin_tone = "cool_winter_bright"
            self.color_result = 8
        else :
            self.skin_tone = "cool_winter_deep"
            self.color_result = 9

        return self.skin_tone, self.color_result
        
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