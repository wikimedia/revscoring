def all_true(func, obs):
    for ob in obs:
        if not func(ob):
            raise AssertionError("{0}({1}) is False, but should be True."
                                 .format(func.__name__, repr(ob)))

def all_false(func, obs):
    for ob in obs:
        if func(ob):
            raise AssertionError("{0}({1}) is True, but should be False."
                                 .format(func.__name__, repr(ob)))
