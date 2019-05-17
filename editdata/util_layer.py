# -*- coding: utf-8 -*-
"""
/***************************************************************************
 
 functions to manage layers
                              -------------------
        begin                : 2019-05-17
        git sha              : $Format:%H$
        author               : M.-D. Van Damme
 ***************************************************************************/
"""

from qgis.core import QgsPoint, QgsGeometry, QgsFeature


def removeFeature(layer, indice):
    """
        Indice de l'élément à supprimer dans le tableau
    """ 
    
    # Compteur des features
    cpt = 0
    
    # On passe en mode edition
    layer.startEditing()
    
    for feature in layer.getFeatures():
        if cpt == indice:
            layer.deleteFeature(feature.id())
        cpt = cpt + 1
        
    # commit to stop editing the layer
    layer.commitChanges()
    
    return layer


def addPointLayer(layer, x, y):
    
    layer.startEditing()
    pr = layer.dataProvider()
        
    geompoint = QgsGeometry.fromPoint(QgsPoint(x,y))
    newFeature = QgsFeature()
    newFeature.setGeometry(geompoint)
    pr.addFeatures([newFeature]) 
                
    layer.commitChanges() 
    
    return layer