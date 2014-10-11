__author__ = 'Ryan'

from BidRequest import BidRequest
from Coordinate import Coordinate
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from csv import writer

user_id_to_bid_request_table = defaultdict(list)
coordinate_count_table = defaultdict(int)
invalid_coordinates = []
imprecise_coordinates = []
exact_duplicate_bid_requests = []


def is_valid_coordinate(coordinate):
    return -90.0 <= coordinate.lat <= 90.0 and -180.0 <= coordinate.lng <= 180.0


def is_precise_enough(coordinate):
    return Decimal(str(coordinate.lat)).as_tuple().exponent <= -4 \
        and Decimal(str(coordinate.lng)).as_tuple().exponent <= -4


def is_exact_duplicate_bid_request(bid_request, dictionary):
    current_list = dictionary[bid_request.id_request]
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


def fill_dictionaries_with_data(input_file):
    f = open(input_file, "r")
    for line in f:
        bid_request = parse_line_for_bid_request(line)
        coordinate = bid_request.coordinate
        id_request = bid_request.id_request

        if not is_valid_coordinate(coordinate):
            invalid_coordinates.append(coordinate)
        if not is_precise_enough(coordinate):
            imprecise_coordinates.append(coordinate)

        if is_valid_coordinate(coordinate) and is_precise_enough(coordinate):
            if not is_exact_duplicate_bid_request(bid_request, user_id_to_bid_request_table):
                user_id_to_bid_request_table[id_request].append(bid_request)
                coordinate_count_table[coordinate] += 1
            else:
                exact_duplicate_bid_requests.append(bid_request)
    f.close()


#not being used
def number_of_values_in_dictionary(dictionary):
    count = 0
    for value in dictionary.values():
        if isinstance(value, list):
            count += len(value)
        else:
            count += value
    return count


def write_bid_requests_to_file(output_file, data):
    f = open(output_file, "wb")
    row_writer = writer(open(output_file, "wb"))
    row_writer.writerow(["id_request", "time", "lat", "lng"])
    if isinstance(data, list):
        for bid_request in data:
            row_writer.writerow([bid_request.id_request, bid_request.time, bid_request.coordinate.lat,
                                 bid_request.coordinate.lng])
    else:
        for id_request in data:
            current_list = data[id_request]
            for bid_request in current_list:
                row_writer.writerow([bid_request.id_request, bid_request.time, bid_request.coordinate.lat,
                                     bid_request.coordinate.lng])
    f.close()


def write_coordinates_to_file(output_file, data):
    f = open(output_file, "wb")
    row_writer = writer(open(output_file, "wb"))
    if isinstance(data, list):
        row_writer.writerow(["lat", "lng"])
    else:
        row_writer.writerow(["frequency", "lat", "lng"])
    for coordinate in data:
        if isinstance(data, list):
            row_writer.writerow([coordinate.lat, coordinate.lng])
        else:
            row_writer.writerow([data[coordinate], coordinate.lat, coordinate.lng])
    f.close()


def write_to_all_files():
    fill_dictionaries_with_data("input2")
    write_bid_requests_to_file("good_bid_requests.csv", user_id_to_bid_request_table)
    write_bid_requests_to_file("exact_duplicate_bid_requests.csv", exact_duplicate_bid_requests)
    write_coordinates_to_file("invalid_coordinates.csv", invalid_coordinates)
    write_coordinates_to_file("imprecise_coordinates.csv", imprecise_coordinates)
    write_coordinates_to_file("coordinate_frequency.csv", coordinate_count_table)

write_to_all_files()
