# -*- coding: utf-8 -*-
"""

"""

from sampleConvexHull_Jarvis import convexe

T = [[1,3],[4,1],[6,4],[5,5],[2,2],[2,1]]

X = [1,4,6,5,2,2]
Y = [3,1,4,5,2,1]
N = 6
ptmax = 6

env = convexe(X, Y, N, ptmax)
print (env)

#indices = []
#Ne = len(env)
#for e in range(0, int(Ne/2)):
#    x = env[0::2][e]
#    y = env[1::2][e]
#    for i in range(len(X)):
#        if x == X[i] and y == Y[i]:
#            indices.append(i)
#print (indices)