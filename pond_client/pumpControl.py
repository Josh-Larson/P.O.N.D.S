import RPi.GPIO as GPIO
from datetime import datetime as dt

class pumpControl:
    def __init__(self,pin,pumpTimes):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
        self.pin = pin

        self.pumpTimes = pumpTimes
        self.pumpStatus = False
        self.pumpOverride = False
        self.pumpOverrideTime = -1

        self.activeDays = [0,1,2,3,4]

    def setTimes(self,times):
        self.pumpTimes = times

    def setOverride(self,seconds):
        time = dt.now()
        currTime = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
        self.pumpOverride = True
        if currTime + seconds >= 86340:
            self.pumpOverrideTime = 86340
        else:
            self.pumpOverrideTime = currTime + seconds

    def setAuto(self):
        self.pumpOverride = False
        self.pumpOverrideTime = -1

    def setPump(self,status):
        if type(status) is bool and self.pumpOverride:
            self.pumpStatus = status
            GPIO.output(self.pin,self.pumpStatus)

    def updatePump(self):
        time = dt.now()
        currTime = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()

        if not self.pumpOverride:
            if self.pumpStatus:
                if currTime >= self.pumpTimes[1] or currTime < self.pumpTimes[0] or dt.weekday(time) not in self.activeDays:
                    self.pumpStatus = False
                    GPIO.output(self.pin, self.pumpStatus)

            else:
                if self.pumpTimes[0] <= currTime < self.pumpTimes[1] and dt.weekday(time) in self.activeDays:
                    self.pumpStatus = True
                    GPIO.output(self.pin, self.pumpStatus)

        else:
            if currTime >= self.pumpOverrideTime:
                self.setAuto()

        return self.pumpStatus

    def getStatus(self):
        return self.pumpStatus

    def getOverride(self):
        return [self.pumpOverride,self.pumpOverrideTime]

    def shutdown(self):
        GPIO.output(self.pin, 0)
        GPIO.cleanup()