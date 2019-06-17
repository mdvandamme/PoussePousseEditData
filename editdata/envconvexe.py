# -*- coding: utf-8 -*-
"""
Calcul de l'enveloppe convexe.


"""


# Returns a positive value, if OAB makes a counter-clockwise turn,
# negative for clockwise turn, and zero if the points are collinear.
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def envconvexe(T):
    
    E = []

    # 1. Sort points by x coordinate, then by y coordinate
    T.sort(key=lambda x: (x[0],x[1]))

    if len(T) <= 1:
        return E

    # Construction de l'env dessous
    lower = []
    for p in T:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Construction de l'env dessus
    upper = []
    for p in reversed(T):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # On concatene.
    E = lower[:-1] + upper[:-1]
    
    # On ajoute le premier point pour boucler
    E.append(E[0])
    
    return E