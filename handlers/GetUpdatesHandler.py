import json
import urllib2

import webapp2
from google.appengine.api import urlfetch

from utils.token import get_base_url

BASE_URL = get_base_url()


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(
            json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))