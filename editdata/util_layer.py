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
from qgis.core import QgsVectorLayer, QgsMapLayer, QgsMapLayerRegistry
from qgis.core import QgsFillSymbolV2, QgsSingleSymbolRendererV2, QgsMarkerSymbolV2

from PyQt4.QtGui import QColor

def getLayer(nom):
    
    # Layer a retourner
    layerATrouver = None
    
    layers = QgsMapLayerRegistry.instance().mapLayers().values()
    for layer in layers:
        if layer.type() == QgsMapLayer.VectorLayer:
            if (layer.name() == nom):
                layerATrouver = layer
    
    return layerATrouver 
                

def removeAllFeature(layer):
    layer.startEditing()
    for feature in layer.getFeatures():
        layer.deleteFeature(feature.id())
    layer.commitChanges()
    return layer

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


def createLayerGrille(uriGrille):
    layerGrille = QgsVectorLayer(uriGrille, "Grille", "ogr")
    QgsMapLayerRegistry.instance().addMapLayer(layerGrille)
    
    # Style 
    props = {'color': '241,241,241,0', 'size':'1', 'color_border' : '255,0,0'}
    s = QgsFillSymbolV2.createSimple(props)
    layerGrille.setRendererV2(QgsSingleSymbolRendererV2(s))
    
    return layerGrille


def createLayerPoint(proj):
    
    layerStopLine = QgsVectorLayer ("Point?crs=" + proj, "PointsASaisir", "memory")
            
    # Style
    # Symbologie des stations
    symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,127,0'})
    symbolPoint.setColor(QColor.fromRgb(216,7,96))  #F 216,7,96
    symbolPoint.setSize(2)
    layerStopLine.rendererV2().setSymbol(symbolPoint)
    
    return layerStopLine


def zoomFeature(iface, layer, currId):
    # On parcours les index jusqu'à celui qu'on a 
    for feature in layer.getFeatures():
        id = feature.attributes()[0]
        if str(id) == currId:
            # zoom sur la couche
            layer.selectByIds([id])
            iface.mapCanvas().zoomToSelected(layer)
            iface.mapCanvas().refresh();
            layer.selectByIds([]);


