from models.SenseData import SensedData
import webapp2
# standard app engine imports
from google.appengine.ext.webapp import template

# ================================


class MainHandler(webapp2.RequestHandler):
    def get(self):
        sense_data = SensedData()

        # print sense_data

        data = sense_data.query().fetch()

        # print "Data = {}".format(data[0])

        lista_posizione_e_data = []
        trip_total = []

        for i in xrange(len(data)):
            # if str(data[i]['timestamp'][:11]) == str(data[0]['timestamp'][:11]):
            temp = []

            a = data[i].latitude
            b = data[i].longitude
            c = data[i].trip_id
            # d = data[i].updated_at
            # e = data[i].trip_id

            temp.append(float(a))
            temp.append(float(b))
            temp.append(int(c))
            # temp.append(str(d))
            # temp.append(int(e))

            lista_posizione_e_data.append(temp)
            trip_total.append(int(c))

            # print lista_posizione_e_data

        template_values = {
            'coordinate': lista_posizione_e_data,
            'trip_all': trip_total,
            'last_trip': max(trip_total),
            'lat': data[0].latitude,
            'long': data[0].longitude,
            'speed': data[0].speed,
            'date': data[0].updated_at,
            'trip': data[0].trip_id
        }

        self.response.write(template.render("templates/home.html", template_values))

