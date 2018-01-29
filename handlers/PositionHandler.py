import urllib

import webapp2
import json

from models.SenseData import SensedData
import datetime as dt
import logging

from utils.Trip import check_trip


class PositionHandler(webapp2.RequestHandler):
    def post(self):

        api_key = self.request.get('apiKey')
        timestamp = self.request.get('data')

        logging.warning("PositionHandler, key: {}".format(api_key))
        logging.warning("PositionHandler, timestamp: {}".format(timestamp))

        api_key = 'prova'
        if api_key == 'prova':


            # "%02d-%02d-%02d_%02d:%02d:%02d", month, day, year, hour, minute, second

            updated_at = dt.datetime.strptime(timestamp,"%m-%d-%Y_%H:%M:%S")
            is_new_trip = check_trip(updated_at)

            latitude = self.request.get('latitude')
            longitude = self.request.get('longitutde')
            speed = self.request.get('speed')

            sense_data = SensedData()
            sense_data.latitude = latitude
            sense_data.longitude = longitude
            sense_data.speed = speed
            sense_data.updated_at = updated_at

            logging.warning(
                "PositionHandler, latitude: {}, longitude: {}, speed: {}".
                    format(latitude,
                           longitude,
                           speed,
                           updated_at))

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

