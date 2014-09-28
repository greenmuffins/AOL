__author__ = 'Kevin'

from collections import defaultdict
import operator
import sys
from point import point
from operator import itemgetter

d = defaultdict(list)

with open('input2') as fp:
    for line in fp:
        line = line.split('|')
        ##decimal places, duplicates with same lat, lng, and device-id
        kevin = point(line[1],line[2],line[3])
        d[kevin].append(kevin)

sorted(d.items(), key=lambda e: e[1][2])
print d
#sorted(d.iteritems(), key=itemgetter(1), reverse=False)
print d.itervalues().next()



