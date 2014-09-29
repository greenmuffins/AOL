__author__ = 'Kevin'

from collections import defaultdict
import operator
import sys
from point import point
from operator import itemgetter
import decimal
from decimal import*

f = open('testtest','w')
d = {}
x = 0
with open('ogood') as fp:
    for line in fp:
        line = line.split('|')
        ##decimal places, duplicates with same lat, lng, and device-id
        kevin = point(line[1],line[2],line[3])
        if Decimal(line[2]).as_tuple().exponent < -4 and Decimal(line[3]).as_tuple().exponent < -4:
            try:
                d[kevin].append(kevin)
            except KeyError:
                d[kevin] = []
                d[kevin].append(kevin)
        else:
            x += 1

#print '///////////////////////////'
f.write(str(x) + ' number of points with imprecise measurements \n')
d = sorted(d.items(), key=lambda (k,v): len(v), reverse=True)
for ngo in d:
    #ngo = d[x]
    f.write(str(len(ngo[1])) + ': ' + (ngo[1])[0].coord + '\n')
    #print len(listA)
    #for pointA in listA[1]:
        #print pointA
