#
#  file:  melody_merge.py
#
#  Mix melodies
#
#  RTK, 26-Dec-2019
#  Last update:  27-Oct-2020
#
################################################################

import time
import os
import sys
import pickle

import numpy as np
from midiutil import MIDIFile

sys.path.append("../")

from Jaya import *
from GWO import *
from PSO import *
from DE import *
from RO import *
from GA import *

from RandomInitializer import *
from Bounds import *
from LinearInertia import *
from RandomInertia import *


################################################################
#  MusicBounds
#
class MusicBounds(Bounds):
    """Subclass of Bounds to enforce note limits"""

    def __init__(self, lower, upper):
        """Just call the superclass constructor"""
        super().__init__(lower, upper, enforce="resample")

    def Validate(self, p):
        """Enforce note and duration discretization"""

        i = 0
        while (i < p.shape[0]):
            note, duration = p[i:(i+2)]
            p[i] = int(note)
            p[i+1] = np.round(4*duration)/4
            i += 2

        return p


################################################################
#  MusicObjective
#
class MusicObjective:
    """Music objective function"""

    def __init__(self, template1, template2=None, alpha=0.5):
        """Store the templates"""

        if (template2 is None):
            template2 = template1
            alpha = 1.0
        if (len(template1) < len(template2)):
            template2 = template2[:len(template1)]
        if (len(template2) < len(template1)):
            template1 = template1[:len(template2)]
        self.template1 = template1
        self.template2 = template2
        self.alpha = alpha

    def Evaluate(self, p):
        """Evaluate a given melody"""

        d1 = ((p - self.template1)**2).sum()
        d2 = ((p - self.template2)**2).sum()
        return self.alpha*d1 + (1.0-self.alpha)*d2


################################################################
#  StoreMelody
#
def StoreMelody(p, fname):
    """Write a melody to disk"""

    tempo = 120
    volume = 100
    m = MIDIFile(1)
    m.addTempo(0, 0, tempo)
    m.addProgramChange(0, 0, 0, 0)  # acoustic piano

    i = 0
    t = 0.0
    while (i < len(p)):
        note, duration = p[i:(i+2)]
        i += 2
        if (note == 35):
            m.addNote(0, 0, 21, t, duration, 0) # rest
        else:
            m.addNote(0, 0, int(note), t, duration, volume)
        t += duration

    with open(fname, "wb") as f:
        m.writeFile(f)


################################################################
#  DisplayMelody
#
def DisplayMelody(p):
    """Display a melody"""

    print("    ", end="")
    i = 0
    while (i < len(p)):
        note, duration = p[i:(i+2)]
        i += 2
        print("%d,%0.2f " % (note, duration), end="")
    print()


################################################################
#  PlayMelody
#
def PlayMelody(p):
    """Play a melody"""
    
    StoreMelody(p, "/tmp/xyzzy.mid")
    os.system("wildmidi /tmp/xyzzy.mid >/dev/null 2>/dev/null")


################################################################
#  main
#
def main():
    """Swarm melody creator"""

    if (len(sys.argv) == 1):
        print()
        print("swarm_melody <template1> <template2> <alpha> <outdir> <npart> <max_iter>")
        print()
        print("  <template1>      - first template melody (.npy)")
        print("  <template2>|none - second template melody (.npy)")
        print("  <alpha>          - balance between melodies [0,1]")
        print("  <outdir>         - output directory (overwritten)")
        print("  <npart>          - swarm size (template sets dimensions)")
        print("  <max_iter>       - maximum number of iterations")
        print("  <alg>            - algorithm: PSO,DE,RO,GWO,JAYA,GA")
        print()
        return

    template1 = np.load(sys.argv[1])
    if (sys.argv[2].lower() != "none"):
        template2 = np.load(sys.argv[2])
    else:
        template2 = "none"
    alpha = float(sys.argv[3])
    outdir = sys.argv[4]
    npart = int(sys.argv[5])
    max_iter = int(sys.argv[6])
    alg = sys.argv[7].upper()

    #  Create the objective function
    if (sys.argv[2].lower() != "none"):
        template2 = np.load(sys.argv[2])
        music = MusicObjective(template1, template2, alpha)
    else:
        music = MusicObjective(template1, None, alpha)

    ndim = music.template1.shape[0]

    #  Create the bounds object
    note_lo = 35  # 36..84, 35 = rest (play w/zero volume)
    note_hi = 84  # C2..C6
    dur_lo  = 1/4 # 1/16th note
    dur_hi  = 2   # limit to half notes
    lower = [note_lo, dur_lo] * ndim
    upper = [note_hi, dur_hi] * ndim
    b = MusicBounds(lower, upper)

    #  Build the swarm and optimize
    ri = RandomInitializer(npart, ndim, bounds=b)
    if (alg == "PSO"):
        swarm = PSO(obj=music, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b,
                    inertia=LinearInertia())
    elif (alg == "DE"):
        swarm = DE(obj=music, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "RO"):
        swarm = RO(obj=music, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "GWO"):
        swarm = GWO(obj=music, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "JAYA"):
        swarm = Jaya(obj=music, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    elif (alg == "GA"):
        swarm = GA(obj=music, npart=npart, ndim=ndim, max_iter=max_iter, init=ri, bounds=b)
    else:
        raise ValueError("Unknown swarm algorithm: %s" % alg)

    st = time.time()
    swarm.Optimize()
    en = time.time()
    print("Storing final melody, time = %0.3f seconds" % (en-st,))
    print()

    #  Store the final melody
    os.system("rm -rf %s" % outdir)
    os.system("mkdir %s" % outdir)
    res = swarm.Results()
    melody = res["gpos"][-1]
    DisplayMelody(melody)
    PlayMelody(melody)
    StoreMelody(melody, outdir+"/melody.mid")
    np.save(outdir+"/melody.npy", melody)
    pickle.dump(res,open(outdir+"/results.pkl","wb"))
    with open(outdir+"/README.txt", "w") as f:
        f.write("%s, %d particles, %d iterations\n" % (alg, npart, max_iter))
    print()


if (__name__ == "__main__"):
    main()

