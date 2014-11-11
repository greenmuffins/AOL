__author__ = 'Ryan'

from collections import defaultdict
from csv import writer
from Helper import parse_line_for_bid_request, distance, number_of_values_in_dictionary
from time import mktime
from operator import itemgetter

coordinate_count_table = defaultdict(int)
device_id_to_bid_request_table = defaultdict(list)

exact_duplicate_bid_requests = []
good_coordinates = []
imprecise_coordinates = []
invalid_coordinates = []


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
    fc.write("user_id,distance,speed,score")
    for user_id in device_id_to_bid_request_table:
        curr_list = device_id_to_bid_request_table[user_id]
        if len(curr_list) > 1:
            for x in range(len(curr_list) - 1):
                t = (curr_list[x].time.year, curr_list[x].time.month, curr_list[x].time.day, curr_list[x].time.hour,
                     curr_list[x].time.minute, curr_list[x].time.second, 1, 1, 0)
                t2 = (curr_list[x+1].time.year, curr_list[x+1].time.month, curr_list[x+1].time.day,
                      curr_list[x+1].time.hour, curr_list[x+1].time.minute, curr_list[x+1].time.second, 2, 1, 0)
                diff_time = mktime(t2)-mktime(t)
                if diff_time == 0:
                    diff_time = 0.01
                speed = distance(curr_list[0].coordinate.lat, curr_list[0].coordinate.lng, curr_list[1].coordinate.lat,
                                 curr_list[1].coordinate.lng) / (diff_time / 3600)
                if speed < 161:
                    score = 1
                elif speed > 644:
                    score = 0
                    count += 1
                else:
                    score = 1 - ((speed - 161) / 483)
                fc.write(str(user_id) + "," + str(distance(curr_list[0].coordinate.lng, curr_list[0].coordinate.lat,
                                                           curr_list[1].coordinate.lng, curr_list[1].coordinate.lat))
                         + "," + str(speed) + "," + str(score) + "\n")
    fc.write("faster than 400 miles/hour" + str(count))


def check_device_id(input_file, output_file):
    count = 0
    count_ex = 0
    f = open(input_file, "rU")
    fw = open(output_file, "w")
    next(f)
    for line in f:
        split_line = line.split(',')
        device_id = str(split_line[2])
        if len(device_id_to_bid_request_table[device_id]) != 0:
            fw.write(str(device_id) + "," + str(len(device_id_to_bid_request_table[device_id])) + "\n")
            count_ex += 1
        else:
            count += 1
    fw.write("count: " + str(count) + " count_ex: " + str(count_ex))
    f.close()
    fw.close()


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


def write_scores_to_file(output_file, data):
    f = open(output_file, "w")
    f.write("freq,lat,lng,score")
    sorted_coordinate_count = sorted(data.items(), key=itemgetter(1), reverse=True)
    denominator = float(number_of_values_in_dictionary(data)) * (10 ** 3)
    for coordinate in sorted_coordinate_count:
        score = 1 - float(data[coordinate[0]]) / denominator
        f.write(str(coordinate[0].lat) + "," + str(coordinate[0].lng) + "," + str(data[coordinate[0]])
                + "," + str(score) + "\n")
    f.close()


def write_to_all_files(input_file):
    fill_dictionaries_with_data(input_file)
    # check_device_id("device_download.csv", "app_id_info.csv")
    # concurrency("concurrency.csv")
    write_bid_requests_to_file("good_bid_requests.csv", device_id_to_bid_request_table)
    write_bid_requests_to_file("exact_duplicate_bid_requests.csv", exact_duplicate_bid_requests)
    write_coordinates_to_file("invalid_coordinates.csv", invalid_coordinates)
    write_coordinates_to_file("imprecise_coordinates.csv", imprecise_coordinates)
    write_coordinates_to_file("coordinate_frequency.csv", coordinate_count_table)
    write_coordinates_to_file("good_coordinates.csv", good_coordinates)
    write_scores_to_file("good_coordinate_scores.csv", coordinate_count_table)

write_to_all_files("input2")

