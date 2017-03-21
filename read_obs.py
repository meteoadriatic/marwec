import requests as req
import xmltodict
import datetime as dt
import os

'''
try:
    os.remove('data/input/Maksimir.obs.csv')
except:
    pass
'''

STATIONS = ["Zagreb-Maksimir"]
output_path = "data/input/"
file_name = "Maksimir.obs.csv"
hours = 24


def to_timestamp(dt, epoch=dt.datetime(1970, 1, 1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


# create directory if doesn't exists
if not os.path.exists(output_path):
    print ("Creating directory {}".format(output_path))
    os.makedirs(output_path)

# fetch weather data
for hour in range(hours):
    url = 'http://vrijeme.hr/tablice/hrvatska_n_{hour:02}.xml'.format(hour=hour)
    response = req.get(url)
    response.raise_for_status()
    data = response.content
    doc = xmltodict.parse(data)

    current_date = doc['Hrvatska']['DatumTermin']['Datum']
    current_time = doc['Hrvatska']['DatumTermin']['Termin']
    current_date_time = current_date + '_' + current_time
    current_date_time = dt.datetime.strptime(current_date_time, "%d.%m.%Y_%H")
    current_unix_time = to_timestamp(current_date_time)
    print('date =', current_date, ', time =', current_time, ', timestamp  =', int(current_unix_time))

    dhmz_stations = doc["Hrvatska"]["Grad"]
    file = output_path + file_name
    with open(file, "a") as output_file:
        for station in dhmz_stations:
            try:
                if station["GradIme"] in STATIONS:
                    try:
                        temperature = float(station["Podatci"]["Temp"])
                        temperature += 273.15  # convert C to K
                        print ("temperature = {:1}".format(temperature))
                        output_file.write("{},{:1}\n".format(current_unix_time, temperature))
                    except ValueError as e:
                        print ("Couldn't convert value to float: {}, error: {}".format(temperature, e))
                        continue
            except KeyError as e:
                print (str(e))
