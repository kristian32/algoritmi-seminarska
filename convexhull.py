# All Convex Hull functions needed for L2

__all__ = ["grahamHull", "union", "diameter"]

def orientation(p, q, r):
    '''Vrne pozitivno vrednost, ce je <p,q,r> usmerjen v smeri urinega kazalca,
    vrne negativno, ce je v nasprotni smeri urinega kazalca in 0, ce so tocke kolinearne.'''
    return (q[1]-p[1])*(r[0]-p[0]) - (q[0]-p[0])*(r[1]-p[1])

def grahamHull(P):
    '''Grahamov algoritem za iskanje zgornje in spodnje konveksne ovojnice.'''
    U = []
    L = []
    P.sort()
    for p in P:
        while len(U) > 1 and orientation(U[-2],U[-1],p) <= 0: U.pop()
        while len(L) > 1 and orientation(L[-2],L[-1],p) >= 0: L.pop()
        U.append(p)
        L.append(p)
    return U,L

def sweepHull(D, upper=True):
    '''Sweep algoritem za urejena seznama tock
    zgornje in spodnje ovojnice, ki potrebuje linearen cas.'''
    if len(D) <= 2:
        # D ima najvec 2 elementa, torej je ze konveksna ovojnica
        return D
    E = [D[0], D[1]]
    if upper:
        for d in D[2:]:
            while len(E) >= 2 and orientation(E[-2], E[-1], d) <= 0:
                E.pop()
            E.append(d)
    else:
        for d in D[2:]:
            while len(E) >= 2 and orientation(E[-2], E[-1], d) >= 0:
                E.pop()
            E.append(d)
    return E

def merge(S1, S2):
    '''Zdruzi 2 po velikosti urejena seznama v linearnem casu.
    Uporabljamo za zdruzevanje 2 zgornjih ali 2 spodnjih ovojnic.'''
    n = len(S1) + len(S2)
    S = [None]*n
    i = 0
    j = 0
    S1 += [(float("inf"),0)]
    S2 += [(float("inf"),0)]
    for k in range(n):
        if S1[i][0] <= S2[j][0]:
            S[k] = S1[i]
            i += 1
        else:
            S[k] = S2[j]
            j += 1
    return S

def union(U1, L1, U2, L2):
    '''Sprejme 2 zgornji in 2 spodnji ovojnici, ki pripadata 2 konveksnima
    ovojnicama. Vrne zgornjo in spodnjo konveksno ovojnico unije
    zacetnih ovojnic.'''
    if len(U1) + len(L1) == 0 or len(U2) + len(L2) == 0:
        # Ena izmed konveksnih ovojnic je prazna
        # Vrni neprazno
        return U1+U2, L1+L2
    elif len(U1) == 1 and len(L1) == 1:
        if len(U2) == 1 and len(L2) == 1:
            # Obe konveksni ovojnici vsebujeta le 1 element
            if U1[0] == U2[0]:
                # Ta element je enak, torej gre za isto ovojnico
                return U1, L1
            else:
                # Ovojnica je daljica
                temp = [min(U1[0], U2[0]), max(U1[0], U2[0])]
                return temp, temp
    U = merge(U1,U2)
    L = merge(L1,L2)
    return sweepHull(U), sweepHull(L)

def rotatingCalipers(U, L):
    '''Uporabi algoritem "rotatingCalipers" za izracun parov ekstremnih tock
    mnozice P v vseh smereh.'''
    i = 0
    j = len(L) - 1
    while i < len(U) - 1 or j > 0:
        yield U[i], L[j]
        
        # if all the way through one side of hull, advance the other side
        if i == len(U) - 1: j -= 1
        elif j == 0: i += 1
        
        # still points left on both lists, compare slopes of next hull edges
        # being careful to avoid divide-by-zero in slope calculation
        elif (U[i+1][1]-U[i][1])*(L[j][0]-L[j-1][0]) > \
                (L[j][1]-L[j-1][1])*(U[i+1][0]-U[i][0]):
            i += 1
        else: j -= 1

def diameter(U, L):
    '''Vrne premer mnozice P, tj. par tock, ki je najbolj oddaljen v P.'''
    diam, pair = max([((p[0]-q[0])**2 + (p[1]-q[1])**2, (p,q))
                     for p,q in rotatingCalipers(U, L)])
    return pair, diam