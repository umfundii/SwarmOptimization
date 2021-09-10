#
#  file:  melody_match.py
#
#  Generate a melody similar to those in a database of
#  melodies.
#
#  RTK, 21-Jan-2020
#  Last update:  27-Oct-2020
#
################################################################

import time
import os
import sys
import pickle

import numpy as np
from midiutil import MIDIFile
from PIL import Image

sys.path.append("../")

from Jaya import *
from GWO import *
from PSO import *
from DE import *
from RO import *
from GA import *

from QuasirandomInitializer import *
from RandomInitializer import *
from SphereInitializer import *
from Bounds import *
from LinearInertia import *

# Note duration multiplier
M = 0.5

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
            p[i+1] = int(duration*10)/10
            i += 2

        return p


################################################################
#  MusicObjective
#
class MusicObjective:
    """Measure the quality of the melody"""
    
    def __init__(self, db):
        """Constructor"""

        self.fcount = 0
        self.db = db

    def Evaluate(self, p):
        """Evaluate a given melody"""

        #  Count this call
        self.fcount += 1

        #  Random database melody
        n = np.random.randint(0, len(self.db))
        b = self.db[n][:len(p)].copy()
        b[1::2] = b[1::2]*30
        a = p.copy()
        a[1::2] = a[1::2]*30

        #  MSE 
        return np.sqrt(((b-a)**2).sum()/len(a))


################################################################
#  LoadDatabase
#
def LoadDatabase(dbdir):
    """Load a database of melodies"""

    dnames = [dbdir+"/"+i for i in os.listdir(dbdir) if i.find(".npy") != -1]
    dnames.sort()
    db = []
    for name in dnames:
        db.append(np.load(name))
    return db


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
            m.addNote(0, 0, 21, t, M*duration, 0) # rest
        else:
            m.addNote(0, 0, int(note), t, M*duration, volume)
        t += M*duration

    with open(fname, "wb") as f:
        m.writeFile(f)


################################################################
#  DisplayMelody
#
def DisplayMelody(p):
    """Display a melody"""

    ans = ""
    i = 0
    while (i < len(p)):
        note, duration = p[i:(i+2)]
        i += 2
        ans += "%d,%0.2f " % (note, duration)
    ans += "\n"
    return ans


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
        print("melody_match <length> <outfile> <npart> <max_iter> <alg> RI|QI|SI <db>")
        print()
        print("  <length>   - number of notes in the melody")
        print("  <outdir>   - output directory")
        print("  <npart>    - swarm size (template sets dimensions)")
        print("  <max_iter> - maximum number of iterations")
        print("  <alg>      - algorithm: PSO,DE,RO,GWO,JAYA,GA")
        print("  RI|QI|SI   - random, quasirandom, or sphere initializer")
        print("  <db>       - database of existing melodies")
        print()
        return

    ndim = int(sys.argv[1])
    if (ndim < 20):
        ndim = 20
    ndim *= 2
    outdir = sys.argv[2]
    npart = int(sys.argv[3])
    max_iter = int(sys.argv[4])
    alg = sys.argv[5].upper()
    itype = sys.argv[6].upper()
    db = LoadDatabase(sys.argv[7])

    if (not os.path.exists(outdir)):
        os.system("rm -rf %s" % outdir)
        os.system("mkdir %s" % outdir)
    else:
        print("\nOutput directory already exists\n")
        return

    #  Create the bounds object
    note_lo = 35  # 36..84, 35 = rest (play w/zero volume)
    note_hi = 84  # C2..C6
    dur_lo  = 0.3
    dur_hi  = 2.4
    lower = [note_lo, dur_lo] * ndim
    upper = [note_hi, dur_hi] * ndim
    b = MusicBounds(lower, upper)

    #  Create the objective function
    music = MusicObjective(db)

    #  Build the swarm and optimize
    if (itype == "QI"):
        ri = QuasirandomInitializer(npart, ndim, bounds=b)
    elif (itype == "SI"):
        ri = SphereInitializer(npart, ndim, bounds=b)
    else:
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

    results  = "\nMelody match:\n\n"
    results += "npart = %d\n" % npart
    results += "niter = %d\n" % max_iter
    results += "alg = %s\n" % alg
    results += "init = %s\n\n" % itype
    results += "Optimization time = %0.3f seconds\n" % (en-st,)

    #  Store the final melody
    res = swarm.Results()
    melody = res["gpos"][-1]
    results += DisplayMelody(melody) + "\n"
    PlayMelody(melody)
    StoreMelody(melody, outdir+("/melody_%s.mid" % alg))
    np.save(outdir+("/melody_%s.npy" % alg), melody)
    pickle.dump(res,open(outdir+("/melody_%s.pkl" % alg),"wb"))
    
    results += "%d best updates, final objective value %0.12f\n\n" % (len(res["gbest"]), res["gbest"][-1])

    mname = outdir+("/melody_%s.mid" % alg)
    os.system("musescore -o %s -T 0 %s >/dev/null 2>/dev/null" % (outdir+"/source.png", mname))
    os.system("mv %s %s" % (outdir+"/source-1.png", outdir+"/score.png"))
    im = np.array(Image.open(outdir+"/score.png"))
    im = Image.fromarray(255-im[:,:,3])
    im.save(outdir+"/score.png")

    print(results)
    with open(outdir+"/README.txt","w") as f:
        f.write(results)


if (__name__ == "__main__"):
    main()

