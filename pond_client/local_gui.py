from PyQt5.QtWidgets import QApplication, QWidget
import sys
from gui.home import Ui_PONDcontrol
from gui.override import Ui_Form as Ui_Override
from gui.pin import Ui_Pin
from pond_c2 import PondC2
from datetime import time


class LocalGUI:
	def __init__(self):
		self.mainWindow = QWidget()
		self.main = Ui_PONDcontrol()
		self.main.setupUi(self.mainWindow)
		self.mainWindow.show()
		self.mainWindow.showFullScreen()
		self.main.ledMode.addItems(['Clock', 'Rainbow', 'Maluda', 'Off'])
		
		self.overrideWindow = QWidget()
		self.override = Ui_Override()
		self.override.setupUi(self.overrideWindow)
		for i in range(24):
			self.override.hours.addItem(str(i))
		for i in range(60):
			self.override.minutes.addItem(str(i))
		
		self.pinWindow = QWidget()
		self.pin = Ui_Pin()
		self.pin.setupUi(self.pinWindow)
		
		self.pond = PondC2()
		
		self.main.onTime.setTime(time(int(self.pond.defaults[1] / 3600), int(self.pond.defaults[1] % 3600 / 60)))
		self.main.offTime.setTime(time(int(self.pond.defaults[2] / 3600), int(self.pond.defaults[2] % 3600 / 60)))
		
		self.main.override.clicked.connect(self.begin_override)
		self.main.automatic.clicked.connect(self.end_override)
		self.main.setTimes.clicked.connect(self.set_times)
		self.main.sysOn.clicked.connect(self.system_on)
		self.main.sysOff.clicked.connect(self.system_off)
		self.main.ledMode.currentIndexChanged.connect(self.set_led)
		self.main.days.clicked.connect(self.set_days)
		self.main.lock.clicked.connect(self.lock)
		self.main.exit.clicked.connect(self.exit)
		
		self.override.ok.clicked.connect(self.approve_override)
		self.override.cancel.clicked.connect(self.deny_override)
		
		def enter_pin_number(num):
			self.pin.number.insert(num)
		
		self.pin.enter.clicked.connect(self.check_unlock)
		self.pin.back.clicked.connect(self._back)
		self.pin.but1.clicked.connect(lambda: enter_pin_number("1"))
		self.pin.but2.clicked.connect(lambda: enter_pin_number("2"))
		self.pin.but3.clicked.connect(lambda: enter_pin_number("3"))
		self.pin.but4.clicked.connect(lambda: enter_pin_number("4"))
		self.pin.but5.clicked.connect(lambda: enter_pin_number("5"))
		self.pin.but6.clicked.connect(lambda: enter_pin_number("6"))
		self.pin.but7.clicked.connect(lambda: enter_pin_number("7"))
		self.pin.but8.clicked.connect(lambda: enter_pin_number("8"))
		self.pin.but9.clicked.connect(lambda: enter_pin_number("9"))
		self.pin.but0.clicked.connect(lambda: enter_pin_number("0"))
		
		self.lockable_ui_elements = [
			self.main.onTime, self.main.offTime,
			self.main.onDown, self.main.onUp,
			self.main.offDown, self.main.offUp,
			self.main.setTimes,
			self.main.ledMode,
			self.main.override,
			self.main.sysOff, self.main.sysOn,
			self.main.automatic,
			self.main.days,
			self.main.exit
		]
		
		self.password = '2017'
		self.exitCount = 0
	
	def begin_override(self):
		self.overrideWindow.show()
		self.override.hours.setCurrentIndex(0)
		self.override.minutes.setCurrentIndex(0)
		self.exitCount = 0
	
	def approve_override(self):
		self.main.override.setEnabled(False)
		self.main.sysOff.setEnabled(True)
		self.main.sysOn.setEnabled(True)
		self.main.automatic.setEnabled(True)
		self.overrideWindow.hide()
		
		override_time = int(self.override.hours.currentText()) * 3600 + int(self.override.minutes.currentText()) * 60
		self.pond.setOverride('on', override_time)
	
	def deny_override(self):
		self.overrideWindow.hide()
	
	def end_override(self):
		self.main.override.setEnabled(True)
		self.main.sysOff.setEnabled(False)
		self.main.sysOn.setEnabled(False)
		self.main.automatic.setEnabled(False)
		self.exitCount = 0
		
		self.pond.setOverride('off', 0)
	
	def set_times(self):
		on_time = self.main.onTime.time().toString().rsplit(':', 1)[0]
		off_time = self.main.offTime.time().toString().rsplit(':', 1)[0]
		self.pond.setTimes(on_time, off_time)
		self.exitCount = 0
	
	def set_days(self):
		if self.main.days.isChecked():
			self.pond.setDays([0, 1, 2, 3])
		else:
			self.pond.setDays([0, 1, 2, 3, 4])
		self.exitCount = 0
	
	def system_on(self):
		if self.pond.getOverride()[0]:
			self.pond.setPump('on')
		else:
			self.end_override()
		self.exitCount = 0
	
	def system_off(self):
		if self.pond.getOverride()[0]:
			self.pond.setPump('off')
		else:
			self.end_override()
		self.exitCount = 0
	
	def set_led(self):
		self.pond.setLED(self.main.ledMode.currentIndex())
		self.exitCount = 0
	
	def lock(self):
		self.exitCount = 0
		if self.main.lock.isChecked():
			self.main.lock.setText('Unlock')
			for element in self.lockable_ui_elements:
				element.setEnabled(False)
		else:
			self.pin.number.clear()
			self.pinWindow.showFullScreen()
			self.main.lock.setText('Lock')
	
	def check_unlock(self):
		self.exitCount = 0
		if self.pin.number.text() == self.password:
			# Unlock
			for element in self.lockable_ui_elements:
				element.setEnabled(True)
			
			override = self.pond.getOverride()[0]
			self.main.override.setEnabled(not override)
			self.main.sysOff.setEnabled(override)
			self.main.sysOn.setEnabled(override)
			self.main.automatic.setEnabled(override)
		else:
			self.main.lock.setChecked(True)
			self.main.lock.setText('Unlock')
		self.pin.number.clear()
		self.pinWindow.hide()
	
	def exit(self):
		if self.exitCount < 2:
			self.exitCount += 1
		else:
			self.pond.quit()
			self.mainWindow.close()
	
	def _back(self):
		self.pin.number.backspace()


def main():
	app = QApplication(sys.argv)
	_ = LocalGUI()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
