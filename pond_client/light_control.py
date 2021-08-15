from hardware_control import *
from time import sleep
from datetime import datetime as dt


class LightControl:
	def __init__(self, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel, mirrored):
		self.strip = Adafruit_NeoPixel(led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel)
		self.strip.begin()
		self.ledMode = 0
		self.iterator = 0
		self.linked = True
		self.linkTime = -1
		self.mirrored = mirrored
	
	def test_led(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(0, 255, 0))
			self.strip.show()
			sleep(10 / 1000.0)
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(255, 0, 0))
			self.strip.show()
			sleep(10 / 1000.0)
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(0, 0, 255))
			self.strip.show()
			sleep(10 / 1000.0)
		sleep(3)
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(0, 0, 0))
		self.strip.show()
	
	def set_mode(self, mode):
		"""
		Modes:
		3- Off
		0- Clock
		1- Rainbow
		2- Maluda
		"""
		self.ledMode = mode if 0 <= mode <= 3 else self.ledMode
	
	def set_unlink(self, seconds):
		time = dt.now()
		current_time = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
		self.linked = False
		if current_time + seconds >= 86340:
			self.linkTime = 86340
		else:
			self.linkTime = current_time + seconds
	
	def set_link(self):
		self.linked = True
		self.linkTime = -1
	
	def update_led(self, status):
		if self.linked and not status:
			run = False
		else:
			run = True
		
		if run:
			if self.ledMode == 0:
				self.draw_led(self._led_clock(5, 5, 5, Color(0, 255, 0), Color(255, 0, 0), Color(0, 0, 255), True), self.mirrored)
			elif self.ledMode == 1:
				self.draw_led(self._rainbow_cycle(self.iterator), self.mirrored)
				self.iterator = self.iterator + 1 if self.iterator < 255 else 0
			elif self.ledMode == 2:
				self.draw_led(self._maluda_light(self.iterator), self.mirrored)
				self.iterator = self.iterator + 1 if self.iterator < self.strip.numPixels() * 2 else 0
			else:
				self.clear_led()
		else:
			self.clear_led()
		
		if not self.linked:
			time = dt.now()
			current_time = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
			if current_time >= self.linkTime:
				self.set_link()
	
	def clear_led(self):
		self.shutdown()
	
	def shutdown(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(0, 0, 0))
		self.strip.show()
	
	def draw_led(self, leds, mirror=False, delay=0):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(0, 0, 0))
		
		if not mirror:
			for i in leds.keys():
				self.strip.setPixelColor(i, leds[i])
			self.strip.show()
			sleep(delay / 1000)
		
		else:
			for i in leds.keys():
				self.strip.setPixelColor(self.strip.numPixels() - i - 1, leds[i])
			self.strip.show()
			sleep(delay / 1000)
	
	@staticmethod
	def _interp(value, value_max, value_scale):
		scaled = float(value) / float(value_max)
		return int(scaled * value_scale)

	@staticmethod
	def _wrap(val, value_max):
		if type(val) is int:
			val = [val]
		new = []
		for i in val:
			if 0 <= i <= value_max:
				new.append(i)
			elif i < 0:
				new.append(value_max + (i + 1))
			else:
				new.append(i - value_max - 1)
		if len(new) == 1:
			return new[0]
		else:
			return new

	@staticmethod
	def _wrap_count(val, target, value_max, direction=1):
		if direction == 1:
			if target > val:
				return target - val
			else:
				return (value_max - val) + target
		elif direction == 0:
			if target < val:
				return val - target
			else:
				return (value_max - target) + val

	def _led_clock(self, hour_size, min_size, sec_size, hour_color, min_color, sec_color, seconds=False):
		time = dt.now()
		current_time = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
		
		second = current_time % 60
		minute = current_time / 60 % 60
		hour = (current_time / 60 / 60) % 12  # 12-hour time
		
		sec_pos = self._interp(second, 60, self.strip.numPixels() - 1)
		min_pos = self._interp(minute, 60, self.strip.numPixels() - 1)
		hour_pos = self._interp(hour, 12, self.strip.numPixels() - 1)
		
		sec_list = [sec_pos]
		min_list = [min_pos]
		hour_list = [hour_pos]
		
		for i in range(int((sec_size - 1) / 2)):
			sec_list.append(sec_pos + (i + 1))
			sec_list.insert(0, sec_pos - (i + 1))
		for i in range(int((min_size - 1) / 2)):
			min_list.append(min_pos + (i + 1))
			min_list.insert(0, min_pos - (i + 1))
		for i in range(int((hour_size - 1) / 2)):
			hour_list.append(hour_pos + (i + 1))
			hour_list.insert(0, hour_pos - (i + 1))
		
		sec_list = self._wrap(sec_list, self.strip.numPixels() - 1)
		min_list = self._wrap(min_list, self.strip.numPixels() - 1)
		hour_list = self._wrap(hour_list, self.strip.numPixels() - 1)
		
		leds = {}
		
		if seconds:
			for i in sec_list:
				leds[i] = sec_color
		for i in min_list:
			leds[i] = min_color
		for i in hour_list:
			leds[i] = hour_color
		
		return leds

	@staticmethod
	def _wheel(pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos * 3, 255 - pos * 3, 0)
		elif pos < 170:
			pos -= 85
			return Color(255 - pos * 3, 0, pos * 3)
		else:
			pos -= 170
			return Color(0, pos * 3, 255 - pos * 3)

	def _rainbow_cycle(self, iterator=0):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		leds = {}
		for i in range(self.strip.numPixels()):
			leds[i] = self._wheel((int(i * 256 / self.strip.numPixels()) + iterator) & 255)
		return leds

	def _maluda_light(self, iterator=0):
		leds = {}
		if iterator <= self.strip.numPixels():
			for i in range(iterator):
				leds[i] = Color(239, 255, 1)
			return leds
		else:
			iterator = iterator - self.strip.numPixels()
			for i in range(self.strip.numPixels()):
				if iterator != 0:
					leds[i] = Color(0, 0, 0)
					iterator -= 1
				else:
					leds[i] = Color(239, 255, 1)
			return leds
