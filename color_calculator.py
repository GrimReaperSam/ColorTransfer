import numpy as np
import cv2
from sklearn.cluster import KMeans


def kmeans(image, k=4):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    clt = KMeans(n_clusters=k)
    clt.fit(image)

    number_labels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=number_labels)

    hist = hist.astype("float")
    hist /= hist.sum()

    colors = list()
    for (_, col) in zip(hist, clt.cluster_centers_):
        colors.append(col)

    return colors
