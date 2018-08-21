# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'override.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 140)
        Form.setMinimumSize(QtCore.QSize(300, 0))
        Form.setMaximumSize(QtCore.QSize(300, 140))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.hours = QtWidgets.QComboBox(Form)
        self.hours.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.hours.setFont(font)
        self.hours.setObjectName("hours")
        self.horizontalLayout_2.addWidget(self.hours)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(10, 16777215))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.minutes = QtWidgets.QComboBox(Form)
        self.minutes.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.minutes.setFont(font)
        self.minutes.setObjectName("minutes")
        self.horizontalLayout_2.addWidget(self.minutes)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel = QtWidgets.QPushButton(Form)
        self.cancel.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.ok = QtWidgets.QPushButton(Form)
        self.ok.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.ok.setFont(font)
        self.ok.setObjectName("ok")
        self.horizontalLayout.addWidget(self.ok)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Override Time"))
        self.label_2.setText(_translate("Form", "Length of Override:"))
        self.label.setText(_translate("Form", ":"))
        self.cancel.setText(_translate("Form", "Cancel"))
        self.ok.setText(_translate("Form", "Override"))

