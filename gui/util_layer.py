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
from qgis.core import QgsField
from PyQt4.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsMapLayer, QgsMapLayerRegistry, QgsVectorDataProvider
from qgis.core import QgsFillSymbolV2, QgsSingleSymbolRendererV2, QgsMarkerSymbolV2
from qgis.core import QgsSymbolV2, QgsRuleBasedRendererV2

from PyQt4.QtGui import QColor


CONST_ATTRIBUT_ID = "ppid"
CONST_NOM_LAYER_GRILLE = "Grille"
CONST_NOM_LAYER_PT_SAISIR = "PointsASaisir"
CONST_NOM_LAYER_PT_CONTROLE = "PointsAControler"


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
    if layer != None:
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
    
    layerGrille = QgsVectorLayer(uriGrille, CONST_NOM_LAYER_GRILLE, "ogr")
    
    fieldIndex = getFieldIndex(layerGrille)
    if fieldIndex < 0:
        caps = layerGrille.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.AddAttributes:
            layerGrille.dataProvider().addAttributes([QgsField(CONST_ATTRIBUT_ID, QVariant.Int)])
        layerGrille.updateFields()
    
    # Style 
    props = {'color': '241,241,241,0', 'size':'1', 'color_border' : '255,0,0'}
    s = QgsFillSymbolV2.createSimple(props)
    layerGrille.setRendererV2(QgsSingleSymbolRendererV2(s))
    
    return layerGrille


def getFieldIndex(layerGrille):
    
    fieldIndex = -1
    
    cpt = 0
    for field in layerGrille.pendingFields():
        if field.name() == CONST_ATTRIBUT_ID:
            fieldIndex = cpt
        cpt = cpt + 1
    
    return fieldIndex


def updateAttId(layerGrille, g):
    
    fieldIndex = getFieldIndex(layerGrille)
    
    layerGrille.startEditing()
    for feature in layerGrille.getFeatures():
        geom = feature.geometry()
        x = geom.centroid().asPoint().x()
        y = geom.centroid().asPoint().y()
        (ifeat, jfeat) = g.getIJ (x,y)
        id = g.getId(ifeat, jfeat)
    
        # 
        layerGrille.changeAttributeValue(feature.id(), fieldIndex, id)
    layerGrille.commitChanges()


def createLayerPoint(proj):
    
    layerStopLine = QgsVectorLayer ("Point?crs=" + proj, CONST_NOM_LAYER_PT_SAISIR, "memory")
            
    # Style
    # Symbologie des stations
    symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,127,0'})
    symbolPoint.setColor(QColor.fromRgb(216,7,96))  #F 216,7,96
    symbolPoint.setSize(2)
    layerStopLine.rendererV2().setSymbol(symbolPoint)
    
    return layerStopLine


def createLayerControle(proj):
    
    layerStopLine = QgsVectorLayer ("Point?crs=" + proj, CONST_NOM_LAYER_PT_CONTROLE, "memory")
                
    # Style
    # Symbologie des stations
    symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,216,0'})
    symbolPoint.setColor(QColor.fromRgb(255,216,0))  #F 216,7,96
    symbolPoint.setSize(2)
    layerStopLine.rendererV2().setSymbol(symbolPoint)
    
    return layerStopLine


def zoomFeature(iface, layer, g, currId):
    
    idx = getFieldIndex(layer)
    
    # On parcours les index jusqu'à celui qu'on a 
    for feature in layer.getFeatures():
        
#        geom = feature.geometry()
#        x = geom.centroid().asPoint().x()
#        y = geom.centroid().asPoint().y()
#        (ifeat, jfeat) = g.getIJ (x,y)
#        id = g.getId(ifeat, jfeat)
        id = feature.attributes()[idx]
        
        if str(id) == currId:
            # zoom sur la couche
            layer.selectByIds([id])
            iface.mapCanvas().zoomToSelected(layer)
            iface.mapCanvas().refresh();
            layer.selectByIds([]);



def setStyleGrilleSaisie(layerGrille, currid):
    
    props1 = {'color': '241,241,241,0', 'size':'0', 'color_border' : '255,0,0', 'width_border':'0.5'}
    symbol1 = QgsFillSymbolV2.createSimple(props1)
                
    props2 = {'color': '255,127,0,0', 'size':'0', 'color_border' : '255,127,0'}
    symbol2 = QgsFillSymbolV2.createSimple(props2)
    
    # On definit les règles de symbologie
    cell_rules = (
            ('Cellule en cours', CONST_ATTRIBUT_ID + ' = ' + str(currid), symbol1),
            ('Autre cellule', CONST_ATTRIBUT_ID + ' != ' + str(currid), symbol2)
    )
    
    # create a new rule-based renderer
    symbol = QgsSymbolV2.defaultSymbol(layerGrille.geometryType())
    renderer = QgsRuleBasedRendererV2(symbol)

    # get the "root" rule
    root_rule = renderer.rootRule()

    for label, expression, symbol in cell_rules:
    
        # create a clone (i.e. a copy) of the default rule
        rule = root_rule.children()[0].clone()
    
        # set the label, expression and color
        rule.setLabel(label)
        rule.setFilterExpression(expression)
    
        # rule.symbol().setColor(QColor(color_name))
        rule.setSymbol(symbol)
    
        # append the rule to the list of rules
        root_rule.appendChild(rule)


    # delete the default rule
    root_rule.removeChildAt(0)

    # apply the renderer to the layer
    layerGrille.setRendererV2(renderer)

    return layerGrille


def setStyleGrilleControle(layerGrille, idList):
    
    # Symbologie: cellule a controler
    props1 = {'color': '241,241,241,0', 'size':'0', 'color_border' : '255,0,0'}
    symbol1 = QgsFillSymbolV2.createSimple(props1)
            
    #props2 = {'color': '255,127,0,0', 'size':'0', 'color_border' : '255,127,0', 'width_border':'1'}
    #symbol2 = QgsFillSymbolV2.createSimple(props2)
       
    # Symbologie: cellule a griser     
    props3 = {'color': '180,180,180', 'size':'1', 'color_border' : '180,180,180'}
    symbol3 = QgsFillSymbolV2.createSimple(props3)
    symbol3.setAlpha(0.70)


    # On definit les règles de symbologie
    txtRule = ' in ('
    for i in range(len(idList)):
        id = idList[i]
        txtRule = txtRule + str(id) + ', '
    txtRule = txtRule[0:len(txtRule) - 2]
    txtRule = txtRule + ')'
    
    cell_rules = (
            ('A controler', CONST_ATTRIBUT_ID + ' ' + txtRule, symbol1),
            ('Pass', CONST_ATTRIBUT_ID + ' not ' + txtRule, symbol3)
    )
    
    # create a new rule-based renderer
    symbol = QgsSymbolV2.defaultSymbol(layerGrille.geometryType())
    renderer = QgsRuleBasedRendererV2(symbol)

    # get the "root" rule
    root_rule = renderer.rootRule()

    for label, expression, symbol in cell_rules:
    
        # create a clone (i.e. a copy) of the default rule
        rule = root_rule.children()[0].clone()
    
        # set the label, expression and color
        rule.setLabel(label)
        rule.setFilterExpression(expression)
    
        # rule.symbol().setColor(QColor(color_name))
        rule.setSymbol(symbol)
    
        # append the rule to the list of rules
        root_rule.appendChild(rule)


    # delete the default rule
    root_rule.removeChildAt(0)

    # apply the renderer to the layer
    layerGrille.setRendererV2(renderer)

    return layerGrille

