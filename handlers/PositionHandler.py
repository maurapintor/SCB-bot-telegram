import urllib

import webapp2
import json

from models.SenseData import SensedData
import datetime as dt
import logging

from utils.Trip import check_trip
from utils.telegramMsg import sendLocation, sendMsg

chat_id = -195433658

class PositionHandler(webapp2.RequestHandler):
    def post(self):

        api_key = self.request.get('apiKey')
        #user_requested = self.request.get('requested')
        timestamp = self.request.get('data')
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')
        speed = self.request.get('speed')
        updated_at = dt.datetime.strptime(timestamp, "%m-%d-%Y_%H:%M:%S")

        logging.warning("PositionHandler, key: {}".format(api_key))
        logging.warning("PositionHandler, timestamp: {}".format(timestamp))

        api_key = 'prova'
        if api_key == 'prova':

            sense_data = SensedData().query().order(
                -SensedData.updated_at).fetch()

            if len(sense_data) is 0:
                trip_id = 0
                self.put_data(latitude, longitude, speed, updated_at,trip_id)
            else:
                print (sense_data[0].updated_at)
                last_sample = sense_data[0]
                trip_id = sense_data[0].trip_id
                #"%02d-%02d-%02d_%02d:%02d:%02d", month, day, year, hour, minute, second
                is_new_trip = check_trip(last_sample, updated_at)

                if is_new_trip:
                    trip_id += 1
                    sendMsg(chat_id,"Attenzione il tuo veicolo si sta muovendo!")
                    sendLocation(chat_id,latitude,longitude)

                self.put_data(latitude, longitude, speed, updated_at,trip_id)

            self.response.status_int = 200
            resp = json.dumps(
                {"Position update status": "ok"})
            self.response.write(resp)

        else:
            logging.warning(
                "PositionHandler, post() method. Not allowed with this key.")
            webapp2.abort(401, detail="Not Authorized")

        #ddd = dt.datetime.strptime(b_dict["date_time"],"%m/%d/%Y %H:%M:%S")

    def put_data(self, latitude, longitude, speed, updated_at,trip_id):
        sense_data = SensedData()
        sense_data.latitude = latitude
        sense_data.longitude = longitude
        sense_data.speed = speed
        sense_data.updated_at = updated_at
        sense_data.trip_id = trip_id
        logging.warning(
            "PositionHandler, latitude: {}, longitude: {}, speed: {}".
                format(latitude,
                       longitude,
                       speed,
                       updated_at))
        sense_data.put()

