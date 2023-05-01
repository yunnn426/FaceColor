#import my module
from process_image import *
from color_extract import get_color
from tone_detector import ImageAnalyzer

#import module
import dlib
import cv2
from imutils import face_utils
from skimage import io, color

#경고 무시
import warnings
warnings.filterwarnings('ignore')

## face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#웜톤 이미지 10장
warm_img = ["warm/warm1.jpg", "warm/warm2.jpg", "warm/warm3.jpg", "warm/warm4.jpg",
            "warm/warm5.jpg", "warm/warm6.jpg", "warm/warm7.jpg", "warm/warm8.jpg",
            "warm/warm9.jpg", "warm/warm10.jpg"]

#쿨톤 이미지 10장
cool_img = ["cool/cool1.jpg", "cool/cool2.jpg", "cool/cool3.jpg", "cool/cool4.jpg",
            "cool/cool5.jpg", "cool/cool6.jpg", "cool/cool7.jpg", "cool/cool8.jpg",
            "cool/cool9.jpg", "cool/cool10.jpg"]

#이미지 불러오기
def get_image(img_path):
    img = cv2.imread(img_path)
    return img

#얼굴 랜드마크 분석
def get_face(raw_img):
    #image -> cv2 image
    img = cv2.imread(raw_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #detece face 
    rect = detector(gray, 1)[0] #face 하나만 가져옴

    #determine facial landmark
    shape = predictor(gray, rect)
    #and convert landmark(x,y) to NumPy array
    shape = face_utils.shape_to_np(shape)

    return shape

# # #convert dlib rectangle to bounding box
# (x, y, w, h) = face_utils.rect_to_bb(rect)
# cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#draw circles
# for (x, y) in shape:
#     cv2.circle(img, (x, y), 2, (0, 0, 255), -1)

# #######
# ##show output image(face detection + facial landmarks)
# cv2.imshow('img', img)
# cv2.waitKey()
# cv2.destroyAllWindows()


##    1. draw eyebrow box (18~22, 23~27)
##    수정 필요, 눈썹으로는 머리색 구할 수 없음


# ##    2. draw lip box (49~60 - 61~68)
# #draw lipsOut to rectangle
# lip1_img = points4_img(img, shape, 48, 54, 52, 58) #get image for lips using 4 points
# show_img(lip1_img)

# #get lip color
# rgb = get_color(lip1_img)
# # #print(rgb)
# # lab = color.rgb2lab([rgb])
# # print(lab)

# ##    3. draw eye box
# #draw eye1 to rectangle
# eye1_img = points2_img(img, shape, 37, 40) #get eye image using 2 points
# show_img(eye1_img)

# #draw eye2 to rectangle
# eye2_img = points2_img(img, shape, 43, 46)
# show_img(eye2_img)


#중첩리스트 풀기
def flatten(list):
    result = []
    for item in list:
        result.extend(item)
    return result


##    4. draw skin box
#draw skin to rectangle
def get_skin_rgb(img, shape):
    mid1 = (shape[40] + shape[48]) // 2
    skin1_img = points1_img(img, mid1, False)
    #show_img(skin1_img)
    rgb1 = get_color(skin1_img)

    mid2 = (shape[47] + shape[54]) // 2
    skin2_img = points1_img(img, mid2, True)
    #show_img(skin2_img)
    rgb2 = get_color(skin2_img)

    rgb = (rgb1 + rgb2) / 2
    rgb_arr = flatten(rgb)
    
    return rgb_arr


#ImageAnalyzer 호출
image_analyzer = ImageAnalyzer()

#웜톤 이미지 10장 분석
print("### 10 Warm images ###")
for img_path in warm_img :
    shape = get_face(img_path)
    img = get_image(img_path)
    rgb = get_skin_rgb(img, shape)

    skin_tone = image_analyzer.analyze_image(rgb)

    print('skin-tone:', skin_tone)  


#쿨톤 이미지 10장 분석
# print("\n\n### 10 Cool images ###")
# for img_path in cool_img :
#     shape = get_face(img_path)
#     img = get_image(img_path)
#     rgb = get_skin_rgb(img, shape)

#     skin_tone = image_analyzer.analyze_image(rgb)

#     print('skin-tone:', skin_tone)  