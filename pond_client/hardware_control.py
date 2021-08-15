try:
	import RPi.GPIO as GPIO
	mock_gpio = False
except ImportError:
	print("RPi.GPIO not found!  Defaulting to mock GPIO")
	mock_gpio = True
	import mock_gpio as GPIO

try:
	from neopixel import *
	mock_neopixel = False
except ImportError:
	print("Neopixel library not found!  Defaulting to mock neopixel")
	mock_neopixel = True
	from mock_neopixel import *
