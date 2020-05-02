import time
from L_1 import L1
from L_2 import L2

def measure_time(P, metric):
    start = time.time()
    print(metric.name())
    print("Given set of ", len(P), " points")

    S = metric.three_dispersion(P)
    print("The optimal result is: ", S)

    end = time.time()
    print("Time elapsed: ", end - start, "\n")


P1 = {(4, 1), (4, 2), (4, 3), (4, 4),
      (3, 1), (3, 2), (3, 3), (3, 4),
      (2, 1), (2, 2), (2, 3), (2, 4),
              (1, 2)}

P2 = {(4, 1), (4, 2), (4, 3), (4, 4),
      (3, 1), (3, 2)}

P3 = {(4, 1), (4, 2), (4, 3), (4, 4),
      (3, 1), (3, 2), (3, 3), (3, 4),
      (2, 1), (2, 2), (2, 3), (2, 4)}

measure_time(P1, L1())
# measure_time(P2, L1())
# measure_time(P3, L1())