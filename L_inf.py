# 3-Dispersion in L_inf

from quickmedian import quickmedian

def getBestDist(l, h, pa, pl, ph, pd, dim=0):
    dist_lh = min(min(abs(pa[dim]-l[dim]), abs(pa[dim]-h[dim])), h[1-dim]-l[1-dim])
    dist_lph = min(min(abs(pa[dim]-l[dim]), abs(pa[dim]-ph[dim])), ph[1-dim]-l[1-dim])
    dist_plh = min(min(abs(pa[dim]-pl[dim]), abs(pa[dim]-h[dim])), h[1-dim]-pl[1-dim])
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

def getPnext(P, medp, dim, smallest):
    return [p for p in P if p[dim] > medp] if smallest else [p for p in P if p[dim] < medp]

def case23(P, dim=0, smallest=True):
    '''Case 2 za dim=0 in Case 3 za dim=1.
    Če smallest, potem je pa tocka z najmanjso dim-koordinato (za dim=0 je pa=pn),
    sicer je tocka z najvecjo dim-koordinato (za dim=0 je pa=p1).'''
    fact = 1 if smallest else -1 # Factor for multiplications
    pa = min(P, key=lambda x: x[dim]) if smallest else max(P, key=lambda x: x[dim])# pa je skrajna tocka v dim => (pb,pc) je type-V
    pl = min(P, key=lambda x: (x[1-dim], -fact * x[dim]))
    ph = max(P, key=lambda x: (x[1-dim], fact * x[dim]))
    pd = min(min(abs(pa[dim]-pl[dim]), abs(pa[dim]-ph[dim])), ph[1-dim]-pl[1-dim])

    medp = quickmedian([p[dim] for p in P])
    Pnext = getPnext(P, medp, dim, smallest) # Razdelimo P na pol, vzamemo "naslednjo" polovico
    while len(Pnext) > 1 or (len(Pnext) == 0 and len(P) > 2):
        if len(Pnext) == 0:
            # Robni primer, kjer so vse tocke v "non-next" polovici
            # Ker je teh tock >2, imamo vec vrednosti z dim-koordinato enako medp
            # Najprej poizkusimo za Pmedian
            Pmedian = [p for p in P if p[dim] == medp]
            # Vse tocke iz Pmedian imajo isto dim-koordinato
            l = min(Pmedian, key=lambda x: x[1-dim])
            h = max(Pmedian, key=lambda x: x[1-dim])
            pl, ph, pd = getBestDist(l, h, pa, pl, ph, pd, dim)
            P = [p for p in P if p[dim] < medp] if smallest else [p for p in P if p[dim] > medp]
        else:
            # Preverimo, ce je boljsa resitev v Pnext
            l = min(Pnext, key=lambda x: (x[1-dim], -fact * x[dim])) # Zelimo najnizjo tocko ... ce jih je vec, tisto, ki je najdlje od pa horizontalno
            h = max(Pnext, key=lambda x: (x[1-dim], fact * x[dim]))
            pl, ph, pd = getBestDist(l, h, pa, pl, ph, pd, dim)
            if abs(pa[dim]-medp) < h[1-dim]-l[1-dim]:
                # Vemo, da se lahko pomaknemo strogo v smeri "next"
                P = Pnext
            else:
                # Nadaljujemo iskanje v "non-next" polovici P
                P = [p for p in P if p[dim] <= medp] if smallest else [p for p in P if p[dim] >= medp]
        medp = quickmedian([p[dim] for p in P]) # Mediana po x
        Pnext = getPnext(P, medp, dim, smallest) # Desna polovica mnozice P glede na x
    return (pa,pl,ph), pd

def case1(P):
    return case14(P, 0)

def case2(P):
    S1, d1 = case23(P, 0, True)
    S2, d2 = case23(P, 0, False)
    return S1 if d1 > d2 else S2

def case3(P):
    S1, d1 = case23(P, 1, True)
    S2, d2 = case23(P, 1, False)
    return S1 if d1 > d2 else S2

def case4(P):
    return case14(P, 1)

P = [(0,0), (1,1), (1.5,-1), (5, -5), (6, 5), (7, -1), (8, 1)]
print(case23(P))
P1 = [(y,x) for x,y in P]
print(case23(P1, 1))
P2 = [(-x,y) for x,y in P]
print(case23(P2, smallest=False))
print()

P = [(0,0), (1,1), (1,-1), (1,3)]
print(case23(P))
P1 = [(y,x) for x,y in P]
print(case23(P1, 1))
P2 = [(-x,y) for x,y in P]
print(case23(P2, smallest=False))
print()

P = [(0,0), (2,10), (3,-10), (5,1), (5,-1), (5,3)]
print(case23(P))
P1 = [(y,x) for x,y in P]
print(case23(P1, 1))
P2 = [(-x,y) for x,y in P]
print(case23(P2, smallest=False))
print()

P = [(0,0), (1,-10), (2,10), (100,-5), (101,0), (102,5), (103,0), (104,0), (105,0)]
print(case23(P))
P1 = [(y,x) for x,y in P]
print(case23(P1, 1))
P2 = [(-x,y) for x,y in P]
print(case23(P2, smallest=False))
print()

P = [(0,0), (1,-10), (2,10), (100,3), (100,2), (100,1), (100,-3)]
print(case23(P))
P1 = [(y,x) for x,y in P]
print(case23(P1, 1))
P2 = [(-x,y) for x,y in P]
print(case23(P2, smallest=False))
print()