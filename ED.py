from numpy import genfromtxt
from math import cos, asin, sqrt
import numpy as np
from sys import exit
#from pylab import *

#ALGORYTM DO OBLICZANIA NAJBLIŻSZEJ WSPÓŁRZĘDNEJ GEOGRAFICZNEJ
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

#WCZYTUJĘ DANE
sensor_locations = genfromtxt('Airly_data/sensor_locations.csv', delimiter=',')
furnaces = genfromtxt('Piece/CSV/WS_PIECE_17_BUD_cvs.csv', delimiter=',', usecols=range(9))
airly_all = genfromtxt('Airly_data/all-2017.csv', delimiter=';', dtype='unicode')

#DEKLARUJĘ TABLICE DO PRZECHOWYWANIA WSPÓŁRZĘDNYCH GEOGRAFICZNYCH
sensor_coordinates=[]
closest_sensor=[]
furnace_coordinates=[]
f0_mean = []
f1_mean= []
f2_mean = []
f3_mean = []
f4_mean = []
f5_mean = []
f6_mean= []
f7_mean = []
f8_mean = []
f_more = []

#TWORZĘ TABLICĘ ZE WSPÓŁRZĘDNYMI SENSORÓW
row_count_sensors = sum(1 for row in sensor_locations)
for x in range(1,row_count_sensors):
    lon = sensor_locations[x,2]
    lat = sensor_locations[x,1]
    sensor_coordinates.append({'lat':lat, 'lon': lon})

#NA LIŚCIE PIECÓW SPRAWDZAM PO KOLEI, W KTÓRYCH MIEJSACH SĄ JAKIEŚ PIECE (W SUMIE TRZEBA TO ZROBIĆ TEŻ DLA MIEJSC GDZIE NIE MA PIECÓW)
#NASTĘPNIE SZUKAM DLA DANEGO MIEJSCA Z PIECEM NAJBLIŻSZEGO SENSORA I PRINTUJĘ GO
row_count = sum(1 for row in furnaces)
for x in range(1,row_count):
    #if furnaces[x, 6] != 0:
    number_of_furnaces = int(furnaces[x,6])
    lon = furnaces[x,0]
    lat = furnaces[x,1]
    furnace_coordinates = {'lat':lat, 'lon': lon}
    closest_sensor=closest(sensor_coordinates, furnace_coordinates)

#Szukam ID najbliższego sensora
    for y in range(1,row_count_sensors):
        if sensor_locations[y,1] == closest_sensor['lat'] and sensor_locations[y,2] == closest_sensor['lon']:
            sensor_id = sensor_locations[y,0]

    column_count_airly = sum(1 for column in airly_all.T)
    row_count_airly = sum(1 for column in airly_all)
    pm25 = []
    #  znajdujemy kolumnę, w której są dane pyłowe dla danego sensora, tworzymy tablicę z danymi z sensora dla danego pieca

    for z in range(0,column_count_airly):
        if airly_all[0,z] == str(int(sensor_id)) + "_pm25":
            for w in range(1,row_count_airly):
                pm25.append(airly_all[w,z])
# teraz każdemu miejscu przypisana jest ilość pieców i tablica z zapyleniem
    #print(pm25)
    #print(number_of_furnaces)


    pm25 = list(filter(None, pm25))
    pm25 = list(map(float, pm25))
    if pm25:
        mean_pm25 = sum(pm25) / len(pm25)
        if (number_of_furnaces == 0):
             f0_mean.append(mean_pm25)
        elif (number_of_furnaces == 1):
             f1_mean.append(mean_pm25)
        elif (number_of_furnaces == 2):
            f2_mean.append(mean_pm25)
        elif (number_of_furnaces == 3):
            f3_mean.append(mean_pm25)
        elif (number_of_furnaces == 4):
            f4_mean.append(mean_pm25)
        elif (number_of_furnaces == 5):
            f5_mean.append(mean_pm25)
        elif (number_of_furnaces == 6):
            f6_mean.append(mean_pm25)
        elif (number_of_furnaces == 7):
            f7_mean.append(mean_pm25)
        elif (number_of_furnaces == 8):
            f8_mean.append(mean_pm25)
        else:
            f_more.append(mean_pm25)
    else:
        continue



f0_mean = sum(f0_mean) / len(f0_mean)
f1_mean = sum(f1_mean) / len(f1_mean)
f2_mean = sum(f2_mean) / len(f2_mean)
f3_mean = sum(f3_mean) / len(f3_mean)
f4_mean = sum(f4_mean) / len(f4_mean)
f5_mean = sum(f5_mean) / len(f5_mean)
f6_mean = sum(f6_mean) / len(f6_mean)
f7_mean = sum(f7_mean) / len(f7_mean)
f8_mean = sum(f8_mean) / len(f8_mean)
f_more = sum(f_more) / len(f_more)

f_summary = []
f_summary.append(f0_mean)
f_summary.append(f1_mean)
f_summary.append(f2_mean)
f_summary.append(f3_mean)
f_summary.append(f4_mean)
f_summary.append(f5_mean)
f_summary.append(f6_mean)
f_summary.append(f7_mean)
f_summary.append(f8_mean)
f_summary.append(f_more)

plot([1,2,3,4], [1,4,9,16])
savefig('wykres.png')


'''
        f0_mean = []
    f1_mean= []
    f2_mean = []
    f3_mean = []
    f4_mean = []
    pm25_length = sum(1 for column in pm25)
    print(pm25_length)
    furnaces_array = []
    exit(0)
    for u in range(0,pm25_length):
        furnaces_array.append(number_of_furnaces)

'''
'''
TODO
Liczenie współczynnika określającego jakąś proporcję między zapyleniem a ilością pieców w regionie
'''