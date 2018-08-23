from neopixel import *
from time import sleep
from datetime import datetime as dt

class ledControl:
    def __init__(self, LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,mirrored):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.ledMode = 0
        self.iterator = 0
        self.linked = True
        self.linkTime = -1
        self.mirrored = mirrored
        
    def testLed(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i,Color(0,255,0))
            self.strip.show()
            sleep(10/1000.0)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i,Color(255,0,0))
            self.strip.show()
            sleep(10/1000.0)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i,Color(0,0,255))
            self.strip.show()
            sleep(10/1000.0)
        sleep(3)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i,Color(0,0,0))
        self.strip.show()

    def setMode(self, mode):
        """
        Modes:
        2- Off
        0- Clock
        1- Rainbow
        """
        self.ledMode = mode if 0 <= mode <= 3 else self.ledMode

    def setUnlink(self,seconds):
        time = dt.now()
        currTime = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
        self.linked = False
        if currTime + seconds >= 86340:
            self.linkTime = 86340
        else:
            self.linkTime = currTime + seconds

    def setLink(self):
        self.linked = True
        self.linkTime = -1

    def updateLed(self,status):
        if self.linked and not status:
            run = False
        else:
            run = True

        if run:
            if self.ledMode == 0:
                self.drawLED(self._ledClock(5, 5, 5, Color(0, 255, 0), Color(255, 0, 0), Color(0, 0, 255),True),self.mirrored)
            elif self.ledMode == 1:
                self.drawLED(self._rainbowCycle(20,self.iterator),self.mirrored)
                self.iterator = self.iterator + 1 if self.iterator < 255 else 0
            else:
                self.clearLed()
        else:
            self.clearLed()

        if not self.linked:
            time = dt.now()
            currTime = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()
            if currTime >= self.linkTime:
                self.setLink()


    def clearLed(self):
        self.shutdown()


    def shutdown(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i,Color(0,0,0))
        self.strip.show()


    def drawLED(self,leds,mirror=False,delay=0):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i,Color(0,0,0))
            
        if not mirror:
            for i in leds.keys():
                self.strip.setPixelColor(i, leds[i])
            self.strip.show()
            sleep(delay/1000)

        else:
            for i in leds.keys():
                self.strip.setPixelColor(self.strip.numPixels()-i-1,leds[i])
            self.strip.show()
            sleep(delay/1000)




    def _interp(self,value, valMax, scaledMax):
        scaled = float(value) / float(valMax)
        return int(scaled * scaledMax)


    def _wrap(self,val,valMax):
        if type(val) is int:
            val = [val]
        new = []
        for i in val:
            if 0 <= i <= valMax:
                new.append(i)
            elif i < 0:
                new.append(valMax + (i+1))
            else:
                new.append(i-valMax-1)
        if len(new) == 1:
            return new[0]
        else:
            return new


    def _wrapCount(self,val,target,valMax,direction=1):
        if direction == 1:
            if target > val:
                return target - val
            else:
                return (valMax - val) + target
        elif direction == 0:
            if target < val:
                return val - target
            else:
                return (valMax - target) + val


    def _ledClock(self,hourSize,minSize,secSize,hourColor,minColor,secColor,seconds=False):
        time = dt.now()
        currTime = (time - time.replace(hour=0, minute=0, second=0)).total_seconds()

        second = currTime % 60
        minute = currTime / 60 % 60
        hour = currTime / 60 / 60
        if hour > 11: hour = hour - 12

        secPos = self._interp(second,60,self.strip.numPixels()-1)
        minPos = self._interp(minute, 60, self.strip.numPixels()-1)
        hourPos = self._interp(hour, 12, self.strip.numPixels()-1)

        secList = [secPos]
        minList = [minPos]
        hourList = [hourPos]

        for i in range(int((secSize-1)/2)):
            secList.append(secPos + (i+1))
            secList.insert(0, secPos - (i+1))
        for i in range(int((minSize-1)/2)):
            minList.append(minPos + (i+1))
            minList.insert(0, minPos - (i+1))
        for i in range(int((hourSize-1)/2)):
            hourList.append(hourPos + (i+1))
            hourList.insert(0, hourPos - (i+1))

        secList = self._wrap(secList,self.strip.numPixels()-1)
        minList = self._wrap(minList, self.strip.numPixels()-1)
        hourList = self._wrap(hourList,self.strip.numPixels()-1)

        leds = {}

        if seconds:
            for i in secList:
                leds[i] = secColor
        for i in minList:
            leds[i] = minColor
        for i in hourList:
            leds[i] = hourColor

        return leds


    def _wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)


    def _rainbowCycle(self, iterator=0):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        leds = {}
        for i in range(self.strip.numPixels()):
            leds[i] = self._wheel((int(i * 256 / self.strip.numPixels()) + iterator) & 255)
        return leds


    def _ledSpin(self, strip, color, loops):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i,Color(0,0,0))
        strip.show()
        head = 0
        tail = strip.numPixels() - 1
        grow = strip.numPixels() / loops
        currSize = 1
        for i in range(loops):
            for j in range(strip.numPixels()):
                strip.setPixelColor(head, color)
                if currSize == grow * i:
                    strip.setPixelColor(tail,Color(0,0,0))
                else:
                    currSize += 1
                strip.show()