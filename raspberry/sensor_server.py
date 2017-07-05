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

temp = 0

class Simple(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        global temp
        pprint.pprint(request)
        temp = float(request.args['value'][0])
        pprint.pprint(temp)
        return "OK"

def main():

    site = server.Site(Simple())
    reactor.listenTCP(8081, site)
    reactor.startRunning(False)

    while True:
        lcd.home()
        sleep(0.05)
        print 'Temp: %1.1fC' % (temp)
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message('Temp: %1.1f\337C ' % (temp) )

        reactor.iterate()
        sleep(2)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
