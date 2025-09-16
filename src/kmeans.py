
from __future__ import annotations
from typing import List, Tuple
import random

Point = Tuple[float,float]

def kmeans(points: List[Point], k: int, max_iters: int = 100, seed: int = 42):
    rnd = random.Random(seed)
    cents = rnd.sample(points, k)
    labels = [0]*len(points)

    def d2(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2

    for _ in range(max_iters):
        changed = False
        for i,p in enumerate(points):
            best = min(range(k), key=lambda j: d2(p, cents[j]))
            if labels[i] != best:
                labels[i] = best; changed = True
        sums = [(0.0,0.0,0) for _ in range(k)]
        sx=[0.0]*k; sy=[0.0]*k; cnt=[0]*k
        for (x,y),lbl in zip(points, labels):
            sx[lbl]+=x; sy[lbl]+=y; cnt[lbl]+=1
        new_cents=[]
        for j in range(k):
            if cnt[j]==0:
                new_cents.append(points[rnd.randrange(len(points))])
            else:
                new_cents.append((sx[j]/cnt[j], sy[j]/cnt[j]))
        if not changed: break
        cents = new_cents
    return cents, labels
