#!/usr/bin/env python

import webapp2
import json
import logging
import utils
import time
import os
import datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import db

class Sensor(db.Model):
    temperature = db.FloatProperty(required = True)
    battery     = db.FloatProperty(required = True)
    added       = db.DateTimeProperty(auto_now_add = True, indexed=True)

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

    def get(self):

        #sensors_data = Sensor.all().filter('added >', datetime.date.today() - datetime.timedelta(days=7)).order('added').fetch(None)
        sensors_data = Sensor.all().order('added').fetch(None)

        temperature_data = []
        battery_data     = []

        #start_date = int(time.mktime(sensors_data[0].added.timetuple()))*1000

        for item in sensors_data:
            temperature_data.append([int(time.mktime(item.added.timetuple()))*1000 ,round(item.temperature, 1)])
            battery_data.append([int(time.mktime(item.added.timetuple()))*1000, round(item.battery, 2)])
        
        path = os.path.join(os.path.dirname(__file__), 'templates/charts.html')
        self.response.out.write(template.render(path, {
            'temperature_data' : utils.GqlEncoder().encode(temperature_data), 
            'battery_data' : utils.GqlEncoder().encode(battery_data)
            }))

class LastRequestHandler(webapp2.RequestHandler):
    def get(self):
        
        ordered_list = db.GqlQuery('select * from Sensor order by added desc limit 1')
        last = ordered_list.get()
        
        logging.debug("last: %s", last)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(utils.GqlEncoder().encode(last))

class CleanRequestHandler(webapp2.RequestHandler):
    def get(self, bulk = 'old'):
        logging.debug("bulk: %s", bulk)
        try:
            while True:
                q = Sensor.all()

                if bulk != 'all':
                    q.filter('added <', datetime.date.today() - datetime.timedelta(days=14))
                
                assert q.count()
                db.delete(q.fetch(200))
                time.sleep(0.5)
        except Exception, e:
            self.response.out.write(repr(e)+'\n')
            pass


app = webapp2.WSGIApplication([
    ('/sensor', SensorRequestHandler),
    ('/sensor/last', LastRequestHandler),
    ('/sensor/clean/?(all)?', CleanRequestHandler)
], debug=True)
