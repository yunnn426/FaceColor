from PIL import Image
from tone_detector import ImageAnalyzer

#웜 기준 컬러
warm = ["basecolor/warm_fall1.jpg", "basecolor/warm_fall2.jpg", "basecolor/warm_fall3.jpg", "basecolor/warm_fall4.jpg", "basecolor/warm_fall5.jpg", "basecolor/warm_fall6.jpg",
        "basecolor/warm_spring1.jpg", "basecolor/warm_spring2.jpg", "basecolor/warm_spring3.jpg", "basecolor/warm_spring4.jpg", "basecolor/warm_spring5.jpg", "basecolor/warm_spring6.jpg"]
#웜 기준 컬러의 lab (a, b)
warm_std_a = []
warm_std_b = []

#쿨 기준 컬러
cool = ["basecolor/cool_summer1.jpg", "basecolor/cool_summer2.jpg", "basecolor/cool_summer3.jpg", "basecolor/cool_summer4.jpg", "basecolor/cool_summer5.jpg", "basecolor/cool_summer6.jpg",
            "basecolor/cool_winter1.jpg", "basecolor/cool_winter2.jpg", "basecolor/cool_winter3.jpg", "basecolor/cool_winter4.jpg", "basecolor/cool_winter5.jpg", "basecolor/cool_winter6.jpg"]
#쿨 기준 컬러의 lab (a, b)
cool_std_a = []
cool_std_b = []

def get_lab(x):
    # 이미지 열기
    img = Image.open(x)

    # 이미지의 rgb값 계산
    avg_color = img.resize((1, 1)).getpixel((0, 0))

    image_analyzer = ImageAnalyzer()
    
    #lab값 계산
    lab_color = image_analyzer.RGB_to_LAB(avg_color)
    
    return lab_color


#웜 lab 계산
for x in warm:
    lab_color = get_lab(x)
   
    #lab값 저장
    warm_std_a.append(lab_color[1])
    warm_std_b.append(lab_color[2])

#쿨 lab 계산
for x in cool:
    lab_color = get_lab(x)

    #lab값 저장
    cool_std_a.append(lab_color[1])
    cool_std_b.append(lab_color[2])

print("warm_std_a: ", warm_std_a)
print("warm_std_b: ", warm_std_b)
print("cool_std_a: ", cool_std_a)
print("cool_std_b: ", cool_std_b)