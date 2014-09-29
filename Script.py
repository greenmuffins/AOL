__author__ = 'Ryan'

from BidRequest import BidRequest
from Coordinate import Coordinate
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from operator import itemgetter

user_to_bid_request = defaultdict(list)
invalid_coordinates = defaultdict(int)
imprecise_coordinates = defaultdict(int)
exact_duplicate_bid_requests = defaultdict(int)
coordinate_count = defaultdict(int)


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


def fill_dictionaries_with_data():
    f = open("input", "r")
    for line in f:
        bid_request = parse_line_for_bid_request(line)
        coordinate = bid_request.coordinate
        time = bid_request.time
        id_request = bid_request.id_request

        if not is_valid_coordinate(coordinate):
            invalid_coordinates[bid_request] += 1
        if not is_precise_enough(coordinate):
            imprecise_coordinates[bid_request] += 1

        if is_valid_coordinate(coordinate) and is_precise_enough(coordinate):
            if not is_exact_duplicate_bid_request(id_request, time, coordinate, user_to_bid_request):
                user_to_bid_request[id_request].append(bid_request)
                coordinate_count[coordinate] += 1
            else:
                exact_duplicate_bid_requests[bid_request] += 1
    f.close()


def number_of_values_in_dictionary(dictionary):
    count = 0
    for value in dictionary.values():
        if isinstance(value, list):
            count += len(value)
        else:
            count += value
    return count


def write_good_bid_requests_to_file():
    f = open("good_bid_requests.txt", "w")
    f.write("Number of unique user ids: " + str(len(user_to_bid_request.keys())) + "\n")
    f.write("Number of unique bid requests: "
            + str(number_of_values_in_dictionary(user_to_bid_request)) + "\n")
    for key in user_to_bid_request:
        f.write(str(user_to_bid_request[key]) + "\n")
    f.close()


def write_invalid_bid_requests_to_file():
    f = open("invalid_bid_requests.txt", "w")
    f.write("Number of invalid bid requests: "
            + str(number_of_values_in_dictionary(invalid_coordinates)) + "\n")
    sorted_invalid_coordinates = sorted(invalid_coordinates.items(), key=itemgetter(1), reverse=True)
    for bid_request in sorted_invalid_coordinates:
        f.write(str(bid_request[1]) + ": " + str(bid_request[0]) + "\n")
    f.close()


def write_imprecise_bid_requests_to_file():
    f = open("imprecise_bid_requests.txt", "w")
    f.write("Number of imprecise bid requests: "
            + str(number_of_values_in_dictionary(imprecise_coordinates)) + "\n")
    sorted_imprecise_coordinates = sorted(imprecise_coordinates.items(), key=itemgetter(1), reverse=True)
    for bid_request in sorted_imprecise_coordinates:
        f.write(str(bid_request[1]) + ": " + str(bid_request[0]) + "\n")
    f.close()


def write_exact_duplicate_bid_requests_to_file():
    f = open("exact_duplicate_bid_requests.txt", "w")
    f.write("Number of exact duplicate bid requests: "
            + str(number_of_values_in_dictionary(exact_duplicate_bid_requests)) + "\n")
    sorted_exact_duplicate_bid_requests = sorted(exact_duplicate_bid_requests.items(), key=itemgetter(1), reverse=True)
    for bid_request in sorted_exact_duplicate_bid_requests:
        f.write(str(bid_request[1]) + ": " + str(bid_request[0]) + "\n")
    f.close()


def write_coordinates_to_file():
    f = open("good_coordinates.txt", "w")
    f.write("Number of good coordinates: "
            + str(number_of_values_in_dictionary(coordinate_count)) + "\n")
    sorted_coordinate_count = sorted(coordinate_count.items(), key=itemgetter(1), reverse=True)
    for coordinate in sorted_coordinate_count:
        f.write(str(coordinate[1]) + ": " + str(coordinate[0]) + "\n")
    f.close()


fill_dictionaries_with_data()
write_good_bid_requests_to_file()
write_invalid_bid_requests_to_file()
write_imprecise_bid_requests_to_file()
write_exact_duplicate_bid_requests_to_file()
write_coordinates_to_file()

