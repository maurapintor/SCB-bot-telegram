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

        sense_data = SensedData()

        # print sense_data

        data = sense_data.query().fetch()

        # print "Data = {}".format(data[0])

        lista_posizione_e_data = []
        trip_total = []

        for i in xrange(len(data)):
            # if str(data[i]['timestamp'][:11]) == str(data[0]['timestamp'][:11]):
                temp = []

                a = data[i].latitude
                b = data[i].longitude
                c = data[i].trip_id
                # d = data[i].updated_at
                # e = data[i].trip_id

                temp.append(float(a))
                temp.append(float(b))
                temp.append(int(c))
                # temp.append(str(d))
                # temp.append(int(e))

                lista_posizione_e_data.append(temp)
                trip_total.append(int(c))

               # print lista_posizione_e_data

        template_values = {
            'coordinate': lista_posizione_e_data,
            'trip_all': trip_total,
            'last_trip': max(trip_total),
            'lat': data[0].latitude,
            'long': data[0].longitude,
            'speed': data[0].speed,
            'date': data[0].updated_at,
            'trip': data[0].trip_id
        }

        self.response.write(template.render("templates/home.html", template_values))


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
        trip_total = []

        for i in xrange(len(data)):
            # if str(data[i]['timestamp'][:11]) == str(data[0]['timestamp'][:11]):
                temp = []

                a = data[i].latitude
                b = data[i].longitude
                c = data[i].trip_id
                # d = data[i].updated_at
                # e = data[i].trip_id

                temp.append(float(a))
                temp.append(float(b))
                temp.append(int(c))
                # temp.append(str(d))
                # temp.append(int(e))

                lista_posizione_e_data.append(temp)
                trip_total.append(int(c))

               # print lista_posizione_e_data

        template_values = {
            'coordinate': lista_posizione_e_data,
            'trip_all': trip_total,
            'last_trip': max(trip_total),
            'lat': data[0].latitude,
            'long': data[0].longitude,
            'speed': data[0].speed,
            'date': data[0].updated_at,
            'trip': data[0].trip_id
        }

        self.response.write(template.render("templates/mappa.html", template_values))


class DirectionHandler(webapp2.RequestHandler):
    def get(self):

        sense_data = SensedData()

        # print sense_data

        data = sense_data.query().fetch()

        start = "{},%20{}".format(data[0].latitude, data[0].longitude)
        finish = "{},%20{}".format(data[-1].latitude, data[-1].longitude)

        print start, finish

        urlBase = "https://maps.googleapis.com/maps/api/directions/json"
        origin = start
        destination = finish
        sensor = "false"
        key = "AIzaSyBkrnpgt5jQGEfSi6miJ388nh53jf_lH_E"

        url = urlBase + "?origin=" + origin + "&destination=" + destination + "&sensor=" + sensor + "&key=" + key

        headers = {
            'cache-control': "no-cache",
            'postman-token': "248c881d-a192-e7ba-1dd4-2fadc5d52852",
            'content-type': "application/x-www-form-urlencoded"
            }

        try:
            result = urlfetch.fetch(
                url=url,
                method=urlfetch.POST,
                headers=headers)

            # print values.content
            if result.status_code == 200:
                response = json.loads(result.content)
                # print response['routes'][0]['legs'][0]['steps']
                # print type(response['routes'][0]['legs'][0]['steps'][0])

                print response['routes'][0]['legs'][0]['steps'][0].keys()


                data = []
                lista_posizione_e_data = []
                trip_total = []

                for i in xrange(len(response['routes'][0]['legs'][0]['steps'])):
                    latitude = response['routes'][0]['legs'][0]['steps'][i]['start_location']['lat']
                    longitude = response['routes'][0]['legs'][0]['steps'][i]['start_location']['lng']
                    print "Lat = {}, Lon = {}".format(latitude, longitude)

                    temp = []

                    a = latitude
                    b = longitude
                    # c = data[i].trip_id

                    temp.append(float(a))
                    temp.append(float(b))
                    # temp.append(int(c))

                    lista_posizione_e_data.append(temp)
                    # trip_total.append(int(c))

                    # print lista_posizione_e_data

                template_values = {
                    'coordinate': lista_posizione_e_data,
                    # 'trip_all': trip_total,
                    # 'last_trip': max(trip_total),
                    # 'lat': data[0].latitude,
                    # 'long': data[0].longitude,
                    # 'speed': data[0].speed,
                    # 'date': data[0].updated_at,
                    # 'trip': data[0].trip_id
                }

                self.response.write(template.render("templates/home.html", template_values))

                # pass

            else:
                print ("Errore")



        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        pass


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
    ('/direction', DirectionHandler),
    ('/put', PutHandler),
    ('/ultimotragitto', UltimoTragittoHandler),
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
    ('/position/put', PositionHandler),
    ('/position/get', PositionRequestHandler),
    ('/dataRequestLastAjax', AjaxHandler),
    ('/position/stop',StopHandler),
], debug=True)
