# Draw graphs for random input

import random
import time
import matplotlib.pyplot as plt

class Graphs:
    def __init__(self):
        self.name = 'Graphs'
    
    @staticmethod
    def createTimeGraphs(metrics, nrange, plt, rep=1, M=1000, minmax=False):
        if type(metrics) is not list:
            metrics = [metrics]
        tts = [[None]*len(nrange) for _ in range(len(metrics))] # Total times
        ttmaxs = [[None]*len(nrange) for _ in range(len(metrics))]
        ttmins = [[None]*len(nrange) for _ in range(len(metrics))]
        for i, n in enumerate(nrange):
            print(n)
            times = [0] * len(metrics)
            tmaxs = [0] * len(metrics)
            tmins = [float("inf")] * len(metrics)
            for j in range(rep):
                P = [(random.randrange(M), random.randrange(M)) for _ in range(n)]
                for j, metric in enumerate(metrics):
                    t0 = time.time()
                    metric.three_dispersion(P)
                    t = time.time()-t0
                    times[j] += t
                    if t > tmaxs[j]:
                        tmaxs[j] = t
                    if t < tmins[j]:
                        tmins[j] = t
            for j, t in enumerate(times):
                tts[j][i] = round(t * 1000 / rep)
                ttmaxs[j][i] = round(tmaxs[j] * 1000)
                ttmins[j][i] = round(tmins[j] * 1000)
        # colors = ["b", "r", "g"]
        for i, metric in enumerate(metrics):
            tt = tts[i]
            line, = plt.plot(nrange, tt)
            line.set_label(metric.metric)
            if minmax:
                linemax, = plt.plot(nrange, ttmaxs[i], alpha=0.2, color="r")
                linemin, = plt.plot(nrange, ttmins[i], alpha=0.2, color="g")
        if minmax:
            linemax.set_label("max")
            linemin.set_label("min")
        if len(metrics) == 1:
            plt.title(f"Časovna zahtevnost za 3-disperzijski problem z {metrics[0].metric} metriko.")
            if minmax:
                plt.legend(loc="upper left")
        else:
            plt.legend(loc="upper left")
            plt.title("Časovna zahtevnost za Max-Min 3-disperzijski problem.")
        plt.ylabel("čas [ms]")
        plt.xlabel("število vhodnih točk")
        plt.show()