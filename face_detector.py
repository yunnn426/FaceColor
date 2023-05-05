#import my module
from process_image import *


#import module
import dlib
import cv2
from imutils import face_utils
import numpy as np

class FaceDetector:
    def __init__(self, image):
        ## face detector와 landmark predictor 정의
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("res/shape_predictor_68_face_landmarks.dat")

        #image -> cv2 image
        self.img = cv2.imread(image)

        #init face parts
        self.right_eye = []
        self.left_eye = []
        self.mouth = []
        self.left_cheek = []
        self.right_cheek = []

        self.detect_face()
    
    def detect_face(self):
        #얼굴 랜드마크 분석
        face_parts = [[],[],[],[],[],[],[],[]]

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        #detece face 
        rect = self.detector(gray, 1)[0] #face 하나만 가져옴

        #determine facial landmark
        shape = self.predictor(gray, rect)

        #and convert landmark(x,y) to NumPy array
        shape = face_utils.shape_to_np(shape)

        idx = 0
        for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():   #FACIAL_LANDMARKS_IDXS: mouth, inner_mouth, right_eyebrow, left_eyebrow, right_eye, left_eye, nose, jaw
            face_parts[idx] = shape[i:j]
            idx += 1
        
        self.right_eye = self.extract_face_part(face_parts[4])
        self.left_eye = self.extract_face_part(face_parts[5])
        self.mouth = self.extract_face_part(face_parts[0])
        #좌우 뺨은 상대적으로 추출
        self.left_cheek = self.img[shape[29][1]:shape[33][1], shape[4][0]:shape[48][0]]
        self.right_cheek = self.img[shape[29][1]:shape[33][1], shape[54][0]:shape[12][0]]

    def extract_face_part(self, face_part_points):
        (x, y, w, h) = cv2.boundingRect(face_part_points)
        crop = self.img[y:y+h, x:x+w]
        adj_points = np.array([np.array([p[0]-x, p[1]-y]) for p in face_part_points])

        # Create an mask
        mask = np.zeros((crop.shape[0], crop.shape[1]))
        cv2.fillConvexPoly(mask, adj_points, 1)
        mask = mask.astype(bool)
        crop[np.logical_not(mask)] = [255, 0, 0]

        #show_img(crop)
        return crop


# ##    1. draw eyebrow box (18~22, 23~27)
# ##    수정 필요, 눈썹으로는 머리색 구할 수 없음

# #중첩리스트 풀기
# def flatten(list):
#     result = []
#     for item in list:
#         result.extend(item)
#     return result


# #############################
# #   Get Face Parts to RGB   #
# #     (lips, eyes, skin)    #
# #############################

# ## 입술 rgb 구하기

# def get_lip_rgb(img, shape):
#     lip_img = points4_img(img, shape, 48, 54, 52, 58) #get image for lips using 4 points
#     show_img(lip_img)
#     #get lip color
#     rgb = get_color(lip_img)
#     rgb_arr = flatten(rgb)

#     return rgb_arr


# ## 눈동자 rgb 구하기

# def get_eye_rgb(img, shape):
#     #좌우 눈동자 구하기
#     eye1_img = points2_img(img, shape, 37, 40) #get eye image using 2 points
#     eye2_img = points2_img(img, shape, 43, 46)

#     #눈동자1 rgb값
#     rgb1 = get_color(eye1_img)
#     #눈동자2 rgb값
#     rgb2 = get_color(eye2_img)
#     #평균 rgb
#     rgb = (rgb1 + rgb2) / 2
#     rgb_arr = flatten(rgb)

#     return rgb_arr


# ## 피부 rgb 구하기

# def get_skin_rgb(img, shape):
#     #좌우 뺨 구하기
#     mid1 = (shape[40] + shape[48]) // 2
#     skin1_img = points1_img(img, mid1, False)
#     #뺨1 rgb값
#     rgb1 = get_color(skin1_img)

#     mid2 = (shape[47] + shape[54]) // 2
#     skin2_img = points1_img(img, mid2, True)
#     #뺨2 rgb값
#     rgb2 = get_color(skin2_img)

#     #평균 rgb
#     rgb = (rgb1 + rgb2) / 2
#     rgb_arr = flatten(rgb)
    
#     return rgb_arr
