from ..feature import function_applier

math_min = min
math_max = max


@function_applier
def min(fist_arg, second_arg, *other_args, name=None, returns=float):
    return math_min, name, returns


@function_applier
def max(fist_arg, second_arg, *other_args, name=None, returns=float):
    return math_max, name, returns
