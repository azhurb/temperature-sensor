#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
from twisted.web import server, resource
from twisted.internet import reactor
import pprint

#lcd = Adafruit_CharLCD(pins_db=[23, 17, 27, 22])

#lcd.begin(16,1)

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
    global temp

    lcd = Adafruit_CharLCD(pins_db=[23, 17, 27, 22])

    lcd.begin(16,1)

    site = server.Site(Simple())
    reactor.listenTCP(8081, site)
    reactor.startRunning(False)

    while True:

        #lcd.clear()
        #lcd.home()
        #lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        #lcd.message('Temp: %s' % ( temp, '+22.3\337C') )
        #print 'Temp: %1.1fC' % (temp)
        #lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        #lcd.message(datetime.now().strftime('%b %d  %H:%M:%S'))
        #lcd.message('Temp: %1.1fC ' % (temp) )
        #print 'Temp: %1.1fC' % (temp)

        #lcd.clear()
        lcd.home()
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message('IP %s' % ( '172.16.1.117' ) )

        sleep(2)
        reactor.iterate()

if __name__=="__main__":
    main()
