import cv2

#import my module
from color_extract import ColorExtractor
from tone_detector import ToneDetector
from face_detector import FaceDetector
import firebase

#경고 무시
import warnings
warnings.filterwarnings('ignore')

#샘플이미지 각각 25장
spring_path = "res/spring/warm"
fall_path = "res/fall/warm"

summer_path = "res/summer/cool"
winter_path = "res/winter/cool"

#예시 이미지 10장 (1~5: 웜톤, 6~10: 쿨톤)
example_path = "res/example/ex"

#테스트 이미지 (무작위)
test_path = "res/test/test"

#결과값
color = "None"
face = "a"

def main():
    analysis()
    #process_test(test_path)
    #print("Warm>Fall 사진 25장")
    #process_test(fall_path)
    #print("Cool>Winter 사진 25장")
    #process_test(winter_path)
    #process_test(fall_path)
    #process_test(winter_path)

## show image
def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
#이미지 1장 처리
def analysis():
    #Face Detection
    face_detector = FaceDetector("user_image/user.jpg")

    #오류 처리
    from face_detector import flag
    #print(flag)
    if (flag == 1):
        print("처리할 수 없는 사진")
        return
    
    face = [face_detector.left_cheek, face_detector.right_cheek,
            face_detector.mouth,
            face_detector.left_eye, face_detector.right_eye]
    
    #Color Detection
    clusters = 2
    lab_b = []
    hsv_s = []
    hsv_v = []

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

        #hsv
        hsv_color = tone_detector.RGB_to_HSV(rgb_color)
        hsv_s.append(hsv_color[1])
        hsv_v.append(hsv_color[2])
        #print(hsv_color)
    
    #print(lab_b)
    
    #1차 톤 구분 (웜 / 쿨)
    tone = tone_detector.warm_or_cool(lab_b)

    #2차 톤 구분
    #봄 / 가을
    if (tone == "warm"):
        season = tone_detector.spring_or_fall(hsv_v)

    #여름 / 겨울
    else:
        season = tone_detector.summer_or_winter(hsv_v)

    #3차 세부 구분
    #세부 구분은 입술 색으로만 판별함

    global color
    #봄> 브라이트/라이트
    if (season == "warm_spring"):
        detail, color = tone_detector.season_spring(hsv_s[2], hsv_v[2])

    #가을> 
    elif (season == "warm_fall"):
        detail, color = tone_detector.season_fall(hsv_s[2], hsv_v[2])

    #여름> 라이트/브라이트/뮤트
    elif (season == "cool_summer"):
        detail, color = tone_detector.season_summer(hsv_s[2], hsv_v[2])

    #겨울> 브라이트/딥
    else:
        detail, color = tone_detector.season_winter(hsv_s[2], hsv_v[2])
    
    print("color_result: ", color)
    print("skin-tone: ", detail)
    
    


#예시 이미지 10장 처리
def process_test(path):
    for i in range(25):
        img_path = path + str(i + 26) + ".jpg"
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
        hsv_s = []
        hsv_v = []

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

            #hsv
            hsv_color = tone_detector.RGB_to_HSV(rgb_color)
            hsv_s.append(hsv_color[1])
            hsv_v.append(hsv_color[2])
    
        #print(lab_b)
        #1차 톤 구분 (웜 / 쿨)
        tone = tone_detector.warm_or_cool(lab_b)

        #2차 톤 구분
        #봄 / 가을
        if (tone == "warm"):
            season = tone_detector.spring_or_fall(hsv_v)

        #여름 / 겨울
        else:
            season = tone_detector.summer_or_winter(hsv_v)

        #3차 세부 구분
        #세부 구분은 입술 색으로만 판별함

        #봄> 브라이트/라이트
        if (season == "warm_spring"):
            detail = tone_detector.season_spring(hsv_s[2], hsv_v[2])

        #가을> 딥/뮤트/스트롱
        elif (season == "warm_fall"):
            detail = tone_detector.season_fall(hsv_s[2], hsv_v[2])

        #여름> 라이트/브라이트/뮤트
        elif (season == "cool_summer"):
            detail = tone_detector.season_summer(hsv_s[2], hsv_v[2])

        #겨울> 브라이트/딥
        else:
            detail = tone_detector.season_winter(hsv_s[2], hsv_v[2])

        print("skin-tone: ", detail)





#최초 실행
if __name__ == '__main__':
    firebase.start()
    main()
    firebase.result(color)