from pylab import sqrt


def L_2_metric(p1, p2):  # euclidean distance
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def getS(P):
    pass


def ThreeDispersionL2(P):
    pass


P = {(4, 1), (4, 2), (4, 3), (4, 4),
     (3, 1), (3, 2), (3, 3), (3, 4),
     (2, 1), (2, 2), (2, 3), (2, 4),
     (1, 1), (1, 2), (1, 3), (1, 4)}

S = ThreeDispersionL2(P)
