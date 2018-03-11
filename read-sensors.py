import glob
import re
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
print (os.path.join(script_dir, '../server/'))
sys.path.append(os.path.join(script_dir, '../server/'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensors.settings")

# from sensors.models import *

'''
    SUMMARY
loop through 1 wire devices folder and return that data in an
{
    'id': 'value'
}
format. Right now, this is just for temperature sensors, and may need to be updated to
work with other types of devices.
'''


'''
    SETUP
'''

w1_list = glob.glob("/sys/bus/w1/devices/*")
w1_folder_regex = re.compile('\d+-\d+')

sensor_reading_regex = re.compile('[\d]+\n')


# Sample data
#w1_list = ['foobar', '1234567890-2345678900987654321']
# end sample data

'''
    RUN
'''


w1_list = filter(w1_folder_regex.search, w1_list)

for sensor in w1_list:
    sensor_serial = None
    sensor_reading = None

    sensor_serial = w1_folder_regex.search(sensor).group(0)

    try:
        sensor_obj = Sensor.objects.get(serial=sensor_serial)
    except sensor.DoesNotExist:
        sensor_obj = Sensor(serial=sensor_serial)
        sensor_obj.save()

    with open(sensor + '/w1_slave') as f:
        sensor_reading = f.readlines()

    sensor_reading = ' '.join(sensor_reading)
    sensor_reading = sensor_reading_regex.search(sensor_reading).group(0)

    reading = Reading(sensor=sensor_obj, value=sensor_reading)
    reading.save()
