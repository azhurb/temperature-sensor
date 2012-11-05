#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
from twisted.web import server, resource
from twisted.internet import reactor
import pprint

lcd = Adafruit_CharLCD(pins_db=[23, 17, 27, 22])

lcd.begin(16,1)

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        pprint.pprint(request)
        return "<html>%s Iterations!</html>"%n

def main():
    global n
    site = server.Site(Simple())
    reactor.listenTCP(8081, site)
    reactor.startRunning(False)
    n=0
    while True:
        #n+=1
        #if n%1000==0:
        #    print n

        #lcd.clear()
        lcd.home()
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message('Temp: %s' % ( '+22.3\337C') )

        sleep(0.001)
        reactor.iterate()

if __name__=="__main__":
    main()
