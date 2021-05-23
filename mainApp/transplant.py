import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teum.settings")
django.setup()
from mainApp.models import *
import time
import datetime

import csv


def save_station():

    with open("station_info_basic.csv", "r", encoding="utf-8-sig") as station_file:

        reader = csv.reader(station_file)

        for data in reader:
            station = Station()
            station.line = data[0][0]
            station.name = data[1]
            if (data[3] == "Y"):
                station.foothold = True
            else:
                station.foothold = False

            station.platform = int(data[2])
            station.save()

def distance_save():
    with open("distance_info_basic.csv", "r", encoding="utf-8-sig") as distance_file:

        reader = csv.reader(distance_file)

        for data in reader:

            station = Station.objects.filter(line=data[0][0], name=data[1], platform=int(data[2]))
            door = Door()
            door.station = station.first()
            door.car_number = int(data[3])
            door.door_number = int(data[4])
            door.distance = float(data[5])
            door.save()

def save_complexity():
    with open("complexity_info_basic.csv", "r", encoding="utf-8-sig") as complexity_file:
        reader = csv.reader(complexity_file)

        for data in reader:

            station = Station.objects.filter(line=data[1][0], name__contains=data[2], platform=data[3]).first()

            if station is not None:

                complexity = Complexity()
                complexity.station = station
                complexity.day = int(data[0])
                complexity.save()



                time_start = "05:30"
                datetime_object = datetime.datetime.strptime(time_start, "%H:%M")


                for j in range(4, 43):

                    time = Time()
                    time.complex_id = complexity
                    time.time = datetime_object

                    if (data[j] != " " or ""):
                        time.complexity = data[j]
                        time.save()
                    else:
                        time.complexity = 0.0
                        time.save()

                    datetime_object = datetime_object + datetime.timedelta(minutes=30)



def test():

    now = datetime.datetime.now()
    nowTime = now.strftime('%H:%M')
    print(type(now.time()))
    print(now.time())

    date = "05:30"
    dateTimeobj = datetime.datetime.strptime(date, "%H:%M")
    print(dateTimeobj)

    for i in range(39):
        print(dateTimeobj.strftime("%H:%M"))
        dateTimeobj = dateTimeobj + datetime.timedelta(minutes=30)



    obj = Time()
    obj.complex_id = Complexity.objects.first()
    obj.time = now.time()
    obj.complexity = 1
    obj.save()

    print(dateTimeobj.time() < now.time())

    for i in range(4, 43):
        print(i)


save_station()
distance_save()
save_complexity()