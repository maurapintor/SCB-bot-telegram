import webapp2
from google.appengine.ext.webapp import template


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = "ciao"
        self.response.out.write(
            template.render("templates/home.html", template_values))