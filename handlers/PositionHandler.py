import datetime as dt
import json
import logging

import webapp2
from google.appengine.api import memcache

from models.SenseData import SensedData
from utils.Trip import check_trip
from utils.telegramMsg import sendLocation, sendMsg, sendToAll, \
    sendLocationToAll


class PositionHandler(webapp2.RequestHandler):
    def post(self):

        api_key = self.request.get('apiKey')
        user_requested = self.request.get('requested')
        timestamp = self.request.get('data')
        latitude = self.request.get('latitude')
        longitude = self.request.get('longitude')
        speed = self.request.get('speed')
        updated_at = dt.datetime.strptime(timestamp, "%m-%d-%Y_%H:%M:%S")
        logging.warning("PositionHandler, is_requested: {}".format(user_requested))
        logging.warning("PositionHandler, key: {}".format(api_key))
        logging.warning("PositionHandler, timestamp: {}".format(timestamp))

        api_key = 'prova'
        if api_key == 'prova':

            sense_data = SensedData().query().order(-SensedData.trip_id).\
                order(-SensedData.updated_at).fetch()
            print (sense_data)
            is_user = bool(int(user_requested))
            if len(sense_data) is 0:
                trip_id = 0
                self.put_data(latitude, longitude, speed, updated_at, trip_id,
                              user_requested)
            elif not is_user:
                print (sense_data[0].updated_at)
                last_sample = sense_data[0]

                trip_id = sense_data[0].trip_id
                # "%02d-%02d-%02d_%02d:%02d:%02d", month, day, year, hour, minute, second
                is_new_trip = check_trip(last_sample, updated_at)

                if is_new_trip:
                    trip_id += 1
                    sendToAll("Attenzione il tuo veicolo si sta muovendo!")
                    sendLocationToAll(latitude, longitude)

                self.put_data(latitude, longitude, speed, updated_at, trip_id,
                              user_requested)
            elif is_user:
                trip_id = -1
                self.put_data(latitude, longitude, speed, updated_at, trip_id,
                              user_requested)
                try:
                    ch_id = memcache.get('chat_id')
                    memcache.flush_all()
                    sendLocation(ch_id, latitude, longitude)
                    logging.warning("PositionHandler, TRY is_user elif scope")
                except:
                    pass
                logging.warning("PositionHandler, is_user elif scope")

            self.response.status_int = 200
            resp = json.dumps(
                {"Position update status": "ok"})
            self.response.write(resp)

        else:
            logging.warning(
                "PositionHandler, post() method. Not allowed with this key.")
            webapp2.abort(401, detail="Not Authorized")

            # ddd = dt.datetime.strptime(b_dict["date_time"],"%m/%d/%Y %H:%M:%S")

    def put_data(self, latitude, longitude, speed, updated_at, trip_id,
                 is_requested):
        sense_data = SensedData()
        sense_data.latitude = latitude
        sense_data.longitude = longitude
        sense_data.speed = speed
        sense_data.updated_at = updated_at
        sense_data.trip_id = trip_id
        sense_data.user_requested = is_requested
        logging.warning(
            "PositionHandler, latitude: {}, longitude: {}, speed: {}".
                format(latitude,
                       longitude,
                       speed,
                       updated_at))
        sense_data.put()
