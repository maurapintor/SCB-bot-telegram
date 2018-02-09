import datetime

import webapp2

from handlers import PositionRequestHandler, MainHandler, MeHandler, \
    GetUpdatesHandler, WebhookHandler, StopHandler
from handlers.MapHandler import MapHandler
from handlers.PositionHandler import PositionHandler
from handlers.SetWebHookHandler import SetWebhookHandler
from models.SenseData import SensedData

# standard app engine imports
from utils.token import get_base_url

BASE_URL = get_base_url()


# ================================


class PutHandler(webapp2.RequestHandler):
    def get(self):
        for i in xrange(10):
            sense_data = SensedData()
            sense_data.latitude = str(39.230129 + (i * 0.01))
            sense_data.longitude = str(9.113895 + (i * 0.01))
            sense_data.speed = "speed"
            sense_data.updated_at = datetime.datetime.now()
            sense_data.trip_id = i
            print sense_data
            sense_data.put()


class AjaxHandler(webapp2.RequestHandler):
    def post(self):
        pass

        # def dataRequestAjax():
        #     dataReceived = request.get_data()
        #     print dataReceived
        #     return jsonify(get_last_value(dataReceived))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/position', PositionHandler),
    ('/map', MapHandler),
    ('/put', PutHandler),
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/position/put', PositionHandler),
    ('/position/get', PositionRequestHandler),
    ('/dataRequestLastAjax', AjaxHandler),
    ('/position/stop',StopHandler),
], debug=True)
