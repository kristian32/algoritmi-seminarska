# main datoteka za Max-Min 3-disperzijski problem

import sys
from time import time
# from getopt import getopt
import getopt
import matplotlib.pyplot as plt
from L_1 import L1
from L_2 import L2
from L_inf import Linf

class fileFunctions:

    @staticmethod
    def readFile(f):
        '''Sprejme datoteko f in iz nje prebere vrednosti ter ustvari seznam tock.'''
        n = int(f.readline())
        P = [None] * n
        for i in range(n):
            P[i] = tuple(map(int, f.readline().split(" ")))
        return P

    @staticmethod
    def writeFile(f, S):
        '''Sprejme datoteko f in seznam tock S in ga izpise v f.'''
        for s in S:
            f.write(" ".join(map(str, s)))
            f.write("\n")
    
    @staticmethod
    def showPlot(P, Ss, titles, xlabel="", ylabel=""):
        '''Sprejme mnozico tock, seznam mnozic resitev in seznam naslovo.
        Narise graf graf za vsako mnozico resitev.'''
        points_x = [p[0] for p in P]
        points_y = [p[1] for p in P]
        fig = plt.figure()
        pos = ((len(Ss) - 1) // 2 + 1) * 100 + (len(Ss) // 2 + 1) * 10 + 1
        for i,S in enumerate(Ss):
            Sx = [s[0] for s in S]
            Sy = [s[1] for s in S]

            ax = fig.add_subplot(pos+i)

            plt.scatter(points_x, points_y, s=1000/len(P), marker='o', color='b')
            plt.scatter(Sx, Sy, s=max(1000/len(P), 10), marker='o', color='r')

            l, r = ax.get_xlim()
            left, right = min(l, -l/5), max(r + 1, 1)
            l, h = ax.get_ylim()
            low, high = min(l, -l/5), max(h + 1, 1)

            plt.arrow(left, 0, right - left, 0, length_includes_head=True, head_width=0.15)
            plt.arrow(0, low, 0, high - low, length_includes_head=True, head_width=0.15)

            plt.xlim(left, right)
            plt.ylim(low, high)

            plt.title(titles[i])
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

        plt.grid()
        plt.show()

def main():
    '''Glede na dane vhodne argumente izracuna resitve v zeljenih metrikah in
    po potrebi prikaze porabljen cas in/ali narise graf(e).'''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:tp", ["metric=", "time", "plot"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    toPlot = False
    toTime = False
    Ls = []
    for o,v in opts:
        if o == "-m":
            print(v)
            if "0" in v:
                Ls.append(Linf())
            if "1" in v:
                Ls.append(L1())
            if "2" in v:
                Ls.append(L2())
        elif o == "-t":
            toTime = True
        else:
            toPlot = True
    if len(Ls) == 0:
        Ls.append(Linf())
    
    if len(args) == 0:
        infile = sys.stdin
        outfile = sys.stdout
    else:
        infile = open(args[0])
        outfile = sys.stdin if len(args) == 1 else open(args[1])
    
    P = fileFunctions.readFile(infile)
    Ss = [None] * len(Ls) # resitve
    for i,L in enumerate(Ls):
        t = time()
        Ss[i] = L.three_dispersion(P)
        t = time() - t
        outfile.write(L.name)
        outfile.write("\n")
        fileFunctions.writeFile(outfile, Ss[i])
        if toTime:
            outfile.write(str(round(t*1000)))
            outfile.write("ms\n")
        outfile.write("\n")
    
    if toPlot:
        fileFunctions.showPlot(P, Ss, [L.name for L in Ls])

if __name__ == "__main__":
    main()