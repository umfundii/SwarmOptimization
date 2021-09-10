import os
from PIL import Image

d = os.listdir("../test_images/")

for i in d:
    im = Image.open("../test_images/"+i).resize((128,128), Image.BICUBIC) 
    im.save("/tmp/image.png")
    os.system("python3 enhance.py /tmp/image.png 20 500 GA RI ga/%s" % (os.path.basename(i[:-4]),))

os.system("rm /tmp/image.png")

