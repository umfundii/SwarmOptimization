import os

f = [i for i in os.listdir("test_images")]

for t in f:
    for n in [4,6,8]:
        print("%s_%d:" % (t[:-4],n))
        for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
            fname = "segmentations/%s_20_2000_%s_%d/README.txt" % (t[:-4],alg,n)
            w = [i[:-1] for i in open(fname) if i.find("Silhouette") != -1][0]
            score = float(w.split()[-1])
            print("    %4s: %0.8f" % (alg,score))
        print()

