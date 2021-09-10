import os
from PIL import Image

d = os.listdir("../test_images/")

for i in d:
    for alg in ["RO","PSO","DE","JAYA","GWO","GA"]:
        im = Image.open("../test_images/"+i).resize((128,128), Image.BICUBIC) 
        im.save("/tmp/image.png")
        os.system("python3 enhance.py /tmp/image.png 10 50 %s RI results/%s_%s" % (alg,os.path.basename(i[:-4]),alg))

os.system("rm /tmp/image.png")

