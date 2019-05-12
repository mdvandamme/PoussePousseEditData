# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PoussePousseEditData
                                 A QGIS plugin
                                 
 PoussePousseEditData est un plugIn QGis de création et de contrôle 
       de jeu de données géographiques sur fond cartographique
                              -------------------
        begin                : 2018-07-09
        git sha              : $Format:%H$
        copyright            : (C) 2018 by IGN
        email                : marie-dominique.van-damme@ign.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon, QTableWidgetItem, QColor

from qgis.core import QgsVectorLayer, QgsMapLayer
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsPoint, QgsGeometry, QgsFeature

from qgis.core import QgsFillSymbolV2, QgsSingleSymbolRendererV2, QgsMarkerSymbolV2
from qgis.core import QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2

# Initialize Qt resources from file resources.py
from resources import resources

# Import the code for the gui
from gui.geodata_matching_dialog import GeodataMatchingDialog
from gui.nearest_feature_map_tool import NearestFeatureMapTool
from gui.valider_dialog import PluginPoussePousseValideDialog

import os.path
import time


class ParcoursGrille:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PoussePousseEditData_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        #self.dlg = GeodataMatchingDialog()
        self.pluginIsActive = False
        self.dockwidget = None

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PoussePousseEditData')
        
        # We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PoussePousseEditData')
        self.toolbar.setObjectName(u'PoussePousseEditData')
        
        self.dlg = PluginPoussePousseValideDialog()
        

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PoussePousseEditData', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar."""

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action
    

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PoussePousseEditData/img/logoPoussePousseEditData.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Panneau des outils pour la saisie et la validation des données'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # Create a new NearestFeatureMapTool and keep reference
        self.nearestFeatureMapTool = NearestFeatureMapTool(self.iface.mapCanvas())
        icon_path = ':/plugins/PoussePousseEditData/img/CreateStopLine.png'
        action = self.add_action(
            icon_path,
            text = self.tr(u'Add stop-line.'),
            callback = self.addStopLine,
            parent = self.iface.mainWindow())
        action.setCheckable(True)
        self.nearestFeatureMapTool.setAction(action)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PoussePousseEditData'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
    
    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.pluginIsActive = False


    def run(self):
        """Run method that performs all the real work"""
        
        if not self.pluginIsActive:
            self.pluginIsActive = True       
       
            if self.dockwidget == None:
                self.dockwidget = GeodataMatchingDialog()
                
                # On initialise la cellule de démarrage
                self.dockwidget.currentId.setText("0")
                
                # Gestion des fichiers
                # self.dockwidget.feuFilename.setDisabled(True);
                
                # Gestion du tableau
                self.dockwidget.tableCoordFeu.setRowCount(0);
                self.dockwidget.tableCoordFeu.setColumnCount(0);
                self.nearestFeatureMapTool.setTable(self.dockwidget.tableCoordFeu)
                
                # On active les boutons avec des evenements click
                self.dockwidget.btSuiv.clicked.connect(self.doSuivant)
                self.dockwidget.btGo.clicked.connect(self.goId)
                self.dockwidget.btSynchronize.clicked.connect(self.synchronize)
                self.dockwidget.btZoomGrille.clicked.connect(self.zoomEmprise)
                self.dockwidget.btViderFichier.clicked.connect(self.raz)
                self.dockwidget.btValider.clicked.connect(self.valider)
                
                self.dockwidget.fileImportGrille.fileChanged.connect(self.importGrille)
                self.dockwidget.fileOuvrirInventaireCSV.fileChanged.connect(self.importInventaireCSV)
                
        # show the dockwidget
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        self.dockwidget.show()
        
    def zoomEmprise(self):
        layerGrille = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'Grille'):
                    layerGrille = layer
        
        extent = layerGrille.extent()
        self.iface.mapCanvas().setExtent(extent)
        self.iface.mapCanvas().refresh();
    
    def addStopLine(self):
        
        self.iface.mapCanvas().setMapTool(self.nearestFeatureMapTool)
        
        
    def importGrille(self):
        
        # On charge la couche
        uri = self.dockwidget.fileImportGrille.filePath()
        # print (uri)
        layerGrille = QgsVectorLayer(uri, "Grille", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layerGrille)
        
        self.projGrille = layerGrille.crs().authid()

        # Style 
        props = {'color': '241,241,241,0', 'size':'1', 'color_border' : '255,0,0'}
        s = QgsFillSymbolV2.createSimple(props)
        layerGrille.setRendererV2(QgsSingleSymbolRendererV2(s))
        
        self.goTo("0")

        self.zoomEmprise()
        self.iface.mapCanvas().refresh();
        
        
        
    def importInventaireCSV(self):
        
        # ====================================================
        #    Fichier CSV
        #
        # self.dockwidget.feuFilename.setText("stop_line.dat")
        #self.uriSL = os.path.join(os.path.dirname(__file__) + str('/resources/feu/'),'stop_line.dat')
        #isSLExist = os.path.exists(self.uriSL)
        self.uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
        
        with open(self.uriSL) as f:
            i = 0
            num_lines = sum(1 for line in open(self.uriSL))
            self.dockwidget.tableCoordFeu.setRowCount(num_lines - 1);
            
            cpt = 0
            for line in f:
                if cpt == 0:
                    # Ligne d'entete
                    entetes = line.strip().split(",")
                    self.dockwidget.tableCoordFeu.setColumnCount(len(entetes));
                    colHearder = []
                    for j in range(len(entetes)):
                        nom = entetes[j]
                        colHearder.append(nom)
                    self.dockwidget.tableCoordFeu.setHorizontalHeaderLabels(colHearder)
                else:
                    coord = line.strip().split(",")
                    if len(coord) > 1:
                        itemX = QTableWidgetItem(str(coord[0]))
                        itemY = QTableWidgetItem(str(coord[1]))
                        self.dockwidget.tableCoordFeu.setItem(i, 0, itemX)
                        self.dockwidget.tableCoordFeu.setItem(i, 1, itemY)
                        i = i + 1
                cpt = cpt + 1
            
            f.close()
            
        # On synchronize layer-fichier
        self.synchronize()
        
    
    def synchronize(self):
        # ====================================================
        #    Layer
        #
        self.layerStopLine = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsASaisir'):
                    self.layerStopLine = layer
        
        if self.layerStopLine == None:
            # creation du layer point
            proj = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            if hasattr(self, 'projGrille') and self.projGrille != None:
                proj = self.projGrille
            self.layerStopLine = QgsVectorLayer ("Point?crs=" + proj, "PointsASaisir", "memory")
            
            # Style
            # Symbologie des stations
            symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,127,0'})
            symbolPoint.setColor(QColor.fromRgb(216,7,96))  #F 216,7,96
            symbolPoint.setSize(3)
            self.layerStopLine.rendererV2().setSymbol(symbolPoint)
            
            # La couche est creee , il faut l'ajouter a l'interface
            QgsMapLayerRegistry.instance().addMapLayer(self.layerStopLine)
            
        else:
            # le layer existe, on supprime les features
            self.layerStopLine.startEditing()
            for feature in self.layerStopLine.getFeatures():
                self.layerStopLine.deleteFeature(feature.id())
            self.layerStopLine.commitChanges()
            

        # On passe le layer à l'outil click
        self.nearestFeatureMapTool.setLayer(self.layerStopLine)
        self.nearestFeatureMapTool.setUrl(self.uriSL)
        
        
        # On synchronise avec le fichier
        cpt = 0
        self.layerStopLine.startEditing()
        pr = self.layerStopLine.dataProvider()
        with open(self.uriSL) as f:
            for line in f:
                if cpt > 0:
                    coord = line.strip().split(",")
                    if len(coord) > 1:
                        geompoint = QgsGeometry.fromPoint(QgsPoint(float(coord[0]), float(coord[1])))
                        newFeature = QgsFeature()
                        newFeature.setGeometry(geompoint)
                        pr.addFeatures([newFeature]) 
                cpt = cpt + 1
        self.layerStopLine.commitChanges() 
        
        # On rafraichit le canvas
        self.iface.mapCanvas().refresh();
        
        
    
    def doSuivant(self):
        
        # On recupere l'id en cours
        currId = self.dockwidget.currentId.text()
        
        # On recupere le layer
        layerGrille = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'Grille'):
                    layerGrille = layer
        
        
        # Liste des identifiants
        idList = []
        for feature in layerGrille.getFeatures():
            id = feature.attributes()[0]
            idList.append(id)
            
        # Nombre de cellule par ligne
        xmax = 0
        cpt = 0
        for feature in layerGrille.getFeatures():
            geom = feature.geometry()
            if cpt > 0:
                if geom.boundingBox().xMaximum() > xmax:
                    xmax = geom.boundingBox().xMaximum()
                else:
                    break
            else:
                xmax = geom.boundingBox().xMaximum()
            cpt = cpt + 1
        nCell = cpt
        
        # On permutte tous les nCell
        cpt = 0
        for i in range(0, len(idList), nCell):
            if ((cpt%2) == 1):
                # On permutte
                for j in range (i, int((i + i + nCell) / 2)):
                    k = j - i
                    t = idList[i + nCell - 1 - k]
                    idList[i + nCell - 1 - k] = idList[i + k]
                    idList[i + k] = t
            cpt = cpt + 1
        # print (idList)
        

        # On cherche l'index de la valeur currId
        newindex = 0
        for i in range(len(idList)):
            if (idList[i] == int(currId)):
                newindex = i
        if (newindex < (len(idList) - 1)):
            # incremente au suivant
            nextId = idList[newindex + 1]
            self.dockwidget.currentId.setText(str(nextId))
            self.goTo(str(nextId))
        
                
                
    def goId(self):
        
        # On recupere l'id en cours
        currId = self.dockwidget.currentId.text()
        self.goTo(currId)
        
        
        
    def goTo(self, currId):
        
        layerGrille = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'Grille'):
                    layerGrille = layer
        
        # On parcours les index jusqu'à celui qu'on a 
        for feature in layerGrille.getFeatures():
            id = feature.attributes()[0]
            if str(id) == currId:
                # zoom sur la couche
                layerGrille.setSelectedFeatures([id]);
                self.iface.mapCanvas().zoomToSelected(layerGrille)
                self.iface.mapCanvas().refresh();
                layerGrille.setSelectedFeatures([]);
        
        # On change le focus
        props1 = {'color': '241,241,241,0', 'size':'0', 'color_border' : '255,0,0'}
        symbol1 = QgsFillSymbolV2.createSimple(props1)
        
        props2 = {'color': '255,127,0,0', 'size':'0', 'color_border' : '255,127,0', 'width_border':'1'}
        symbol2 = QgsFillSymbolV2.createSimple(props2)
        
        categories = []
        for feature in layerGrille.getFeatures():
            id = feature.attributes()[0]
            if str(id) == currId:
                category = QgsRendererCategoryV2(id, symbol2, str(id))
                categories.append(category)
            else:
                category = QgsRendererCategoryV2(id, symbol1, str(id))
                categories.append(category)
        
        
        # Create the renderer and assign it to a layer
        expression = 'id' # Field name
        renderer = QgsCategorizedSymbolRendererV2(expression, categories)
        layerGrille.setRendererV2(renderer)
        
        self.iface.mapCanvas().refresh();
            
    
    def raz(self):
        
        # ====================================================
        #    Layer
        #
        layerStopLine = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsASaisir'):
                    layerStopLine = layer
    
        # On supprime les features du layer
        # pr = layerStopLine.dataProvider()
        layerStopLine.startEditing()
            
        for feat in layerStopLine.getFeatures():
            layerStopLine.deleteFeature(feat.id())
            
        # commit to stop editing the layer
        layerStopLine.commitChanges()
        
        
        # ====================================================
        #    Fichier
        #
        # On recupere la ligne d'entete
        uriSL = self.uriSL
        txtEntete = ''
        with open(uriSL, 'r') as file:
            for line in file:
                txtEntete = line
                break
            file.close()
            
        # On vide le fichier
        with open(uriSL, "w") as file:
            file.write(txtEntete)
            file.close()
            
        file.close()
        
        
        #
        with open(self.uriSL) as f:
            i = 0
            num_lines = sum(1 for line in open(self.uriSL))
            self.dockwidget.tableCoordFeu.setRowCount(num_lines - 1);
            
            cpt = 0
            for line in f:
                if cpt == 0:
                    # Ligne d'entete
                    entetes = line.strip().split(",")
                    self.dockwidget.tableCoordFeu.setColumnCount(len(entetes));
                    colHearder = []
                    for j in range(len(entetes)):
                        nom = entetes[j]
                        colHearder.append(nom)
                    self.dockwidget.tableCoordFeu.setHorizontalHeaderLabels(colHearder)
                else:
                    coord = line.strip().split(",")
                    if len(coord) > 1:
                        itemX = QTableWidgetItem(str(coord[0]))
                        itemY = QTableWidgetItem(str(coord[1]))
                        self.dockwidget.tableCoordFeu.setItem(i, 0, itemX)
                        self.dockwidget.tableCoordFeu.setItem(i, 1, itemY)
                        i = i + 1
                cpt = cpt + 1
            
            f.close()
            
    
    def valider(self):
        
        # On désactive le fichier d'inventaire
        self.dockwidget.fileOuvrirInventaireCSV.setDisabled(True)
        self.dockwidget.btSynchronize.setDisabled(True)
        self.dockwidget.btViderFichier.setDisabled(True)
        
        # On supprime le layer
        layerStopLine = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsASaisir'):
                    layerStopLine = layer
        if layerStopLine != None:
            QgsMapLayerRegistry.instance().removeMapLayers( [layerStopLine.id()] )
        
        # On crée un nouveau fichier
        # on cree le fichier
        self.uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
        head, tail = os.path.split(self.uriSL)
        
        tps = time.strftime("%Y_%m_%d_%H_%M_%S")
        chemin = head + '\\validation_' + tps + '.dat'
        f = open(chemin, "w+")
        f.write('x,y' + '\n')
        f.close()
        
        self.uriSL = chemin
        
        # Vider le tableau
        with open(self.uriSL) as f:
            i = 0
            num_lines = sum(1 for line in open(self.uriSL))
            self.dockwidget.tableCoordFeu.setRowCount(num_lines - 1);
            
            cpt = 0
            for line in f:
                if cpt == 0:
                    # Ligne d'entete
                    entetes = line.strip().split(",")
                    self.dockwidget.tableCoordFeu.setColumnCount(len(entetes));
                    colHearder = []
                    for j in range(len(entetes)):
                        nom = entetes[j]
                        colHearder.append(nom)
                    self.dockwidget.tableCoordFeu.setHorizontalHeaderLabels(colHearder)
                else:
                    coord = line.strip().split(",")
                    if len(coord) > 1:
                        itemX = QTableWidgetItem(str(coord[0]))
                        itemY = QTableWidgetItem(str(coord[1]))
                        self.dockwidget.tableCoordFeu.setItem(i, 0, itemX)
                        self.dockwidget.tableCoordFeu.setItem(i, 1, itemY)
                        i = i + 1
                cpt = cpt + 1
            
            f.close()
            
        # On cree un layer de validation
        # ====================================================
        #    Layer
        #
        self.layerStopLine = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsAControler'):
                    self.layerStopLine = layer
        
        if self.layerStopLine == None:
            # creation du layer point
            proj = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            if hasattr(self, 'projGrille') and self.projGrille != None:
                proj = self.projGrille
            self.layerStopLine = QgsVectorLayer ("Point?crs=" + proj, "PointsAControler", "memory")
            
            # Style
            # Symbologie des stations
            symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,216,0'})
            symbolPoint.setColor(QColor.fromRgb(255,216,0))  #F 216,7,96
            symbolPoint.setSize(3)
            self.layerStopLine.rendererV2().setSymbol(symbolPoint)
            
            # La couche est creee , il faut l'ajouter a l'interface
            QgsMapLayerRegistry.instance().addMapLayer(self.layerStopLine)
            
            
        # On passe le chemin et le layer a l'outil de saisie
        self.nearestFeatureMapTool.setLayer(self.layerStopLine)
        self.nearestFeatureMapTool.setUrl(self.uriSL)
        
        # popup
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            nbCell = int(self.dlg.editNbCellTirage.text())
            print (nbCell)
        