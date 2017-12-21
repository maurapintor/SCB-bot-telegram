import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import paho.mqtt.client as mqtt

class SmartCarBoxBot(object):

    my_topic = "scb/control"
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.broker = "broker.hivemq.com"
        self.port = 1883
        self.client1 = mqtt.Client("control-scb")  # create client object

    def button(self, bot, update):
        if update.message.text == "Avvio Tracking":
            bot.send_message(chat_id=update.message.chat_id, text="Tracking is Active")
            self.start_tracking()
        elif update.message.text == "Stop Tracking":
            bot.send_message(chat_id=update.message.chat_id, text="Tracking Stopped")
            self.stop_tracking()
        elif update.message.text == "Posizione":
            bot.send_message(chat_id=update.message.chat_id, text="Position is: here")
            self.ask_position()
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Non capisco",
                             parse_mode=telegram.ParseMode.HTML)

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
        custom_keyboard = [['Avvio Tracking', 'Stop Tracking'],
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

    def start_tracking(self):
        self.publish("start")

    def stop_tracking(self):
        self.publish("stop")

    def ask_position(self):
        self.publish("position")

    def publish(self, message):
        self.client1.connect(self.broker, self.port)  # establish connection
        self.client1.publish(my_topic, message)  # publish

if __name__ == '__main__':
    bot_token = '502810340:AAEQKZAkwwhvA0B6Fkk5rTvlY_ERWp1Nd5k'
    scb = SmartCarBoxBot(bot_token)
    scb.run()


