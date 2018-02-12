import webapp2
from google.appengine.ext.webapp import template

from models.SenseData import SensedData


class MapHandler(webapp2.RequestHandler):
    def get(self):
        sense_data = SensedData()

        # print sense_data

        data = sense_data.query().fetch()

        # print "Data = {}".format(data[0])

        lista_posizione_e_data = []

        for i in xrange(len(data)):
            # if str(data[i]['timestamp'][:11]) == str(data[0]['timestamp'][:11]):
            temp = []

            a = data[i].latitude
            b = data[i].longitude
            # c = data[i].speed
            # d = data[i].updated_at
            # e = data[i].trip_id

            temp.append(float(a))
            temp.append(float(b))
            # temp.append(str(c))
            # temp.append(str(d))
            # temp.append(int(e))

            lista_posizione_e_data.append(temp)

            # print lista_posizione_e_data

        template_values = {
            'coordinate': lista_posizione_e_data,
            'lat': data[0].latitude,
            'long': data[0].longitude,
            'speed': data[0].speed,
            'date': data[0].updated_at,
            'trip': data[0].trip_id
        }

        self.response.write(
            template.render("templates/mappa.html", template_values))
