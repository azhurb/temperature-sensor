#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import logging

from google.appengine.ext import db

class Sensor(db.Model):
    temperature = db.FloatProperty(required = True)
    battery = db.FloatProperty(required = True)
    added = db.DateTimeProperty(auto_now_add = True)

class MainHandler(webapp2.RequestHandler):
    def post(self):
        logging.debug("request.body: %s", self.request.body)
        data = json.loads(self.request.body)
        params = json.loads(data['value'])
        temp = params['temp']
        battery = params['battery']
        logging.debug("temp: %s", temp)
        logging.debug("battery: %s", battery)

        sensor = Sensor(temperature = temp, battery = battery)
        sensor.put()

        self.response.out.write('OK')


app = webapp2.WSGIApplication([
    ('/temp', MainHandler)
], debug=True)
