# -*- coding: utf-8 -*-
"""

"""

class Grille:
    
    def __init__(self, nx, ny, xmin, ymin, rx, ry):
        self.nx = nx
        self.ny = ny
        self.xmin = xmin
        self.ymin = ymin
        self.rx = rx
        self.ry = ry


    def getIJ(self, x, y):
        """
        retourne (i,j) pour le centroid (x,y)
        """
        (it,jt) = (0,0)
        
        for i in range(self.nx):
            for j in range(self.ny):
                
                # cellule en cours
                xmin_cell = self.xmin + i * self.rx
                ymin_cell = self.ymin + j * self.ry
                
                if x >= xmin_cell and x < (xmin_cell + self.rx):
                    if y >= ymin_cell and y < (ymin_cell + self.ry):
                        it = i
                        jt = j
        
        return (it,jt)


    def getId(self, i, j):
        """
            Pour une cellule donnee, on retourne son identifiant
        """
        
        id = (self.ny - j - 1) * self.nx + i
        return id