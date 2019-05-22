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

from qgis.core import QgsMarkerSymbolV2

# Initialize Qt resources from file resources.py
from resources import resources

# Import the code for the gui
from editdata.geodata_matching_dialog import GeodataMatchingDialog
from editdata.valider_dialog import PluginPoussePousseValideDialog
from editdata.feature_tool_add import FeatureToolAdd
from editdata.feature_tool_delete import FeatureToolDelete

import os.path
import time

# Tirage des points
import sampleConvexHull as tirage

from editdata import util_layer
from editdata import util_io
from editdata import util_table



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
        
        self.uriSettings = os.path.join(self.plugin_dir, 'settings.conf')

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
            text=self.tr(u'Panneau des outils pour la saisie, le contrôle et la validation des données'),
            callback=self.InitPoussePousse,
            parent=self.iface.mainWindow())
        
        # Create a new FeatureToolAdd and keep reference
        self.featureToolAdd = FeatureToolAdd(self.iface.mapCanvas())
        icon_path = ':/plugins/PoussePousseEditData/img/add.png'
        action = self.add_action(
            icon_path,
            text = self.tr(u'Add stop-line.'),
            callback = self.addStopLine,
            parent = self.iface.mainWindow())
        action.setCheckable(True)
        self.featureToolAdd.setAction(action)
        
        # Create a new FeatureToolDelete and keep reference
        icon_path = ':/plugins/PoussePousseEditData/img/delete.png'
        self.featureToolDelete = FeatureToolDelete(self.iface.mapCanvas())
        action = self.add_action(
            icon_path,
            text = self.tr(u'Delete stop-line.'),
            callback = self.deleteStopLine,
            parent = self.iface.mainWindow())
        action.setCheckable(True)
        self.featureToolDelete.setAction(action)


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


    def InitPoussePousse(self):
        """Run method that performs all the real work"""
        
        if not self.pluginIsActive:
            
            self.pluginIsActive = True       
       
            if self.dockwidget == None:
                
                self.dockwidget = GeodataMatchingDialog()
                
                # =======
                #   Settings
                existeFicPoint = False
                
                isSettingsExist = os.path.exists(self.uriSettings)
                if (not isSettingsExist):
                    # on cree le fichier
                    util_io.createSettingsFile(self.uriSettings)
                else:
                    # On recupere les infos pour initialiser
                    uriGrille = util_io.getUrlSettings(self.uriSettings, 'grille')
                    if uriGrille != '':
                        self.dockwidget.fileImportGrille.setFilePath(uriGrille.strip())
                        self.importGrille()
                    uriPtASaisir = util_io.getUrlSettings(self.uriSettings, 'ptASaisir')
                    if uriPtASaisir != '':
                        self.dockwidget.fileOuvrirInventaireCSV.setFilePath(uriPtASaisir.strip())
                        self.importInventaireCSV()
                        existeFicPoint = True
                    
                # On initialise la cellule de démarrage
                self.dockwidget.currentId.setText("0")
                
                if not existeFicPoint:
                    self.dockwidget.tableCoordFeu.setRowCount(0)
                    self.dockwidget.tableCoordFeu.setColumnCount(0)
                
                # Gestion du tableau
                self.featureToolAdd.setTable(self.dockwidget.tableCoordFeu)
                self.featureToolDelete.setTable(self.dockwidget.tableCoordFeu)
                #
                # 
                
                # On active les boutons avec des evenements click
                self.dockwidget.btSuiv.clicked.connect(self.doSuivant)
                self.dockwidget.btGo.clicked.connect(self.goId)
                self.dockwidget.btSynchronize.clicked.connect(self.synchronize)
                self.dockwidget.btZoomGrille.clicked.connect(self.zoomEmprise)
                self.dockwidget.btViderFichier.clicked.connect(self.raz)
                self.dockwidget.btControler.clicked.connect(self.controler)
                
                self.dockwidget.fileImportGrille.fileChanged.connect(self.importGrille)
                self.dockwidget.fileOuvrirInventaireCSV.fileChanged.connect(self.importInventaireCSV)
                
                self.dockwidget.fileControleCSV.setDisabled(True)
                self.dockwidget.fileControleCSV.setText('')
                
                self.dockwidget.btCheck.setDisabled(True)
                
        self.iface.mapCanvas().refresh()
                
        # show the dockwidget
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
        self.dockwidget.show()
        
    #
    def zoomEmprise(self):
        
        layerGrille = util_layer.getLayer('Grille')
        
        if layerGrille != None:
            extent = layerGrille.extent()
            self.iface.mapCanvas().setExtent(extent)
            self.iface.mapCanvas().refresh()
    
    
    def importGrille(self):
        
        # On charge la couche
        uriGrille = self.dockwidget.fileImportGrille.filePath().strip()
        # print (uriGrille)
        
        # 
        layerGrille = util_layer.getLayer('Grille')
        if layerGrille == None:
            layerGrille = util_layer.createLayerGrille(uriGrille)
            QgsMapLayerRegistry.instance().addMapLayer(layerGrille)
        else:
            # On supprime le layer
            QgsMapLayerRegistry.instance().removeMapLayers( [layerGrille.id()] )
            # On reconstruit avec le nouveau fichier
            layerGrille = util_layer.createLayerGrille(uriGrille)
            QgsMapLayerRegistry.instance().addMapLayer(layerGrille)
        
        # Projection pour la construction des autres layers
        self.projGrille = layerGrille.crs().authid()
        
        # On enregistre le chemin dans les settings
        util_io.addUrlSettings(self.uriSettings, 'grille', uriGrille)

        # On intialise les variables de grandeur de la grille
        self.init_param_grille()
        
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
        util_io.addUrlSettings(self.uriSettings, 'ptASaisir', uriSL)
        
        # charge le tableau
        self.dockwidget.tableCoordFeu = util_table.charge(uriSL, self.dockwidget.tableCoordFeu)
            
        # On synchronize layer-fichier
        self.synchronize()
        
        
    
    def synchronize(self):
        
        """
            Tableau est deja chargé
            On prend les infos du fichier vers le layer
        """
        
        # ====================================================
        #    Layer: creer ou supprimer les features
        #
        layerStopLine = util_layer.getLayer('PointsASaisir')
        
        if layerStopLine == None:
            # creation du layer point
            proj = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
            if hasattr(self, 'projGrille') and self.projGrille != None:
                proj = self.projGrille
            layerStopLine = util_layer.createLayerPoint(proj)
            
            # La couche est creee , il faut l'ajouter a l'interface
            QgsMapLayerRegistry.instance().addMapLayer(layerStopLine)
            
        else:
            # le layer existe, on supprime les features
            layerStopLine = util_layer.removeAllFeature(layerStopLine)
            
            
        # ====================================================
        #   On synchronise avec le fichier
        #
        uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
        
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
        
        # ====================================================
        # On passe le layer aux outils click
        self.featureToolAdd.setLayer(layerStopLine)
        self.featureToolDelete.setLayer(layerStopLine)
        
        self.featureToolAdd.setUrl(uriSL)
        self.featureToolDelete.setUrl(uriSL)
        
        # ====================================================
        # On rafraichit le canvas
        self.iface.mapCanvas().refresh();
        
        
    def init_param_grille(self):
        
        # On recupere le layer
        layerGrille = util_layer.getLayer('Grille')
        
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
        # Nombre de cellule par colonne
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
        
        layerGrille = util_layer.getLayer('Grille')
        
        if layerGrille != None:
            # zoom sur la cellule
            util_layer.zoomFeature(self.iface, layerGrille, currId)
            
            # On change le focus si saisie
            changeFocus = True
            layers = QgsMapLayerRegistry.instance().mapLayers().values()
            for layer in layers:
                if layer.type() == QgsMapLayer.VectorLayer:
                    if (layer.name() == 'PointsAControler'):
                        changeFocus = False
                        
            if changeFocus:
                layerGrille = util_layer.setStyleGrilleSaisie(layerGrille, currId)
        
        #        
        self.iface.mapCanvas().refresh();
            
        
    
    def raz(self):
        """
        Vider le fichier des points saisis
        """
        
        # ====================================================
        #    Layer
        layerStopLine = util_layer.getLayer('PointsASaisir')
    
        # On supprime les features du layer
        layerStopLine = util_layer.removeAllFeature(layerStopLine)
        
        
        # ====================================================
        #    Fichier
        #
        uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
        util_io.suppLignePoint(uriSL)
            
        
        # ====================================================
        #    Tableau
        #
        self.dockwidget.tableCoordFeu = util_table.charge(uriSL, self.dockwidget.tableCoordFeu)
            
        
    
    def controler(self):
        
        # popup
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        # ==============================================================================
        # See if OK was pressed
        if result:
            
            # On désactive beaucoup d'action
            self.dockwidget.fileImportGrille.setDisabled(True)
            self.dockwidget.fileOuvrirInventaireCSV.setDisabled(True)
            self.dockwidget.btSynchronize.setDisabled(True)
            self.dockwidget.btViderFichier.setDisabled(True)
            self.dockwidget.btCheck.setDisabled(False)
            
        
            layerStopLine = util_layer.getLayer('PointsASaisir')
            featuresPointEnvConvexe = layerStopLine.getFeatures()
            layerGrille = util_layer.getLayer('Grille')
        
            # On supprime le layer
            if layerStopLine != None:
                QgsMapLayerRegistry.instance().removeMapLayers( [layerStopLine.id()] )
        
            # On crée un nouveau fichier
            uriSL = self.dockwidget.fileOuvrirInventaireCSV.filePath()
            head, tail = os.path.split(uriSL)
            tps = time.strftime("%Y%m%d_%H%M%S")
            chemin = head + '\\ctrl_' + tps + '.dat'
            f = open(chemin, "w+")
            f.write('x,y' + '\n')
            f.close()
            
            self.dockwidget.fileControleCSV.setText(chemin)
            
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
                symbolPoint.setSize(2)
                layerStopLine.rendererV2().setSymbol(symbolPoint)
                
                # La couche est creee , il faut l'ajouter a l'interface
                QgsMapLayerRegistry.instance().addMapLayer(layerStopLine)
                
            
            # On passe le chemin et le layer a l'outil de saisie
            self.featureToolAdd.setLayer(layerStopLine)
            self.featureToolAdd.setUrl(uriSL)
            
            self.featureToolDelete.setLayer(layerStopLine)
            self.featureToolDelete.setUrl(uriSL)
        
            
            # ====================================================
            # ----------------------------------------------------------
            r = 10
            N = int(self.dlg.editNbCellTirage.text())
            #print (nbCell)
            
            xmin = layerGrille.extent().xMinimum()
            xmax = layerGrille.extent().xMaximum()
            ymin = layerGrille.extent().yMinimum()
            ymax = layerGrille.extent().yMaximum()
            
            nx = self.nx
            # print ('nx=' + str(nx))
            ny = self.ny
            r = self.r
            
            # Mode du tirage
            if self.dlg.radioEmprise.isChecked():
                T = tirage.sampleInConvexHull(xmin, ymin, nx, ny, r, N, [[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin]])
            elif self.dlg.radioEnvConvexe.isChecked():
                tabdonnee = []
                for feature in featuresPointEnvConvexe:
                    geom = feature.geometry()
                    x = geom.asPoint().x()
                    y = geom.asPoint().y()
                    tabdonnee.append([x,y])   
                # print (ny)
                T = tirage.sampleInConvexHull(xmin, ymin, nx, ny, r, N, tabdonnee)
            # print (T)
            
            # ----------------------------------------------------------------------------
            # On change le parcours
            self.idList = []
            
            # -----------------------------------------------------------------------------
            #    Style layer
            for feature in layerGrille.getFeatures():
                id = feature.attributes()[0]
                
                # est-ce que tire ?
                tire = False
                for (i,j) in T:
                    j = ny - j
                    encours = (i ) * nx + j
                    
                    if encours == int(id):
                        tire = True
                
                if tire:
                    self.idList.append(int(id))
            # print (self.idList)


            layerGrille = util_layer.setStyleGrilleControle(layerGrille, self.idList)
            
            
            # On initialise la cellule de démarrage
            premier = str(self.idList[0])
            self.dockwidget.currentId.setText(premier)
            self.goTo(premier)
            
            self.zoomEmprise()
            
        
    def addStopLine(self):
        
        self.iface.mapCanvas().setMapTool(self.featureToolAdd)
        
    
    def deleteStopLine(self):
        
        self.iface.mapCanvas().setMapTool(self.featureToolDelete)





