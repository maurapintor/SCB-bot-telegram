import webapp2
import json

from models.SenseData import SensedData
import datetime as dt

class PositionHandler(webapp2.RequestHandler):
    def post(self):
        b_dict = json.loads(self.request.body)
        sense_data = SensedData()
        sense_data.latitude = b_dict["latitude"]
        sense_data.longitude = b_dict["longitude"]
        ddd = dt.datetime.strptime(b_dict["date_time"],"%m/%d/%Y %H:%M:%S")
        sense_data.timestamp = ddd
        sense_data.speed = b_dict["speed"]
        sense_data.put()
        self.response.status_int = 200
        resp = json.dumps(
            {"Position update status": "ok"})
        self.response.write(resp)