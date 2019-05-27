# -*- coding: utf-8 -*-
"""

"""

def right(a,b,c):
	return ((a == c) or (b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]) < 0)


def convexHull(T):
    
	X = [p[0] for p in T]
	H = [X.index(min(X))]

	while((len(H) < 3) or (H[-1] != H[0])):
		H.append(0)
		for i in range(len(T)):
			if not (right(T[H[-2]], T[H[-1]], T[i])):
				H[-1] = i
    
	return (H)


#xmin = 651041.254154
#ymin = 6859441.59625
#r = 250

#T = [[3,2],[1,3],[4,1],[6,1],[3,1],[2,2],[2,1],[1,5],[2,3],[1,4],[4,2],[3,4],[5,1],[2,5]]
T = [[1,3],[4,1],[6,4],[5,5],[2,2],[2,1]]
#TReel = []
#for (i,j) in T:
#    x = xmin + i * r
#    y = ymin + j * r
#    TReel.append([x,y])
    
# print (TReel)
#H = convexHull(TReel)
H = convexHull(T)
print (H)