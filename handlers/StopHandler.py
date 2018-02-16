import logging

import webapp2

from utils.telegramMsg import sendToAll, sendLocationToAll


class StopHandler(webapp2.RequestHandler):
    def post(self):
        api_key = self.request.get('apiKey')
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')

        logging.warning("StopHandler, key: {}".format(api_key))
        logging.warning("StopHandler, lat {} | lon {}".format(latitude, longitude))

        api_key = 'prova'
        if api_key == 'prova':
            sendToAll("Pare che il veicolo si sia fermato.")
            sendLocationToAll(latitude, longitude)

        else:
            logging.warning(
                "PositionHandler, post() method. Not allowed with this key.")
            webapp2.abort(401, detail="Not Authorized")
