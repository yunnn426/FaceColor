from sklearn.cluster import KMeans
import cv2
import numpy as np
import matplotlib.pyplot as plt

#색 추출 프로세스
class ColorExtractor:
    COLORS = None
    
    def __init__(self, image, n_clusters):
        self.color = [] #final rgb color

        #k-means clustering
        ##image to scikit-learn
        k_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        k_img = k_img.reshape((k_img.shape[0] * k_img.shape[1], 3))

        clt = KMeans(n_clusters)
        clt.fit(k_img)

        self.COLORS = clt.cluster_centers_
        
        face_color, hist1 = self.centroid_histogram(clt) #비율과 그 컬러 반환, 블루마스크 제거되면 1개, 없으면 2개
        
        self.color = self.get_face_color(face_color, hist1.tolist()) #최종 face part color 추출

        bar = self.plot_colors(hist1, clt.cluster_centers_) ##clt.cluster_centers_: return rgb
        #print(face_color)
        # show our color bart
        # plt.figure()
        # plt.axis("off")
        # plt.imshow(bar)
        # plt.show()

    def get_face_color(self, color_list, hist):
        color = []
        if len(color_list) == 1:
            color = color_list[0]
            
        else: #히스토그램 2개일 때 비율 큰 색 반환
            a = hist[0]
            b = hist[1]
            if a > b: 
                color = color_list[0]
            else:
                color = color_list[1]
        
        return color

    #컬러 분율
    def centroid_histogram(self, clt):
        # grab the number of different clusters and create a histogram
        # based on the number of pixels assigned to each cluster
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)

        # normalize the histogram, such that it sums to one
        hist = hist.astype("float")
        hist /= hist.sum()
        
        colors = self.COLORS
        color_list = []
        
        for i in range(2):
            colors[i] = colors[i].astype(int)
        
        color_list = colors.tolist()
        #print("전: ", color_list)

        for i in color_list: 
            if i[2] > 250: #blue mask 삭제
                color_list.remove(i)
        
        #print("후: ", color_list)
        #print(hist)
        # return the histogram
        return color_list, hist

    # 히스토그램 그리기
    def plot_colors(self, hist, centroids):
        # initialize the bar chart representing the relative frequency
        # of each of the colors
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0

        # loop over the percentage of each cluster and the color of
        # each cluster
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                        color.astype("uint8").tolist(), -1)
            startX = endX

        # return the bar chart
        return bar