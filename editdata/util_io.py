# -*- coding: utf-8 -*-
"""
/***************************************************************************
 
 Functions to manage files
                              -------------------
        begin                : 2019-05-17
        git sha              : $Format:%H$
        author               : M.-D. Van Damme
 ***************************************************************************/


"""


def suppLigne(urlfic, indice):
    """
        Indice de l'élément à supprimer dans le tableau
    """    
    lignesAGarder = []
    with open(urlfic, 'r') as file:
        cpt = 0
        for line in file:
            # si l'indice ne correspond pas à celui que l'on doit supprimer
            if cpt == 0:
                lignesAGarder.append(line)
            elif cpt != (indice + 1):
                lignesAGarder.append(line)
            cpt = cpt + 1
        file.close()
            
    # On ecrase le fichier avec les nouvelles lignes
    with open(urlfic, "w+") as file:
        for line in lignesAGarder:
            file.write(line)
        file.close()
            

def addLigne(urlfic, x, y):
    with open(urlfic, 'a') as file:
        file.write(str(x) + ',' + str(y) + '\n')
        file.close()