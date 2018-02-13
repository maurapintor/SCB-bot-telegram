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
        maxtemp = []

        for i in xrange(len(data)):
            c = data[i].trip_id
            maxtemp.append(int(c))

        for i in xrange(len(data)):

            c = data[i].trip_id
            trip_total.append(int(c))

            if (data[i].trip_id == max(maxtemp)):
                print "son dentro"
                temp = []
                a = data[i].latitude
                b = data[i].longitude
                # c = data[i].trip_id
                d = data[i].updated_at
                # e = data[i].trip_id

                temp.append(float(a))
                temp.append(float(b))
                # temp.append(int(c))
                temp.append(str(d))
                # temp.append(int(e))

                lista_posizione_e_data.append(temp)
                # trip_total.append(int(c))

                # print lista_posizione_e_data
                print d

        trip_total = list(set(trip_total))

        template_values = {
            'coordinate': lista_posizione_e_data,
            'trip_all': trip_total,
        }

        self.response.write(template.render("templates/home.html", template_values))



class TragittoHandler(webapp2.RequestHandler):
    def get(self, trip_id):

        sense_data = SensedData()
        print trip_id
        # print sense_data

        data = sense_data.query().fetch()

        print "Data = {}".format(data[0])

        lista_posizione_e_data = []
        trip_total = []

        for i in xrange(len(data)):

            c = data[i].trip_id
            trip_total.append(int(c))

            if (data[i].trip_id == int(trip_id)):
                # print "son dentro"
                temp = []
                a = data[i].latitude
                b = data[i].longitude
                # c = data[i].trip_id
                d = data[i].updated_at
                # e = data[i].trip_id

                temp.append(float(a))
                temp.append(float(b))
                # temp.append(int(c))
                temp.append(str(d))
                # temp.append(int(e))

                lista_posizione_e_data.append(temp)
                # trip_total.append(int(c))

                # print lista_posizione_e_data

        trip_total = list(set(trip_total))

        # print lista_posizione_e_data

        lista_posizione_e_data = sorted(lista_posizione_e_data, key=lambda item: item[2])

        # for i in lis2:
        #     print i

        template_values = {
            'coordinate': lista_posizione_e_data,
            'trip_all': trip_total,
        }

        self.response.write(template.render("templates/home.html", template_values))