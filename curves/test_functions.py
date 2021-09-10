#
#  file:  test_functions.py
#
#  RTK, 16-Aug-2020
#  Last update:  17-Aug-2020
#
################################################################

import os

for alg in ["RO","PSO","DE","GWO","Jaya","GA"]:
    os.system("python3 curves.py NIST/chwirut1.txt -1x-1x-1 1x1x1 3 20 10000 1e-9 %s RI plots/chwirut1_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/chwirut1.txt -1x-1x-1 1x1x1 3 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/eckerle4.txt 0x0x0 5x5x500 3 20 10000 1e-9 %s RI plots/eckerle4_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/eckerle4.txt 0x0x0 5x5x500 3 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/ENSO.txt -2x-2x-2x-2x-2x-2x-2x-2x-2 15x5x5x50x2x1x30x1x3 9 20 10000 1e-9 %s RI plots/ENSO_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/ENSO.txt -2x-2x-2x-2x-2x-2x-2x-2x-2 15x5x5x50x2x1x30x1x3 9 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/gauss1.txt 0x0x0x0x0x0x0x0 100x1x110x70x25x75x200x20 8 20 10000 1e-9 %s RI plots/gauss1_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/gauss1.txt 0x0x0x0x0x0x0x0 100x1x110x70x25x75x200x20 8 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/gauss2.txt 0x0x0x0x0x0x0x0 100x1x110x110x25x75x200x20 8 20 10000 1e-9 %s RI plots/gauss2_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/gauss2.txt 0x0x0x0x0x0x0x0 100x1x110x110x25x75x200x20 8 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/hahn1.txt 0x-1x0x-1x-1x0x-1 2x1x1x1x1x1x1 7 20 10000 1e-9 %s RI plots/hahn1_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/hahn1.txt 0x-1x0x-1x-1x0x-1 2x1x1x1x1x1x1 7 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/sinexp.txt -5x-5x0x0x0 5x5x30x10x1 5 20 10000 1e-9 %s RI plots/sinexp_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/sinexp.txt -5x-5x0x0x0 5x5x30x10x1 5 20 10000 1e-9 %s RI" % (alg,))
    os.system("python3 curves.py NIST/thurber.txt 0x0x0x0x0x0x0 1500x1600x600x100x1x1x1 7 20 10000 1e-9 %s RI plots/thurber_%s_plot.png" % (alg,alg))
    for i in range(4):
        os.system("python3 curves.py NIST/thurber.txt 0x0x0x0x0x0x0 1500x1600x600x100x1x1x1 7 20 10000 1e-9 %s RI" % (alg,))

