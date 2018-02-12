from models.SenseData import SensedData

import webapp2
# standard app engine imports
from google.appengine.ext.webapp import template

from handlers import PositionRequestHandler, GetUpdatesHandler, SetWebhookHandler, WebhookHandler, MeHandler, \
    MainHandler
from handlers.PositionHandler import PositionHandler

TOKEN = '502810340:AAEQKZAkwwhvA0B6Fkk5rTvlY_ERWp1Nd5k'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class UltimoTragittoHandler(webapp2.RequestHandler):
    def get(self):

        sense_data = SensedData()

        # print sense_data

        data = sense_data.query().fetch()

        # print "Data = {}".format(data[0])

        lista_posizione_e_data = []

        maxtemp = []
        for i in xrange(len(data)):

            c = data[i].trip_id
            maxtemp.append(int(c))



        for i in xrange(len(data)):
            print data[i].trip_id
            print "max = "
            print max(maxtemp)

            if (data[i].trip_id == max(maxtemp)):

                print "son dentro"
                temp = []

                a = data[i].latitude
                b = data[i].longitude
                # c = data[i].trip_id
                # d = data[i].updated_at
                # e = data[i].trip_id

                temp.append(float(a))
                temp.append(float(b))
                # temp.append(int(c))
                # temp.append(str(d))
                # temp.append(int(e))

                lista_posizione_e_data.append(temp)

            print lista_posizione_e_data

        # print lista_posizione_e_data

        template_values = {
            'coordinate': lista_posizione_e_data,
            'lat': data[0].latitude,
            'long': data[0].longitude,
            'speed': data[0].speed,
            'date': data[0].updated_at,
            'trip': data[0].trip_id
        }

        self.response.write(template.render("templates/ultimo_tragitto.html", template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/position', PositionHandler),
    ('/ultimotragitto', UltimoTragittoHandler),
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/position/put', PositionHandler),
    ('/position/get', PositionRequestHandler),
], debug=True)
