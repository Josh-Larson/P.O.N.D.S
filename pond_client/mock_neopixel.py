

class Color:
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b


class Adafruit_NeoPixel:
	def __init__(self, led_count, led_pin, led_freq_hz, led_dma, led_invert, led_brightness, led_channel):
		self.led_count = led_count
		self.led_pin = led_pin
		self.led_freq_hz = led_freq_hz
		self.led_dma = led_dma
		self.led_invert = led_invert
		self.led_brightness = led_brightness
		self.led_channel = led_channel
		
		self.led_status = [Color(0, 0, 0) for _ in range(self.led_count)]
	
	def numPixels(self):
		return self.led_count
	
	def setPixelColor(self, idx, color):
		assert 0 <= idx < self.led_count
		self.led_status[idx] = color
	
	def begin(self):
		pass
	
	def show(self):
		pass
