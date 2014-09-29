__author__ = 'Ryan'


class BidRequest:
    def __init__(self, id_request, time, coordinate):
        self.id_request = id_request
        self.time = time
        self.coordinate = coordinate

    def __repr__(self):
        return "id: " + str(self.id_request) + ", coordinate: " + str(self.coordinate) + ", time: " + str(self.time)

    def __eq__(self, other):
        return isinstance(other, BidRequest) and self.id_request == other.id_request and self.time == other.time \
            and self.coordinate == other.coordinate

    def __hash__(self):
        return hash("id: " + str(self.id_request) + ", coordinate: " + str(self.coordinate)
                    + ", time: " + str(self.time))
