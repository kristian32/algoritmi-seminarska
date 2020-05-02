from pylab import sqrt
from scipy.spatial import ConvexHull
from quickmedian import quickmedian


class L2:
    def __init__(self):
        self.name = "3-dispersion in L2"

    def L_2_metric(self, p1, p2):  # euclidean distance
        return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def diameter_L2(self, Pi):
        p1, p2 = self.diameter_extremes(Pi)
        return self.L_2_metric(p1, p2)

    def diameter_extremes(self, Pi):  # TODO is it correct?
        return Pi[0], Pi[-1]

    def sort_by_Pa(self, P, pa):
        P.sort(key=lambda p: self.L_2_metric(p, pa))
        return P

    def three_dispersion(self, P):
        i_opt = 0
        i_opt_index = 0
        pa_opt_index = 0

        for pa_index in range(len(P)):
            pa = P[pa_index]
            P_pa = self.sort_by_Pa(P, pa)

            # I = [i for i in range(1, len(P_pa))]
            # for i in I:  # TODO use quickmedian
            for i in range(1, len(P_pa)):
                # median_i = quickmedian(I, i)
                Pi = P_pa[0:i]
                pi = P_pa[i]

                # hull = ConvexHull(Pi)

                v = min(self.L_2_metric(pa, pi), self.diameter_L2(Pi))
                if v > i_opt:
                    i_opt = v
                    i_opt_index = i
                    pa_opt_index = pa_index

        pa = P[pa_opt_index]
        Pi = P[0:i_opt_index]
        pb, pc = self.diameter_extremes(Pi)

        return pa, pb, pc
