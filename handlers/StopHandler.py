import logging

import webapp2

from utils.telegramMsg import sendMsg

chat_id = -195433658


class StopHandler(webapp2.RequestHandler):
    def post(self):
        api_key = self.request.get('apiKey')
        logging.warning("PositionRequestHandler, key: {}".format(api_key))

        api_key = 'prova'
        if api_key == 'prova':
            sendMsg(chat_id, "Pare che il veicolo si sia fermato.")

        else:
            logging.warning(
                "PositionHandler, post() method. Not allowed with this key.")
            webapp2.abort(401, detail="Not Authorized")
