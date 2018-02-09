import logging
import urllib

import webapp2
from google.appengine.api import urlfetch


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
