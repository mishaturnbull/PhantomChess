# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Math functions that are useful for chess."""

import math
'''
def dist(p1, p2):
    if p1.x == p2.x:
        return abs(p2.y - p1.y)
    else:
        dx = abs(p2.x - p1.x)
        dy = abs(p2.y - p1.y)
        return math.sqrt(dx**2 + dy**2)
'''
def round_down(x, place=1):
    val = math.trunc(x*place) / float(place)
    return int(val) if int(val) == val else val

#def round_up(x):
#    return round_down(x) + 1

if __name__ == '__main__':
    print('=' * 35)
    fmt = 'round_down({}, {:>2}) --> {}'
    for i in xrange(20):
        print(fmt.format(math.pi, i+1, round_down(math.pi, i+1)))
