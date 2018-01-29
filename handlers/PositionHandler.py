import urllib

import webapp2
import json

from models.SenseData import SensedData
import datetime as dt
import logging

from utils.Trip import check_trip


class PositionHandler(webapp2.RequestHandler):
    def post(self):

        key = self.request.get('apiKey')

        if key == 'prova':


            timestamp = self.request.get('timestamp')
            updated_to = dt.datetime.strptime(timestamp,"%m/%d/%Y %H:%M:%S")
            #is_new_trip = check_trip()

            latitude = self.request.get('latitude')
            longitude = self.request.get('longitutde')
            speed = self.request.get('speed')

            sense_data = SensedData()
            sense_data.latitude = latitude
            sense_data.longitude = longitude
            sense_data.speed = speed
            sense_data.updated_to = updated_to

            logging.warning(
                "PositionHandler, latitude: {}, longitude: {}, speed: {}".
                    format(latitude,
                           longitude,
                           speed,
                           updated_to))

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

