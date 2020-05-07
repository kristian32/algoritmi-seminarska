# 3-Dispersion in L_2

from convexhull import sweepHull, union, diameter
from math import ceil

class L2:
    def __init__(self):
        self.name = "3-dispersion in L2"
        self.metric = "$L_2$"
    
    @staticmethod
    def L2metric(x, y):
        return (x[0]-y[0])**2 + (x[1]-y[1])**2
    
    def getMaxMinDist(self, S):
        return min(self.L2metric(S[0],S[1]), self.L2metric(S[0],S[2]), self.L2metric(S[1],S[2]))

    def three_dispersion(self, Porg):
        assert len(Porg) >= 3 # Iscemo 3 tocke, ce jih toliko sploh ni, naloga nima smisla

        opt_S = (Porg[0], Porg[1], Porg[2])
        opt_d = self.getMaxMinDist(opt_S)

        P = [p for p in Porg] # Naredimo kopijo P, ki ga bomo nato cel cas sortirali
        n = len(P) # oznacimo stevilo tock z n

        # Za vsak pa v P izracunamo maxmin S
        for pa in Porg:
            Uright = None
            Lright = None

            P.sort(key=lambda p: self.L2metric(pa, p))
            I = [0, n-1]
            fromLeft = False
            while I[1]-I[0] > 0 or (fromLeft and I[1]-I[0] > -1):
                # Izracunamo mediano zaporednih indeksov I ... mediana je tukaj enaka mean
                i = ceil((I[0]+I[1]) / 2)
                dpi = self.L2metric(pa, P[i]) # d(pa, pi)

                # Izracunajmo sedaj konveksno ovojnico Pi = P[i:]
                U, L = sweepHull(P[i:(I[1]+1)])
                if I[1] < n-1:
                    # Zdruzimo C in Cright, da dobimo CH(Pi)
                    # Cright = (Uright, Lright) bo vedno obstajal, ko pridemo do te situacije
                    U, L = union(U, L, Uright, Lright)
                
                if i == n-1:
                    # Smo na najbolj desni tocki, torej je I[0] = n-2, I[1] = n-1
                    pb, pc = P[-2:]
                    break
                
                d, (pb,pc) = diameter(U, L)

                if dpi < d:
                    # Razdalja do P[i] je strogo manjsa od razdalje d(pb,pc)
                    # Torej vemo, da resitev ni v levi polovici P[:i], temvec
                    # je v desni, ce je se nismo nasli ... pomaknemo se v desno polovico
                    I[0] = i
                    fromLeft = False
                else:
                    # d(pa, P[i]) >= d(pb, pc) ... nadaljujemo iskanje v levi polovici
                    # Za nadaljne izracune bomo potrebovali trenutno konveksno ovojnico,
                    # ki jo bomo združili z ovojnico iz dobljenih podintervalov v linearnem casu
                    Uright = U
                    Lright = L
                    I[1] = i-1
                    fromLeft = True
            # Nasli smo optimalen par za pa, to sta (pb, pc)
            # Preverimo, ce je trojka (pa,pb,pc) najboljsa resitev do sedaj
            dpa = self.getMaxMinDist((pa,pb,pc))
            if dpa > opt_d:
                opt_S = (pa,pb,pc)
                opt_d = dpa
        return opt_S