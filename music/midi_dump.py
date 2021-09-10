#
#  file: midi_dump.py
#
#  Extract the notes and duration from a set of MIDI files.
#
#  RTK, 20-Oct-2020
#  Last update:  24-Oct-2020
#
################################################################

import os
import sys
import numpy as np

for arg in sys.argv[1:]:
    print("    extacting %s...." % os.path.basename(arg))
    os.system("mftext %s >/tmp/xyzzy" % arg)
    lines = [i[:-1] for i in open("/tmp/xyzzy") if (i.find("pitch") != -1) and (i.find("chan=1") != -1)]
    k=0
    p = []
    while (k < len(lines)):
      pitch = int(lines[k].split()[-2].split("=")[1])
      t0 = int(lines[k].split()[0].split("=")[1])
      try:
        t1 = int(lines[k+1].split()[0].split("=")[1])
      except:
        break
      p.append(pitch)
      p.append(0.21*(t1-t0)/50)
      k += 2
    p = np.array(p)
    np.save(arg[:-4]+".npy", p)

os.system("rm -f /tmp/xyzzy")

