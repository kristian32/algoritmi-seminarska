# 3-Dispersion in L_1

from math import sin, cos, radians
from quickmedian import quickmedian

class L1v2:
    def __init__(self):
        self.name = "3-dispersion in L1"
        self.metric = "$L_1$"

    @staticmethod
    def L_1_metric(p1, p2):  # manhattan distance
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def getMaxMinDistList(S):
        SS = [L1v2.L_1_metric(S[0], S[1]), L1v2.L_1_metric(S[0], S[2]), L1v2.L_1_metric(S[1], S[2])]
        SS.sort(reverse=True)
        return SS

    @staticmethod
    def getMaxMinDist(S):
        return min(L1v2.L_1_metric(S[0], S[1]), L1v2.L_1_metric(S[0], S[2]), L1v2.L_1_metric(S[1], S[2]))

    @staticmethod
    def rotate_points(P, alpha):
        alpha_r = radians(alpha)
        P_new = [None] * len(P)
        c = cos(alpha_r)
        s = sin(alpha_r)
        for i in range(len(P)):
            x,y = P[i]
            P_new[i] = (x*c-y*s, y*c+x*s)
        return P_new

    def is_type_U(self, pu, pv):
        if pu[0] <= pv[0]:
            return pu[1] <= pv[1]
        return pv[1] <= pu[1]

    def get_S(self, P, smallest):

        assert len(P) >= 3  # Ce nimamo vsaj 3 tock, problem ni smiselen

        fact = 1 if smallest else -1  # Faktor ... 1 = pa je min, -1 = pa je max, torej samo prezrcalimo tocke preko y-osi (dim=0) oz. x-osi (dim=1)
        pa = max(P, key=lambda x: fact * x[0])  # Zacetna tocka

        key_dim = lambda x:  L1v2.L_1_metric(pa, x)  # Kljuc za primerjanje v dimenziji (dim)
        key1 = lambda x: x[1] # Uporabljamo samo zato, ker je sicer VSC pobarval spodaj kot napako, ceprav je ni bilo, in je bilo nadlezno

        pl = pa
        ph = pa

        wentRight = False

        pcD = max(P, key=lambda x: x[0]) # vedno najbolj desna tocka
        hright = None
        lright = None

        while len(P) > 1:
            pi = quickmedian(P, key_dim)
            pi_key = key_dim(pi)
            Pi = [pi] + [p for p in P if key_dim(p) > pi_key]  # Pi ... tocke, ki so od pa oddaljene vsaj toliko kot pi | ce obstaja vec tock enakih pi, jih pobrisemo

            dpi = L1v2.L_1_metric(pa, pi)  # d(pa,pi)

            # type U
            pbU = min(Pi, key=lambda x: x[1])
            if lright is not None and key1(lright) < pbU[1]:
                pbU = lright
            pcU = max(Pi, key=lambda x: x[1])
            if hright is not None and key1(hright) > pcU[1]:
                pcU = hright
            # type D
            pbD = pi

            U = L1v2.L_1_metric(pbU, pcU)
            D = L1v2.L_1_metric(pbD, pcD)

            if U > D:
                pl = pbU
                ph = pcU
                diam = U
            else:
                pl = pbD
                ph = pcD
                diam = D

            if dpi < diam:
                # Iskanje se bo nadaljevalo v desni polovici Pi
                P = Pi
                wentRight = True
            else:
                # Iskanje se bo nadaljevalo v levi polovici Pi
                P = [p for p in P if key_dim(p) < pi_key]
                hright = pcU
                lright = pbU
                wentRight = False

        if wentRight and hright is not None:
            # Na zadnjem koraku smo zeleli iti desno, torej je d(pa,pi) < diam(Pi)
            # Mozno je torej, da je optimalna resitev bila bolj desno od nase trenutne
            return max([(pa, pl, ph), (pa, pl, hright), (pa, lright, ph), (pa, lright, hright)], key=L1v2.getMaxMinDist)
        else:
            # Na zadnjem koraku smo sli v levo polovico, torej d(pa,pi) >= diam(Pi)
            # V levi polovici je tocka P[0], preverimo, ce je boljsa od pl/ph
            return max([(pa, pl, ph), (pa, pl, P[0]), (pa, P[0], ph)], key=L1v2.getMaxMinDist)

    def three_dispersion(self, P):
        val = []
        angles = [-45, -135, -225, -315]
        for angle in angles:
            for pa_index in [True, False]:  # min or max x value
                P_rot = self.rotate_points(P, angle)
                s = self.get_S(P_rot, pa_index)  # sorted by x descending?
                s_rot = self.rotate_points(s, -angle)
                val.append(s_rot)
        return max(val, key=lambda x: self.getMaxMinDist(x))