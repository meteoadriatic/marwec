# -*- coding: utf-8 -*-
import requests as req
import xmltodict
import datetime as dt
import os
from dateutil import tz
import pandas as pd

local_tz = tz.gettz('Europe/Zagreb')

STATIONS = ["Zagreb-Maksimir"]
output_path = "data/input/"
xml_output_path = "data/input/xml/"
file_name = "Maksimir.obs.csv"
hours = 24


def to_timestamp(dt, epoch=dt.datetime(1970, 1, 1)):
    td = dt - epoch.replace(tzinfo=tz.tzutc())
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


# create directory if doesn't exists
if not os.path.exists(output_path):
    print("Creating directory {}".format(output_path))
    os.makedirs(output_path)

# create directory if doesn't exists
if not os.path.exists(xml_output_path):
    print("Creating directory {}".format(xml_output_path))
    os.makedirs(xml_output_path)

# create empty dataframe
df = pd.DataFrame(columns=('timestamp', 'tmp2m', 'weather'))

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
    current_date_time = current_date_time.replace(tzinfo=local_tz)
    current_unix_time = to_timestamp(current_date_time)
    current_unix_time = int(current_unix_time)
    print('date =', current_date, ', time =', current_time, ', timestamp  =', int(current_unix_time))

    xml_filename = "{path}{timestamp}.xml".format(path=xml_output_path, timestamp=current_unix_time)
    with open(xml_filename, "w") as out_xml:
        out_xml.write(data)

    dhmz_stations = doc["Hrvatska"]["Grad"]
    #file = output_path + file_name
    # with open(file, "a") as output_file:
    for station in dhmz_stations:
        try:
            if station["GradIme"] in STATIONS:
                try:
                    temperature = float(station["Podatci"]["Temp"])
                    temperature += 273.15  # convert C to K
                    temperature = float("{0:.1f}".format(temperature))
                    print("temperature = {:1}".format(temperature))
                    if station["@autom"] == "0":
                        weather_type = str(station["Podatci"]["Vrijeme"])
                    else:
                        weather_type = 'NA'
                    print(weather_type)
                    # output_file.write("{},{:1},{}\n".format(current_unix_time, temperature, weather_type))
                    df = df.append({'timestamp': current_unix_time, 'tmp2m': temperature, 'weather': weather_type}, ignore_index=True)
                except ValueError as e:
                    print("Couldn't convert value to float: {}, error: {}".format(temperature, e))
                    continue
        except KeyError as e:
            print(str(e))

df['timestamp'] = df['timestamp'].map(lambda x: '%0.0f' % x)
df = df.sort_values('timestamp')
file = output_path + file_name
with open(file, 'a') as f:
    df.to_csv(f, header=False, index=False)
