import json

import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import paho.mqtt.client as mqtt
from utils.token import TOKEN

mqtt_bridge_url = 'http://tools.lysis-iot.com'
topic = 'scb'


class SmartCarBoxBot(object):

    def __init__(self, bot_token):
        self.my_topic = topic
        self.bot_token = bot_token
        self.broker = mqtt_bridge_url
        self.port = 1883
        self.client1 = mqtt.Client("scb")  # create client object

    def button(self, bot, update):
        if update.message.text == "Hello!":
            bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm the SCB Bot!"
                                                                  " I know where you left your car :D")
        elif update.message.text == "Posizione":
            bot.send_message(chat_id=update.message.chat_id, text="Position is: here")
            self.get_position()
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Non capisco",
                             parse_mode=telegram.ParseMode.HTML)

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Nice to meet you, {}".format(update.message.from_user.first_name))
        print update.message
        custom_keyboard = [['Hello!'],
                           ['Posizione']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)

        bot.send_message(chat_id=update.message.chat_id,
                         text='Ciao!',
                         reply_markup=reply_markup)

    def run(self):

        self.bot = telegram.Bot(token=self.bot_token)
        self.updater = Updater(token=self.bot_token)

        dispatcher = self.updater.dispatcher
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        start_handler = CommandHandler('start', self.start)
        echo_handler = MessageHandler(Filters.text, self.button)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(echo_handler)

        self.updater.start_polling()

    def get_position(self):
        pass


if __name__ == '__main__':
    scb = SmartCarBoxBot(TOKEN)
    scb.run()
