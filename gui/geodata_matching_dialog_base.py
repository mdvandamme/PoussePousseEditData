# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'geodata_matching_dialog_base.ui'
#
# Created: Fri May 03 11:34:26 2019
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(274, 626)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(150)
        sizePolicy.setHeightForWidth(DockWidget.sizePolicy().hasHeightForWidth())
        DockWidget.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.btSuiv = QtGui.QPushButton(self.dockWidgetContents)
        self.btSuiv.setGeometry(QtCore.QRect(140, 240, 111, 23))
        self.btSuiv.setObjectName(_fromUtf8("btSuiv"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(10, 210, 101, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.currentId = QtGui.QLineEdit(self.dockWidgetContents)
        self.currentId.setGeometry(QtCore.QRect(100, 210, 61, 21))
        self.currentId.setObjectName(_fromUtf8("currentId"))
        self.btGo = QtGui.QPushButton(self.dockWidgetContents)
        self.btGo.setGeometry(QtCore.QRect(170, 210, 75, 23))
        self.btGo.setObjectName(_fromUtf8("btGo"))
        self.tableCoordFeu = QtGui.QTableWidget(self.dockWidgetContents)
        self.tableCoordFeu.setGeometry(QtCore.QRect(10, 320, 251, 181))
        self.tableCoordFeu.setRowCount(5)
        self.tableCoordFeu.setColumnCount(2)
        self.tableCoordFeu.setObjectName(_fromUtf8("tableCoordFeu"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 121, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.feuFilename = QtGui.QLineEdit(self.dockWidgetContents)
        self.feuFilename.setGeometry(QtCore.QRect(110, 110, 151, 20))
        self.feuFilename.setReadOnly(True)
        self.feuFilename.setObjectName(_fromUtf8("feuFilename"))
        self.btOuvrir = QtGui.QPushButton(self.dockWidgetContents)
        self.btOuvrir.setGeometry(QtCore.QRect(40, 140, 191, 23))
        self.btOuvrir.setObjectName(_fromUtf8("btOuvrir"))
        self.fileImportGrille = QgsFileWidget(self.dockWidgetContents)
        self.fileImportGrille.setGeometry(QtCore.QRect(40, 30, 211, 27))
        self.fileImportGrille.setObjectName(_fromUtf8("fileImportGrille"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setGeometry(QtCore.QRect(0, 70, 271, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.line_2 = QtGui.QFrame(self.dockWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(0, 180, 271, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.line_3 = QtGui.QFrame(self.dockWidgetContents)
        self.line_3.setGeometry(QtCore.QRect(0, 290, 271, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "PoussePousseEditData", None))
        self.btSuiv.setText(_translate("DockWidget", ">>", None))
        self.label.setText(_translate("DockWidget", "Cellule en cours :", None))
        self.btGo.setText(_translate("DockWidget", "Go", None))
        self.label_2.setText(_translate("DockWidget", "Fichier en cours : ", None))
        self.btOuvrir.setText(_translate("DockWidget", "Synchroniser le fichier et le layer", None))
        self.label_3.setText(_translate("DockWidget", "Import grille:", None))

from qgis.gui import QgsFileWidget
