# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'geodata_matching_dialog_base.ui'
#
# Created: Tue May 21 17:30:25 2019
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
        DockWidget.resize(373, 675)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(150)
        sizePolicy.setHeightForWidth(DockWidget.sizePolicy().hasHeightForWidth())
        DockWidget.setSizePolicy(sizePolicy)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.btSuiv = QtGui.QPushButton(self.dockWidgetContents)
        self.btSuiv.setGeometry(QtCore.QRect(230, 90, 111, 23))
        self.btSuiv.setObjectName(_fromUtf8("btSuiv"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setGeometry(QtCore.QRect(40, 50, 101, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.currentId = QtGui.QLineEdit(self.dockWidgetContents)
        self.currentId.setGeometry(QtCore.QRect(130, 50, 61, 21))
        self.currentId.setObjectName(_fromUtf8("currentId"))
        self.btGo = QtGui.QPushButton(self.dockWidgetContents)
        self.btGo.setGeometry(QtCore.QRect(200, 50, 75, 23))
        self.btGo.setObjectName(_fromUtf8("btGo"))
        self.tableCoordFeu = QtGui.QTableWidget(self.dockWidgetContents)
        self.tableCoordFeu.setGeometry(QtCore.QRect(10, 300, 341, 181))
        self.tableCoordFeu.setRowCount(5)
        self.tableCoordFeu.setColumnCount(2)
        self.tableCoordFeu.setObjectName(_fromUtf8("tableCoordFeu"))
        self.btSynchronize = QtGui.QPushButton(self.dockWidgetContents)
        self.btSynchronize.setGeometry(QtCore.QRect(30, 500, 181, 23))
        self.btSynchronize.setObjectName(_fromUtf8("btSynchronize"))
        self.fileImportGrille = QgsFileWidget(self.dockWidgetContents)
        self.fileImportGrille.setGeometry(QtCore.QRect(80, 0, 261, 27))
        self.fileImportGrille.setObjectName(_fromUtf8("fileImportGrille"))
        self.label_3 = QtGui.QLabel(self.dockWidgetContents)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line_2 = QtGui.QFrame(self.dockWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(0, 130, 371, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_4 = QtGui.QLabel(self.dockWidgetContents)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 261, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.btPrec = QtGui.QPushButton(self.dockWidgetContents)
        self.btPrec.setGeometry(QtCore.QRect(120, 90, 111, 23))
        self.btPrec.setObjectName(_fromUtf8("btPrec"))
        self.btZoomGrille = QtGui.QPushButton(self.dockWidgetContents)
        self.btZoomGrille.setGeometry(QtCore.QRect(20, 90, 101, 23))
        self.btZoomGrille.setObjectName(_fromUtf8("btZoomGrille"))
        self.fileOuvrirInventaireCSV = QgsFileWidget(self.dockWidgetContents)
        self.fileOuvrirInventaireCSV.setGeometry(QtCore.QRect(80, 180, 251, 27))
        self.fileOuvrirInventaireCSV.setObjectName(_fromUtf8("fileOuvrirInventaireCSV"))
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(20, 190, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_5 = QtGui.QLabel(self.dockWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(170, 210, 191, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(8)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.btViderFichier = QtGui.QPushButton(self.dockWidgetContents)
        self.btViderFichier.setGeometry(QtCore.QRect(210, 500, 111, 23))
        self.btViderFichier.setObjectName(_fromUtf8("btViderFichier"))
        self.btControler = QtGui.QPushButton(self.dockWidgetContents)
        self.btControler.setGeometry(QtCore.QRect(20, 570, 321, 23))
        self.btControler.setObjectName(_fromUtf8("btControler"))
        self.label_6 = QtGui.QLabel(self.dockWidgetContents)
        self.label_6.setGeometry(QtCore.QRect(20, 280, 151, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.line_3 = QtGui.QFrame(self.dockWidgetContents)
        self.line_3.setGeometry(QtCore.QRect(0, 540, 371, 16))
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.label_7 = QtGui.QLabel(self.dockWidgetContents)
        self.label_7.setGeometry(QtCore.QRect(10, 240, 71, 20))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.fileControleCSV = QtGui.QLineEdit(self.dockWidgetContents)
        self.fileControleCSV.setEnabled(False)
        self.fileControleCSV.setGeometry(QtCore.QRect(80, 240, 251, 20))
        self.fileControleCSV.setObjectName(_fromUtf8("fileControleCSV"))
        self.btValider = QtGui.QPushButton(self.dockWidgetContents)
        self.btValider.setGeometry(QtCore.QRect(20, 600, 321, 23))
        self.btValider.setObjectName(_fromUtf8("btValider"))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "PoussePousseEditData", None))
        self.btSuiv.setText(_translate("DockWidget", ">>", None))
        self.label.setText(_translate("DockWidget", "Cellule en cours :", None))
        self.btGo.setText(_translate("DockWidget", "Go", None))
        self.btSynchronize.setText(_translate("DockWidget", "Synchroniser le fichier et le layer", None))
        self.label_3.setText(_translate("DockWidget", "Import grille:", None))
        self.label_4.setText(_translate("DockWidget", "Fichier de saisie des données ponctuelles:", None))
        self.btPrec.setText(_translate("DockWidget", "<<", None))
        self.btZoomGrille.setText(_translate("DockWidget", "Zoom Grille", None))
        self.label_2.setText(_translate("DockWidget", "Import CSV:", None))
        self.label_5.setText(_translate("DockWidget", "Caractère séparateur \",\" Avec Entête", None))
        self.btViderFichier.setText(_translate("DockWidget", "Vider fichier", None))
        self.btControler.setText(_translate("DockWidget", "Contrôler la saisie", None))
        self.label_6.setText(_translate("DockWidget", "Vue sur le fichier en cours:", None))
        self.label_7.setText(_translate("DockWidget", "Contrôle CSV:", None))
        self.btValider.setText(_translate("DockWidget", "Valider", None))

from qgis.gui import QgsFileWidget
