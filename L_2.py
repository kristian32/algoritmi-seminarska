from pylab import sqrt
from scipy.spatial import ConvexHull
from quickmedian import quickmedian


def L_2_metric(p1, p2):  # euclidean distance
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def diameter_L2(Pi):
    p1, p2 = diameter_extremes(Pi)
    return L_2_metric(p1, p2)


def diameter_extremes(Pi):  # TODO is it correct?
    return Pi[0], Pi[-1]


def sort_by_Pa(P, pa):
    P.sort(key=lambda p: L_2_metric(p, pa))
    return P


def three_dispersion_L2(P):
    i_opt = 0
    i_opt_index = 0
    pa_opt_index = 0

    for pa_index in range(len(P)):
        pa = P[pa_index]
        P_pa = sort_by_Pa(P, pa)

        # I = [i for i in range(1, len(P_pa))]
        # for i in I:  # TODO use quickmedian
        for i in range(1, len(P_pa)):
            # median_i = quickmedian(I, i)
            Pi = P_pa[0:i]
            pi = P_pa[i]

            # hull = ConvexHull(Pi)

            v = min(L_2_metric(pa, pi), diameter_L2(Pi))
            if v > i_opt:
                i_opt = v
                i_opt_index = i
                pa_opt_index = pa_index

    pa = P[pa_opt_index]
    Pi = P[0:i_opt_index]
    pb, pc = diameter_extremes(Pi)

    return pa, pb, pc


P = [(4, 1), (4, 2), (4, 3), (4, 4),
     (3, 1), (3, 2), (3, 3), (3, 4),
     (2, 1), (2, 2), (2, 3), (2, 4),
             (1, 2)]

S = three_dispersion_L2(P)
print(S)
