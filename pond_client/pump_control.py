from hardware_control import GPIO
from datetime import datetime as dt


class PumpControl:
	def __init__(self, pin, pump_times):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
		self.pin = pin
		
		self.pump_times = pump_times
		self.pump_status = False
		self.pump_override = False
		self.pump_override_time = -1
		
		self.activeDays = [0, 1, 2, 3, 4]
	
	def set_times(self, times):
		self.pump_times = times
	
	def set_days(self, days):
		self.activeDays = days
	
	def set_override(self, seconds):
		time = dt.now()
		current_time = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
		self.pump_override = True
		if current_time + seconds >= 86340:
			self.pump_override_time = 86340
		else:
			self.pump_override_time = current_time + seconds
	
	def set_automatic_mode(self):
		self.pump_override = False
		self.pump_override_time = -1
	
	def get_override_state(self):
		return [self.pump_override, self.pump_override_time]
	
	def set_pump_status(self, status):
		if type(status) is bool and self.pump_override:
			self.pump_status = status
			GPIO.output(self.pin, GPIO.HIGH if self.pump_status else GPIO.LOW)
	
	def get_pump_status(self):
		return self.pump_status
	
	def update_pump(self):
		time = dt.now()
		current_time = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
		
		if not self.pump_override:
			if self.pump_status:
				if current_time >= self.pump_times[1] or current_time < self.pump_times[0] or dt.weekday(time) not in self.activeDays:
					self.pump_status = False
					GPIO.output(self.pin, GPIO.HIGH if self.pump_status else GPIO.LOW)
			
			else:
				if self.pump_times[0] <= current_time < self.pump_times[1] and dt.weekday(time) in self.activeDays:
					self.pump_status = True
					GPIO.output(self.pin, GPIO.HIGH if self.pump_status else GPIO.LOW)
		
		else:
			if current_time >= self.pump_override_time:
				self.set_automatic_mode()
		
		return self.pump_status
	
	def shutdown(self):
		GPIO.output(self.pin, GPIO.LOW)
		GPIO.cleanup()
