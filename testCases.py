import glob
import matplotlib.pyplot as plt
import time
from numpy.ma import sqrt
from L_1 import L1
from L_2 import L2
from L_inf import Linf


def calculate(P, metric):
    start = time.time()
    print(metric.name)
    print("Given set of ", len(P), " points")

    S = metric.three_dispersion(P)
    print("The optimal result is: ", S)

    end = time.time()
    print("Time elapsed: ", end - start, "\n")

    return S, end - start


def show_plot(points_x, points_y, Sx, Sy, title="", xlabel="", ylabel=""):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    plt.scatter(points_x, points_y, s=100, marker='o', color='b')
    plt.scatter(Sx, Sy, s=100, marker='o', color='r')

    l, r = ax.get_xlim()
    left, right = min(l, -l/5), max(r + 1, 1)
    l, h = ax.get_ylim()
    low, high = min(l, -l/5), max(h + 1, 1)

    plt.arrow(left, 0, right - left, 0, length_includes_head=True, head_width=0.15)
    plt.arrow(0, low, 0, high - low, length_includes_head=True, head_width=0.15)

    plt.xlim(left, right)
    plt.ylim(low, high)

    plt.title(title, y=1.08)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.grid()
    plt.show()


def get_x_y_values(P):
    Px, Py = [], []
    for p in P:
        Px.append(p[0])
        Py.append(p[1])
    return Px, Py


def show_measured_time_by_P_size():
    P_length = [len(p) for p, p_name in P]
    for i in range(len(measured_times[::len(P)])):
        measured_for_metric = measured_times[i::len(metrics)]
        show_plot(measured_for_metric, P_length, [], [], metrics[i].name, "time [ms]",
                  "size of P")  # show elapsed time based on size of P


P1 = [(4, 1), (4, 2), (4, 3), (4, 4),
      (3, 1), (3, 2), (3, 3), (3, 4),
      (2, 1), (2, 2), (2, 3), (2, 4),
              (1, 2)]

P2 = [(4, 1), (4, 2), (4, 3), (4, 4),
      (3, 1), (3, 2)]

P3 = [(4, 1), (4, 2), (4, 3), (4, 4),
      (3, 1), (3, 2), (3, 3), (3, 4),
      (2, 1), (2, 2), (2, 3), (2, 4)]

e = 0.9
c = sqrt(2)/2
ec = e*c
P4 = [(-sqrt(3)/2,-1/2), (sqrt(3)/2,-1/2), (0,1), (ec*(1-sqrt(3))/2, ec*(-1-sqrt(3))/2),
        (ec*(1+sqrt(3))/2, ec*(sqrt(3)-1)/2), (-ec,ec)] + \
            [(-sqrt(39)/8,-5/8), (sqrt(39)/8,-5/8)]

P = [(P1, "P1"), (P2, "P2"), (P3, "P3"), (P4, "P4")]  # TODO add more samples
metrics = [L1(), L2(), Linf()]

measured_times = []
S = []

for p, p_name in P:
    px, py = get_x_y_values(p)
    for metric in metrics:
        s, t = calculate(p, metric)
        sx, sy = get_x_y_values(s)
        show_plot(px, py, sx, sy, metric.name + " on " + p_name)  # show all points and selected ones on plot
        measured_times.append(t*1000)  # time in ms
        S.append(s)

show_measured_time_by_P_size()
