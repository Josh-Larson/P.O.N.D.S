from multiprocessing import Event, Process, Pipe
from datetime import datetime as dt
from pickle import dump, load
from time import sleep
from ledControl import ledControl
from pumpControl import pumpControl

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

    def getOverride(self):
        self.pipe.send(['override','GET'])
        try:
            self.pipe.poll(5)
            return self.pipe.recv()
        except:
            return 'Timeout'

    def setPump(self, bool):
        if bool == 'on' or bool == 'off':
            self.pipe.send(['pump',bool])

    def setOverride(self, bool,minutes):
        if bool == 'on' or bool == 'off':
            seconds = minutes * 60
            self.pipe.send(['override',bool,seconds])

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
        # Setup LED Data
        LED_COUNT = 300  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


        # Create NeoPixel object with appropriate configuration.
        led = ledControl(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        led.setMode(current[0])
        pump = pumpControl(23,current[1:])


        while not exitEvent.is_set():

            if pipe.poll():
                data = pipe.recv()

                if data[0] == 'times':
                    pump.setTimes(data[1:])

                if data[0] == 'pump':
                    if data[1] == 'on':
                        pump.setPump(True)
                    elif data[1] == 'off':
                        pump.setPump(False)
                    elif data[1] == 'GET':
                        pipe.send(pump.getStatus())

                if data[0] == 'override':
                    if data[1] == 'on':
                        pump.setOverride(data[2])
                    elif data[1] == 'off':
                        pump.setAuto()
                    elif data[1] == 'GET':
                        pipe.send(pump.getOverride())


            # Turns pump on or off
            led.updateLed(pump.updatePump())




        pipe.close()
        led.shutdown()
        pump.shutdown()
        print("Done")



if __name__ == "__main__":
    c = pondC2()