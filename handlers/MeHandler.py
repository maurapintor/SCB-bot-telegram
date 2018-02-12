import urllib2

import webapp2
import json
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

from utils.token import get_base_url


class MeHandler(webapp2.RequestHandler):
    def get(self):
        template_values = "ciao"
        BASE_URL = get_base_url()

        self.response.out.write(
            template.render("templates/home.html", template_values))
        urlfetch.set_default_fetch_deadline(60)
        # commento foo
        self.response.write(
            json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))