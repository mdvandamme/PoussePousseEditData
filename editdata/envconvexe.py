# -*- coding: utf-8 -*-
"""
Calcul de l'enveloppe convexe.


"""

#
# Fonction retourne :
#   - une valeur positive si OAB est orienté dans le sens des aiguilles d'une montre
#   - une valeur négative si OAB est orienté dans le sens contraire
#   - 0 si les points sont alignés
#
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


#
# Calcul de l'enveloppe.
#    
def envconvexe(T):
    
    E = []

    # 1. On trie les points suivant leur x, puis leur y
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
