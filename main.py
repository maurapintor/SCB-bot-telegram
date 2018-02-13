import datetime
import webapp2

from models.SenseData import SensedData

from handlers import PositionRequestHandler, GetUpdatesHandler, SetWebhookHandler, WebhookHandler, MeHandler, \
    MainHandler

from handlers.PositionHandler import PositionHandler

from handlers.MainHandler import TragittoHandler

# ================================



class PutHandler(webapp2.RequestHandler):
    def get(self):
        for i in xrange(10):
            sense_data = SensedData()
            sense_data.latitude = str(39.230129 + (i*0.13))
            sense_data.longitude = str(9.113895 + (i*0.02))
            sense_data.speed = "speed"
            sense_data.updated_at = datetime.datetime.now()
            sense_data.trip_id = -i
            print sense_data
            sense_data.put()



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (r'/trip/(\d+)', TragittoHandler),
    ('/position', PositionHandler),
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/position/put', PositionHandler),
    ('/position/get', PositionRequestHandler),
    ('/put', PutHandler),
], debug=True)


