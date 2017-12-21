from google.appengine.ext import ndb


class SensedData(ndb.Model):
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()
    speed = ndb.StringProperty()