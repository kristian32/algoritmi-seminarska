# Draw graphs for random input

import random
import time
import matplotlib.pyplot as plt

class Graphs:
    def __init__(self):
        self.name = 'Graphs'
    
    @staticmethod
    def createTimeGraphs(metrics, nrange, plt, rep=1, M=1000):
        if type(metrics) is not list:
            metrics = [metrics]
        tts = [[None]*len(nrange) for _ in range(len(metrics))] # Total times
        for i, n in enumerate(nrange):
            print(n)
            times = [0] * len(metrics)
            for j in range(rep):
                P = [(random.randrange(M), random.randrange(M)) for _ in range(n)]
                for j, metric in enumerate(metrics):
                    t = time.time()
                    metric.three_dispersion(P)
                    times[j] += time.time()-t
            for j, t in enumerate(times):
                tts[j][i] = round(t * 1000 / rep)
        for i, metric in enumerate(metrics):
            tt = tts[i]
            line, = plt.plot(nrange, tt)
            line.set_label(metric.metric)
        if len(metrics) == 1:
            plt.title(f"Time complexity for 3-Dispersion Problem using {metrics[0].metric} metric.")
        else:
            plt.legend(loc="upper left")
            plt.title("Time complexity for Max-Min 3-Dispersion Problem.")
        plt.ylabel("time [ms]")
        plt.xlabel("number of input points")
        plt.show()