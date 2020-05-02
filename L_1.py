from pylab import sin, cos, math


def L_1_metric(p1, p2):  # manhattan distance
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def rotate_points(P, alpha):
    alpha_r = math.radians(alpha)
    P_new = []
    for (x, y) in P:
        P_new.append((x * cos(alpha_r) + y * sin(alpha_r), y * cos(alpha_r) - x * sin(alpha_r)))
    return P_new


def isTypeU(pu, pv):
    if pu[0] <= pv[0]:
        return pu[1] <= pv[1]
    return pv[1] <= pu[1]


def diameterL1(Pi):
    p1, p2 = diameter_extremes(Pi)
    return L_1_metric(p1, p2)


def diameter_extremes(Pi):  # TODO is correct?
    return Pi[0], Pi[-1]


def getS(P):
    pa = P[-1]  # we assume P is sorted descending by value x
    opt_i = 0
    opt_i_index = 0

    for i in range(1, len(P)):
        Pi = P[0:i]
        pi = P[i]
        v = min(L_1_metric(pa, pi), diameterL1(Pi))
        if v > opt_i:
            opt_i = v
            opt_i_index = i

    Pi = P[0:opt_i_index]
    p1, p2 = diameter_extremes(Pi)

    if isTypeU(p1, p2):
        return opt_i, (pa, min(Pi, key=lambda t: t[1]), max(Pi, key=lambda t: t[1]))

    return opt_i, (pa, min(Pi, key=lambda t: t[0]), max(Pi, key=lambda t: t[0]))  # typeD


def ThreeDispersionL1(P):
    val, S = [], []
    for angle in [45, 135, 225, 315]:
        v, s = getS(rotate_points(P, angle))  # sorted by x descending?
        val.append(v)
        S.append(s)

    return S[val.index(max(val))]


P = {(4, 1), (4, 2), (4, 3), (4, 4),
     (3, 1), (3, 2), (3, 3), (3, 4),
     (2, 1), (2, 2), (2, 3), (2, 4),
             (1, 2)}

S = ThreeDispersionL1(P)
print(S)
print(rotate_points(S, 315))
