import urllib

import webapp2
import json

from models.SenseData import SensedData
import datetime as dt
import logging

class PositionHandler(webapp2.RequestHandler):
    def post(self):

        key = self.request.get('apiKey')

        if key == 'smartcarbox-xobractrams':

            is_new
            latitude = self.request.get('latitude')
            longitude = self.request.get('longitutde')
            speed = self.request.get('speed')

            sense_data = SensedData()
            sense_data.latitude = latitude
            sense_data.longitude = longitude
            sense_data.speed = speed

            logging.warning(
                "PositionHandler, latitude: {}, longitude: {}, speed: {}".
                    format(latitude,
                           longitude,
                           speed))

            sense_data.put()
            self.response.status_int = 200
            resp = json.dumps(
                {"Position update status": "ok"})
            self.response.write(resp)
        else:
            logging.warning(
                "PositionHandler, post() method. Not allowed with this key.")
            webapp2.abort(401, detail="Not Authorized")

        #ddd = dt.datetime.strptime(b_dict["date_time"],"%m/%d/%Y %H:%M:%S")

