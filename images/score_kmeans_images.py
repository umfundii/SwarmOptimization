import os

f = [i for i in os.listdir("test_images")]

for t in f:
    for n in [4,6,8]:
        fname = "kmeans/%s_1000_%d/README.txt" % (t[:-4],n)
        w = [i[:-1] for i in open(fname) if i.find("Silhouette") != -1][0]
        score = float(w.split()[-1])
        print("%12s_%d: %0.8f" % (t[:-4],n,score))

