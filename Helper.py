__author__ = 'Ryan'

from BidRequest import BidRequest
from Coordinate import Coordinate
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt


def parse_line_for_bid_request(line_string):
    split_line = line_string.split('|')
    time = create_datetime(split_line[0][:19])
    id_request = split_line[1]
    lat = float(split_line[2])
    lng = float(split_line[3])
    return BidRequest(id_request, time, Coordinate(lat, lng))


def create_datetime(datetime_string):
    year = int(datetime_string[:4])
    month = int(datetime_string[5:7])
    day = int(datetime_string[8:10])
    hour = int(datetime_string[11:13])
    minute = int(datetime_string[14:16])
    second = int(datetime_string[17:len(datetime_string)])
    return datetime(year, month, day, hour, minute, second)


def distance(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def number_of_values_in_dictionary(dictionary):
    count = 0
    for value in dictionary.values():
        if isinstance(value, list):
            count += len(value)
        else:
            count += value
    return count


def is_point_in_polygon(lat, lng, lat_points, lng_points):
    j = len(lat_points) - 1
    odd_nodes = False
    for i in range(len(lat_points)):
        if (lng_points[i] <= lng < lng_points[j] or lng_points[j] <= lng < lng_points[i]) \
                and (lat <= (lat_points[j] - lat_points[i]) * (lng - lng_points[i]) / (lng_points[j] - lng_points[i]) +
                     lat_points[i]):
            odd_nodes = not odd_nodes
        j = i
    return odd_nodes


def is_point_in_north_america(lat, lng):
    lat_points = [48, 24, 24, 7, 5, 31, 50, 55, 72, 72]
    lng_points = [-50, -81, -88, -75, -85, -125, -130, -170, -165, -68]
    return is_point_in_polygon(lat, lng, lat_points, lng_points)


def convert_from_eastern_to_local_time(lat, lng, time):
    if -90 < lng <= -75:
        return time-timedelta(hours=1)
    elif -105 < lng <= -90:
        return time-timedelta(hours=2)
    elif -126 < lng <= -105:
        return time-timedelta(hours=3)
    else:
        return time


print is_point_in_north_america(39, -98)
print convert_from_eastern_to_local_time(30, -120, datetime(2014, 5, 5, 14, 30, 3))
