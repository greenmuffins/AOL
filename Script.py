__author__ = 'Ryan'

from collections import defaultdict
from Coordinate import Coordinate
from csv import writer
from decimal import Decimal
from Helper import parse_line_for_bid_request, distance, number_of_values_in_dictionary
from time import mktime
from operator import itemgetter

coordinate_count_table = defaultdict(int)
device_id_to_bid_request_table = defaultdict(list)
device_id_to_frequency = defaultdict(int)

exact_duplicate_bid_requests = []
good_coordinates = []
imprecise_coordinates = []
invalid_coordinates = []
zip_codes = []


def is_exact_duplicate_bid_request(bid_request, dictionary):
    current_list = dictionary[bid_request.id_request]
    return bid_request in current_list


def fill_dictionaries_with_data(input_file):
    f = open(input_file, "r")
    for line_string in f:
        bid_request = parse_line_for_bid_request(line_string)
        coordinate = bid_request.coordinate
        id_request = bid_request.id_request

        if not coordinate.is_valid_coordinate():
            invalid_coordinates.append(coordinate)
        if not coordinate.is_precise_enough():
            imprecise_coordinates.append(coordinate)

        if coordinate.is_valid_coordinate and coordinate.is_precise_enough():
            if not is_exact_duplicate_bid_request(bid_request, device_id_to_bid_request_table):
                device_id_to_bid_request_table[id_request].append(bid_request)
                coordinate_count_table[coordinate] += 1
                good_coordinates.append(coordinate)
                device_id_to_frequency[id_request] += 1
            else:
                exact_duplicate_bid_requests.append(bid_request)
    f.close()


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


def concurrency(output_file):
    fc = open(output_file, "w")
    count = 0
    for key in device_id_to_bid_request_table:
        curr_list = device_id_to_bid_request_table[key]
        if len(curr_list) > 1:
            for x in range(0, len(curr_list) - 1):
                t = (curr_list[x].time.year, curr_list[x].time.month, curr_list[x].time.day, curr_list[x].time.hour,
                     curr_list[x].time.minute, curr_list[x].time.second, 1, 1, 0)
                t2 = (curr_list[x+1].time.year, curr_list[x+1].time.month, curr_list[x+1].time.day,
                      curr_list[x+1].time.hour, curr_list[x+1].time.minute, curr_list[x+1].time.second, 2, 1, 0)
                diff_time = mktime(t2)-mktime(t)
                #print diff_time
                if diff_time == 0:
                    diff_time = 0.01
                speed = distance(curr_list[0].coordinate.lat, curr_list[0].coordinate.lng, curr_list[1].coordinate.lat,
                                 curr_list[1].coordinate.lng)/(diff_time / 3600)
                if speed < 161:
                    score = 1
                elif speed > 644:
                    score = 0
                    count += 1
                else:
                    score = 1 - ((speed - 161) / 483)
                fc.write(str(key) + "," + str(distance(curr_list[0].coordinate.lng, curr_list[0].coordinate.lat,
                                                       curr_list[1].coordinate.lng, curr_list[1].coordinate.lat))
                         + "," + str(speed) + "," + str(score) + "\n")
    fc.write("faster than 400 miles/hour" + str(count))


def fill_zip_hash_table(input_file):
    f = open(input_file, "rU")
    for line in f:
        line = line.split(',')
        lat = round(float(line[0]), 3)
        lng = round(float(line[1]), 3)
        zip_codes.append(Coordinate(lat, lng))
    f.close()


def check_device_id(input_file, output_file):
    count = 0
    count_ex = 0
    f = open(input_file, "rU")
    fw = open(output_file, "w")
    next(f)
    for line in f:
        split_line = line.split(',')
        device_id = str(split_line[2])
        if device_id_to_frequency[device_id] != 0:
            fw.write(str(device_id) + "," + str(device_id_to_frequency[device_id]) + "\n")
            count_ex += 1
        else:
            count += 1
    fw.write("count: " + str(count) + " count_ex: " + str(count_ex))
    f.close()
    fw.close()


def check_zip_dict(output_file1, output_file2):
    fc = open(output_file1, "w")
    fv = open(output_file2, "w")
    for coordinate in good_coordinates:
        if coordinate in zip_codes:
            fc.write(coordinate.lat + "," + coordinate.lng + "\n")
        else:
            fv.write(coordinate.lat + "," + coordinate.lng + "\n")


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


def write_scores_to_file(output_file):
    f = open(output_file, "w")
    sorted_coordinate_count = sorted(coordinate_count_table.items(), key=itemgetter(1), reverse=True)
    for coordinate in sorted_coordinate_count:
        score = float(coordinate_count_table[coordinate[0]]) / float(number_of_values_in_dictionary(
            coordinate_count_table)) * (10 ** 3)
#       print score
        f.write(str(score) + "\n")
        f.write(str(coordinate[0]) + ","+str(coordinate_count_table[coordinate[0]]) + "," + str(score) + "\n")
    f.close()


def write_to_all_files(input_file):
    fill_dictionaries_with_data(input_file)
    # fill_zip_hash_table("zipcode.txt")
    # check_zip_dict("centroid.csv", "valid.csv")
    # check_device_id("device_download.csv", "app_id_info.csv")
    # concurrency("concurrency.csv")
    write_bid_requests_to_file("good_bid_requests.csv", device_id_to_bid_request_table)
    write_bid_requests_to_file("exact_duplicate_bid_requests.csv", exact_duplicate_bid_requests)
    write_coordinates_to_file("invalid_coordinates.csv", invalid_coordinates)
    write_coordinates_to_file("imprecise_coordinates.csv", imprecise_coordinates)
    write_coordinates_to_file("coordinate_frequency.csv", coordinate_count_table)
    write_coordinates_to_file("good_coordinates.csv", good_coordinates)
    write_scores_to_file("good_coordinate_scores.csv")

write_to_all_files("input2")
