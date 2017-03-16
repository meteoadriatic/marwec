import urllib.request
import xmltodict
import datetime
import os

try:
    os.remove('data/input/Maksimir.obs.csv')
except:
    pass

for num in range(00, 24):
    num = str(num)
    num = num.zfill(2)
    url = 'http://vrijeme.hr/tablice/hrvatska_n_' + num + '.xml'
    response = urllib.request.urlopen(url)
    data = response.read()
    doc = xmltodict.parse(data)

    current_date = doc['Hrvatska']['DatumTermin']['Datum']
    current_time = doc['Hrvatska']['DatumTermin']['Termin']
    current_date_time = current_date + '_' + current_time
    current_unix_time = datetime.datetime.strptime(current_date_time, "%d.%m.%Y_%H").timestamp()
    print('date =', current_date, ', time =', current_time, ', timestamp  =', int(current_unix_time))

    locindex = 0
    while True:
        locindex = locindex + 1
        location = doc['Hrvatska']['Grad'][locindex]['GradIme']
        temperature = doc['Hrvatska']['Grad'][locindex]['Podatci']['Temp']
        temperature = float(temperature)
        temperature = temperature + 273.15
        temperature = "{0:.1f}".format(temperature)
        if location == 'Zagreb-Maksimir':
            print('temperature =', temperature)
            with open("data/input/Maksimir.obs.csv", "a") as myfile:
                myfile.write(str(int(current_unix_time)) + '\t' + str(temperature) + '\n')
            break
