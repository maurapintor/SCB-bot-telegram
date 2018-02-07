import urllib

from google.appengine.api import urlfetch

mqtt_bridge_url = 'http://34.217.126.242/MqttPublish/publish.php'


def mqtt_publish():
    form_data = urllib.urlencode(
        {'topic': 'scb', 'message': 'position'})

    result = urlfetch.fetch(
        url='http://34.217.126.242/MqttPublish/publish.php',
        payload=form_data,
        method=urlfetch.POST)
    return result
