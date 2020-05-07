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
        for i, metric in enumerate(metrics):
            tt = tts[i]
            line, = plt.plot(nrange, tt)
            line.set_label(metric.metric)
            if minmax:
                linemax, = plt.plot(nrange, ttmaxs[i], alpha=0.2)
                linemin, = plt.plot(nrange, ttmins[i], alpha=0.2)
                linemax.set_label(f"{metric.metric} max")
                linemin.set_label(f"{metric.metric} min")
        if len(metrics) == 1:
            plt.title(f"Time complexity for 3-Dispersion Problem using {metrics[0].metric} metric.")
            if minmax:
                plt.legend(loc="upper left")
        else:
            plt.legend(loc="upper left")
            plt.title("Time complexity for Max-Min 3-Dispersion Problem.")
        plt.ylabel("time [ms]")
        plt.xlabel("number of input points")
        plt.show()