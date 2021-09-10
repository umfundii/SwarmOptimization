#
#  file:  kmeans.py
#
#  Image segmentation using K-means.
#
#  RTK, 01-Jan-2020
#  Last update:  01-Jan-2020
#
################################################################

import time
import os
import sys
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

if (len(sys.argv) == 1):
    print()
    print("kmeans <src> <nclusters> <iterations> <output>")
    print()
    print("  <src>       - source image (grayscale)")
    print("  <nclusters> - number of clusters (e.g. 4)")
    print("  <iterations>- number of iterations(e.g. 1000)")
    print("  <output>    - output directory (overwritten)")
    print()
    exit(0)

img = np.array(Image.open(sys.argv[1]).convert("L"))
n = int(sys.argv[2])
iterations = int(sys.argv[3])
outdir = sys.argv[4]

os.system("rm -rf %s; mkdir %s" % (outdir,outdir))

#  Change from image to vector
v = img.reshape((img.shape[0]*img.shape[1],1))

#  Apply k-means
clf = KMeans(n_clusters=n, max_iter=iterations, tol=0, 
        init='random', n_jobs=-1)

st = time.time()
clf.fit(v)
en = time.time()

centers = clf.cluster_centers_
labels = clf.labels_
seg = centers[labels].reshape(img.shape)

#  Silhouette score over random 25% of samples
idx = np.argsort(np.random.random(v.shape[0]))
idx = idx[:(int(0.25*len(idx)))]
score = silhouette_score(v[idx], labels[idx], metric="euclidean")

#  Store outputs
Image.fromarray(img).save(outdir+"/original.png")
Image.fromarray(seg.astype("uint8")).save(outdir+"/segmented.png")
np.save(outdir+"/cluster_centers.npy", centers)
np.save(outdir+"/pixel_labels.npy", labels)

s  = "\n"
s += "K-means (clusters=%d)\n\n" % n
s += "Clustering took %0.3f seconds (iterations=%d)\n" % (en-st, iterations)
s += "Silhouette score = %0.6f\n" % score
s += "\n"

print(s)
with open(outdir+"/README.txt","w") as f:
    f.write(s)


