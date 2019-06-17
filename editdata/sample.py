# -*- coding: utf-8 -*-

import random

import envconvexe as envconv
import geom as geom


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

# ---------------------------------------------------
# Fonction d'echantillonnage d'indices de cellules 
# dans l'enveloppe convexe d'un semis de points
# Entrees : 
#      - xmin, ymin : coordonnees min de la grille
#      - nx, ny : nombres de cellules en x et y
#      - r : taille des cellules
#      - N : nombre de cellules a echantillonner
#      - T : tableau (a 2 colonnes) du semis
# Sortie : liste d'indices de cellules selectionnees
# ---------------------------------------------------
def sampleInConvexHull(xmin, ymin, nx, ny, r, N, T):

    if (N > 0.5 * nx * ny):
        print("Erreur : N est superieur a 50% du nombre de cellules")
        return 1
    
    
    H = envconv.envconvexe(T)
    
    # Tableau des cellules de l'env convexe
    CELL = []
    
    t = r / 10
    for ix in range(nx):
        for iy in range(ny):
            
            # A-B
            for p in range(11):
                xp = xmin + r * ix + p * t
                yp = ymin + r * (iy + 1)
                if geom.isInside(H, len(H), [xp, yp]):
                    if [ix,iy] not in CELL:
                        CELL.append([ix,iy])
            # B-C
            for p in range(11):
                xp = xmin + r * (ix + 1)
                yp = ymin + r * iy + p * t
                if geom.isInside(H, len(H), [xp, yp]):
                    if [ix,iy] not in CELL:
                        CELL.append([ix,iy])
            
            # C-D
            for p in range(11):
                xp = xmin + r * ix + p * t
                yp = ymin + r * iy
                if geom.isInside(H, len(H), [xp, yp]):
                    if [ix,iy] not in CELL:
                        CELL.append([ix,iy])
                        
            # D-A
            for p in range(11):
                xp = xmin + r * ix
                yp = ymin + r * iy + p * t
                if geom.isInside(H, len(H), [xp, yp]):
                    if [ix,iy] not in CELL:
                        CELL.append([ix,iy])

    cpt = 0
    I = list()
    while (len(I) < N):
            
        cpt = cpt + 1
        if cpt > 5:
            break
            
        while (len(I) < 1.5*N):
            i = random.sample(range(len(CELL)), 1)[0]
            # if CELL[i] not in CELL:
            I.append(CELL[i])
        
        # On supprime les doublons
        J = []
        for c in range(len(I)):
            if len(J) == 0 or I[c] not in J:
                J.append(I[c])
        I = J
    
        
    if (len(I) > N):
        I = [I[i] for i in range(N)]

    
    return I
		
		
		
