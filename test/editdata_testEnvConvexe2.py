# -*- coding: utf-8 -*-
"""

"""


def test():		
	
	xmin = 100
	ymin = 200
	r = 2
	nx = 40
	ny = 30
	npts = 3
	N = 599

	xmax = xmin+r*nx
	ymax = ymin+r*ny

	for ix in range(nx):
		for iy in range(ny):
			xc = getCellVerticesX(xmin, r, ix)
			yc = getCellVerticesY(ymin, r, iy)
			plt.plot(xc, yc, linewidth=0.5, color='k')
				
		
		
	T = list()
	for i in range(npts):
		x = random.random()*(xmax-xmin)+xmin
		y = random.random()*(ymax-ymin)+ymin
		T.append([x,y])
		
	X = column(T,0)
	Y = column(T,1)	
	plt.plot(X,Y,'ro',markersize=3)	
		
	I = sampleInConvexHull(xmin, ymin, nx, ny, r, N, T)	
	
	# Pour echantillonner sens prendre en compte l'enveloppe convexe
	# I = sampleInConvexHull(xmin, ymin, nx, ny, r, N, [[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin]])

	for i in range(len(I)):
		xc = getCellVerticesX(xmin, r, I[i][0])
		yc = getCellVerticesY(ymin, r, I[i][1])
		plt.fill(xc, yc, color='k')


	plt.show()
	
#test()