import cv2
OFFSET = 30

## 4가지 좌표일 때 이미지 영역 구하기
def points4_img(img, arr, p1, p2, p3, p4):
    (x, y) = arr[p1]
    (z, w) = arr[p2]
    (a, b) = arr[p3]
    (c, d) = arr[p4]
    width = abs(z - x)
    height = abs(b - d)
    img = img[y-(height//2):y+(height//2), x:x+width]
    return img

## 2가지 좌표일 때 이미지 영역 구하기
def points2_img(img, arr, p1, p2):
    (x, y) = arr[p1]
    (z, w) = arr[p2]
    width = abs(z - x)
    height = abs(w - y)
    img = img[y:y+height, x:x+width]
    return img

## 1가지 좌표일 때 이미지 영역 구하기
def points1_img(img, xy, isPlus):
    (a, b) = xy
    if (isPlus):
        img = img[b:b+OFFSET, a:a+OFFSET]
    else:
        img = img[b-OFFSET:b, a-OFFSET:a]
    
    return img

## show image
def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
