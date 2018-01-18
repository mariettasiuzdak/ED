from numpy import genfromtxt
from math import cos, asin, sqrt
import numpy as np
from sys import exit

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

#DEKLARUJĘ TABLICE DO PRZECHOWYWANIA WSPÓŁRZĘDNYCH GEOGRAFICZNYCH
sensor_coordinates=[]
closest_sensor=[]
furnace_coordinates=[]

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
    if furnaces[x, 6] == 0:
        number_of_furnaces = furnaces[x, 6]
        lon = furnaces[x,0]
        lat = furnaces[x,1]
        furnace_coordinates = {'lat':lat, 'lon': lon}
        closest_sensor=closest(sensor_coordinates, furnace_coordinates)
        print(closest_sensor)
        #exit(0)
'''
TODO
Skoro mamy już najbliższy sensor przypisany do pieca, musimy pobrać ID danego sensora na podstawie współrzędnych, a potem na podstawie ID znaleźć
wartośći PM2.5 przypisane do tego sensora z całego roku.

Następnie będziemy liczyć współczynnik określający jakąś proporcję między zapyleniem a ilością pieców w regionie
'''