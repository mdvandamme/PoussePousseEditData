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
from PyQt4.QtGui import QTableWidgetItem

from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsPoint, QgsGeometry, QgsFeature

import os.path


class NearestFeatureMapTool(QgsMapTool):
    
    
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
                if (layer.name() == 'Grille'):
                    layerGrille = layer
        
        p = mouseEvent.pos()
        # Determine the location of the click in real-world coords
        layerPoint = self.toLayerCoordinates( layerGrille, p )

        # On ajoute les coordonnées au tableau
        n = self.table.rowCount()
        self.table.insertRow( n );
        
        itemX = QTableWidgetItem(str(layerPoint.x()))
        itemY = QTableWidgetItem(str(layerPoint.y()))
        self.table.setItem(n, 0, itemX);
        self.table.setItem(n, 1, itemY);
        self.table.scrollToBottom();
        
        # On enregistre dans le fichier
        # uriSL = os.path.join(os.path.dirname(__file__) + str('/../resources/feu/'),'stop_line.dat')
        uriSL = self.url
        with open(uriSL, 'a') as file:
            file.write(str(layerPoint.x()) + ',' + str(layerPoint.y()) + '\n')
        file.close()
        
        
        # On synchronise avec le fichier
        self.layer.startEditing()
        pr = self.layer.dataProvider()
        
        geompoint = QgsGeometry.fromPoint(QgsPoint(layerPoint.x(),layerPoint.y()))
        newFeature = QgsFeature()
        newFeature.setGeometry(geompoint)
        pr.addFeatures([newFeature]) 
                
        self.layer.commitChanges() 
        
        QgsMapLayerRegistry.instance().addMapLayer(self.layer)
        self.canvas.refresh();

