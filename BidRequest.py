__author__ = 'Ryan'


class BidRequest:
    def __init__(self, id_request, time, lat, lng):
        self.id_request = id_request
        self.time = time
        self.lat = lat
        self.lng = lng
        self.coord = str(lat) + ", " + str(lng)

    def __repr__(self):
        return "id: " + str(self.id_request) + ", coord: " + self.coord

    def __eq__(self, other):
        return isinstance(other, BidRequest) and self.coord == other.coord and self.time == other.time \
            and self.id_request == other.id_request

    def __hash__(self):
        return hash(self.coord)

    def get_id(self):
        return self.id_request

    def get_time(self):
        return self.time

    def get_lat(self):
        return self.lat

    def get_lng(self):
        return self.lng
