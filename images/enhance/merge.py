import numpy as np
from PIL import Image

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/barbara_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/barbara_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/barbara_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/barbara_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/barbara_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/barbara_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("barbara_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/boat_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/boat_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/boat_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/boat_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/boat_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/boat_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("boat_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/cameraman_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/cameraman_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/cameraman_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/cameraman_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/cameraman_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/cameraman_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("cameraman_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/fruits_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/fruits_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/fruits_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/fruits_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/fruits_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/fruits_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("fruits_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/goldhill_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/goldhill_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/goldhill_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/goldhill_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/goldhill_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/goldhill_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("goldhill_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/lena_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/lena_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/lena_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/lena_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/lena_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/lena_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("lena_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/peppers_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/peppers_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/peppers_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/peppers_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/peppers_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/peppers_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("peppers_merged.png")

img = np.zeros((128*2,128*3), dtype="uint8")
img[:128,:128] =    np.array(Image.open("results/zelda_DE/enhanced.png"))
img[:128,128:256] = np.array(Image.open("results/zelda_GA/enhanced.png"))
img[:128,256:] =    np.array(Image.open("results/zelda_GWO/enhanced.png"))
img[128:,:128] =    np.array(Image.open("results/zelda_JAYA/enhanced.png"))
img[128:,128:256] = np.array(Image.open("results/zelda_PSO/enhanced.png"))
img[128:,256:] =    np.array(Image.open("results/zelda_RO/enhanced.png"))
img[128,:] = img[:,128] = img[:,256] = 0
Image.fromarray(img).save("zelda_merged.png")

