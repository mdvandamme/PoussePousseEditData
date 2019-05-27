# -*- coding: utf-8 -*-
"""
/***************************************************************************
 
 Create new point. Synchonize with layer and file
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

import util_table
import util_layer
import util_io

class FeatureToolAdd(QgsMapTool):
    
    
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
        layerPoint = self.toLayerCoordinates( layerGrille, p )

        # =============================================================================
        #   Ajout dans le layer, tableau, fichier
        
        # On ajoute la ligne au tableau
        self.table = util_table.addLigne(self.table, layerPoint.x(), layerPoint.y())
        
        # On enregistre dans le fichier
        util_io.addLigne(self.url, layerPoint.x(), layerPoint.y())
        
        # On synchronise avec le layer
        self.layer = util_layer.addPointLayer(self.layer, layerPoint.x(), layerPoint.y())
        
        # ====================================================================
        # Un petit refresh
        # QgsMapLayerRegistry.instance().addMapLayer(self.layer)
        self.canvas.refresh();

