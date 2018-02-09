import json
import urllib
import urllib2

import webapp2
from google.appengine.api import urlfetch

from utils.token import get_base_url


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        BASE_URL = get_base_url()
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(
                urllib2.urlopen(BASE_URL + 'setWebhook',
                                urllib.urlencode({'url': url})))))

