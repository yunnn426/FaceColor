#import my module
from process_image import *
from color_extract import ColorExtractor
from tone_detector import ToneDetector
from face_detector import FaceDetector

#경고 무시
import warnings
warnings.filterwarnings('ignore')

#웜톤 이미지 10장
warm_img = ["res/warm/warm1.jpg", "res/warm/warm2.jpg", "res/warm/warm3.jpg", "res/warm/warm4.jpg",
            "res/warm/warm5.jpg", "res/warm/warm6.jpg", "res/warm/warm7.jpg", "res/warm/warm8.jpg",
            "res/warm/warm9.jpg", "res/warm/warm10.jpg"]

#쿨톤 이미지 10장
cool_img = ["res/cool/cool1.jpg", "res/cool/cool2.jpg", "res/cool/cool3.jpg", "res/cool/cool4.jpg",
            "res/cool/cool5.jpg", "res/cool/cool6.jpg", "res/cool/cool7.jpg", "res/cool/cool8.jpg",
            "res/cool/cool9.jpg", "res/cool/cool10.jpg"]


def main():
    process_one()

    #process_warm()  

    
#샘플이미지 1장 처리
def process_one():
    #Face Detection
    face_detector = FaceDetector("res/warm/warm1.jpg")
    face = [face_detector.left_cheek, face_detector.right_cheek,
            face_detector.mouth,
            face_detector.left_eye, face_detector.right_eye]
        
    #Color Detection
    clusters = 2
    lab_b = []
    tone_detector = ToneDetector()
    for f in face: #뺨 좌 -> 뺨 우 -> 입술 -> 눈 좌 -> 눈 우 순으로 rgb, lab 계산 
        show_img(f)

        #rgb
        color_extractor = ColorExtractor(f, clusters)
        rgb_color = color_extractor.color
        #print(rgb_color)
        
        #lab
        lab_color = tone_detector.RGB_to_LAB(rgb_color)
        #print(lab_color)
        lab_b.append(lab_color[2])
    
    #print(lab_b)
    tone = tone_detector.warm_or_cool(lab_b)
    print("skin-tone: ", tone)

#웜톤 샘플 10장 처리
def process_warm():
    for img_path in warm_img:
        #Face Detection
        face_detector = FaceDetector(img_path)
        face = [face_detector.left_cheek, face_detector.right_cheek,
                face_detector.mouth,
                face_detector.left_eye, face_detector.right_eye]
            
        #Color Detection
        clusters = 2
        lab_b = []
        tone_detector = ToneDetector()
        for f in face: #뺨 좌 -> 뺨 우 -> 입술 -> 눈 좌 -> 눈 우 순으로 rgb, lab 계산 
            #show_img(f)

            #rgb
            color_extractor = ColorExtractor(f, clusters)
            rgb_color = color_extractor.color
            #print(rgb_color)
            
            #lab
            lab_color = tone_detector.RGB_to_LAB(rgb_color)
            #print(lab_color)
            lab_b.append(lab_color[2])
    
        #print(lab_b)
        tone = tone_detector.warm_or_cool(lab_b)
        print("skin-tone:", tone)


if __name__ == '__main__':
    main()


#그래프 출력용
#b_results = []
# from test import plot_lab
# plot_lab(b_results)