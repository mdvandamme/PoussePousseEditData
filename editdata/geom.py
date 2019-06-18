# -*- coding: utf-8 -*-
"""
Intersection de 2 segments.

"""

import sys
import envconvexe as envconv

# 
# Fonction qui retourne vrai si le point q est sur le segment pr
# p, q, r: 3 points alignés
# return boolean
def onSegment(p, q, r):

    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) 
            and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    
    return False


#
# Retourne le type d'orientation de 3 points (p, q, r)
#    - 0 si les 3 points sont alignés
#    - 1 si l'orientation est dans le sens des aiguilles d'une montre
#    - 2 dans le sens contraire    
def orientation(p, q, r):
    
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]); 
    
    if (val == 0):
        # alignés
        return 0
  
    # sinon
    if val > 0:
        return 1
    else:
        return 2


# 
# Retourne vrai si 2 segments s'intersectent, faux sinon.
# Les segments sont: p1q1 et p2q2
#
def doIntersect(p1, q1, p2, q2):

    # 4 orientations 
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
  
    # (p1, q1, p2) et (p1, q1, q2) ont des orientations différentes
    # (p2, q2, p1) et (p2, q2, q1) ont des orientations différentes
    if (o1 != o2 and o3 != o4):
        return True 
  
    # cas particuliers
    # p1, q1 et p2 sont alignes et p2 sur le segment p1q1 
    if (o1 == 0 and onSegment(p1, p2, q1)):
        return True
  
    # p1, q1 et q2 sont alignes et q2 sur le segment p1q1 
    if (o2 == 0 and onSegment(p1, q2, q1)):
        return True
  
    # p2, q2 et p1 sont alignes et p1 sur le segment p2q2 
    if (o3 == 0 and onSegment(p2, p1, q2)):
        return True
  
    # p2, q2 et q1 sont alignes et q1 sur le segment p2q2 
    if (o4 == 0 and onSegment(p2, q1, q2)):
        return True
  
    # Sinon 
    return False 


#
# Retourne vrai si le point p se trouve à l'intérieur du polygon
#
# polygon: tableau des coordonnées des sommets
# n : nombre de sommets du polygone
# Point p à tester
def isInside(polygon, n, p):
    
    # Au moins 3 sommets dans le polygone
    if n < 3:
        return False
  
    # Creation d'un point pour faire un segment horizontal infini en partant de p
    extreme = [sys.maxsize, p[1]]
  
    # On compte le nombre d'intersection du segment infini avec le polygone
    count = 0
    i = 0
    while True:
        # print (i)
        next = (i+1)%n
  
        # print (str(polygon[i]) + "#" + str(polygon[next]) + "#" + str(p))
    
        # Verifie si le segment infini interecte 
        # le segment du polygone de sommet polygon[i] et polygon[next]
        if doIntersect(polygon[i], polygon[next], p, extreme): 
            # Si le point p est aligne avec le segment i-next
            # alors il faut vérifier s'il est dans le segment => vrai
            # faux sinon
            if orientation(polygon[i], p, polygon[next]) == 0:
                return onSegment(polygon[i], p, polygon[next])
  
            count = count + 1
            

        i = next
        
        if i == 0:
            break
    
    # print ('nb = ' + str(count))
    
    # Retourne vrai si le nombre est impair, faux sinon
    return count%2 == 1


def column(matrix, i):
    return [row[i] for row in matrix]


def aire_polygone(X, Y):

    aire = 0

    X.append(X[0])
    Y.append(Y[0])
        
    n = len(X)
    
    for i in range(0, n-1):
        aire += X[i]*Y[i+1]-X[i+1]*Y[i]
        
    aire *= 0.5
    aire = abs(aire)

    return aire



def aire_env_convexe(T):
    
    H = envconv.envconvexe(T)

    X = column(H,0)
    Y = column(H,1)

    a = aire_polygone(X, Y)

    return a

