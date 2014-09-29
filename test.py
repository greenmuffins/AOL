__author__ = 'Kevin'

from collections import defaultdict
import operator
import sys
from point import point
from operator import itemgetter

d = {}

with open('input') as fp:
    for line in fp:
        line = line.split('|')
        ##decimal places, duplicates with same lat, lng, and device-id
        kevin = point(line[1],line[2],line[3])
        try:
            d[kevin].append(kevin)
        except KeyError:
            d[kevin] = []
            d[kevin].append(kevin)

print '///////////////////////////'
d = sorted(d.items(), key=lambda (k,v): len(v), reverse=True)
for x in range(0,5):
    ngo = d[x]
    print len(ngo[1])
    #print len(listA)
    #for pointA in listA[1]:
        #print pointA
