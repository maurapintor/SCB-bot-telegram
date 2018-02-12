import logging
import urllib

import webapp2
from google.appengine.api import urlfetch

url = 'http://tools.lysis-iot.com/MqttPublish/publish.php'
topic = 'scb'


class PositionRequestHandler(webapp2.RequestHandler):
    def post(self):
        api_key = self.request.get('apiKey')
        logging.warning("PositionRequestHandler, key: {}".format(api_key))

        api_key = 'prova'
        if api_key == 'prova':
            form_data = urllib.urlencode(
                {'topic': topic, 'message': 'position'})

            response = urlfetch.fetch(
                url=url,
                payload=form_data,
                method=urlfetch.POST)

            self.response.write(response)
        else:
            self.response.write('apiKey incorrect')
