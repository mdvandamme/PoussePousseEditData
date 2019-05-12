# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'valider_dialog_base.ui'
#
# Created: Mon May 13 00:07:28 2019
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
        Dialog.resize(400, 235)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.radioEmprise = QtGui.QRadioButton(Dialog)
        self.radioEmprise.setGeometry(QtCore.QRect(90, 50, 95, 20))
        self.radioEmprise.setChecked(True)
        self.radioEmprise.setObjectName(_fromUtf8("radioEmprise"))
        self.radioEnvConvexe = QtGui.QRadioButton(Dialog)
        self.radioEnvConvexe.setGeometry(QtCore.QRect(90, 80, 181, 20))
        self.radioEnvConvexe.setObjectName(_fromUtf8("radioEnvConvexe"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 171, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 132, 191, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.editNbCellTirage = QtGui.QLineEdit(Dialog)
        self.editNbCellTirage.setGeometry(QtCore.QRect(200, 130, 113, 22))
        self.editNbCellTirage.setObjectName(_fromUtf8("editNbCellTirage"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.radioEmprise.setText(_translate("Dialog", "Emprise", None))
        self.radioEnvConvexe.setText(_translate("Dialog", "Enveloppe convexe", None))
        self.label.setText(_translate("Dialog", "Echantilloner dans:", None))
        self.label_2.setText(_translate("Dialog", "Nb de cellule à échantilloner:", None))

