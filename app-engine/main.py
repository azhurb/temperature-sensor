#!/usr/bin/env python

import webapp2
import json
import logging
import utils
import time 

from google.appengine.ext import db

class Sensor(db.Model):
    temperature = db.FloatProperty(required = True)
    battery     = db.FloatProperty(required = True)
    added       = db.DateTimeProperty(auto_now_add = True)

class SensorRequestHandler(webapp2.RequestHandler):
    def post(self):
        logging.debug("request.body: %s", self.request.body)

        data    = json.loads(self.request.body)
        params  = json.loads(data['value'])
        temp    = params['temp']
        battery = params['battery']
        
        logging.debug("temp: %s", temp)
        logging.debug("battery: %s", battery)

        sensor = Sensor(temperature = temp, battery = battery)
        sensor.put()

        self.response.out.write('OK')

class LastRequestHandler(webapp2.RequestHandler):
    def get(self):
        
        ordered_list = db.GqlQuery('select * from Sensor order by added desc limit 1')
        last = ordered_list.get()
        
        logging.debug("last: %s", last)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(utils.GqlEncoder().encode(last))

app = webapp2.WSGIApplication([
    ('/sensor', SensorRequestHandler),
    ('/sensor/last', LastRequestHandler)
], debug=True)