# Quick Median (linear time median)

import random

def quickselect(xs, k, key=lambda x: x):
    if len(xs) == 1:
        # Median of list with 1 element
        assert k == 0
        return xs[0]
    
    pivot = random.choice(xs)
    pivot_key = key(pivot)

    left = []
    right = []
    pivots = []
    for x in xs:
        x_key = key(x)
        if x_key < pivot_key:
            left.append(x)
        elif x_key == pivot_key:
            pivots.append(x)
        else:
            right.append(x)
    
    if k < len(left):
        # Median is in left
        return quickselect(left, k, key)
    elif k < len(left) + len(pivots):
        # Pivot is the median
        return pivots[0]
    else:
        # Median is in right
        return quickselect(right, k - len(left) - len(pivots), key)

def quickmedian(xs, key=lambda x: x):
    '''Vrnemo mediano, ce je xs lihe dolzine. Ce je sode dolzine, vrnemo desno
    tocko izmed srednjih dveh.'''
    return quickselect(xs, len(xs) // 2, key)