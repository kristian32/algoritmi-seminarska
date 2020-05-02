# 3-Dispersion in L_inf

from quickmedian import quickmedian

def dinf(x, y):
    d = 0
    for i in range(len(x)):
        di = abs(x[i]-y[i])
        if di > d:
            d = di
    return d

def getLowHigh(xs, dim=0):
    # Vrne tocko z max vrednostjo v dimenziji dim in z min vrednostjo v tej dimenziji
    assert len(xs) > 1
    low = xs[0]
    high = xs[0]
    for x in xs:
        if x[dim] < low[dim]:
            low = x
        elif x[dim] > high[dim]:
            high = x
    return low, high

def getBestDist(l, h, pa, pl, ph, pd, dim=0):
    dist_lh = min(min(l[dim],h[dim])-pa[dim], h[1-dim] - l[1-dim])
    dist_lph = min(min(l[dim],ph[dim])-pa[dim], ph[1-dim]-l[1-dim])
    dist_plh = min(min(pl[dim],h[dim])-pa[dim], h[1-dim]-pl[dim])
    dist = max(pd, dist_lh, dist_lph, dist_plh)
    if dist_lh == dist:
        # l in h sta nova najbolja izbira
        pl = l
        ph = h
        pd = dist
    elif dist_lph == dist:
        # l in ph je nova najboljsa izbira
        pl = l
        pd = dist
    elif dist_plh == dist:
        # pl in h je nova najboljsa izbira
        ph = h
        pd = dist
    return pl, ph, pd

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

def case23left(P, dim=0):
    # Case 2 where pa = pn (leftmost point) => (pb,pc) is type-V
    pa = min(P, key=lambda x: x[dim])
    pl = min(P, key=lambda x: (x[1-dim], -x[dim]))
    ph = max(P, key=lambda x: (x[1-dim], x[dim]))
    pd = min(min(pl[dim], ph[dim]), ph[1-dim] - pl[1-dim])

    medp = quickmedian([p[dim] for p in P])
    Pright = [p for p in P if p[dim] > medp] # Desna polovica mnozice P glede na x
    while len(Pright) > 1 or (len(Pright) == 0 and len(P) > 1):
        if len(Pright) == 0:
            # Robni primer, kjer so vse tocke v levi polovici, ali pa imajo
            # x-koordinato enako mediani
            # Najprej poizkusimo za Pmedian
            Pmedian = [p for p in P if p[dim] == medp]
            l, h = getLowHigh(Pmedian, 1-dim)
            pl, ph, pd = getBestDist(l, h, pa, pl, ph, pd, dim)
            P = [p for p in P if p[dim] < medp]
        else:
            l, h = getLowHigh(Pright, 1-dim)
            pl, ph, pd = getBestDist(l, h, pa, pl, ph, pd, dim)
            if medp - pa[dim] < h[1-dim] - l[1-dim]:
                # Vemo, da se lahko pomaknemo strogo desno
                P = Pright
            else:
                # Nadaljujemo iskanje v levi polovici P
                P = [p for p in P if p[dim] <= medp]
        medp = quickmedian([p[dim] for p in P]) # Mediana po x
        Pright = [p for p in P if p[dim] > medp] # Desna polovica mnozice P glede na x
    return (pa,pl,ph), pd

P = [(0,0), (1,1), (1.5,-1), (5, -5), (6, 5), (7, -1), (8, 1)]
print(case23left(P))
P1 = [(y,x) for x,y in P]
print(case23left(P1, 1))
print()

P = [(0,0), (1,1), (1,-1), (1,3)]
print(case23left(P))
P1 = [(y,x) for x,y in P]
print(case23left(P1, 1))
print()

P = [(0,0), (2,10), (3,-10), (5,1), (5,-1), (5,3)]
print(case23left(P))
P1 = [(y,x) for x,y in P]
print(case23left(P1, 1))
print()

P = [(0,0), (1,-10), (2,10), (100,-5), (101,0), (102,5), (103,0), (104,0), (105,0)]
print(case23left(P))
P1 = [(y,x) for x,y in P]
print(case23left(P1, 1))
print()

P = [(0,0), (1,-10), (2,10), (100,3), (100,2), (100,1), (100,-3)]
print(case23left(P))
P1 = [(y,x) for x,y in P]
print(case23left(P1, 1))
print()