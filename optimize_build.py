import sys
import random
import math
import copy
import glob
import numpy as np
import os

# fix random seed
random.seed(10)
# build id
ID_=int(sys.argv[1])
# number of builds
N_=int(sys.argv[2])
# CACHE running time
CACHE_=float(sys.argv[3])
# lessons/eggs yml
YML_=sys.argv[4:]
# number of projects
NP_=len(YML_)
# MC parameter
KBT_=1.0

# calculate score from batch
def get_score(batch, rtime):
    m = N_* [0.0]
    for i in range(N_):
        for j in batch[i]:
            m[i] += rtime[j]
        # add cache time
        if(i==0): m[i] += CACHE_
    # calculate score
    s = max(m)
    # return score
    return s

# MC accept
def accept_or_reject(x, x_new, ene, e_new, kbt):
    ac = 0.0
    delta = (e_new-ene)/kbt
    # downhill move -> always accepted
    if(delta<0.):
      ene = e_new
      x = copy.deepcopy(x_new)
      ac = 1.0
    # uphill move -> accept with certain probability
    else:
       r = random.random()
       delta = math.exp(-delta)
       if(r < delta):
          ene = e_new
          x = copy.deepcopy(x_new)
          ac = 1.0
    return x, ene, ac

# read timing data file
rlab=[]; rtime=[]
try:
 for lines in open("timing", "r").readlines():
     riga=lines.strip().split()
     # add label
     rlab.append(riga[0])
     # add timing
     rtime.append(float(riga[1]))
except:
 pass

# calculate average time
if(len(rtime)>0):
 rave = np.mean(np.array(rtime))
else:
 rave = 1.0
# fill missing entries
label = rlab.copy()
for p in YML_:
    if p not in label:
       rlab.append(p)
       rtime.append(rave)

# prepare batches
batch = [ [] for i in range(N_) ]
# initialize batches with vanilla assignment
for i in range(NP_):
    ii = i % N_
    batch[ii].append(i)

# get initial score
score = get_score(batch, rtime)
# initialize acceptance
acc = 0.0
# initializing best
score_best = score
batch_best = copy.deepcopy(batch)
#
# loop over MC steps
for istep in range(100000):
    # propose move
    batch_new = copy.deepcopy(batch)
    # pick random origin batch with at least 2 entries
    ii = [ i for i in range(N_) if len(batch[i])>1 ]
    # random choice 
    i = random.choice(ii)
    # pick random entry in i-th batch
    j = random.randrange(len(batch[i]))
    # pick random destination batch
    d = list(range(N_))
    # remove origin batch
    d.remove(i)
    # choose randomly
    k = random.choice(d)
    # add to k-th batch
    batch_new[k].append(batch_new[i][j])
    # remove from i-th batch
    batch_new[i].pop(j)
    # calculate new score
    score_new = get_score(batch_new, rtime)
    # accept or reject
    batch, score, ac = accept_or_reject(batch, batch_new, score, score_new, KBT_)
    # increase acceptance
    acc += ac 
    # save best
    if(score<score_best):
      score_best = score
      batch_best = copy.deepcopy(batch)

# write pathlist only for ID_ replica
fp = open("pathlist"+str(ID_), "w")
# loop on batch
for j in batch_best[ID_]:
    # write path
    fp.write("%s\n" % rlab[j])
