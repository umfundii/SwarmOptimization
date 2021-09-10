import numpy as np
from PIL import Image

mos_d = np.array(Image.open("crane_fly_30_200_DE.png"))
mos_p = np.array(Image.open("crane_fly_30_200_PSO.png"))
mos_u = np.array(Image.open("crane_fly_unaligned.png"))

bry_d = np.array(Image.open("bryozoa_30_200_DE.png"))
bry_p = np.array(Image.open("bryozoa_30_200_PSO.png"))
bry_u = np.array(Image.open("bryozoa_unaligned.png"))

coi_d = np.array(Image.open("coin_30_200_DE.png"))
coi_p = np.array(Image.open("coin_30_200_PSO.png"))
coi_u = np.array(Image.open("coin_unaligned.png"))

y,x = np.gradient(mos_d)
mos_ds = np.sqrt(x*x+y*y).mean()
y,x = np.gradient(mos_p)
mos_ps = np.sqrt(x*x+y*y).mean()
y,x = np.gradient(mos_u)
mos_us = np.sqrt(x*x+y*y).mean()

y,x = np.gradient(bry_d)
bry_ds = np.sqrt(x*x+y*y).mean()
y,x = np.gradient(bry_p)
bry_ps = np.sqrt(x*x+y*y).mean()
y,x = np.gradient(bry_u)
bry_us = np.sqrt(x*x+y*y).mean()

y,x = np.gradient(coi_d)
coi_ds = np.sqrt(x*x+y*y).mean()
Image.fromarray(x.astype("uint8")).save("sharpness_coin_x.png")
Image.fromarray(y.astype("uint8")).save("sharpness_coin_y.png")
y,x = np.gradient(coi_p)
coi_ps = np.sqrt(x*x+y*y).mean()
y,x = np.gradient(coi_u)
coi_us = np.sqrt(x*x+y*y).mean()

print()
print("Sharpness:")
print("    Crane Fly:")
print("        DE       :  %0.9f" % mos_ds)
print("        PSO      :  %0.9f" % mos_ps)
print("        unaligned:  %0.9f" % mos_us)
print("    Bryozoa:")
print("        DE       :  %0.9f" % bry_ds)
print("        PSO      :  %0.9f" % bry_ps)
print("        unaligned:  %0.9f" % bry_us)
print("    Coin:")
print("        DE       :  %0.9f" % coi_ds)
print("        PSO      :  %0.9f" % coi_ps)
print("        unaligned:  %0.9f" % coi_us)
print()

