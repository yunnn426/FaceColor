#import my module
from process_image import *
from color_extract import get_color

#import module
import dlib
import cv2
from imutils import face_utils
from skimage import io, color

## face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#image 가져오기
img = cv2.imread("image4.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#detece face 
rect = detector(gray, 1)[0] #face 하나만 가져옴

#determine facial landmark
shape = predictor(gray, rect)
#and convert landmark(x,y) to NumPy array
shape = face_utils.shape_to_np(shape)

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


##    2. draw lip box (49~60 - 61~68)
#draw lipsOut to rectangle
lip1_img = points4_img(img, shape, 48, 54, 52, 58) #get image for lips using 4 points
show_img(lip1_img)

#get lip color
rgb = get_color(lip1_img)
# #print(rgb)
# lab = color.rgb2lab([rgb])
# print(lab)

##    3. draw eye box
#draw eye1 to rectangle
eye1_img = points2_img(img, shape, 37, 40) #get eye image using 2 points
show_img(eye1_img)

#draw eye2 to rectangle
eye2_img = points2_img(img, shape, 43, 46)
show_img(eye2_img)


##    4. draw skin box
#draw skin to rectangle
mid1 = (shape[40] + shape[48]) // 2
skin1_img = points1_img(img, mid1, False)
rgb1 = get_color(skin1_img)

mid2 = (shape[47] + shape[54]) // 2
skin2_img = points1_img(img, mid2, True)
rgb2 = get_color(skin2_img)

rgb = (rgb1 + rgb2) / 2
print(rgb)
#lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2Lab)
#print(lab)