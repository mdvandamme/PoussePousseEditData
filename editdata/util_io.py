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

#import os


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


def suppLignePoint(urlfic):
    
    txtEntete = ''
    with open(urlfic, 'r') as file:
        for line in file:
            txtEntete = line
            break
        file.close()
            
    # On vide le fichier
    with open(urlfic, "w") as file:
        file.write(txtEntete)
        file.close()



def addLigne(urlfic, x, y):
    with open(urlfic, 'a') as file:
        file.write(str(x) + ',' + str(y) + '\n')
        file.close()


def createSettingsFile(uriSettings):
    # on cree le fichier
    f = open(uriSettings, "a")
    f.close()


def getUrlSettings(uriSettings, cle):
    urlARetourner = ''
    with open(uriSettings, "r") as f:
        for line in f:
            if line.strip().rstrip('\n').startswith(cle):
                infos = line.strip().rstrip('\n').split("=")
                urlARetourner = infos[1]
        f.close()
    return urlARetourner


def addUrlSettings(uriSettings, cle, newUrl):

    # On recupere les url du fichier        
    uriGrille = getUrlSettings(uriSettings, 'grille')
    uriPtASaisir = getUrlSettings(uriSettings, 'ptASaisir')
        
    # On ecrase par le nouveau chemin   
    if cle == 'grille':
        uriGrille = newUrl
    if cle == 'ptASaisir':
        uriPtASaisir = newUrl
        
    # On ecrase le fichier avec les URL
    with open(uriSettings, "w") as f:
        if uriGrille != '':
            f.write('grille=' + uriGrille + '\n') # os.linesep
        if uriPtASaisir != '':
            f.write('ptASaisir=' + uriPtASaisir)
        # On ferme le fichier
        f.close()

        