#
#  file: nn.py
#
#  Compare swarm training to backprop
#
#  RTK, 13-Dec-2019
#  Last update:  19-Aug-2020
#
################################################################

import sys
import time
import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier

sys.path.append("../../")

from RandomInitializer import *
from QuasirandomInitializer import *
from SphereInitializer import *
from Bounds import *
from LinearInertia import *

from DE import *
from PSO import *
from RO import *
from Jaya import *
from GWO import *
from GA import *

################################################################
#  SwarmObjective
#
class SwarmObjective:
    def __init__(self, snn, xtrn, ytrn):
        """Keep the NN object and test data"""
        self.snn = snn
        self.xtrn = xtrn
        self.ytrn = ytrn

    def Evaluate(self, weights):
        """Test the NN with the given weights"""
        self.snn.coefs_[0] = weights[:1800].reshape((30,60))
        self.snn.coefs_[1] = weights[1800:1860].reshape((60,1))
        self.snn.intercepts_[0] = weights[1860:1920]
        self.snn.intercepts_[1] = weights[1920]
        return 1.0 - self.snn.score(self.xtrn, self.ytrn)


################################################################
#  Set weights
#
def SetWeights(snn, weights):
    """Set the weight of the given NN object"""
    snn.coefs_[0] = weights[:1800].reshape((30,60))
    snn.coefs_[1] = weights[1800:1860].reshape((60,1))
    snn.intercepts_[0] = weights[1860:1920]
    snn.intercepts_[1] = weights[1920]


################################################################
#  confmat
#
def confmat(prob, ytst):
    """2x2 confusion table"""

    p = np.argmax(prob, axis=1)
    tp=tn=fp=fn=0
    for i in range(len(ytst)):
        if (ytst[i]==1) and (p[i]==1):
            tp += 1
        if (ytst[i]==1) and (p[i]==0):
            fn += 1
        if (ytst[i]==0) and (p[i]==1):
            fp += 1
        if (ytst[i]==0) and (p[i]==0):
            tn += 1

    d = np.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    if (d != 0):
        mcc = (tp*tn - fp*fn) / d
    else:
        mcc = 0.0

    return tn,fp,fn,tp,mcc


################################################################
#  main
#
def main():
    """train the models"""

    if (len(sys.argv) == 1):
        print()
        print("nn <npart> <niter> RI|QI|SI")
        print()
        print("  <npart>  - number of swarm particles")
        print("  <niter>  - number of swarm iterations")
        print("  RI|QI|SI - swarm initializer")
        print()
        return

    npart = int(sys.argv[1])
    niter = int(sys.argv[2])
    ndim = 1921 # params in a 30 > 60 > 1 MLP
    itype = sys.argv[3].upper()

    #  Load the train and test data
    xtrn = np.load("nn_xtrn.npy")
    ytrn = np.load("nn_ytrn.npy")
    xtst = np.load("nn_xtst.npy")
    ytst = np.load("nn_ytst.npy")

    #  For tracking performance
    MCC = []; M = []
    TP = []; TN = []
    FP = []; FN = []
    T = []; SC = []

    #  Baseline - use backprop
    nnodes = 60
    clf = MLPClassifier(hidden_layer_sizes=(nnodes,),
            solver="lbfgs", max_iter=3000, tol=0)
    st = time.time()
    clf.fit(xtrn, ytrn)
    en = time.time()
    mlp_prob = clf.predict_proba(xtst)
    mlp_score = clf.score(xtst, ytst)
    tn,fp,fn,tp,mcc = confmat(mlp_prob, ytst)
    TP.append(tp); TN.append(tn); FP.append(fp); FN.append(fn); T.append(en-st); SC.append(mlp_score)
    MCC.append(mcc)
    M.append("MLP")

    snn = MLPClassifier(hidden_layer_sizes=(nnodes,), max_iter=1)
    snn.fit(xtrn,ytrn)  # dummy training - weights discarded
    obj = SwarmObjective(snn,xtrn,ytrn)  # train data

    #  Use very small initial weights
    b = Bounds(-0.01*np.ones(ndim), 0.01*np.ones(ndim), enforce="resample")

    if (itype == "SI"):
        i = SphereInitializer(npart, ndim, bounds=b)
    elif (itype == "QI"):
        i = QuasirandomInitializer(npart, ndim, bounds=b)
    else:
        i = RandomInitializer(npart, ndim, bounds=b)

    #  But increase the range allowed by the weights
    b = Bounds(-10*np.ones(ndim), 10*np.ones(ndim), enforce="resample")

    #  Loop over algorithms
    for alg in ["RO","PSO","DE","GWO","JAYA","GA"]:
        if (alg == "RO"):
            swarm = RO(obj=obj, npart=npart, ndim=ndim, max_iter=niter, init=i, bounds=b)
        elif (alg == "PSO"):
            swarm = PSO(obj=obj, npart=npart, ndim=ndim, max_iter=niter, init=i, bounds=b, inertia=LinearInertia())
        elif (alg == "DE"):
            swarm = DE(obj=obj, npart=npart, ndim=ndim, max_iter=niter, init=i, bounds=b)
        elif (alg == "GWO"):
            swarm = GWO(obj=obj, npart=npart, ndim=ndim, max_iter=niter, init=i, bounds=b)
        elif (alg == "JAYA"):
            swarm = Jaya(obj=obj, npart=npart, ndim=ndim, max_iter=niter, init=i, bounds=b)
        elif (alg == "GA"):
            swarm = GA(obj=obj, npart=npart, ndim=ndim, max_iter=niter, init=i, bounds=b)

        st = time.time()
        swarm.Optimize()
        en = time.time()

        SetWeights(obj.snn, swarm.gpos[-1])
        prob = obj.snn.predict_proba(xtst)
        score= obj.snn.score(xtst, ytst)

        tn,fp,fn,tp,mcc = confmat(prob, ytst)
        TP.append(tp); TN.append(tn); FP.append(fp); FN.append(fn); T.append(en-st); SC.append(score)
        MCC.append(mcc)
        M.append(alg)

    #  Rank the results by MCC
    MCC = np.array(MCC)
    idx = np.argsort(1.0-MCC)
    MCC = MCC[idx]
    M = np.array(M)[idx]
    TP = np.array(TP)[idx]
    TN = np.array(TN)[idx]
    FP = np.array(FP)[idx]
    FN = np.array(FN)[idx]
    T = np.array(T)[idx]
    SC = np.array(SC)[idx]

    #  Results
    print()
    print("Ranked: (npart=%d, niter=%d)" % (npart, niter))
    print("  MCC       Score       TP   FP   FN   TN     time")
    for i in range(len(M)):
        print("%10.6f  %0.6f  %4d %4d %4d %4d %8.3f  %s" % (MCC[i],SC[i],TP[i],FP[i],FN[i],TN[i],T[i],M[i]))
    print()


if (__name__ == "__main__"):
    main()

