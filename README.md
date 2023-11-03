# FaceColor
> [Mosa](https://github.com/yunnn426/Mosa)의 퍼스널 컬러 진단기 부분입니다.


## 사용자의 사진에서 컬러 추출
- openCV와 dlib을 활용해 사용자의 얼굴 사진에서 눈, 코, 입 영역을 탐지한다.
- 눈, 입은 마스크 형태로 추출하고, 좌우 볼 영역은 사각형으로 자른다.
- 네 가지 영역의 대표 색을 k-means clustering을 통해 추출한다.

  
![Group 6](https://github.com/yunnn426/FaceColor/assets/95147113/308f5fb4-1f20-4fbe-b866-bec3e48efe95)

## 퍼스널 컬러 진단
- 퍼스널 컬러 별 대표 연예인 사진 수천장을 모아 각 컬러에 대한 눈, 입, 볼의 기준 색을 미리 계산하였다.
- 위 단계에서 계산한 사용자의 대표 색과 퍼스널 컬러 별 기준값을 비교해 눈, 입, 볼에 대해 퍼스널 컬러를 구한 후
- 얼굴 부위 별 가중치에 따라 최종 퍼스널 컬러를 구한다.


```
#피부(좌우), 입술, 눈동자(좌우) 가중치
weight = [30, 30, 20, 5, 5]
```



![Group 7](https://github.com/yunnn426/FaceColor/assets/95147113/eda3a540-d590-45dc-86a1-990ef5875b47)
