from pylab import sin, cos, math


def L_1_metric(p1, p2):  # manhattan distance
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def rotate_points(P, alpha):
    alpha_r = math.radians(alpha)
    P_new = []
    for (x, y) in P:
        P_new.append((x * cos(alpha_r) + y * sin(alpha_r), y * cos(alpha_r) - x * sin(alpha_r)))
    return P_new


def is_type_U(pu, pv):
    if pu[0] <= pv[0]:
        return pu[1] <= pv[1]
    return pv[1] <= pu[1]


def diameter_L1(Pi):
    p1, p2 = diameter_extremes(Pi)
    return L_1_metric(p1, p2)


def diameter_extremes(Pi):  # TODO is it correct?
    return Pi[0], Pi[-1]


def get_S(P, pa_index):
    pa = P[pa_index]  # we assume P is sorted descending by value x
    opt_i = 0
    opt_i_index = 0

    for i in range(1, len(P)):
        if pa_index == -1:
            Pi = P[0:i]
            pi = P[i]
        else:
            Pi = P[-i:]
            pi = P[-i]

        v = min(L_1_metric(pa, pi), diameter_L1(Pi))
        if v > opt_i:
            opt_i = v
            opt_i_index = i

    if pa_index == -1:
        Pi = P[0:opt_i_index]
    else:
        Pi = P[-opt_i_index:]

    p1, p2 = diameter_extremes(Pi)

    index = 0  # typeD
    if is_type_U(p1, p2):
        index = 1

    min_pi = min(Pi, key=lambda t: t[index])
    max_pi = max(Pi, key=lambda t: t[index])

    if pa_index == -1:
        return opt_i, (pa, min_pi, max_pi)

    return opt_i, (pa, max_pi, min_pi)


def three_dispersion_L1(P):
    val, S = [], []
    angles = [-45, -135, -225, -315]
    for angle in angles:
        for pa_index in [0, -1]:  # min or max x value
            v, s = get_S(rotate_points(P, angle), pa_index)  # sorted by x descending?
            val.append(v)
            S.append(s)

    i = val.index(max(val))
    return rotate_points(S[i], -angles[i // 2])


P = {(4, 1), (4, 2), (4, 3), (4, 4),
     (3, 1), (3, 2), (3, 3), (3, 4),
     (2, 1), (2, 2), (2, 3), (2, 4),
             (1, 2)}

S = three_dispersion_L1(P)
print(S)
