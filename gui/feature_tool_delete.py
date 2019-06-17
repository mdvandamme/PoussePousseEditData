# -*- coding: utf-8 -*-
"""
/***************************************************************************
 
 Delete point. Synchonize with layer and file
                              -------------------
        begin                : 2018-07-11
        git sha              : $Format:%H$
        author               : M.-D. Van Damme
 ***************************************************************************/


"""
from qgis.gui import QgsMapTool
from qgis.core import QgsMapLayer
from PyQt4.QtGui import QCursor
from PyQt4.QtCore import Qt

import math
import sys

import util_layer
import util_io
import util_table


class FeatureToolDelete(QgsMapTool):
    
    
    def __init__(self, canvas):
        super(QgsMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)
    
    def activate(self):
        self.canvas.setCursor(self.cursor)
    
    def setTable(self, table):
        self.table = table
        
    def setLayer(self, layer):
        self.layer = layer
        
    def setUrl(self, url):
        self.url = url
    
        
    def canvasReleaseEvent(self, mouseEvent):
        """ 
        Each time the mouse is clicked on the map canvas, perform 
        the following tasks:
            ...
        """
        
        layerGrille = None
        for layer in self.canvas.layers():
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == util_layer.CONST_NOM_LAYER_GRILLE):
                    layerGrille = layer
        
        p = mouseEvent.pos()
        # Determine the location of the click in real-world coords
        layerPoint = self.toLayerCoordinates(layerGrille, p)

        # ====================================================================
        # On cherche le point le plus proche
        d = sys.float_info.max
        indice = -1
        for i in range(self.table.rowCount()):
            x = float(self.table.item(i, 0).text())
            y = float(self.table.item(i, 1).text())
            
            dc = math.sqrt((layerPoint.x() - x)**2 + (layerPoint.y() - y)**2)
            if dc < d:
                d = dc
                indice = i

        # ====================================================================
        # On supprime le point du fichier
        util_io.suppLigne(self.url, indice)
        
        # On supprime les coordonnées du tableau
        self.table = util_table.suppLigne(self.table, indice)
        
        # On supprime le point du layer
        self.layer = util_layer.removeFeature(self.layer, indice)
        
        # ====================================================================
        # Un petit refresh
        self.canvas.refresh();

