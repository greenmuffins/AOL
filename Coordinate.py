__author__ = 'Ryan'

from decimal import Decimal

class Coordinate:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __repr__(self):
        return "lat: " + str(self.lat) + ", lng: " + str(self.lng)

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.lat == other.lat and self.lng == other.lng

    def __hash__(self):
        return hash((self.lat, self.lng))

    def get_coordinate(self):
        return [self.lat, self.lng]

    def is_valid_coordinate(self):
        return -90.0 <= self.lat <= 90.0 and -180.0 <= self.lng <= 180.0

    def is_precise_enough(self):
        return Decimal(str(self.lat)).as_tuple().exponent <= -4 \
            and Decimal(str(self.lng)).as_tuple().exponent <= -4
