__author__ = 'Ryan'

from BidRequest import BidRequest
from Coordinate import Coordinate
from collections import defaultdict
from datetime import datetime
from decimal import Decimal

invalid_coordinates = []
imprecise_coordinates = []
exact_duplicate_bid_requests = []
centroids = defaultdict(list)


def is_valid_coordinate(coordinate):
    return -90.0 <= coordinate.lat <= 90.0 and -180.0 <= coordinate.lng <= 180.0


def is_precise_enough(coordinate):
    return Decimal(str(coordinate.lat)).as_tuple().exponent <= -4 \
        and Decimal(str(coordinate.lng)).as_tuple().exponent <= -4


def is_exact_duplicate_bid_request(id_request, time, coordinate, dictionary):
    current_list = dictionary[id_request]
    bid_request = BidRequest(id_request, time, coordinate)
    return bid_request in current_list


def parse_line_for_bid_request(line):
    split_line = line.split('|')
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


def fill_user_id_dictionary_with_data():
    user_to_bid_request = defaultdict(list)
    f = open("input", "r")
    for line in f:
        # checks valid point and checks enough decimals
        bid_request = parse_line_for_bid_request(line)
        coordinate = bid_request.coordinate
        time = bid_request.time
        id_request = bid_request.id_request

        if not is_valid_coordinate(coordinate):
            invalid_coordinates.append(bid_request)
        if not is_precise_enough(coordinate):
            imprecise_coordinates.append(bid_request)

        if is_valid_coordinate(coordinate) and is_precise_enough(coordinate):
                if not is_exact_duplicate_bid_request(id_request, time, coordinate, user_to_bid_request):
                    user_to_bid_request[id_request].append(bid_request)
                else:
                    exact_duplicate_bid_requests.append(bid_request)

    f.close()
    return user_to_bid_request


table = fill_user_id_dictionary_with_data()
print len(table.items())
for key in table:
    print str(table[key]) + " " + str(len(table[key]))

print "Number of invalid bid requests: " + str(len(invalid_coordinates))
print "Number of imprecise bid requests: " + str(len(imprecise_coordinates))
print "Number of exact duplicate bid requests: " + str(len(exact_duplicate_bid_requests))
