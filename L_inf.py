# 3-Dispersion in L_inf

def dinf(x, y):
    d = 0
    for i in range(len(x)):
        di = abs(x[i]-y[i])
        if di > d:
            d = di
    return d

def case14(P, dim=0):
    maxp = P[dim]
    minp = P[dim]
    for p in P:
        if p[dim] < minp[dim]:
            minp = p
        elif p[dim] > maxp[dim]:
            maxp = p
    dist = float("inf")
    pm = None
    midx = (maxp[dim]+minp[dim]) / 2 # x-coord. of midpoint between maxp and minp
    for p in P:
        dp = abs(midx - p[dim])
        if dp < dist:
            dist = dp
            pm = p
    return (minp, pm, maxp)

def case1(P):
    return case14(P, 0)

def case4(P):
    return case14(P, 1)

def case2left(P):
    # Case 2 where pa = pn (leftmost point) => (pb,pc) is type-V
    pa = min(P)