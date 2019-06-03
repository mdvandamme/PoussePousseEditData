import random
import matplotlib.pyplot as plt
import math
import sys


def column(matrix, i):
    return [row[i] for row in matrix]
	


def right(a,b,c):
	return ((a == c) or (b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]) <= 0)
            
    
def convexHull(T):
    
	X = [p[0] for p in T]
	H = [X.index(min(X))]

	while((len(H) < 3) or (H[-1] != H[0])):
		H.append(0)
		for i in range(len(T)):
			if not (right(T[H[-2]], T[H[-1]], T[i])):
				H[-1] = i
    
	return (H)


# ----------------------------------------
# Fonction de calcul de l azimut (en degre)
# Entrees : coordonnees de P1 et P2
# Sortie : azimut (en degre) de P1 vers P2
# ---------------------------------------
def azimut(x1,y1,x2,y2):

    dx = x2-x1
    dy = y2-y1    
    
    if (dx == 0) & (dy == 0):
        print("Erreur : les points p1 et p2 doivent etre distincts")
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
def convexeJarvis(T):
    
    # print (T)
    X = []
    Y = []
    xmax = - sys.float_info.max
    for t in T:
        x = t[0]
        X.append(x)
        Y.append(t[1])
        if x > xmax:
            xmax = x
    N = len(X)
    
    # ------------------------------
    
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
        
        # Remise a zero des parametres
        angle_min = 360
        pt_suivant = -1
    
        # On parcourt tous les points pour initialiser angle_min et pt_suivant
        for i in range(0,N):
    
            # Si le point est deja dans l'enveloppe
            if i in enveloppe:
                continue
        
            # Calcul de l'azimut au candidat suivant
            angle = azimut(X[index], Y[index], X[i], Y[i])
            #print angle
            
            # Si l'angle est inferieur a l'angle min precedent
            # i.e. au fur et a mesure des iterations, les angles doivent s'agrandir
            if angle < angle_courant:
                continue
        
            # Si l'angle est plus petit que le meilleur candidat actuel
            if angle <= angle_min:
                angle_min = angle
                pt_suivant = i
    
        # Meilleur candidat
        index = pt_suivant
        
        # Condition d'arret
        angle_initial = azimut(X[index], Y[index], X[enveloppe[0]], Y[enveloppe[0]])
        if (angle_min >= angle_initial and len(enveloppe) > 1):
            enveloppe.append(enveloppe[0])
            break    
        
        # Ajout du point a l'enveloppe
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
    
    # print (indices)
    return indices


	
def getCellVerticesX(xmin, r, ix):
	return [xmin + r*ix, xmin + r*(ix+1), xmin + r*(ix+1), xmin + r*ix, xmin + r*ix]
	
def getCellVerticesY(ymin, r, iy):
	return [ymin+r*iy, ymin+r*iy, ymin+r*(iy+1), ymin+r*(iy+1), ymin+r*iy]
	
# ----------------------------------------
# Fonction booleenne d'inclusion
# Entrees : polygone et coordonnees x, y
# Sortie : true s'il y a inclusion
# ----------------------------------------
def inclusion(polygone, x, y):
    
    # Coordonnees max
    cmax = max(polygone)
    
    # Creation d'un segment
    segment = list()
    
    segment.append(x)
    segment.append(y)
    segment.append(2*cmax)
    segment.append(2*cmax)
    
    # Calcul du nombre d'intersections
    n = 0
    
    for i in range(0, int(len(polygone)/2-1)):
        
        edge = list()
        edge.append(polygone[2*i])
        edge.append(polygone[2*i+1])
        edge.append(polygone[2*i+2])
        edge.append(polygone[2*i+3])
        
        if intersects(segment, edge):
            n += 1
        
    edge = list()
    edge.append(polygone[0])
    edge.append(polygone[1])
    edge.append(polygone[len(polygone)-2])
    edge.append(polygone[len(polygone)-1])
    
    if intersects(segment, edge):
            n += 1
            
    if n % 2 == 0:
        return False
    
    else:
        return True
# ----------------------------------------
# Fonction equation cartesienne
# Entree : segment
# Sortie : liste de parametres (a,b,c)
# ----------------------------------------
def cartesienne(segment):
    
    parametres = list();
    
    x1 = segment[0]
    y1 = segment[1]
    x2 = segment[2]
    y2 = segment[3]
    
    u1 = x2-x1
    u2 = y2-y1
    
    b = -u1
    a = u2
    
    c = -(a*x1+b*y1)
    
    parametres.append(a)
    parametres.append(b)
    parametres.append(c)
    
    return parametres


# ----------------------------------------
# Fonction de test d'equation de droite
# Entrees : paramatres et coords (x,y)
# Sortie : en particulier 0 si le point 
# appartient a la droite
# ----------------------------------------
def eval(param, x, y):
    
    a = param[0]
    b = param[1]
    c = param[2]
    
    return a*x+b*y+c

# ----------------------------------------
# Fonction booleenne d'intersection
# Entrees : segment1 et segment2
# Sortie : true s'il y a intersection
# ----------------------------------------
def intersects(segment1, segment2):
    
    param_1 = cartesienne(segment1)
    param_2 = cartesienne(segment2)

    x11 = segment1[0]
    y11 = segment1[1]
    x12 = segment1[2]
    y12 = segment1[3]
    
    x21 = segment2[0]
    y21 = segment2[1]
    x22 = segment2[2]
    y22 = segment2[3]
    
    
    val11 = eval(param_1,x21,y21)
    val12 = eval(param_1,x22,y22)
    
    val21 = eval(param_2,x11,y11)
    val22 = eval(param_2,x12,y12)
    
    val1 = val11*val12
    val2 = val21*val22
    
    return (val1 <= 0) & (val2 <= 0)
    

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
    H = convexHull(T)
    # H = convexeJarvis(T)

    X = column(T,0)
    Y = column(T,1)

    XC = [X[i] for i in H]
    YC = [Y[i] for i in H]

    a = aire_polygone(XC, YC)

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

    
    plt.axis([xmin,xmin+nx*r,ymin,ymin+ny*r])

    H = convexHull(T)
    #H = convexeJarvis(T)

    # n = len(T)
    X = column(T,0)
    Y = column(T,1)
	
    if (N > 0.5 * nx * ny):
        print("Erreur : N est superieur a 50% du nombre de cellules")
        return 1
	
    XC = [X[i] for i in H]
    YC = [Y[i] for i in H]
	
    hull = [val for pair in zip(XC, YC) for val in pair]

    cpt = 0
    I = list()
    while(len(I) < N):
        cpt = cpt + 1
        if cpt > 5:
            break
        while(len(I) < 1.5*N):
	
            ix = random.sample(range(nx), 1)[0]
            iy = random.sample(range(ny), 1)[0]
            xc = getCellVerticesX(xmin, r, ix)
            yc = getCellVerticesY(ymin, r, iy)
		
            for i in range(4):
                if inclusion(hull, xc[i], yc[i]):
                    I.append((ix,iy))
                    break
			
        I = list(dict.fromkeys(I))
		
    if (len(I) > N):
        I = [I[i] for i in range(N)]

	
    return I
		
		
		
