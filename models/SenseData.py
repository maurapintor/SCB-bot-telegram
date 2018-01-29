from google.appengine.ext import ndb


class SensedData(ndb.Model):
    latitude = ndb.StringProperty()
    longitude = ndb.StringProperty()
    updated_at = ndb.DateTimeProperty(auto_now=False)
    speed = ndb.StringProperty()
    trip_id = ndb.StringProperty()