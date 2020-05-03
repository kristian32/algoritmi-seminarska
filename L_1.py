# 3-Dispersion in L_1

from math import sin, cos, radians

class L1:
    def __init__(self):
        self.name = "3-dispersion in L1"

    @staticmethod
    def L_1_metric(p1, p2):  # manhattan distance
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    @staticmethod
    def rotate_points(P, alpha):
        alpha_r = radians(alpha)
        P_new = []
        for (x, y) in P:
            P_new.append((x * cos(alpha_r) + y * sin(alpha_r), y * cos(alpha_r) - x * sin(alpha_r)))
        return P_new

    def is_type_U(self, pu, pv):
        if pu[0] <= pv[0]:
            return pu[1] <= pv[1]
        return pv[1] <= pu[1]

    def diameter_L1(self, Pi):
        p1, p2 = self.diameter_extremes(Pi)
        return self.L_1_metric(p1, p2)

    def diameter_extremes(self, Pi):
        return Pi[0], Pi[-1]

    def get_S(self, P, pa_index):
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

            v = min(self.L_1_metric(pa, pi), self.diameter_L1(Pi))
            if v > opt_i:
                opt_i = v
                opt_i_index = i

        if pa_index == -1:
            p1, p2 = self.diameter_extremes(P[0:opt_i_index])
        else:
            p1, p2 = self.diameter_extremes(P[-opt_i_index:])

        index = 0  # typeD
        if self.is_type_U(p1, p2):
            index = 1

        if p1[index] > p2[index]:
            min_pi = p2
            max_pi = p1
        else:
            min_pi = p1
            max_pi = p2

        if pa_index == -1:
            return opt_i, (pa, min_pi, max_pi)

        return opt_i, (pa, max_pi, min_pi)

    def getMaxMinDist(self, S):
        return min(self.L_1_metric(S[0], S[1]), self.L_1_metric(S[0], S[2]), self.L_1_metric(S[1], S[2]))

    def three_dispersion(self, P):
        val, S = [], []
        angles = [-45, -135, -225, -315]
        for angle in angles:
            for pa_index in [0, -1]:  # min or max x value
                P_rot = self.rotate_points(P, angle)  # we rotate P
                # P_rot_sorted = sorted(P_rot, key=lambda tup: self.L_1_metric(tup, P_rot[pa_index]), reverse=False)  # we assume them as sorted
                P_rot_sorted = sorted(P_rot, key=lambda tup: (tup[0], tup[1]), reverse=True)  # we assume them as sorted
                v, s = self.get_S(P_rot_sorted, pa_index)  # sorted by x descending?
                val.append(v)
                S.append(self.rotate_points(s, -angle))

        return max(S, key=lambda Si: self.getMaxMinDist(Si))
