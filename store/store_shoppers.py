import os

for n in [10,25,50,75,100,150,250,500,1000]:
    print("%4d shoppers..." % n)
    cmd = "python3 store_shop.py products.pkl %d 30 4000 JAYA RI >shoppers/jaya_%d_30_4000.txt" % (n,n)
    os.system(cmd)
    os.system("mv results.pkl shoppers/jaya_%d_30_4000_results.pkl" % n)

