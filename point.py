__author__ = 'khn9mc'
from collections import defaultdict
import operator
from decimal import*
from operator import itemgetter

class point:
    def __init__(self, id, lat, lon):
        self.id = id
        self.coord = str(lat) + "," + str(lon)

    def __str__(self):
        return "id: " + str(self.id) + ", coord: " + self.coord

    def __eq__(self, other):
        return isinstance(other, point) and other.coord == self.coord

    def __hash__(self):
        return hash(self.coord)

if __name__ == "__main__":
    Kevin = point(1,2,3)
    print Kevin
    Ngo = point(5,2,3)
    print Kevin == Ngo
    d = defaultdict(int)
    d[Kevin] += 1
    d[Ngo] += 1
    d[point(2,3,3)] += 1
    sorted(d.iteritems(), key=itemgetter(1), reverse=True)
    print d
    dict = defaultdict(list)
    dict[Kevin].append(Kevin)
    dict[Ngo].append(Ngo)
    dict[point(2,3,3)].append(point(2,3,3))
    sorted(dict.iteritems(), key=itemgetter(1), reverse=True)
    print(dict)
    d = Decimal('1.23152')
    print Decimal('1.23152')
    print Decimal('1.23152').as_tuple().exponent
