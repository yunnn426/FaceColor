import cv2

#import my module
from color_extract import ColorExtractor
from tone_detector import ToneDetector
from face_detector import FaceDetector
import firebase

#경고 무시
import warnings
warnings.filterwarnings('ignore')

#샘플이미지 각각 50장
warm_path = "res/warm/warm"
cool_path = "res/cool/cool"

#예시 이미지 10장 (1~5: 웜톤, 6~10: 쿨톤)
example_path = "res/example/ex"

#테스트 이미지 (무작위)
test_path = "res/test/test"

def main():
    #process_one()
    #process_test(example_path)
    process_test(example_path)

## show image
def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
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
    print("skin-tone: ", tone)


#예시 이미지 10장 처리
def process_test(path):
    for i in range(10):
        img_path = path + str(i + 1) + ".jpg"
        print(img_path)
        
        #Face Detection
        face_detector = FaceDetector(img_path)

        #오류 처리
        from face_detector import flag
        #print(flag)
        if (flag == 1):
            print("처리할 수 없는 사진")
            return
    
        #뺨 좌 -> 뺨 우 -> 입술 -> 눈 좌 -> 눈 우 순으로 face에 저장
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



#최초 실행
if __name__ == '__main__':
    firebase.start()
    main()