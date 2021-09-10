import os

f = [i for i in os.listdir("test_images")]

for alg in ["RO","DE","PSO","GWO","JAYA","GA"]:
    for n in [4,6,8]:
        for t in f:
            cmd = "python3 segment.py test_images/%s %d 20 2000 %s RI segmentations/%s_20_2000_%s_%d" % \
                    (t,n,alg,t[:-4],alg,n)
            print(cmd, flush=True)
            os.system(cmd)

