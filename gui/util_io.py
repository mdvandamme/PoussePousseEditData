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

import os
import time


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


def createFicControle(uriSL):
    
    head, tail = os.path.split(uriSL)
    tps = time.strftime("%Y%m%d_%H%M%S")
    chemin = head + '\\ctrl_' + tps + '.dat'
    f = open(chemin, "w+")
    f.write('x,y' + '\n')
    f.close()
    
    return chemin


#
# indic: (N,Nc,nbXA,nbXV,completion,scompletion,missing,error,serror,rmse,srmse,be,sbe,bn,sbn)
#
def createFicValidation(uriSL, indic):
    
    head, tail = os.path.split(uriSL)
    tps = time.strftime("%Y%m%d_%H%M%S")
    chemin = head + '\\qual_' + tps + '.dat'
    f = open(chemin, "w+")
    
    f.write('--------------------------------------------------------------------------\n')
    f.write(' Rapport des erreurs de saisie \n')
    f.write('--------------------------------------------------------------------------\n')
    f.write(' Date: ' + tps + '\n')
    f.write('--------------------------------------------------------------------------\n')
    f.write('Nombre de cellules tirées: ' + str(indic[0]) + " / " + str(indic[1]) + '\n')
    f.write("Taille de l'échantillon d'acquisition: " + str(indic[2]) + '\n')
    f.write("Taille de l'échantillon de contrôle: " + str(indic[3]) + '\n')
    f.write('--------------------------------------------------------------------------\n')
    f.write('Complétion: ' + str(indic[4]) + ' ± ' + str(indic[5]) + ' % \n')
    f.write('Nombre théorique de points manquants: < ' + str(indic[6]) + ' \n')
    f.write('Moyenne des erreurs: ' + str(indic[7]) + ' ± ' + str(indic[8]) + ' m \n')
    f.write('Écart quadratique moyen: ' + str(indic[9]) + ' ± ' + str(indic[10]) + ' m \n')
    f.write('--------------------------------------------------------------------------\n')
    f.write('Biais en X: ' + str(indic[11]) + ' ± ' + str(indic[12]) + ' m \n')
    f.write('Biais en Y: ' + str(indic[13]) + ' ± ' + str(indic[14]) + ' m \n')
    f.write('--------------------------------------------------------------------------\n')
    
    f.close()
    
    return chemin
    

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

        