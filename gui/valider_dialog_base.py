# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'valider_dialog_base.ui'
#
# Created: Tue Jul 09 09:11:19 2019
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(470, 185)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(140, 140, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.radioEmprise = QtGui.QRadioButton(Dialog)
        self.radioEmprise.setGeometry(QtCore.QRect(207, 20, 95, 20))
        self.radioEmprise.setChecked(True)
        self.radioEmprise.setObjectName(_fromUtf8("radioEmprise"))
        self.radioEnvConvexe = QtGui.QRadioButton(Dialog)
        self.radioEnvConvexe.setGeometry(QtCore.QRect(208, 40, 241, 20))
        self.radioEnvConvexe.setObjectName(_fromUtf8("radioEnvConvexe"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(87, 20, 171, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 201, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.editNbCellTirage = QtGui.QLineEdit(Dialog)
        self.editNbCellTirage.setGeometry(QtCore.QRect(210, 80, 71, 22))
        self.editNbCellTirage.setObjectName(_fromUtf8("editNbCellTirage"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Contrôle - Paramètres de l\'échantillonage", None))
        self.radioEmprise.setText(_translate("Dialog", "Emprise", None))
        self.radioEnvConvexe.setText(_translate("Dialog", "Enveloppe convexe des points saisis", None))
        self.label.setText(_translate("Dialog", "Echantilloner dans:", None))
        self.label_2.setText(_translate("Dialog", "Nombre de cellule à échantilloner:", None))

