# 3-Dispersion in L_inf

from quickmedian import quickmedian

class Linf:
    def __init__(self):
        self.name = "3-dispersion in Linf"
        self.metric = "$L_{\\infty}$"

    def getBestDist(self, l, h, pa, pl, ph, pd, dim=0):
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

    def case14(self, P, dim=0):
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

    def getPnext(self, P, medp, dim, smallest):
        return [p for p in P if p[dim] > medp] if smallest else [p for p in P if p[dim] < medp]

    def case23(self, P, dim=0, smallest=True):
        '''Case 2 za dim=0 in Case 3 za dim=1.
        Če smallest, potem je pa tocka z najmanjso dim-koordinato (za dim=0 je pa=pn),
        sicer je tocka z najvecjo dim-koordinato (za dim=0 je pa=p1).'''
        fact = 1 if smallest else -1 # Factor for multiplications
        pa = min(P, key=lambda x: x[dim]) if smallest else max(P, key=lambda x: x[dim])# pa je skrajna tocka v dim => (pb,pc) je type-V
        pl = min(P, key=lambda x: (x[1-dim], -fact * x[dim]))
        ph = max(P, key=lambda x: (x[1-dim], fact * x[dim]))
        pd = min(min(abs(pa[dim]-pl[dim]), abs(pa[dim]-ph[dim])), ph[1-dim]-pl[1-dim])

        medp = quickmedian([p[dim] for p in P])
        Pnext = self.getPnext(P, medp, dim, smallest) # Razdelimo P na pol, vzamemo "naslednjo" polovico
        while len(Pnext) > 1 or (len(Pnext) == 0 and len(P) > 2):
            if len(Pnext) == 0:
                # Robni primer, kjer so vse tocke v "non-next" polovici
                # Ker je teh tock >2, imamo vec vrednosti z dim-koordinato enako medp
                # Najprej poizkusimo za Pmedian
                Pmedian = [p for p in P if p[dim] == medp]
                # Vse tocke iz Pmedian imajo isto dim-koordinato
                l = min(Pmedian, key=lambda x: x[1-dim])
                h = max(Pmedian, key=lambda x: x[1-dim])
                pl, ph, pd = self.getBestDist(l, h, pa, pl, ph, pd, dim)
                P = [p for p in P if p[dim] < medp] if smallest else [p for p in P if p[dim] > medp]
                if len(P) < 2:
                    break
            else:
                # Preverimo, ce je boljsa resitev v Pnext
                l = min(Pnext, key=lambda x: (x[1-dim], -fact * x[dim])) # Zelimo najnizjo tocko ... ce jih je vec, tisto, ki je najdlje od pa horizontalno
                h = max(Pnext, key=lambda x: (x[1-dim], fact * x[dim]))
                pl, ph, pd = self.getBestDist(l, h, pa, pl, ph, pd, dim)
                if abs(pa[dim]-medp) < h[1-dim]-l[1-dim]:
                    # Vemo, da se lahko pomaknemo strogo v smeri "next"
                    P = Pnext
                else:
                    # Nadaljujemo iskanje v "non-next" polovici P
                    P = [p for p in P if p[dim] <= medp] if smallest else [p for p in P if p[dim] >= medp]
            medp = quickmedian([p[dim] for p in P]) # Mediana po x
            Pnext = self.getPnext(P, medp, dim, smallest) # Desna polovica mnozice P glede na x
        return (pa,pl,ph)
    
    def LinfMetric(self, x, y):
        return max(abs(x[0]-y[0]), abs(x[1]-y[1]))

    def getMaxMinDist(self, S):
        return min(self.LinfMetric(S[0],S[1]), self.LinfMetric(S[0],S[2]), self.LinfMetric(S[1],S[2]))
    
    def three_dispersion(self, P):
        # Vrne 3-disperzijo za metriko Linf in mnozico 2-dimenzionalnih tock P
        # Izracuna disperzijo za vse mozne primere ter izbere najboljso moznost
        Slist = [self.case14(P, 0), self.case23(P, 0, True), self.case23(P, 0, False),
                self.case23(P, 1, True), self.case23(P, 1, False), self.case14(P, 1)]
        return max(Slist, key=lambda S: self.getMaxMinDist(S))