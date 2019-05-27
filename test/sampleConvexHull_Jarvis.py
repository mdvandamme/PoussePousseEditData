# -*- coding: utf-8 -*-
"""

"""
import math
import sys


# ----------------------------------------
# Fonction de calcul de l azimut (en degré)
# Entrees : coordonnees de P1 et P2
# Sortie : azimut (en degré) de P1 vers P2
# ---------------------------------------
def azimut(x1,y1,x2,y2):

    dx = x2-x1
    dy = y2-y1    
    
    if (dx == 0) & (dy == 0):
        print("Erreur : les points p1 et p2 doivent être distincts")
        return 0
    
    if x1 != x2:
        azimut = 2*math.atan(dx/(math.sqrt(dx*dx+dy*dy)+dy)) * 180 / math.pi
    else:
        azimut = 0
    
    if azimut < 0:
        azimut += 360
    
    return azimut

# -----------------------------------------------------------
# Calcul de l enveloppe convexe 
#
# -----------------------------------------------------------
def convexeJarvis(X, Y, N, xmax):
    
    min_x = xmax
    index = -1

    for i in range(0, N):
        if X[i] <= min_x:
            min_x = X[i]
            index = i
    
    min_y = sys.float_info.max
    for i in range(0, N):
        if X[i] == min_x:
            if Y[i] < min_y:
                min_y = Y[i]
                index = i
    
    enveloppe = list()
    enveloppe.append(index)

    angle_courant = 0
    
    # Boucle infine
    while 1 == 1:
        
        # Remise à zéro des paramètres
        angle_min = 360
        pt_suivant = -1
    
        # On parcourt tous les points pour initialiser angle_min et pt_suivant
        for i in range(0,N):
    
            # Si le point est déjà dans l'enveloppe
            if i in enveloppe:
                continue
        
            # Calcul de l'azimut au candidat suivant
            angle = azimut(X[index], Y[index], X[i], Y[i])
            #print angle
            
            # Si l'angle est inférieur à l'angle min précédent
            # i.e. au fur et à mesure des itérations, les angles doivent s'agrandir
            if angle < angle_courant:
                continue
        
            # Si l'angle est plus petit que le meilleur candidat actuel
            if angle <= angle_min:
                angle_min = angle
                pt_suivant = i
    
        # Meilleur candidat
        index = pt_suivant
        
        # Condition d'arrêt
        angle_initial = azimut(X[index], Y[index], X[enveloppe[0]], Y[enveloppe[0]])
        if (angle_min >= angle_initial and len(enveloppe) > 1):
            enveloppe.append(enveloppe[0])
            break    
        
        # Ajout du point à l'enveloppe
        angle_courant = angle_min
        enveloppe.append(pt_suivant)
        
    env = list()
    # print "taille de l'env = ", len(enveloppe)
    for i in range(0, len(enveloppe)):
        env.append(X[enveloppe[i]])
        env.append(Y[enveloppe[i]])
    
    
    indices = []
    Ne = len(env)
    for e in range(0, int(Ne/2)):
        x = env[0::2][e]
        y = env[1::2][e]
        for i in range(len(X)):
            if X[i] == x and Y[i] == y:
                indices.append(i)
    
    return indices