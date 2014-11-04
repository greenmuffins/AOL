__author__ = 'Ryan'

from BidRequest import BidRequest
from Coordinate import Coordinate
from datetime import datetime
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