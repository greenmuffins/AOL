__author__ = 'Ryan'


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
