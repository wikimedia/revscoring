import math

from ..feature import function_applier

abs_builtin = abs


@function_applier
def log(arg, name, returns):
    return math.log, name, returns or float


@function_applier
def exp(arg, name, returns):
    return math.exp, name, returns or float


@function_applier
def abs(arg, name, returns):
    return abs_builtin, name, returns or float
