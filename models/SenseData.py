from google.appengine.ext import ndb


class SensedData(ndb.Model):
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()
    updated_to = ndb.DateTimeProperty(auto_now=False)
    speed = ndb.StringProperty()
    trip_id = ndb.StringProperty()