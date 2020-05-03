# 3-Dispersion in L_2

from convexhull import grahamHull, union, diameter
from math import sqrt, ceil

class L2:
    def __init__(self):
        self.name = "3-dispersion in L2"
    
    def L2metric(self, x, y):
        return sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
    
    def getMaxMinDist(self, S):
        return min(self.L2metric(S[0],S[1]), self.L2metric(S[0],S[2]), self.L2metric(S[1],S[2]))

    
    def three_dispersion(self, P):
        assert len(P) >= 3

        opt_S = (P[0], P[1], P[2])
        opt_d = self.getMaxMinDist(opt_S)

        Porg = [p for p in P] # Naredimo kopijo P, ki ga bomo nato cel cas sortirali
        n = len(P) # oznacimo stevilo tock z n

        # Za vsak pa v P izracunamo maxmin S
        for pa in Porg:
            opt_pair = None
            opt_dist = -1
            P.sort(key=lambda p: self.L2metric(pa, p))
            I = [0, n-1]
            while I[1]-I[0] > -1:
                # TODO - premisli, ce je razlika = 1, torej imamo 2 elementa se
                # Izracunamo mediano zaporednih indeksov I ... mediana je tukaj enaka mean
                i = ceil((I[0]+I[1]) / 2)
                dpi = self.L2metric(pa, P[i]) # d(pa, pi)

                # Izracunajmo sedaj konveksno ovojnico Pi = P[i:]
                U, L = grahamHull(P[i:(I[1]+1)])
                if I[1] < n-1:
                    # Zdruzimo C in Cright, da dobimo CH(Pi)
                    U, L = union(U, L, Uright, Lright)
                
                if i == n-1:
                    # Smo na najbolj desni tocki, torej je I[0] = n-2, I[1] = n-1
                    d = self.getMaxMinDist((pa, P[-2], P[-1]))
                    if d > opt_d:
                        opt_pair = (pa, P[-2], P[-1])
                        opt_d = d
                    break
                
                pair, d = diameter(U, L)

                # Preverimo najprej, ce smo nasli novo najboljso vrednost
                di = min(dpi, d)
                if di > opt_dist:
                    opt_pair = pair
                    opt_dist = di

                if dpi < d:
                    # Razdalja do P[i] je strogo manjsa od razdalje d(pb,pc)
                    # Torej vemo, da resitev ni v levi polovici P[:i], temvec
                    # je v desni, ce je se nismo nasli ... pomaknemo se v desno polovico
                    I[0] = i+1
                    Uright = [] # Zgolj, da javi napako, ce algoritem ne bi deloval pravilno
                    Lright = []
                else:
                    # d(pa, P[i]) >= d(pb, pc) ... nadaljujemo iskanje v levi polovici
                    # Za nadaljne izracune bomo potrebovali trenutno konveksno ovojnico,
                    # ki jo bomo združili z ovojnico iz dobljenih podintervalov v linearnem casu
                    Uright = U
                    Lright = L
                    I[1] = i-1
            # Nasli smo optimalen par opt_pair za pa
            # Primerjajmo (pa, opt_pair) sedaj z opt_S
            dpa = self.getMaxMinDist((pa, opt_pair[0], opt_pair[1]))
            if dpa > opt_d:
                opt_S = (pa, opt_pair[0], opt_pair[1])
                opt_d = dpa
        return opt_S

L2 = L2()

P = [(0,0), (1,1), (3,2), (4,2)]
print(L2.three_dispersion(P))
print(L2.getMaxMinDist(((0, 0), (1, 1), (3, 2))))
print(L2.getMaxMinDist(((0, 0), (1, 1), (4, 2))))

P = [(0,0), (6,0), (3,0), (2,0), (1,0)]
print(L2.three_dispersion(P))