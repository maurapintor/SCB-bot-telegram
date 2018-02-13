import urllib

from google.appengine.api import urlfetch

mqtt_bridge_url = 'http://tools.lysis-iot.com/MqttPublish/publish.php'
topic = 'scb'


def mqtt_publish():
    form_data = urllib.urlencode(
        {'topic': topic, 'message': 'position'})

    result = urlfetch.fetch(
        url='http://tools.lysis-iot.com/MqttPublish/publish.php',
        payload=form_data,
        method=urlfetch.POST)
    return result
