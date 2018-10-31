#!/usr/bin/env python3
from collections import namedtuple
from enum import Enum

UnitType = Enum('UnitType', 'root unit mult div paren')

UnitSyntaxTree = namedtuple('UnitSyntaxTree', 'type attrs left_child right_child')

Unit = namedtuple('Unit', 'name symbol type si')

# SI Units
AMP      = Unit('ampere',   'A',   'current',     None)
CANDELA  = Unit('candela',  'cd',  'luminosityl', None)
KELVIN   = Unit('kelvin',   'K',   'temperature', None)
KILOGRAM = Unit('kilogram', 'kg',  'mass',        None)
METER    = Unit('meter',    'm',   'length',      None)
MOLE     = Unit('mole',     'mol', 'substance',   None)
SECOND   = Unit('second',   's',   'time',        None)
# The dataset is small enough that it's reasonable to store directly in code.
# If it grows past a certain point it may be better to store in a database.
UNITS = {
        'minute': 
