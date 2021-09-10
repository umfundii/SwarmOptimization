#
#  file:  melody_maker.py
#
#  Generate a melody
#
#  RTK, 11-Jan-2020
#  Last update:  30-Oct-2020
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
            p[i+1] = np.floor(duration)
            i += 2

        return p


################################################################
#  MusicObjective
#
class MusicObjective:
    """Measure the quality of the melody"""
    
    def __init__(self, note_lo, note_hi, mode="major"):
        """Constructor"""

        self.mode = mode
        self.fcount = 0
        self.lo = note_lo
        self.hi = note_hi + 1

    def Durations(self, p):
        """Favor quarter and half notes"""

        d = p[1::2].astype("int32")
        dp = np.bincount(d, minlength=8)
        b = dp / dp.sum()
        a = np.array([0,0,100,0,60,0,20,0])
        a = a / a.sum()
        return np.sqrt(((a-b)**2).sum())

    def CheckRange(self, p):
        """Is within note range?"""

        notes = p[::2]
        lo = notes.min()
        hi = notes.max()
        return 0 if (hi-lo) <= 18 else 1

    def ModeNotes(self, notes, mode):
        """Return the distance between the nodes and the given mode"""

        modes = {
            "ionian":     [2,2,1,2,2,2,1],
            "dorian":     [2,1,2,2,2,1,2],
            "phrygian":   [1,2,2,2,1,2,2],
            "lydian":     [2,2,2,1,2,2,1],
            "mixolydian": [2,2,1,2,2,1,2],
            "aeolian":    [2,1,2,2,1,2,2],
            "locrian":    [1,2,2,1,2,2,2],
            "major":      [2,2,1,2,2,2,1],
            "minor":      [2,1,2,2,1,2,2],
        }
        
        m = modes[mode.lower()]

        #  Actual notes in this melody
        A = np.zeros(self.hi-self.lo+1)
        for i in range(notes.shape[0]):
            A[int(notes[i]-self.lo)] = 1

        #  Notes in the given mode based on this root
        B = np.zeros(self.hi-self.lo+1)
        note = int(notes[0])
        while (note <= self.hi):
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[0]
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[1]
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[2]
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[3]
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[4]
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[5]
            if (note <= self.hi):
                B[note-self.lo] = 1
            note += m[6]
            if (note <= self.hi):
                B[note-self.lo] = 1
        note = int(notes[0])
        while (note >= self.lo):
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[6]
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[5]
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[4]
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[3]
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[2]
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[1]
            if (note >= self.lo):
                B[note-self.lo] = 1
            note -= m[0]
            if (note >= self.lo):
                B[note-self.lo] = 1

        return A,B

    def Intervals(self, notes, mode):
        """Count valid third and fifth intervals"""

        #  Count major, minor thirds and fifths
        #  favoring thirds over fifths
        _,B = self.ModeNotes(notes, mode)
        valid = minor = major = fifth = 0
        for i in range(len(notes)-1):
            x = int(notes[i]-self.lo)
            y = int(notes[i+1]-self.lo)
            if (B[x] == 1) and (B[y] == 1):
                valid += 1
                if (abs(x-y) == 3):
                    minor += 1
                if (abs(x-y) == 4):
                    major += 1
                if (abs(x-y) == 7):
                    fifth += 1
        w = (3*minor + 3*major + fifth) / 7
        return 1.0 - np.array([valid,w])/len(notes)

    def Distance(self, notes, mode):
        """Hamming distance between notes and mode notes"""

        A,B = self.ModeNotes(notes, mode)
        lo = int(notes.min() - self.lo)
        hi = int(notes.max() - self.lo)
        a = A[lo:(hi+2)]
        b = B[lo:(hi+2)]
        score = (np.logical_xor(a,b)*1).sum()
        score /= len(a)
        return score

    def Evaluate(self, p):
        """Evaluate a given melody"""

        #  Count this call
        self.fcount += 1

        #  Distance from the mode
        score = self.Distance(p[::2], self.mode)

        #  Durations
        dur = self.Durations(p)

        #  Favor melodies covering no more than 18 steps
        R = self.CheckRange(p)

        #  Distance from desired arrangement of intervals
        v,t = self.Intervals(p[::2], self.mode)

        return R + v + t + score + dur


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
        ans += "%d,%0.2f " % (note, M*duration)
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
        print("melody_maker <length> <outfile> <npart> <max_iter> <alg> RI|MI|SI <mode>")
        print()
        print("  <length>   - number of notes in the melody")
        print("  <outdir>   - output directory")
        print("  <npart>    - swarm size (template sets dimensions)")
        print("  <max_iter> - maximum number of iterations")
        print("  <alg>      - algorithm: PSO,DE,RO,GWO,JAYA,GA")
        print("  RI|QI|SI   - initializer")
        print("  <mode>     - mode")
        print()
        return

    ndim = int(sys.argv[1])
    ndim *= 2
    outdir = sys.argv[2]
    npart = int(sys.argv[3])
    max_iter = int(sys.argv[4])
    alg = sys.argv[5].upper()
    itype = sys.argv[6].upper()
    mode = sys.argv[7].lower()

    if (not os.path.exists(outdir)):
        os.system("rm -rf %s" % outdir)
        os.system("mkdir %s" % outdir)
    else:
        print("\nOutput directory already exists\n")
        return

    #  Create the bounds object
    note_lo = 35  # 36..84, 35 = rest (play w/zero volume)
    note_hi = 84  # C2..C6
    dur_lo  = 1   # multiples of M
    dur_hi  = 5
    lower = [note_lo, dur_lo] * ndim
    upper = [note_hi, dur_hi] * ndim
    b = MusicBounds(lower, upper)

    #  Create the objective function
    music = MusicObjective(note_lo, note_hi, mode)

    #  Build the swarm and optimize
    if (itype == "QI"):
        ri = QuasiInitializer(npart, ndim, bounds=b)
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

    results  = "\nMelody maker:\n\n"
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
    
    results += "%d best updates, final objective value %0.4f\n\n" % (len(res["gbest"]), res["gbest"][-1])

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

