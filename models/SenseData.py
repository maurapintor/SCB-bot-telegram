from google.appengine.ext import ndb


class SensedData(ndb.Model):
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now=True)
    speed = ndb.StringProperty()
    trip_id = ndb.StringProperty()