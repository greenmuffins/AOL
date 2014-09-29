__author__ = 'Ryan'

from BidRequest import BidRequest
from collections import defaultdict
from datetime import datetime

invalid_coordinates = []
imprecise_coordinates = []
duplicate_coordinates = []


def is_valid_coordinates(lat, lng):
    return -90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0


def is_precise_enough(lat, lng):
    return len(str(lat-int(lat))) >= 4 and len(str(lng-int(lng))) >= 4


def is_duplicate(id_request, time, lat, lng, dictionary):
    current_list = dictionary[id_request]
    bid_request = BidRequest(id_request, time, lat, lng)
    if bid_request in current_list:
        return True
    return False


def parse_line_for_bid_request(line):
    split_line = line.split('|')
    time = create_datetime(split_line[0][:19])
    id_request = split_line[1]
    lat = float(split_line[2])
    lng = float(split_line[3])
    return BidRequest(id_request, time, lat, lng)


def create_datetime(datetime_string):
    year = int(datetime_string[:4])
    month = int(datetime_string[5:7])
    day = int(datetime_string[8:10])
    hour = int(datetime_string[11:13])
    minute = int(datetime_string[14:16])
    second = int(datetime_string[17:len(datetime_string)])
    return datetime(year, month, day, hour, minute, second)


def fill_dictionary_with_data():
    user_to_bid_request = defaultdict(list)
    f = open("input", "r")
    for line in f:
        # checks valid point and checks enough decimals
        bid_request = parse_line_for_bid_request(line)
        if is_valid_coordinates(bid_request.get_lat(), bid_request.get_lng()):
            if is_precise_enough(bid_request.get_lat(), bid_request.get_lng()):
                if not is_duplicate(bid_request.get_id(), bid_request.get_time(), bid_request.get_lat(),
                                    bid_request.get_lng(), user_to_bid_request):
                    user_to_bid_request[bid_request.get_id()].append(bid_request)
                else:
                    duplicate_coordinates.append(bid_request)
            else:
                imprecise_coordinates.append(bid_request)
        else:
            invalid_coordinates.append(bid_request)
    f.close()
    return user_to_bid_request

table = fill_dictionary_with_data()
print len(table.items())
print table

print "Number of invalid bid requests: " + str(len(invalid_coordinates))
print "Number of imprecise bid requests: " + str(len(imprecise_coordinates))
print "Number of duplicate bid requests: " + str(len(duplicate_coordinates))
print imprecise_coordinates