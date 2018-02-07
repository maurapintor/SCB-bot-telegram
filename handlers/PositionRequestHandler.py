import urllib

import webapp2
import json

from google.appengine.api import urlfetch

from models.SenseData import SensedData
import datetime as dt
import logging

from utils.Trip import check_trip
from utils.telegramMsg import sendLocation, sendMsg


class PositionRequestHandler(webapp2.RequestHandler):
    def post(self):
        api_key = self.request.get('apiKey')
        logging.warning("PositionRequestHandler, key: {}".format(api_key))

        api_key = 'prova'
        if api_key == 'prova':
            form_data = urllib.urlencode(
                {'topic': 'scb', 'message': 'position'})

            response = urlfetch.fetch(
                url='http://34.217.126.242/MqttPublish/publish.php',
                payload=form_data,
                method=urlfetch.POST)

            self.response.write(response)
        else:
            self.response.write('apiKey incorrect')