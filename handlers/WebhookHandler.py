import json
import logging

import webapp2
from google.appengine.api import urlfetch

from models.Enable import setEnabled, getEnabled
from utils.HTTP2MQTT import mqtt_publish
from utils.telegramMsg import reply


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