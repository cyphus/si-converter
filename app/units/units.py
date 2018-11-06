#!/usr/bin/env python3
from collections import namedtuple
from math import pi

Unit = namedtuple('Unit', 'name symbol si_equivalent coefficient')

# The dataset is small enough that it's reasonable to store directly in code.
# If it grows much more, better to serialize to a file as CSV, JSON, etc.
"""
UNITS is a list of units accepted as input to the si_converter
"""
UNITS = [
    Unit('minute', 'min', 's', 60),
    Unit('hour', 'h', 's', 3600),
    Unit('day', 'd', 's', 86400),
    Unit('degree', '°', 'rad', pi / 180),
    # 'minute' the angle has no name to avoid ambiguitiy with the duration
    Unit(None, '‘', 'rad', pi / 10800),
    Unit('second', '“', 'rad', pi / 648000),
    Unit('hectare', 'ha', 'm2', 10000),
    Unit('litre', 'L', 'm3', 0.001),
    Unit('tonne', 't', 'kg', 10000),
]
