from models.SenseData import SensedData


def check_trip(timestamp=0):

    sense_data = SensedData()

    sense_data = SensedData().query().order(-SensedData.updated_to).fetch()
    print sense_data[0].updated_to
    last_sample = sense_data[0]

    return