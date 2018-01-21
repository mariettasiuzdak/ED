from numpy import genfromtxt
from math import cos, asin, sqrt, isnan
import numpy as np
from sys import exit


# ALGORYTM DO OBLICZANIA NAJBLIZSZEJ WSPOLRZEDNEJ GEOGRAFICZNEJ
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))


def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'], v['lon'], p['lat'], p['lon']))


def calculate_factor_p(num_of_furnaces, sensor_coor, place_coor, alpha):
    return num_of_furnaces / pow(
        distance(sensor_coor['lat'], sensor_coor['lon'], place_coor['lat'], place_coor['lon']), alpha)

if __name__ == '__main__':

    # WCZYTUJE DANE
    sensor_locations = genfromtxt('Airly_data/sensor_locations.csv', delimiter=',')
    furnaces = genfromtxt('Piece/CSV/WS_PIECE_17_BUD_cvs.csv', delimiter=',', usecols=range(9))
    airly_all = genfromtxt('Airly_data/all-2017.csv', delimiter=';', dtype='unicode')
    data_wios_pm25 = genfromtxt('dane_wios_25.csv', delimiter=',')

    # DEKLARUJE TABLICE DO PRZECHOWYWANIA WSPOLRZEDNYCH GEOGRAFICZNYCH
    sensor_coordinates = []
    closest_sensor = []
    furnace_coordinates = []
    factor_p = []

    # TWORZE TABLICE ZE WSPOLRZEDNYMI SENSOROW
    row_count_sensors = sum(1 for row in sensor_locations)
    for x in range(1, row_count_sensors):
        lon = sensor_locations[x, 2]
        lat = sensor_locations[x, 1]
        sensor_coordinates.append({'lat': lat, 'lon': lon})

    # TWORZYMY TABLICE Z ID SENSOROW DO PRZECHOWYWANIA WSPOLCZYNNIKOW
    for x in range(1, row_count_sensors):
        id = sensor_locations[x, 0]
        lon = sensor_locations[x, 2]
        lat = sensor_locations[x, 1]
        factor_p.append({'id': int(id), 'factor': 0, 'lon': lon, 'lat': lat})

    row_count = sum(1 for row in furnaces)

    # LICZYMY WSPOLCZYNNIK P WG WZORU
    for sensor in factor_p:
        for x in range(1, row_count):
            number_of_furnaces = int(furnaces[x, 6])
            lon = furnaces[x, 0]
            lat = furnaces[x, 1]
            place_coord = {'lat': lat, 'lon': lon}
            res = calculate_factor_p(number_of_furnaces, sensor, place_coord, 2)
            if not isnan(res):
                sensor['factor'] += res

    # for sensor in factor_p:
    #     print sensor['id'], sensor['factor']

    # NA LISCIE PIECOW SPRAWDZAM PO KOLEI, W KTORYCH MIEJSACH SA JAKIES PIECE (W SUMIE TRZEBA TO ZROBIC TEZ DLA MIEJSC GDZIE NIE MA PIECOW)
    # NASTEPNIE SZUKAM DLA DANEGO MIEJSCA Z PIECEM NAJBLIZSZEGO SENSORA I PRINTUJE GO

    for x in range(1, row_count):
        # if furnaces[x, 6] != 0:
        number_of_furnaces = int(furnaces[x, 6])
        lon = furnaces[x, 0]
        lat = furnaces[x, 1]
        furnace_coordinates = {'lat': lat, 'lon': lon}
        closest_sensor = closest(sensor_coordinates, furnace_coordinates)

        # Szukam ID najblizszego sensora
        for y in range(1, row_count_sensors):
            if sensor_locations[y, 1] == closest_sensor['lat'] and sensor_locations[y, 2] == closest_sensor['lon']:
                sensor_id = sensor_locations[y, 0]

        column_count_airly = sum(1 for column in airly_all.T)
        row_count_airly = sum(1 for column in airly_all)
        pm25 = []
        #  znajdujemy kolumne, w ktorej sa dane pylowe dla danego sensora, tworzymy tablice z danymi z sensora dla danego pieca

        for z in range(0, column_count_airly):
            if airly_all[0, z] == str(int(sensor_id)) + "_pm25":
                for w in range(1, row_count_airly):
                    pm25.append(airly_all[w, z])
                    # teraz kazdemu miejscu przypisana jest ilosc piecow i tablica z zapyleniem

            # print(pm25)
            # print(number_of_furnaces)



    '''
    TODO
    Liczenie wspolczynnika okreslajacego jakas proporcje miedzy zapyleniem a iloscia piecow w regionie
    '''
