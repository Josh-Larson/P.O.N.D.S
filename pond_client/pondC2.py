from multiprocessing import Event, Process, Pipe
from datetime import datetime as dt
from pickle import dump, load
from time import sleep
from light_control import LightControl
from pump_control import PumpControl

class pondC2():

    def __init__(self):
        self.pipe, p2 = Pipe()
        self.exitEvent = Event()

        try:
            self.defaults = load(open("defaults.p",'rb'))
        except:
            self.defaults = [0,21600,61200,300,False] #LED Mode, Pump On Time (0600), Pump Off Time (1700), NumPixels,Mirrored
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
            return ['Timeout']

    def setPump(self, bool):
        if bool == 'on' or bool == 'off':
            self.pipe.send(['pump',bool])

    def setOverride(self, bool,minutes):
        if bool == 'on' or bool == 'off':
            seconds = minutes * 60
            self.pipe.send(['override',bool,seconds])

    def getLED(self):
        pass

    def setLED(self, value):
        self.pipe.send(['LED',value])

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

    def setDays(self,days=[0,1,2,3,4]):
        self.pipe.send(['days',days])


    def quit(self):
        self.exitEvent.set()
        self.process.join()




    def _pondC2(self,pipe,exitEvent,current):
        # Setup LED Data
        LED_COUNT = current[3]  # Number of LED pixels.
        LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


        # Create NeoPixel object with appropriate configuration.
        led = LightControl(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, current[4])
        led.setMode(current[0])
        pump = PumpControl(23, current[1:])


        while not exitEvent.is_set():

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
                    led.setMode(data[1])

                if data[0] == 'days':
                    pump.set_days(data[1])


            # Turns pump on or off
            led.updateLed(pump.update_pump())




        pipe.close()
        led.shutdown()
        pump.shutdown()
        print("Done")



if __name__ == "__main__":
    c = pondC2()