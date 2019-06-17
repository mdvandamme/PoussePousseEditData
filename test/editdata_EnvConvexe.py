# -*- coding: utf-8 -*-
"""

Calcul de l'enveloppe convexe par l'algo d'Andrew (1979)


@author: Marie-Dominique Van Damme

"""
import random
import matplotlib.pyplot as plt

import geom as geom


def getCellVerticesX(xmin, r, ix):
	return [xmin+r*ix, xmin+r*(ix+1), xmin+r*(ix+1), xmin+r*ix, xmin+r*ix]
	
def getCellVerticesY(ymin, r, iy):
	return [ymin+r*iy, ymin+r*iy, ymin+r*(iy+1), ymin+r*(iy+1), ymin+r*iy]

def column(matrix, i):
    return [row[i] for row in matrix]

   
# 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
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

    # Build lower hull 
    lower = []
    for p in T:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(T):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]



# ===========================================================================================
#T = [[3,2],[1,3],[4,1],[6,1],[3,1],[2,2],[2,1],[1,5],[2,3],[1,4],[4,2],[3,4],[5,1],[2,5]]


xmin = 651041.254154
ymin = 6859441.59625
nx = 7
ny = 7
r = 250

for ix in range(nx):
    for iy in range(ny):
        xc = getCellVerticesX(xmin, r, ix)
        yc = getCellVerticesY(ymin, r, iy)
        plt.plot(xc, yc, linewidth=0.5, color='k')
    
T = list()
urlALire = 'D:\\DATA\\PoussePousse\\feu\\Points.csv'
with open(urlALire, "r") as f:
    for line in f:
        x = line.split(',')[0]
        y = line.split(',')[1]
        if x != 'x':
            T.append([float(x),float(y)])


X = column(T,0)
Y = column(T,1)	            


H = envconvexe(T)
# on ajoute le premier point
H.append(T[0])

XC = column(H,0) #[X[i] for i in H]
YC = column(H,1) #[Y[i] for i in H]
plt.plot(XC,YC, color='#FFDD44', linewidth=3)	

#plt.xlim([0,7])
#plt.ylim([0,7])

plt.xlim([xmin, xmin + r * nx])
plt.ylim([ymin, ymin + r * ny])


# Les points
plt.plot(X,Y,'ro',markersize=3)


# Tableau des cellules de l'env convexe
CELL = []

t = r / 10
for ix in range(nx):
    for iy in range(ny):
        
        A = [xmin + r * ix, ymin + r * (iy + 1)]
        B = [xmin + r * (ix + 1), ymin + r * (iy + 1)]
        C = [xmin + r * (ix + 1), ymin + r * iy]
        D = [xmin + r * ix, ymin + r * iy]
        
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
        

print ('nb=' + str(len(CELL)))
#for p in CELL:
#    print (p)
           
# Tirage au sort
N = 10
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

print (I)

# plt.gca().add_patch(plt.Circle((xmin + 2*r, ymin + 2*r), 200, color='r'))

for i in I:
    x1 = xmin + i[0] * r
    x2 = xmin + (i[0] + 1) * r
    y1 = ymin + i[1] * r
    plt.gca().add_patch(
        plt.Rectangle((x1, y1), r, r, fill=True, edgecolor='aqua', linewidth=3)
    )


plt.show()