# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gunseol_list_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QTableWidgetItem
class Ui_Form(object):

    def __init__(self, businessname, personname):
        self.businessname = businessname
        self.personname = personname

    def setupUi(self, Form):
        Form.setObjectName("건설경기동향조사 수집대상처 명부")
        Form.resize(488, 397)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(110, 30, 281, 291))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(self.businessname))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(210, 340, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Form.close)
        
        self.tableWidget.setHorizontalHeaderLabels(['기업체명', '담당자'])
        for row in range(len(self.businessname)):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(self.businessname[row]))
        for row in range(len(self.personname)):
            self.tableWidget.setItem(row, 1, QTableWidgetItem(self.personname[row]))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "닫기"))

   

if __name__ == "__main__":
    businessname = ['포스코건설', '삼성물산']
    personname = ['김웅곤', '김필상']
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form(businessname, personname)
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

