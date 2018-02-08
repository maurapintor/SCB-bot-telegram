import json
import logging
import urllib
import urllib2

import datetime

from models.SenseData import SensedData


import webapp2
# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

from handlers import PositionRequestHandler
from handlers.PositionHandler import PositionHandler
from utils.HTTP2MQTT import mqtt_publish

TOKEN = '502810340:AAEQKZAkwwhvA0B6Fkk5rTvlY_ERWp1Nd5k'

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()


def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = "ciao"
        self.response.out.write(
            template.render("templates/home.html", template_values))


class MeHandler(webapp2.RequestHandler):
    def get(self):
        template_values = "ciao"
        self.response.out.write(
            template.render("templates/home.html", template_values))
        urlfetch.set_default_fetch_deadline(60)
        # commento foo
        self.response.write(
            json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(
            json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(
                urllib2.urlopen(BASE_URL + 'setWebhook',
                                urllib.urlencode({'url': url})))))


def reply(chat_id, message_id, msg=None, img=None):
    if msg:
        # logging.info(str(chat_id.__dict__))
        logging.info(msg.encode('utf-8'))
        logging.info(str(message_id))

        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
            'chat_id': str(chat_id),
            'text': msg.encode('utf-8'),
            'disable_web_page_preview': 'true',
            'reply_to_message_id': str(message_id),
        })).read()

    else:
        logging.error('no msg or img specified')
        resp = None

    logging.info('send response:')
    logging.info(resp)


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        first_name = fr['first_name']
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return
        if text.startswith('/'):
            if text == '/mais3cr3tpa55u0rd':
                reply(chat_id, message_id, 'Bot enabled')
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)


            elif getEnabled(chat_id):
                if text.lower() == '/position':

                    # mqtt request
                    # datastore write

                    response = mqtt_publish()

                    result = 200

                    if result == 200:
                        reply(chat_id, message_id,
                              'fatto mqtt')

                    else:
                        reply(chat_id, message_id, 'Qualcosa went wrong!')

                elif text == '/Spegni':
                    pass

                else:
                    reply(chat_id, message_id, 'Non ti capisco, mi dispiace.')
            else:
                reply(chat_id, message_id,
                      'Prima o poi doveva accadere. Chi sei? Non ti conosco, 1 fiorino')



        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply(
                'telebot starter kit, created by yukuku: https://github.com/yukuku/telebot')
        elif 'what time' in text:
            reply(chat_id, message_id, 'look at the corner of your screen!')
        else:
            if getEnabled(chat_id):
                reply(chat_id, message_id,
                      'I got your message! (but I do not know how to answer)')
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


class MapHandler(webapp2.RequestHandler):
    def get(self):

        sense_data = SensedData()

        # print sense_data

        data = sense_data.query().fetch()

        # print "Data = {}".format(data[0])

        lista_posizione_e_data = []

        for i in xrange(len(data)):
            # if str(data[i]['timestamp'][:11]) == str(data[0]['timestamp'][:11]):
                temp = []

                a = data[i].latitude
                b = data[i].longitude
                # c = data[i].speed
                # d = data[i].updated_at
                # e = data[i].trip_id

                temp.append(float(a))
                temp.append(float(b))
                # temp.append(str(c))
                # temp.append(str(d))
                # temp.append(int(e))

                lista_posizione_e_data.append(temp)

               # print lista_posizione_e_data

        template_values = {
            'coordinate': lista_posizione_e_data,
            'lat': data[0].latitude,
            'long': data[0].longitude,
            'speed': data[0].speed,
            'date': data[0].updated_at,
            'trip': data[0].trip_id
        }

        self.response.write(template.render("templates/mappa.html", template_values))



class PutHandler(webapp2.RequestHandler):
    def get(self):
        for i in xrange(10):
            sense_data = SensedData()
            sense_data.latitude = str(39.230129 + (i*0.01))
            sense_data.longitude = str(9.113895 + (i*0.01))
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
], debug=True)
