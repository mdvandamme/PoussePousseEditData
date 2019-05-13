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

# Tirage des points
import sampleConvexHull as tirage


class ParcoursGrille:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor."""
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
        
        # remove layer ?
        
    
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
                
                # =======
                #   Settings
                trouve = False
                self.uriSettings = os.path.join(self.plugin_dir,'settings.conf')
                isSettingsExist = os.path.exists(self.uriSettings)
                if (not isSettingsExist):
                    # on cree le fichier
                    f = open(self.uriSettings, "w+")
                    f.close()
                else:
                    # On recupere les infos pour initialiser
                    
                    with open(self.uriSettings) as f:
                        for line in f:
                            
                            prefix = 'grille'
                            if line.strip().startswith(prefix):
                                uriGrille = line[7:len(line)]
                                self.dockwidget.fileImportGrille.setFilePath(uriGrille.strip())
                                self.importGrille()
                            
                            prefix = 'ptASaisir'
                            if line.strip().startswith(prefix):
                                uriPtASaisir = line[10:len(line)]
                                self.dockwidget.fileOuvrirInventaireCSV.setFilePath(uriPtASaisir.strip())
                                self.importInventaireCSV()
                                trouve = True
                                
                                
                            
                    f.close()
        
                # On initialise la cellule de démarrage
                self.dockwidget.currentId.setText("0")
                
                if not trouve:
                    self.dockwidget.tableCoordFeu.setRowCount(0)
                    self.dockwidget.tableCoordFeu.setColumnCount(0)
                
                # Gestion des fichiers
                # self.dockwidget.feuFilename.setDisabled(True);
                
                # Gestion du tableau
                self.nearestFeatureMapTool.setTable(self.dockwidget.tableCoordFeu)
                
                #
                # 
                
                # On active les boutons avec des evenements click
                self.dockwidget.btSuiv.clicked.connect(self.doSuivant)
                self.dockwidget.btGo.clicked.connect(self.goId)
                self.dockwidget.btSynchronize.clicked.connect(self.synchronize)
                self.dockwidget.btZoomGrille.clicked.connect(self.zoomEmprise)
                self.dockwidget.btViderFichier.clicked.connect(self.raz)
                self.dockwidget.btValider.clicked.connect(self.valider)
                
                self.dockwidget.fileImportGrille.fileChanged.connect(self.importGrille)
                self.dockwidget.fileOuvrirInventaireCSV.fileChanged.connect(self.importInventaireCSV)
                
        self.iface.mapCanvas().refresh()
                
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
        
        if layerGrille != None:
            extent = layerGrille.extent()
            self.iface.mapCanvas().setExtent(extent)
            self.iface.mapCanvas().refresh()
    
    
    def addStopLine(self):
        
        self.iface.mapCanvas().setMapTool(self.nearestFeatureMapTool)
        
        
    def importGrille(self):
        
        # On charge la couche
        uriGrille = self.dockwidget.fileImportGrille.filePath().strip()
        # print (uriGrille)
        
        # print (uri)
#        layerGrille = None
#        layers = QgsMapLayerRegistry.instance().mapLayers().values()
#        for layer in layers:
#            if layer.type() == QgsMapLayer.VectorLayer:
#                if (layer.name() == 'Grille'):
#                    layerGrille = layer
        
#        if layerGrille == None:
        layerGrille = QgsVectorLayer(uriGrille, "Grille", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layerGrille)
        
        self.projGrille = layerGrille.crs().authid()

        # Style 
        props = {'color': '241,241,241,0', 'size':'1', 'color_border' : '255,0,0'}
        s = QgsFillSymbolV2.createSimple(props)
        layerGrille.setRendererV2(QgsSingleSymbolRendererV2(s))
        
        # On intialise les variables de grandeur de la grille
        self.init_param_grille()
        
        # On enregistre le chemin dans les settings
        self.settings('grille', uriGrille)
        
        self.goTo("0")

        self.zoomEmprise()
        self.iface.mapCanvas().refresh();
        
        
        
    def importInventaireCSV(self):
        
        # ====================================================
        #    Fichier CSV
        #
        uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath().strip()
        # print (uriSL)
        
        # On enregistre le chemin dans les settings
        self.settings('ptASaisir', uriSL)
        
        with open(uriSL) as f:
            i = 0
            num_lines = sum(1 for line in open(uriSL))
            #print (num_lines)
            self.dockwidget.tableCoordFeu.setRowCount(num_lines - 1)
            
            cpt = 0
            for line in f:
                if cpt == 0:
                    # Ligne d'entete
                    entetes = line.strip().split(",")
                    # print (len(entetes))
                    self.dockwidget.tableCoordFeu.setColumnCount(len(entetes))
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
        layerStopLine = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsASaisir'):
                    layerStopLine = layer
        
        if layerStopLine == None:
            # creation du layer point
            proj = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            if hasattr(self, 'projGrille') and self.projGrille != None:
                proj = self.projGrille
            layerStopLine = QgsVectorLayer ("Point?crs=" + proj, "PointsASaisir", "memory")
            
            # Style
            # Symbologie des stations
            symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,127,0'})
            symbolPoint.setColor(QColor.fromRgb(216,7,96))  #F 216,7,96
            symbolPoint.setSize(3)
            layerStopLine.rendererV2().setSymbol(symbolPoint)
            
            # La couche est creee , il faut l'ajouter a l'interface
            QgsMapLayerRegistry.instance().addMapLayer(layerStopLine)
            
        else:
            # le layer existe, on supprime les features
            layerStopLine.startEditing()
            for feature in layerStopLine.getFeatures():
                layerStopLine.deleteFeature(feature.id())
            layerStopLine.commitChanges()
            

        # On passe le layer à l'outil click
        self.nearestFeatureMapTool.setLayer(layerStopLine)
        uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
        self.nearestFeatureMapTool.setUrl(uriSL)
        
        
        # On synchronise avec le fichier
        cpt = 0
        layerStopLine.startEditing()
        pr = layerStopLine.dataProvider()
        with open(uriSL) as f:
            for line in f:
                if cpt > 0:
                    coord = line.strip().split(",")
                    if len(coord) > 1:
                        geompoint = QgsGeometry.fromPoint(QgsPoint(float(coord[0]), float(coord[1])))
                        newFeature = QgsFeature()
                        newFeature.setGeometry(geompoint)
                        pr.addFeatures([newFeature]) 
                cpt = cpt + 1
        layerStopLine.commitChanges() 
        
        # On rafraichit le canvas
        self.iface.mapCanvas().refresh();
        
        
    def init_param_grille(self):
        
        # On recupere le layer
        layerGrille = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'Grille'):
                    layerGrille = layer
        
        
        # Liste des identifiants
        self.idList = []
        for feature in layerGrille.getFeatures():
            id = feature.attributes()[0]
            self.idList.append(id)
            
        # Nombre de cellule par ligne
        xmax = 0
        self.r = 0
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
                self.r = xmax - geom.boundingBox().xMinimum()
            cpt = cpt + 1
        self.nx = cpt
        
        # Nombre de cellule par colonne
        nb = layerGrille.featureCount()
        # print (nb)
        self.ny = nb / self.nx
        
        # On permutte toutes les nCell de x
        cpt = 0
        for i in range(0, len(self.idList), self.nx):
            if ((cpt%2) == 1):
                # On permutte
                for j in range (i, int((i + i + self.nx) / 2)):
                    k = j - i
                    t = self.idList[i + self.nx - 1 - k]
                    self.idList[i + self.nx - 1 - k] = self.idList[i + k]
                    self.idList[i + k] = t
            cpt = cpt + 1
        # print (idList)
        
    
    def doSuivant(self):
        
        # On recupere l'id en cours
        currId = self.dockwidget.currentId.text()
        
        # On cherche l'index de la valeur currId
        newindex = 0
        for i in range(len(self.idList)):
            if (self.idList[i] == int(currId)):
                newindex = i
        if (newindex < (len(self.idList) - 1)):
            # incremente au suivant
            nextId = self.idList[newindex + 1]
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
        
        if layerGrille != None:
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
        uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
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
        with open(uriSL) as f:
            i = 0
            num_lines = sum(1 for line in open(uriSL))
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
        layerGrille = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsASaisir'):
                    layerStopLine = layer
                if layer.name() == 'Grille':
                    layerGrille = layer
        
        if layerStopLine != None:
            QgsMapLayerRegistry.instance().removeMapLayers( [layerStopLine.id()] )
        
        # On crée un nouveau fichier
        # on cree le fichier
        uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
        head, tail = os.path.split(uriSL)
        
        tps = time.strftime("%Y_%m_%d_%H_%M_%S")
        chemin = head + '\\validation_' + tps + '.dat'
        f = open(chemin, "w+")
        f.write('x,y' + '\n')
        f.close()
        
        uriSL = chemin
        
        # Vider le tableau
        with open(uriSL) as f:
            i = 0
            num_lines = sum(1 for line in open(uriSL))
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
        layerStopLine = None
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                if (layer.name() == 'PointsAControler'):
                    layerStopLine = layer
        
        if layerStopLine == None:
            # creation du layer point
            proj = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            if hasattr(self, 'projGrille') and self.projGrille != None:
                proj = self.projGrille
            layerStopLine = QgsVectorLayer ("Point?crs=" + proj, "PointsAControler", "memory")
            
            # Style
            # Symbologie des stations
            symbolPoint = QgsMarkerSymbolV2.createSimple({'name': 'square', 'color_border': '255,216,0'})
            symbolPoint.setColor(QColor.fromRgb(255,216,0))  #F 216,7,96
            symbolPoint.setSize(3)
            layerStopLine.rendererV2().setSymbol(symbolPoint)
            
            # La couche est creee , il faut l'ajouter a l'interface
            QgsMapLayerRegistry.instance().addMapLayer(layerStopLine)
            
            
        # On passe le chemin et le layer a l'outil de saisie
        self.nearestFeatureMapTool.setLayer(layerStopLine)
        self.nearestFeatureMapTool.setUrl(uriSL)
        
        # popup
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        # See if OK was pressed
        if result:
            
            r = 10
            N = int(self.dlg.editNbCellTirage.text())
            #print (nbCell)
            
            xmin = layerGrille.extent().xMinimum()
            xmax = layerGrille.extent().xMaximum()
            ymin = layerGrille.extent().yMinimum()
            ymax = layerGrille.extent().yMaximum()
            
            nx = self.nx
            ny = self.ny
            r = self.r
            
            T = tirage.sampleInConvexHull(xmin, ymin, nx, ny, r, N, [[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin]])
            print (T)
            
            
    def settings(self, cle, newUrl):
        
        uriGrille = ''
        uriPtASaisir = ''
        
        # On ouvre le fichier et on enregistre les clés
        with open(self.uriSettings) as f:
            for line in f:
                # entetes = line.strip().split(",")
                prefix = 'grille'
                if line.strip().startswith(prefix):
                    uriGrille = line[7:len(line)]
                
                prefix = 'ptASaisir'
                if line.strip().startswith(prefix):
                    uriPtASaisir = line[10:len(line)]
                    
            f.close()
    
        f = open(self.uriSettings, "w+")
        
        if cle == 'grille':
            f.write('grille:' + newUrl + '\n')
        else:
            if uriGrille != '':
                f.write('grille:' + uriGrille + '\n')
                
        if cle == 'ptASaisir':
            f.write('ptASaisir:' + newUrl + '\n')
        else:
            if uriPtASaisir != '':
                f.write('ptASaisir:' + uriPtASaisir + '\n')
                
        # On ferme le fichier
        f.close()
            
        