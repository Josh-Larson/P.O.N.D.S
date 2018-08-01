from multiprocessing import Event, Process, Pipe
from datetime import datetime as dt
from pickle import dump, load
import RPi.GPIO as GPIO
from neopixel import *
from time import sleep

class pondC2():

    def __init__(self):
        self.pipe, p2 = Pipe()
        self.exitEvent = Event()

        try:
            self.defaults = load(open("defaults.p",'rb'))
        except:
            self.defaults = ['clock',21600,61200] #LED Mode, Pump On Time (0600), Pump Off Time (1700)
            dump(self.defaults,open("defaults.p",'wb'))

        self.process = Process(target=self._pondC2, args=(p2,self.exitEvent,self.defaults,))
        self.process.start()

    def getStatus(self):
        pass

    def getPump(self):
        self.pipe.send(['pump','GET'])
        try:
            self.pipe.poll(5)
            return self.pipe.recv()
        except:
            return 'Timeout'

    def setPump(self, bool):
        if bool == 'on' or bool == 'off' or bool == 'auto':
            self.pipe.send(['pump',bool])

    def getLED(self):
        pass

    def setLED(self, value, clear=False, pattern=True):
        pass

    def getTimes(self):
        on = self.defaults[1]/3600
        on = str(on).rjust(2,'0') + ':' + str((self.defaults[1]- (on*3600))/60).ljust(2,'0')
        off = self.defaults[2] / 3600
        off = str(off).rjust(2,'0') + ':' + str((self.defaults[2] - (off * 3600)) / 60).ljust(2,'0')
        return (on,off)

    def setTimes(self,onTime='HH:mm', offTime='HH:mm'):
        if onTime != 'HH:mm':
            self.defaults[1] = (int(onTime.split(':')[0])*3600) + (int(onTime.split(':')[1])*60)
        if offTime != 'HH:mm':
            self.defaults[2] = (int(offTime.split(':')[0]) * 3600) + (int(offTime.split(':')[1]) * 60)

        dump(self.defaults, open("defaults.p", 'wb'))
        self.pipe.send(['times',self.defaults[1],self.defaults[2]])


    def quit(self):
        self.exitEvent.set()
        self.process.join()




    def _pondC2(self,pipe,exitEvent,current):
        # Grab Current Data
        ledMode = current[0]
        pumpTimes = current[1:]

        # Setup Other Variables
        pumpStatus = False
        pumpOverride = False

        # Setup LED Data
        LED_COUNT = 300  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Setup GPIO for Pump Control
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23,GPIO.OUT)
        GPIO.output(23,0)

        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        # Test the LEDs in the Strip
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,Color(0,255,0))
            strip.show()
            sleep(10/1000.0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,Color(255,0,0))
            strip.show()
            sleep(10/1000.0)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,Color(0,0,255))
            strip.show()
            sleep(10/1000.0)
        sleep(3)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,Color(0,0,0))
        strip.show()


        while not exitEvent.is_set():
            if pipe.poll():
                data = pipe.recv()

                if data[0] == 'times':
                    pumpTimes = data[1:]

                if data[0] == 'pump':
                    if data[1] == 'on':
                        pumpOverride = True
                        pumpStatus = True
                        GPIO.output(23, 1)
                    elif data[1] == 'off':
                        pumpOverride = True
                        pumpStatus = False
                        GPIO.output(23, 0)
                    elif data[1] == 'auto':
                        pumpOverride = False
                    elif data[1] == 'GET':
                        pipe.send(pumpStatus)


            # Fetches the current time in seconds
            time= dt.now()
            currTime = (time - time.replace(hour=0,minute=0,second=0)).total_seconds()

            # Turns pump on or off
            if pumpStatus and not pumpOverride:
                if currTime >= pumpTimes[1] or currTime < pumpTimes[0]:
                    pumpStatus = False
                    GPIO.output(23,0)
            elif pumpTimes[0] <= currTime < pumpTimes[1] and not pumpOverride:
                pumpStatus = True
                GPIO.output(23,1)



        pipe.close()
        GPIO.output(23, 0)
        GPIO.cleanup()
        print("Done")



if __name__ == "__main__":
    c = pondC2()