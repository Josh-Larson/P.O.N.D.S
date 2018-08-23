from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem, QMessageBox, QMainWindow, QLCDNumber
import sys
from home import Ui_PONDcontrol
from override import Ui_Form as Ui_Override
from pondC2 import pondC2
from datetime import time


class localGUI():

    def __init__(self):
        self.mainWindow = QWidget()
        self.main = Ui_PONDcontrol()
        self.main.setupUi(self.mainWindow)
        self.mainWindow.show()
        self.mainWindow.showMaximized()
        self.main.ledMode.addItems(['Clock','Rainbow','Off'])
        
        self.overrideWindow = QWidget()
        self.override = Ui_Override()
        self.override.setupUi(self.overrideWindow)
        for i in range(24):
            self.override.hours.addItem(str(i))
        for i in range(60):
            self.override.minutes.addItem(str(i))

        self.pond = pondC2()

        self.main.onTime.setTime(time(int(self.pond.defaults[1]/3600),int(self.pond.defaults[1]%3600/60)))
        self.main.offTime.setTime(time(int(self.pond.defaults[2]/3600),int(self.pond.defaults[2]%3600/60)))



        self.main.override.clicked.connect(self.beginOverride)
        self.main.automatic.clicked.connect(self.endOverride)
        self.main.setTimes.clicked.connect(self.setTimes)
        self.main.sysOn.clicked.connect(self.sysOn)
        self.main.sysOff.clicked.connect(self.sysOff)
        self.main.ledMode.currentIndexChanged.connect(self.setLED)

        self.mainWindow.closeEvent = self.closeEvent

        self.override.ok.clicked.connect(self.approveOverride)
        self.override.cancel.clicked.connect(self.denyOverride)


    def beginOverride(self):
        self.overrideWindow.show()

    def approveOverride(self):
        self.main.override.setEnabled(False)
        self.main.sysOff.setEnabled(True)
        self.main.sysOn.setEnabled(True)
        self.main.automatic.setEnabled(True)
        self.overrideWindow.hide()

        time = int(self.override.hours.currentText()) * 3600 + int(self.override.minutes.currentText()) * 60
        self.pond.setOverride('on', time)

    def denyOverride(self):
        self.overrideWindow.hide()

    def endOverride(self):
        self.main.override.setEnabled(True)
        self.main.sysOff.setEnabled(False)
        self.main.sysOn.setEnabled(False)
        self.main.automatic.setEnabled(False)

        self.pond.setOverride('off',0)

    def setTimes(self):
        onTime = self.main.onTime.time().toString().rsplit(':',1)[0]
        offTime = self.main.offTime.time().toString().rsplit(':',1)[0]
        self.pond.setTimes(onTime,offTime)

    def sysOn(self):
        if self.pond.getOverride()[0]:
            self.pond.setPump('on')
        else:
            self.endOverride()

    def sysOff(self):
        if self.pond.getOverride()[0]:
            self.pond.setPump('off')
        else:
            self.endOverride()

    def setLED(self):
        self.pond.setLED(self.main.ledMode.currentIndex())

    def closeEvent(self,event):
        msg = "Are you sure you want to shutdown pond management?"
        reply = QMessageBox.question(self.mainWindow,"Question",msg,QMessageBox.Yes,QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.pond.quit()
            event.accept()
        else:
            event.ignore()









def main():
    app = QApplication(sys.argv)
    gui = localGUI()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
