from sklearn.cluster import KMeans
import cv2
import numpy as np
import matplotlib.pyplot as plt
#된거 같아요 !@!
#색 추출 프로세스
def get_color(img):
    #k-means clustering
    ##image to scikit-learn
    k_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    k_img = k_img.reshape((k_img.shape[0] * k_img.shape[1], 3))

    k = 1  #define k
    clt = KMeans(n_clusters = k)
    clt.fit(k_img)

    return clt.cluster_centers_
    
    # hist1 = centroid_histogram(clt)
    # bar = plot_colors(hist1, clt.cluster_centers_) ##clt.cluster_centers_: return rgb
    # print(clt.cluster_centers_)
    # # show our color bart
    # plt.figure()
    # plt.axis("off")
    # plt.imshow(bar)
    # plt.show()


#컬러 분율
def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
    
    # return the histogram
    return hist

# 히스토그램 그리기
def plot_colors(hist, centroids):
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