# Quick Median (linear time median)

import random

def quickselect(xs, k):
    if len(xs) == 1:
        # Median of list with 1 element
        assert k == 0
        return xs[0]
    
    pivot = random.choice(xs)

    left = []
    right = []
    pivots = []
    for x in xs:
        if x < pivot:
            left.append(x)
        elif x == pivot:
            pivots.append(x)
        else:
            right.append(x)
    
    if k < len(left):
        # Median is in left
        return quickselect(left, k)
    elif k < len(left) + len(pivots):
        # Pivot is the median
        return pivots[0]
    else:
        # Median is in right
        return quickselect(right, k - len(left) - len(pivots))

def quickmedian(xs):
    if len(xs) % 2 == 0:
        return 0.5 * (quickselect(xs, len(xs) // 2) + quickselect(xs, len(xs) // 2 - 1))
    else:
        return quickselect(xs, len(xs) // 2)