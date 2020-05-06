# 3-Dispersion in L_inf

from quickmedian import quickmedian

class Linf:
    def __init__(self):
        self.name = "3-dispersion in Linf"
        self.metric = "$L_{\\infty}$"
    
    @staticmethod
    def LinfMetric(x, y):
        return max(abs(x[0]-y[0]), abs(x[1]-y[1]))

    @staticmethod
    def getMaxMinDist(S):
        return min(Linf.LinfMetric(S[0],S[1]), Linf.LinfMetric(S[0],S[2]), Linf.LinfMetric(S[1],S[2]))

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

    def case23(self, P, dim=0, smallest=True):
        '''Case 2: imamo bodisi 2x H 1x V (dim=0), ali ravno obratno (dim=1).
        pa je bodisi najmanjsa vrednost (smallest), ali najvecja (!smallest).'''

        assert len(P) >= 3 # Ce nimamo vsaj 3 tock, problem ni smiselen

        fact = 1 if smallest else -1 # Faktor ... 1 = pa je min, -1 = pa je max, torej samo prezrcalimo tocke preko y-osi (dim=0) oz. x-osi (dim=1)
        key_dim = lambda x: (fact * x[dim], x[1-dim]) # Kljuc za primerjanje v dimenziji (dim)
        key_max = lambda x: (x[1-dim], fact * x[dim]) # Kljuc za primerjanje v dimenziji (1-dim) za max
        key_min = lambda x: (x[1-dim], -fact * x[dim]) # Kljuc za primerjanje v dimenziji (1-dim) za min
        
        pa = min(P, key=key_dim) # Zacetna tocka

        Pi = P # Pi je na zacetku kar celotna množica
        pl = pa
        ph = pa

        hright = None
        lright = None

        wentRight = False
        
        while len(P) > 1:
            pi = quickmedian(P, key_dim)
            pi_key = key_dim(pi)
            Pi = [pi] + [p for p in P if key_dim(p) > pi_key] # Pi ... tocke, ki so od pa oddaljene vsaj toliko kot pi | ce obstaja vec tock enakih pi, jih pobrisemo

            # Posodobimo / pobrisemo pl/ph, ce nista znotraj Pi
            if pi_key > key_dim(pl):
                pl = pi if lright is None else lright
            if pi_key > key_dim(ph):
                ph = pi if hright is None else hright
            
            # Poiscemo ekstremni tocki v (1-dim) dimenziji
            l = min(Pi, key=key_min)
            h = max(Pi, key=key_max)
            pl = l if key_min(l) < key_min(pl) else pl
            ph = h if key_max(h) > key_max(ph) else ph

            # Sedaj se moramo odlociti, kako nadaljevati
            diam = ph[1-dim]-pl[1-dim] # diam(Pi)
            dpi = abs(pa[dim]-pi[dim]) # d(pa,pi)
            if dpi < diam:
                # Iskanje se bo nadaljevalo v desni polovici Pi
                P = Pi
                wentRight = True
            else:
                # Iskanje se bo nadaljevalo v levi polovici Pi
                P = [p for p in P if key_dim(p) < pi_key]
                hright = ph
                lright = pl
                wentRight = False
        if wentRight:
            # Na zadnjem koraku smo zeleli iti desno, torej je d(pa,pi) < diam(Pi)
            # Mozno je torej, da je optimalna resitev bila bolj desno od nase trenutne
            return max([(pa,pl,ph), (pa,pl,hright), (pa,lright,ph), (pa,lright,hright)], key=Linf.getMaxMinDist)
        else:
            # Na zadnjem koraku smo sli v levo polovico, torej d(pa,pi) >= diam(Pi)
            # V levi polovici je tocka P[0], preverimo, ce je boljsa od pl/ph
            return max([(pa, pl, ph), (pa, pl, P[0]), (pa, P[0], ph)], key=Linf.getMaxMinDist)

    def three_dispersion(self, P):
        # Vrne 3-disperzijo za metriko Linf in mnozico 2-dimenzionalnih tock P
        # Izracuna disperzijo za vse mozne primere ter izbere najboljso moznost
        Slist = [self.case14(P, 0), self.case23(P, 0, True), self.case23(P, 0, False),
                self.case23(P, 1, True), self.case23(P, 1, False), self.case14(P, 1)]
        return max(Slist, key=Linf.getMaxMinDist)