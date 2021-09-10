import os

f = [i for i in os.listdir("test_images")]

for n in [4,6,8]:
    for t in f:
        cmd = "python3 kmeans.py test_images/%s %d 1000 kmeans/%s_1000_%d" % \
                (t,n,t[:-4],n)
        print(cmd, flush=True)
        os.system(cmd)

