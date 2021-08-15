from multiprocessing import Event, Process, Pipe
from pickle import dump, load
from light_control import LightControl
from pump_control import PumpControl


class PondC2:
	def __init__(self):
		self.pipe, p2 = Pipe()
		self.exitEvent = Event()
		
		try:
			self.defaults = load(open("defaults.p", 'rb'))
		except FileNotFoundError:
			self.defaults = [0, 21600, 61200, 300, False]  # LED Mode, Pump On Time (0600), Pump Off Time (1700), NumPixels,Mirrored
			dump(self.defaults, open("defaults.p", 'wb'))
		
		self.process = Process(target=self._pond_c2, args=(p2, self.exitEvent, self.defaults,))
		self.process.start()
	
	def get_status(self):
		pass
	
	def get_pump(self):
		self.pipe.send(['pump', 'GET'])
		try:
			self.pipe.poll(5)
			return self.pipe.recv()
		except EOFError:
			return 'Timeout'
	
	def get_override(self):
		self.pipe.send(['override', 'GET'])
		try:
			self.pipe.poll(5)
			return self.pipe.recv()
		except EOFError:
			return ['Timeout']
	
	def set_pump(self, pump):
		if pump == 'on' or pump == 'off':
			self.pipe.send(['pump', pump])
	
	def set_override(self, override, minutes):
		if override == 'on' or override == 'off':
			seconds = minutes * 60
			self.pipe.send(['override', override, seconds])
	
	def get_led(self):
		pass
	
	def set_led(self, value):
		self.pipe.send(['LED', value])
	
	def get_times(self):
		on = self.defaults[1] / 3600
		on = str(on).rjust(2, '0') + ':' + str((self.defaults[1] - (on * 3600)) / 60).ljust(2, '0')
		off = self.defaults[2] / 3600
		off = str(off).rjust(2, '0') + ':' + str((self.defaults[2] - (off * 3600)) / 60).ljust(2, '0')
		return on, off
	
	def set_times(self, on_time='HH:mm', off_time='HH:mm'):
		if on_time != 'HH:mm':
			self.defaults[1] = (int(on_time.split(':')[0]) * 3600) + (int(on_time.split(':')[1]) * 60)
		if off_time != 'HH:mm':
			self.defaults[2] = (int(off_time.split(':')[0]) * 3600) + (int(off_time.split(':')[1]) * 60)
		
		dump(self.defaults, open("defaults.p", 'wb'))
		self.pipe.send(['times', self.defaults[1], self.defaults[2]])
	
	def set_days(self, days=None):
		if days is None:
			days = [0, 1, 2, 3, 4]
		self.pipe.send(['days', days])
	
	def quit(self):
		self.exitEvent.set()
		self.process.join()
	
	@staticmethod
	def _pond_c2(pipe, exit_event, current):
		# Setup LED Data
		led_count = current[3]  # Number of LED pixels.
		led_pin = 18  # GPIO pin connected to the pixels (18 uses PWM!).
		led_freq_hz = 800000  # LED signal frequency in hertz (usually 800khz)
		led_dma = 10  # DMA channel to use for generating signal (try 10)
		led_brightness = 255  # Set to 0 for darkest and 255 for brightest
		led_invert = False  # True to invert the signal (when using NPN transistor level shift)
		led_channel = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
		
		# Create NeoPixel object with appropriate configuration.
		led = LightControl(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel, current[4])
		led.set_mode(current[0])
		pump = PumpControl(23, current[1:])
		
		while not exit_event.is_set():
			
			if pipe.poll():
				data = pipe.recv()
				
				if data[0] == 'times':
					pump.set_times(data[1:])
				
				if data[0] == 'pump':
					if data[1] == 'on':
						pump.set_pump_status(True)
					elif data[1] == 'off':
						pump.set_pump_status(False)
					elif data[1] == 'GET':
						pipe.send(pump.get_pump_status())
				
				if data[0] == 'override':
					if data[1] == 'on':
						pump.set_override(data[2])
					elif data[1] == 'off':
						pump.set_automatic_mode()
					elif data[1] == 'GET':
						pipe.send(pump.get_override_state())
				
				if data[0] == 'LED':
					led.set_mode(data[1])
				
				if data[0] == 'days':
					pump.set_days(data[1])
			
			# Turns pump on or off
			led.update_led(pump.update_pump())
		
		pipe.close()
		led.shutdown()
		pump.shutdown()
		print("Done")


if __name__ == "__main__":
	c = PondC2()
