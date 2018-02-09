import logging
import urllib
import urllib2

from google.appengine.api import urlfetch

from utils.token import get_base_url

BASE_URL = get_base_url()


def sendLocation(chat_id, latitude, longitude):

    # logging.info(str(chat_id.__dict__))
    urlfetch.set_default_fetch_deadline(60)
    resp = urllib2.urlopen(BASE_URL + 'sendLocation', urllib.urlencode({
        'chat_id': str(chat_id),
        'disable_web_page_preview': 'true',
        'latitude': latitude,
        'longitude': longitude,
    })).read()

    logging.info('send update:')
    logging.info(resp)


def sendMsg(chat_id, msg = None):
    urlfetch.set_default_fetch_deadline(60)
    if msg:
        #logging.info(str(chat_id.__dict__))
        logging.info(msg.encode('utf-8'))

        resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
            'chat_id': str(chat_id),
            'text': msg.encode('utf-8'),
            'disable_web_page_preview': 'true',
        })).read()

    else:
        logging.error('no msg or img specified')
        resp = None

    logging.info('send response:')
    logging.info(resp)

def sendToAll():
    pass


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
